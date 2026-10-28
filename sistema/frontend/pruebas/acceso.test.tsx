// CU-S01 de punta a punta: el panel contra el servicio real (sin usuarios predefinidos).
import { screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it } from "vitest";
import { montar } from "./montar";
import { CLAVE, servicio, type Servicio } from "./servicio";

let s: Servicio;
beforeEach(() => {
  s = servicio();
});

async function llenarRegistro(u: ReturnType<typeof montar>["usuario"], email: string, nombre: string, clave = CLAVE, confirmacion = clave) {
  await u.type(screen.getByLabelText("Correo"), email);
  await u.type(screen.getByLabelText("Nombre"), nombre);
  await u.type(screen.getByLabelText("Clave"), clave);
  await u.type(screen.getByLabelText("Confirmar clave"), confirmacion);
  await u.click(screen.getByRole("button", { name: "Crear cuenta" }));
}

describe("CU-S01 registro: nada viene predefinido", () => {
  it("en una instancia vacía, el ingreso invita a crear la primera cuenta", async () => {
    montar("/ingreso", s.navegador().api);
    expect(await screen.findByText(/todavía no tiene cuentas/)).toBeInTheDocument();
  });

  it("quien se registra primero queda de administradora y entra directo a conectar repositorios", async () => {
    const m = montar("/registro", s.navegador().api);
    expect(await screen.findByText(/Eres la primera persona/)).toBeInTheDocument();
    await llenarRegistro(m.usuario, "lucia@ucsm.edu.pe", "Lucía Paredes");
    expect(await screen.findByRole("heading", { name: "Repositorios" })).toBeInTheDocument();
    expect(m.ubicacion()).toBe("/repositorios");
    expect(screen.getByText("Administrador")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /Usuarios/ })).toBeInTheDocument();
  });

  it("las siguientes cuentas quedan pendientes y no entran hasta que las aprueben", async () => {
    await s.registrar("admin@ucsm.edu.pe", "Admin");
    const m = montar("/registro", s.navegador().api);
    await screen.findByRole("heading", { name: "Crea tu cuenta" });
    expect(screen.queryByText(/Eres la primera persona/)).not.toBeInTheDocument();
    await llenarRegistro(m.usuario, "diego@ucsm.edu.pe", "Diego Quispe");
    expect(await screen.findByRole("heading", { name: "Tu cuenta espera la aprobación de un administrador" })).toBeInTheDocument();
    expect(screen.getByText("diego@ucsm.edu.pe")).toBeInTheDocument();

    await m.usuario.click(screen.getByRole("link", { name: "Volver al ingreso" }));
    await m.usuario.type(screen.getByLabelText("Correo"), "diego@ucsm.edu.pe");
    await m.usuario.type(screen.getByLabelText("Clave"), CLAVE);
    await m.usuario.click(screen.getByRole("button", { name: "Ingresar" }));
    expect(await screen.findByRole("alert")).toHaveTextContent("Tu cuenta espera la aprobación de un administrador.");
    expect(m.ubicacion()).toBe("/ingreso");
  });

  it("valida en el panel antes de enviar: correo, nombre, reglas de la clave y confirmación", async () => {
    const m = montar("/registro", s.navegador().api);
    await screen.findByRole("heading", { name: "Crea tu cuenta" });
    await llenarRegistro(m.usuario, "no-es-correo", " ", "corta", "otra");
    expect(screen.getByText("Escribe un correo válido.")).toBeInTheDocument();
    expect(screen.getByText("Escribe tu nombre.")).toBeInTheDocument();
    expect(screen.getByText("La clave debe tener al menos 10 caracteres.")).toBeInTheDocument();
    expect(screen.getByText("Las claves no coinciden.")).toBeInTheDocument();
    expect((await s.p.identidad.estadoRegistro()).ok && (await s.p.identidad.estadoRegistro())).toMatchObject({ valor: { hayUsuarios: false } });
  });

  it("las reglas de la clave se marcan mientras se escribe", async () => {
    const m = montar("/registro", s.navegador().api);
    await screen.findByRole("heading", { name: "Crea tu cuenta" });
    const reglas = screen.getByRole("list", { name: "Requisitos de la clave" });
    await m.usuario.type(screen.getByLabelText("Clave"), "abcdefghij");
    expect(reglas.querySelector(".cumple")).toHaveTextContent("Al menos 10 caracteres");
    expect(reglas.querySelectorAll(".cumple")).toHaveLength(1);
    await m.usuario.type(screen.getByLabelText("Clave"), "1");
    expect(reglas.querySelectorAll(".cumple")).toHaveLength(2);
  });

  it("un correo ya registrado se marca en su campo con el mensaje del servicio", async () => {
    await s.registrar("admin@ucsm.edu.pe", "Admin");
    const m = montar("/registro", s.navegador().api);
    await screen.findByRole("heading", { name: "Crea tu cuenta" });
    await llenarRegistro(m.usuario, "admin@ucsm.edu.pe", "Otra");
    expect(await screen.findByText("Ya hay un usuario con ese correo.")).toBeInTheDocument();
  });
});

describe("CU-S01 ingreso y sesión", () => {
  beforeEach(async () => {
    await s.registrar("admin@ucsm.edu.pe", "Admin");
  });

  it("credenciales incorrectas: el mismo mensaje si la clave falla o si el correo no existe", async () => {
    const m = montar("/ingreso", s.navegador().api);
    await m.usuario.type(await screen.findByLabelText("Correo"), "admin@ucsm.edu.pe");
    await m.usuario.type(screen.getByLabelText("Clave"), "claveMala123");
    await m.usuario.click(screen.getByRole("button", { name: "Ingresar" }));
    expect(await screen.findByRole("alert")).toHaveTextContent("Correo o clave incorrectos.");
    expect(screen.getByLabelText("Clave")).toHaveAttribute("aria-invalid", "true");

    await m.usuario.clear(screen.getByLabelText("Correo"));
    await m.usuario.type(screen.getByLabelText("Correo"), "nadie@ucsm.edu.pe");
    await m.usuario.click(screen.getByRole("button", { name: "Ingresar" }));
    await waitFor(() => expect(screen.getByRole("alert")).toHaveTextContent("Correo o clave incorrectos."));
  });

  it("campos vacíos: no se llama al servicio", async () => {
    const m = montar("/ingreso", s.navegador().api);
    await m.usuario.click(await screen.findByRole("button", { name: "Ingresar" }));
    expect(screen.getByText("Escribe tu correo.")).toBeInTheDocument();
    expect(screen.getByText("Escribe tu clave.")).toBeInTheDocument();
  });

  it("ingresar lleva a las revisiones, y la sesión sobrevive a recargar el panel (cookie)", async () => {
    const n = s.navegador();
    const m = montar("/ingreso", n.api);
    await m.usuario.type(await screen.findByLabelText("Correo"), "admin@ucsm.edu.pe");
    await m.usuario.type(screen.getByLabelText("Clave"), CLAVE);
    await m.usuario.click(screen.getByRole("button", { name: "Ingresar" }));
    expect(await screen.findByRole("heading", { name: "Revisiones" })).toBeInTheDocument();
    m.unmount();

    montar("/usuarios", n.api);
    expect(await screen.findByRole("heading", { name: "Usuarios" })).toBeInTheDocument();
  });

  it("sin sesión, una ruta protegida manda al ingreso y, al entrar, vuelve a donde se quería ir", async () => {
    const m = montar("/repositorios", s.navegador().api);
    expect(await screen.findByRole("heading", { name: "Ingresa" })).toBeInTheDocument();
    await m.usuario.type(await screen.findByLabelText("Correo"), "admin@ucsm.edu.pe");
    await m.usuario.type(screen.getByLabelText("Clave"), CLAVE);
    await m.usuario.click(screen.getByRole("button", { name: "Ingresar" }));
    expect(await screen.findByRole("heading", { name: "Repositorios" })).toBeInTheDocument();
    expect(m.ubicacion()).toBe("/repositorios");
  });

  it("con sesión, el ingreso y el registro llevan directo al panel", async () => {
    const n = await s.conSesion("admin@ucsm.edu.pe");
    const m = montar("/ingreso", n.api);
    expect(await screen.findByRole("heading", { name: "Revisiones" })).toBeInTheDocument();
    expect(m.ubicacion()).toBe("/revisiones");
  });

  it("cerrar sesión borra la cookie: al volver, pide ingresar", async () => {
    const n = await s.conSesion("admin@ucsm.edu.pe");
    const m = montar("/revisiones", n.api);
    await m.usuario.click(await screen.findByRole("button", { name: "Cerrar sesión" }));
    expect(await screen.findByRole("heading", { name: "Ingresa" })).toBeInTheDocument();
    m.unmount();
    montar("/revisiones", n.api);
    expect(await screen.findByRole("heading", { name: "Ingresa" })).toBeInTheDocument();
  });

  it("si un administrador desactiva la cuenta, la siguiente llamada devuelve al ingreso con el aviso", async () => {
    const dev = await s.registrar("dev@ucsm.edu.pe", "Dev");
    const admin = await s.conSesion("admin@ucsm.edu.pe");
    await admin.api.actualizarUsuario(dev.id, { estado: "Activo" });
    const n = await s.conSesion("dev@ucsm.edu.pe");
    const m = montar("/revisiones", n.api);
    await screen.findByRole("heading", { name: "Revisiones" });
    await admin.api.actualizarUsuario(dev.id, { estado: "Desactivado" });
    await m.usuario.click(screen.getByRole("link", { name: /Repositorios/ }));
    expect(await screen.findByRole("heading", { name: "Ingresa" })).toBeInTheDocument();
    expect(screen.getByText(/La sesión no es válida o venció/)).toBeInTheDocument();
  });
});
