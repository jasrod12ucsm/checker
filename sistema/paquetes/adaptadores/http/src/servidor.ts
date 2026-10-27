import Fastify, { type FastifyReply, type FastifyRequest } from "fastify";
import cookie from "@fastify/cookie";
import estaticos from "@fastify/static";
import type { z } from "zod";
import { puede, type Usuario } from "@centinela/identidad";
import type { RepositorioId, Resultado, RevisionId, UsuarioId, HallazgoId } from "@centinela/kernel";
import type { ErrorProducto, Producto } from "@centinela/producto";
import { respuestaDe } from "./errores";
import * as E from "./esquemas";
import { vistaHallazgo, vistaRepositorio, vistaRevision, vistaUsuario } from "./vistas";

export const COOKIE_SESION = "centinela_sesion";

export interface OpcionesServidor {
  readonly urlPublica: string;
  /** `true` detrás de HTTPS: la cookie solo viaja cifrada. */
  readonly cookieSegura: boolean;
  /** Intentos fallidos de ingreso por correo antes de bloquear 15 minutos. */
  readonly maxIntentos?: number;
  readonly registrar?: boolean;
  /** Carpeta del frontend ya construido (`frontend/dist`); se sirve en `/` con retorno a `index.html`. */
  readonly frontend?: string;
}

declare module "fastify" {
  interface FastifyRequest {
    cuerpoCrudo: string;
  }
}

class EntradaInvalida extends Error {
  constructor(readonly detalle: string) {
    super(detalle);
  }
}

function validar<S extends z.ZodType>(esquema: S, x: unknown): z.output<S> {
  const r = esquema.safeParse(x);
  if (!r.success) throw new EntradaInvalida(r.error.issues.map((i) => `${i.path.join(".") || "cuerpo"}: ${i.message}`).join("; "));
  return r.data;
}

const enviarError = (rep: FastifyReply, e: ErrorProducto) => {
  const r = respuestaDe(e);
  return rep.code(r.estado).send({ error: { codigo: e.tipo, mensaje: r.mensaje } });
};

async function responder<T>(rep: FastifyReply, r: Resultado<T, ErrorProducto>, estado: number, vista: (x: T) => unknown) {
  return r.ok ? rep.code(estado).send(vista(r.valor)) : enviarError(rep, r.error);
}

export function crearServidor(p: Producto, o: OpcionesServidor) {
  const app = Fastify({ logger: o.registrar ?? false, bodyLimit: 5 * 1024 * 1024 });
  void app.register(cookie);

  // El cuerpo crudo se guarda: la firma del webhook se calcula sobre los bytes recibidos.
  app.decorateRequest("cuerpoCrudo", "");
  app.addContentTypeParser("application/json", { parseAs: "string" }, (req, cuerpo, listo) => {
    req.cuerpoCrudo = cuerpo as string;
    try {
      listo(null, cuerpo === "" ? {} : JSON.parse(cuerpo as string));
    } catch {
      listo(new EntradaInvalida("el cuerpo no es JSON válido"), undefined);
    }
  });

  app.setErrorHandler((e, _req, rep) => {
    if (e instanceof EntradaInvalida) return rep.code(400).send({ error: { codigo: "EntradaInvalida", mensaje: e.detalle } });
    const { statusCode: estado, message } = e as { statusCode?: number; message?: string };
    if (estado !== undefined && estado >= 400 && estado < 500) return rep.code(estado).send({ error: { codigo: "Peticion", mensaje: message ?? "Petición inválida." } });
    app.log.error(e);
    return rep.code(500).send({ error: { codigo: "Interno", mensaje: "Error interno del servidor." } });
  });

  const fallos = new Map<string, { n: number; desde: number }>();
  const MAX = o.maxIntentos ?? 10;
  const VENTANA = 15 * 60 * 1000;

  const cookieSesion = { path: "/", httpOnly: true, sameSite: "strict" as const, secure: o.cookieSegura };

  /** Resuelve el usuario de la cookie; si no hay sesión válida, responde 401 y devuelve undefined. */
  async function usuario(req: FastifyRequest, rep: FastifyReply): Promise<Usuario | undefined> {
    const r = await p.identidad.sesionActual(req.cookies[COOKIE_SESION]);
    if (r.ok) return r.valor;
    await enviarError(rep, r.error);
    return undefined;
  }

  const repos = (u: Usuario) => {
    const r = p.repositorios.listar(u);
    return r.then((x) => new Map(x.ok ? x.valor.map((repo) => [repo.id, repo]) : []));
  };

  app.get("/salud", async () => ({ ok: true }));

  // RF-S01 — sesión

  // RF-S01 — registro: nada viene predefinido

  app.get("/api/registro", async (_req, rep) => responder(rep, await p.identidad.estadoRegistro(), 200, (x) => x));

  app.post("/api/registro", async (req, rep) => {
    const b = validar(E.Registro, req.body);
    const r = await p.identidad.registrar(b);
    if (!r.ok) return enviarError(rep, r.error);
    if (r.valor.estado === "Activo") {
      // El primer usuario (administrador) entra directamente.
      const s = await p.identidad.iniciarSesion(b.email, b.clave);
      if (s.ok) void rep.setCookie(COOKIE_SESION, s.valor.token, cookieSesion);
    }
    return rep.code(201).send({ usuario: vistaUsuario(r.valor), pendienteDeAprobacion: r.valor.estado === "Pendiente" });
  });

  app.post("/api/sesion", async (req, rep) => {
    const b = validar(E.Ingreso, req.body);
    const clave = b.email.trim().toLowerCase();
    const f = fallos.get(clave);
    if (f && f.n >= MAX && Date.now() - f.desde < VENTANA)
      return rep.code(429).send({ error: { codigo: "DemasiadosIntentos", mensaje: "Demasiados intentos fallidos. Espera 15 minutos." } });
    const r = await p.identidad.iniciarSesion(b.email, b.clave);
    if (!r.ok) {
      if (r.error.tipo === "CredencialesInvalidas") fallos.set(clave, f && Date.now() - f.desde < VENTANA ? { n: f.n + 1, desde: f.desde } : { n: 1, desde: Date.now() });
      return enviarError(rep, r.error);
    }
    fallos.delete(clave);
    void rep.setCookie(COOKIE_SESION, r.valor.token, cookieSesion);
    return rep.code(200).send(vistaUsuario(r.valor.usuario));
  });

  app.get("/api/sesion", async (req, rep) => {
    const u = await usuario(req, rep);
    if (u) return rep.send(vistaUsuario(u));
  });

  app.delete("/api/sesion", async (req, rep) => {
    const t = req.cookies[COOKIE_SESION];
    if (t !== undefined) await p.identidad.cerrarSesion(t);
    void rep.clearCookie(COOKIE_SESION, cookieSesion);
    return rep.code(204).send();
  });

  app.get("/api/usuarios", async (req, rep) => {
    const u = await usuario(req, rep);
    if (u) return responder(rep, await p.identidad.listarUsuarios(u), 200, (xs) => xs.map(vistaUsuario));
  });

  app.post("/api/usuarios", async (req, rep) => {
    const u = await usuario(req, rep);
    if (u) return responder(rep, await p.identidad.crearUsuario(u, validar(E.NuevoUsuario, req.body)), 201, vistaUsuario);
  });

  app.patch("/api/usuarios/:id", async (req, rep) => {
    const u = await usuario(req, rep);
    if (!u) return;
    const { id } = validar(E.ConId, req.params);
    const c = validar(E.CambioUsuario, req.body);
    const cambio = { ...(c.estado === undefined ? {} : { estado: c.estado }), ...(c.rol === undefined ? {} : { rol: c.rol }) };
    return responder(rep, await p.identidad.actualizarUsuario(u, id as UsuarioId, cambio), 200, vistaUsuario);
  });

  // RF-S02 — repositorios

  app.get("/api/repositorios", async (req, rep) => {
    const u = await usuario(req, rep);
    if (u) return responder(rep, await p.repositorios.listar(u), 200, (xs) => xs.map((r) => vistaRepositorio(r, puede(u.rol, "gestionar-repositorios"), o.urlPublica)));
  });

  app.post("/api/repositorios", async (req, rep) => {
    const u = await usuario(req, rep);
    if (u) return responder(rep, await p.repositorios.conectar(u, validar(E.NuevoRepositorio, req.body)), 201, (r) => vistaRepositorio(r, true, o.urlPublica));
  });

  app.patch("/api/repositorios/:id", async (req, rep) => {
    const u = await usuario(req, rep);
    if (!u) return;
    const { id } = validar(E.ConId, req.params);
    const a = validar(E.AjustesRepositorio, req.body);
    const ajustes = { ...(a.politica === undefined ? {} : { politica: a.politica }), ...(a.bloquearMerge === undefined ? {} : { bloquearMerge: a.bloquearMerge }) };
    return responder(rep, await p.repositorios.configurar(u, id as RepositorioId, ajustes), 200, (r) => vistaRepositorio(r, true, o.urlPublica));
  });

  app.delete("/api/repositorios/:id", async (req, rep) => {
    const u = await usuario(req, rep);
    if (!u) return;
    const { id } = validar(E.ConId, req.params);
    return responder(rep, await p.repositorios.desconectar(u, id as RepositorioId), 200, (r) => vistaRepositorio(r, true, o.urlPublica));
  });

  // RF-S03 y RF-S04 — revisiones

  app.get("/api/revisiones", async (req, rep) => {
    const u = await usuario(req, rep);
    if (!u) return;
    const f = validar(E.FiltroRevisiones, req.query);
    const r = await p.revisiones.listar(u, f.repositorio as RepositorioId | undefined);
    const rs = await repos(u);
    return responder(rep, r, 200, (xs) => xs.map((x) => vistaRevision(x, rs.get(x.repositorioId))));
  });

  app.post("/api/revisiones", async (req, rep) => {
    const u = await usuario(req, rep);
    if (!u) return;
    const b = validar(E.SolicitudRevision, req.body);
    const r = await p.revisiones.solicitarRevision(u, b.repositorioId as RepositorioId, b.numeroPr);
    const rs = await repos(u);
    return responder(rep, r, 202, (x) => vistaRevision(x, rs.get(x.repositorioId)));
  });

  app.get("/api/revisiones/:id", async (req, rep) => {
    const u = await usuario(req, rep);
    if (!u) return;
    const { id } = validar(E.ConId, req.params);
    return responder(rep, await p.revisiones.detalle(u, id as RevisionId), 200, (d) => ({
      ...vistaRevision(d.revision, d.repositorio),
      hallazgos: d.hallazgos.map((h) => vistaHallazgo(h, (x) => d.clasificadores.get(x as UsuarioId))),
    }));
  });

  app.post("/api/revisiones/:id/reintento", async (req, rep) => {
    const u = await usuario(req, rep);
    if (!u) return;
    const { id } = validar(E.ConId, req.params);
    const r = await p.revisiones.reintentar(u, id as RevisionId);
    const rs = await repos(u);
    return responder(rep, r, 202, (x) => vistaRevision(x, rs.get(x.repositorioId)));
  });

  // RF-S05 — clasificar

  app.patch("/api/hallazgos/:id", async (req, rep) => {
    const u = await usuario(req, rep);
    if (!u) return;
    const { id } = validar(E.ConId, req.params);
    return responder(rep, await p.revisiones.clasificar(u, id as HallazgoId, validar(E.Clasificar, req.body).clasificacion), 200, (h) => vistaHallazgo(h, () => u.nombre));
  });

  // RF-S03 — webhook de GitHub (sin sesión: lo autentica la firma)

  app.post("/webhooks/github", async (req, rep) => {
    const evento = req.headers["x-github-event"];
    const firma = req.headers["x-hub-signature-256"];
    const b = validar(E.EventoGitHub, req.body);
    const pr = b.pull_request;
    const r = await p.revisiones.recibirWebhook({
      evento: typeof evento === "string" ? evento : "",
      repositorio: b.repository.full_name,
      cuerpo: req.cuerpoCrudo,
      firma: typeof firma === "string" ? firma : undefined,
      ...(pr && b.action !== undefined
        ? { pullRequest: { accion: b.action, numero: pr.number, titulo: pr.title, autor: pr.user.login, shaCabeza: pr.head.sha } }
        : {}),
    });
    if (!r.ok) return enviarError(rep, r.error);
    return rep.code(r.valor.tipo === "Encolada" ? 202 : 200).send(r.valor);
  });

  if (o.frontend !== undefined) {
    void app.register(estaticos, { root: o.frontend, wildcard: false });
    // Las rutas del frontend (p. ej. /revisiones/<id>, el enlace que va a GitHub) cargan la SPA.
    app.setNotFoundHandler((req, rep) => {
      if (req.method === "GET" && !req.url.startsWith("/api/") && !req.url.startsWith("/webhooks/")) return rep.sendFile("index.html");
      return rep.code(404).send({ error: { codigo: "NoEncontrado", mensaje: "La ruta no existe." } });
    });
  }

  return app;
}
