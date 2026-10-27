// Pruebas de aptitud: la arquitectura se comprueba, no se promete.
// Cada paquete solo importa lo que su capa permite (bodega-arquitectura, adaptado a TypeScript).
import { readdirSync, readFileSync, statSync } from "node:fs";
import { join, relative } from "node:path";
import { describe, expect, it } from "vitest";

const RAIZ = new URL("../paquetes/", import.meta.url).pathname;

interface Capa {
  readonly paquetes: readonly string[];
  /** Paquetes @centinela/* que puede importar. */
  readonly internos: readonly string[];
  /** Módulos externos permitidos (node:* incluido). */
  readonly externos: readonly string[];
}

const DOMINIO = ["kernel", "identidad", "repositorios", "revisiones"];
const CAPAS: Record<string, Capa> = {
  kernel: { paquetes: ["kernel"], internos: [], externos: [] },
  identidad: { paquetes: ["contextos/identidad"], internos: ["kernel"], externos: [] },
  repositorios: { paquetes: ["contextos/repositorios"], internos: ["kernel", "identidad"], externos: [] },
  revisiones: { paquetes: ["contextos/revisiones"], internos: ["kernel", "identidad", "repositorios"], externos: [] },
  producto: { paquetes: ["producto"], internos: DOMINIO, externos: [] },
  sqlite: { paquetes: ["adaptadores/sqlite"], internos: [...DOMINIO, "producto"], externos: ["better-sqlite3", "zod", "node:fs"] },
  cripto: { paquetes: ["adaptadores/cripto"], internos: [...DOMINIO, "producto"], externos: ["node:crypto"] },
  github: {
    paquetes: ["adaptadores/github"],
    internos: [...DOMINIO, "producto"],
    externos: ["zod", "node:child_process", "node:fs/promises", "node:os", "node:path", "node:stream", "node:stream/promises", "node:stream/web"],
  },
  analizador: { paquetes: ["adaptadores/analizador"], internos: [...DOMINIO, "producto"], externos: ["node:child_process", "node:fs", "node:path"] },
  http: { paquetes: ["adaptadores/http"], internos: [...DOMINIO, "producto"], externos: ["fastify", "@fastify/cookie", "@fastify/static", "zod"] },
  app: { paquetes: ["app"], internos: [...DOMINIO, "producto", "sqlite", "cripto", "github", "analizador", "http"], externos: ["zod", "node:fs", "node:path", "node:crypto"] },
};

function archivos(dir: string): string[] {
  return readdirSync(dir).flatMap((n) => {
    const p = join(dir, n);
    return statSync(p).isDirectory() ? archivos(p) : p.endsWith(".ts") && !p.endsWith(".test.ts") ? [p] : [];
  });
}

const IMPORT = /(?:^|\n)\s*(?:import|export)\s[^;]*?from\s+["']([^"']+)["']|import\(\s*["']([^"']+)["']\s*\)/g;
const importsDe = (codigo: string) => [...codigo.matchAll(IMPORT)].map((m) => (m[1] ?? m[2])!);

describe("fronteras entre paquetes", () => {
  for (const [nombre, capa] of Object.entries(CAPAS)) {
    for (const paquete of capa.paquetes) {
      it(`${paquete} solo importa lo permitido`, () => {
        const violaciones: string[] = [];
        for (const f of archivos(join(RAIZ, paquete, "src"))) {
          for (const m of importsDe(readFileSync(f, "utf8"))) {
            if (m.startsWith(".")) continue;
            const interno = m.startsWith("@centinela/") ? m.slice("@centinela/".length) : undefined;
            const ok = interno !== undefined ? capa.internos.includes(interno) : capa.externos.includes(m);
            if (!ok) violaciones.push(`${relative(RAIZ, f)} importa ${m}`);
          }
        }
        expect(violaciones, `capa ${nombre}`).toEqual([]);
      });
    }
  }

  it("todos los paquetes están cubiertos por una capa", () => {
    const declarados = Object.values(CAPAS).flatMap((c) => c.paquetes).sort();
    const reales = ["kernel", "producto", "app", ...["contextos", "adaptadores"].flatMap((g) => readdirSync(join(RAIZ, g)).map((n) => `${g}/${n}`))].sort();
    expect(declarados).toEqual(reales);
  });
});

describe("reglas de código", () => {
  const todos = Object.values(CAPAS).flatMap((c) => c.paquetes.flatMap((p) => archivos(join(RAIZ, p, "src"))));
  const dominio = todos.filter((f) => /\/(kernel|contextos|producto)\//.test(f));

  it("los códigos HTTP solo aparecen en adaptadores/http/src/errores.ts (y las respuestas propias del servidor)", () => {
    const fuera = todos.filter((f) => !f.includes("adaptadores/http/")).filter((f) => /\b(statusCode|\.code\(\d)/.test(readFileSync(f, "utf8")));
    expect(fuera.map((f) => relative(RAIZ, f))).toEqual([]);
  });

  it("el dominio y el producto no leen el reloj ni generan azar por su cuenta", () => {
    const malos = dominio.filter((f) => /Date\.now\(|new Date\(|Math\.random\(|crypto\./.test(readFileSync(f, "utf8")));
    expect(malos.map((f) => relative(RAIZ, f))).toEqual([]);
  });

  it("el dominio no lanza excepciones para errores de negocio (usa Resultado)", () => {
    // Las únicas excepciones permitidas son las de invariantes rotas: inalcanzable, desenvolver y el generador de ids.
    const permitidas = ["kernel/src/resultado.ts", "producto/src/casos-revisiones.ts"];
    const malos = dominio.filter((f) => !permitidas.some((p) => f.endsWith(p))).filter((f) => /\bthrow\b/.test(readFileSync(f, "utf8")));
    expect(malos.map((f) => relative(RAIZ, f))).toEqual([]);
  });

  it("no hay `any` explícito en el código de producción", () => {
    const malos = todos.filter((f) => /:\s*any\b|as any\b|<any>/.test(readFileSync(f, "utf8")));
    expect(malos.map((f) => relative(RAIZ, f))).toEqual([]);
  });
});
