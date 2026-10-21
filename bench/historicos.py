#!/usr/bin/env python3
"""Errores reales de invalidación, sacados del historial de proyectos C++.

Etapa 1 — minar:   python3 bench/historicos.py minar <dir_clones> <candidatos.json>
  Busca en los mensajes de commit las correcciones de invalidación de
  iteradores, referencias o punteros, y se queda con las que tocan una
  mutación de contenedor en el diff. La revisión a mano de los candidatos
  produce bench/historicos.json (la lista curada, con el porqué de cada uno).

Etapa 2 — analizar: python3 bench/historicos.py analizar <dir_clones> <salida.json>
  Para cada error curado: analiza el archivo corregido en el commit ANTERIOR
  (tiene el error: debería avisar) y en el commit de la CORRECCIÓN (no debería),
  con CSA y con CSA + plugin. Un aviso cuenta si cae en una función que la
  corrección tocó.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

MENSAJE = re.compile(
    r"iterator[s]? (?:are |is |was |get |gets |being )?invalidat|invalidat\w* (?:the )?iterator|"
    r"invalid(?:ated)? iterator|iterator invalidation|dangling (?:reference|pointer|iterator)|"
    r"use[- ]after[- ](?:free|erase|move)|heap-use-after-free|"
    r"reference (?:invalidat|to .* after (?:push_back|emplace_back|insert|erase|resize))|"
    r"erase[sd]? (?:while|during) (?:iterat|loop)|modif\w+ (?:a |the )?(?:container|map|vector|set) while iterat|"
    r"reallocat\w* .*(?:invalidat|dangling)|after (?:push_back|emplace_back) .*(?:invalid|dangling)|"
    r"realloc\w*.*(?:pointer|reference|iterator)|(?:pointer|reference|iterator)s? .*realloc|"
    r"stale (?:iterator|reference|pointer)|(?:after|while) (?:erase|erasing)|erase\(it\)|"
    r"invalidat\w* (?:the |a |all )?(?:reference|pointer)s?",
    re.I)
FUERTE = re.compile(r"iterator|invalidat|realloc|erase|push_back|emplace|vector|std::map|unordered|"
                    r"container|dangling reference|reference to (?:an? )?element", re.I)
MUTACION = re.compile(r"\.(?:erase|push_back|emplace_back|emplace|insert|clear|resize|reserve|"
                      r"pop_back|pop_front|push_front|emplace_front|rehash|assign|swap)\s*\(|"
                      r"\[[^\]]+\]\s*=|std::(?:vector|map|set|unordered_\w+|deque|list)")
CPP = (".cc", ".cpp", ".cxx", ".h", ".hpp", ".hh")


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True,
                          errors="replace").stdout


def minar(raiz: Path, salida: Path) -> None:
    from concurrent.futures import ThreadPoolExecutor
    repos = sorted(p for p in raiz.iterdir() if (p / ".git").exists())
    if len(sys.argv) > 4:
        repos = [p for p in repos if p.name in sys.argv[4].split(",")]
    with ThreadPoolExecutor(max_workers=len(repos)) as pool:
        candidatos = [c for lst in pool.map(minar_repo, repos) for c in lst]
    salida.write_text(json.dumps(candidatos, indent=1, ensure_ascii=False))
    print(f"{len(candidatos)} candidatos -> {salida}")


def minar_repo(repo: Path) -> list[dict]:
    candidatos = []
    if True:
        # git --grep no entiende la sintaxis de Python: un filtro grueso con
        # palabras sueltas (OR) y el fino con MENSAJE.
        gruesos = [a for w in ("invalidat", "dangling", "use-after", "use after", "after-free",
                               "while iterat", "realloc", "stale iter", "stale ref", "stale pointer",
                               "after eras", "erase(it", "while eras") for a in ("--grep", w)]
        log = git(repo, "log", "--all", "--no-merges", "-i", *gruesos,
                  "--format=%H%x1f%ad%x1f%s%x1f%b%x1e", "--date=short")
        n = 0
        for reg in log.split("\x1e"):
            partes = reg.strip().split("\x1f")
            if len(partes) < 3:
                continue
            h, fecha, titulo = partes[:3]
            cuerpo = partes[3] if len(partes) > 3 else ""
            if not MENSAJE.search(titulo + "\n" + cuerpo):
                continue
            # Bajar el diff cuesta (clon parcial): sólo si el mensaje habla de contenedores.
            if not FUERTE.search(titulo + "\n" + cuerpo):
                continue
            archivos = [f for f in git(repo, "show", "--format=", "--name-only", h).split() if f.endswith(CPP)]
            if not archivos or len(archivos) > 8:
                continue  # sin C++, o una corrección mezclada con mucho más
            diff = git(repo, "show", "--format=", "-U0", h, "--", *archivos)
            cambios = [l for l in diff.splitlines() if l[:1] in "+-" and not l.startswith(("+++", "---"))]
            if not any(MUTACION.search(l) for l in cambios) or len(cambios) > 200:
                continue
            candidatos.append({"proyecto": repo.name, "commit": h, "fecha": fecha, "titulo": titulo,
                               "cuerpo": cuerpo.strip()[:600], "archivos": archivos, "lineas": len(cambios)})
            n += 1
        print(f"{repo.name:14} {n:4} candidatos", flush=True)
    return candidatos


# ── etapa 2 ─────────────────────────────────────────────────────────────────
PLUGIN = Path(__file__).resolve().parent.parent / "build" / "plugin" / "libContainerInvalidation.so"
CSA = ["core", "cplusplus", "alpha.cplusplus.IteratorModeling", "alpha.cplusplus.ContainerModeling",
       "alpha.cplusplus.InvalidatedIterator", "alpha.cplusplus.IteratorRange",
       "alpha.cplusplus.MismatchedIterator"]
AVISO = re.compile(r"^(?P<file>[^:\s]+):(?P<line>\d+):(?P<col>\d+): warning: (?P<msg>.*?) \[(?P<chk>[\w.]+)\]$")


def hunks(repo: Path, commit: str, archivo: str) -> list[tuple[int, int]]:
    """Rangos de líneas del archivo en el commit ANTERIOR que la corrección tocó."""
    out = []
    for m in re.finditer(r"^@@ -(\d+)(?:,(\d+))? ", git(repo, "show", "--format=", "-U0", commit, "--", archivo), re.M):
        a, n = int(m.group(1)), int(m.group(2) or 1)
        out.append((a, a + max(n, 1) - 1))
    return out


def preparar(repo: Path, commit: str, destino: Path) -> bool:
    # El árbol se reutiliza entre proyectos: se borra entero y se poda el registro.
    shutil.rmtree(destino, ignore_errors=True)
    subprocess.run(["git", "-C", str(repo), "worktree", "prune"], capture_output=True)
    p = subprocess.run(["git", "-C", str(repo), "worktree", "add", "--detach", "-f", str(destino), commit],
                       capture_output=True, text=True)
    return p.returncode == 0


def banderas(arbol: Path, archivo: str, extra: list[str]) -> list[str]:
    """Sin compile_commands de una versión vieja: las carpetas de cabeceras
    habituales del árbol, la del archivo, y lo que diga la entrada curada."""
    inc = [arbol, arbol / Path(archivo).parent]
    for d in ("include", "src", "lib", "src/include", "util", "third_party", "port"):
        if (arbol / d).is_dir():
            inc.append(arbol / d)
    # Las -I relativas de la entrada curada son relativas a la raíz del árbol.
    rel = [f"-I{arbol / a[2:]}" if a.startswith("-I") and not a.startswith("-I/") else a for a in extra]
    return [f"-I{p}" for p in inc] + rel


def analizar_tu(arbol: Path, archivo: str, extra: list[str], plugin: bool, std: str) -> dict:
    checkers = list(CSA) + (["ucsm.ContainerInvalidation"] if plugin else [])
    cmd = ["clang++", f"-std={std}", "-fno-color-diagnostics", "-w", "--analyze", "-o", "/dev/null",
           *banderas(arbol, archivo, extra),
           *(["-Xclang", "-load", "-Xclang", str(PLUGIN)] if plugin else []),
           "-Xclang", f"-analyzer-checker={','.join(checkers)}",
           "-Xclang", "-analyzer-config", "-Xclang", "aggressive-binary-operation-simplification=true",
           *(["-Xclang", "-analyzer-config", "-Xclang", "ucsm.ContainerInvalidation:PolicyMode=Possibly"] if plugin else []),
           "-Xclang", "-analyzer-inlining-mode=all", str(arbol / archivo)]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=1800, cwd=arbol)
    avisos = []
    for l in p.stderr.splitlines():
        m = AVISO.match(l)
        if m and Path(m["file"]).resolve() == (arbol / archivo).resolve():
            avisos.append({"line": int(m["line"]), "msg": m["msg"], "checker": m["chk"]})
    errores = [l for l in p.stderr.splitlines() if ": error:" in l or ": fatal error:" in l]
    return {"codigo": p.returncode, "errores": errores[:5], "avisos": avisos}


def relevantes(avisos: list[dict], rangos: list[tuple[int, int]], margen: int) -> list[dict]:
    """Avisos de invalidación cerca de lo que la corrección tocó."""
    return [a for a in avisos
            if (a["checker"] == "ucsm.ContainerInvalidation" or a["checker"].startswith("alpha.cplusplus"))
            and any(i - margen <= a["line"] <= f + margen for i, f in rangos)]


def analizar(raiz: Path, salida: Path) -> None:
    curados = json.loads((Path(__file__).parent / "historicos.json").read_text())
    raiz = raiz.resolve()
    tmp = raiz / "_arbol"
    res = []
    for c in curados:
        repo = raiz / c["proyecto"]
        r = dict(c)
        for lado, commit in (("antes", f"{c['commit']}^"), ("despues", c["commit"])):
            if not preparar(repo, commit, tmp):
                r[lado] = {"incidente": "checkout"}
                continue
            rangos = hunks(repo, c["commit"], c["archivo"]) if lado == "antes" else \
                [(a, b) for a, b in hunks_despues(repo, c["commit"], c["archivo"])]
            lado_r = {}
            for cond, plugin in (("csa", False), ("plugin", True)):
                t = analizar_tu(tmp, c["archivo"], c.get("banderas", []), plugin, c.get("std", "c++17"))
                if t["codigo"] != 0 and not t["avisos"]:
                    lado_r[cond] = {"incidente": t["errores"] or ["clang falló"]}
                    continue
                lado_r[cond] = {"avisos": relevantes(t["avisos"], rangos, c.get("margen", 40)),
                                "todos": len(t["avisos"])}
            r[lado] = lado_r
        res.append(r)
        print(c["id"], json.dumps({k: r[k] for k in ("antes", "despues")}, ensure_ascii=False)[:400], flush=True)
    subprocess.run(["git", "-C", str(raiz / curados[0]["proyecto"]), "worktree", "prune"], capture_output=True)
    salida.write_text(json.dumps(res, indent=1, ensure_ascii=False))


def hunks_despues(repo: Path, commit: str, archivo: str) -> list[tuple[int, int]]:
    """Los mismos rangos, en las líneas del commit de la corrección."""
    out = []
    for m in re.finditer(r"^@@ -\S+ \+(\d+)(?:,(\d+))? ", git(repo, "show", "--format=", "-U0", commit, "--", archivo), re.M):
        a, n = int(m.group(1)), int(m.group(2) or 1)
        out.append((a, a + max(n, 1) - 1))
    return out


if __name__ == "__main__":
    {"minar": lambda: minar(Path(sys.argv[2]), Path(sys.argv[3])),
     "analizar": lambda: analizar(Path(sys.argv[2]), Path(sys.argv[3]))}[sys.argv[1]]()
