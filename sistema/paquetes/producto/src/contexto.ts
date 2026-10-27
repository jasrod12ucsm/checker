import { err, ok, type GeneradorIds, type Reloj, type Resultado } from "@centinela/kernel";
import { Autorizado, type Permiso, type Usuario } from "@centinela/identidad";
import type { ErrorProducto } from "./errores";
import type { Almacen, Analizador, Bitacora, Claves, Fuentes, GitHub, Secretos } from "./puertos";

export interface Dependencias {
  readonly almacen: Almacen;
  readonly claves: Claves;
  readonly secretos: Secretos;
  readonly github: GitHub;
  readonly fuentes: Fuentes;
  readonly analizador: Analizador;
  readonly reloj: Reloj;
  readonly ids: GeneradorIds;
  readonly bitacora: Bitacora;
  /** URL con la que el navegador llega al sistema; va en los enlaces que se publican en GitHub. */
  readonly urlPublica: string;
}

export type R<T> = Promise<Resultado<T, ErrorProducto>>;

export const autorizar = <P extends Permiso>(actor: Usuario, permiso: P) => Autorizado.para(actor, permiso);

export function encontrado<T>(x: T | undefined, error: ErrorProducto): Resultado<T, ErrorProducto> {
  return x === undefined ? err(error) : ok(x);
}

export const enlaceRevision = (d: Dependencias, id: string) => `${d.urlPublica.replace(/\/$/, "")}/revisiones/${id}`;
