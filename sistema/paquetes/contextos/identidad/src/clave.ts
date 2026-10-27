import { err, ok, type Marca, type Resultado } from "@centinela/kernel";
import type { ErrorIdentidad } from "./errores";

/** Clave que cumple la política: al menos 10 caracteres, con letras y números. */
export type ClaveNueva = Marca<string, "ClaveNueva">;

export function claveNueva(s: string): Resultado<ClaveNueva, ErrorIdentidad> {
  if (s.length < 10) return err({ tipo: "ClaveDebil", motivo: "debe tener al menos 10 caracteres" });
  if (s.length > 128) return err({ tipo: "ClaveDebil", motivo: "debe tener como máximo 128 caracteres" });
  if (!/[A-Za-z]/.test(s) || !/[0-9]/.test(s)) return err({ tipo: "ClaveDebil", motivo: "debe tener letras y números" });
  return ok(s as ClaveNueva);
}
