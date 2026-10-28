// CU-S04 a CU-S07 de punta a punta: revisar un PR, verlo avanzar solo, leer sus hallazgos, clasificarlos y reintentar.
import { screen, waitFor, within } from "@testing-library/react";
import { beforeEach, describe, expect, it } from "vitest";
import type { Repositorio } from "../src/dominio/modelo";
import { montar } from "./montar";
import { AVISOS_DEMO, servicio, type Servicio } from "./servicio";

const SHA = "d3m0000000000000000000000000000000000001";

let s: Servicio;
let admin: Awaited<ReturnType<Servicio["conSesion"]>>;
let repo: Repositorio;

beforeEach(async () => {
  s = servicio();
  await s.registrar("lucia@ucsm.edu.pe", "Lucía Paredes");
  admin = await s.conSesion("lucia@ucsm.edu.pe");
  const r = await admin.api.conectar({ nombre: "demo/centinela-demo", politica: "Possibly", bloquearMerge: true });
  if (!r.ok) throw new Error("no conectó");
  repo = r.valor;
  s.prEnGitHub(1, "Agrega una caché de nombres", SHA, AVISOS_DEMO);
});

/** Pide la revisión por la API (como lo haría el webhook) y devuelve su id. */
async function revisionPedida(numero = 1) {
  const r = await admin.api.solicitar(repo.id, numero);
  if (!r.ok) throw new Error(JSON.stringify(r.error));
  return r.valor.id;
}

describe("CU-S06 lista de revisiones", () => {
  it("sin revisiones, explica de dónde salen", async () => {
    montar("/revisiones", admin.api);
    expect(await screen.findByText("Todavía no hay revisiones.")).toBeInTheDocument();
  });

  it("sin repositorios, el administrador recibe el enlace para conectar el primero", async () => {
    const otro = servicio();
    await otro.registrar("a@ucsm.edu.pe", "A");
    const n = await otro.conSesion("a@ucsm.edu.pe");
    montar("/revisiones", n.api);
    expect(await screen.findByText("Todavía no hay repositorios conectados.")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Conecta el primero" })).toHaveAttribute("href", "/repositorios");
  });

  it("una revisión pendiente se ve en curso y la lista se actualiza sola hasta publicarla", async () => {
    await revisionPedida();
    montar("/revisiones", admin.api);
    const filaPr = await screen.findByRole("row", { name: /Agrega una caché de nombres/ });
    expect(within(filaPr).getByText("Pendiente")).toBeInTheDocument();
    expect(within(filaPr).getByText("d3m0000")).toBeInTheDocument();
    expect(screen.getByText("Se actualiza sola")).toBeInTheDocument();

    await s.trabajar();
    expect(await within(await screen.findByRole("row", { name: /Agrega una caché/ })).findByText("Publicada · Con problemas")).toBeInTheDocument();
    expect(screen.getByText("1 confirmados · 1 posibles · 0 descartados")).toBeInTheDocument();
    await waitFor(() => expect(screen.queryByText("Se actualiza sola")).not.toBeInTheDocument());
  });

  it("filtra por estado y por repositorio", async () => {
    await revisionPedida();
    await s.trabajar();
    s.prEnGitHub(2, "Corrige el pool de nodos", "a".repeat(40), []);
    await revisionPedida(2);
    await s.trabajar();
    const m = montar("/revisiones", admin.api);
    await screen.findByText("2 revisiones");
    await m.usuario.selectOptions(screen.getByLabelText("Estado"), "Aprobada");
    expect(screen.getByText("1 revisión")).toBeInTheDocument();
    expect(screen.getByText("Corrige el pool de nodos")).toBeInTheDocument();
    expect(screen.queryByText("Agrega una caché de nombres")).not.toBeInTheDocument();
    await m.usuario.selectOptions(screen.getByLabelText("Estado"), "Fallida");
    expect(screen.getByText("Ninguna revisión cumple el filtro.")).toBeInTheDocument();
    await m.usuario.selectOptions(screen.getByLabelText("Estado"), "Todos");
    await m.usuario.selectOptions(screen.getByLabelText("Repositorio"), repo.id);
    expect(screen.getByText("2 revisiones")).toBeInTheDocument();
  });
});

describe("CU-S05 revisar un PR ahora", () => {
  it("pide la revisión, abre su detalle y lo ve terminar sin recargar", async () => {
    const m = montar("/revisiones", admin.api);
    await m.usuario.click(await screen.findByRole("button", { name: "Revisar un PR ahora" }));
    const d = screen.getByRole("dialog", { name: "Revisar un PR ahora" });
    expect(within(d).getByLabelText("Repositorio")).toHaveValue(repo.id);
    await m.usuario.type(within(d).getByLabelText("Número de PR"), "1");
    await m.usuario.click(within(d).getByRole("button", { name: "Revisar" }));
    expect(await screen.findByRole("heading", { name: "Agrega una caché de nombres" })).toBeInTheDocument();
    expect(m.ubicacion()).toMatch(/^\/revisiones\/[0-9a-f-]+$/);
    expect(screen.getByText("Pendiente")).toBeInTheDocument();
    expect(screen.getByText("manual")).toBeInTheDocument();

    await s.trabajar();
    expect(await screen.findByText("Publicada · Con problemas")).toBeInTheDocument();
  });

  it("un número inválido no se envía", async () => {
    const m = montar("/revisiones", admin.api);
    await m.usuario.click(await screen.findByRole("button", { name: "Revisar un PR ahora" }));
    const d = screen.getByRole("dialog");
    await m.usuario.type(within(d).getByLabelText("Número de PR"), "abc");
    await m.usuario.click(within(d).getByRole("button", { name: "Revisar" }));
    expect(within(d).getByText(/Escribe el número del pull request/)).toBeInTheDocument();
  });

  it("si GitHub no tiene el PR, muestra el error del servicio", async () => {
    const m = montar("/revisiones", admin.api);
    await m.usuario.click(await screen.findByRole("button", { name: "Revisar un PR ahora" }));
    const d = screen.getByRole("dialog");
    await m.usuario.type(within(d).getByLabelText("Número de PR"), "99");
    await m.usuario.click(within(d).getByRole("button", { name: "Revisar" }));
    expect(await within(d).findByText(/GitHub no respondió como se esperaba/)).toBeInTheDocument();
  });

  it("si ese commit ya se revisó, lo dice y enlaza la revisión existente", async () => {
    const id = await revisionPedida();
    await s.trabajar();
    const m = montar("/revisiones", admin.api);
    await m.usuario.click(await screen.findByRole("button", { name: "Revisar un PR ahora" }));
    const d = screen.getByRole("dialog");
    await m.usuario.type(within(d).getByLabelText("Número de PR"), "#1");
    await m.usuario.click(within(d).getByRole("button", { name: "Revisar" }));
    expect(await within(d).findByText(/Ese commit ya se revisó/)).toBeInTheDocument();
    expect(within(d).getByRole("link", { name: "Ir a la revisión" })).toHaveAttribute("href", `/revisiones/${id}`);
  });
});

describe("CU-S06 y CU-S07 detalle, clasificar y reintentar", () => {
  it("muestra el veredicto, las cifras, cada hallazgo con su ruta y el bloqueo del merge", async () => {
    const id = await revisionPedida();
    await s.trabajar();
    montar(`/revisiones/${id}`, admin.api);
    expect(await screen.findByText("Publicada · Con problemas")).toBeInTheDocument();
    expect(screen.getByText(/bloquea el merge/)).toBeInTheDocument();
    expect(screen.getByText("Veredicto: 1 uso confirmado y 1 posible de una referencia invalidada (política Possibly).")).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: /Hallazgos 2 en 1 archivo/ })).toBeInTheDocument();
    const posible = screen.getByRole("article", { name: "Hallazgo en la línea 17" });
    expect(within(posible).getByText("17:12")).toBeInTheDocument();
    expect(within(posible).getByText("std::vector::push_back", { selector: "p code" })).toBeInTheDocument();
    expect(within(posible).getAllByRole("listitem")).toHaveLength(3);
    expect(within(screen.getByRole("article", { name: "Hallazgo en la línea 24" })).getByText("Confirmado", { selector: ".insignia" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /Ver archivo en el PR/ })).toHaveAttribute("href", "https://github.com/demo/centinela-demo/pull/1/files");
  });

  it("clasificar como falso positivo lo oculta, guarda quién lo marcó y el interruptor lo vuelve a mostrar", async () => {
    const id = await revisionPedida();
    await s.trabajar();
    const m = montar(`/revisiones/${id}`, admin.api, s.reloj);
    const posible = await screen.findByRole("article", { name: "Hallazgo en la línea 17" });
    await m.usuario.click(within(posible).getByRole("button", { name: "Falso positivo" }));
    await waitFor(() => expect(screen.queryByRole("article", { name: "Hallazgo en la línea 17" })).not.toBeInTheDocument());
    expect(screen.getByRole("heading", { name: /Hallazgos 1 en 1 archivo/ })).toBeInTheDocument();

    await m.usuario.click(screen.getByRole("switch", { name: "Mostrar falsos positivos (1)" }));
    const otraVez = screen.getByRole("article", { name: "Hallazgo en la línea 17" });
    expect(within(otraVez).getByRole("button", { name: /Falso positivo/ })).toHaveAttribute("aria-pressed", "true");
    expect(within(otraVez).getByText("Marcado por Lucía Paredes · hace un momento")).toBeInTheDocument();

    const det = await admin.api.revision(id);
    expect(det.ok && det.valor.hallazgos.find((h) => h.linea === 17)).toMatchObject({ clasificacion: "FalsoPositivo", autoria: { por: { nombre: "Lucía Paredes" } } });
  });

  it("reintentar después de marcar el falso positivo: la nueva corrida lo descarta y queda aprobada", async () => {
    s.prEnGitHub(1, "Agrega una caché de nombres", SHA, [AVISOS_DEMO[0]!]);
    const id = await revisionPedida();
    await s.trabajar();
    const m = montar(`/revisiones/${id}`, admin.api);
    await m.usuario.click(within(await screen.findByRole("article", { name: "Hallazgo en la línea 17" })).getByRole("button", { name: "Falso positivo" }));
    await screen.findByRole("switch", { name: "Mostrar falsos positivos (1)" });
    await m.usuario.click(screen.getByRole("button", { name: "Reintentar" }));
    expect(await screen.findByText("Revisión en cola de nuevo.")).toBeInTheDocument();
    await s.trabajar();
    expect(await screen.findByText("Publicada · Aprobada")).toBeInTheDocument();
    expect(screen.getByText("2", { selector: ".datos dd" })).toBeInTheDocument();
    expect(within(screen.getByText("Descartados como falso positivo").closest(".cifra")! as HTMLElement).getByText("1")).toBeInTheDocument();
  });

  it("una revisión fallida dice por qué y se puede reintentar", async () => {
    s.t.analizador.error = new Error("clang terminó con código 1");
    const id = await revisionPedida();
    await s.trabajar();
    const m = montar(`/revisiones/${id}`, admin.api);
    expect(await screen.findByText("Fallida")).toBeInTheDocument();
    expect(screen.getByText(/No se pudo completar:/)).toBeInTheDocument();
    s.t.analizador.error = undefined;
    await m.usuario.click(screen.getByRole("button", { name: "Reintentar" }));
    await s.trabajar();
    expect(await screen.findByText("Publicada · Con problemas")).toBeInTheDocument();
  });

  it("una revisión que no existe muestra el error del servicio con la opción de reintentar", async () => {
    montar("/revisiones/00000000-0000-4000-8000-ffffffffffff", admin.api);
    expect(await screen.findByText("La revisión no existe.")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Reintentar" })).toBeInTheDocument();
  });

  it("el desarrollador también revisa y clasifica (su rol lo permite)", async () => {
    const id = await revisionPedida();
    await s.trabajar();
    await s.registrar("dev@ucsm.edu.pe", "Diego Quispe");
    const us = await admin.api.usuarios();
    await admin.api.actualizarUsuario(us.ok ? us.valor.find((u) => u.nombre === "Diego Quispe")!.id : "", { estado: "Activo" });
    const dev = await s.conSesion("dev@ucsm.edu.pe");
    const m = montar(`/revisiones/${id}`, dev.api, s.reloj);
    const confirmado = await screen.findByRole("article", { name: "Hallazgo en la línea 24" });
    await m.usuario.click(within(confirmado).getByRole("button", { name: "Confirmado" }));
    expect(await within(confirmado).findByText(/Marcado por Diego Quispe/)).toBeInTheDocument();
  });
});
