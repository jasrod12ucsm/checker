import { despues, err, ok, type Instante, type Marca, type Resultado, type UsuarioId } from "@centinela/kernel";
import type { ErrorIdentidad } from "./errores";
import { exigirActivo, type Usuario } from "./usuario";

/** Hash del token de sesión: la base guarda el hash, el navegador el token. */
export type HashToken = Marca<string, "HashToken">;

export interface Sesion {
  readonly tokenHash: HashToken;
  readonly usuarioId: UsuarioId;
  readonly creada: Instante;
  readonly expira: Instante;
}

export const DURACION_SESION_MS = 8 * 60 * 60 * 1000;

/** Ingreso: solo un usuario existente, con la clave correcta y activo abre sesión. */
export function ingresar(
  usuario: Usuario | undefined,
  claveCorrecta: boolean,
  tokenHash: HashToken,
  ahora: Instante,
): Resultado<Sesion, ErrorIdentidad> {
  if (usuario === undefined || !claveCorrecta) return err({ tipo: "CredencialesInvalidas" });
  const activo = exigirActivo(usuario);
  if (!activo.ok) return activo;
  return ok({ tokenHash, usuarioId: usuario.id, creada: ahora, expira: despues(ahora, DURACION_SESION_MS) });
}

/** Una sesión vale si no expiró y su usuario sigue activo. */
export function validarSesion(
  sesion: Sesion | undefined,
  usuario: Usuario | undefined,
  ahora: Instante,
): Resultado<Usuario, ErrorIdentidad> {
  if (sesion === undefined || usuario === undefined || ahora >= sesion.expira) return err({ tipo: "SesionInvalida" });
  return exigirActivo(usuario);
}
