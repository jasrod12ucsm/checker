# Base de datos

La construcción de la base (análisis, diseño conceptual, lógico y físico,
implementación, pruebas y despliegue) está en la
[sección 7.2](../construccion/7-2-datos.md). Aquí está el esquema entero.

![Modelo entidad-relación](../diagramas/sistema-er.svg)

[`sistema/paquetes/adaptadores/sqlite/src/esquema.sql:1`](https://github.com/jasrod12ucsm/checker/blob/main/sistema/paquetes/adaptadores/sqlite/src/esquema.sql#L1-L89)

```sql
-- Esquema de Centinela C++ (versión 2). Cada tabla es un agregado del dominio.
-- Una base creada con una versión anterior se actualiza con migraciones.sql al abrirla.
CREATE TABLE usuarios (
  id          TEXT PRIMARY KEY,
  email       TEXT NOT NULL UNIQUE,
  nombre      TEXT NOT NULL,
  rol         TEXT NOT NULL CHECK (rol IN ('administrador', 'desarrollador')),
  hash_clave  TEXT NOT NULL,
  estado      TEXT NOT NULL CHECK (estado IN ('Pendiente', 'Activo', 'Desactivado')),
  creado_en   INTEGER NOT NULL
);

CREATE TABLE sesiones (
  token_hash  TEXT PRIMARY KEY,
  usuario_id  TEXT NOT NULL REFERENCES usuarios(id),
  creada      INTEGER NOT NULL,
  expira      INTEGER NOT NULL
);
CREATE INDEX sesiones_usuario ON sesiones(usuario_id);

CREATE TABLE repositorios (
  id               TEXT PRIMARY KEY,
  nombre           TEXT NOT NULL UNIQUE,
  politica         TEXT NOT NULL CHECK (politica IN ('Silent', 'Possibly')),
  bloquear_merge   INTEGER NOT NULL CHECK (bloquear_merge IN (0, 1)),
  secreto_webhook  TEXT NOT NULL,
  activo           INTEGER NOT NULL CHECK (activo IN (0, 1)),
  conectado_por    TEXT NOT NULL REFERENCES usuarios(id),
  conectado_en     INTEGER NOT NULL
);

-- El estado se guarda aplanado: `estado` dice la variante y solo sus columnas tienen valor.
CREATE TABLE revisiones (
  id              TEXT PRIMARY KEY,
  repositorio_id  TEXT NOT NULL REFERENCES repositorios(id),
  numero_pr       INTEGER NOT NULL CHECK (numero_pr > 0),
  titulo          TEXT NOT NULL,
  autor           TEXT NOT NULL,
  sha_cabeza      TEXT NOT NULL,
  origen          TEXT NOT NULL CHECK (origen IN ('webhook', 'manual')),
  solicitada_por  TEXT REFERENCES usuarios(id),
  creada_en       INTEGER NOT NULL,
  intentos        INTEGER NOT NULL CHECK (intentos >= 1),
  estado          TEXT NOT NULL CHECK (estado IN ('Pendiente', 'EnAnalisis', 'Publicada', 'Fallida')),
  desde           INTEGER NOT NULL,
  veredicto       TEXT CHECK (veredicto IN ('Aprobada', 'ConProblemas')),
  archivos        INTEGER,
  no_compilados   INTEGER,
  confirmados     INTEGER,
  posibles        INTEGER,
  suprimidos      INTEGER,
  motivo          TEXT,
  UNIQUE (repositorio_id, numero_pr, sha_cabeza),
  CHECK ((estado = 'Publicada') = (veredicto IS NOT NULL)),
  CHECK ((estado = 'Fallida') = (motivo IS NOT NULL))
);
CREATE INDEX revisiones_repo ON revisiones(repositorio_id, creada_en DESC);

CREATE TABLE hallazgos (
  id             TEXT PRIMARY KEY,
  revision_id    TEXT NOT NULL REFERENCES revisiones(id) ON DELETE CASCADE,
  archivo        TEXT NOT NULL,
  linea          INTEGER NOT NULL CHECK (linea > 0),
  columna        INTEGER NOT NULL CHECK (columna > 0),
  clase          TEXT NOT NULL CHECK (clase IN ('Confirmado', 'Posible')),
  mensaje        TEXT NOT NULL,
  ruta           TEXT NOT NULL,           -- JSON: [{archivo, linea, mensaje}]
  huella         TEXT NOT NULL,
  clasificacion  TEXT NOT NULL CHECK (clasificacion IN ('SinRevisar', 'Confirmado', 'FalsoPositivo')),
  clasificado_por TEXT REFERENCES usuarios(id),
  clasificado_en  INTEGER,
  CHECK ((clasificado_por IS NULL) = (clasificado_en IS NULL))
);
CREATE INDEX hallazgos_revision ON hallazgos(revision_id);

CREATE TABLE descartes (
  repositorio_id  TEXT NOT NULL REFERENCES repositorios(id),
  huella          TEXT NOT NULL,
  por             TEXT NOT NULL REFERENCES usuarios(id),
  en              INTEGER NOT NULL,
  PRIMARY KEY (repositorio_id, huella)
);

-- Cola de trabajos: se escribe en la misma transacción que la revisión.
CREATE TABLE trabajos (
  revision_id  TEXT PRIMARY KEY REFERENCES revisiones(id),
  encolado_en  INTEGER NOT NULL,
  tomado       INTEGER NOT NULL DEFAULT 0 CHECK (tomado IN (0, 1))
);
```

## Versiones del esquema y migraciones

La versión del esquema se guarda en `PRAGMA user_version`. Una base nueva se
crea directamente en la versión actual (2). Una base de una versión anterior se
actualiza sola al abrirla: `abrirAlmacen` corre los bloques de
`migraciones.sql` que le faltan, en una sola transacción, y verifica las claves
foráneas antes de confirmar. Una base de una versión más nueva que el binario
no se abre.

| Versión | Cambio |
|---|---|
| 1 | esquema inicial; la cuenta tenía `activo` (0 o 1) |
| 2 | `usuarios.estado` (`Pendiente`, `Activo`, `Desactivado`) en lugar de `activo`; `hallazgos.clasificado_por` y `clasificado_en`. Una cuenta inactiva de la versión 1 queda `Pendiente`, porque la versión 1 no distinguía un registro sin aprobar de una baja |

[`sistema/paquetes/adaptadores/sqlite/src/migraciones.sql:1`](https://github.com/jasrod12ucsm/checker/blob/main/sistema/paquetes/adaptadores/sqlite/src/migraciones.sql#L1-L21)

```sql
-- Migraciones del esquema. Cada bloque lleva una base de la versión N a la N+1;
-- `abrirAlmacen` corre, en una transacción, los bloques que le faltan a la base.

-- @version 2: estado de la cuenta (Pendiente | Activo | Desactivado) y autoría de la clasificación.
-- En la versión 1 una cuenta inactiva podía ser un registro sin aprobar o una baja: no hay
-- cómo distinguirlas, así que queda Pendiente y un administrador la aprueba o la rechaza.
CREATE TABLE usuarios_v2 (
  id          TEXT PRIMARY KEY,
  email       TEXT NOT NULL UNIQUE,
  nombre      TEXT NOT NULL,
  rol         TEXT NOT NULL CHECK (rol IN ('administrador', 'desarrollador')),
  hash_clave  TEXT NOT NULL,
  estado      TEXT NOT NULL CHECK (estado IN ('Pendiente', 'Activo', 'Desactivado')),
  creado_en   INTEGER NOT NULL
);
INSERT INTO usuarios_v2 (id, email, nombre, rol, hash_clave, estado, creado_en)
  SELECT id, email, nombre, rol, hash_clave, CASE activo WHEN 1 THEN 'Activo' ELSE 'Pendiente' END, creado_en FROM usuarios;
DROP TABLE usuarios;
ALTER TABLE usuarios_v2 RENAME TO usuarios;
ALTER TABLE hallazgos ADD COLUMN clasificado_por TEXT REFERENCES usuarios(id);
ALTER TABLE hallazgos ADD COLUMN clasificado_en INTEGER CHECK ((clasificado_por IS NULL) = (clasificado_en IS NULL));
```

[`sistema/paquetes/adaptadores/sqlite/src/almacen.ts:22`](https://github.com/jasrod12ucsm/checker/blob/main/sistema/paquetes/adaptadores/sqlite/src/almacen.ts#L22-L35)

```typescript
function migrar(db: Database.Database, desde: number) {
  db.pragma("foreign_keys = OFF");
  db.transaction(() => {
    for (let v = desde + 1; v <= VERSION; v++) {
      const sql = MIGRACIONES.get(v);
      if (sql === undefined) throw new Error(`falta la migración a la versión ${v} del esquema`);
      db.exec(sql);
    }
    const rotas = db.pragma("foreign_key_check") as unknown[];
    if (rotas.length > 0) throw new Error(`la migración dejó ${rotas.length} claves foráneas rotas`);
    db.pragma(`user_version = ${VERSION}`);
  })();
  db.pragma("foreign_keys = ON");
}
```

[`sistema/paquetes/adaptadores/sqlite/src/almacen.test.ts:130`](https://github.com/jasrod12ucsm/checker/blob/main/sistema/paquetes/adaptadores/sqlite/src/almacen.test.ts#L130-L157)

```typescript
  it("una base de la versión 1 se migra al abrirla: activos siguen activos, inactivos quedan pendientes", () => {
    const dir = mkdtempSync(join(tmpdir(), "centinela-"));
    try {
      const ruta = join(dir, "v1.db");
      const db = new Database(ruta);
      db.exec(readFileSync(new URL("./fixtures/esquema-v1.sql", import.meta.url), "utf8"));
      db.pragma("user_version = 1");
      const ins = db.prepare("INSERT INTO usuarios VALUES (?, ?, 'N', ?, 'h', ?, 0)");
      ins.run(U.id, "a@b.co", "administrador", 1);
      ins.run("00000000-0000-4000-8000-000000000002", "d@b.co", "desarrollador", 0);
      db.prepare("INSERT INTO repositorios VALUES (?, 'ucsm/demo', 'Silent', 0, 's', 1, ?, 0)").run(R.id, U.id);
      db.prepare("INSERT INTO revisiones (id, repositorio_id, numero_pr, titulo, autor, sha_cabeza, origen, creada_en, intentos, estado, desde) VALUES (?, ?, 7, 'T', 'a', 'abc', 'webhook', 0, 1, 'Pendiente', 0)").run(H.revisionId, R.id);
      db.prepare("INSERT INTO hallazgos VALUES (?, ?, 'src/a.cpp', 11, 3, 'Confirmado', 'm', '[]', 'abcd1234', 'Confirmado')").run(H.id, H.revisionId);
      db.close();

      const a = abrirAlmacen(ruta);
      expect(a.usuarios.listar().map((u) => u.estado)).toEqual(["Activo", "Pendiente"]);
      expect(a.hallazgos.porId(H.id)).toMatchObject({ clasificacion: "Confirmado", clasificadoPor: null });
      a.cerrar();
      const despues = new Database(ruta);
      expect(despues.pragma("user_version", { simple: true })).toBe(2);
      expect(despues.pragma("foreign_key_check")).toEqual([]);
      despues.close();
      abrirAlmacen(ruta).cerrar(); // abrirla otra vez no vuelve a migrar
    } finally {
      rmSync(dir, { recursive: true });
    }
  });
```
