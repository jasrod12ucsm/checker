import { describe, expect, it } from "vitest";
import { desenvolver, instante, type RepositorioId, type Email, type Texto, type UsuarioId } from "@centinela/kernel";
import { Autorizado, type HashClave } from "@centinela/identidad";
import { conectar, configurar, desconectar, nombreRepo, type DatosConexion, type SecretoWebhook } from "./index";

const admin = { id: "00000000-0000-4000-8000-000000000001" as UsuarioId, email: "a@b.co" as Email, nombre: "A" as Texto, rol: "administrador" as const, hashClave: "h" as HashClave, estado: "Activo" as const, creadoEn: instante(0) };
const por = desenvolver(Autorizado.para(admin, "gestionar-repositorios"));
const datos = (id = "00000000-0000-4000-8000-0000000000a1"): DatosConexion => ({
  id: id as RepositorioId,
  nombre: desenvolver(nombreRepo("ucsm/demo")),
  politica: "Possibly",
  bloquearMerge: true,
  secretoWebhook: "s1" as SecretoWebhook,
});

describe("repositorios", () => {
  it("el nombre es propietario/nombre", () => {
    expect(nombreRepo("ucsm/demo.cpp").ok).toBe(true);
    expect(nombreRepo("demo").ok).toBe(false);
    expect(nombreRepo("a/b/c").ok).toBe(false);
  });
  it("conectar guarda quién y cuándo", () => {
    expect(conectar(por, undefined, datos(), instante(5))).toMatchObject({ ok: true, valor: { activo: true, conectadoPor: admin.id, conectadoEn: 5 } });
  });
  it("un repositorio activo no se conecta dos veces", () => {
    const r = desenvolver(conectar(por, undefined, datos(), instante(5)));
    expect(conectar(por, r, datos(), instante(6))).toEqual({ ok: false, error: { tipo: "RepositorioYaConectado" } });
  });
  it("reconectar uno desconectado conserva su id (y sus revisiones)", () => {
    const r = desconectar(por, desenvolver(conectar(por, undefined, datos(), instante(5))));
    const otra = desenvolver(conectar(por, r, { ...datos("00000000-0000-4000-8000-0000000000b2"), secretoWebhook: "s2" as SecretoWebhook }, instante(9)));
    expect(otra).toMatchObject({ id: r.id, activo: true, secretoWebhook: "s2" });
  });
  it("no se configura un repositorio desconectado", () => {
    const r = desconectar(por, desenvolver(conectar(por, undefined, datos(), instante(5))));
    expect(configurar(por, r, { politica: "Silent" })).toEqual({ ok: false, error: { tipo: "RepositorioDesconectado" } });
  });
});
