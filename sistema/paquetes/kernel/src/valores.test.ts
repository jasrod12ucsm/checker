import { describe, expect, it } from "vitest";
import { email, positivo, texto, usuarioId } from "./index";

describe("valores del kernel", () => {
  it("normaliza el correo y rechaza lo que no es correo", () => {
    expect(email("  Ana@Ejemplo.COM ")).toEqual({ ok: true, valor: "ana@ejemplo.com" });
    expect(email("ana@")).toMatchObject({ ok: false, error: { campo: "email" } });
  });
  it("el texto no puede estar vacío ni pasar del máximo", () => {
    expect(texto("nombre", "   ").ok).toBe(false);
    expect(texto("nombre", "x".repeat(11), 10).ok).toBe(false);
    expect(texto("nombre", " Ana ")).toEqual({ ok: true, valor: "Ana" });
  });
  it("los identificadores son UUID", () => {
    expect(usuarioId("123").ok).toBe(false);
    expect(usuarioId("8f14e45f-ceea-4e7a-9b1d-3c1c2b9a0d11").ok).toBe(true);
  });
  it("positivo solo acepta enteros mayores que cero", () => {
    expect(positivo("pr", 0).ok).toBe(false);
    expect(positivo("pr", 1.5).ok).toBe(false);
    expect(positivo("pr", 7).ok).toBe(true);
  });
});
