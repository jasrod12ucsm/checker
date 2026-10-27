import type { Instante } from "./valores";

/** El tiempo y los identificadores vienen de fuera: así el dominio es determinista en las pruebas. */
export interface Reloj {
  ahora(): Instante;
}
export interface GeneradorIds {
  nuevo(): string;
}
