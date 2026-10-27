// ACL: traduce la salida de texto de clang (`-analyzer-output=text`) a avisos del dominio.
import type { Positivo } from "@centinela/kernel";
import type { Aviso, Nota } from "@centinela/revisiones";

export const CHECKER = "ucsm.ContainerInvalidation";

// El mismo formato que lee bench/codigo_real.py: archivo:línea:columna: tipo: mensaje [checker]
const LINEA = /^(?<archivo>[^:\s][^:]*):(?<linea>\d+):(?<col>\d+): (?<tipo>warning|note|error): (?<msg>.*?)(?: \[(?<chk>[\w.-]+)\])?$/;

const relativa = (ruta: string) => ruta.replace(/^\.\//, "");

/**
 * Cada `warning` del checker abre un aviso; las `note` que siguen son su ruta.
 * Avisos de otros checkers de CSA (core.*) se ignoran junto con sus notas.
 */
export function leerSalida(texto: string): Aviso[] {
  const avisos: Aviso[] = [];
  let actual: { base: Omit<Aviso, "ruta">; ruta: Nota[] } | undefined;
  const cerrar = () => {
    if (actual) avisos.push({ ...actual.base, ruta: actual.ruta });
    actual = undefined;
  };
  for (const linea of texto.split("\n")) {
    const m = LINEA.exec(linea.trimEnd());
    if (!m?.groups) continue;
    const g = m.groups as { archivo: string; linea: string; col: string; tipo: string; msg: string; chk?: string };
    if (g.tipo === "note") {
      actual?.ruta.push({ archivo: relativa(g.archivo), linea: Number(g.linea) as Positivo, mensaje: g.msg });
      continue;
    }
    cerrar();
    if (g.tipo === "warning" && g.chk === CHECKER) {
      actual = {
        base: {
          archivo: relativa(g.archivo),
          linea: Number(g.linea) as Positivo,
          columna: Number(g.col) as Positivo,
          clase: /posiblemente/i.test(g.msg) ? "Posible" : "Confirmado",
          mensaje: g.msg,
        },
        ruta: [],
      };
    }
  }
  cerrar();
  return avisos;
}
