import type { Instante, Positivo, RepositorioId, RevisionId, UsuarioId } from "@centinela/kernel";

export type Pendiente = { readonly tipo: "Pendiente"; readonly encoladaEn: Instante };
export type EnAnalisis = { readonly tipo: "EnAnalisis"; readonly iniciadaEn: Instante };
export type Publicada = {
  readonly tipo: "Publicada";
  readonly terminadaEn: Instante;
  readonly veredicto: Veredicto;
  readonly resumen: Resumen;
};
export type Fallida = { readonly tipo: "Fallida"; readonly terminadaEn: Instante; readonly motivo: string };

/** Pendiente → EnAnalisis → Publicada | Fallida; Publicada | Fallida → Pendiente al reintentar. */
export type EstadoRevision = Pendiente | EnAnalisis | Publicada | Fallida;

/** `ConProblemas`: hay al menos un hallazgo no suprimido. */
export type Veredicto = "Aprobada" | "ConProblemas";

export interface Resumen {
  readonly archivosAnalizados: number;
  readonly noCompilados: number;
  readonly confirmados: number;
  readonly posibles: number;
  readonly suprimidos: number;
}

export type Origen = "webhook" | "manual";

export interface PullRequest {
  readonly numero: Positivo;
  readonly titulo: string;
  readonly autor: string;
  readonly shaCabeza: string;
}

/** Una revisión es el análisis de un commit (la cabeza de un PR) de un repositorio. */
export interface Revision<E extends EstadoRevision = EstadoRevision> {
  readonly id: RevisionId;
  readonly repositorioId: RepositorioId;
  readonly pr: PullRequest;
  readonly origen: Origen;
  readonly solicitadaPor: UsuarioId | null;
  readonly creadaEn: Instante;
  readonly intentos: number;
  readonly estado: E;
}

export const es =
  <T extends EstadoRevision["tipo"]>(tipo: T) =>
  (r: Revision): r is Revision<Extract<EstadoRevision, { tipo: T }>> =>
    r.estado.tipo === tipo;
export const esPendiente = es("Pendiente");
export const esEnAnalisis = es("EnAnalisis");
