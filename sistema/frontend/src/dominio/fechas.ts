// Fechas para la pantalla, en hora de Lima por defecto. `ahora` se pasa como argumento: nada de reloj escondido.

const MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"];

interface Partes {
  readonly anio: number;
  readonly mes: number;
  readonly dia: number;
  readonly hora: string;
}

function partes(ms: number, zona: string): Partes {
  const f = new Intl.DateTimeFormat("en-CA", { timeZone: zona, year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", hourCycle: "h23" });
  const p = Object.fromEntries(f.formatToParts(new Date(ms)).map((x) => [x.type, x.value]));
  return { anio: Number(p["year"]), mes: Number(p["month"]), dia: Number(p["day"]), hora: `${p["hour"]}:${p["minute"]}` };
}

const diaDe = (p: Partes) => Date.UTC(p.anio, p.mes - 1, p.dia) / 86_400_000;

/** «24 oct 2026». */
export function fecha(iso: string, zona = "America/Lima"): string {
  const p = partes(Date.parse(iso), zona);
  return `${p.dia} ${MESES[p.mes - 1]} ${p.anio}`;
}

/** «26 oct 2026, 21:41». */
export const fechaHora = (iso: string, zona = "America/Lima"): string => `${fecha(iso, zona)}, ${partes(Date.parse(iso), zona).hora}`;

/** «hoy, 20:12», «ayer, 16:40» o «2 sep 2026». */
export function fechaRelativa(iso: string, ahora: number, zona = "America/Lima"): string {
  const p = partes(Date.parse(iso), zona);
  const dias = diaDe(partes(ahora, zona)) - diaDe(p);
  if (dias === 0) return `hoy, ${p.hora}`;
  if (dias === 1) return `ayer, ${p.hora}`;
  return fecha(iso, zona);
}

/** «hace 2 min», «hace 3 h», «hace un momento»; más de un día, la fecha. */
export function haceCuanto(iso: string, ahora: number, zona = "America/Lima"): string {
  const s = Math.max(0, Math.round((ahora - Date.parse(iso)) / 1000));
  if (s < 60) return "hace un momento";
  if (s < 3600) return `hace ${Math.floor(s / 60)} min`;
  if (s < 86_400) return `hace ${Math.floor(s / 3600)} h`;
  return fecha(iso, zona);
}

/** «hoy», «ayer» o «2 sep 2026»: la columna «Alta». */
export function diaRelativo(iso: string, ahora: number, zona = "America/Lima"): string {
  const dias = diaDe(partes(ahora, zona)) - diaDe(partes(Date.parse(iso), zona));
  return dias === 0 ? "hoy" : dias === 1 ? "ayer" : fecha(iso, zona);
}
