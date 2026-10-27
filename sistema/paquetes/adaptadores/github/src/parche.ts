/**
 * Líneas del lado nuevo que aparecen en un parche unificado de GitHub (agregadas o de contexto).
 * Solo sobre ellas acepta GitHub un comentario con `side: RIGHT`.
 */
export function lineasDelParche(parche: string | undefined): Set<number> {
  const lineas = new Set<number>();
  if (parche === undefined) return lineas;
  let nueva = 0;
  for (const l of parche.split("\n")) {
    const h = /^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@/.exec(l);
    if (h) {
      nueva = Number(h[1]);
      continue;
    }
    if (nueva === 0 || l.startsWith("-") || l.startsWith("\\")) continue;
    lineas.add(nueva++);
  }
  return lineas;
}
