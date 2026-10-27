import { err, ok, type ErrorValor, type Instante, type Marca, type RepositorioId, type Resultado, type UsuarioId } from "@centinela/kernel";
import type { Autorizado } from "@centinela/identidad";

/** `propietario/nombre` tal como lo escribe GitHub. */
export type NombreRepo = Marca<string, "NombreRepo">;
export function nombreRepo(s: string): Resultado<NombreRepo, ErrorValor> {
  const t = s.trim();
  return /^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})\/[A-Za-z0-9._-]{1,100}$/.test(t)
    ? ok(t as NombreRepo)
    : err({ tipo: "ValorInvalido", campo: "nombre", motivo: "debe ser propietario/nombre" });
}

/**
 * Política del checker para el repositorio (la opción `PolicyMode`):
 * `Silent` solo comenta usos inválidos seguros; `Possibly` también los que
 * dependen de la capacidad o del rehash sin garantía en el código.
 */
export type Politica = "Silent" | "Possibly";

/** Secreto compartido con GitHub para firmar los webhooks. Lo genera el adaptador. */
export type SecretoWebhook = Marca<string, "SecretoWebhook">;

export interface Repositorio {
  readonly id: RepositorioId;
  readonly nombre: NombreRepo;
  readonly politica: Politica;
  /** Si es verdadero, un hallazgo confirmado pone el estado del commit en `failure` y bloquea el merge. */
  readonly bloquearMerge: boolean;
  readonly secretoWebhook: SecretoWebhook;
  readonly activo: boolean;
  readonly conectadoPor: UsuarioId;
  readonly conectadoEn: Instante;
}

export type ErrorRepositorios =
  | ErrorValor
  | { readonly tipo: "RepositorioYaConectado" }
  | { readonly tipo: "RepositorioNoEncontrado" }
  | { readonly tipo: "RepositorioDesconectado" };

export interface DatosConexion {
  readonly id: RepositorioId;
  readonly nombre: NombreRepo;
  readonly politica: Politica;
  readonly bloquearMerge: boolean;
  readonly secretoWebhook: SecretoWebhook;
}

/** Conectar: un repositorio activo no se conecta dos veces; uno desconectado se reactiva con secreto nuevo. */
export function conectar(
  por: Autorizado<"gestionar-repositorios">,
  existente: Repositorio | undefined,
  datos: DatosConexion,
  ahora: Instante,
): Resultado<Repositorio, ErrorRepositorios> {
  if (existente?.activo) return err({ tipo: "RepositorioYaConectado" });
  const base = { ...datos, activo: true, conectadoPor: por.usuarioId, conectadoEn: ahora };
  return ok(existente === undefined ? base : { ...base, id: existente.id });
}

export interface Ajustes {
  readonly politica?: Politica;
  readonly bloquearMerge?: boolean;
}

export function configurar(_por: Autorizado<"gestionar-repositorios">, repo: Repositorio, ajustes: Ajustes): Resultado<Repositorio, ErrorRepositorios> {
  if (!repo.activo) return err({ tipo: "RepositorioDesconectado" });
  return ok({ ...repo, ...ajustes });
}

/** Desconectar no borra las revisiones: deja de aceptar webhooks y de revisar. */
export function desconectar(_por: Autorizado<"gestionar-repositorios">, repo: Repositorio): Repositorio {
  return { ...repo, activo: false };
}
