import type { ErrorIdentidad } from "@centinela/identidad";
import type { ErrorRepositorios } from "@centinela/repositorios";
import type { ErrorRevisiones } from "@centinela/revisiones";

/** Todos los errores que un caso de uso devuelve; el adaptador HTTP los traduce en `errores.ts`. */
export type ErrorProducto =
  | ErrorIdentidad
  | ErrorRepositorios
  | ErrorRevisiones
  | { readonly tipo: "FirmaInvalida" }
  | { readonly tipo: "ErrorGitHub"; readonly detalle: string };
