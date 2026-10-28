// Un GitHub simulado con muchos pull requests, para las pruebas no funcionales (práctica 8).
// El PR n tiene `archivos(n)` copias de demo/pr/src/cache.cpp (dos defectos cada una) y su propio sha.
import { execFileSync } from "node:child_process";
import { cpSync, mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { createServer } from "node:http";
import { tmpdir } from "node:os";
import { join } from "node:path";

export const REPO = "carga/centinela-carga";
const FUENTE = readFileSync(new URL("../demo/pr/src/cache.cpp", import.meta.url), "utf8");
export const shaDe = (n: number) => n.toString(16).padStart(40, "0");

export function githubVarios(puerto: number, archivos: (n: number) => number, titulo: (n: number) => string = (n) => `PR de carga ${n}`) {
  const tarballs = new Map<number, Buffer>();
  const publicados = { revisiones: 0, estados: 0 };
  const nombres = (k: number) => Array.from({ length: k }, (_, i) => `src/m${i + 1}.cpp`);

  function tarball(k: number): Buffer {
    const hecho = tarballs.get(k);
    if (hecho) return hecho;
    const dir = mkdtempSync(join(tmpdir(), "gh-"));
    const raiz = join(dir, "repo");
    cpSync(new URL("../demo/pr/", import.meta.url).pathname, raiz, { recursive: true });
    for (const n of nombres(k)) writeFileSync(join(raiz, n), FUENTE);
    const t = execFileSync("tar", ["-czf", "-", "-C", dir, "repo"]);
    tarballs.set(k, t);
    return t;
  }

  const servidor = createServer((req, res) => {
    let cuerpo = "";
    req.on("data", (c) => (cuerpo += c));
    req.on("end", () => {
      const u = req.url ?? "";
      const json = (x: unknown, estado = 200) => {
        res.writeHead(estado, { "content-type": "application/json" });
        res.end(JSON.stringify(x));
      };
      const pr = /^\/repos\/[^/]+\/[^/]+\/pulls\/(\d+)(\/files|\/reviews)?/.exec(u);
      if (pr) {
        const n = Number(pr[1]);
        if (pr[2] === "/files") {
          const lineas = FUENTE.replace(/\n$/, "").split("\n");
          const patch = [`@@ -0,0 +1,${lineas.length} @@`, ...lineas.map((l) => `+${l}`)].join("\n");
          return json(u.includes("page=1") ? nombres(archivos(n)).map((filename) => ({ filename, status: "added", patch })) : []);
        }
        if (pr[2] === "/reviews") {
          publicados.revisiones++;
          return json({ id: publicados.revisiones }, 201);
        }
        return json({ number: n, title: titulo(n), user: { login: "carga" }, head: { sha: shaDe(n) } });
      }
      const tb = /^\/repos\/[^/]+\/[^/]+\/tarball\/([0-9a-f]{40})$/.exec(u);
      if (tb) {
        res.writeHead(200, { "content-type": "application/x-gzip" });
        return res.end(tarball(archivos(parseInt(tb[1]!, 16))));
      }
      if (req.method === "POST" && u.includes("/statuses/")) {
        publicados.estados++;
        return json({ id: publicados.estados }, 201);
      }
      json({ message: "Not Found" }, 404);
    });
  });
  servidor.listen(puerto, "127.0.0.1");
  return {
    publicados,
    evento: (n: number) => JSON.stringify({ action: "opened", repository: { full_name: REPO }, pull_request: { number: n, title: titulo(n), user: { login: "carga" }, head: { sha: shaDe(n) } } }),
    cerrar: () => servidor.close(),
  };
}
