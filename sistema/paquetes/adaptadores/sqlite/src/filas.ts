// Fila → dominio: toda fila se valida al leerla (el TryFrom de la persistencia).
// Si la base tiene algo que el dominio no admite, es un error de infraestructura, no se disimula.
import { z } from "zod";
import { email, hallazgoId, instante, positivo, repositorioId, revisionId, texto, usuarioId, type ErrorValor, type Instante, type Resultado, type UsuarioId } from "@centinela/kernel";
import type { HashClave, HashToken, Sesion, Usuario } from "@centinela/identidad";
import { nombreRepo, type Repositorio, type SecretoWebhook } from "@centinela/repositorios";
import type { Autoria, EstadoRevision, Hallazgo, Huella, Revision } from "@centinela/revisiones";

export class FilaCorrupta extends Error {
  constructor(tabla: string, detalle: string) {
    super(`fila inválida en ${tabla}: ${detalle}`);
  }
}

const valor = <T>(f: (s: never) => Resultado<T, ErrorValor>) =>
  z.unknown().transform((s, ctx) => {
    const r = f(s as never);
    if (r.ok) return r.valor;
    ctx.addIssue({ code: "custom", message: r.error.motivo });
    return z.NEVER;
  });
const marca = <T>() => z.string().transform((s) => s as T);
const ms = z.number().int().transform(instante);
const bool = z.union([z.literal(0), z.literal(1)]).transform((n) => n === 1);
const pos = (campo: string) => valor((n: number) => positivo(campo, n));

const usuario = z.object({
  id: valor(usuarioId),
  email: valor(email),
  nombre: valor((s: string) => texto("nombre", s, 100)),
  rol: z.enum(["administrador", "desarrollador"]),
  hash_clave: marca<HashClave>(),
  estado: z.enum(["Pendiente", "Activo", "Desactivado"]),
  creado_en: ms,
});

const sesion = z.object({ token_hash: marca<HashToken>(), usuario_id: valor(usuarioId), creada: ms, expira: ms });

const repositorio = z.object({
  id: valor(repositorioId),
  nombre: valor(nombreRepo),
  politica: z.enum(["Silent", "Possibly"]),
  bloquear_merge: bool,
  secreto_webhook: marca<SecretoWebhook>(),
  activo: bool,
  conectado_por: valor(usuarioId),
  conectado_en: ms,
});

const n = z.number().int().nonnegative();
const revision = z.object({
  id: valor(revisionId),
  repositorio_id: valor(repositorioId),
  numero_pr: pos("numero_pr"),
  titulo: z.string(),
  autor: z.string(),
  sha_cabeza: z.string(),
  origen: z.enum(["webhook", "manual"]),
  solicitada_por: valor(usuarioId).nullable(),
  creada_en: ms,
  intentos: z.number().int().positive(),
  estado: z.enum(["Pendiente", "EnAnalisis", "Publicada", "Fallida"]),
  desde: ms,
  veredicto: z.enum(["Aprobada", "ConProblemas"]).nullable(),
  archivos: n.nullable(),
  no_compilados: n.nullable(),
  confirmados: n.nullable(),
  posibles: n.nullable(),
  suprimidos: n.nullable(),
  motivo: z.string().nullable(),
});

const nota = z.object({ archivo: z.string(), linea: pos("linea"), mensaje: z.string() });
const hallazgo = z.object({
  id: valor(hallazgoId),
  revision_id: valor(revisionId),
  archivo: z.string(),
  linea: pos("linea"),
  columna: pos("columna"),
  clase: z.enum(["Confirmado", "Posible"]),
  mensaje: z.string(),
  ruta: z.string().transform((s, ctx) => {
    const r = z.array(nota).safeParse(JSON.parse(s));
    if (r.success) return r.data;
    ctx.addIssue({ code: "custom", message: "ruta no es una lista de notas" });
    return z.NEVER;
  }),
  huella: marca<Huella>(),
  clasificacion: z.enum(["SinRevisar", "Confirmado", "FalsoPositivo"]),
  clasificado_por: valor(usuarioId).nullable(),
  clasificado_en: ms.nullable(),
});

function leer<S extends z.ZodType>(tabla: string, esquema: S, fila: unknown): z.output<S> {
  const r = esquema.safeParse(fila);
  if (!r.success) throw new FilaCorrupta(tabla, r.error.issues.map((i) => `${i.path.join(".")}: ${i.message}`).join("; "));
  return r.data;
}

export function aUsuario(fila: unknown): Usuario {
  const f = leer("usuarios", usuario, fila);
  return { id: f.id, email: f.email, nombre: f.nombre, rol: f.rol, hashClave: f.hash_clave, estado: f.estado, creadoEn: f.creado_en };
}

export function aSesion(fila: unknown): Sesion {
  const f = leer("sesiones", sesion, fila);
  return { tokenHash: f.token_hash, usuarioId: f.usuario_id, creada: f.creada, expira: f.expira };
}

export function aRepositorio(fila: unknown): Repositorio {
  const f = leer("repositorios", repositorio, fila);
  return {
    id: f.id,
    nombre: f.nombre,
    politica: f.politica,
    bloquearMerge: f.bloquear_merge,
    secretoWebhook: f.secreto_webhook,
    activo: f.activo,
    conectadoPor: f.conectado_por,
    conectadoEn: f.conectado_en,
  };
}

export function aRevision(fila: unknown): Revision {
  const f = leer("revisiones", revision, fila);
  let estado: EstadoRevision;
  switch (f.estado) {
    case "Pendiente":
      estado = { tipo: "Pendiente", encoladaEn: f.desde };
      break;
    case "EnAnalisis":
      estado = { tipo: "EnAnalisis", iniciadaEn: f.desde };
      break;
    case "Fallida":
      if (f.motivo === null) throw new FilaCorrupta("revisiones", "Fallida sin motivo");
      estado = { tipo: "Fallida", terminadaEn: f.desde, motivo: f.motivo };
      break;
    case "Publicada":
      if (f.veredicto === null || f.archivos === null || f.no_compilados === null || f.confirmados === null || f.posibles === null || f.suprimidos === null)
        throw new FilaCorrupta("revisiones", "Publicada sin resumen");
      estado = {
        tipo: "Publicada",
        terminadaEn: f.desde,
        veredicto: f.veredicto,
        resumen: { archivosAnalizados: f.archivos, noCompilados: f.no_compilados, confirmados: f.confirmados, posibles: f.posibles, suprimidos: f.suprimidos },
      };
      break;
  }
  return {
    id: f.id,
    repositorioId: f.repositorio_id,
    pr: { numero: f.numero_pr, titulo: f.titulo, autor: f.autor, shaCabeza: f.sha_cabeza },
    origen: f.origen,
    solicitadaPor: f.solicitada_por,
    creadaEn: f.creada_en,
    intentos: f.intentos,
    estado,
  };
}

export function deRevision(r: Revision) {
  const e = r.estado;
  const base = {
    id: r.id,
    repositorio_id: r.repositorioId,
    numero_pr: r.pr.numero,
    titulo: r.pr.titulo,
    autor: r.pr.autor,
    sha_cabeza: r.pr.shaCabeza,
    origen: r.origen,
    solicitada_por: r.solicitadaPor,
    creada_en: r.creadaEn,
    intentos: r.intentos,
    estado: e.tipo,
    veredicto: null as string | null,
    archivos: null as number | null,
    no_compilados: null as number | null,
    confirmados: null as number | null,
    posibles: null as number | null,
    suprimidos: null as number | null,
    motivo: null as string | null,
  };
  switch (e.tipo) {
    case "Pendiente":
      return { ...base, desde: e.encoladaEn };
    case "EnAnalisis":
      return { ...base, desde: e.iniciadaEn };
    case "Fallida":
      return { ...base, desde: e.terminadaEn, motivo: e.motivo };
    case "Publicada":
      return {
        ...base,
        desde: e.terminadaEn,
        veredicto: e.veredicto,
        archivos: e.resumen.archivosAnalizados,
        no_compilados: e.resumen.noCompilados,
        confirmados: e.resumen.confirmados,
        posibles: e.resumen.posibles,
        suprimidos: e.resumen.suprimidos,
      };
  }
}

export function aHallazgo(fila: unknown): Hallazgo {
  const f = leer("hallazgos", hallazgo, fila);
  return {
    id: f.id,
    revisionId: f.revision_id,
    archivo: f.archivo,
    linea: f.linea,
    columna: f.columna,
    clase: f.clase,
    mensaje: f.mensaje,
    ruta: f.ruta,
    huella: f.huella,
    clasificacion: f.clasificacion,
    clasificadoPor: autoria(f.clasificado_por, f.clasificado_en),
  };
}

function autoria(por: UsuarioId | null, en: Instante | null): Autoria | null {
  if (por === null && en === null) return null;
  if (por === null || en === null) throw new FilaCorrupta("hallazgos", "clasificado_por y clasificado_en van juntos");
  return { por, en };
}
