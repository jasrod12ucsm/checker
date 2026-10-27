// Integración con clang y el plugin reales: corre dentro de la imagen de Docker,
// donde CENTINELA_PLUGIN apunta a libContainerInvalidation.so. Fuera, se omite.
import { cpSync, existsSync, mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { describe, expect, it } from "vitest";
import { analizadorClang, argumentos, OPCIONES_CLANG } from "./clang";

const PLUGIN = process.env["CENTINELA_PLUGIN"] ?? "";
const EJEMPLO = new URL("../../../../../ejemplos/prueba.cpp", import.meta.url).pathname;

describe("argumentos de clang", () => {
  it("carga el plugin, fija la política, pide la ruta en texto y analiza con inlining all (D-22)", () => {
    const a = argumentos({ ...OPCIONES_CLANG, plugin: "/p.so" }, "/no-existe", "src/a.cpp", "Possibly");
    expect(a.join(" ")).toContain("-Xclang -load -Xclang /p.so");
    expect(a.join(" ")).toContain("-Xclang -analyzer-inlining-mode=all");
    expect(a.join(" ")).toContain("ucsm.ContainerInvalidation:PolicyMode=Possibly");
    expect(a.at(-1)).toBe("src/a.cpp");
  });
});

describe.skipIf(!existsSync(PLUGIN))("clang + checker de verdad", () => {
  const analizador = analizadorClang({ ...OPCIONES_CLANG, plugin: PLUGIN });
  it("en ejemplos/prueba.cpp da un confirmado en Silent y además un posible en Possibly", async () => {
    const dir = mkdtempSync(join(tmpdir(), "centinela-"));
    try {
      cpSync(EJEMPLO, join(dir, "prueba.cpp"));
      writeFileSync(join(dir, "roto.cpp"), "#include \"no-existe.h\"\nint main() {}\n");
      const silent = await analizador.analizar(dir, ["prueba.cpp", "roto.cpp"], "Silent");
      expect(silent.analizados).toBe(1);
      expect(silent.noCompilados).toEqual(["roto.cpp"]);
      expect(silent.avisos.map((a) => [a.linea, a.clase])).toEqual([[7, "Confirmado"]]);
      const possibly = await analizador.analizar(dir, ["prueba.cpp"], "Possibly");
      expect(possibly.avisos.map((a) => a.clase).sort()).toEqual(["Confirmado", "Posible"]);
      expect(possibly.avisos.find((a) => a.clase === "Posible")?.ruta.length).toBeGreaterThan(0);
    } finally {
      rmSync(dir, { recursive: true });
    }
  }, 60_000);
});
