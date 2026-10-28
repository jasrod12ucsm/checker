// Reglas de la pantalla de usuarios, puras: qué se puede hacer con cada cuenta y en qué orden se muestran.
import type { Decision, EstadoUsuario, Usuario } from "./modelo";

export const pendientes = (us: readonly Usuario[]): readonly Usuario[] => us.filter((u) => u.estado === "Pendiente");

const ORDEN: Readonly<Record<EstadoUsuario, number>> = { Activo: 0, Desactivado: 1, Pendiente: 2 };

/** Primero tú, después los activos, los desactivados y los pendientes; dentro de cada grupo, por nombre. */
export function ordenarUsuarios(us: readonly Usuario[], yo: string): readonly Usuario[] {
  return [...us].sort((a, b) => Number(b.id === yo) - Number(a.id === yo) || ORDEN[a.estado] - ORDEN[b.estado] || a.nombre.localeCompare(b.nombre, "es"));
}

export function iniciales(nombre: string): string {
  const palabras = nombre.trim().split(/\s+/).filter((p) => p !== "");
  const letras = palabras.length > 1 ? [palabras[0]!, palabras[palabras.length - 1]!] : palabras;
  return letras.map((p) => p[0]!.toLocaleUpperCase("es")).join("") || "?";
}

/**
 * La acción de la fila. Nadie se desactiva ni se cambia el rol a sí mismo (la misma regla que el servicio);
 * un pendiente se decide arriba, en «Pendientes de aprobación».
 */
export type AccionUsuario =
  | { readonly tipo: "Propio" }
  | { readonly tipo: "Decidir" }
  | { readonly tipo: "Cambiar"; readonly hacia: Decision; readonly texto: string };

export function accionPara(u: Usuario, yo: string): AccionUsuario {
  if (u.id === yo) return { tipo: "Propio" };
  if (u.estado === "Pendiente") return { tipo: "Decidir" };
  return u.estado === "Activo" ? { tipo: "Cambiar", hacia: "Desactivado", texto: "Desactivar" } : { tipo: "Cambiar", hacia: "Activo", texto: "Activar" };
}

export const puedeCambiarRol = (u: Usuario, yo: string): boolean => u.id !== yo;

export const reemplazar = (us: readonly Usuario[], u: Usuario): readonly Usuario[] =>
  us.some((x) => x.id === u.id) ? us.map((x) => (x.id === u.id ? u : x)) : [...us, u];
