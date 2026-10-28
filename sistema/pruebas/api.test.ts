// La API completa: Fastify + SQLite en memoria + scrypt/HMAC reales; GitHub y clang son dobles.
import { beforeEach, describe, expect, it } from "vitest";
import { desenvolver, type Positivo } from "@centinela/kernel";
import { producto, type Producto } from "@centinela/producto";
import { abrirAlmacen } from "@centinela/sqlite";
import { claves, firmar, secretos } from "@centinela/cripto";
import { crearServidor, COOKIE_SESION, CABECERAS_SEGURIDAD } from "@centinela/http";
import { dependencias } from "./dobles";

const CLAVE = "clave12345678";
let app: ReturnType<typeof crearServidor>;
let p: Producto;
let t: ReturnType<typeof dependencias>;

beforeEach(async () => {
  t = dependencias(abrirAlmacen(":memory:"));
  p = producto({ ...t.deps, claves, secretos });
  desenvolver(await p.identidad.registrar({ email: "admin@ucsm.edu.pe", nombre: "Admin", clave: CLAVE }));
  app = crearServidor(p, { urlPublica: "https://centinela.ucsm.edu.pe", cookieSegura: true, maxIntentos: 3 });
});

async function entrar(email = "admin@ucsm.edu.pe", clave = CLAVE) {
  const r = await app.inject({ method: "POST", url: "/api/sesion", payload: { email, clave } });
  const c = r.cookies.find((x) => x.name === COOKIE_SESION);
  return { r, cookie: c ? `${COOKIE_SESION}=${c.value}` : "" };
}

describe("RF-S01 registro (nada predefinido)", () => {
  it("una instancia nueva no tiene usuarios; quien se registra primero es administrador y entra directo", async () => {
    const vacia = producto({ ...dependencias(abrirAlmacen(":memory:")).deps, claves, secretos });
    const srv = crearServidor(vacia, { urlPublica: "http://x", cookieSegura: false });
    expect((await srv.inject({ method: "GET", url: "/api/registro" })).json()).toEqual({ hayUsuarios: false });
    const r = await srv.inject({ method: "POST", url: "/api/registro", payload: { email: "duena@ucsm.edu.pe", nombre: "Dueña", clave: CLAVE } });
    expect(r.statusCode).toBe(201);
    expect(r.json()).toMatchObject({ usuario: { rol: "administrador", estado: "Activo" }, pendienteDeAprobacion: false });
    const cookie = `${COOKIE_SESION}=${r.cookies.find((c) => c.name === COOKIE_SESION)!.value}`;
    expect((await srv.inject({ method: "GET", url: "/api/sesion", headers: { cookie } })).json().email).toBe("duena@ucsm.edu.pe");
  });
  it("los siguientes quedan pendientes, sin sesión, hasta que un administrador los aprueba", async () => {
    const r = await app.inject({ method: "POST", url: "/api/registro", payload: { email: "nuevo@ucsm.edu.pe", nombre: "Nuevo", clave: CLAVE } });
    expect(r.json()).toMatchObject({ usuario: { rol: "desarrollador", estado: "Pendiente" }, pendienteDeAprobacion: true });
    expect(r.cookies.find((c) => c.name === COOKIE_SESION)).toBeUndefined();
    const intento = await entrar("nuevo@ucsm.edu.pe");
    expect(intento.r.statusCode).toBe(403);
    expect(intento.r.json().error.mensaje).toBe("Tu cuenta espera la aprobación de un administrador.");
    const { cookie } = await entrar();
    const id = r.json().usuario.id;
    expect((await app.inject({ method: "PATCH", url: `/api/usuarios/${id}`, headers: { cookie }, payload: { estado: "Activo", rol: "administrador" } })).json()).toMatchObject({ estado: "Activo", rol: "administrador" });
    expect((await entrar("nuevo@ucsm.edu.pe")).r.statusCode).toBe(200);
  });
  it("rechazar un registro deja la cuenta desactivada y el ingreso lo dice; no se puede volver a Pendiente", async () => {
    const r = await app.inject({ method: "POST", url: "/api/registro", payload: { email: "rechazo@ucsm.edu.pe", nombre: "Rechazo", clave: CLAVE } });
    const { cookie } = await entrar();
    const url = `/api/usuarios/${r.json().usuario.id}`;
    expect((await app.inject({ method: "PATCH", url, headers: { cookie }, payload: { estado: "Desactivado" } })).json()).toMatchObject({ estado: "Desactivado" });
    const intento = await entrar("rechazo@ucsm.edu.pe");
    expect(intento.r.statusCode).toBe(403);
    expect(intento.r.json().error).toEqual({ codigo: "UsuarioDesactivado", mensaje: "Tu cuenta está desactivada: pide a un administrador que la reactive." });
    expect((await app.inject({ method: "PATCH", url, headers: { cookie }, payload: { estado: "Pendiente" } })).statusCode).toBe(400);
  });
  it("registro inválido: 400; correo en uso: 409; cambio vacío: 400; cambiarse a sí mismo: 409", async () => {
    expect((await app.inject({ method: "POST", url: "/api/registro", payload: { email: "a@b.co", nombre: "A", clave: "corta" } })).statusCode).toBe(400);
    expect((await app.inject({ method: "POST", url: "/api/registro", payload: { email: "admin@ucsm.edu.pe", nombre: "A", clave: CLAVE } })).statusCode).toBe(409);
    const { r, cookie } = await entrar();
    const yo = r.json().id;
    expect((await app.inject({ method: "PATCH", url: `/api/usuarios/${yo}`, headers: { cookie }, payload: {} })).statusCode).toBe(400);
    expect((await app.inject({ method: "PATCH", url: `/api/usuarios/${yo}`, headers: { cookie }, payload: { rol: "desarrollador" } })).statusCode).toBe(409);
  });
});

describe("RF-S01 autenticación", () => {
  it("ingresar pone una cookie httpOnly, SameSite=Strict y Secure, y no devuelve el hash", async () => {
    const { r } = await entrar();
    expect(r.statusCode).toBe(200);
    const c = r.cookies.find((x) => x.name === COOKIE_SESION)!;
    expect(c).toMatchObject({ httpOnly: true, sameSite: "Strict", secure: true, path: "/" });
    expect(r.json()).toEqual(expect.objectContaining({ email: "admin@ucsm.edu.pe", rol: "administrador" }));
    expect(r.body).not.toContain("scrypt");
  });
  it("sin sesión, la API responde 401", async () => {
    for (const url of ["/api/sesion", "/api/usuarios", "/api/repositorios", "/api/revisiones"]) {
      expect((await app.inject({ method: "GET", url })).statusCode).toBe(401);
    }
  });
  it("clave incorrecta: 401; tras 3 fallos, 429 aunque luego acierte", async () => {
    for (let i = 0; i < 3; i++) expect((await entrar("admin@ucsm.edu.pe", "mala1234567")).r.statusCode).toBe(401);
    expect((await entrar()).r.statusCode).toBe(429);
  });
  it("cerrar sesión invalida la cookie", async () => {
    const { cookie } = await entrar();
    expect((await app.inject({ method: "DELETE", url: "/api/sesion", headers: { cookie } })).statusCode).toBe(204);
    expect((await app.inject({ method: "GET", url: "/api/sesion", headers: { cookie } })).statusCode).toBe(401);
  });
  it("el administrador crea un desarrollador, que no puede crear usuarios", async () => {
    const { cookie } = await entrar();
    const nuevo = { email: "dev@ucsm.edu.pe", nombre: "Dev", clave: CLAVE, rol: "desarrollador" };
    expect((await app.inject({ method: "POST", url: "/api/usuarios", headers: { cookie }, payload: nuevo })).statusCode).toBe(201);
    expect((await app.inject({ method: "POST", url: "/api/usuarios", headers: { cookie }, payload: nuevo })).statusCode).toBe(409);
    const dev = await entrar("dev@ucsm.edu.pe");
    const r = await app.inject({ method: "POST", url: "/api/usuarios", headers: { cookie: dev.cookie }, payload: { ...nuevo, email: "x@ucsm.edu.pe" } });
    expect(r.statusCode).toBe(403);
    expect(r.json().error.codigo).toBe("SinPermiso");
  });
  it("entradas mal formadas: 400 con el campo", async () => {
    const { cookie } = await entrar();
    const r = await app.inject({ method: "POST", url: "/api/usuarios", headers: { cookie }, payload: { email: "a@b.co", nombre: "A", clave: "corta", rol: "desarrollador" } });
    expect(r.statusCode).toBe(400);
    expect(r.json().error.codigo).toBe("ClaveDebil");
    expect((await app.inject({ method: "PATCH", url: "/api/usuarios/no-es-uuid", headers: { cookie }, payload: { estado: "Desactivado" } })).statusCode).toBe(400);
    expect((await app.inject({ method: "POST", url: "/api/sesion", headers: { "content-type": "application/json" }, payload: "{no json" })).statusCode).toBe(400);
  });
});

describe("RF-S02 a RF-S05 por HTTP", () => {
  let cookie: string;
  let repo: { id: string; webhook: { url: string; secreto: string } };
  beforeEach(async () => {
    cookie = (await entrar()).cookie;
    const r = await app.inject({ method: "POST", url: "/api/repositorios", headers: { cookie }, payload: { nombre: "ucsm/demo", politica: "Possibly", bloquearMerge: true } });
    expect(r.statusCode).toBe(201);
    repo = r.json();
    t.github.archivos = [{ ruta: "src/a.cpp", eliminado: false, lineas: new Set([11]) }];
    t.analizador.avisos = [{ archivo: "src/a.cpp", linea: 11 as Positivo, columna: 3 as Positivo, clase: "Confirmado", mensaje: "Uso de una referencia invalidada", ruta: [] }];
  });

  const webhook = (cuerpo: string, firma: string | undefined, evento = "pull_request") =>
    app.inject({
      method: "POST",
      url: "/webhooks/github",
      headers: { "content-type": "application/json", "x-github-event": evento, ...(firma ? { "x-hub-signature-256": firma } : {}) },
      payload: cuerpo,
    });
  const cuerpoPr = (accion = "opened") =>
    JSON.stringify({ action: accion, repository: { full_name: "ucsm/demo" }, pull_request: { number: 7, title: "Caché", user: { login: "ana" }, head: { sha: "abc" } } });

  it("conectar devuelve la URL y el secreto del webhook; el desarrollador no ve el secreto", async () => {
    expect(repo.webhook).toMatchObject({ url: "https://centinela.ucsm.edu.pe/webhooks/github", tipoContenido: "application/json" });
    await app.inject({ method: "POST", url: "/api/usuarios", headers: { cookie }, payload: { email: "dev@ucsm.edu.pe", nombre: "Dev", clave: CLAVE, rol: "desarrollador" } });
    const dev = await entrar("dev@ucsm.edu.pe");
    const lista = (await app.inject({ method: "GET", url: "/api/repositorios", headers: { cookie: dev.cookie } })).json();
    expect(lista[0].webhook).toBeNull();
  });

  it("webhook con firma de GitHub: 202 y queda pendiente; con firma mala, 401", async () => {
    const c = cuerpoPr();
    expect((await webhook(c, firmar(repo.webhook.secreto, c + " "))).statusCode).toBe(401);
    expect((await webhook(c, undefined)).statusCode).toBe(401);
    const r = await webhook(c, firmar(repo.webhook.secreto, c));
    expect(r.statusCode).toBe(202);
    const lista = (await app.inject({ method: "GET", url: "/api/revisiones", headers: { cookie } })).json();
    expect(lista[0]).toMatchObject({ estado: { tipo: "Pendiente" }, pr: { numero: 7, enlace: "https://github.com/ucsm/demo/pull/7" }, repositorio: { nombre: "ucsm/demo" } });
  });

  it("ping y PR cerrado: 200 ignorado", async () => {
    const ping = JSON.stringify({ zen: "x", repository: { full_name: "ucsm/demo" } });
    expect((await webhook(ping, firmar(repo.webhook.secreto, ping), "ping")).json()).toEqual({ tipo: "Ignorado", motivo: "ping" });
    const c = cuerpoPr("closed");
    expect((await webhook(c, firmar(repo.webhook.secreto, c))).statusCode).toBe(200);
  });

  it("detalle con hallazgos, clasificar y reintentar", async () => {
    const c = cuerpoPr();
    const { revisionId } = (await webhook(c, firmar(repo.webhook.secreto, c))).json();
    await p.revisiones.procesarSiguiente();
    const det = (await app.inject({ method: "GET", url: `/api/revisiones/${revisionId}`, headers: { cookie } })).json();
    expect(det).toMatchObject({ estado: { tipo: "Publicada", veredicto: "ConProblemas" }, hallazgos: [{ archivo: "src/a.cpp", linea: 11, clasificacion: "SinRevisar", clasificadoPor: null, clasificadoEn: null }] });

    const h = det.hallazgos[0].id;
    const cl = await app.inject({ method: "PATCH", url: `/api/hallazgos/${h}`, headers: { cookie }, payload: { clasificacion: "FalsoPositivo" } });
    expect(cl.json()).toMatchObject({ clasificacion: "FalsoPositivo", clasificadoPor: { nombre: "Admin" } });
    const otraVez = (await app.inject({ method: "GET", url: `/api/revisiones/${revisionId}`, headers: { cookie } })).json();
    expect(otraVez.hallazgos[0]).toMatchObject({ clasificadoPor: { nombre: "Admin" }, clasificadoEn: expect.stringMatching(/^\d{4}-/) });
    expect((await app.inject({ method: "PATCH", url: `/api/hallazgos/${h}`, headers: { cookie }, payload: { clasificacion: "Otra" } })).statusCode).toBe(400);

    expect((await app.inject({ method: "POST", url: `/api/revisiones/${revisionId}/reintento`, headers: { cookie } })).statusCode).toBe(202);
    expect((await app.inject({ method: "POST", url: `/api/revisiones/${revisionId}/reintento`, headers: { cookie } })).statusCode).toBe(409);
    await p.revisiones.procesarSiguiente();
    const otra = (await app.inject({ method: "GET", url: `/api/revisiones/${revisionId}`, headers: { cookie } })).json();
    expect(otra).toMatchObject({ intentos: 2, estado: { veredicto: "Aprobada", resumen: { suprimidos: 1 } } });
  });

  it("revisar ahora: 202 si GitHub tiene el PR, 502 si no", async () => {
    expect((await app.inject({ method: "POST", url: "/api/revisiones", headers: { cookie }, payload: { repositorioId: repo.id, numeroPr: 9 } })).statusCode).toBe(502);
    t.github.prs.set(9, { numero: 9 as Positivo, titulo: "T", autor: "b", shaCabeza: "def" });
    const r = await app.inject({ method: "POST", url: "/api/revisiones", headers: { cookie }, payload: { repositorioId: repo.id, numeroPr: 9 } });
    expect(r.statusCode).toBe(202);
    expect(r.json()).toMatchObject({ origen: "manual", estado: { tipo: "Pendiente" } });
  });

  it("configurar y desconectar el repositorio", async () => {
    const r = await app.inject({ method: "PATCH", url: `/api/repositorios/${repo.id}`, headers: { cookie }, payload: { politica: "Silent" } });
    expect(r.json().politica).toBe("Silent");
    expect((await app.inject({ method: "PATCH", url: `/api/repositorios/${repo.id}`, headers: { cookie }, payload: { otra: 1 } })).statusCode).toBe(400);
    expect((await app.inject({ method: "DELETE", url: `/api/repositorios/${repo.id}`, headers: { cookie } })).json().activo).toBe(false);
    const c = cuerpoPr();
    expect((await webhook(c, firmar(repo.webhook.secreto, c))).json()).toEqual({ tipo: "Ignorado", motivo: "RepositorioDesconectado" });
  });

  it("recursos que no existen: 404", async () => {
    const otro = "00000000-0000-4000-8000-ffffffffffff";
    expect((await app.inject({ method: "GET", url: `/api/revisiones/${otro}`, headers: { cookie } })).statusCode).toBe(404);
    expect((await app.inject({ method: "PATCH", url: `/api/hallazgos/${otro}`, headers: { cookie }, payload: { clasificacion: "Confirmado" } })).statusCode).toBe(404);
  });
});

it("salud", async () => {
  expect((await app.inject({ method: "GET", url: "/salud" })).json()).toEqual({ ok: true });
});

describe("frontend", () => {
  it("sirve index.html en las rutas de la SPA y 404 JSON en la API", async () => {
    const { mkdtempSync, writeFileSync, rmSync } = await import("node:fs");
    const { join } = await import("node:path");
    const { tmpdir } = await import("node:os");
    const dir = mkdtempSync(join(tmpdir(), "centinela-front-"));
    try {
      writeFileSync(join(dir, "index.html"), "<!doctype html><title>Centinela</title>");
      const conFront = crearServidor(p, { urlPublica: "http://x", cookieSegura: false, frontend: dir });
      expect((await conFront.inject({ method: "GET", url: "/revisiones/123" })).body).toContain("Centinela");
      expect((await conFront.inject({ method: "GET", url: "/api/nada" })).statusCode).toBe(404);
      await conFront.close();
    } finally {
      rmSync(dir, { recursive: true });
    }
  });
});

describe("RNF-S01 cabeceras de seguridad", () => {
  it("toda respuesta (API, error y salud) lleva la política de contenido, nosniff y no se deja enmarcar", async () => {
    const { cookie } = await entrar();
    for (const r of [
      await app.inject({ method: "GET", url: "/salud" }),
      await app.inject({ method: "GET", url: "/api/revisiones", headers: { cookie } }),
      await app.inject({ method: "GET", url: "/api/revisiones" }),
      await app.inject({ method: "GET", url: "/api/no-existe" }),
    ]) {
      for (const [k, v] of Object.entries(CABECERAS_SEGURIDAD)) expect(r.headers[k]).toBe(v);
    }
    expect(CABECERAS_SEGURIDAD["content-security-policy"]).toContain("frame-ancestors 'none'");
  });
});
