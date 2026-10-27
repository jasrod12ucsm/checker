import { inalcanzable } from "@centinela/kernel";
import type { Repositorio } from "@centinela/repositorios";
import { suprimido, type Hallazgo } from "./hallazgo";
import type { Revision } from "./revision";

/** El estado del commit que ve GitHub; con `failure` y la regla de protección, el merge se bloquea. */
export interface EstadoCommit {
  readonly estado: "pending" | "success" | "failure" | "error";
  readonly descripcion: string;
}

export const CONTEXTO_ESTADO = "centinela/invalidacion";

export function estadoCommit(repo: Repositorio, r: Revision): EstadoCommit {
  const e = r.estado;
  switch (e.tipo) {
    case "Pendiente":
      return { estado: "pending", descripcion: "En cola" };
    case "EnAnalisis":
      return { estado: "pending", descripcion: "Analizando" };
    case "Fallida":
      return { estado: "error", descripcion: `El análisis falló: ${e.motivo}`.slice(0, 140) };
    case "Publicada": {
      const n = e.resumen.confirmados + e.resumen.posibles;
      if (e.veredicto === "Aprobada") return { estado: "success", descripcion: "Sin usos de handles invalidados" };
      const texto = `${e.resumen.confirmados} confirmados, ${e.resumen.posibles} posibles`;
      return repo.bloquearMerge
        ? { estado: "failure", descripcion: texto }
        : { estado: "success", descripcion: `${texto} (${n === 1 ? "no bloquea" : "no bloquean"} el merge)` };
    }
    default:
      return inalcanzable(e);
  }
}

/** Texto de un comentario en línea del PR. */
export function comentario(h: Hallazgo): string {
  const titulo = h.clase === "Confirmado" ? "**Uso de un handle invalidado**" : "**Uso de un handle posiblemente invalidado**";
  const ruta = h.ruta.map((n) => `- línea ${n.linea}: ${n.mensaje}`).join("\n");
  return `${titulo} · \`ucsm.ContainerInvalidation\`\n\n${h.mensaje}${ruta ? `\n\n${ruta}` : ""}`;
}

/** Cuerpo de la revisión del PR: el resumen y los hallazgos que no caen en líneas del diff. */
export function cuerpo(r: Revision, fueraDelDiff: readonly Hallazgo[], enlace: string): string {
  if (r.estado.tipo !== "Publicada") return "";
  const s = r.estado.resumen;
  const lineas = [
    `### Centinela C++ — ${r.estado.veredicto === "Aprobada" ? "sin problemas" : "se encontraron problemas"}`,
    "",
    `${s.archivosAnalizados} archivos analizados · ${s.confirmados} confirmados · ${s.posibles} posibles · ${s.suprimidos} descartados como falso positivo`,
  ];
  if (s.noCompilados > 0) lineas.push("", `${s.noCompilados} archivos no compilaron y no se analizaron (por ejemplo, faltan cabeceras generadas).`);
  const fuera = fueraDelDiff.filter((h) => !suprimido(h));
  if (fuera.length > 0) {
    lineas.push("", "Fuera de las líneas modificadas:");
    for (const h of fuera) lineas.push(`- \`${h.archivo}:${h.linea}\` (${h.clase.toLowerCase()}): ${h.mensaje}`);
  }
  lineas.push("", `[Ver la revisión en Centinela](${enlace})`);
  return lineas.join("\n");
}
