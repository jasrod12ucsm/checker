import { err, ok, type HallazgoId, type Instante, type Resultado, type RevisionId, type UsuarioId } from "@centinela/kernel";
import type { Autorizado } from "@centinela/identidad";
import type { Repositorio } from "@centinela/repositorios";
import type { ErrorRevisiones } from "./errores";
import { huella, suprimido, type Analisis, type Clasificacion, type Hallazgo, type Huella } from "./hallazgo";
import type { EnAnalisis, Fallida, Origen, Pendiente, Publicada, PullRequest, Resumen, Revision } from "./revision";

export interface Solicitud {
  readonly id: RevisionId;
  readonly pr: PullRequest;
  readonly origen: Origen;
  readonly solicitadaPor: UsuarioId | null;
}

/**
 * Solicitar: un commit se revisa una sola vez. Si ya hay una revisión de ese sha,
 * no se crea otra (para repetirla está `reintentar`).
 */
export function solicitar(
  repo: Repositorio,
  existenteDelSha: Revision | undefined,
  s: Solicitud,
  ahora: Instante,
): Resultado<Revision<Pendiente>, ErrorRevisiones | { tipo: "RepositorioDesconectado" }> {
  if (!repo.activo) return err({ tipo: "RepositorioDesconectado" });
  if (existenteDelSha !== undefined) {
    const t = existenteDelSha.estado.tipo;
    return err(t === "Pendiente" || t === "EnAnalisis" ? { tipo: "RevisionEnCurso" } : { tipo: "ShaYaRevisado", estado: t });
  }
  return ok({ ...s, repositorioId: repo.id, creadaEn: ahora, intentos: 1, estado: { tipo: "Pendiente", encoladaEn: ahora } });
}

export function iniciar(r: Revision<Pendiente>, ahora: Instante): Revision<EnAnalisis> {
  return { ...r, estado: { tipo: "EnAnalisis", iniciadaEn: ahora } };
}

export interface Publicacion {
  readonly revision: Revision<Publicada>;
  readonly hallazgos: readonly Hallazgo[];
}

/**
 * Publicar: cada aviso distinto es un hallazgo; los de huella descartada en el
 * repositorio nacen como falso positivo. El veredicto solo mira los no suprimidos.
 */
export function publicar(
  r: Revision<EnAnalisis>,
  analisis: Analisis,
  descartadas: ReadonlySet<Huella>,
  nuevoId: () => HallazgoId,
  ahora: Instante,
): Publicacion {
  const vistos = new Set<string>();
  const hallazgos: Hallazgo[] = [];
  for (const a of analisis.avisos) {
    const clave = `${a.archivo}:${a.linea}:${a.columna}:${a.mensaje}`;
    if (vistos.has(clave)) continue;
    vistos.add(clave);
    const hu = huella(a);
    hallazgos.push({ ...a, id: nuevoId(), revisionId: r.id, huella: hu, clasificacion: descartadas.has(hu) ? "FalsoPositivo" : "SinRevisar", clasificadoPor: null });
  }
  const visibles = hallazgos.filter((h) => !suprimido(h));
  const resumen: Resumen = {
    archivosAnalizados: analisis.analizados,
    noCompilados: analisis.noCompilados.length,
    confirmados: visibles.filter((h) => h.clase === "Confirmado").length,
    posibles: visibles.filter((h) => h.clase === "Posible").length,
    suprimidos: hallazgos.length - visibles.length,
  };
  const veredicto = visibles.length === 0 ? "Aprobada" : "ConProblemas";
  return { revision: { ...r, estado: { tipo: "Publicada", terminadaEn: ahora, veredicto, resumen } }, hallazgos };
}

export function fallar(r: Revision<EnAnalisis>, motivo: string, ahora: Instante): Revision<Fallida> {
  return { ...r, estado: { tipo: "Fallida", terminadaEn: ahora, motivo } };
}

/** Reintentar: solo una revisión terminada vuelve a la cola; los hallazgos anteriores se reemplazan. */
export function reintentar(_por: Autorizado<"solicitar-revision">, r: Revision, ahora: Instante): Resultado<Revision<Pendiente>, ErrorRevisiones> {
  if (r.estado.tipo === "Pendiente" || r.estado.tipo === "EnAnalisis") return err({ tipo: "RevisionEnCurso" });
  return ok({ ...r, intentos: r.intentos + 1, estado: { tipo: "Pendiente", encoladaEn: ahora } });
}

/** Qué hacer con la lista de huellas descartadas del repositorio al clasificar. */
export type CambioDescarte = "agregar" | "quitar" | "ninguno";

/** Clasificar deja registrado quién lo hizo y cuándo: el autor sale del testigo, no de un parámetro. */
export function clasificar(
  por: Autorizado<"clasificar-hallazgos">,
  h: Hallazgo,
  nueva: Clasificacion,
  ahora: Instante,
): { readonly hallazgo: Hallazgo; readonly descarte: CambioDescarte } {
  const antes = suprimido(h);
  const despues = nueva === "FalsoPositivo";
  return { hallazgo: { ...h, clasificacion: nueva, clasificadoPor: { por: por.usuarioId, en: ahora } }, descarte: antes === despues ? "ninguno" : despues ? "agregar" : "quitar" };
}
