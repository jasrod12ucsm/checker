import { inalcanzable } from "./resultado";

/**
 * Por qué falló una llamada al servicio. `Negocio` trae el código y el mensaje que decidió el servicio
 * (`{"error": {codigo, mensaje}}`); los otros tres son fallas del camino, no del negocio.
 */
export type ErrorApi =
  | { readonly tipo: "Negocio"; readonly estado: number; readonly codigo: string; readonly mensaje: string }
  | { readonly tipo: "SinSesion"; readonly mensaje: string }
  | { readonly tipo: "Red"; readonly detalle: string }
  | { readonly tipo: "RespuestaInvalida"; readonly detalle: string };

/** El texto que ve la persona. El servicio ya redacta los de negocio; el panel solo redacta los del camino. */
export function mensajeDe(e: ErrorApi): string {
  switch (e.tipo) {
    case "Negocio":
    case "SinSesion":
      return e.mensaje;
    case "Red":
      return "No se pudo contactar con Centinela. Revisa tu conexión e inténtalo de nuevo.";
    case "RespuestaInvalida":
      return "Centinela respondió algo inesperado. Recarga la página; si sigue, avisa al administrador.";
    default:
      return inalcanzable(e);
  }
}

/** Un error de negocio con ese código (p. ej. `EmailEnUso`), para reaccionar a él en una pantalla. */
export const esCodigo = (e: ErrorApi, codigo: string): boolean => e.tipo === "Negocio" && e.codigo === codigo;
