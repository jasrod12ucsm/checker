// Dobles de prueba de los puertos del producto: almacén en memoria, GitHub y analizador falsos.
import { instante, type Instante, type RevisionId } from "@centinela/kernel";
import type { HashClave, HashToken, Sesion, Usuario } from "@centinela/identidad";
import type { Repositorio, SecretoWebhook } from "@centinela/repositorios";
import type { Aviso, EstadoCommit, Hallazgo, Huella, PullRequest, Revision } from "@centinela/revisiones";
import type { Almacen, Analizador, ArchivoCambiado, ComentarioEnLinea, Dependencias, GitHub } from "@centinela/producto";

export function almacenEnMemoria(): Almacen {
  const usuarios = new Map<string, Usuario>();
  const sesiones = new Map<string, Sesion>();
  const repos = new Map<string, Repositorio>();
  const revs = new Map<string, Revision>();
  const hs = new Map<string, Hallazgo>();
  const desc = new Map<string, Set<Huella>>();
  const cola: RevisionId[] = [];
  return {
    usuarios: {
      porId: (id) => usuarios.get(id),
      porEmail: (e) => [...usuarios.values()].find((u) => u.email === e),
      contar: () => usuarios.size,
      listar: () => [...usuarios.values()],
      guardar: (u) => void usuarios.set(u.id, u),
    },
    sesiones: {
      porHash: (h) => sesiones.get(h),
      guardar: (s) => void sesiones.set(s.tokenHash, s),
      borrar: (h) => void sesiones.delete(h),
      borrarDeUsuario: (id) => {
        for (const [k, s] of sesiones) if (s.usuarioId === id) sesiones.delete(k);
      },
    },
    repositorios: {
      porId: (id) => repos.get(id),
      porNombre: (n) => [...repos.values()].find((r) => r.nombre === n),
      listar: () => [...repos.values()],
      guardar: (r) => void repos.set(r.id, r),
    },
    revisiones: {
      porId: (id) => revs.get(id),
      delSha: (repo, n, sha) => [...revs.values()].find((r) => r.repositorioId === repo && r.pr.numero === n && r.pr.shaCabeza === sha),
      listar: (f) => [...revs.values()].filter((r) => f.repositorioId === undefined || r.repositorioId === f.repositorioId).reverse().slice(0, f.limite),
      enAnalisis: () => [...revs.values()].filter((r) => r.estado.tipo === "EnAnalisis"),
      guardar: (r) => void revs.set(r.id, r),
    },
    hallazgos: {
      porId: (id) => hs.get(id),
      deRevision: (id) => [...hs.values()].filter((h) => h.revisionId === id),
      reemplazar: (id, nuevos) => {
        for (const [k, h] of hs) if (h.revisionId === id) hs.delete(k);
        for (const h of nuevos) hs.set(h.id, h);
      },
      guardar: (h) => void hs.set(h.id, h),
    },
    descartes: {
      deRepositorio: (id) => desc.get(id) ?? new Set(),
      agregar: (id, h) => void desc.set(id, new Set([...(desc.get(id) ?? []), h])),
      quitar: (id, h) => void desc.get(id)?.delete(h),
    },
    trabajos: {
      encolar: (id) => void cola.push(id),
      tomar: () => cola.shift(),
      terminar: () => {},
    },
    transaccion: (f) => f(),
  };
}

export class GitHubFalso implements GitHub {
  prs = new Map<number, PullRequest>();
  archivos: ArchivoCambiado[] = [];
  revisiones: { numero: number; sha: string; cuerpo: string; comentarios: readonly ComentarioEnLinea[] }[] = [];
  estados: { sha: string; estado: EstadoCommit; enlace: string }[] = [];
  fallarPublicacion = false;
  async pullRequest(_repo: string, numero: number) {
    const pr = this.prs.get(numero);
    if (!pr) throw new Error(`GitHub 404: PR ${numero}`);
    return pr;
  }
  async archivosCambiados() {
    return this.archivos;
  }
  async publicarRevision(_repo: string, numero: number, sha: string, cuerpo: string, comentarios: readonly ComentarioEnLinea[]) {
    if (this.fallarPublicacion) throw new Error("GitHub 422");
    this.revisiones.push({ numero, sha, cuerpo, comentarios });
  }
  async publicarEstado(_repo: string, sha: string, estado: EstadoCommit, enlace: string) {
    this.estados.push({ sha, estado, enlace });
  }
}

export class AnalizadorFalso implements Analizador {
  avisos: Aviso[] = [];
  llamadas: { dir: string; archivos: readonly string[]; politica: string }[] = [];
  error: Error | undefined;
  async analizar(dir: string, archivos: readonly string[], politica: string) {
    this.llamadas.push({ dir, archivos, politica });
    if (this.error) throw this.error;
    return { analizados: archivos.length, noCompilados: [], avisos: this.avisos.filter((a) => archivos.includes(a.archivo)) };
  }
}

export class RelojFalso {
  t: Instante = instante(1_700_000_000_000);
  ahora() {
    return this.t;
  }
  avanzar(ms: number) {
    this.t = instante(this.t + ms);
  }
}

export function idsSecuenciales() {
  let n = 0;
  return { nuevo: () => `00000000-0000-4000-8000-${(++n).toString(16).padStart(12, "0")}` };
}

export function dependencias(almacen: Almacen = almacenEnMemoria()) {
  const github = new GitHubFalso();
  const analizador = new AnalizadorFalso();
  const reloj = new RelojFalso();
  const liberados: string[] = [];
  const bitacora: { nivel: string; msg: string }[] = [];
  const deps: Dependencias = {
    almacen,
    claves: {
      hashear: async (c) => `plano$${c}` as HashClave,
      verificar: async (c, h) => h === `plano$${c}`,
    },
    secretos: {
      token: () => {
        const token = `tok-${Math.random()}`;
        return { token, hash: `h(${token})` as HashToken };
      },
      hashDeToken: (t) => `h(${t})` as HashToken,
      secretoWebhook: () => "secreto" as SecretoWebhook,
      firmaValida: (s, cuerpo, firma) => firma === `${s}:${cuerpo.length}`,
    },
    github,
    fuentes: { obtener: async (_r, sha) => ({ dir: `/tmp/fuente-${sha}`, liberar: async () => void liberados.push(sha) }) },
    analizador,
    reloj,
    ids: idsSecuenciales(),
    bitacora: { info: (msg) => void bitacora.push({ nivel: "info", msg }), error: (msg) => void bitacora.push({ nivel: "error", msg }) },
    urlPublica: "http://centinela.local",
  };
  return { deps, github, analizador, reloj, liberados, bitacora };
}

/** Firma que acepta el doble de `secretos.firmaValida`. */
export const firmaFalsa = (cuerpo: string) => `secreto:${cuerpo.length}`;
