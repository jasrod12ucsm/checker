import { execFile } from "node:child_process";
import { existsSync } from "node:fs";
import { dirname, join } from "node:path";
import type { Politica } from "@centinela/repositorios";
import type { Analisis, Aviso } from "@centinela/revisiones";
import type { Analizador } from "@centinela/producto";
import { CHECKER, leerSalida } from "./salida";

export interface OpcionesClang {
  readonly clang: string;
  /** Ruta a libContainerInvalidation.so. */
  readonly plugin: string;
  readonly estandar: string;
  readonly tiempoMaximoMs: number;
  readonly paralelo: number;
}

export const OPCIONES_CLANG: OpcionesClang = { clang: "clang++", plugin: "", estandar: "c++17", tiempoMaximoMs: 120_000, paralelo: 4 };

/**
 * Los argumentos de una invocación: los de la guía de uso del checker, más el modo de
 * inlining `all` que se usó en código real (D-22): con el modo por defecto, una función ya
 * inlinada no se reanaliza como raíz y un defecto cortado por el presupuesto no se ve.
 */
export function argumentos(o: OpcionesClang, dir: string, archivo: string, politica: Politica): string[] {
  const incluir = [".", "include", "src", dirname(archivo)].filter((d, i, xs) => xs.indexOf(d) === i && existsSync(join(dir, d)));
  return [
    `-std=${o.estandar}`,
    "--analyze",
    "-o",
    "/dev/null",
    "-Xclang", "-load", "-Xclang", o.plugin,
    "-Xclang", `-analyzer-checker=${CHECKER}`,
    "-Xclang", "-analyzer-config", "-Xclang", `${CHECKER}:PolicyMode=${politica}`,
    "-Xclang", "-analyzer-output=text",
    "-Xclang", "-analyzer-inlining-mode=all",
    ...incluir.map((d) => `-I${d}`),
    archivo,
  ];
}

interface Corrida {
  readonly codigo: number | null;
  readonly salida: string;
}

const correr = (o: OpcionesClang, dir: string, args: string[]) =>
  new Promise<Corrida>((ok) => {
    execFile(o.clang, args, { cwd: dir, timeout: o.tiempoMaximoMs, maxBuffer: 16 * 1024 * 1024 }, (e, stdout, stderr) => {
      const codigo = e === null ? 0 : typeof e.code === "number" ? e.code : null;
      ok({ codigo, salida: `${stdout}\n${stderr}` });
    });
  });

/** Analizador con clang y el plugin del checker: una invocación por archivo, `paralelo` a la vez. */
export function analizadorClang(o: OpcionesClang): Analizador {
  return {
    async analizar(dir, archivos, politica): Promise<Analisis> {
      const avisos: Aviso[] = [];
      const noCompilados: string[] = [];
      let analizados = 0;
      const cola = [...archivos];
      const trabajador = async () => {
        for (let f = cola.shift(); f !== undefined; f = cola.shift()) {
          const r = await correr(o, dir, argumentos(o, dir, f, politica));
          if (r.codigo === 0) {
            analizados++;
            avisos.push(...leerSalida(r.salida));
          } else {
            noCompilados.push(f);
          }
        }
      };
      await Promise.all(Array.from({ length: Math.max(1, o.paralelo) }, trabajador));
      return { analizados, noCompilados: noCompilados.sort(), avisos };
    },
  };
}
