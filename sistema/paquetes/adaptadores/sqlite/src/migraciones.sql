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

-- @version 3: índice para la lista general de revisiones. Sin él, con 20 000 revisiones cada
-- consulta ordenaba la tabla entera (prueba de volumen, capítulo 8): 55 consultas/s; con él, 889 (sistema/no-funcionales/resultados/volumen.json).
CREATE INDEX revisiones_creada ON revisiones(creada_en DESC);
