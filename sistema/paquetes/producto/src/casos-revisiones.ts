import { err, hallazgoId, ok, positivo, revisionId, type HallazgoId, type RepositorioId, type RevisionId, type UsuarioId } from "@centinela/kernel";
import type { Usuario } from "@centinela/identidad";
import { nombreRepo, type Repositorio } from "@centinela/repositorios";
import {
  clasificar,
  comentario,
  cuerpo,
  esEnAnalisis,
  esPendiente,
  estadoCommit,
  fallar,
  iniciar,
  publicar,
  reintentar,
  solicitar,
  suprimido,
  type Analisis,
  type Clasificacion,
  type EnAnalisis,
  type Hallazgo,
  type PullRequest,
  type Revision,
} from "@centinela/revisiones";
import { autorizar, encontrado, enlaceRevision, type Dependencias, type R } from "./contexto";

const ACCIONES_QUE_REVISAN = new Set(["opened", "synchronize", "reopened"]);
export const esCpp = (ruta: string) => /\.(cpp|cc|cxx|c\+\+)$/i.test(ruta);

/** Lo que el adaptador HTTP extrae de un webhook de GitHub, ya validado con su esquema. */
export interface Webhook {
  readonly evento: string;
  readonly repositorio: string;
  readonly cuerpo: string;
  readonly firma: string | undefined;
  readonly pullRequest?: { readonly accion: string; readonly numero: number; readonly titulo: string; readonly autor: string; readonly shaCabeza: string };
}

export type ResultadoWebhook = { readonly tipo: "Encolada"; readonly revisionId: RevisionId } | { readonly tipo: "Ignorado"; readonly motivo: string };

export interface DetalleRevision {
  readonly revision: Revision;
  readonly repositorio: Repositorio;
  readonly hallazgos: readonly Hallazgo[];
  /** Nombre de cada persona que clasificó alguno de los hallazgos, para mostrar «Marcado por …». */
  readonly clasificadores: ReadonlyMap<UsuarioId, string>;
}

export function casosRevisiones(d: Dependencias) {
  const { almacen: a } = d;

  /** Efecto de mejor esfuerzo: si GitHub no responde, la revisión sigue su curso y queda en la bitácora. */
  async function estadoEnGitHub(repo: Repositorio, r: Revision) {
    try {
      await d.github.publicarEstado(repo.nombre, r.pr.shaCabeza, estadoCommit(repo, r), enlaceRevision(d, r.id));
    } catch (e) {
      d.bitacora.error("no se pudo publicar el estado del commit", { revision: r.id, error: String(e) });
    }
  }

  function encolar(repo: Repositorio, pr: PullRequest, origen: "webhook" | "manual", actor: Usuario | null) {
    const id = revisionId(d.ids.nuevo());
    if (!id.ok) return id;
    return a.transaccion(() => {
      const r = solicitar(repo, a.revisiones.delSha(repo.id, pr.numero, pr.shaCabeza), { id: id.valor, pr, origen, solicitadaPor: actor?.id ?? null }, d.reloj.ahora());
      if (!r.ok) return r;
      a.revisiones.guardar(r.valor);
      a.trabajos.encolar(r.valor.id, d.reloj.ahora());
      return r;
    });
  }

  async function analizarYPublicar(repo: Repositorio, r: Revision<EnAnalisis>) {
    const cambiados = (await d.github.archivosCambiados(repo.nombre, r.pr.numero)).filter((f) => !f.eliminado && esCpp(f.ruta));
    let analisis: Analisis = { analizados: 0, noCompilados: [], avisos: [] };
    if (cambiados.length > 0) {
      const fuente = await d.fuentes.obtener(repo.nombre, r.pr.shaCabeza);
      try {
        analisis = await d.analizador.analizar(fuente.dir, cambiados.map((f) => f.ruta), repo.politica);
      } finally {
        await fuente.liberar();
      }
    }
    const nuevoId = (): HallazgoId => {
      const h = hallazgoId(d.ids.nuevo());
      if (!h.ok) throw new Error("el generador de ids no dio un UUID");
      return h.valor;
    };
    const pub = publicar(r, analisis, a.descartes.deRepositorio(repo.id), nuevoId, d.reloj.ahora());
    const visibles = pub.hallazgos.filter((h) => !suprimido(h));
    if (visibles.length > 0) {
      const lineas = new Map(cambiados.map((f) => [f.ruta, f.lineas]));
      const enDiff = visibles.filter((h) => lineas.get(h.archivo)?.has(h.linea));
      const fuera = visibles.filter((h) => !enDiff.includes(h));
      await d.github.publicarRevision(
        repo.nombre,
        r.pr.numero,
        r.pr.shaCabeza,
        cuerpo(pub.revision, fuera, enlaceRevision(d, r.id)),
        enDiff.map((h) => ({ ruta: h.archivo, linea: h.linea, cuerpo: comentario(h) })),
      );
    }
    return pub;
  }

  return {
    /** RF-S03: GitHub avisa que se abrió o actualizó un PR; si la firma es válida, se encola su revisión. */
    async recibirWebhook(w: Webhook): R<ResultadoWebhook> {
      const nombre = nombreRepo(w.repositorio);
      const repo = nombre.ok ? a.repositorios.porNombre(nombre.valor) : undefined;
      if (repo === undefined) return err({ tipo: "RepositorioNoEncontrado" });
      if (!d.secretos.firmaValida(repo.secretoWebhook, w.cuerpo, w.firma)) return err({ tipo: "FirmaInvalida" });
      if (w.evento === "ping") return ok({ tipo: "Ignorado", motivo: "ping" });
      if (w.evento !== "pull_request" || w.pullRequest === undefined) return ok({ tipo: "Ignorado", motivo: `evento ${w.evento}` });
      if (!ACCIONES_QUE_REVISAN.has(w.pullRequest.accion)) return ok({ tipo: "Ignorado", motivo: `acción ${w.pullRequest.accion}` });
      const numero = positivo("numero", w.pullRequest.numero);
      if (!numero.ok) return numero;
      const { titulo, autor, shaCabeza } = w.pullRequest;
      const r = encolar(repo, { numero: numero.valor, titulo, autor, shaCabeza }, "webhook", null);
      if (!r.ok) {
        const t = r.error.tipo;
        if (t === "RevisionEnCurso" || t === "ShaYaRevisado" || t === "RepositorioDesconectado") return ok({ tipo: "Ignorado", motivo: t });
        return r;
      }
      await estadoEnGitHub(repo, r.valor);
      return ok({ tipo: "Encolada", revisionId: r.valor.id });
    },

    /** RF-S03: un usuario pide revisar ahora un PR (sin esperar el webhook). */
    async solicitarRevision(actor: Usuario, repoId: RepositorioId, numeroPr: number): R<Revision> {
      const por = autorizar(actor, "solicitar-revision");
      if (!por.ok) return por;
      const repo = encontrado(a.repositorios.porId(repoId), { tipo: "RepositorioNoEncontrado" });
      if (!repo.ok) return repo;
      const numero = positivo("numeroPr", numeroPr);
      if (!numero.ok) return numero;
      let pr: PullRequest;
      try {
        pr = await d.github.pullRequest(repo.valor.nombre, numero.valor);
      } catch (e) {
        return err({ tipo: "ErrorGitHub", detalle: String(e) });
      }
      const r = encolar(repo.valor, pr, "manual", actor);
      if (r.ok) await estadoEnGitHub(repo.valor, r.valor);
      return r;
    },

    async reintentar(actor: Usuario, id: RevisionId): R<Revision> {
      const por = autorizar(actor, "solicitar-revision");
      if (!por.ok) return por;
      const r = a.transaccion(() => {
        const rev = encontrado(a.revisiones.porId(id), { tipo: "RevisionNoEncontrada" });
        if (!rev.ok) return rev;
        const p = reintentar(por.valor, rev.valor, d.reloj.ahora());
        if (!p.ok) return p;
        a.revisiones.guardar(p.valor);
        a.trabajos.encolar(id, d.reloj.ahora());
        return p;
      });
      if (r.ok) {
        const repo = a.repositorios.porId(r.valor.repositorioId);
        if (repo) await estadoEnGitHub(repo, r.valor);
      }
      return r;
    },

    /**
     * El trabajador: toma una revisión de la cola, la analiza y publica el resultado.
     * Devuelve `false` si la cola estaba vacía.
     */
    async procesarSiguiente(): Promise<boolean> {
      const id = a.trabajos.tomar();
      if (id === undefined) return false;
      const pendiente = a.revisiones.porId(id);
      const repo = pendiente && a.repositorios.porId(pendiente.repositorioId);
      if (pendiente === undefined || repo === undefined || !esPendiente(pendiente)) {
        a.trabajos.terminar(id);
        return true;
      }
      const enCurso = iniciar(pendiente, d.reloj.ahora());
      a.revisiones.guardar(enCurso);
      await estadoEnGitHub(repo, enCurso);
      let final: Revision;
      try {
        const pub = await analizarYPublicar(repo, enCurso);
        a.transaccion(() => {
          a.revisiones.guardar(pub.revision);
          a.hallazgos.reemplazar(id, pub.hallazgos);
          a.trabajos.terminar(id);
        });
        final = pub.revision;
        d.bitacora.info("revisión publicada", { revision: id, ...pub.revision.estado.resumen });
      } catch (e) {
        final = fallar(enCurso, String(e instanceof Error ? e.message : e).slice(0, 500), d.reloj.ahora());
        a.transaccion(() => {
          a.revisiones.guardar(final);
          a.trabajos.terminar(id);
        });
        d.bitacora.error("revisión fallida", { revision: id, error: String(e) });
      }
      await estadoEnGitHub(repo, final);
      return true;
    },

    /** Al arrancar: lo que quedó en análisis cuando el proceso se cayó se marca como fallido. */
    recuperarInterrumpidas(): number {
      const colgadas = a.revisiones.enAnalisis().filter(esEnAnalisis);
      a.transaccion(() => {
        for (const r of colgadas) {
          a.revisiones.guardar(fallar(r, "el análisis se interrumpió", d.reloj.ahora()));
          a.trabajos.terminar(r.id);
        }
      });
      return colgadas.length;
    },

    /** RF-S04 */
    async listar(actor: Usuario, repositorioId?: RepositorioId): R<readonly Revision[]> {
      const por = autorizar(actor, "consultar-revisiones");
      if (!por.ok) return por;
      return ok(a.revisiones.listar(repositorioId === undefined ? { limite: 200 } : { repositorioId, limite: 200 }));
    },

    async detalle(actor: Usuario, id: RevisionId): R<DetalleRevision> {
      const por = autorizar(actor, "consultar-revisiones");
      if (!por.ok) return por;
      const r = encontrado(a.revisiones.porId(id), { tipo: "RevisionNoEncontrada" });
      if (!r.ok) return r;
      const repo = encontrado(a.repositorios.porId(r.valor.repositorioId), { tipo: "RepositorioNoEncontrado" });
      if (!repo.ok) return repo;
      const hallazgos = a.hallazgos.deRevision(id);
      const clasificadores = new Map<UsuarioId, string>();
      for (const h of hallazgos) {
        const quien = h.clasificadoPor === null ? undefined : a.usuarios.porId(h.clasificadoPor.por);
        if (quien) clasificadores.set(quien.id, quien.nombre);
      }
      return ok({ revision: r.valor, repositorio: repo.valor, hallazgos, clasificadores });
    },

    /** RF-S05: marcar un hallazgo; un falso positivo deja de reportarse en ese repositorio. */
    async clasificar(actor: Usuario, id: HallazgoId, nueva: Clasificacion): R<Hallazgo> {
      const por = autorizar(actor, "clasificar-hallazgos");
      if (!por.ok) return por;
      return a.transaccion(() => {
        const h = encontrado(a.hallazgos.porId(id), { tipo: "HallazgoNoEncontrado" });
        if (!h.ok) return h;
        const rev = a.revisiones.porId(h.valor.revisionId)!;
        const c = clasificar(por.valor, h.valor, nueva, d.reloj.ahora());
        a.hallazgos.guardar(c.hallazgo);
        if (c.descarte === "agregar") a.descartes.agregar(rev.repositorioId, c.hallazgo.huella, actor.id, d.reloj.ahora());
        if (c.descarte === "quitar") a.descartes.quitar(rev.repositorioId, c.hallazgo.huella);
        return ok<Hallazgo>(c.hallazgo);
      });
    },
  };
}


