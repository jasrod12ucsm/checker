// Gráficos del capítulo 8 a partir de resultados/*.json (nada se copia a mano).
//   npx tsx no-funcionales/graficos.ts ../libro/capturas
// Dibuja cada gráfico como SVG y lo convierte a PNG con Chrome (Playwright).
import { readFileSync } from "node:fs";
import { chromium } from "playwright-core";

const SALIDA = process.argv[2] ?? ".";
const leer = (n: string) => JSON.parse(readFileSync(new URL(`./resultados/${n}.json`, import.meta.url), "utf8")).datos;
const AZUL = "#2a78d6", NARANJA = "#eb6834", TINTA = "#0b0b0b", SECUNDARIA = "#52514e", TENUE = "#898781", REJILLA = "#e1e0d9", FONDO = "#fcfcfb";
const fmt = (n: number) => n.toLocaleString("es-ES", { maximumFractionDigits: 1 });
/** Un tope «redondo» y cuatro divisiones iguales (1, 2, 2,5 o 5 por potencia de diez). */
function escala(maximo: number): { max: number; marcas: number[] } {
  const crudo = (maximo * 1.1) / 4 || 1;
  const p = 10 ** Math.floor(Math.log10(crudo));
  const paso = [1, 2, 2.5, 5, 10].map((k) => k * p).find((x) => x >= crudo)!;
  return { max: paso * 4, marcas: [0, 1, 2, 3, 4].map((i) => i * paso) };
}

interface Panel { titulo: string; unidad: string; x: string[]; y: number[]; }

/** Paneles pequeños con la misma x (un solo eje y por panel: nunca dos escalas en un gráfico). */
function lineas(titulo: string, ejeX: string, paneles: Panel[]): string {
  const W = 340, H = 230, M = { i: 52, d: 16, a: 34, b: 44 };
  const cuerpo = paneles.map((p, k) => {
    const { max, marcas } = escala(Math.max(...p.y));
    const px = (i: number) => M.i + (i * (W - M.i - M.d)) / (p.x.length - 1);
    const py = (v: number) => H - M.b - (v / max) * (H - M.a - M.b);
    return `<g transform="translate(${k * W},0)">
      <text x="${M.i}" y="20" font-size="13" font-weight="600" fill="${TINTA}">${p.titulo}</text>
      ${marcas.map((m) => `<line x1="${M.i}" x2="${W - M.d}" y1="${py(m)}" y2="${py(m)}" stroke="${REJILLA}"/><text x="${M.i - 6}" y="${py(m) + 4}" font-size="10" fill="${TENUE}" text-anchor="end">${fmt(m)}</text>`).join("")}
      ${p.x.map((x, i) => `<text x="${px(i)}" y="${H - M.b + 16}" font-size="10" fill="${TENUE}" text-anchor="middle">${x}</text>`).join("")}
      <text x="${(M.i + W - M.d) / 2}" y="${H - 8}" font-size="10" fill="${SECUNDARIA}" text-anchor="middle">${ejeX}</text>
      <text x="12" y="${(M.a + H - M.b) / 2}" font-size="10" fill="${SECUNDARIA}" text-anchor="middle" transform="rotate(-90 12 ${(M.a + H - M.b) / 2})">${p.unidad}</text>
      <polyline fill="none" stroke="${AZUL}" stroke-width="2" points="${p.y.map((v, i) => `${px(i)},${py(v)}`).join(" ")}"/>
      ${p.y.map((v, i) => `<circle cx="${px(i)}" cy="${py(v)}" r="4" fill="${AZUL}" stroke="${FONDO}" stroke-width="2"/>`).join("")}
      ${[0, p.y.length - 1].map((i) => `<text x="${px(i)}" y="${py(p.y[i]!) - 9}" font-size="10" fill="${TINTA}" text-anchor="middle">${fmt(p.y[i]!)}</text>`).join("")}
    </g>`;
  });
  return svg(paneles.length * W, H, titulo, cuerpo.join(""));
}

/** Barras agrupadas: una serie por color, con su valor escrito sobre cada barra y leyenda arriba. */
function barras(titulo: string, unidad: string, grupos: string[], series: { nombre: string; color: string; y: number[] }[]): string {
  const W = 720, H = 300, M = { i: 60, d: 20, a: 56, b: 40 };
  const { max, marcas } = escala(Math.max(...series.flatMap((s) => s.y)));
  const ancho = (W - M.i - M.d) / grupos.length;
  const bw = Math.min(56, (ancho * 0.6) / series.length);
  const py = (v: number) => H - M.b - (v / max) * (H - M.a - M.b);
  const cuerpo = `
    ${marcas.map((m) => `<line x1="${M.i}" x2="${W - M.d}" y1="${py(m)}" y2="${py(m)}" stroke="${REJILLA}"/><text x="${M.i - 6}" y="${py(m) + 4}" font-size="10" fill="${TENUE}" text-anchor="end">${fmt(m)}</text>`).join("")}
    <text x="14" y="${(M.a + H - M.b) / 2}" font-size="10" fill="${SECUNDARIA}" text-anchor="middle" transform="rotate(-90 14 ${(M.a + H - M.b) / 2})">${unidad}</text>
    ${series.length < 2 ? "" : series.map((s, k) => `<rect x="${M.i + k * 150}" y="30" width="12" height="12" rx="2" fill="${s.color}"/><text x="${M.i + 18 + k * 150}" y="40" font-size="11" fill="${SECUNDARIA}">${s.nombre}</text>`).join("")}
    ${grupos.map((g, i) => {
      const x0 = M.i + i * ancho + (ancho - bw * series.length - 2 * (series.length - 1)) / 2;
      return series.map((s, k) => {
        const x = x0 + k * (bw + 2), v = s.y[i]!, y = py(v);
        return `<path d="M${x},${H - M.b} V${y + 4} q0,-4 4,-4 h${bw - 8} q4,0 4,4 V${H - M.b} Z" fill="${s.color}"/><text x="${x + bw / 2}" y="${y - 5}" font-size="10" fill="${TINTA}" text-anchor="middle">${fmt(v)}</text>`;
      }).join("") + `<text x="${M.i + i * ancho + ancho / 2}" y="${H - M.b + 16}" font-size="11" fill="${SECUNDARIA}" text-anchor="middle">${g}</text>`;
    }).join("")}`;
  return svg(W, H, titulo, cuerpo);
}

const svg = (w: number, h: number, titulo: string, cuerpo: string) =>
  `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h + 26}" font-family="DejaVu Sans, sans-serif"><rect width="100%" height="100%" fill="${FONDO}"/><text x="12" y="18" font-size="14" font-weight="700" fill="${TINTA}">${titulo}</text><g transform="translate(0,26)">${cuerpo}</g></svg>`;

const estres = leer("estres");
const esc = estres.lectura.escalones as Record<string, { solicitudesPorS: number; latenciaMs: { p99: number }; total: number; timeouts: number }>;
const conex = Object.keys(esc);
const volumen = leer("volumen"), antes = leer("volumen-antes-indice");
const config = leer("configuracion");

const graficos: [string, string][] = [
  ["g-estres", lineas("Estrés: GET /api/revisiones (200 de 1 000) con más conexiones simultáneas", "conexiones simultáneas", [
    { titulo: "Rendimiento", unidad: "solicitudes por segundo", x: conex, y: conex.map((c) => esc[c]!.solicitudesPorS) },
    { titulo: "Latencia p99", unidad: "milisegundos", x: conex, y: conex.map((c) => esc[c]!.latenciaMs.p99) },
    { titulo: "Sin respuesta en 10 s", unidad: "% de solicitudes", x: conex, y: conex.map((c) => Math.round((esc[c]!.timeouts / (esc[c]!.total + esc[c]!.timeouts)) * 1000) / 10) },
  ])],
  ["g-volumen", barras("Volumen: la lista de revisiones antes y después del índice por fecha", "solicitudes por segundo", ["1 000 revisiones", "20 000 revisiones"], [
    { nombre: "sin índice (v2)", color: NARANJA, y: [1, 2].map((i) => antes.base[i].lista.solicitudesPorS) },
    { nombre: "con índice (v3)", color: AZUL, y: [1, 2].map((i) => volumen.base[i].lista.solicitudesPorS) },
  ])],
  ["g-paralelo", barras("Configuración: un PR de 16 archivos según CENTINELA_PARALELO", "segundos hasta publicar", config.paralelo.map((p: { paralelo: number }) => `${p.paralelo} ${p.paralelo === 1 ? "proceso" : "procesos"}`), [
    { nombre: "tiempo de la revisión", color: AZUL, y: config.paralelo.map((p: { segundos: number }) => p.segundos) },
  ])],
];

const b = await chromium.launch({ executablePath: "/usr/bin/google-chrome", headless: true });
const p = await b.newPage({ deviceScaleFactor: 2 });
for (const [nombre, contenido] of graficos) {
  await p.setContent(`<body style="margin:0">${contenido}</body>`);
  await p.locator("svg").screenshot({ path: `${SALIDA}/${nombre}.png` });
  console.log("gráfico", nombre);
}
await b.close();
