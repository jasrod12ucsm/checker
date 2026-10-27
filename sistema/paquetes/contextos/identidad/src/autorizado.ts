import { err, ok, type Resultado, type UsuarioId } from "@centinela/kernel";
import type { ErrorIdentidad } from "./errores";
import { exigirActivo, puede, type Permiso, type Usuario } from "./usuario";

/**
 * Testigo de autorización: tener un `Autorizado<"gestionar-usuarios">` prueba que
 * alguien activo con ese permiso pidió la operación. El constructor es privado y el
 * campo `#permiso` lo hace nominal: la única forma de obtenerlo es `Autorizado.para`.
 */
export class Autorizado<P extends Permiso> {
  readonly #permiso: P;
  private constructor(
    readonly usuarioId: UsuarioId,
    permiso: P,
  ) {
    this.#permiso = permiso;
  }

  get permiso(): P {
    return this.#permiso;
  }

  static para<P extends Permiso>(usuario: Usuario, permiso: P): Resultado<Autorizado<P>, ErrorIdentidad> {
    const activo = exigirActivo(usuario);
    if (!activo.ok) return activo;
    if (!puede(usuario.rol, permiso)) return err({ tipo: "SinPermiso", permiso });
    return ok(new Autorizado(usuario.id, permiso));
  }
}
