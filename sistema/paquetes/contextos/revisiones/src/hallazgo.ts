import type { HallazgoId, Instante, Marca, Positivo, RevisionId, UsuarioId } from "@centinela/kernel";

/** `Confirmado`: el uso es inválido en toda ejecución. `Posible`: depende de la capacidad o del rehash. */
export type ClaseHallazgo = "Confirmado" | "Posible";

/** Lo que dice una persona del hallazgo. `FalsoPositivo` lo suprime en las revisiones siguientes del repositorio. */
export type Clasificacion = "SinRevisar" | "Confirmado" | "FalsoPositivo";

/** Un paso de la ruta que explica el aviso: dónde se obtuvo el handle, qué lo invalidó. */
export interface Nota {
  readonly archivo: string;
  readonly linea: Positivo;
  readonly mensaje: string;
}

/** Un aviso tal como lo entrega el analizador, ya traducido del texto de clang. */
export interface Aviso {
  readonly archivo: string;
  readonly linea: Positivo;
  readonly columna: Positivo;
  readonly clase: ClaseHallazgo;
  readonly mensaje: string;
  readonly ruta: readonly Nota[];
}

/** Identifica "el mismo problema" entre commits: archivo y mensaje, sin números de línea. */
export type Huella = Marca<string, "Huella">;

export function huella(aviso: Pick<Aviso, "archivo" | "mensaje">): Huella {
  const normal = aviso.mensaje.replace(/\(l[ií]nea \d+\)/g, "").replace(/\s+/g, " ").trim();
  // FNV-1a de 32 bits: estable, sin dependencias y suficiente para agrupar dentro de un repositorio.
  let h = 0x811c9dc5;
  for (const c of `${aviso.archivo}\u0000${normal}`) {
    h ^= c.codePointAt(0)!;
    h = Math.imul(h, 0x01000193) >>> 0;
  }
  return h.toString(16).padStart(8, "0") as Huella;
}

/** Quién clasificó un hallazgo y cuándo. Van juntos: no hay autor sin fecha ni fecha sin autor. */
export interface Autoria {
  readonly por: UsuarioId;
  readonly en: Instante;
}

export interface Hallazgo extends Aviso {
  readonly id: HallazgoId;
  readonly revisionId: RevisionId;
  readonly huella: Huella;
  readonly clasificacion: Clasificacion;
  /** `null` si nadie lo clasificó todavía, o si nació suprimido por un descarte anterior del repositorio. */
  readonly clasificadoPor: Autoria | null;
}

/** Un hallazgo marcado como falso positivo no cuenta para el veredicto ni se comenta en el PR. */
export const suprimido = (h: Pick<Hallazgo, "clasificacion">): boolean => h.clasificacion === "FalsoPositivo";

/** Lo que entrega el analizador para un commit. */
export interface Analisis {
  readonly analizados: number;
  /** Archivos que clang no pudo compilar (p. ej. faltan cabeceras generadas): no se analizaron. */
  readonly noCompilados: readonly string[];
  readonly avisos: readonly Aviso[];
}
