import { err, ok, type Email, type Instante, type Marca, type Resultado, type Texto, type UsuarioId } from "@centinela/kernel";
import type { ErrorIdentidad } from "./errores";

export type Rol = "administrador" | "desarrollador";

/**
 * Permisos del sistema. Significado: lo que un usuario puede pedir que se haga.
 * El administrador puede todo; el desarrollador, lo del día a día sobre las revisiones.
 */
export type Permiso =
  | "gestionar-usuarios"
  | "gestionar-repositorios"
  | "consultar-revisiones"
  | "solicitar-revision"
  | "clasificar-hallazgos";

const PERMISOS: Readonly<Record<Rol, readonly Permiso[]>> = {
  administrador: [
    "gestionar-usuarios",
    "gestionar-repositorios",
    "consultar-revisiones",
    "solicitar-revision",
    "clasificar-hallazgos",
  ],
  desarrollador: ["consultar-revisiones", "solicitar-revision", "clasificar-hallazgos"],
};

export const puede = (rol: Rol, permiso: Permiso): boolean => PERMISOS[rol].includes(permiso);

/** Hash de una clave. Solo lo produce el adaptador de hashing; el dominio no ve la clave en claro guardada. */
export type HashClave = Marca<string, "HashClave">;

/**
 * Ciclo de vida de una cuenta. `Pendiente`: se registró y espera aprobación (nunca entró).
 * `Activo`: puede ingresar. `Desactivado`: rechazada o dada de baja por un administrador.
 */
export type EstadoUsuario = "Pendiente" | "Activo" | "Desactivado";

/** Lo que un administrador puede decidir sobre una cuenta: nadie vuelve a quedar pendiente. */
export type Decision = Exclude<EstadoUsuario, "Pendiente">;

export interface Usuario {
  readonly id: UsuarioId;
  readonly email: Email;
  readonly nombre: Texto;
  readonly rol: Rol;
  readonly hashClave: HashClave;
  readonly estado: EstadoUsuario;
  readonly creadoEn: Instante;
}

/** Solo una cuenta activa ingresa, mantiene su sesión o recibe un permiso. */
export function exigirActivo(u: Usuario): Resultado<Usuario, ErrorIdentidad> {
  switch (u.estado) {
    case "Activo":
      return ok(u);
    case "Pendiente":
      return err({ tipo: "UsuarioPendiente" });
    case "Desactivado":
      return err({ tipo: "UsuarioDesactivado" });
  }
}
