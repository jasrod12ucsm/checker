import type { Email, Instante, Positivo, RepositorioId, RevisionId, UsuarioId, HallazgoId } from "@centinela/kernel";
import type { HashClave, HashToken, Sesion, Usuario } from "@centinela/identidad";
import type { NombreRepo, Politica, Repositorio, SecretoWebhook } from "@centinela/repositorios";
import type { Analisis, EstadoCommit, Hallazgo, Huella, PullRequest, Revision } from "@centinela/revisiones";

// Almacenamiento: un puerto por lo que cada caso de uso necesita, sin repositorio genérico.
// Son síncronos porque SQLite lo es; así una transacción es una función normal.

export interface Usuarios {
  porId(id: UsuarioId): Usuario | undefined;
  porEmail(email: Email): Usuario | undefined;
  contar(): number;
  listar(): readonly Usuario[];
  guardar(u: Usuario): void;
}

export interface Sesiones {
  porHash(h: HashToken): Sesion | undefined;
  guardar(s: Sesion): void;
  borrar(h: HashToken): void;
  borrarDeUsuario(id: UsuarioId): void;
}

export interface Repositorios {
  porId(id: RepositorioId): Repositorio | undefined;
  porNombre(n: NombreRepo): Repositorio | undefined;
  listar(): readonly Repositorio[];
  guardar(r: Repositorio): void;
}

export interface FiltroRevisiones {
  readonly repositorioId?: RepositorioId;
  readonly limite: number;
}

export interface Revisiones {
  porId(id: RevisionId): Revision | undefined;
  delSha(repo: RepositorioId, numero: Positivo, sha: string): Revision | undefined;
  listar(f: FiltroRevisiones): readonly Revision[];
  enAnalisis(): readonly Revision[];
  guardar(r: Revision): void;
}

export interface Hallazgos {
  porId(id: HallazgoId): Hallazgo | undefined;
  deRevision(id: RevisionId): readonly Hallazgo[];
  /** Los hallazgos de una revisión se reemplazan enteros al publicarla. */
  reemplazar(id: RevisionId, hs: readonly Hallazgo[]): void;
  guardar(h: Hallazgo): void;
}

/** Huellas marcadas como falso positivo en cada repositorio. */
export interface Descartes {
  deRepositorio(id: RepositorioId): ReadonlySet<Huella>;
  agregar(id: RepositorioId, h: Huella, por: UsuarioId, en: Instante): void;
  quitar(id: RepositorioId, h: Huella): void;
}

/** Cola de trabajos en la misma base: encolar va en la misma transacción que la revisión (outbox). */
export interface Trabajos {
  encolar(id: RevisionId, en: Instante): void;
  tomar(): RevisionId | undefined;
  terminar(id: RevisionId): void;
}

export interface Almacen {
  readonly usuarios: Usuarios;
  readonly sesiones: Sesiones;
  readonly repositorios: Repositorios;
  readonly revisiones: Revisiones;
  readonly hallazgos: Hallazgos;
  readonly descartes: Descartes;
  readonly trabajos: Trabajos;
  transaccion<T>(f: () => T): T;
}

// Efectos externos.

export interface Claves {
  hashear(clave: string): Promise<HashClave>;
  verificar(clave: string, hash: HashClave): Promise<boolean>;
}

export interface Secretos {
  /** Token de sesión nuevo: el token va a la cookie, el hash a la base. */
  token(): { readonly token: string; readonly hash: HashToken };
  hashDeToken(token: string): HashToken;
  secretoWebhook(): SecretoWebhook;
  /** Firma `X-Hub-Signature-256` de GitHub sobre el cuerpo crudo. */
  firmaValida(secreto: SecretoWebhook, cuerpo: string, firma: string | undefined): boolean;
}

export interface ArchivoCambiado {
  readonly ruta: string;
  readonly eliminado: boolean;
  /** Líneas del lado nuevo que aparecen en el diff: solo en ellas GitHub acepta comentarios. */
  readonly lineas: ReadonlySet<number>;
}

export interface ComentarioEnLinea {
  readonly ruta: string;
  readonly linea: number;
  readonly cuerpo: string;
}

export interface GitHub {
  pullRequest(repo: NombreRepo, numero: Positivo): Promise<PullRequest>;
  archivosCambiados(repo: NombreRepo, numero: Positivo): Promise<readonly ArchivoCambiado[]>;
  publicarRevision(repo: NombreRepo, numero: Positivo, sha: string, cuerpo: string, comentarios: readonly ComentarioEnLinea[]): Promise<void>;
  publicarEstado(repo: NombreRepo, sha: string, estado: EstadoCommit, enlace: string): Promise<void>;
}

/** El código fuente del commit en un directorio temporal. */
export interface Fuentes {
  obtener(repo: NombreRepo, sha: string): Promise<{ readonly dir: string; liberar(): Promise<void> }>;
}

export interface Analizador {
  analizar(dir: string, archivos: readonly string[], politica: Politica): Promise<Analisis>;
}

export interface Bitacora {
  info(msg: string, datos?: Record<string, unknown>): void;
  error(msg: string, datos?: Record<string, unknown>): void;
}
