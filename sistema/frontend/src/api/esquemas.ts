// La frontera de entrada del panel: cada respuesta del servicio se valida aquí antes de llegar a una pantalla
// (el `TryFrom` de las guías). Si el contrato cambia sin avisar, falla aquí con un error claro, no en un render.
import { z } from "zod";
import type { DetalleRevision, Hallazgo, Repositorio, Revision, Usuario } from "../dominio/modelo";

const fechaIso = z.iso.datetime({ offset: true });
const rol = z.enum(["administrador", "desarrollador"]);

export const UsuarioDto = z.object({
  id: z.string(),
  email: z.string(),
  nombre: z.string(),
  rol,
  estado: z.enum(["Pendiente", "Activo", "Desactivado"]),
  creadoEn: fechaIso,
}) satisfies z.ZodType<Usuario>;

export const EstadoRegistroDto = z.object({ hayUsuarios: z.boolean() });
export const RegistroDto = z.object({ usuario: UsuarioDto, pendienteDeAprobacion: z.boolean() });

export const RepositorioDto = z.object({
  id: z.string(),
  nombre: z.string(),
  politica: z.enum(["Silent", "Possibly"]),
  bloquearMerge: z.boolean(),
  activo: z.boolean(),
  conectadoEn: fechaIso,
  webhook: z.object({ url: z.string(), secreto: z.string(), tipoContenido: z.string(), eventos: z.array(z.string()) }).nullable(),
}) satisfies z.ZodType<Repositorio>;

const resumen = z.object({
  archivosAnalizados: z.number().int(),
  noCompilados: z.number().int(),
  confirmados: z.number().int(),
  posibles: z.number().int(),
  suprimidos: z.number().int(),
});

const estado = z.discriminatedUnion("tipo", [
  z.object({ tipo: z.literal("Pendiente"), desde: fechaIso }),
  z.object({ tipo: z.literal("EnAnalisis"), desde: fechaIso }),
  z.object({ tipo: z.literal("Fallida"), desde: fechaIso, motivo: z.string() }),
  z.object({ tipo: z.literal("Publicada"), desde: fechaIso, veredicto: z.enum(["Aprobada", "ConProblemas"]), resumen }),
]);

export const RevisionDto = z.object({
  id: z.string(),
  repositorio: z.object({ id: z.string(), nombre: z.string() }).nullable(),
  pr: z.object({ numero: z.number().int(), titulo: z.string(), autor: z.string(), shaCabeza: z.string(), enlace: z.string().nullable() }),
  origen: z.enum(["webhook", "manual"]),
  solicitadaPor: z.string().nullable(),
  creadaEn: fechaIso,
  intentos: z.number().int(),
  estado,
}) satisfies z.ZodType<Revision>;

/** En el cable, quién y cuándo viajan en dos campos; aquí se juntan en `autoria`, que existe entera o no existe. */
export const HallazgoDto = z
  .object({
    id: z.string(),
    archivo: z.string(),
    linea: z.number().int(),
    columna: z.number().int(),
    clase: z.enum(["Confirmado", "Posible"]),
    mensaje: z.string(),
    ruta: z.array(z.object({ archivo: z.string(), linea: z.number().int(), mensaje: z.string() })),
    huella: z.string(),
    clasificacion: z.enum(["SinRevisar", "Confirmado", "FalsoPositivo"]),
    clasificadoPor: z.object({ id: z.string(), nombre: z.string().nullable() }).nullable(),
    clasificadoEn: fechaIso.nullable(),
  })
  .refine((h) => (h.clasificadoPor === null) === (h.clasificadoEn === null), "clasificadoPor y clasificadoEn van juntos")
  .transform(({ clasificadoPor, clasificadoEn, ...h }): Hallazgo => ({
    ...h,
    autoria: clasificadoPor !== null && clasificadoEn !== null ? { por: clasificadoPor, en: clasificadoEn } : null,
  }));

export const DetalleDto = RevisionDto.extend({ hallazgos: z.array(HallazgoDto) }) satisfies z.ZodType<DetalleRevision>;

export const ErrorDto = z.object({ error: z.object({ codigo: z.string(), mensaje: z.string() }) });
