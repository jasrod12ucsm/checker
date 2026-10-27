/** Resultado de una operación que puede fallar con un error de dominio, sin excepciones. */
export type Resultado<T, E> =
  | { readonly ok: true; readonly valor: T }
  | { readonly ok: false; readonly error: E };

export const ok = <T>(valor: T): Resultado<T, never> => ({ ok: true, valor });
export const err = <E>(error: E): Resultado<never, E> => ({ ok: false, error });

/** Para el adaptador o la prueba que ya comprobó `ok`: devuelve el valor o lanza. */
export function desenvolver<T, E>(r: Resultado<T, E>): T {
  if (r.ok) return r.valor;
  throw new Error(`desenvolver sobre un error: ${JSON.stringify(r.error)}`);
}

/** Marca el final de un `switch` exhaustivo: si falta un caso, no compila. */
export function inalcanzable(x: never): never {
  throw new Error(`caso no contemplado: ${JSON.stringify(x)}`);
}
