import { describe, expect, it } from "vitest";
import Database from "better-sqlite3";
import { instante, type HallazgoId, type Positivo, type RepositorioId, type RevisionId, type UsuarioId, type Email, type Texto } from "@centinela/kernel";
import type { HashClave, HashToken, Usuario } from "@centinela/identidad";
import type { NombreRepo, Repositorio, SecretoWebhook } from "@centinela/repositorios";
import type { Hallazgo, Huella, Revision } from "@centinela/revisiones";
import { abrirAlmacen, FilaCorrupta } from "./index";
import { mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const U: Usuario = { id: "00000000-0000-4000-8000-000000000001" as UsuarioId, email: "a@b.co" as Email, nombre: "Ana" as Texto, rol: "administrador", hashClave: "scrypt$x$y" as HashClave, estado: "Activo", creadoEn: instante(10) };
const R: Repositorio = { id: "00000000-0000-4000-8000-0000000000a1" as RepositorioId, nombre: "ucsm/demo" as NombreRepo, politica: "Possibly", bloquearMerge: true, secretoWebhook: "s" as SecretoWebhook, activo: true, conectadoPor: U.id, conectadoEn: instante(11) };
const V = (id: string, sha: string, estado: Revision["estado"], creadaEn = 12): Revision => ({
  id: id as RevisionId,
  repositorioId: R.id,
  pr: { numero: 7 as Positivo, titulo: "T", autor: "ana", shaCabeza: sha },
  origen: "manual",
  solicitadaPor: U.id,
  creadaEn: instante(creadaEn),
  intentos: 1,
  estado,
});
const H: Hallazgo = {
  id: "00000000-0000-4000-8000-0000000000e1" as HallazgoId,
  revisionId: "00000000-0000-4000-8000-0000000000c1" as RevisionId,
  archivo: "src/a.cpp",
  linea: 11 as Positivo,
  columna: 3 as Positivo,
  clase: "Confirmado",
  mensaje: "m",
  ruta: [{ archivo: "src/a.cpp", linea: 9 as Positivo, mensaje: "obtiene" }],
  huella: "abcd1234" as Huella,
  clasificacion: "SinRevisar",
  clasificadoPor: null,
};

function conDatos() {
  const a = abrirAlmacen(":memory:");
  a.usuarios.guardar(U);
  a.repositorios.guardar(R);
  return a;
}

describe("almacén SQLite", () => {
  it("guarda y lee cada agregado sin perder nada", () => {
    const a = conDatos();
    expect(a.usuarios.porId(U.id)).toEqual(U);
    expect(a.usuarios.porEmail(U.email)).toEqual(U);
    expect(a.repositorios.porNombre(R.nombre)).toEqual(R);
    const s = { tokenHash: "t" as HashToken, usuarioId: U.id, creada: instante(1), expira: instante(2) };
    a.sesiones.guardar(s);
    expect(a.sesiones.porHash(s.tokenHash)).toEqual(s);
    a.sesiones.borrarDeUsuario(U.id);
    expect(a.sesiones.porHash(s.tokenHash)).toBeUndefined();
  });

  it("cada estado de la revisión se guarda y se recupera igual", () => {
    const a = conDatos();
    const estados: Revision["estado"][] = [
      { tipo: "Pendiente", encoladaEn: instante(1) },
      { tipo: "EnAnalisis", iniciadaEn: instante(2) },
      { tipo: "Fallida", terminadaEn: instante(3), motivo: "x" },
      { tipo: "Publicada", terminadaEn: instante(4), veredicto: "ConProblemas", resumen: { archivosAnalizados: 2, noCompilados: 1, confirmados: 1, posibles: 0, suprimidos: 1 } },
    ];
    const id = "00000000-0000-4000-8000-0000000000c1";
    for (const e of estados) {
      a.revisiones.guardar(V(id, "abc", e));
      expect(a.revisiones.porId(id as RevisionId)?.estado).toEqual(e);
    }
    expect(a.revisiones.delSha(R.id, 7 as Positivo, "abc")?.id).toBe(id);
  });

  it("hallazgos, ruta incluida, y su reemplazo por revisión", () => {
    const a = conDatos();
    a.revisiones.guardar(V(H.revisionId, "abc", { tipo: "EnAnalisis", iniciadaEn: instante(1) }));
    a.hallazgos.reemplazar(H.revisionId, [H]);
    expect(a.hallazgos.deRevision(H.revisionId)).toEqual([H]);
    const marcado: Hallazgo = { ...H, clasificacion: "FalsoPositivo", clasificadoPor: { por: U.id, en: instante(50) } };
    a.hallazgos.guardar(marcado);
    expect(a.hallazgos.porId(H.id)).toEqual(marcado);
    a.hallazgos.reemplazar(H.revisionId, []);
    expect(a.hallazgos.deRevision(H.revisionId)).toEqual([]);
  });

  it("la base no admite dos revisiones del mismo sha de un PR", () => {
    const a = conDatos();
    a.revisiones.guardar(V("00000000-0000-4000-8000-0000000000c1", "abc", { tipo: "Pendiente", encoladaEn: instante(1) }));
    expect(() => a.revisiones.guardar(V("00000000-0000-4000-8000-0000000000c2", "abc", { tipo: "Pendiente", encoladaEn: instante(1) }))).toThrow(/UNIQUE/);
  });

  it("la cola entrega en orden y no entrega dos veces lo tomado", () => {
    const a = conDatos();
    for (const [i, sha] of ["a", "b"].entries()) {
      const id = `00000000-0000-4000-8000-00000000000${i}` as RevisionId;
      a.revisiones.guardar(V(id, sha, { tipo: "Pendiente", encoladaEn: instante(1) }));
      a.trabajos.encolar(id, instante(100 + i));
    }
    expect(a.trabajos.tomar()).toBe("00000000-0000-4000-8000-000000000000");
    expect(a.trabajos.tomar()).toBe("00000000-0000-4000-8000-000000000001");
    expect(a.trabajos.tomar()).toBeUndefined();
  });

  it("los descartes son por repositorio", () => {
    const a = conDatos();
    a.descartes.agregar(R.id, "h1" as Huella, U.id, instante(1));
    a.descartes.agregar(R.id, "h1" as Huella, U.id, instante(2));
    expect([...a.descartes.deRepositorio(R.id)]).toEqual(["h1"]);
    a.descartes.quitar(R.id, "h1" as Huella);
    expect(a.descartes.deRepositorio(R.id).size).toBe(0);
  });

  it("una transacción que lanza no deja nada escrito", () => {
    const a = abrirAlmacen(":memory:");
    expect(() =>
      a.transaccion(() => {
        a.usuarios.guardar(U);
        throw new Error("falla a mitad");
      }),
    ).toThrow();
    expect(a.usuarios.contar()).toBe(0);
  });

  it("la base no admite un autor de la clasificación sin fecha", () => {
    const a = conDatos();
    a.revisiones.guardar(V(H.revisionId, "abc", { tipo: "EnAnalisis", iniciadaEn: instante(1) }));
    expect(() => a.hallazgos.guardar({ ...H, clasificadoPor: { por: U.id, en: null as never } })).toThrow(/CHECK/);
  });

  it("una base de la versión 1 se migra al abrirla (v2: activos siguen activos, inactivos quedan pendientes; v3: índice por fecha)", () => {
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
      expect(despues.pragma("user_version", { simple: true })).toBe(3);
      expect(despues.pragma("foreign_key_check")).toEqual([]);
      // v3: la lista general recorre el índice por fecha y no ordena la tabla (prueba de volumen, capítulo 8).
      const plan = (despues.prepare("EXPLAIN QUERY PLAN SELECT * FROM revisiones ORDER BY creada_en DESC, rowid DESC LIMIT 200").all() as { detail: string }[]).map((f) => f.detail).join(" | ");
      expect(plan).toContain("revisiones_creada");
      expect(plan).not.toContain("TEMP B-TREE FOR ORDER BY"); // solo desempata la misma fecha, no ordena todo
      despues.close();
      abrirAlmacen(ruta).cerrar(); // abrirla otra vez no vuelve a migrar
    } finally {
      rmSync(dir, { recursive: true });
    }
  });

  it("una base de una versión más nueva que el binario no se abre", () => {
    const dir = mkdtempSync(join(tmpdir(), "centinela-"));
    try {
      const ruta = join(dir, "v9.db");
      const db = new Database(ruta);
      db.pragma("user_version = 9");
      db.close();
      expect(() => abrirAlmacen(ruta)).toThrow(/versión 9/);
    } finally {
      rmSync(dir, { recursive: true });
    }
  });

  it("una fila que el dominio no admite es un error, no un valor a medias", () => {
    const dir = mkdtempSync(join(tmpdir(), "centinela-"));
    try {
      const ruta = join(dir, "c.db");
      abrirAlmacen(ruta).cerrar();
      const db = new Database(ruta);
      db.prepare("INSERT INTO usuarios VALUES ('no-es-uuid', 'a@b.co', 'A', 'administrador', 'h', 'Activo', 0)").run();
      db.close();
      const a = abrirAlmacen(ruta);
      expect(() => a.usuarios.listar()).toThrow(FilaCorrupta);
      a.cerrar();
    } finally {
      rmSync(dir, { recursive: true });
    }
  });
});
