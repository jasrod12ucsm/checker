// Pruebas no funcionales de Centinela C++ (práctica 8): carga, estrés, volumen, configuración y seguridad.
//   docker compose run --rm sistema-no-funcionales          (dentro de la imagen: clang y el checker reales)
//   npx tsx no-funcionales/medir.ts [carga|estres|volumen|configuracion|seguridad]...
// Cada escenario arranca su propio Centinela en un proceso aparte (servidor.ts) y lo mide desde
// fuera por HTTP. Los resultados quedan en no-funcionales/resultados/<escenario>.json.
import { spawn, type ChildProcess } from "node:child_process";
import { mkdirSync, mkdtempSync, readFileSync, rmSync, statSync, writeFileSync } from "node:fs";
import { cpus, freemem, totalmem, tmpdir, type as so, release } from "node:os";
import { join } from "node:path";
import autocannon from "autocannon";
import { firmar } from "@centinela/cripto";
import { githubVarios } from "./github-varios";

const RESULTADOS = new URL("./resultados/", import.meta.url).pathname;
mkdirSync(RESULTADOS, { recursive: true });
const SERVIDOR = new URL("./servidor.ts", import.meta.url).pathname;
const PUERTO_GH = 9998;
let puerto = 8090;

interface Instancia {
  url: string;
  cookie: string;
  email: string;
  clave: string;
  secreto: string;
  repoId: string;
  sembradas: { ultima: string; grande: string };
  sembrarMs: number;
  bd: string;
  proceso: ChildProcess;
  memoria(): { rssMb: number; picoMb: number };
  detener(): Promise<void>;
}

/** Arranca un Centinela con su propia base en un directorio temporal. */
async function arrancar(entorno: Record<string, string> = {}): Promise<Instancia> {
  const p = puerto++;
  const dir = mkdtempSync(join(tmpdir(), "centinela-nf-"));
  const bd = join(dir, "centinela.db");
  const proceso = spawn(process.execPath, ["--import", "tsx", SERVIDOR], {
    env: { ...process.env, CENTINELA_PUERTO: String(p), CENTINELA_BD: bd, CENTINELA_URL_PUBLICA: `http://127.0.0.1:${p}`, CENTINELA_GITHUB_API: `http://127.0.0.1:${PUERTO_GH}`, CENTINELA_INTERVALO_MS: "100", ...entorno },
    stdio: ["ignore", "pipe", "pipe"],
  });
  let errores = "";
  proceso.stderr!.on("data", (c) => (errores += c));
  const info = await new Promise<Record<string, unknown>>((ok, mal) => {
    let salida = "";
    proceso.stdout!.on("data", (c: Buffer) => {
      salida += c;
      const m = /LISTO (\{.*\})/.exec(salida);
      if (m) ok(JSON.parse(m[1]!));
    });
    proceso.on("exit", (c) => mal(new Error(`el servidor terminó (${c}): ${errores}`)));
  });
  const estado = () => readFileSync(`/proc/${proceso.pid}/status`, "utf8");
  const mb = (campo: string) => Number(new RegExp(`${campo}:\\s+(\\d+)`).exec(estado())![1]) / 1024;
  return {
    ...(info as Omit<Instancia, "url" | "bd" | "proceso" | "memoria" | "detener">),
    url: `http://127.0.0.1:${p}`,
    bd,
    proceso,
    memoria: () => ({ rssMb: Math.round(mb("VmRSS")), picoMb: Math.round(mb("VmHWM")) }),
    detener: () =>
      new Promise((ok) => {
        proceso.once("exit", () => {
          rmSync(dir, { recursive: true, force: true });
          ok();
        });
        proceso.kill("SIGTERM");
      }),
  };
}

type Medicion = { solicitudesPorS: number; latenciaMs: { p50: number; p90: number; p97_5: number; p99: number; max: number }; total: number; no2xx: number; errores: number; timeouts: number; bytesPorS: number };

async function golpear(url: string, o: { connections: number; duration: number; headers?: Record<string, string>; method?: "GET" | "POST"; body?: string }): Promise<Medicion> {
  const r = await autocannon({ url, connections: o.connections, duration: o.duration, headers: o.headers ?? {}, method: o.method ?? "GET", ...(o.body ? { body: o.body } : {}), timeout: 10 });
  return {
    solicitudesPorS: Math.round(r.requests.average),
    latenciaMs: { p50: r.latency.p50, p90: r.latency.p90, p97_5: r.latency.p97_5, p99: r.latency.p99, max: r.latency.max },
    total: r.requests.total,
    no2xx: r.non2xx,
    errores: r.errors,
    timeouts: r.timeouts,
    bytesPorS: Math.round(r.throughput.average),
  };
}

const guardar = (nombre: string, datos: unknown) => {
  writeFileSync(join(RESULTADOS, `${nombre}.json`), `${JSON.stringify({ escenario: nombre, fecha: new Date().toISOString(), entorno: entorno(), datos }, null, 2)}\n`);
  console.log(`→ resultados/${nombre}.json`);
};

function entorno() {
  const leer = (f: string) => { try { return readFileSync(f, "utf8"); } catch { return ""; } };
  return {
    cpu: cpus()[0]?.model ?? "?",
    hilos: cpus().length,
    memoriaGb: Math.round(totalmem() / 2 ** 30),
    memoriaLibreGb: Math.round(freemem() / 2 ** 30),
    so: `${so()} ${release()}`,
    distribucion: /PRETTY_NAME="([^"]+)"/.exec(leer("/etc/os-release"))?.[1] ?? "?",
    node: process.version,
  };
}

const esperar = (ms: number) => new Promise((ok) => setTimeout(ok, ms));
const pedir = (i: Instancia, ruta: string, init: RequestInit = {}) => fetch(`${i.url}${ruta}`, { ...init, headers: { cookie: i.cookie, ...(init.headers as Record<string, string> | undefined) } });

async function webhook(i: Instancia, evento: string, firma = firmar(i.secreto, evento)) {
  const t = performance.now();
  const r = await fetch(`${i.url}/webhooks/github`, { method: "POST", headers: { "content-type": "application/json", "x-github-event": "pull_request", "x-hub-signature-256": firma }, body: evento });
  return { estado: r.status, ms: performance.now() - t, cuerpo: (await r.json()) as { revisionId?: string } };
}

/** Espera a que una revisión termine; devuelve su estado y cuánto tardó. */
async function terminar(i: Instancia, id: string, maxMs = 600_000) {
  const t = Date.now();
  for (;;) {
    const d = (await (await pedir(i, `/api/revisiones/${id}`)).json()) as { estado: { tipo: string; resumen?: Record<string, number> }; hallazgos: unknown[] };
    if (d.estado.tipo === "Publicada" || d.estado.tipo === "Fallida" || Date.now() - t > maxMs) return { ...d, ms: Date.now() - t };
    await esperar(100);
  }
}

// ── Carga: el uso normal esperado, sostenido ────────────────────────────────────────────
async function carga() {
  const i = await arrancar({ SEMBRAR: "1000", HALLAZGOS_POR_REVISION: "5", HALLAZGOS_GRANDE: "0" });
  const h = { cookie: i.cookie };
  const rutas: [string, string, Record<string, string>][] = [
    ["GET /salud", "/salud", {}],
    ["GET /api/sesion", "/api/sesion", h],
    ["GET /api/revisiones (200 de 1000)", "/api/revisiones", h],
    ["GET /api/revisiones/:id (5 hallazgos)", `/api/revisiones/${i.sembradas.ultima}`, h],
    ["GET /api/repositorios", "/api/repositorios", h],
    ["GET / (panel web)", "/", {}],
  ];
  const datos: Record<string, Medicion> = {};
  for (const [nombre, ruta, headers] of rutas) {
    datos[nombre] = await golpear(`${i.url}${ruta}`, { connections: 20, duration: 20, headers });
    console.log(nombre, datos[nombre]!.solicitudesPorS, "sol/s p99", datos[nombre]!.latenciaMs.p99, "ms");
  }
  guardar("carga", { conexiones: 20, duracionS: 20, base: "1000 revisiones, 5000 hallazgos", rutas: datos, memoria: i.memoria() });
  await i.detener();
}

// ── Estrés: subir la concurrencia hasta ver dónde se degrada ─────────────────────────────
async function estres() {
  const gh = githubVarios(PUERTO_GH, () => 1);
  const i = await arrancar({ SEMBRAR: "1000", HALLAZGOS_POR_REVISION: "5", HALLAZGOS_GRANDE: "0", CENTINELA_PARALELO: "4" });
  const escalones: Record<number, Medicion> = {};
  for (const c of [10, 50, 100, 200, 400, 800, 1600]) {
    escalones[c] = await golpear(`${i.url}/api/revisiones`, { connections: c, duration: 10, headers: { cookie: i.cookie } });
    console.log("estrés", c, "conexiones:", escalones[c]!.solicitudesPorS, "sol/s p99", escalones[c]!.latenciaMs.p99, "ms errores", escalones[c]!.errores + escalones[c]!.timeouts);
  }
  // El ingreso usa scrypt a propósito (caro): cuántos ingresos por segundo aguanta.
  const ingreso = await golpear(`${i.url}/api/sesion`, { connections: 20, duration: 10, method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ email: i.email, clave: i.clave }) });
  console.log("ingresos/s", ingreso.solicitudesPorS);

  // Ráfaga: 50 PR abiertos a la vez, cada uno analizado de verdad por clang y el checker.
  const N = 50;
  const t0 = performance.now();
  const acuses = await Promise.all(Array.from({ length: N }, (_, k) => webhook(i, gh.evento(k + 1))));
  const acuseMs = performance.now() - t0;
  const ids = acuses.map((a) => a.cuerpo.revisionId!);
  let pico = i.memoria().picoMb;
  const vigilar = setInterval(() => (pico = Math.max(pico, i.memoria().picoMb)), 500);
  const finales = [];
  for (const id of ids) finales.push(await terminar(i, id));
  clearInterval(vigilar);
  const drenadoS = (performance.now() - t0) / 1000;
  const lat = acuses.map((a) => a.ms).sort((a, b) => a - b);
  guardar("estres", {
    lectura: { ruta: "GET /api/revisiones (200 de 1000)", duracionS: 10, escalones },
    ingreso: { ruta: "POST /api/sesion (scrypt)", conexiones: 20, ...ingreso },
    rafagaWebhooks: {
      pr: N,
      estados: Object.fromEntries([...new Set(acuses.map((a) => a.estado))].map((e) => [e, acuses.filter((a) => a.estado === e).length])),
      acuseTotalMs: Math.round(acuseMs),
      acuseMs: { p50: Math.round(lat[Math.floor(N * 0.5)]!), p99: Math.round(lat[N - 1]!), max: Math.round(lat[N - 1]!) },
      publicadas: finales.filter((f) => f.estado.tipo === "Publicada").length,
      fallidas: finales.filter((f) => f.estado.tipo === "Fallida").length,
      drenadoS: Math.round(drenadoS),
      revisionesPorMinuto: Math.round((N / drenadoS) * 60 * 10) / 10,
      publicadoEnGitHub: { ...gh.publicados },
      memoriaPicoMb: pico,
    },
  });
  gh.cerrar();
  await i.detener();
}

// ── Volumen: mucha información guardada y PR grandes ─────────────────────────────────────
async function volumen() {
  const base: Record<string, unknown>[] = [];
  for (const n of [0, 1000, 20000]) {
    const i = await arrancar({ SEMBRAR: String(n), HALLAZGOS_POR_REVISION: "5", HALLAZGOS_GRANDE: n > 0 ? "500" : "0" });
    const lista = await golpear(`${i.url}/api/revisiones`, { connections: 10, duration: 10, headers: { cookie: i.cookie } });
    const cuerpo = (await (await pedir(i, "/api/revisiones")).json()) as unknown[];
    const fila: Record<string, unknown> = { revisiones: n, hallazgos: n * 5 + (n > 0 ? 500 : 0), sembrarS: Math.round(i.sembrarMs / 100) / 10, tamanoBdMb: Math.round((statSync(i.bd).size + (() => { try { return statSync(`${i.bd}-wal`).size; } catch { return 0; } })()) / 2 ** 20 * 10) / 10, listaDevuelve: cuerpo.length, lista };
    if (n > 0) {
      fila["detalleGrande"] = await golpear(`${i.url}/api/revisiones/${i.sembradas.grande}`, { connections: 10, duration: 10, headers: { cookie: i.cookie } });
      fila["detalleGrandeKb"] = Math.round(Buffer.byteLength(await (await pedir(i, `/api/revisiones/${i.sembradas.grande}`)).text()) / 1024);
    }
    fila["memoria"] = i.memoria();
    console.log("volumen", n, "lista p99", lista.latenciaMs.p99, "ms");
    base.push(fila);
    await i.detener();
  }
  // PR con 1, 10 y 40 archivos C++, analizados de verdad.
  const archivos = [1, 10, 40];
  const gh = githubVarios(PUERTO_GH, (n) => archivos[n - 1] ?? 1);
  const i = await arrancar({ CENTINELA_PARALELO: "4" });
  const pr: Record<string, unknown>[] = [];
  for (const [k, a] of archivos.entries()) {
    const w = await webhook(i, gh.evento(k + 1));
    const f = await terminar(i, w.cuerpo.revisionId!);
    pr.push({ archivos: a, estado: f.estado.tipo, hallazgos: f.hallazgos.length, resumen: f.estado.resumen, segundos: Math.round(f.ms / 100) / 10 });
    console.log("PR de", a, "archivos:", f.ms, "ms", f.hallazgos.length, "hallazgos");
  }
  gh.cerrar();
  // Un cuerpo de más de 5 MB se rechaza sin procesarlo.
  const enorme = await fetch(`${i.url}/webhooks/github`, { method: "POST", headers: { "content-type": "application/json" }, body: `{"x":"${"a".repeat(6 * 2 ** 20)}"}` });
  guardar("volumen", { base, pullRequests: pr, cuerpo6Mb: enorme.status });
  await i.detener();
}

// ── Configuración: el mismo trabajo con distintos ajustes del servicio ───────────────────
async function configuracion() {
  const gh = githubVarios(PUERTO_GH, () => 16);
  const paralelo: Record<string, unknown>[] = [];
  for (const p of [1, 2, 4, 8]) {
    const i = await arrancar({ CENTINELA_PARALELO: String(p) });
    const w = await webhook(i, gh.evento(p));
    const f = await terminar(i, w.cuerpo.revisionId!);
    paralelo.push({ paralelo: p, archivos: 16, estado: f.estado.tipo, hallazgos: f.hallazgos.length, segundos: Math.round(f.ms / 100) / 10, memoriaPicoMb: i.memoria().picoMb });
    console.log("paralelo", p, f.ms, "ms");
    await i.detener();
  }
  // Política del repositorio: «Possibly» publica confirmados y posibles; «Silent», solo confirmados.
  const politicas: Record<string, unknown> = {};
  for (const politica of ["Possibly", "Silent"]) {
    const i = await arrancar({});
    await pedir(i, `/api/repositorios/${i.repoId}`, { method: "PATCH", headers: { "content-type": "application/json" }, body: JSON.stringify({ politica }) });
    const w = await webhook(i, gh.evento(100));
    const f = await terminar(i, w.cuerpo.revisionId!);
    politicas[politica] = { estado: f.estado.tipo, resumen: f.estado.resumen, hallazgos: f.hallazgos.length };
    await i.detener();
  }
  // Tiempo máximo de análisis (CENTINELA_TIEMPO_MAXIMO_S): es por invocación de clang, es decir, por archivo.
  // Con 5 s y un solo hilo, un PR de 40 archivos tarda más de 5 s en total pero ningún archivo llega al límite.
  const gh40 = githubVarios(PUERTO_GH + 1, () => 40);
  const i = await arrancar({ CENTINELA_PARALELO: "1", CENTINELA_TIEMPO_MAXIMO_S: "5", CENTINELA_GITHUB_API: `http://127.0.0.1:${PUERTO_GH + 1}` });
  const w = await webhook(i, gh40.evento(1));
  const f = (await terminar(i, w.cuerpo.revisionId!)) as { estado: { tipo: string; motivo?: string }; ms: number };
  gh40.cerrar();
  await i.detener();
  gh.cerrar();
  guardar("configuracion", { paralelo, politicas, tiempoMaximoPorArchivo: { tiempoMaximoS: 5, paralelo: 1, archivos: 40, estado: f.estado.tipo, motivo: f.estado.motivo ?? null, segundos: Math.round(f.ms / 100) / 10 } });
}

// ── Seguridad: cada propiedad, comprobada contra el servicio en marcha ───────────────────
async function seguridad() {
  const gh = githubVarios(PUERTO_GH, () => 1, (n) => (n === 7 ? `<img src=x onerror="alert('xss')"> PR ${n}` : `PR ${n}`));
  const i = await arrancar({});
  const casos: { propiedad: string; prueba: string; esperado: string; obtenido: string; ok: boolean }[] = [];
  const caso = (propiedad: string, prueba: string, esperado: string, obtenido: string | number | boolean) => {
    casos.push({ propiedad, prueba, esperado, obtenido: String(obtenido), ok: String(obtenido) === esperado });
  };
  const sin = (ruta: string, method = "GET") => fetch(`${i.url}${ruta}`, { method, headers: { "content-type": "application/json" }, ...(method === "GET" ? {} : { body: "{}" }) }).then((r) => r.status);

  // Autenticación
  for (const [m, r] of [["GET", "/api/revisiones"], ["GET", "/api/repositorios"], ["GET", "/api/usuarios"], ["POST", "/api/revisiones"], ["PATCH", `/api/repositorios/${i.repoId}`], ["DELETE", `/api/repositorios/${i.repoId}`], ["PATCH", "/api/hallazgos/x"]] as const)
    caso("Autenticación", `${m} ${r} sin sesión`, "401", await sin(r, m));
  caso("Autenticación", "cookie inventada", "401", (await fetch(`${i.url}/api/revisiones`, { headers: { cookie: "centinela_sesion=inventada" } })).status);
  caso("Autenticación", "clave equivocada", "401", (await fetch(`${i.url}/api/sesion`, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ email: i.email, clave: "otraClave12345" }) })).status);
  const intentos = [];
  for (let k = 0; k < 11; k++) intentos.push((await fetch(`${i.url}/api/sesion`, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ email: "victima@ucsm.edu.pe", clave: `adivina${k}12345` }) })).status);
  caso("Autenticación", "11 claves equivocadas seguidas (fuerza bruta)", "429", intentos.at(-1)!);
  const ing = await fetch(`${i.url}/api/sesion`, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ email: i.email, clave: i.clave }) });
  const setCookie = ing.headers.get("set-cookie") ?? "";
  caso("Autenticación", "la cookie de sesión es HttpOnly", "true", /HttpOnly/i.test(setCookie));
  caso("Autenticación", "la cookie de sesión es SameSite=Strict", "true", /SameSite=Strict/i.test(setCookie));
  const otra = setCookie.split(";")[0]!;
  await fetch(`${i.url}/api/sesion`, { method: "DELETE", headers: { cookie: otra } });
  caso("Autenticación", "la sesión cerrada ya no sirve", "401", (await fetch(`${i.url}/api/revisiones`, { headers: { cookie: otra } })).status);

  // Autorización: una desarrolladora aprobada no administra.
  const dev = { email: "dev@ucsm.edu.pe", clave: "ClaveDev2026x" };
  await fetch(`${i.url}/api/registro`, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ ...dev, nombre: "Dev" }) });
  const usuarios = (await (await pedir(i, "/api/usuarios")).json()) as { id: string; email: string }[];
  const idDev = usuarios.find((u) => u.email === dev.email)!.id;
  caso("Autorización", "una cuenta pendiente no puede ingresar", "403", (await fetch(`${i.url}/api/sesion`, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(dev) })).status);
  await pedir(i, `/api/usuarios/${idDev}`, { method: "PATCH", headers: { "content-type": "application/json" }, body: JSON.stringify({ estado: "Activo", rol: "desarrollador" }) });
  const cDev = ((await fetch(`${i.url}/api/sesion`, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(dev) })).headers.get("set-cookie") ?? "").split(";")[0]!;
  const comoDev = (ruta: string, method: string, body?: unknown) => fetch(`${i.url}${ruta}`, { method, headers: { cookie: cDev, ...(body === undefined ? {} : { "content-type": "application/json" }) }, ...(body === undefined ? {} : { body: JSON.stringify(body) }) }).then((r) => r.status);
  caso("Autorización", "desarrollador lee revisiones", "200", await comoDev("/api/revisiones", "GET"));
  caso("Autorización", "desarrollador lista usuarios", "403", await comoDev("/api/usuarios", "GET"));
  caso("Autorización", "desarrollador conecta un repositorio", "403", await comoDev("/api/repositorios", "POST", { nombre: "otro/repo", politica: "Possibly", bloquearMerge: true }));
  caso("Autorización", "desarrollador cambia la política", "403", await comoDev(`/api/repositorios/${i.repoId}`, "PATCH", { politica: "Silent" }));
  caso("Autorización", "desarrollador se hace administrador", "403", await comoDev(`/api/usuarios/${idDev}`, "PATCH", { rol: "administrador" }));
  await pedir(i, `/api/usuarios/${idDev}`, { method: "PATCH", headers: { "content-type": "application/json" }, body: JSON.stringify({ estado: "Desactivado" }) });
  caso("Autorización", "al desactivarla, su sesión abierta deja de servir", "401", await comoDev("/api/revisiones", "GET"));

  await pedir(i, `/api/usuarios/${idDev}`, { method: "PATCH", headers: { "content-type": "application/json" }, body: JSON.stringify({ estado: "Activo" }) });
  const cDevActivo = ((await fetch(`${i.url}/api/sesion`, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(dev) })).headers.get("set-cookie") ?? "").split(";")[0]!;

  // Integridad: webhooks firmados y entradas validadas.
  const ev = gh.evento(7);
  caso("Integridad", "webhook sin firma", "401", (await webhook(i, ev, "")).estado);
  caso("Integridad", "webhook con firma de otro secreto", "401", (await webhook(i, ev, firmar("otro-secreto", ev))).estado);
  caso("Integridad", "webhook con el cuerpo alterado tras firmar", "401", (await webhook(i, ev.replace("PR 7", "PR 8"), firmar(i.secreto, ev))).estado);
  const bueno = await webhook(i, ev);
  caso("Integridad", "webhook bien firmado", "202", bueno.estado);
  caso("Integridad", "el mismo webhook repetido no duplica la revisión", "200", (await webhook(i, ev)).estado);
  for (const [n, p] of [["inyección SQL en el nombre del repositorio", { nombre: "a/b'; DROP TABLE usuarios;--", politica: "Possibly", bloquearMerge: true }], ["política desconocida", { nombre: "a/b", politica: "Todo", bloquearMerge: true }], ["tipos equivocados", { nombre: 5, politica: "Possibly", bloquearMerge: "si" }]] as const)
    caso("Integridad", n, "400", (await pedir(i, "/api/repositorios", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(p) })).status);
  caso("Integridad", "JSON mal formado", "400", (await pedir(i, "/api/repositorios", { method: "POST", headers: { "content-type": "application/json" }, body: "{nombre:" })).status);
  caso("Integridad", "id de revisión con inyección SQL", "400", (await pedir(i, `/api/revisiones/${encodeURIComponent("x' OR '1'='1")}`)).status);
  caso("Integridad", "cuerpo de 6 MB (límite 5 MB)", "413", (await fetch(`${i.url}/webhooks/github`, { method: "POST", headers: { "content-type": "application/json" }, body: `{"x":"${"a".repeat(6 * 2 ** 20)}"}` })).status);
  caso("Integridad", "la tabla usuarios sigue ahí después de la inyección", "200", (await pedir(i, "/api/usuarios")).status);

  // Confidencialidad: nada sensible sale en las respuestas.
  const todo = JSON.stringify([await (await pedir(i, "/api/usuarios")).json(), await (await pedir(i, "/api/sesion")).json(), await (await pedir(i, "/api/repositorios")).json()]);
  caso("Confidencialidad", "las respuestas no incluyen el hash de la clave", "false", /hash|scrypt|\$/.test(todo));
  const listaDev = await (await fetch(`${i.url}/api/repositorios`, { headers: { cookie: cDevActivo } })).text();
  caso("Confidencialidad", "un desarrollador no ve el secreto del webhook", "false", listaDev.includes(i.secreto));
  caso("Confidencialidad", "la clave no aparece en ninguna respuesta", "false", todo.includes(i.clave));
  const det = await terminar(i, bueno.cuerpo.revisionId!);
  caso("Confidencialidad", "el título con HTML se devuelve como texto (el panel no lo interpreta)", "true", JSON.stringify(det).includes("<img src=x"));
  const errores = await (await fetch(`${i.url}/api/revisiones/${encodeURIComponent("../../etc/passwd")}`)).text();
  caso("Confidencialidad", "un error no expone rutas ni trazas", "false", /\/opt\/|at .*\.ts|stack/i.test(errores));

  // Disponibilidad: el servicio sigue respondiendo tras todo lo anterior.
  caso("Disponibilidad", "GET /salud después de las pruebas", "200", await sin("/salud"));
  const cabeceras = Object.fromEntries((await fetch(`${i.url}/`)).headers.entries());
  const deApi = (await fetch(`${i.url}/api/revisiones`)).headers;
  caso("Integridad", "el panel declara una política de contenido que bloquea scripts ajenos y en línea", "true", (cabeceras["content-security-policy"] ?? "").includes("default-src 'self'"));
  caso("Integridad", "el panel no se deja enmarcar (clickjacking)", "DENY", cabeceras["x-frame-options"] ?? "");
  caso("Integridad", "la API pide no adivinar el tipo de contenido", "nosniff", deApi.get("x-content-type-options") ?? "");
  guardar("seguridad", { casos, aprobados: casos.filter((c) => c.ok).length, total: casos.length, cabecerasDelPanel: cabeceras });
  console.log(`seguridad: ${casos.filter((c) => c.ok).length}/${casos.length}`);
  for (const c of casos.filter((x) => !x.ok)) console.log("  FALLA", c.propiedad, c.prueba, "esperado", c.esperado, "obtenido", c.obtenido);
  // En el CI, una propiedad de seguridad que se rompe hace fallar la construcción (regresión).
  if (casos.some((c) => !c.ok)) process.exitCode = 1;
  gh.cerrar();
  await i.detener();
}

const ESCENARIOS = { carga, estres, volumen, configuracion, seguridad } as const;
const pedidos = process.argv.slice(2).filter((a): a is keyof typeof ESCENARIOS => a in ESCENARIOS);
for (const nombre of pedidos.length > 0 ? pedidos : (Object.keys(ESCENARIOS) as (keyof typeof ESCENARIOS)[])) {
  console.log(`\n=== ${nombre} ===`);
  await ESCENARIOS[nombre]();
}
process.exit(process.exitCode ?? 0);
