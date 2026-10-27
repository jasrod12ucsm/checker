import { inalcanzable } from "@centinela/kernel";
import type { ErrorProducto } from "@centinela/producto";

export interface Respuesta {
  readonly estado: number;
  readonly mensaje: string;
}

/** El único lugar del sistema donde un error de dominio se vuelve un código HTTP. */
export function respuestaDe(e: ErrorProducto): Respuesta {
  switch (e.tipo) {
    case "ValorInvalido":
      return { estado: 400, mensaje: `El campo ${e.campo} ${e.motivo}.` };
    case "ClaveDebil":
      return { estado: 400, mensaje: `La clave ${e.motivo}.` };
    case "CredencialesInvalidas":
      return { estado: 401, mensaje: "Correo o clave incorrectos." };
    case "SesionInvalida":
      return { estado: 401, mensaje: "La sesión no es válida o venció. Vuelve a iniciar sesión." };
    case "FirmaInvalida":
      return { estado: 401, mensaje: "La firma del webhook no corresponde al secreto del repositorio." };
    case "UsuarioPendiente":
      return { estado: 403, mensaje: "Tu cuenta espera la aprobación de un administrador." };
    case "UsuarioDesactivado":
      return { estado: 403, mensaje: "Tu cuenta está desactivada: pide a un administrador que la reactive." };
    case "SinPermiso":
      return { estado: 403, mensaje: `No tienes permiso para ${e.permiso.replace("-", " ")}.` };
    case "UsuarioNoEncontrado":
      return { estado: 404, mensaje: "El usuario no existe." };
    case "RepositorioNoEncontrado":
      return { estado: 404, mensaje: "El repositorio no está conectado." };
    case "RevisionNoEncontrada":
      return { estado: 404, mensaje: "La revisión no existe." };
    case "HallazgoNoEncontrado":
      return { estado: 404, mensaje: "El hallazgo no existe." };
    case "EmailEnUso":
      return { estado: 409, mensaje: "Ya hay un usuario con ese correo." };
    case "NoPuedeModificarseASiMismo":
      return { estado: 409, mensaje: "No puedes desactivar ni cambiar el rol de tu propio usuario." };
    case "RepositorioYaConectado":
      return { estado: 409, mensaje: "El repositorio ya está conectado." };
    case "RepositorioDesconectado":
      return { estado: 409, mensaje: "El repositorio está desconectado." };
    case "RevisionEnCurso":
      return { estado: 409, mensaje: "La revisión de ese commit está en curso." };
    case "ShaYaRevisado":
      return { estado: 409, mensaje: "Ese commit ya se revisó; usa «Reintentar» en su revisión." };
    case "TransicionInvalida":
      return { estado: 409, mensaje: `Una revisión ${e.desde} no puede pasar a ${e.hacia}.` };
    case "ErrorGitHub":
      return { estado: 502, mensaje: `GitHub no respondió como se esperaba: ${e.detalle}` };
    default:
      return inalcanzable(e);
  }
}
