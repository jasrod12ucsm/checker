// Lo que el panel sabe del servicio: el contrato de la API (libro, «API HTTP»), ya validado en la frontera.
// Los estados son uniones con nombre: cada variante lleva solo sus datos.

export type Rol = "administrador" | "desarrollador";
export type EstadoUsuario = "Pendiente" | "Activo" | "Desactivado";
/** Lo que un administrador decide sobre una cuenta: nadie vuelve a quedar pendiente. */
export type Decision = Exclude<EstadoUsuario, "Pendiente">;

export interface Usuario {
  readonly id: string;
  readonly email: string;
  readonly nombre: string;
  readonly rol: Rol;
  readonly estado: EstadoUsuario;
  readonly creadoEn: string;
}

export type Politica = "Silent" | "Possibly";

export interface Webhook {
  readonly url: string;
  readonly secreto: string;
  readonly tipoContenido: string;
  readonly eventos: readonly string[];
}

export interface Repositorio {
  readonly id: string;
  readonly nombre: string;
  readonly politica: Politica;
  readonly bloquearMerge: boolean;
  readonly activo: boolean;
  readonly conectadoEn: string;
  /** Solo lo recibe quien administra repositorios. */
  readonly webhook: Webhook | null;
}

export interface Resumen {
  readonly archivosAnalizados: number;
  readonly noCompilados: number;
  readonly confirmados: number;
  readonly posibles: number;
  readonly suprimidos: number;
}

export type Veredicto = "Aprobada" | "ConProblemas";

export type EstadoRevision =
  | { readonly tipo: "Pendiente"; readonly desde: string }
  | { readonly tipo: "EnAnalisis"; readonly desde: string }
  | { readonly tipo: "Fallida"; readonly desde: string; readonly motivo: string }
  | { readonly tipo: "Publicada"; readonly desde: string; readonly veredicto: Veredicto; readonly resumen: Resumen };

export type Origen = "webhook" | "manual";

export interface PullRequest {
  readonly numero: number;
  readonly titulo: string;
  readonly autor: string;
  readonly shaCabeza: string;
  readonly enlace: string | null;
}

export interface Revision {
  readonly id: string;
  readonly repositorio: { readonly id: string; readonly nombre: string } | null;
  readonly pr: PullRequest;
  readonly origen: Origen;
  readonly solicitadaPor: string | null;
  readonly creadaEn: string;
  readonly intentos: number;
  readonly estado: EstadoRevision;
}

export type ClaseHallazgo = "Confirmado" | "Posible";
export type Clasificacion = "SinRevisar" | "Confirmado" | "FalsoPositivo";

export interface Paso {
  readonly archivo: string;
  readonly linea: number;
  readonly mensaje: string;
}

/** Quién clasificó y cuándo: van juntos o no van. */
export interface Autoria {
  readonly por: { readonly id: string; readonly nombre: string | null };
  readonly en: string;
}

export interface Hallazgo {
  readonly id: string;
  readonly archivo: string;
  readonly linea: number;
  readonly columna: number;
  readonly clase: ClaseHallazgo;
  readonly mensaje: string;
  readonly ruta: readonly Paso[];
  readonly huella: string;
  readonly clasificacion: Clasificacion;
  readonly autoria: Autoria | null;
}

export interface DetalleRevision extends Revision {
  readonly hallazgos: readonly Hallazgo[];
}
