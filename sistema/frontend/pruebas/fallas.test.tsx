// El camino, no el negocio: el servicio caído o respondiendo fuera de contrato. El panel avisa y deja reintentar.
import { screen } from "@testing-library/react";
import { beforeEach, describe, expect, it } from "vitest";
import type { Api } from "../src/api/puerto";
import type { ErrorApi } from "../src/dominio/errores";
import { err } from "../src/dominio/resultado";
import { montar } from "./montar";
import { servicio, type Servicio } from "./servicio";

let s: Servicio;
let real: Api;
beforeEach(async () => {
  s = servicio();
  await s.registrar("lucia@ucsm.edu.pe", "Lucía Paredes");
  real = (await s.conSesion("lucia@ucsm.edu.pe")).api;
});

/** La API real, salvo `revisiones`, que falla las primeras `n` veces con el error dado. */
function conFallas(n: number, error: ErrorApi): Api {
  let restantes = n;
  return { ...real, revisiones: (repo) => (restantes-- > 0 ? Promise.resolve(err(error)) : real.revisiones(repo)) };
}

describe("fallas del camino", () => {
  it("sin red: lo dice con palabras y «Reintentar» vuelve a pedir", async () => {
    const m = montar("/revisiones", conFallas(1, { tipo: "Red", detalle: "Failed to fetch" }));
    expect(await screen.findByRole("alert")).toHaveTextContent("No se pudo contactar con Centinela.");
    await m.usuario.click(screen.getByRole("button", { name: "Reintentar" }));
    expect(await screen.findByText("Todavía no hay repositorios conectados.")).toBeInTheDocument();
  });

  it("una respuesta fuera de contrato no rompe la pantalla", async () => {
    montar("/revisiones", conFallas(1, { tipo: "RespuestaInvalida", detalle: "estado.tipo" }));
    expect(await screen.findByRole("alert")).toHaveTextContent("Centinela respondió algo inesperado.");
    expect(screen.getByRole("heading", { name: "Revisiones" })).toBeInTheDocument();
  });

  it("sin servicio al abrir el panel, queda en el ingreso (no en blanco)", async () => {
    const caido: Api = { ...real, sesion: () => Promise.resolve(err({ tipo: "Red", detalle: "x" })), estadoRegistro: () => Promise.resolve(err({ tipo: "Red", detalle: "x" })) };
    montar("/revisiones", caido);
    expect(await screen.findByRole("heading", { name: "Ingresa" })).toBeInTheDocument();
  });

  it("una ruta que no existe ofrece volver a las revisiones", async () => {
    montar("/no-existe", real);
    expect(await screen.findByText("Esta página no existe.")).toBeInTheDocument();
  });

  it("los avisos se cierran con su botón", async () => {
    await s.registrar("ana@ucsm.edu.pe", "Ana Huamán");
    const m = montar("/usuarios", real);
    await m.usuario.click(await screen.findByRole("button", { name: "Aprobar a Ana Huamán" }));
    await screen.findByText(/Se aprobó a Ana Huamán/);
    await m.usuario.click(screen.getByRole("button", { name: "Cerrar aviso" }));
    expect(screen.queryByText(/Se aprobó a Ana Huamán/)).not.toBeInTheDocument();
  });
});
