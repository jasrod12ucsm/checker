import { z } from "zod";

const booleano = z.enum(["true", "false", "1", "0"]).transform((s) => s === "true" || s === "1");

/** Toda la configuración viene de variables de entorno `CENTINELA_*`; se valida al arrancar. */
const Esquema = z.object({
  CENTINELA_PUERTO: z.coerce.number().int().min(0).max(65535).default(8080),
  CENTINELA_HOST: z.string().default("0.0.0.0"),
  CENTINELA_BD: z.string().default("datos/centinela.db"),
  CENTINELA_URL_PUBLICA: z.url().default("http://localhost:8080"),
  CENTINELA_COOKIE_SEGURA: booleano.default(false),
  CENTINELA_GITHUB_API: z.url().default("https://api.github.com"),
  CENTINELA_GITHUB_TOKEN: z.string().min(1, "falta el token de GitHub (CENTINELA_GITHUB_TOKEN)"),
  CENTINELA_CLANG: z.string().default("clang++"),
  CENTINELA_PLUGIN: z.string().default("/work/build/plugin/libContainerInvalidation.so"),
  CENTINELA_PARALELO: z.coerce.number().int().min(1).max(64).default(4),
  CENTINELA_TIEMPO_MAXIMO_S: z.coerce.number().int().min(5).default(120),
  CENTINELA_INTERVALO_MS: z.coerce.number().int().min(50).default(1000),
  CENTINELA_FRONTEND: z.string().optional(),
});

export type Configuracion = z.output<typeof Esquema>;

export function leerConfiguracion(entorno: Record<string, string | undefined>): Configuracion {
  const r = Esquema.safeParse(entorno);
  if (!r.success) throw new Error(`configuración inválida:\n${r.error.issues.map((i) => `  ${i.path.join(".")}: ${i.message}`).join("\n")}`);
  return r.data;
}
