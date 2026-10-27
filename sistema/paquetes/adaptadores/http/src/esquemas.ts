// Lo que entra por HTTP se valida aquí antes de llegar a un caso de uso.
import { z } from "zod";

const uuid = z.uuid();
export const ConId = z.object({ id: uuid });

export const Ingreso = z.object({ email: z.string().max(254), clave: z.string().max(128) });
export const NuevoUsuario = z.object({
  email: z.string().max(254),
  nombre: z.string().max(100),
  clave: z.string().max(128),
  rol: z.enum(["administrador", "desarrollador"]),
});
export const Registro = z.object({ email: z.string().max(254), nombre: z.string().max(100), clave: z.string().max(128) });
export const CambioUsuario = z
  .object({ estado: z.enum(["Activo", "Desactivado"]).optional(), rol: z.enum(["administrador", "desarrollador"]).optional() })
  .strict()
  .refine((c) => c.estado !== undefined || c.rol !== undefined, "indica estado o rol");

const politica = z.enum(["Silent", "Possibly"]);
export const NuevoRepositorio = z.object({ nombre: z.string().max(140), politica, bloquearMerge: z.boolean() });
export const AjustesRepositorio = z.object({ politica: politica.optional(), bloquearMerge: z.boolean().optional() }).strict();

export const FiltroRevisiones = z.object({ repositorio: uuid.optional() });
export const SolicitudRevision = z.object({ repositorioId: uuid, numeroPr: z.number().int() });
export const Clasificar = z.object({ clasificacion: z.enum(["SinRevisar", "Confirmado", "FalsoPositivo"]) });

/** De un webhook de GitHub solo se lee esto; el cuerpo crudo se conserva para verificar la firma. */
export const EventoGitHub = z.object({
  action: z.string().optional(),
  repository: z.object({ full_name: z.string() }),
  pull_request: z
    .object({ number: z.number().int(), title: z.string(), user: z.object({ login: z.string() }), head: z.object({ sha: z.string() }) })
    .optional(),
});
