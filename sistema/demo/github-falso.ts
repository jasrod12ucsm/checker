// Un GitHub mínimo en memoria para demostrar Centinela sin credenciales: un repositorio
// `demo/centinela-demo` con el PR #1, cuyos archivos son los de demo/pr/. Registra lo que
// Centinela publica (revisiones y estados) y lo muestra en GET /_registro.
import { execFileSync } from "node:child_process";
import { readdirSync, readFileSync, statSync } from "node:fs";
import { createServer } from "node:http";
import { join, relative } from "node:path";

export const REPO = "demo/centinela-demo";
const SHA = "d3m0000000000000000000000000000000000001";
const DIR = new URL("./pr/", import.meta.url).pathname;

function archivos(dir: string): string[] {
  return readdirSync(dir).flatMap((n) => (statSync(join(dir, n)).isDirectory() ? archivos(join(dir, n)) : [join(dir, n)]));
}

export function githubFalso(puerto: number) {
  const registro: { tipo: string; cuerpo: unknown }[] = [];
  const lista = archivos(DIR).map((f) => {
    const texto = readFileSync(f, "utf8");
    const lineas = texto.replace(/\n$/, "").split("\n");
    return { filename: relative(DIR, f), status: "added", patch: [`@@ -0,0 +1,${lineas.length} @@`, ...lineas.map((l) => `+${l}`)].join("\n") };
  });
  const tarball = execFileSync("tar", ["-czf", "-", "--transform", "s,^\\.,demo-centinela-demo-d3m0,", "-C", DIR, "."]);

  const servidor = createServer((req, res) => {
    let cuerpo = "";
    req.on("data", (c) => (cuerpo += c));
    req.on("end", () => {
      const u = req.url ?? "";
      const json = (x: unknown, estado = 200) => {
        res.writeHead(estado, { "content-type": "application/json" });
        res.end(JSON.stringify(x));
      };
      if (u === "/_registro") return json(registro);
      if (u === `/repos/${REPO}/pulls/1`) return json({ number: 1, title: "Agrega una caché de nombres", user: { login: "ana-dev" }, head: { sha: SHA } });
      if (u.startsWith(`/repos/${REPO}/pulls/1/files`)) return json(u.includes("page=1") ? lista : []);
      if (u === `/repos/${REPO}/tarball/${SHA}`) {
        res.writeHead(200, { "content-type": "application/x-gzip" });
        return res.end(tarball);
      }
      if (req.method === "POST" && (u === `/repos/${REPO}/pulls/1/reviews` || u === `/repos/${REPO}/statuses/${SHA}`)) {
        registro.push({ tipo: u.includes("reviews") ? "revision" : "estado", cuerpo: JSON.parse(cuerpo) });
        return json({ id: registro.length }, 201);
      }
      json({ message: "Not Found" }, 404);
    });
  });
  servidor.listen(puerto, "127.0.0.1");
  return {
    registro,
    sha: SHA,
    evento: () => JSON.stringify({ action: "opened", repository: { full_name: REPO }, pull_request: { number: 1, title: "Agrega una caché de nombres", user: { login: "ana-dev" }, head: { sha: SHA } } }),
    cerrar: () => servidor.close(),
  };
}
