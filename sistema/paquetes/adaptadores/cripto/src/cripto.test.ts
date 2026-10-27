import { describe, expect, it } from "vitest";
import type { SecretoWebhook } from "@centinela/repositorios";
import { claves, firmar, secretos } from "./index";

describe("claves (scrypt)", () => {
  it("verifica la clave correcta y rechaza otra", async () => {
    const h = await claves.hashear("clave12345678");
    expect(h).toMatch(/^scrypt\$/);
    expect(await claves.verificar("clave12345678", h)).toBe(true);
    expect(await claves.verificar("clave12345679", h)).toBe(false);
  });
  it("dos hashes de la misma clave son distintos (sal aleatoria)", async () => {
    expect(await claves.hashear("clave12345678")).not.toBe(await claves.hashear("clave12345678"));
  });
  it("un hash con otro formato no se acepta y no lanza", async () => {
    expect(await claves.verificar("x", "md5$abc" as never)).toBe(false);
  });
});

describe("secretos", () => {
  it("el token no se guarda: se guarda su hash", () => {
    const t = secretos.token();
    expect(t.hash).not.toBe(t.token);
    expect(secretos.hashDeToken(t.token)).toBe(t.hash);
  });
  it("valida la firma X-Hub-Signature-256 de GitHub", () => {
    const s = "s3creto" as SecretoWebhook;
    const cuerpo = '{"action":"opened"}';
    expect(secretos.firmaValida(s, cuerpo, firmar(s, cuerpo))).toBe(true);
    expect(secretos.firmaValida(s, cuerpo + " ", firmar(s, cuerpo))).toBe(false);
    expect(secretos.firmaValida(s, cuerpo, undefined)).toBe(false);
    expect(secretos.firmaValida(s, cuerpo, "sha1=abc")).toBe(false);
  });
});
