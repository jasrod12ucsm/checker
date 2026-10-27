// El sistema compuesto de verdad (SQLite, scrypt, Fastify, trabajador) con GitHub y clang falsos.
import { afterEach, expect, it } from "vitest";
import { leerConfiguracion } from "./configuracion";
import { componer } from "./componer";
import { AnalizadorFalso, GitHubFalso } from "../../../pruebas/dobles";

let sistema: ReturnType<typeof componer> | undefined;
afterEach(async () => {
  await sistema?.detener();
});

it("arranca vacío, atiende el registro y el HTTP, y el trabajador procesa la cola", async () => {
  const c = leerConfiguracion({
    CENTINELA_GITHUB_TOKEN: "t",
    CENTINELA_BD: ":memory:",
    CENTINELA_PUERTO: "0",
    CENTINELA_HOST: "127.0.0.1",
    CENTINELA_INTERVALO_MS: "50",
  });
  const github = new GitHubFalso();
  github.prs.set(3, { numero: 3 as never, titulo: "T", autor: "a", shaCabeza: "abc" });
  sistema = componer(c, { github, fuentes: { obtener: async () => ({ dir: "/tmp", liberar: async () => {} }) }, analizador: new AnalizadorFalso() });
  await sistema.arrancar();
  const s = sistema.servidor;
  expect((await s.inject({ method: "GET", url: "/api/registro" })).json()).toEqual({ hayUsuarios: false });
  const ingreso = await s.inject({ method: "POST", url: "/api/registro", payload: { email: "admin@ucsm.edu.pe", nombre: "Admin", clave: "clave12345678" } });
  expect(ingreso.statusCode).toBe(201);
  const cookie = ingreso.headers["set-cookie"] as string;
  const repo = (await s.inject({ method: "POST", url: "/api/repositorios", headers: { cookie }, payload: { nombre: "ucsm/demo", politica: "Silent", bloquearMerge: false } })).json();
  const r = (await s.inject({ method: "POST", url: "/api/revisiones", headers: { cookie }, payload: { repositorioId: repo.id, numeroPr: 3 } })).json();
  let estado = "Pendiente";
  for (let i = 0; i < 40 && estado !== "Publicada"; i++) {
    await new Promise((ok) => setTimeout(ok, 50));
    estado = (await s.inject({ method: "GET", url: `/api/revisiones/${r.id}`, headers: { cookie } })).json().estado.tipo;
  }
  expect(estado).toBe("Publicada");
  expect(github.estados.map((e) => e.estado.estado)).toEqual(["pending", "pending", "success"]);
});
