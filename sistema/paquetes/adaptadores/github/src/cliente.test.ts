// El cliente contra un GitHub falso en un puerto local: se comprueba lo que se envía.
import { execFileSync } from "node:child_process";
import { existsSync, mkdtempSync, readFileSync, rmSync, writeFileSync, mkdirSync } from "node:fs";
import { createServer, type Server } from "node:http";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { afterAll, beforeAll, describe, expect, it } from "vitest";
import type { Positivo } from "@centinela/kernel";
import type { NombreRepo } from "@centinela/repositorios";
import { clienteGitHub, ErrorGitHub } from "./cliente";

const recibidas: { metodo: string; url: string; auth: string | undefined; cuerpo: unknown }[] = [];
let servidor: Server;
let api = "";
let tarball: Buffer;
const repo = "ucsm/demo" as NombreRepo;

beforeAll(async () => {
  const dir = mkdtempSync(join(tmpdir(), "centinela-tar-"));
  mkdirSync(join(dir, "ucsm-demo-abc", "src"), { recursive: true });
  writeFileSync(join(dir, "ucsm-demo-abc", "src", "a.cpp"), "int main() {}\n");
  execFileSync("tar", ["-czf", join(dir, "t.tgz"), "-C", dir, "ucsm-demo-abc"]);
  tarball = readFileSync(join(dir, "t.tgz"));
  rmSync(dir, { recursive: true });

  servidor = createServer((req, res) => {
    let cuerpo = "";
    req.on("data", (c) => (cuerpo += c));
    req.on("end", () => {
      recibidas.push({ metodo: req.method!, url: req.url!, auth: req.headers.authorization, cuerpo: cuerpo ? JSON.parse(cuerpo) : undefined });
      const u = req.url!;
      res.setHeader("content-type", "application/json");
      if (u === "/repos/ucsm/demo/pulls/7") return res.end(JSON.stringify({ number: 7, title: "Caché", user: { login: "ana" }, head: { sha: "abc" }, extra: 1 }));
      if (u.startsWith("/repos/ucsm/demo/pulls/7/files")) {
        const pagina = Number(new URL(u, "http://x").searchParams.get("page"));
        const lote = pagina === 1 ? Array.from({ length: 100 }, (_, i) => ({ filename: `f${i}.cpp`, status: "modified", patch: "@@ -1 +1 @@\n+x" })) : [{ filename: "viejo.cpp", status: "removed" }];
        return res.end(JSON.stringify(lote));
      }
      if (u === "/repos/ucsm/demo/tarball/abc") {
        res.setHeader("content-type", "application/x-gzip");
        return res.end(tarball);
      }
      if (u === "/repos/ucsm/demo/pulls/404") {
        res.statusCode = 404;
        return res.end('{"message":"Not Found"}');
      }
      if (req.method === "POST") {
        res.statusCode = 201;
        return res.end("{}");
      }
      res.statusCode = 500;
      res.end("{}");
    });
  });
  await new Promise<void>((ok) => servidor.listen(0, "127.0.0.1", ok));
  const dir2 = servidor.address();
  api = `http://127.0.0.1:${typeof dir2 === "object" && dir2 ? dir2.port : 0}`;
});
afterAll(() => new Promise<void>((ok) => servidor.close(() => ok())));

describe("cliente de GitHub", () => {
  const gh = () => clienteGitHub({ api, token: "tkn" });
  it("lee el PR con el token y se queda con lo que usa", async () => {
    expect(await gh().pullRequest(repo, 7 as Positivo)).toEqual({ numero: 7, titulo: "Caché", autor: "ana", shaCabeza: "abc" });
    expect(recibidas.at(-1)?.auth).toBe("Bearer tkn");
  });
  it("pagina los archivos cambiados y marca los eliminados", async () => {
    const fs = await gh().archivosCambiados(repo, 7 as Positivo);
    expect(fs).toHaveLength(101);
    expect(fs[0]).toEqual({ ruta: "f0.cpp", eliminado: false, lineas: new Set([1]) });
    expect(fs.at(-1)).toMatchObject({ ruta: "viejo.cpp", eliminado: true });
  });
  it("publica la revisión con comentarios en el lado nuevo", async () => {
    await gh().publicarRevision(repo, 7 as Positivo, "abc", "cuerpo", [{ ruta: "src/a.cpp", linea: 11, cuerpo: "c" }]);
    expect(recibidas.at(-1)).toMatchObject({
      metodo: "POST",
      url: "/repos/ucsm/demo/pulls/7/reviews",
      cuerpo: { commit_id: "abc", event: "COMMENT", body: "cuerpo", comments: [{ path: "src/a.cpp", line: 11, side: "RIGHT", body: "c" }] },
    });
  });
  it("publica el estado del commit con su contexto", async () => {
    await gh().publicarEstado(repo, "abc", { estado: "failure", descripcion: "1 confirmados" }, "http://c/revisiones/1");
    expect(recibidas.at(-1)).toMatchObject({ url: "/repos/ucsm/demo/statuses/abc", cuerpo: { state: "failure", context: "centinela/invalidacion", target_url: "http://c/revisiones/1" } });
  });
  it("una respuesta de error es un ErrorGitHub con el estado", async () => {
    await expect(gh().pullRequest(repo, 404 as Positivo)).rejects.toBeInstanceOf(ErrorGitHub);
  });
  it("descarga y extrae el código del commit, y liberar lo borra", async () => {
    const f = await gh().obtener(repo, "abc");
    expect(readFileSync(join(f.dir, "src", "a.cpp"), "utf8")).toContain("main");
    await f.liberar();
    expect(existsSync(f.dir)).toBe(false);
  });
});
