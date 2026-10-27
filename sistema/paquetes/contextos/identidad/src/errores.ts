import type { ErrorValor } from "@centinela/kernel";
import type { Permiso } from "./usuario";

/** Lo que puede salir mal en el contexto de identidad. El HTTP lo traduce en un solo archivo. */
export type ErrorIdentidad =
  | ErrorValor
  | { readonly tipo: "CredencialesInvalidas" }
  | { readonly tipo: "SesionInvalida" }
  | { readonly tipo: "UsuarioPendiente" }
  | { readonly tipo: "UsuarioDesactivado" }
  | { readonly tipo: "SinPermiso"; readonly permiso: Permiso }
  | { readonly tipo: "EmailEnUso" }
  | { readonly tipo: "ClaveDebil"; readonly motivo: string }
  | { readonly tipo: "NoPuedeModificarseASiMismo" }
  | { readonly tipo: "UsuarioNoEncontrado" };
