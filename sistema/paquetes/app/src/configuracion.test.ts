import { describe, expect, it } from "vitest";
import { leerConfiguracion } from "./configuracion";

describe("configuración", () => {
  it("toma valores por omisión razonables y exige el token de GitHub", () => {
    expect(() => leerConfiguracion({})).toThrow(/CENTINELA_GITHUB_TOKEN/);
    const c = leerConfiguracion({ CENTINELA_GITHUB_TOKEN: "t" });
    expect(c).toMatchObject({ CENTINELA_PUERTO: 8080, CENTINELA_COOKIE_SEGURA: false, CENTINELA_GITHUB_API: "https://api.github.com" });
  });
  it("valida los tipos", () => {
    expect(() => leerConfiguracion({ CENTINELA_GITHUB_TOKEN: "t", CENTINELA_PUERTO: "abc" })).toThrow(/CENTINELA_PUERTO/);
    expect(leerConfiguracion({ CENTINELA_GITHUB_TOKEN: "t", CENTINELA_COOKIE_SEGURA: "true" }).CENTINELA_COOKIE_SEGURA).toBe(true);
  });
});
