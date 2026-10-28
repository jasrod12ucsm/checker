// @vitest-environment node
// Contraste WCAG 2.1 AA de los tokens de color, en el tema claro y en el oscuro. La auditoría con axe
// (capítulo 8) encontró el botón primario del tema oscuro en 3,56:1; esta prueba impide que vuelva.
import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";

const CSS = readFileSync(new URL("../src/estilos.css", import.meta.url), "utf8");

function tokens(bloque: string): Record<string, string> {
  return Object.fromEntries([...bloque.matchAll(/--([a-z0-9-]+):\s*(#[0-9a-f]{6})/gi)].map((m) => [m[1]!, m[2]!.toLowerCase()]));
}
const claro = tokens(CSS.slice(0, CSS.indexOf("@media (prefers-color-scheme: dark)")));
const oscuro = { ...claro, ...tokens(CSS.slice(CSS.indexOf("@media (prefers-color-scheme: dark)"), CSS.indexOf("}", CSS.indexOf("@media (prefers-color-scheme: dark)") + 40))) };

const luminancia = (hex: string) => {
  const [r, g, b] = [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16) / 255).map((c) => (c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4));
  return 0.2126 * r! + 0.7152 * g! + 0.0722 * b!;
};
const contraste = (a: string, b: string) => {
  const [x, y] = [luminancia(a), luminancia(b)].sort((m, n) => n - m);
  return (x! + 0.05) / (y! + 0.05);
};

/** Texto sobre fondo que el panel usa de verdad; 4,5:1 es el mínimo AA para texto normal. */
const PARES: [string, string][] = [
  ["texto", "fondo"], ["texto", "superficie"], ["tenue", "superficie"], ["tenue", "fondo"],
  ["primario-texto", "primario"], ["primario", "superficie"], ["primario", "superficie-2"], ["peligro", "superficie"],
  ["exito", "exito-fondo"], ["aviso", "aviso-fondo"], ["peligro", "peligro-fondo"], ["info", "info-fondo"], ["neutro", "neutro-fondo"],
];

describe("contraste de los tokens (WCAG 2.1 AA, 4,5:1)", () => {
  for (const [tema, t] of [["claro", claro], ["oscuro", oscuro]] as const) {
    for (const [texto, fondo] of PARES) {
      it(`${tema}: --${texto} sobre --${fondo}`, () => {
        expect(t[texto], texto).toBeDefined();
        expect(t[fondo], fondo).toBeDefined();
        expect(contraste(t[texto]!, t[fondo]!)).toBeGreaterThanOrEqual(4.5);
      });
    }
  }

  it("la fórmula da los valores conocidos: negro sobre blanco 21:1, el botón oscuro anterior (blanco sobre #5b82f0) 3,56:1", () => {
    expect(contraste("#000000", "#ffffff")).toBeCloseTo(21, 1);
    expect(contraste("#ffffff", "#5b82f0")).toBeCloseTo(3.56, 1);
  });
});
