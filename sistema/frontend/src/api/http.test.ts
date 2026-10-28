// El adaptador HTTP con un `fetch` falso: rutas, cuerpos, y que nunca lanza.
import { describe, expect, it } from "vitest";
import { apiHttp, type Fetch } from "./http";

const usuario = { id: "u1", email: "a@b.pe", nombre: "Ana", rol: "administrador", estado: "Activo", creadoEn: "2026-10-27T02:45:19.470Z" };

function falso(respuesta: () => Response | Promise<Response>) {
  const pedidos: { url: string; init: RequestInit }[] = [];
  const f: Fetch = async (url, init) => {
    pedidos.push({ url, init });
    return respuesta();
  };
  return { f, pedidos };
}

const json = (status: number, cuerpo: unknown) => new Response(JSON.stringify(cuerpo), { status, headers: { "content-type": "application/json" } });

describe("apiHttp", () => {
  it("envía el JSON con su cabecera y valida la respuesta", async () => {
    const { f, pedidos } = falso(() => json(200, usuario));
    const r = await apiHttp(f, "http://srv").ingresar({ email: "a@b.pe", clave: "x" });
    expect(r).toEqual({ ok: true, valor: usuario });
    expect(pedidos[0]).toMatchObject({ url: "http://srv/api/sesion", init: { method: "POST", credentials: "same-origin", body: '{"email":"a@b.pe","clave":"x"}', headers: { "content-type": "application/json" } } });
  });

  it("un error del servicio vuelve como Negocio con su código, estado y mensaje", async () => {
    const { f } = falso(() => json(409, { error: { codigo: "EmailEnUso", mensaje: "Ya hay un usuario con ese correo." } }));
    expect(await apiHttp(f).registrar({ email: "a@b.pe", nombre: "A", clave: "c" })).toEqual({ ok: false, error: { tipo: "Negocio", estado: 409, codigo: "EmailEnUso", mensaje: "Ya hay un usuario con ese correo." } });
  });

  it("la sesión vencida se distingue (el panel vuelve al ingreso); credenciales inválidas no", async () => {
    const venc = falso(() => json(401, { error: { codigo: "SesionInvalida", mensaje: "La sesión venció." } }));
    expect(await apiHttp(venc.f).sesion()).toEqual({ ok: false, error: { tipo: "SinSesion", mensaje: "La sesión venció." } });
    const malas = falso(() => json(401, { error: { codigo: "CredencialesInvalidas", mensaje: "Correo o clave incorrectos." } }));
    expect(await apiHttp(malas.f).ingresar({ email: "a", clave: "b" })).toMatchObject({ ok: false, error: { tipo: "Negocio", estado: 401 } });
  });

  it("la red caída no lanza: devuelve Red", async () => {
    const { f } = falso(() => Promise.reject(new TypeError("Failed to fetch")));
    expect(await apiHttp(f).usuarios()).toEqual({ ok: false, error: { tipo: "Red", detalle: "TypeError: Failed to fetch" } });
  });

  it("una respuesta fuera de contrato no llega a la pantalla: RespuestaInvalida con el campo culpable", async () => {
    const { f } = falso(() => json(200, { ...usuario, rol: "superusuario" }));
    const r = await apiHttp(f).sesion();
    expect(r.ok).toBe(false);
    expect(!r.ok && r.error).toMatchObject({ tipo: "RespuestaInvalida", detalle: expect.stringContaining("rol") });
  });

  it("un cuerpo que no es JSON y un error sin cuerpo también son RespuestaInvalida", async () => {
    expect(await apiHttp(falso(() => new Response("<html>", { status: 200 })).f).sesion()).toMatchObject({ ok: false, error: { tipo: "RespuestaInvalida" } });
    expect(await apiHttp(falso(() => new Response("", { status: 500 })).f).sesion()).toEqual({ ok: false, error: { tipo: "RespuestaInvalida", detalle: "HTTP 500 sin cuerpo de error" } });
  });

  it("cerrar sesión acepta el 204 sin cuerpo", async () => {
    const { f, pedidos } = falso(() => new Response(null, { status: 204 }));
    expect(await apiHttp(f).salir()).toEqual({ ok: true, valor: undefined });
    expect(pedidos[0]!.init).toMatchObject({ method: "DELETE" });
  });

  it("junta quién y cuándo clasificó en `autoria`; si el servicio manda uno sin el otro, lo rechaza", async () => {
    const h = { id: "h", archivo: "a.cpp", linea: 1, columna: 2, clase: "Posible", mensaje: "m", ruta: [], huella: "x", clasificacion: "Confirmado" };
    const bien = falso(() => json(200, { ...h, clasificadoPor: { id: "u1", nombre: "Ana" }, clasificadoEn: "2026-10-27T02:45:19.470Z" }));
    expect(await apiHttp(bien.f).clasificar("h", "Confirmado")).toMatchObject({ ok: true, valor: { autoria: { por: { nombre: "Ana" }, en: "2026-10-27T02:45:19.470Z" } } });
    expect(bien.pedidos[0]).toMatchObject({ url: "/api/hallazgos/h", init: { method: "PATCH", body: '{"clasificacion":"Confirmado"}' } });
    const sin = falso(() => json(200, { ...h, clasificadoPor: null, clasificadoEn: null }));
    expect(await apiHttp(sin.f).clasificar("h", "SinRevisar")).toMatchObject({ ok: true, valor: { autoria: null } });
    const roto = falso(() => json(200, { ...h, clasificadoPor: { id: "u1", nombre: "Ana" }, clasificadoEn: null }));
    expect(await apiHttp(roto.f).clasificar("h", "Confirmado")).toMatchObject({ ok: false, error: { tipo: "RespuestaInvalida" } });
  });

  it("cada operación va a su ruta y método, con los ids escapados", async () => {
    const { f, pedidos } = falso(() => json(500, { error: { codigo: "Interno", mensaje: "x" } }));
    const api = apiHttp(f);
    await api.estadoRegistro();
    await api.crearUsuario({ email: "a@b.pe", nombre: "A", clave: "c", rol: "desarrollador" });
    await api.actualizarUsuario("u/1", { estado: "Activo" });
    await api.repositorios();
    await api.conectar({ nombre: "o/r", politica: "Silent", bloquearMerge: true });
    await api.configurar("r1", { politica: "Possibly" });
    await api.desconectar("r1");
    await api.revisiones();
    await api.revisiones("r 1");
    await api.revision("v1");
    await api.solicitar("r1", 7);
    await api.reintentar("v1");
    expect(pedidos.map((p) => `${p.init.method} ${p.url}`)).toEqual([
      "GET /api/registro",
      "POST /api/usuarios",
      "PATCH /api/usuarios/u%2F1",
      "GET /api/repositorios",
      "POST /api/repositorios",
      "PATCH /api/repositorios/r1",
      "DELETE /api/repositorios/r1",
      "GET /api/revisiones",
      "GET /api/revisiones?repositorio=r%201",
      "GET /api/revisiones/v1",
      "POST /api/revisiones",
      "POST /api/revisiones/v1/reintento",
    ]);
    expect(pedidos[10]!.init.body).toBe('{"repositorioId":"r1","numeroPr":7}');
  });
});
