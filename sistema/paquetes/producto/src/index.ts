export type * from "./puertos";
export type * from "./errores";
export * from "./contexto";
export * from "./casos-identidad";
export * from "./casos-repositorios";
export * from "./casos-revisiones";

import type { Dependencias } from "./contexto";
import { casosIdentidad } from "./casos-identidad";
import { casosRepositorios } from "./casos-repositorios";
import { casosRevisiones } from "./casos-revisiones";

/** Todos los casos de uso del sistema, con sus dependencias ya inyectadas. */
export function producto(d: Dependencias) {
  return { identidad: casosIdentidad(d), repositorios: casosRepositorios(d), revisiones: casosRevisiones(d) };
}
export type Producto = ReturnType<typeof producto>;
