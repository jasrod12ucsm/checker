// CU-S03 de punta a punta: conectar, ver el webhook, editar la política, desconectar; el desarrollador solo mira.
import { screen, within } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { montar } from "./montar";
import { servicio, type Servicio } from "./servicio";

let s: Servicio;
let admin: Awaited<ReturnType<Servicio["conSesion"]>>;

beforeEach(async () => {
  s = servicio();
  await s.registrar("lucia@ucsm.edu.pe", "Lucía Paredes");
  admin = await s.conSesion("lucia@ucsm.edu.pe");
});

async function conectar(m: ReturnType<typeof montar>, nombre: string, politica?: "Possibly") {
  await m.usuario.click(await screen.findByRole("button", { name: "Conectar repositorio" }));
  const d = screen.getByRole("dialog", { name: "Conectar repositorio" });
  await m.usuario.type(within(d).getByLabelText("Repositorio"), nombre);
  if (politica) await m.usuario.click(within(d).getByRole("radio", { name: /Possibly/ }));
  await m.usuario.click(within(d).getByRole("button", { name: "Conectar" }));
  return d;
}

describe("CU-S03 repositorios", () => {
  it("sin repositorios, lo dice e invita a conectar el primero", async () => {
    montar("/repositorios", admin.api);
    expect(await screen.findByText("Todavía no hay repositorios conectados.")).toBeInTheDocument();
  });

  it("conectar muestra la URL del webhook y el secreto (oculto hasta pedirlo) con los pasos de GitHub", async () => {
    const m = montar("/repositorios", admin.api);
    await conectar(m, "https://github.com/lab-sistemas/simulador.git", "Possibly");
    const w = await screen.findByRole("dialog", { name: "Configura el webhook de lab-sistemas/simulador" });
    expect(within(w).getByText("Conectado")).toBeInTheDocument();
    expect(within(w).getByLabelText("URL del webhook")).toHaveValue("https://centinela.ucsm.edu.pe/webhooks/github");
    const secreto = within(w).getByLabelText("Secreto");
    expect(secreto).toHaveAttribute("type", "password");
    expect(secreto).toHaveValue("secreto");
    await m.usuario.click(within(w).getByRole("button", { name: /Mostrar/ }));
    expect(secreto).toHaveAttribute("type", "text");
    expect(within(w).getByText(/El paso 5 es lo que permite/)).toBeInTheDocument();
    await m.usuario.click(within(w).getByRole("button", { name: "Listo" }));

    const filaRepo = screen.getByRole("row", { name: /lab-sistemas\/simulador/ });
    expect(within(filaRepo).getByText("Possibly")).toBeInTheDocument();
    expect(within(filaRepo).getByText("Activo")).toBeInTheDocument();
    expect(within(filaRepo).getByText("Sí")).toBeInTheDocument();
  });

  it("copiar el secreto lo pone en el portapapeles", async () => {
    const m = montar("/repositorios", admin.api);
    await conectar(m, "lab-sistemas/simulador");
    const escribir = vi.spyOn(navigator.clipboard, "writeText");
    const w = await screen.findByRole("dialog", { name: /Configura el webhook/ });
    await m.usuario.click(within(w).getByRole("button", { name: "Copiar secreto" }));
    expect(escribir).toHaveBeenCalledWith("secreto");
    expect(within(w).getByText("Copiado")).toBeInTheDocument();
  });

  it("un nombre mal escrito no se envía; uno ya conectado lo rechaza el servicio en el mismo campo", async () => {
    const m = montar("/repositorios", admin.api);
    const d = await conectar(m, "solo-un-nombre");
    expect(within(d).getByText(/Escribe el repositorio como dueño\/nombre/)).toBeInTheDocument();
    await m.usuario.click(within(d).getByRole("button", { name: "Cancelar" }));

    await conectar(m, "lab-sistemas/simulador");
    await m.usuario.click(await screen.findByRole("button", { name: "Listo" }));
    const otra = await conectar(m, "lab-sistemas/simulador");
    expect(await within(otra).findByText("El repositorio ya está conectado.")).toBeInTheDocument();
  });

  it("editar la política y el bloqueo del merge", async () => {
    await admin.api.conectar({ nombre: "lab-sistemas/motor-rutas", politica: "Silent", bloquearMerge: true });
    const m = montar("/repositorios", admin.api);
    await m.usuario.click(await screen.findByRole("button", { name: "Editar lab-sistemas/motor-rutas" }));
    const d = screen.getByRole("dialog", { name: "Editar lab-sistemas/motor-rutas" });
    await m.usuario.click(within(d).getByRole("radio", { name: /Possibly/ }));
    await m.usuario.click(within(d).getByRole("switch"));
    await m.usuario.click(within(d).getByRole("button", { name: "Guardar" }));
    const filaRepo = await screen.findByRole("row", { name: /motor-rutas/ });
    expect(within(filaRepo).getByText("Possibly")).toBeInTheDocument();
    expect(within(filaRepo).getByText("No")).toBeInTheDocument();
    expect(await admin.api.repositorios()).toMatchObject({ ok: true, valor: [{ politica: "Possibly", bloquearMerge: false }] });
  });

  it("desconectar pide confirmación y deja el repositorio como desconectado, sin acciones", async () => {
    await admin.api.conectar({ nombre: "lab-sistemas/parser-config", politica: "Silent", bloquearMerge: false });
    const m = montar("/repositorios", admin.api);
    await m.usuario.click(await screen.findByRole("button", { name: "Desconectar lab-sistemas/parser-config" }));
    const d = screen.getByRole("dialog", { name: /^¿Desconectar lab-sistemas\/parser-config/ });
    await m.usuario.click(within(d).getByRole("button", { name: "Desconectar" }));
    expect(await screen.findByText(/Se desconectó/)).toBeInTheDocument();
    const filaRepo = screen.getByRole("row", { name: /parser-config/ });
    expect(within(filaRepo).getByText("Desconectado")).toBeInTheDocument();
    expect(within(filaRepo).queryByRole("button")).not.toBeInTheDocument();
  });

  it("el desarrollador ve la tabla pero no conecta, ni edita, ni ve el secreto", async () => {
    await admin.api.conectar({ nombre: "lab-sistemas/motor-rutas", politica: "Silent", bloquearMerge: true });
    await s.registrar("dev@ucsm.edu.pe", "Diego Quispe");
    const us = await admin.api.usuarios();
    await admin.api.actualizarUsuario(us.ok ? us.valor.find((u) => u.nombre === "Diego Quispe")!.id : "", { estado: "Activo" });
    const dev = await s.conSesion("dev@ucsm.edu.pe");
    montar("/repositorios", dev.api);
    expect(await screen.findByText("lab-sistemas/motor-rutas")).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Conectar repositorio" })).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /Editar|Desconectar|Webhook/ })).not.toBeInTheDocument();
    expect(await dev.api.repositorios()).toMatchObject({ ok: true, valor: [{ webhook: null }] });
  });
});
