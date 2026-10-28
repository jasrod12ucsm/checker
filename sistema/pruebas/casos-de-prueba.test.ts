// Los casos de prueba del capítulo 8 (CP-01 a CP-14), ejecutables: cada fila de la tabla del libro es una prueba.
// Valores límite de cada campo (obligatorio, tamaño, tipo, formato), cálculos del resumen y vínculos.
import { beforeEach, describe, expect, it } from "vitest";
import { desenvolver, type Positivo } from "@centinela/kernel";
import { producto, type Producto } from "@centinela/producto";
import { abrirAlmacen } from "@centinela/sqlite";
import { claves, firmar, secretos } from "@centinela/cripto";
import { crearServidor, COOKIE_SESION } from "@centinela/http";
import { dependencias } from "./dobles";

const CLAVE = "clave12345678";
const URL_PUBLICA = "https://centinela.ucsm.edu.pe";
let app: ReturnType<typeof crearServidor>;
let p: Producto;
let t: ReturnType<typeof dependencias>;
let cookie: string;

beforeEach(async () => {
  t = dependencias(abrirAlmacen(":memory:"));
  p = producto({ ...t.deps, claves, secretos });
  desenvolver(await p.identidad.registrar({ email: "admin@ucsm.edu.pe", nombre: "Admin", clave: CLAVE }));
  app = crearServidor(p, { urlPublica: URL_PUBLICA, cookieSegura: true });
  const r = await app.inject({ method: "POST", url: "/api/sesion", payload: { email: "admin@ucsm.edu.pe", clave: CLAVE } });
  cookie = `${COOKIE_SESION}=${r.cookies.find((c) => c.name === COOKIE_SESION)!.value}`;
});

const registro = (payload: unknown) => app.inject({ method: "POST", url: "/api/registro", payload: payload as Record<string, unknown> });
const conectar = (payload: unknown) => app.inject({ method: "POST", url: "/api/repositorios", headers: { cookie }, payload: payload as Record<string, unknown> });
const correo = (largo: number) => `${"a".repeat(largo - "@ucsm.edu.pe".length)}@ucsm.edu.pe`;

describe("CP — formulario de registro", () => {
  it("CP-01 correo obligatorio y con formato: vacío, sin @ o sin dominio se rechazan", async () => {
    for (const email of ["", "ana", "ana@", "ana@ucsm", "ana ucsm@x.pe"]) expect((await registro({ email, nombre: "Ana", clave: CLAVE })).statusCode).toBe(400);
  });

  it("CP-02 tamaño del correo: 254 caracteres se acepta, 255 se rechaza", async () => {
    expect((await registro({ email: correo(254), nombre: "Ana", clave: CLAVE })).statusCode).toBe(201);
    expect((await registro({ email: correo(255), nombre: "Ana", clave: CLAVE })).statusCode).toBe(400);
  });

  it("CP-03 nombre obligatorio, de 1 a 100 caracteres", async () => {
    expect((await registro({ email: "a@ucsm.edu.pe", nombre: "", clave: CLAVE })).statusCode).toBe(400);
    expect((await registro({ email: "b@ucsm.edu.pe", nombre: "   ", clave: CLAVE })).statusCode).toBe(400);
    expect((await registro({ email: "c@ucsm.edu.pe", nombre: "N".repeat(100), clave: CLAVE })).statusCode).toBe(201);
    expect((await registro({ email: "d@ucsm.edu.pe", nombre: "N".repeat(101), clave: CLAVE })).statusCode).toBe(400);
  });

  it("CP-04 clave: de 10 a 128 caracteres, con letras y números", async () => {
    const casos: [string, number][] = [["abc456789", 400], ["abc4567890", 201], [`a1${"x".repeat(126)}`, 201], [`a1${"x".repeat(127)}`, 400], ["soloLetrasAqui", 400], ["1234567890", 400]];
    for (const [i, [clave, estado]] of casos.entries()) expect((await registro({ email: `k${i}@ucsm.edu.pe`, nombre: "K", clave })).statusCode, clave).toBe(estado);
  });

  it("CP-05 tipos de dato: un número o un campo ausente donde va texto se rechaza", async () => {
    expect((await registro({ email: 5, nombre: "Ana", clave: CLAVE })).statusCode).toBe(400);
    expect((await registro({ email: "e@ucsm.edu.pe", clave: CLAVE })).statusCode).toBe(400);
    expect((await registro({ email: "e@ucsm.edu.pe", nombre: ["Ana"], clave: CLAVE })).statusCode).toBe(400);
  });

  it("CP-06 correo en uso: 409, sin importar mayúsculas", async () => {
    expect((await registro({ email: "ADMIN@ucsm.edu.pe", nombre: "Otra", clave: CLAVE })).statusCode).toBe(409);
  });
});

describe("CP — formulario de ingreso", () => {
  it("CP-07 correo y clave obligatorios; la respuesta no distingue correo inexistente de clave equivocada", async () => {
    expect((await app.inject({ method: "POST", url: "/api/sesion", payload: { email: "admin@ucsm.edu.pe" } })).statusCode).toBe(400);
    const a = await app.inject({ method: "POST", url: "/api/sesion", payload: { email: "nadie@ucsm.edu.pe", clave: CLAVE } });
    const b = await app.inject({ method: "POST", url: "/api/sesion", payload: { email: "admin@ucsm.edu.pe", clave: "otra1234567" } });
    expect([a.statusCode, b.statusCode]).toEqual([401, 401]);
    expect(a.json()).toEqual(b.json());
  });
});

describe("CP — formulario de repositorio", () => {
  it("CP-08 nombre dueño/repositorio: formatos válidos e inválidos", async () => {
    for (const nombre of ["a/b", "lab-sistemas/motor-rutas", "x/repo.con_puntos-y_guiones"]) expect((await conectar({ nombre, politica: "Possibly", bloquearMerge: true })).statusCode, nombre).toBe(201);
    for (const nombre of ["", "sin-barra", "/repo", "dueño/", "-malo/repo", "a/b/c", "a b/c", `${"d".repeat(40)}/r`]) expect((await conectar({ nombre, politica: "Possibly", bloquearMerge: true })).statusCode, nombre).toBe(400);
  });

  it("CP-09 política y bloqueo obligatorios, con sus valores permitidos", async () => {
    expect((await conectar({ nombre: "a/b" })).statusCode).toBe(400);
    expect((await conectar({ nombre: "a/b", politica: "Todo", bloquearMerge: true })).statusCode).toBe(400);
    expect((await conectar({ nombre: "a/b", politica: "Silent", bloquearMerge: "si" })).statusCode).toBe(400);
    expect((await conectar({ nombre: "a/b", politica: "Silent", bloquearMerge: false })).json()).toMatchObject({ politica: "Silent", bloquearMerge: false });
  });
});

describe("CP — revisar un PR ahora", () => {
  it("CP-10 número de PR: entero positivo; 0, negativo, decimal o texto se rechazan", async () => {
    const repo = (await conectar({ nombre: "ucsm/demo", politica: "Possibly", bloquearMerge: true })).json();
    for (const numeroPr of [0, -1, 1.5, "3"]) expect((await app.inject({ method: "POST", url: "/api/revisiones", headers: { cookie }, payload: { repositorioId: repo.id, numeroPr } })).statusCode, String(numeroPr)).toBe(400);
    expect((await app.inject({ method: "POST", url: "/api/revisiones", headers: { cookie }, payload: { repositorioId: "no-es-uuid", numeroPr: 3 } })).statusCode).toBe(400);
  });
});

describe("CP — cálculos, formatos y vínculos de una revisión", () => {
  let det: { estado: { veredicto: string; resumen: Record<string, number> }; hallazgos: { clase: string }[]; creadaEn: string; pr: { enlace: string; shaCabeza: string } };
  let revisionId: string;
  beforeEach(async () => {
    const repo = (await conectar({ nombre: "ucsm/demo", politica: "Possibly", bloquearMerge: true })).json();
    t.github.archivos = [{ ruta: "src/a.cpp", eliminado: false, lineas: new Set([11, 20, 30]) }];
    const aviso = (linea: number, clase: "Confirmado" | "Posible", mensaje: string) => ({ archivo: "src/a.cpp", linea: linea as Positivo, columna: 3 as Positivo, clase, mensaje, ruta: [] });
    t.analizador.avisos = [aviso(11, "Confirmado", "uno"), aviso(20, "Posible", "dos"), aviso(30, "Posible", "tres")];
    const c = JSON.stringify({ action: "opened", repository: { full_name: "ucsm/demo" }, pull_request: { number: 7, title: "Caché", user: { login: "ana" }, head: { sha: "0123456789abcdef0123456789abcdef01234567" } } });
    revisionId = (await app.inject({ method: "POST", url: "/webhooks/github", headers: { "content-type": "application/json", "x-github-event": "pull_request", "x-hub-signature-256": firmar(repo.webhook.secreto, c) }, payload: c })).json().revisionId;
    await p.revisiones.procesarSiguiente();
    det = (await app.inject({ method: "GET", url: `/api/revisiones/${revisionId}`, headers: { cookie } })).json();
  });

  it("CP-11 el resumen cuenta lo mismo que los hallazgos, y el veredicto sale de ellos", () => {
    const r = det.estado.resumen;
    expect(r.confirmados).toBe(det.hallazgos.filter((h) => h.clase === "Confirmado").length);
    expect(r.posibles).toBe(det.hallazgos.filter((h) => h.clase === "Posible").length);
    expect([r.confirmados, r.posibles, r.suprimidos]).toEqual([1, 2, 0]);
    expect(det.estado.veredicto).toBe("ConProblemas");
  });

  it("CP-12 al marcar los tres como falso positivo y reintentar, los suprimidos suben y el veredicto pasa a aprobada", async () => {
    const ids = ((await app.inject({ method: "GET", url: `/api/revisiones/${revisionId}`, headers: { cookie } })).json().hallazgos as { id: string }[]).map((h) => h.id);
    for (const id of ids) await app.inject({ method: "PATCH", url: `/api/hallazgos/${id}`, headers: { cookie }, payload: { clasificacion: "FalsoPositivo" } });
    await app.inject({ method: "POST", url: `/api/revisiones/${revisionId}/reintento`, headers: { cookie } });
    await p.revisiones.procesarSiguiente();
    const otra = (await app.inject({ method: "GET", url: `/api/revisiones/${revisionId}`, headers: { cookie } })).json();
    expect(otra.estado).toMatchObject({ veredicto: "Aprobada", resumen: { confirmados: 0, posibles: 0, suprimidos: 3 } });
  });

  it("CP-13 formatos: fechas ISO 8601 en UTC y sha de 40 caracteres hexadecimales", () => {
    expect(det.creadaEn).toMatch(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/);
    expect(det.pr.shaCabeza).toMatch(/^[0-9a-f]{40}$/);
  });

  it("CP-14 vínculos: el PR enlaza a GitHub y el estado del commit enlaza a la revisión en Centinela", () => {
    expect(det.pr.enlace).toBe("https://github.com/ucsm/demo/pull/7");
    expect(t.github.estados.at(-1)).toMatchObject({ estado: { estado: "failure", descripcion: "1 confirmados, 2 posibles" }, enlace: `${t.deps.urlPublica}/revisiones/${revisionId}` });
  });
});
