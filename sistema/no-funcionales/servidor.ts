// Centinela real en un proceso aparte, para medirlo desde fuera (práctica 8).
//   node --import tsx no-funcionales/servidor.ts
// Arranca la composición de producción (SQLite en archivo, clang y el checker reales) contra
// el GitHub simulado de github-varios.ts, registra a la primera cuenta, conecta el
// repositorio y, si SEMBRAR=n, llena la base con n revisiones publicadas (volumen).
// Imprime una línea «LISTO {json}» con lo que el medidor necesita.
import { randomBytes, randomUUID } from "node:crypto";
import { componer, leerConfiguracion } from "@centinela/app";
import { abrirAlmacen } from "@centinela/sqlite";
import { huella } from "@centinela/revisiones";
import type { Hallazgo, Revision } from "@centinela/revisiones";
import type { HallazgoId, Instante, Positivo, RepositorioId, RevisionId } from "@centinela/kernel";
import { REPO } from "./github-varios";

const e = process.env;
const BD = e["CENTINELA_BD"]!;
const sistema = componer(leerConfiguracion({ ...e, CENTINELA_GITHUB_TOKEN: "carga", CENTINELA_HOST: "127.0.0.1" }));
await sistema.arrancar();
const s = sistema.servidor;

const email = `carga-${randomBytes(3).toString("hex")}@centinela.local`;
const clave = `${randomBytes(9).toString("base64url")}9a`;
const reg = await s.inject({ method: "POST", url: "/api/registro", payload: { email, nombre: "Medidor", clave } });
const cookie = String(reg.headers["set-cookie"]).split(";")[0]!;
const con = await s.inject({ method: "POST", url: "/api/repositorios", headers: { cookie }, payload: { nombre: REPO, politica: "Possibly", bloquearMerge: true } });
const repo = con.json() as { id: string; webhook: { secreto: string } };

/** Revisiones publicadas sembradas por los puertos del almacén (no por SQL a mano): la base queda como la dejaría el servicio. */
function sembrar(n: number, porRevision: number, grande: number): { ultima: string; grande: string } {
  const a = abrirAlmacen(BD);
  const t0 = Date.now() - n * 60_000;
  const hallazgo = (rev: RevisionId, i: number): Hallazgo => {
    const aviso = { archivo: `src/m${(i % 40) + 1}.cpp`, linea: (20 + i) as Positivo, columna: 5 as Positivo, clase: i % 2 ? "Posible" as const : "Confirmado" as const, mensaje: `Uso del iterador 'it' después de invalidarlo (${i})`, ruta: [{ archivo: `src/m${(i % 40) + 1}.cpp`, linea: (10 + i) as Positivo, mensaje: "Se obtiene el iterador" }] };
    return { ...aviso, id: randomUUID() as HallazgoId, revisionId: rev, huella: huella(aviso), clasificacion: "SinRevisar", clasificadoPor: null };
  };
  const revision = (k: number, hs: number): RevisionId => {
    const id = randomUUID() as RevisionId;
    const r: Revision = {
      id, repositorioId: repo.id as RepositorioId, origen: "webhook", solicitadaPor: null, creadaEn: (t0 + k * 60_000) as Instante, intentos: 1,
      pr: { numero: (100_000 + k) as Positivo, titulo: `PR sembrado ${k}`, autor: "carga", shaCabeza: (0x10000000 + k).toString(16).padStart(40, "f") },
      estado: { tipo: "Publicada", terminadaEn: (t0 + k * 60_000 + 5_000) as Instante, veredicto: hs > 0 ? "ConProblemas" : "Aprobada", resumen: { archivosAnalizados: 3, noCompilados: 0, confirmados: Math.ceil(hs / 2), posibles: Math.floor(hs / 2), suprimidos: 0 } },
    };
    a.revisiones.guardar(r);
    a.hallazgos.reemplazar(id, Array.from({ length: hs }, (_, i) => hallazgo(id, i)));
    return id;
  };
  let ultima = "";
  for (let k = 0; k < n; k += 1000) a.transaccion(() => { for (let j = k; j < Math.min(n, k + 1000); j++) ultima = revision(j, porRevision); });
  const g = grande > 0 ? a.transaccion(() => revision(n, grande)) : "";
  a.cerrar();
  return { ultima, grande: g };
}

const n = Number(e["SEMBRAR"] ?? 0);
const t = Date.now();
const sembradas = n > 0 ? sembrar(n, Number(e["HALLAZGOS_POR_REVISION"] ?? 5), Number(e["HALLAZGOS_GRANDE"] ?? 500)) : { ultima: "", grande: "" };
console.log(`LISTO ${JSON.stringify({ email, clave, cookie, repoId: repo.id, secreto: repo.webhook.secreto, sembradas, sembrarMs: Date.now() - t })}`);

for (const senal of ["SIGINT", "SIGTERM"] as const) process.once(senal, () => void sistema.detener().then(() => process.exit(0)));
