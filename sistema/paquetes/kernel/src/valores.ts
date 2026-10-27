import type { Marca } from "./marca";
import { err, ok, type Resultado } from "./resultado";

export type ErrorValor = { readonly tipo: "ValorInvalido"; readonly campo: string; readonly motivo: string };
const invalido = (campo: string, motivo: string): ErrorValor => ({ tipo: "ValorInvalido", campo, motivo });

// Identificadores: uno por entidad, para que un UsuarioId no se pase donde va un RevisionId.
export type UsuarioId = Marca<string, "UsuarioId">;
export type RepositorioId = Marca<string, "RepositorioId">;
export type RevisionId = Marca<string, "RevisionId">;
export type HallazgoId = Marca<string, "HallazgoId">;

const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/;
function id<T extends string>(campo: string) {
  return (s: string): Resultado<T, ErrorValor> =>
    UUID.test(s) ? ok(s as T) : err(invalido(campo, "no es un identificador"));
}
export const usuarioId = id<UsuarioId>("usuarioId");
export const repositorioId = id<RepositorioId>("repositorioId");
export const revisionId = id<RevisionId>("revisionId");
export const hallazgoId = id<HallazgoId>("hallazgoId");

/** Correo normalizado a minúsculas. */
export type Email = Marca<string, "Email">;
export function email(s: string): Resultado<Email, ErrorValor> {
  const t = s.trim().toLowerCase();
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(t) && t.length <= 254 ? ok(t as Email) : err(invalido("email", "no es un correo"));
}

/** Texto de 1 a `max` caracteres, sin espacios a los lados. */
export type Texto = Marca<string, "Texto">;
export function texto(campo: string, s: string, max = 200): Resultado<Texto, ErrorValor> {
  const t = s.trim();
  if (t.length === 0) return err(invalido(campo, "está vacío"));
  if (t.length > max) return err(invalido(campo, `tiene más de ${max} caracteres`));
  return ok(t as Texto);
}

/** Momento en milisegundos desde la época. Lo da el puerto Reloj; el dominio no lee la hora del sistema. */
export type Instante = Marca<number, "Instante">;
export const instante = (ms: number): Instante => ms as Instante;
export const despues = (t: Instante, ms: number): Instante => (t + ms) as Instante;

/** Lista con al menos un elemento. */
export type NoVacia<T> = readonly [T, ...T[]];
export const noVacia = <T>(xs: readonly T[]): xs is NoVacia<T> => xs.length > 0;

/** Entero positivo (número de PR, línea). */
export type Positivo = Marca<number, "Positivo">;
export function positivo(campo: string, n: number): Resultado<Positivo, ErrorValor> {
  return Number.isInteger(n) && n > 0 ? ok(n as Positivo) : err(invalido(campo, "no es un entero positivo"));
}
