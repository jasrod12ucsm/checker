// Pruebas de extremo a extremo, de configuración y de accesibilidad del panel (práctica 8).
// Se corren desde la máquina anfitriona contra la demostración real (clang y el checker en Docker):
//   docker compose up sistema-demo            (imprime la cuenta de administración)
//   npx tsx no-funcionales/navegadores.ts <correo> <clave> [carpeta-capturas]
// Cada navegador recorre los casos de uso como lo haría una persona (con aserciones, no solo
// capturas); luego se revisa cada pantalla en tres tamaños y dos temas, y se audita con axe-core
// contra WCAG 2.1 AA. Resultados en no-funcionales/resultados/navegadores.json.
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { cpus, release, totalmem } from "node:os";
import { chromium, firefox, webkit, type Browser, type BrowserType, type Page } from "playwright-core";

const EMAIL = process.argv[2] ?? "";
const CLAVE = process.argv[3] ?? "";
const CAPTURAS = process.argv[4];
if (!EMAIL || !CLAVE) throw new Error("uso: navegadores.ts <correo> <clave> [carpeta-capturas]");
const URL_BASE = process.env["CENTINELA_URL"] ?? "http://localhost:8080";
const RESULTADOS = new URL("./resultados/", import.meta.url).pathname;
mkdirSync(RESULTADOS, { recursive: true });
const AXE = readFileSync(new URL("../node_modules/axe-core/axe.min.js", import.meta.url), "utf8");
const CLAVE_EQUIPO = "EquipoUcsm2026";

const NAVEGADORES: { nombre: string; tipo: BrowserType; opciones: Parameters<BrowserType["launch"]>[0] }[] = [
  { nombre: "Google Chrome", tipo: chromium, opciones: { executablePath: "/usr/bin/google-chrome" } },
  { nombre: "Chromium", tipo: chromium, opciones: { executablePath: "/snap/bin/chromium" } },
  { nombre: "Firefox (Gecko)", tipo: firefox, opciones: {} },
  { nombre: "WebKit (motor de Safari)", tipo: webkit, opciones: {} },
];

type Paso = { caso: string; cu: string; ok: boolean; acciones: number; ms: number; error?: string };

/** Un escenario cuenta sus acciones (clics y campos llenados): la medida de eficiencia de la tarea. */
async function escenario(pasos: Paso[], caso: string, cu: string, f: (accion: () => void) => Promise<void>) {
  let acciones = 0;
  const t = performance.now();
  try {
    await f(() => acciones++);
    pasos.push({ caso, cu, ok: true, acciones, ms: Math.round(performance.now() - t) });
  } catch (e) {
    pasos.push({ caso, cu, ok: false, acciones, ms: Math.round(performance.now() - t), error: String(e).split("\n")[0]! });
  }
}

async function recorrido(b: Browser, id: string): Promise<Paso[]> {
  const pasos: Paso[] = [];
  const nueva = async () => (await b.newContext({ viewport: { width: 1440, height: 900 }, locale: "es-PE", timezoneId: "America/Lima" })).newPage();
  const admin = await nueva();
  const sufijo = Date.now().toString(36).slice(-4);
  const quien = { email: `ana.${id}.${sufijo}@ucsm.edu.pe`, nombre: `Ana ${id} ${sufijo}` };
  const repo = `lab-${id}-${sufijo}/motor-rutas`;

  await escenario(pasos, "E2E-01 Ingreso con clave equivocada y luego correcta", "CU-S01", async (a) => {
    await admin.goto(`${URL_BASE}/ingreso`);
    await admin.getByLabel("Correo").fill(EMAIL); a();
    await admin.getByLabel("Clave").fill("claveEquivocada1"); a();
    await admin.getByRole("button", { name: "Ingresar" }).click(); a();
    await admin.getByRole("alert").waitFor();
    await admin.getByLabel("Clave").fill(CLAVE); a();
    await admin.getByRole("button", { name: "Ingresar" }).click(); a();
    await admin.getByRole("heading", { name: "Revisiones" }).waitFor();
  });

  await escenario(pasos, "E2E-02 Ver el detalle de una revisión real y su veredicto", "CU-S06", async (a) => {
    await admin.getByRole("link", { name: "Agrega una caché de nombres" }).click(); a();
    await admin.getByText("Publicada · Con problemas").waitFor();
    await admin.getByRole("article", { name: /Hallazgo en la línea/ }).nth(1).waitFor();
    const n = await admin.getByRole("article", { name: /Hallazgo en la línea/ }).count();
    if (n < 2) throw new Error(`se esperaban 2 hallazgos y hay ${n}`);
  });

  await escenario(pasos, "E2E-03 Clasificar un hallazgo como confirmado", "CU-S07", async (a) => {
    const primero = admin.getByRole("article", { name: /Hallazgo en la línea/ }).first();
    await primero.getByRole("button", { name: "Confirmado" }).click(); a();
    await primero.getByText(/Marcado por/).waitFor();
  });

  await escenario(pasos, "E2E-04 Marcar un falso positivo: deja de verse y se puede volver a mostrar", "CU-S07", async (a) => {
    const segundo = admin.getByRole("article", { name: /Hallazgo en la línea/ }).nth(1);
    await segundo.getByRole("button", { name: "Falso positivo" }).click(); a();
    await admin.getByRole("switch", { name: /Mostrar falsos positivos \(1\)/ }).waitFor();
    const visibles = await admin.getByRole("article", { name: /Hallazgo en la línea/ }).count();
    if (visibles !== 1) throw new Error(`quedan ${visibles} hallazgos visibles`);
    await admin.getByRole("switch", { name: /Mostrar falsos positivos/ }).check(); a();
    await admin.getByRole("article", { name: /Hallazgo en la línea/ }).nth(1).waitFor();
    // Se deja como estaba para el siguiente navegador.
    await admin.getByRole("article", { name: /Hallazgo en la línea/ }).nth(1).getByRole("button", { name: "Sin revisar" }).click(); a();
    await admin.getByRole("article", { name: /Hallazgo en la línea/ }).first().getByRole("button", { name: "Sin revisar" }).click(); a();
  });

  await escenario(pasos, "E2E-05 Revisar ahora un PR ya revisado: el panel enlaza la revisión existente", "CU-S05", async (a) => {
    await admin.getByRole("link", { name: "Revisiones" }).first().click(); a();
    await admin.getByRole("button", { name: "Revisar un PR ahora" }).click(); a();
    await admin.getByLabel("Número de PR").fill("1"); a();
    await admin.getByRole("button", { name: "Revisar", exact: true }).click(); a();
    await admin.getByText(/Ese commit ya se revisó/).waitFor();
    await admin.keyboard.press("Escape"); a();
  });

  await escenario(pasos, "E2E-06 Conectar un repositorio y obtener su webhook", "CU-S03", async (a) => {
    await admin.getByRole("link", { name: "Repositorios" }).click(); a();
    await admin.getByRole("button", { name: "Conectar repositorio" }).click(); a();
    await admin.getByRole("textbox", { name: "Repositorio" }).fill(repo); a();
    await admin.getByRole("button", { name: "Conectar", exact: true }).click(); a();
    await admin.getByText("Conectado", { exact: true }).waitFor();
    await admin.getByRole("button", { name: "Listo" }).click(); a();
    await admin.getByRole("button", { name: `Webhook de ${repo}` }).waitFor();
  });

  const otra = await nueva();
  await escenario(pasos, "E2E-07 Registrarse: la cuenta queda pendiente y no puede ingresar", "CU-S01", async (a) => {
    await otra.goto(`${URL_BASE}/registro`);
    await otra.getByLabel("Correo").fill(quien.email); a();
    await otra.getByLabel("Nombre").fill(quien.nombre); a();
    await otra.getByLabel("Clave", { exact: true }).fill(CLAVE_EQUIPO); a();
    await otra.getByLabel("Confirmar clave").fill(CLAVE_EQUIPO); a();
    await otra.getByRole("button", { name: "Crear cuenta" }).click(); a();
    await otra.getByText("Pendiente de aprobación").waitFor();
    await otra.goto(`${URL_BASE}/ingreso`);
    await otra.getByLabel("Correo").fill(quien.email); a();
    await otra.getByLabel("Clave").fill(CLAVE_EQUIPO); a();
    await otra.getByRole("button", { name: "Ingresar" }).click(); a();
    await otra.getByRole("alert").waitFor();
  });

  await escenario(pasos, "E2E-08 La administración aprueba la cuenta como desarrollador", "CU-S02", async (a) => {
    await admin.getByRole("link", { name: /Usuarios/ }).click(); a();
    await admin.getByRole("button", { name: `Aprobar a ${quien.nombre}` }).click(); a();
    await admin.getByText(new RegExp(`Se aprobó a ${quien.nombre}`)).waitFor();
  });

  await escenario(pasos, "E2E-09 El desarrollador ingresa, revisa, y no puede administrar", "CU-S01, CU-S06", async (a) => {
    await otra.getByRole("button", { name: "Ingresar" }).click(); a();
    await otra.getByRole("heading", { name: "Revisiones" }).waitFor();
    if ((await otra.getByRole("link", { name: /Usuarios/ }).count()) > 0) throw new Error("el desarrollador ve «Usuarios»");
    await otra.goto(`${URL_BASE}/usuarios`);
    await otra.getByText("No tienes permiso para ver esta sección.").waitFor();
  });

  await escenario(pasos, "E2E-10 Cerrar sesión protege el panel", "CU-S01", async (a) => {
    await otra.goto(`${URL_BASE}/revisiones`);
    await otra.getByRole("button", { name: "Cerrar sesión" }).click(); a();
    await otra.getByRole("heading", { name: "Ingresa" }).waitFor();
    await otra.goto(`${URL_BASE}/revisiones`);
    await otra.getByRole("heading", { name: "Ingresa" }).waitFor();
  });

  await escenario(pasos, "E2E-11 Desconectar el repositorio de prueba", "CU-S03", async (a) => {
    await admin.getByRole("link", { name: "Repositorios" }).click(); a();
    await admin.getByRole("button", { name: `Desconectar ${repo}` }).click(); a();
    await admin.getByRole("dialog").getByRole("button", { name: "Desconectar" }).click(); a();
    await admin.getByRole("dialog").waitFor({ state: "detached" });
  });
  await otra.context().close();
  await admin.context().close();
  return pasos;
}

/** Cada pantalla, en celular, tableta y escritorio, claro y oscuro: sin desborde horizontal y con su título visible. */
async function configuraciones(b: Browser, id: string, estado: Awaited<ReturnType<typeof sesion>>) {
  const filas: { pantalla: string; ancho: number; tema: string; ok: boolean; desborde: number }[] = [];
  for (const [ancho, alto] of [[390, 844], [768, 1024], [1440, 900]] as const) {
    for (const tema of ["light", "dark"] as const) {
      const c = await b.newContext({ viewport: { width: ancho, height: alto }, colorScheme: tema, locale: "es-PE", timezoneId: "America/Lima", storageState: estado });
      const p = await c.newPage();
      for (const [pantalla, ruta, titulo] of [["Revisiones", "/revisiones", "Revisiones"], ["Repositorios", "/repositorios", "Repositorios"], ["Usuarios", "/usuarios", "Usuarios"]] as const) {
        await p.goto(`${URL_BASE}${ruta}`, { waitUntil: "domcontentloaded" });
        await p.getByRole("heading", { name: titulo, exact: true }).first().waitFor();
        const desborde = (await p.evaluate("document.documentElement.scrollWidth - window.innerWidth")) as number;
        filas.push({ pantalla, ancho, tema, ok: desborde <= 0, desborde });
      }
      await p.goto(`${URL_BASE}/revisiones`, { waitUntil: "domcontentloaded" });
      await p.getByRole("link", { name: "Agrega una caché de nombres" }).click();
      await p.getByText("Publicada · Con problemas").waitFor();
      const desborde = (await p.evaluate("document.documentElement.scrollWidth - window.innerWidth")) as number;
      filas.push({ pantalla: "Detalle", ancho, tema, ok: desborde <= 0, desborde });
      if (CAPTURAS && ancho !== 1440 && tema === "light") await p.screenshot({ path: `${CAPTURAS}/cfg-${id}-${ancho}.png` });
      await c.close();
    }
  }
  return filas;
}

async function sesion(b: Browser) {
  const c = await b.newContext();
  const p = await c.newPage();
  await p.goto(`${URL_BASE}/ingreso`);
  await p.getByLabel("Correo").fill(EMAIL);
  await p.getByLabel("Clave").fill(CLAVE);
  await p.getByRole("button", { name: "Ingresar" }).click();
  await p.getByRole("heading", { name: "Revisiones" }).waitFor();
  const e = await c.storageState();
  await c.close();
  return e;
}

/** axe-core sobre cada pantalla (reglas WCAG 2.0/2.1 A y AA). */
async function accesibilidad(b: Browser, estado: Awaited<ReturnType<typeof sesion>>) {
  const auditar = async (p: Page, pantalla: string) => {
    await p.addScriptTag({ content: AXE });
    const r = (await p.evaluate(`axe.run({ runOnly: { type: "tag", values: ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"] } })`)) as { violations: { id: string; impact: string; help: string; nodes: { target: string[]; failureSummary: string }[] }[]; passes: unknown[] };
    return { pantalla, reglasAprobadas: r.passes.length, violaciones: r.violations.map((v) => ({ id: v.id, impacto: v.impact, ayuda: v.help, nodos: v.nodes.length, ejemplos: v.nodes.slice(0, 3).map((n) => ({ elemento: n.target.join(" "), detalle: n.failureSummary.split("\n").slice(1).join(" ").trim() })) })) };
  };
  const salida = [];
  for (const tema of ["light", "dark"] as const) {
    // bypassCSP: la política del panel (8.4.6) bloquea scripts en línea, también el de axe; solo la auditoría la salta.
    const anon = await (await b.newContext({ colorScheme: tema, bypassCSP: true })).newPage();
    await anon.goto(`${URL_BASE}/ingreso`);
    await anon.getByRole("heading", { name: "Ingresa" }).waitFor();
    salida.push({ tema, ...(await auditar(anon, "Ingreso")) });
    await anon.goto(`${URL_BASE}/registro`);
    await anon.getByRole("button", { name: "Crear cuenta" }).waitFor();
    salida.push({ tema, ...(await auditar(anon, "Registro")) });
    await anon.context().close();
    const p = await (await b.newContext({ colorScheme: tema, storageState: estado, bypassCSP: true })).newPage();
    for (const [pantalla, ruta, titulo] of [["Revisiones", "/revisiones", "Revisiones"], ["Repositorios", "/repositorios", "Repositorios"], ["Usuarios", "/usuarios", "Usuarios"]] as const) {
      await p.goto(`${URL_BASE}${ruta}`, { waitUntil: "domcontentloaded" });
      await p.getByRole("heading", { name: titulo, exact: true }).first().waitFor();
      await p.waitForTimeout(300);
      salida.push({ tema, ...(await auditar(p, pantalla)) });
    }
    await p.goto(`${URL_BASE}/revisiones`, { waitUntil: "domcontentloaded" });
    await p.getByRole("link", { name: "Agrega una caché de nombres" }).click();
    await p.getByText("Publicada · Con problemas").waitFor();
    salida.push({ tema, ...(await auditar(p, "Detalle de revisión")) });
    await p.getByRole("link", { name: "Repositorios" }).click();
    await p.getByRole("button", { name: "Webhook de demo/centinela-demo" }).click();
    await p.getByRole("dialog").waitFor();
    salida.push({ tema, ...(await auditar(p, "Diálogo del webhook")) });
    await p.context().close();
  }
  return salida;
}

// NAVEGADORES=WebKit corre solo los que coinciden (p. ej., WebKit dentro de la imagen de Playwright, que trae sus bibliotecas).
const FILTRO = process.env["NAVEGADORES"];
const SALIDA = process.env["SALIDA"] ?? "navegadores";
const resultado: Record<string, unknown> = {};
for (const n of NAVEGADORES.filter((x) => FILTRO === undefined || x.nombre.includes(FILTRO))) {
  const id = n.nombre.split(" ")[0]!.toLowerCase().replace(/[^a-z]/g, "");
  let b: Browser;
  try {
    b = await n.tipo.launch({ headless: true, ...n.opciones });
  } catch (e) {
    resultado[n.nombre] = { ejecutado: false, motivo: String(e).split("\n").find((l) => /missing|Host system|error/i.test(l)) ?? String(e).split("\n")[0] };
    console.log(n.nombre, "no se pudo abrir");
    continue;
  }
  const version = b.version();
  const pasos = await recorrido(b, id);
  const estado = await sesion(b);
  const cfg = await configuraciones(b, id, estado);
  const a11y = n.nombre === "Google Chrome" || process.env["AUDITAR"] === "1" ? await accesibilidad(b, estado) : undefined;
  resultado[n.nombre] = { ejecutado: true, version, e2e: pasos, configuraciones: cfg, ...(a11y ? { accesibilidad: a11y } : {}) };
  console.log(`${n.nombre} ${version}: E2E ${pasos.filter((p) => p.ok).length}/${pasos.length}, configuraciones ${cfg.filter((c) => c.ok).length}/${cfg.length}${a11y ? `, violaciones WCAG ${a11y.reduce((s, x) => s + x.violaciones.length, 0)}` : ""}`);
  for (const p of pasos.filter((x) => !x.ok)) console.log("  FALLA", p.caso, p.error);
  for (const c of cfg.filter((x) => !x.ok)) console.log("  DESBORDE", c.pantalla, c.ancho, c.tema, c.desborde);
  for (const x of a11y ?? []) for (const v of x.violaciones) console.log("  WCAG", x.tema, x.pantalla, v.id, v.impacto, v.nodos);
  await b.close();
}
writeFileSync(
  `${RESULTADOS}/${SALIDA}.json`,
  `${JSON.stringify({ escenario: "navegadores", fecha: new Date().toISOString(), entorno: { cpu: cpus()[0]?.model, hilos: cpus().length, memoriaGb: Math.round(totalmem() / 2 ** 30), kernel: release(), node: process.version }, datos: resultado }, null, 2)}\n`,
);
console.log(`→ resultados/${SALIDA}.json`);
