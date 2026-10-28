/** Resultado de una operación que puede fallar, sin excepciones (el mismo contrato que el kernel del servicio). */
export type Resultado<T, E> =
  | { readonly ok: true; readonly valor: T }
  | { readonly ok: false; readonly error: E };

export const ok = <T>(valor: T): Resultado<T, never> => ({ ok: true, valor });
export const err = <E>(error: E): Resultado<never, E> => ({ ok: false, error });

/** Marca el final de un `switch` exhaustivo: si falta un caso, no compila. */
export function inalcanzable(x: never): never {
  throw new Error(`caso no contemplado: ${JSON.stringify(x)}`);
}
