// CU-S02 de punta a punta: aprobar, rechazar, roles, desactivar, crear; y lo que el desarrollador no ve.
import { screen, waitFor, within } from "@testing-library/react";
import { beforeEach, describe, expect, it } from "vitest";
import { montar } from "./montar";
import { CLAVE, servicio, type Servicio } from "./servicio";

let s: Servicio;
let admin: Awaited<ReturnType<Servicio["conSesion"]>>;

beforeEach(async () => {
  s = servicio();
  await s.registrar("lucia@ucsm.edu.pe", "Lucía Paredes");
  admin = await s.conSesion("lucia@ucsm.edu.pe");
});

const fila = (nombre: RegExp | string) => screen.getAllByRole("row").filter((r) => within(r).queryByText(nombre) !== null);

describe("CU-S02 usuarios", () => {
  it("el menú muestra cuántos registros esperan aprobación", async () => {
    await s.registrar("ana@ucsm.edu.pe", "Ana Huamán");
    await s.registrar("rodrigo@ucsm.edu.pe", "Rodrigo Mamani");
    montar("/revisiones", admin.api);
    expect(await screen.findByLabelText("2 por aprobar")).toHaveTextContent("2");
  });

  it("aprobar con el rol elegido: la persona ya puede ingresar con ese rol", async () => {
    await s.registrar("ana@ucsm.edu.pe", "Ana Huamán");
    const m = montar("/usuarios", admin.api);
    await screen.findByRole("heading", { name: /Pendientes de aprobación/ });
    await m.usuario.selectOptions(screen.getByLabelText("Rol al aprobar a Ana Huamán"), "administrador");
    await m.usuario.click(screen.getByRole("button", { name: "Aprobar a Ana Huamán" }));
    expect(await screen.findByText("Se aprobó a Ana Huamán como Administrador.")).toBeInTheDocument();
    expect(screen.getByText("No hay registros por aprobar.")).toBeInTheDocument();
    const ana = await s.conSesion("ana@ucsm.edu.pe");
    expect(ana.usuario).toMatchObject({ rol: "administrador", estado: "Activo" });
    await waitFor(() => expect(screen.queryByLabelText(/por aprobar/)).not.toBeInTheDocument());
  });

  it("rechazar deja la cuenta desactivada y se puede activar después", async () => {
    await s.registrar("ana@ucsm.edu.pe", "Ana Huamán");
    const m = montar("/usuarios", admin.api);
    await m.usuario.click(await screen.findByRole("button", { name: "Rechazar a Ana Huamán" }));
    expect(await screen.findByText("Se rechazó el registro de Ana Huamán.")).toBeInTheDocument();
    expect(within(fila("Ana Huamán")[0]!).getByText("Desactivado")).toBeInTheDocument();
    expect((await s.navegador().api.ingresar({ email: "ana@ucsm.edu.pe", clave: CLAVE })).ok).toBe(false);

    await m.usuario.click(screen.getByRole("button", { name: "Activar a Ana Huamán" }));
    expect(await screen.findByText("Se activó a Ana Huamán.")).toBeInTheDocument();
    expect((await s.navegador().api.ingresar({ email: "ana@ucsm.edu.pe", clave: CLAVE })).ok).toBe(true);
  });

  it("desactivar cierra las sesiones de la persona", async () => {
    await s.registrar("dev@ucsm.edu.pe", "Diego Quispe");
    const yo = await admin.api.usuarios();
    const dev = yo.ok ? yo.valor.find((u) => u.email === "dev@ucsm.edu.pe")! : undefined;
    await admin.api.actualizarUsuario(dev!.id, { estado: "Activo" });
    const sesionDev = await s.conSesion("dev@ucsm.edu.pe");
    const m = montar("/usuarios", admin.api);
    await m.usuario.click(await screen.findByRole("button", { name: "Desactivar a Diego Quispe" }));
    expect(await screen.findByText("Se desactivó a Diego Quispe; sus sesiones se cerraron.")).toBeInTheDocument();
    expect(await sesionDev.api.sesion()).toMatchObject({ ok: false, error: { tipo: "SinSesion" } });
  });

  it("cambiar el rol desde la tabla", async () => {
    await s.registrar("dev@ucsm.edu.pe", "Diego Quispe");
    const lista = await admin.api.usuarios();
    await admin.api.actualizarUsuario(lista.ok ? lista.valor.find((u) => u.nombre === "Diego Quispe")!.id : "", { estado: "Activo" });
    const m = montar("/usuarios", admin.api);
    await m.usuario.selectOptions(await screen.findByLabelText("Rol de Diego Quispe"), "administrador");
    expect(await screen.findByText("Diego Quispe ahora es Administrador.")).toBeInTheDocument();
  });

  it("no puedo desactivarme ni cambiarme el rol: el panel lo dice y no lo ofrece", async () => {
    montar("/usuarios", admin.api);
    await screen.findByRole("heading", { name: /Todos los usuarios/ });
    const mia = fila("Lucía Paredes")[0]!;
    expect(within(mia).getByText("tú")).toBeInTheDocument();
    expect(within(mia).getByText("No puedes desactivar ni cambiar el rol de tu propio usuario.")).toBeInTheDocument();
    expect(within(mia).getByLabelText("Rol de Lucía Paredes")).toBeDisabled();
    expect(within(mia).queryByRole("button", { name: /Desactivar/ })).not.toBeInTheDocument();
  });

  it("crear un usuario: queda activo; un correo en uso se marca en su campo", async () => {
    const m = montar("/usuarios", admin.api);
    await m.usuario.click(await screen.findByRole("button", { name: "Crear usuario" }));
    const dialogo = screen.getByRole("dialog", { name: "Crear usuario" });
    await m.usuario.type(within(dialogo).getByLabelText("Correo"), "lucia@ucsm.edu.pe");
    await m.usuario.type(within(dialogo).getByLabelText("Nombre"), "Valeria Ccama");
    await m.usuario.type(within(dialogo).getByLabelText("Clave inicial"), CLAVE);
    await m.usuario.click(within(dialogo).getByRole("button", { name: "Crear" }));
    expect(await within(dialogo).findByText("Ya hay un usuario con ese correo.")).toBeInTheDocument();

    await m.usuario.clear(within(dialogo).getByLabelText("Correo"));
    await m.usuario.type(within(dialogo).getByLabelText("Correo"), "valeria@ucsm.edu.pe");
    await m.usuario.click(within(dialogo).getByRole("button", { name: "Crear" }));
    expect(await screen.findByText("Se creó la cuenta de Valeria Ccama como Desarrollador.")).toBeInTheDocument();
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
    expect(within(fila("Valeria Ccama")[0]!).getByText("Activo")).toBeInTheDocument();
    expect((await s.navegador().api.ingresar({ email: "valeria@ucsm.edu.pe", clave: CLAVE })).ok).toBe(true);
  });

  it("crear un usuario valida antes de enviar y Escape cierra la ventana", async () => {
    const m = montar("/usuarios", admin.api);
    await m.usuario.click(await screen.findByRole("button", { name: "Crear usuario" }));
    const dialogo = screen.getByRole("dialog", { name: "Crear usuario" });
    await m.usuario.click(within(dialogo).getByRole("button", { name: "Crear" }));
    expect(within(dialogo).getByText("Escribe un correo válido.")).toBeInTheDocument();
    expect(within(dialogo).getByText("La clave debe tener al menos 10 caracteres.")).toBeInTheDocument();
    await m.usuario.keyboard("{Escape}");
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  });
});

describe("CU-S02 lo que el desarrollador no ve", () => {
  beforeEach(async () => {
    await s.registrar("dev@ucsm.edu.pe", "Diego Quispe");
    const lista = await admin.api.usuarios();
    await admin.api.actualizarUsuario(lista.ok ? lista.valor.find((u) => u.nombre === "Diego Quispe")!.id : "", { estado: "Activo" });
  });

  it("el menú no tiene «Usuarios» y la ruta dice que no hay permiso", async () => {
    const dev = await s.conSesion("dev@ucsm.edu.pe");
    montar("/usuarios", dev.api);
    expect(await screen.findByText("No tienes permiso para ver esta sección.")).toBeInTheDocument();
    expect(screen.queryByRole("link", { name: /Usuarios/ })).not.toBeInTheDocument();
    expect(screen.getByText("Desarrollador")).toBeInTheDocument();
  });

  it("aunque el panel lo ocultara mal, el servicio rechaza la operación", async () => {
    const dev = await s.conSesion("dev@ucsm.edu.pe");
    expect(await dev.api.usuarios()).toMatchObject({ ok: false, error: { tipo: "Negocio", estado: 403, mensaje: "No tienes permiso para gestionar usuarios." } });
  });
});
