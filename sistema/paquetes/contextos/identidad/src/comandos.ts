import { err, ok, type Email, type Instante, type Resultado, type Texto, type UsuarioId } from "@centinela/kernel";
import type { Autorizado } from "./autorizado";
import type { ErrorIdentidad } from "./errores";
import type { Decision, HashClave, Rol, Usuario } from "./usuario";

export interface DatosUsuario {
  readonly id: UsuarioId;
  readonly email: Email;
  readonly nombre: Texto;
  readonly rol: Rol;
  readonly hashClave: HashClave;
}

/**
 * Registro público. Nadie viene predefinido: la primera persona que se registra
 * crea la instancia y queda como administradora activa; las siguientes quedan como
 * desarrolladoras pendientes hasta que un administrador las apruebe o las rechace.
 */
export function registrar(
  cantidadUsuarios: number,
  emailEnUso: boolean,
  datos: Omit<DatosUsuario, "rol">,
  ahora: Instante,
): Resultado<Usuario, ErrorIdentidad> {
  if (emailEnUso) return err({ tipo: "EmailEnUso" });
  const primero = cantidadUsuarios === 0;
  return ok({ ...datos, rol: primero ? "administrador" : "desarrollador", estado: primero ? "Activo" : "Pendiente", creadoEn: ahora });
}

/** Alta de usuario: la pide un administrador y el correo no puede estar en uso. */
export function crearUsuario(
  _por: Autorizado<"gestionar-usuarios">,
  emailEnUso: boolean,
  datos: DatosUsuario,
  ahora: Instante,
): Resultado<Usuario, ErrorIdentidad> {
  if (emailEnUso) return err({ tipo: "EmailEnUso" });
  return ok({ ...datos, estado: "Activo", creadoEn: ahora });
}

/**
 * `estado: "Activo"` aprueba una cuenta pendiente o reactiva una desactivada;
 * `estado: "Desactivado"` rechaza una pendiente o da de baja una activa.
 * `Pendiente` no se puede pedir: el tipo `Decision` lo excluye.
 */
export interface CambioUsuario {
  readonly estado?: Decision;
  readonly rol?: Rol;
}

/**
 * Aprobar, rechazar, activar, desactivar o cambiar el rol. Nadie se modifica a sí mismo:
 * así siempre queda al menos el administrador que hace el cambio.
 */
export function actualizarUsuario(por: Autorizado<"gestionar-usuarios">, objetivo: Usuario, cambio: CambioUsuario): Resultado<Usuario, ErrorIdentidad> {
  if (objetivo.id === por.usuarioId) return err({ tipo: "NoPuedeModificarseASiMismo" });
  return ok({ ...objetivo, ...cambio });
}
