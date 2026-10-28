// Cómo se lee una revisión en el panel: etiquetas, filtros, agrupación de hallazgos. Todo puro.
import { inalcanzable } from "./resultado";
import type { Clasificacion, DetalleRevision, EstadoRevision, Hallazgo, Politica, Resumen, Revision } from "./modelo";

export type Tono = "info" | "peligro" | "exito" | "neutro" | "aviso";

export interface Etiqueta {
  readonly texto: string;
  readonly tono: Tono;
}

export function etiquetaEstado(e: EstadoRevision): Etiqueta {
  switch (e.tipo) {
    case "Pendiente":
      return { texto: "Pendiente", tono: "info" };
    case "EnAnalisis":
      return { texto: "En análisis", tono: "info" };
    case "Fallida":
      return { texto: "Fallida", tono: "neutro" };
    case "Publicada":
      return e.veredicto === "Aprobada" ? { texto: "Publicada · Aprobada", tono: "exito" } : { texto: "Publicada · Con problemas", tono: "peligro" };
    default:
      return inalcanzable(e);
  }
}

/** El filtro «Estado» de la lista. `Aprobada` y `ConProblemas` son dos caras de `Publicada`. */
export type FiltroEstado = "Todos" | "EnCurso" | "Aprobada" | "ConProblemas" | "Fallida";

export const FILTROS_ESTADO: readonly { readonly valor: FiltroEstado; readonly texto: string }[] = [
  { valor: "Todos", texto: "Todos" },
  { valor: "EnCurso", texto: "En curso" },
  { valor: "ConProblemas", texto: "Con problemas" },
  { valor: "Aprobada", texto: "Aprobadas" },
  { valor: "Fallida", texto: "Fallidas" },
];

export function cumpleFiltro(e: EstadoRevision, f: FiltroEstado): boolean {
  switch (f) {
    case "Todos":
      return true;
    case "EnCurso":
      return enCurso(e);
    case "Aprobada":
    case "ConProblemas":
      return e.tipo === "Publicada" && e.veredicto === f;
    case "Fallida":
      return e.tipo === "Fallida";
    default:
      return inalcanzable(f);
  }
}

export const enCurso = (e: EstadoRevision): boolean => e.tipo === "Pendiente" || e.tipo === "EnAnalisis";

/** Mientras alguna revisión siga en curso, la lista se vuelve a pedir sola. */
export const hayEnCurso = (rs: readonly Revision[]): boolean => rs.some((r) => enCurso(r.estado));

/** Reintentar solo desde un estado terminado (la misma ley que el servicio). */
export const puedeReintentar = (e: EstadoRevision): boolean => e.tipo === "Publicada" || e.tipo === "Fallida";

export const commitCorto = (sha: string): string => sha.slice(0, 7);

/** «1 confirmados · 1 posibles · 0 descartados», como en la tabla de revisiones. */
export const textoResumen = (r: Resumen): string => `${r.confirmados} confirmados · ${r.posibles} posibles · ${r.suprimidos} descartados`;

export const textoPolitica = (p: Politica): string => (p === "Possibly" ? "También posibles" : "Solo confirmados");

const plural = (n: number, uno: string, varios: string) => `${n} ${n === 1 ? uno : varios}`;

/** El veredicto en una frase para la cabecera del detalle. */
export function textoVeredicto(e: EstadoRevision, politica: Politica | undefined): string {
  switch (e.tipo) {
    case "Pendiente":
      return "En cola: el trabajador la tomará en unos segundos.";
    case "EnAnalisis":
      return "Analizando los archivos C++ cambiados con el checker.";
    case "Fallida":
      return `No se pudo completar: ${e.motivo}`;
    case "Publicada": {
      const r = e.resumen;
      const con = politica === undefined ? "" : ` (política ${politica})`;
      if (e.veredicto === "Aprobada") return `Sin usos de referencias invalidadas en ${plural(r.archivosAnalizados, "archivo", "archivos")}${con}.`;
      const partes = [r.confirmados > 0 ? plural(r.confirmados, "uso confirmado", "usos confirmados") : "", r.posibles > 0 ? plural(r.posibles, "posible", "posibles") : ""].filter((x) => x !== "");
      return `Veredicto: ${partes.join(" y ")} de una referencia invalidada${con}.`;
    }
    default:
      return inalcanzable(e);
  }
}

export interface GrupoArchivo {
  readonly archivo: string;
  readonly hallazgos: readonly Hallazgo[];
}

/**
 * Los hallazgos agrupados por archivo, en orden de archivo y de línea. Los marcados como falso positivo
 * se ocultan salvo que se pida verlos; un archivo sin hallazgos visibles no aparece.
 */
export function agruparPorArchivo(hs: readonly Hallazgo[], mostrarFalsos: boolean): readonly GrupoArchivo[] {
  const visibles = hs.filter((h) => mostrarFalsos || h.clasificacion !== "FalsoPositivo");
  const porArchivo = new Map<string, Hallazgo[]>();
  for (const h of [...visibles].sort((a, b) => a.archivo.localeCompare(b.archivo) || a.linea - b.linea || a.columna - b.columna)) {
    const lista = porArchivo.get(h.archivo);
    if (lista) lista.push(h);
    else porArchivo.set(h.archivo, [h]);
  }
  return [...porArchivo].map(([archivo, hallazgos]) => ({ archivo, hallazgos }));
}

export const cuantosFalsos = (hs: readonly Hallazgo[]): number => hs.filter((h) => h.clasificacion === "FalsoPositivo").length;

/** Reemplaza un hallazgo recién clasificado sin volver a pedir la revisión. */
export const conHallazgo = (d: DetalleRevision, h: Hallazgo): DetalleRevision => ({ ...d, hallazgos: d.hallazgos.map((x) => (x.id === h.id ? h : x)) });

export const CLASIFICACIONES: readonly { readonly valor: Clasificacion; readonly texto: string }[] = [
  { valor: "SinRevisar", texto: "Sin revisar" },
  { valor: "Confirmado", texto: "Confirmado" },
  { valor: "FalsoPositivo", texto: "Falso positivo" },
];

/** Enlace al archivo en el PR de GitHub (pestaña de archivos). */
export const enlaceArchivos = (r: Revision): string | null => (r.pr.enlace === null ? null : `${r.pr.enlace}/files`);

/** Partes de un mensaje: lo que va entre comillas simples (`'std::vector::push_back'`) se muestra como código. */
export function partesMensaje(m: string): readonly { readonly codigo: boolean; readonly texto: string }[] {
  return m
    .split(/'([^']+)'/)
    .map((texto, i) => ({ codigo: i % 2 === 1, texto }))
    .filter((p) => p.texto !== "");
}
