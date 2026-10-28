// El adaptador HTTP del puerto `Api`: el único archivo del panel que llama a `fetch`.
// Nunca lanza: la red caída, un error de negocio o una respuesta fuera de contrato vuelven como `ErrorApi`.
import { z } from "zod";
import type { ErrorApi } from "../dominio/errores";
import { err, ok, type Resultado } from "../dominio/resultado";
import * as D from "./esquemas";
import type { Api } from "./puerto";

export type Fetch = (url: string, init: RequestInit) => Promise<Response>;

type Metodo = "GET" | "POST" | "PATCH" | "DELETE";

async function leerJson(r: Response): Promise<unknown> {
  const texto = await r.text();
  return texto === "" ? undefined : JSON.parse(texto);
}

/** Traduce una respuesta de error del servicio. La sesión vencida se distingue: el panel vuelve al ingreso. */
function errorDe(estado: number, cuerpo: unknown): ErrorApi {
  const e = D.ErrorDto.safeParse(cuerpo);
  if (!e.success) return { tipo: "RespuestaInvalida", detalle: `HTTP ${estado} sin cuerpo de error` };
  if (e.data.error.codigo === "SesionInvalida") return { tipo: "SinSesion", mensaje: e.data.error.mensaje };
  return { tipo: "Negocio", estado, codigo: e.data.error.codigo, mensaje: e.data.error.mensaje };
}

export function apiHttp(f: Fetch = (u, i) => fetch(u, i), base = ""): Api {
  async function pedir<S extends z.ZodType>(metodo: Metodo, ruta: string, esquema: S, cuerpo?: unknown): Promise<Resultado<z.output<S>, ErrorApi>> {
    let r: Response;
    try {
      r = await f(`${base}${ruta}`, {
        method: metodo,
        credentials: "same-origin",
        headers: cuerpo === undefined ? { accept: "application/json" } : { accept: "application/json", "content-type": "application/json" },
        ...(cuerpo === undefined ? {} : { body: JSON.stringify(cuerpo) }),
      });
    } catch (e) {
      return err({ tipo: "Red", detalle: String(e) });
    }
    let json: unknown;
    try {
      json = await leerJson(r);
    } catch {
      return err({ tipo: "RespuestaInvalida", detalle: `HTTP ${r.status}: el cuerpo no es JSON` });
    }
    if (!r.ok) return err(errorDe(r.status, json));
    const v = esquema.safeParse(json);
    return v.success ? ok(v.data) : err({ tipo: "RespuestaInvalida", detalle: `${metodo} ${ruta}: ${v.error.issues.map((i) => `${i.path.join(".")} ${i.message}`).join("; ")}` });
  }

  const id = encodeURIComponent;

  return {
    estadoRegistro: () => pedir("GET", "/api/registro", D.EstadoRegistroDto),
    registrar: (d) => pedir("POST", "/api/registro", D.RegistroDto, d),
    ingresar: (d) => pedir("POST", "/api/sesion", D.UsuarioDto, d),
    sesion: () => pedir("GET", "/api/sesion", D.UsuarioDto),
    salir: () => pedir("DELETE", "/api/sesion", z.undefined()),

    usuarios: () => pedir("GET", "/api/usuarios", D.UsuarioDto.array()),
    crearUsuario: (d) => pedir("POST", "/api/usuarios", D.UsuarioDto, d),
    actualizarUsuario: (u, c) => pedir("PATCH", `/api/usuarios/${id(u)}`, D.UsuarioDto, c),

    repositorios: () => pedir("GET", "/api/repositorios", D.RepositorioDto.array()),
    conectar: (d) => pedir("POST", "/api/repositorios", D.RepositorioDto, d),
    configurar: (r, a) => pedir("PATCH", `/api/repositorios/${id(r)}`, D.RepositorioDto, a),
    desconectar: (r) => pedir("DELETE", `/api/repositorios/${id(r)}`, D.RepositorioDto),

    revisiones: (repo) => pedir("GET", repo === undefined ? "/api/revisiones" : `/api/revisiones?repositorio=${id(repo)}`, D.RevisionDto.array()),
    revision: (r) => pedir("GET", `/api/revisiones/${id(r)}`, D.DetalleDto),
    solicitar: (repositorioId, numeroPr) => pedir("POST", "/api/revisiones", D.RevisionDto, { repositorioId, numeroPr }),
    reintentar: (r) => pedir("POST", `/api/revisiones/${id(r)}/reintento`, D.RevisionDto),
    clasificar: (h, clasificacion) => pedir("PATCH", `/api/hallazgos/${id(h)}`, D.HallazgoDto, { clasificacion }),
  };
}
