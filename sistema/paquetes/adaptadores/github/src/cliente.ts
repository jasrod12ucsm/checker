import { spawn } from "node:child_process";
import { mkdtemp, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { Readable } from "node:stream";
import { pipeline } from "node:stream/promises";
import { z } from "zod";
import { positivo } from "@centinela/kernel";
import type { Fuentes, GitHub } from "@centinela/producto";
import { CONTEXTO_ESTADO } from "@centinela/revisiones";
import { lineasDelParche } from "./parche";

export interface OpcionesGitHub {
  /** `https://api.github.com`, o el servidor falso de las pruebas. */
  readonly api: string;
  readonly token: string;
}

export class ErrorGitHub extends Error {
  constructor(
    readonly estado: number,
    ruta: string,
    detalle: string,
  ) {
    super(`GitHub respondió ${estado} en ${ruta}: ${detalle.slice(0, 300)}`);
  }
}

// Solo los campos que se usan: el resto de la respuesta se ignora.
const PR = z.object({ number: z.number(), title: z.string(), user: z.object({ login: z.string() }), head: z.object({ sha: z.string() }) });
const ARCHIVOS = z.array(z.object({ filename: z.string(), status: z.string(), patch: z.string().optional() }));

export function clienteGitHub(o: OpcionesGitHub): GitHub & Fuentes {
  async function pedir(metodo: string, ruta: string, cuerpo?: unknown): Promise<Response> {
    const r = await fetch(`${o.api}${ruta}`, {
      method: metodo,
      headers: {
        accept: "application/vnd.github+json",
        authorization: `Bearer ${o.token}`,
        "x-github-api-version": "2022-11-28",
        "user-agent": "centinela-cpp",
        ...(cuerpo === undefined ? {} : { "content-type": "application/json" }),
      },
      ...(cuerpo === undefined ? {} : { body: JSON.stringify(cuerpo) }),
      redirect: "follow",
    });
    if (!r.ok) throw new ErrorGitHub(r.status, ruta, await r.text());
    return r;
  }
  const json = async <S extends z.ZodType>(esquema: S, ruta: string): Promise<z.output<S>> => esquema.parse(await (await pedir("GET", ruta)).json());

  return {
    async pullRequest(repo, numero) {
      const pr = await json(PR, `/repos/${repo}/pulls/${numero}`);
      const n = positivo("numero", pr.number);
      if (!n.ok) throw new Error("GitHub devolvió un número de PR inválido");
      return { numero: n.valor, titulo: pr.title, autor: pr.user.login, shaCabeza: pr.head.sha };
    },

    async archivosCambiados(repo, numero) {
      const todos = [];
      for (let pagina = 1; pagina <= 30; pagina++) {
        const lote = await json(ARCHIVOS, `/repos/${repo}/pulls/${numero}/files?per_page=100&page=${pagina}`);
        todos.push(...lote);
        if (lote.length < 100) break;
      }
      return todos.map((f) => ({ ruta: f.filename, eliminado: f.status === "removed", lineas: lineasDelParche(f.patch) }));
    },

    async publicarRevision(repo, numero, sha, cuerpo, comentarios) {
      await pedir("POST", `/repos/${repo}/pulls/${numero}/reviews`, {
        commit_id: sha,
        event: "COMMENT",
        body: cuerpo,
        comments: comentarios.map((c) => ({ path: c.ruta, line: c.linea, side: "RIGHT", body: c.cuerpo })),
      });
    },

    async publicarEstado(repo, sha, estado, enlace) {
      await pedir("POST", `/repos/${repo}/statuses/${sha}`, {
        state: estado.estado,
        description: estado.descripcion,
        context: CONTEXTO_ESTADO,
        target_url: enlace,
      });
    },

    /** Descarga el tarball del commit y lo extrae en un directorio temporal. */
    async obtener(repo, sha) {
      const dir = await mkdtemp(join(tmpdir(), "centinela-fuente-"));
      try {
        const r = await pedir("GET", `/repos/${repo}/tarball/${sha}`);
        if (r.body === null) throw new Error("tarball vacío");
        const tar = spawn("tar", ["-xzf", "-", "--strip-components=1", "-C", dir], { stdio: ["pipe", "ignore", "pipe"] });
        let error = "";
        tar.stderr.on("data", (b: Buffer) => (error += b.toString()));
        const fin = new Promise<void>((ok, mal) => tar.on("close", (c) => (c === 0 ? ok() : mal(new Error(`tar: ${error}`)))));
        await pipeline(Readable.fromWeb(r.body as import("node:stream/web").ReadableStream), tar.stdin);
        await fin;
      } catch (e) {
        await rm(dir, { recursive: true, force: true });
        throw e;
      }
      return { dir, liberar: () => rm(dir, { recursive: true, force: true }) };
    },
  };
}
