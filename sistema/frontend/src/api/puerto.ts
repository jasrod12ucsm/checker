// El puerto: lo que las pantallas necesitan del servicio, en su idioma. Las pantallas solo conocen esta interfaz;
// la implementación (HTTP) la elige la raíz de composición (`main.tsx`) y las pruebas pasan la suya.
import type { DatosIngreso, DatosNuevoUsuario, DatosRegistro, DatosRepositorio } from "../dominio/formularios";
import type { ErrorApi } from "../dominio/errores";
import type { Clasificacion, Decision, DetalleRevision, Hallazgo, Politica, Repositorio, Revision, Rol, Usuario } from "../dominio/modelo";
import type { Resultado } from "../dominio/resultado";

export type Respuesta<T> = Promise<Resultado<T, ErrorApi>>;

export interface CambioUsuario {
  readonly estado?: Decision;
  readonly rol?: Rol;
}

export interface AjustesRepositorio {
  readonly politica?: Politica;
  readonly bloquearMerge?: boolean;
}

export interface Api {
  estadoRegistro(): Respuesta<{ readonly hayUsuarios: boolean }>;
  registrar(d: DatosRegistro): Respuesta<{ readonly usuario: Usuario; readonly pendienteDeAprobacion: boolean }>;
  ingresar(d: DatosIngreso): Respuesta<Usuario>;
  sesion(): Respuesta<Usuario>;
  salir(): Respuesta<void>;

  usuarios(): Respuesta<readonly Usuario[]>;
  crearUsuario(d: DatosNuevoUsuario): Respuesta<Usuario>;
  actualizarUsuario(id: string, c: CambioUsuario): Respuesta<Usuario>;

  repositorios(): Respuesta<readonly Repositorio[]>;
  conectar(d: DatosRepositorio): Respuesta<Repositorio>;
  configurar(id: string, a: AjustesRepositorio): Respuesta<Repositorio>;
  desconectar(id: string): Respuesta<Repositorio>;

  revisiones(repositorioId?: string): Respuesta<readonly Revision[]>;
  revision(id: string): Respuesta<DetalleRevision>;
  solicitar(repositorioId: string, numeroPr: number): Respuesta<Revision>;
  reintentar(id: string): Respuesta<Revision>;
  clasificar(hallazgoId: string, c: Clasificacion): Respuesta<Hallazgo>;
}
