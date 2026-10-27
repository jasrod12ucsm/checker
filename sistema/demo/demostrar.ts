// Demostración de punta a punta: GitHub simulado + Centinela real (SQLite, clang y el checker).
//   docker compose run --rm -p 8080:8080 sistema npx tsx demo/demostrar.ts
// Centinela arranca vacío (no hay usuarios predefinidos). La demostración se registra
// como primera usuaria —queda de administradora— con una clave aleatoria, conecta el
// repositorio, simula el webhook del PR #1 firmado con su secreto, espera la revisión e
// imprime lo que Centinela publicó en GitHub. Después queda en marcha en
// http://localhost:8080 con la cuenta que imprimió.
import { randomBytes } from "node:crypto";
import { firmar } from "@centinela/cripto";
import { componer, leerConfiguracion } from "@centinela/app";
import { githubFalso, REPO } from "./github-falso";

const PUERTO_GH = 9999;
const gh = githubFalso(PUERTO_GH);
const sistema = componer(
  leerConfiguracion({
    ...process.env,
    CENTINELA_GITHUB_TOKEN: "demo",
    CENTINELA_GITHUB_API: `http://127.0.0.1:${PUERTO_GH}`,
    CENTINELA_BD: process.env["CENTINELA_DEMO_BD"] ?? ":memory:",
    CENTINELA_INTERVALO_MS: "200",
  }),
);
await sistema.arrancar();
const s = sistema.servidor;

const email = `demo-${randomBytes(3).toString("hex")}@centinela.local`;
const clave = `${randomBytes(9).toString("base64url")}9a`;
const registro = await s.inject({ method: "POST", url: "/api/registro", payload: { email, nombre: "Demostración", clave } });
if (registro.statusCode !== 201) throw new Error(`no se pudo registrar: ${registro.body}`);
const cookie = String(registro.headers["set-cookie"]);
console.log(`\n0. Registro de la primera cuenta (queda de administradora): ${email}`);
const conectado = await s.inject({ method: "POST", url: "/api/repositorios", headers: { cookie }, payload: { nombre: REPO, politica: "Possibly", bloquearMerge: true } });
const repo = conectado.json();
if (conectado.statusCode !== 201) throw new Error(`no se conectó el repositorio: ${conectado.body}`);
console.log(`1. Repositorio ${REPO} conectado. Webhook: ${repo.webhook.url}`);

const evento = gh.evento();
const w = await s.inject({
  method: "POST",
  url: "/webhooks/github",
  headers: { "content-type": "application/json", "x-github-event": "pull_request", "x-hub-signature-256": firmar(repo.webhook.secreto, evento) },
  payload: evento,
});
console.log(`2. GitHub avisa que se abrió el PR #1 → ${w.statusCode} ${w.body}`);

const id = w.json().revisionId as string;
let det = { estado: { tipo: "Pendiente" } } as { estado: { tipo: string; veredicto?: string; resumen?: unknown }; hallazgos?: { archivo: string; linea: number; clase: string; mensaje: string }[] };
for (let i = 0; i < 300 && (det.estado.tipo === "Pendiente" || det.estado.tipo === "EnAnalisis"); i++) {
  await new Promise((ok) => setTimeout(ok, 200));
  det = (await s.inject({ method: "GET", url: `/api/revisiones/${id}`, headers: { cookie } })).json();
}
console.log(`3. Revisión ${det.estado.tipo}: ${det.estado.veredicto ?? ""} ${JSON.stringify(det.estado.resumen ?? {})}`);
for (const h of det.hallazgos ?? []) console.log(`   - ${h.archivo}:${h.linea} [${h.clase}] ${h.mensaje}`);

if (process.argv.includes("--json")) console.log(JSON.stringify(det, null, 2));
console.log("4. Lo que Centinela publicó en GitHub:");
for (const r of gh.registro) {
  const c = r.cuerpo as { state?: string; description?: string; comments?: { path: string; line: number }[] };
  if (r.tipo === "estado") console.log(`   estado del commit: ${c.state} — ${c.description}`);
  else console.log(`   revisión con ${c.comments?.length ?? 0} comentarios en línea: ${c.comments?.map((x) => `${x.path}:${x.line}`).join(", ")}`);
}

if (process.argv.includes("--salir")) {
  await sistema.detener();
  gh.cerrar();
  const ok = det.estado.veredicto === "ConProblemas" && (det.hallazgos ?? []).every((h) => h.archivo === "src/cache.cpp");
  process.exit(ok ? 0 : 1);
}
console.log(`\nCentinela sigue en marcha: http://localhost:8080 — ${email} / ${clave} (Ctrl+C para salir)`);
