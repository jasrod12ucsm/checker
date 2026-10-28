import type { Rol } from "./modelo";

/** Los permisos del servicio (`contextos/identidad/src/usuario.ts`). El panel oculta lo que el rol no puede; el servicio igual lo rechaza. */
export type Permiso = "gestionar-usuarios" | "gestionar-repositorios" | "consultar-revisiones" | "solicitar-revision" | "clasificar-hallazgos";

const PERMISOS: Readonly<Record<Rol, readonly Permiso[]>> = {
  administrador: ["gestionar-usuarios", "gestionar-repositorios", "consultar-revisiones", "solicitar-revision", "clasificar-hallazgos"],
  desarrollador: ["consultar-revisiones", "solicitar-revision", "clasificar-hallazgos"],
};

export const puede = (rol: Rol, permiso: Permiso): boolean => PERMISOS[rol].includes(permiso);

export const nombreRol = (rol: Rol): string => (rol === "administrador" ? "Administrador" : "Desarrollador");

export interface Seccion {
  readonly ruta: string;
  readonly titulo: string;
  readonly permiso: Permiso;
}

/** El menú lateral: cada sección pide un permiso. Repositorios lo ve todo el equipo; solo el administrador lo cambia. */
export const SECCIONES: readonly Seccion[] = [
  { ruta: "/revisiones", titulo: "Revisiones", permiso: "consultar-revisiones" },
  { ruta: "/repositorios", titulo: "Repositorios", permiso: "consultar-revisiones" },
  { ruta: "/usuarios", titulo: "Usuarios", permiso: "gestionar-usuarios" },
];

export const seccionesDe = (rol: Rol): readonly Seccion[] => SECCIONES.filter((s) => puede(rol, s.permiso));
