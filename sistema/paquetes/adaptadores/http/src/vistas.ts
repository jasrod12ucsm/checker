// Dominio → JSON de la API. Lo que no está aquí no sale del servidor (el hash de la clave, por ejemplo).
import type { Usuario } from "@centinela/identidad";
import type { Repositorio } from "@centinela/repositorios";
import type { Hallazgo, Revision } from "@centinela/revisiones";

const iso = (ms: number) => new Date(ms).toISOString();

export const vistaUsuario = (u: Usuario) => ({ id: u.id, email: u.email, nombre: u.nombre, rol: u.rol, estado: u.estado, creadoEn: iso(u.creadoEn) });

/** El secreto del webhook solo lo ve quien administra repositorios. */
export const vistaRepositorio = (r: Repositorio, conSecreto: boolean, urlPublica: string) => ({
  id: r.id,
  nombre: r.nombre,
  politica: r.politica,
  bloquearMerge: r.bloquearMerge,
  activo: r.activo,
  conectadoEn: iso(r.conectadoEn),
  webhook: conSecreto ? { url: `${urlPublica.replace(/\/$/, "")}/webhooks/github`, secreto: r.secretoWebhook, tipoContenido: "application/json", eventos: ["pull_request"] } : null,
});

export function vistaRevision(r: Revision, repo: Repositorio | undefined) {
  const e = r.estado;
  const estado =
    e.tipo === "Pendiente"
      ? { tipo: e.tipo, desde: iso(e.encoladaEn) }
      : e.tipo === "EnAnalisis"
        ? { tipo: e.tipo, desde: iso(e.iniciadaEn) }
        : e.tipo === "Fallida"
          ? { tipo: e.tipo, desde: iso(e.terminadaEn), motivo: e.motivo }
          : { tipo: e.tipo, desde: iso(e.terminadaEn), veredicto: e.veredicto, resumen: e.resumen };
  return {
    id: r.id,
    repositorio: repo ? { id: repo.id, nombre: repo.nombre } : null,
    pr: { ...r.pr, enlace: repo ? `https://github.com/${repo.nombre}/pull/${r.pr.numero}` : null },
    origen: r.origen,
    solicitadaPor: r.solicitadaPor,
    creadaEn: iso(r.creadaEn),
    intentos: r.intentos,
    estado,
  };
}

/** `nombreDe` resuelve el nombre de quien clasificó; si ya no existe, sale solo su id. */
export const vistaHallazgo = (h: Hallazgo, nombreDe: (id: string) => string | undefined = () => undefined) => ({
  id: h.id,
  archivo: h.archivo,
  linea: h.linea,
  columna: h.columna,
  clase: h.clase,
  mensaje: h.mensaje,
  ruta: h.ruta,
  huella: h.huella,
  clasificacion: h.clasificacion,
  clasificadoPor: h.clasificadoPor === null ? null : { id: h.clasificadoPor.por, nombre: nombreDe(h.clasificadoPor.por) ?? null },
  clasificadoEn: h.clasificadoPor === null ? null : iso(h.clasificadoPor.en),
});
