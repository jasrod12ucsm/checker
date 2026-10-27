import { describe, expect, it } from "vitest";
import { desenvolver, email, instante, texto, type UsuarioId } from "@centinela/kernel";
import {
  Autorizado,
  DURACION_SESION_MS,
  actualizarUsuario,
  claveNueva,
  crearUsuario,
  ingresar,
  registrar,
  validarSesion,
  type HashClave,
  type HashToken,
  type EstadoUsuario,
  type Usuario,
} from "./index";

const T0 = instante(1_000_000);
const usuario = (rol: Usuario["rol"], estado: EstadoUsuario = "Activo", id = "00000000-0000-4000-8000-000000000001"): Usuario => ({
  id: id as UsuarioId,
  email: desenvolver(email(`${rol}@ejemplo.com`)),
  nombre: desenvolver(texto("nombre", rol)),
  rol,
  hashClave: "h" as HashClave,
  estado,
  creadoEn: T0,
});
const datos = { id: "00000000-0000-4000-8000-000000000002" as UsuarioId, email: desenvolver(email("b@ejemplo.com")), nombre: desenvolver(texto("n", "B")), rol: "desarrollador" as const, hashClave: "h" as HashClave };

describe("autorización", () => {
  it("el administrador puede gestionar usuarios; el desarrollador no", () => {
    expect(Autorizado.para(usuario("administrador"), "gestionar-usuarios").ok).toBe(true);
    expect(Autorizado.para(usuario("desarrollador"), "gestionar-usuarios")).toEqual({ ok: false, error: { tipo: "SinPermiso", permiso: "gestionar-usuarios" } });
  });
  it("el desarrollador puede clasificar hallazgos y pedir revisiones", () => {
    expect(Autorizado.para(usuario("desarrollador"), "clasificar-hallazgos").ok).toBe(true);
    expect(Autorizado.para(usuario("desarrollador"), "solicitar-revision").ok).toBe(true);
  });
  it("una cuenta pendiente o desactivada no puede nada, y el error dice cuál de las dos es", () => {
    expect(Autorizado.para(usuario("administrador", "Pendiente"), "consultar-revisiones")).toEqual({ ok: false, error: { tipo: "UsuarioPendiente" } });
    expect(Autorizado.para(usuario("administrador", "Desactivado"), "consultar-revisiones")).toEqual({ ok: false, error: { tipo: "UsuarioDesactivado" } });
  });
});

describe("sesiones", () => {
  const h = "t" as HashToken;
  it("credenciales inválidas no distinguen usuario inexistente de clave mala", () => {
    expect(ingresar(undefined, true, h, T0)).toEqual(ingresar(usuario("desarrollador"), false, h, T0));
  });
  it("la sesión expira a las 8 horas", () => {
    const s = desenvolver(ingresar(usuario("desarrollador"), true, h, T0));
    const u = usuario("desarrollador");
    expect(validarSesion(s, u, instante(T0 + DURACION_SESION_MS - 1)).ok).toBe(true);
    expect(validarSesion(s, u, instante(T0 + DURACION_SESION_MS))).toEqual({ ok: false, error: { tipo: "SesionInvalida" } });
  });
  it("si el usuario se desactiva, su sesión deja de valer", () => {
    const s = desenvolver(ingresar(usuario("desarrollador"), true, h, T0));
    expect(validarSesion(s, usuario("desarrollador", "Desactivado"), T0)).toEqual({ ok: false, error: { tipo: "UsuarioDesactivado" } });
  });
  it("una cuenta pendiente no ingresa aunque la clave sea correcta", () => {
    expect(ingresar(usuario("desarrollador", "Pendiente"), true, h, T0)).toEqual({ ok: false, error: { tipo: "UsuarioPendiente" } });
  });
});

describe("usuarios", () => {
  const admin = usuario("administrador");
  const por = desenvolver(Autorizado.para(admin, "gestionar-usuarios"));
  it("la clave sigue la política", () => {
    expect(claveNueva("corta1").ok).toBe(false);
    expect(claveNueva("sololetrasaqui").ok).toBe(false);
    expect(claveNueva("letras12345").ok).toBe(true);
  });
  it("quien se registra primero queda como administrador activo", () => {
    expect(registrar(0, false, datos, T0)).toMatchObject({ ok: true, valor: { rol: "administrador", estado: "Activo" } });
  });
  it("los siguientes quedan como desarrolladores pendientes de aprobación", () => {
    expect(registrar(1, false, datos, T0)).toMatchObject({ ok: true, valor: { rol: "desarrollador", estado: "Pendiente" } });
  });
  it("no se registra un correo en uso", () => {
    expect(registrar(1, true, datos, T0)).toEqual({ ok: false, error: { tipo: "EmailEnUso" } });
  });
  it("no se crea un usuario con un correo en uso", () => {
    expect(crearUsuario(por, true, datos, T0)).toEqual({ ok: false, error: { tipo: "EmailEnUso" } });
    expect(crearUsuario(por, false, datos, T0)).toMatchObject({ ok: true, valor: { estado: "Activo", rol: "desarrollador" } });
  });
  it("nadie se desactiva ni se cambia el rol a sí mismo", () => {
    expect(actualizarUsuario(por, admin, { estado: "Desactivado" })).toEqual({ ok: false, error: { tipo: "NoPuedeModificarseASiMismo" } });
    expect(actualizarUsuario(por, admin, { rol: "desarrollador" })).toEqual({ ok: false, error: { tipo: "NoPuedeModificarseASiMismo" } });
  });
  it("el administrador aprueba a un pendiente y le da un rol", () => {
    const pendiente = usuario("desarrollador", "Pendiente", datos.id);
    expect(actualizarUsuario(por, pendiente, { estado: "Activo", rol: "administrador" })).toMatchObject({ ok: true, valor: { estado: "Activo", rol: "administrador" } });
  });
  it("rechazar deja la cuenta desactivada, y se puede reactivar después", () => {
    const rechazada = desenvolver(actualizarUsuario(por, usuario("desarrollador", "Pendiente", datos.id), { estado: "Desactivado" }));
    expect(rechazada.estado).toBe("Desactivado");
    expect(actualizarUsuario(por, rechazada, { estado: "Activo" })).toMatchObject({ ok: true, valor: { estado: "Activo" } });
  });
});
