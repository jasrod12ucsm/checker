import { readFileSync } from "node:fs";
import Database from "better-sqlite3";
import type { Hallazgo, Huella } from "@centinela/revisiones";
import type { Almacen } from "@centinela/producto";
import { aHallazgo, aRepositorio, aRevision, aSesion, aUsuario, deRevision } from "./filas";

const ESQUEMA = readFileSync(new URL("./esquema.sql", import.meta.url), "utf8");
const VERSION = 2;

/** Bloques de migraciones.sql por versión de destino: el bloque N lleva una base de N-1 a N. */
const MIGRACIONES = new Map(
  readFileSync(new URL("./migraciones.sql", import.meta.url), "utf8")
    .split(/^-- @version /m)
    .slice(1)
    .map((b) => [Number.parseInt(b, 10), `-- versión ${b}`] as const),
);

/**
 * Lleva una base vieja a la versión actual en una sola transacción. Las claves foráneas se
 * apagan mientras se reconstruyen tablas (así lo pide SQLite) y se verifican al final.
 */
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

/** Abre (o crea) la base. `":memory:"` para pruebas. */
export function abrirAlmacen(ruta: string): Almacen & { cerrar(): void } {
  const db = new Database(ruta);
  db.pragma("journal_mode = WAL");
  db.pragma("foreign_keys = ON");
  db.pragma("busy_timeout = 5000");
  const version = db.pragma("user_version", { simple: true }) as number;
  if (version === 0) {
    db.exec(ESQUEMA);
    db.pragma(`user_version = ${VERSION}`);
  } else if (version < VERSION) {
    migrar(db, version);
  } else if (version > VERSION) {
    throw new Error(`la base está en la versión ${version} del esquema y este binario espera la ${VERSION}`);
  }

  const q = <P extends unknown[] = unknown[]>(sql: string) => {
    const s = db.prepare<P>(sql);
    return { uno: (...p: P) => s.get(...p), todos: (...p: P) => s.all(...p), correr: (...p: P) => s.run(...p) };
  };

  const u = {
    porId: q("SELECT * FROM usuarios WHERE id = ?"),
    porEmail: q("SELECT * FROM usuarios WHERE email = ?"),
    contar: q("SELECT count(*) AS n FROM usuarios"),
    listar: q("SELECT * FROM usuarios ORDER BY creado_en"),
    guardar: q(`INSERT INTO usuarios (id, email, nombre, rol, hash_clave, estado, creado_en)
                VALUES (@id, @email, @nombre, @rol, @hash_clave, @estado, @creado_en)
                ON CONFLICT(id) DO UPDATE SET email = excluded.email, nombre = excluded.nombre, rol = excluded.rol,
                  hash_clave = excluded.hash_clave, estado = excluded.estado`),
  };
  const s = {
    porHash: q("SELECT * FROM sesiones WHERE token_hash = ?"),
    guardar: q("INSERT OR REPLACE INTO sesiones (token_hash, usuario_id, creada, expira) VALUES (?, ?, ?, ?)"),
    borrar: q("DELETE FROM sesiones WHERE token_hash = ?"),
    borrarDeUsuario: q("DELETE FROM sesiones WHERE usuario_id = ?"),
  };
  const r = {
    porId: q("SELECT * FROM repositorios WHERE id = ?"),
    porNombre: q("SELECT * FROM repositorios WHERE nombre = ?"),
    listar: q("SELECT * FROM repositorios ORDER BY nombre"),
    guardar: q(`INSERT INTO repositorios (id, nombre, politica, bloquear_merge, secreto_webhook, activo, conectado_por, conectado_en)
                VALUES (@id, @nombre, @politica, @bloquear_merge, @secreto_webhook, @activo, @conectado_por, @conectado_en)
                ON CONFLICT(id) DO UPDATE SET politica = excluded.politica, bloquear_merge = excluded.bloquear_merge,
                  secreto_webhook = excluded.secreto_webhook, activo = excluded.activo,
                  conectado_por = excluded.conectado_por, conectado_en = excluded.conectado_en`),
  };
  const v = {
    porId: q("SELECT * FROM revisiones WHERE id = ?"),
    delSha: q("SELECT * FROM revisiones WHERE repositorio_id = ? AND numero_pr = ? AND sha_cabeza = ?"),
    listar: q("SELECT * FROM revisiones ORDER BY creada_en DESC, rowid DESC LIMIT ?"),
    listarDe: q("SELECT * FROM revisiones WHERE repositorio_id = ? ORDER BY creada_en DESC, rowid DESC LIMIT ?"),
    enAnalisis: q("SELECT * FROM revisiones WHERE estado = 'EnAnalisis'"),
    guardar: q(`INSERT INTO revisiones (id, repositorio_id, numero_pr, titulo, autor, sha_cabeza, origen, solicitada_por, creada_en,
                  intentos, estado, desde, veredicto, archivos, no_compilados, confirmados, posibles, suprimidos, motivo)
                VALUES (@id, @repositorio_id, @numero_pr, @titulo, @autor, @sha_cabeza, @origen, @solicitada_por, @creada_en,
                  @intentos, @estado, @desde, @veredicto, @archivos, @no_compilados, @confirmados, @posibles, @suprimidos, @motivo)
                ON CONFLICT(id) DO UPDATE SET intentos = excluded.intentos, estado = excluded.estado, desde = excluded.desde,
                  veredicto = excluded.veredicto, archivos = excluded.archivos, no_compilados = excluded.no_compilados, confirmados = excluded.confirmados,
                  posibles = excluded.posibles, suprimidos = excluded.suprimidos, motivo = excluded.motivo`),
  };
  const h = {
    porId: q("SELECT * FROM hallazgos WHERE id = ?"),
    deRevision: q("SELECT * FROM hallazgos WHERE revision_id = ? ORDER BY archivo, linea, columna"),
    borrarDe: q("DELETE FROM hallazgos WHERE revision_id = ?"),
    guardar: q(`INSERT INTO hallazgos (id, revision_id, archivo, linea, columna, clase, mensaje, ruta, huella, clasificacion,
                  clasificado_por, clasificado_en)
                VALUES (@id, @revision_id, @archivo, @linea, @columna, @clase, @mensaje, @ruta, @huella, @clasificacion,
                  @clasificado_por, @clasificado_en)
                ON CONFLICT(id) DO UPDATE SET clasificacion = excluded.clasificacion,
                  clasificado_por = excluded.clasificado_por, clasificado_en = excluded.clasificado_en`),
  };
  const d = {
    de: q("SELECT huella FROM descartes WHERE repositorio_id = ?"),
    agregar: q("INSERT OR IGNORE INTO descartes (repositorio_id, huella, por, en) VALUES (?, ?, ?, ?)"),
    quitar: q("DELETE FROM descartes WHERE repositorio_id = ? AND huella = ?"),
  };
  const t = {
    encolar: q("INSERT INTO trabajos (revision_id, encolado_en) VALUES (?, ?) ON CONFLICT(revision_id) DO UPDATE SET tomado = 0, encolado_en = excluded.encolado_en"),
    tomar: q("UPDATE trabajos SET tomado = 1 WHERE revision_id = (SELECT revision_id FROM trabajos WHERE tomado = 0 ORDER BY encolado_en LIMIT 1) RETURNING revision_id"),
    terminar: q("DELETE FROM trabajos WHERE revision_id = ?"),
  };

  const opcional = <T>(f: (x: unknown) => T, fila: unknown) => (fila === undefined ? undefined : f(fila));
  const b = (x: boolean) => (x ? 1 : 0);

  return {
    usuarios: {
      porId: (id) => opcional(aUsuario, u.porId.uno(id)),
      porEmail: (e) => opcional(aUsuario, u.porEmail.uno(e)),
      contar: () => (u.contar.uno() as { n: number }).n,
      listar: () => u.listar.todos().map(aUsuario),
      guardar: (x) =>
        void u.guardar.correr({ id: x.id, email: x.email, nombre: x.nombre, rol: x.rol, hash_clave: x.hashClave, estado: x.estado, creado_en: x.creadoEn }),
    },
    sesiones: {
      porHash: (hh) => opcional(aSesion, s.porHash.uno(hh)),
      guardar: (x) => void s.guardar.correr(x.tokenHash, x.usuarioId, x.creada, x.expira),
      borrar: (hh) => void s.borrar.correr(hh),
      borrarDeUsuario: (id) => void s.borrarDeUsuario.correr(id),
    },
    repositorios: {
      porId: (id) => opcional(aRepositorio, r.porId.uno(id)),
      porNombre: (n) => opcional(aRepositorio, r.porNombre.uno(n)),
      listar: () => r.listar.todos().map(aRepositorio),
      guardar: (x) =>
        void r.guardar.correr({
          id: x.id,
          nombre: x.nombre,
          politica: x.politica,
          bloquear_merge: b(x.bloquearMerge),
          secreto_webhook: x.secretoWebhook,
          activo: b(x.activo),
          conectado_por: x.conectadoPor,
          conectado_en: x.conectadoEn,
        }),
    },
    revisiones: {
      porId: (id) => opcional(aRevision, v.porId.uno(id)),
      delSha: (repo, n, sha) => opcional(aRevision, v.delSha.uno(repo, n, sha)),
      listar: (f) => (f.repositorioId === undefined ? v.listar.todos(f.limite) : v.listarDe.todos(f.repositorioId, f.limite)).map(aRevision),
      enAnalisis: () => v.enAnalisis.todos().map(aRevision),
      guardar: (x) => void v.guardar.correr(deRevision(x)),
    },
    hallazgos: {
      porId: (id) => opcional(aHallazgo, h.porId.uno(id)),
      deRevision: (id) => h.deRevision.todos(id).map(aHallazgo),
      reemplazar: (id, hs) => {
        h.borrarDe.correr(id);
        for (const x of hs) h.guardar.correr(filaHallazgo(x));
      },
      guardar: (x) => void h.guardar.correr(filaHallazgo(x)),
    },
    descartes: {
      deRepositorio: (id) => new Set(d.de.todos(id).map((f) => (f as { huella: Huella }).huella)),
      agregar: (id, hh, por, en) => void d.agregar.correr(id, hh, por, en),
      quitar: (id, hh) => void d.quitar.correr(id, hh),
    },
    trabajos: {
      encolar: (id, en) => void t.encolar.correr(id, en),
      tomar: () => (t.tomar.uno() as { revision_id: never } | undefined)?.revision_id,
      terminar: (id) => void t.terminar.correr(id),
    },
    transaccion: (f) => db.transaction(f)(),
    cerrar: () => db.close(),
  };
}

function filaHallazgo(x: Hallazgo) {
  return {
    id: x.id,
    revision_id: x.revisionId,
    archivo: x.archivo,
    linea: x.linea,
    columna: x.columna,
    clase: x.clase,
    mensaje: x.mensaje,
    ruta: JSON.stringify(x.ruta),
    huella: x.huella,
    clasificacion: x.clasificacion,
    clasificado_por: x.clasificadoPor?.por ?? null,
    clasificado_en: x.clasificadoPor?.en ?? null,
  };
}
