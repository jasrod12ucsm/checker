import { describe, expect, it } from "vitest";
import { desenvolver, instante, type Email, type HallazgoId, type Positivo, type RepositorioId, type RevisionId, type Texto, type UsuarioId } from "@centinela/kernel";
import { Autorizado, type HashClave } from "@centinela/identidad";
import type { NombreRepo, Repositorio, SecretoWebhook } from "@centinela/repositorios";
import {
  clasificar,
  comentario,
  cuerpo,
  estadoCommit,
  fallar,
  huella,
  iniciar,
  publicar,
  reintentar,
  solicitar,
  type Aviso,
  type Huella,
  type Revision,
} from "./index";

const dev = { id: "00000000-0000-4000-8000-000000000001" as UsuarioId, email: "d@b.co" as Email, nombre: "D" as Texto, rol: "desarrollador" as const, hashClave: "h" as HashClave, estado: "Activo" as const, creadoEn: instante(0) };
const repo: Repositorio = { id: "00000000-0000-4000-8000-0000000000a1" as RepositorioId, nombre: "ucsm/demo" as NombreRepo, politica: "Possibly", bloquearMerge: true, secretoWebhook: "s" as SecretoWebhook, activo: true, conectadoPor: dev.id, conectadoEn: instante(0) };
const pr = { numero: 7 as Positivo, titulo: "Agrega caché", autor: "ana", shaCabeza: "abc123" };
const sol = { id: "00000000-0000-4000-8000-0000000000c1" as RevisionId, pr, origen: "webhook" as const, solicitadaPor: null };
const aviso = (linea: number, clase: Aviso["clase"] = "Confirmado", archivo = "src/a.cpp"): Aviso => ({
  archivo,
  linea: linea as Positivo,
  columna: 3 as Positivo,
  clase,
  mensaje: `Uso de una referencia invalidada: 'std::vector::clear' (línea ${linea - 1}) lo invalidó`,
  ruta: [{ archivo, linea: (linea - 2) as Positivo, mensaje: "El handle al elemento se obtiene de 'std::vector::operator[]'" }],
});
let n = 0;
const ids = () => `00000000-0000-4000-8000-${String(++n).padStart(12, "0")}` as HallazgoId;
const enAnalisis = () => iniciar(desenvolver(solicitar(repo, undefined, sol, instante(1))), instante(2));

describe("solicitar", () => {
  it("crea una revisión pendiente del sha de cabeza", () => {
    expect(solicitar(repo, undefined, sol, instante(1))).toMatchObject({ ok: true, valor: { estado: { tipo: "Pendiente" }, intentos: 1, repositorioId: repo.id } });
  });
  it("un sha no se revisa dos veces", () => {
    const p = desenvolver(solicitar(repo, undefined, sol, instante(1)));
    expect(solicitar(repo, p, sol, instante(2))).toEqual({ ok: false, error: { tipo: "RevisionEnCurso" } });
    const pub = publicar(iniciar(p, instante(2)), { analizados: 1, noCompilados: [], avisos: [] }, new Set(), ids, instante(3)).revision;
    expect(solicitar(repo, pub, sol, instante(4))).toEqual({ ok: false, error: { tipo: "ShaYaRevisado", estado: "Publicada" } });
  });
  it("un repositorio desconectado no se revisa", () => {
    expect(solicitar({ ...repo, activo: false }, undefined, sol, instante(1))).toEqual({ ok: false, error: { tipo: "RepositorioDesconectado" } });
  });
});

describe("publicar", () => {
  it("sin avisos la revisión queda aprobada", () => {
    const p = publicar(enAnalisis(), { analizados: 3, noCompilados: [], avisos: [] }, new Set(), ids, instante(3));
    expect(p.revision.estado).toMatchObject({ tipo: "Publicada", veredicto: "Aprobada", resumen: { archivosAnalizados: 3, confirmados: 0 } });
  });
  it("cuenta confirmados y posibles y descarta avisos repetidos", () => {
    const p = publicar(enAnalisis(), { analizados: 1, noCompilados: [], avisos: [aviso(10), aviso(10), aviso(20, "Posible")] }, new Set(), ids, instante(3));
    expect(p.hallazgos).toHaveLength(2);
    expect(p.revision.estado).toMatchObject({ veredicto: "ConProblemas", resumen: { confirmados: 1, posibles: 1, suprimidos: 0 } });
  });
  it("una huella descartada nace como falso positivo y no cuenta para el veredicto", () => {
    const d = new Set<Huella>([huella(aviso(10))]);
    const p = publicar(enAnalisis(), { analizados: 1, noCompilados: [], avisos: [aviso(10)] }, d, ids, instante(3));
    expect(p.hallazgos[0]?.clasificacion).toBe("FalsoPositivo");
    expect(p.revision.estado).toMatchObject({ veredicto: "Aprobada", resumen: { suprimidos: 1, confirmados: 0 } });
  });
});

describe("huella", () => {
  it("no depende de los números de línea del mensaje (el mismo problema tras mover el código)", () => {
    expect(huella(aviso(10))).toBe(huella(aviso(40)));
  });
  it("sí depende del archivo", () => {
    expect(huella(aviso(10))).not.toBe(huella(aviso(10, "Confirmado", "src/b.cpp")));
  });
});

describe("reintentar y fallar", () => {
  const por = desenvolver(Autorizado.para(dev, "solicitar-revision"));
  it("una revisión fallida vuelve a la cola con un intento más", () => {
    const f = fallar(enAnalisis(), "timeout", instante(3));
    expect(reintentar(por, f, instante(4))).toMatchObject({ ok: true, valor: { intentos: 2, estado: { tipo: "Pendiente" } } });
  });
  it("no se reintenta lo que está en curso", () => {
    expect(reintentar(por, enAnalisis(), instante(4))).toEqual({ ok: false, error: { tipo: "RevisionEnCurso" } });
  });
});

describe("clasificar", () => {
  const por = desenvolver(Autorizado.para(dev, "clasificar-hallazgos"));
  const h = publicar(enAnalisis(), { analizados: 1, noCompilados: [], avisos: [aviso(10)] }, new Set(), ids, instante(3)).hallazgos[0]!;
  it("marcar falso positivo agrega la huella a los descartes; desmarcar la quita", () => {
    const fp = clasificar(por, h, "FalsoPositivo", instante(5));
    expect(fp.descarte).toBe("agregar");
    expect(clasificar(por, fp.hallazgo, "Confirmado", instante(6)).descarte).toBe("quitar");
    expect(clasificar(por, h, "Confirmado", instante(6)).descarte).toBe("ninguno");
  });
  it("un hallazgo nuevo no tiene autor; clasificarlo registra quién y cuándo", () => {
    expect(h.clasificadoPor).toBeNull();
    expect(clasificar(por, h, "Confirmado", instante(7)).hallazgo.clasificadoPor).toEqual({ por: dev.id, en: instante(7) });
  });
});

describe("estado del commit", () => {
  const pub = (avisos: Aviso[]) => publicar(enAnalisis(), { analizados: 1, noCompilados: [], avisos }, new Set(), ids, instante(3)).revision;
  it("con problemas y bloqueo, failure", () => {
    expect(estadoCommit(repo, pub([aviso(10)])).estado).toBe("failure");
  });
  it("con problemas sin bloqueo, success con aviso", () => {
    expect(estadoCommit({ ...repo, bloquearMerge: false }, pub([aviso(10)]))).toEqual({ estado: "success", descripcion: "1 confirmados, 0 posibles (no bloquea el merge)" });
  });
  it("aprobada, success; fallida, error; en cola, pending", () => {
    expect(estadoCommit(repo, pub([])).estado).toBe("success");
    expect(estadoCommit(repo, fallar(enAnalisis(), "x", instante(3))).estado).toBe("error");
    expect(estadoCommit(repo, desenvolver(solicitar(repo, undefined, sol, instante(1)))).estado).toBe("pending");
  });
});

describe("informe", () => {
  it("el comentario lleva la clase, el mensaje y la ruta", () => {
    const h = publicar(enAnalisis(), { analizados: 1, noCompilados: [], avisos: [aviso(10)] }, new Set(), ids, instante(3)).hallazgos[0]!;
    expect(comentario(h)).toContain("**Uso de un handle invalidado**");
    expect(comentario(h)).toContain("- línea 8: El handle al elemento se obtiene");
  });
  it("el cuerpo lista lo que quedó fuera del diff, salvo lo descartado", () => {
    const p = publicar(enAnalisis(), { analizados: 2, noCompilados: [], avisos: [aviso(10), aviso(30, "Posible", "src/b.cpp")] }, new Set([huella(aviso(30, "Posible", "src/b.cpp"))]), ids, instante(3));
    const c = cuerpo(p.revision, p.hallazgos, "http://x/r/1");
    expect(c).toContain("`src/a.cpp:10`");
    expect(c).not.toContain("src/b.cpp");
    expect(c).toContain("1 descartados como falso positivo");
    const r: Revision = p.revision;
    expect(r.estado.tipo).toBe("Publicada");
  });
});

describe("archivos que no compilan", () => {
  it("se cuentan en el resumen y el cuerpo lo dice", () => {
    const p = publicar(enAnalisis(), { analizados: 1, noCompilados: ["src/gen.cpp"], avisos: [] }, new Set(), ids, instante(3));
    expect(p.revision.estado).toMatchObject({ resumen: { archivosAnalizados: 1, noCompilados: 1 } });
    expect(cuerpo(p.revision, [], "u")).toContain("1 archivos no compilaron");
  });
});
