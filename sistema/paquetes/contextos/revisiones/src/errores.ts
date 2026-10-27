import type { ErrorValor } from "@centinela/kernel";
import type { EstadoRevision } from "./revision";

export type ErrorRevisiones =
  | ErrorValor
  | { readonly tipo: "RevisionNoEncontrada" }
  | { readonly tipo: "HallazgoNoEncontrado" }
  | { readonly tipo: "RevisionEnCurso" }
  | { readonly tipo: "ShaYaRevisado"; readonly estado: EstadoRevision["tipo"] }
  | { readonly tipo: "TransicionInvalida"; readonly desde: EstadoRevision["tipo"]; readonly hacia: EstadoRevision["tipo"] };
