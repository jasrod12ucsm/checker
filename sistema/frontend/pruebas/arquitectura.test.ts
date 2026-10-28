// @vitest-environment node
// Pruebas de aptitud del panel: la arquitectura se comprueba, no se promete (bodega-arquitectura, llevada al frontend).
import { readdirSync, readFileSync, statSync } from "node:fs";
import { join, relative } from "node:path";
import { describe, expect, it } from "vitest";

const SRC = new URL("../src/", import.meta.url).pathname;

function archivos(dir: string): string[] {
  return readdirSync(dir).flatMap((n) => {
    const p = join(dir, n);
    return statSync(p).isDirectory() ? archivos(p) : /\.tsx?$/.test(p) && !/\.test\.tsx?$/.test(p) ? [p] : [];
  });
}

const IMPORT = /(?:^|\n)\s*(?:import|export)\s[^;]*?from\s+["']([^"']+)["']|import\s+["']([^"']+)["']/g;
const importsDe = (codigo: string) => [...codigo.matchAll(IMPORT)].map((m) => (m[1] ?? m[2])!);
const carpeta = (f: string) => relative(SRC, f).split("/")[0]!;

/** Qué carpetas de `src/` y qué módulos externos puede importar cada capa. */
const CAPAS: Record<string, { internas: readonly string[]; externos: readonly string[] }> = {
  dominio: { internas: ["dominio"], externos: [] },
  api: { internas: ["dominio", "api"], externos: ["zod"] },
  estado: { internas: ["dominio", "api", "estado"], externos: ["react"] },
  componentes: { internas: ["dominio", "estado", "componentes"], externos: ["react", "react-router"] },
  pantallas: { internas: ["dominio", "estado", "componentes", "pantallas", "api"], externos: ["react", "react-router"] },
};

const fuentes = archivos(SRC).map((f) => ({ f, rel: relative(SRC, f), codigo: readFileSync(f, "utf8") }));

describe("fronteras del panel", () => {
  for (const [capa, permitido] of Object.entries(CAPAS)) {
    it(`${capa} solo importa lo permitido`, () => {
      const violaciones: string[] = [];
      for (const { f, rel, codigo } of fuentes.filter((x) => carpeta(x.f) === capa)) {
        for (const m of importsDe(codigo)) {
          if (m.startsWith(".")) {
            const destino = carpeta(join(f, "..", m));
            if (!permitido.internas.includes(destino)) violaciones.push(`${rel} importa ${m}`);
          } else if (!permitido.externos.includes(m)) violaciones.push(`${rel} importa ${m}`);
        }
      }
      expect(violaciones).toEqual([]);
    });
  }

  it("las pantallas solo conocen el puerto `Api`, nunca el adaptador HTTP", () => {
    const malas = fuentes.filter((x) => carpeta(x.f) === "pantallas" && importsDe(x.codigo).some((m) => m.includes("api/http")));
    expect(malas.map((x) => x.rel)).toEqual([]);
  });

  it("solo `api/http.ts` llama a fetch, y solo `main.tsx` elige el adaptador", () => {
    expect(fuentes.filter((x) => /\bfetch\(/.test(x.codigo)).map((x) => x.rel)).toEqual(["api/http.ts"]);
    expect(fuentes.filter((x) => importsDe(x.codigo).some((m) => m.endsWith("api/http"))).map((x) => x.rel)).toEqual(["main.tsx"]);
  });

  it("el dominio no lee el reloj ni el azar ni el navegador", () => {
    const malas = fuentes.filter((x) => carpeta(x.f) === "dominio" && /Date\.now\(|Math\.random\(|window\.|document\.|localStorage/.test(x.codigo));
    expect(malas.map((x) => x.rel)).toEqual([]);
  });

  it("las pantallas no leen el reloj directamente (lo reciben del contexto)", () => {
    expect(fuentes.filter((x) => carpeta(x.f) === "pantallas" && /Date\.now\(/.test(x.codigo)).map((x) => x.rel)).toEqual([]);
  });

  it("sin `any`, sin `@ts-ignore`, sin `dangerouslySetInnerHTML` y sin almacenar la sesión en el navegador", () => {
    const malas = fuentes.filter((x) => /:\s*any\b|as any\b|@ts-ignore|dangerouslySetInnerHTML|localStorage|sessionStorage/.test(x.codigo));
    expect(malas.map((x) => x.rel)).toEqual([]);
  });

  it("los switch del dominio son exhaustivos: terminan en `inalcanzable`, sin un default que trague casos", () => {
    const malas = fuentes.filter((x) => carpeta(x.f) === "dominio" && /default:(?!\s*return inalcanzable)/.test(x.codigo));
    expect(malas.map((x) => x.rel)).toEqual([]);
  });
});
