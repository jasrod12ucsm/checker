#!/usr/bin/env python3
"""Corre el plugin sobre proyectos C++ reales (código que no escribimos).

Para cada proyecto: cmake con compile_commands.json, y una invocación de
clang --analyze por unidad de traducción con SÓLO nuestro checker en la
salida que se guarda. Cada aviso se guarda con su ruta (notas) para
revisarlo a mano. Se corre dentro de la imagen checker:llvm21.

Uso: python3 bench/codigo_real.py <dir_proyectos> <salida.json> [modo] [inlining] [proyecto,...]
"""
from __future__ import annotations

import json
import re
import shlex
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PLUGIN = RAIZ / "build" / "plugin" / "libContainerInvalidation.so"
PROYECTOS = {
    # ejemplos/ del propio repositorio: dos unidades, para verificar RF-03 en segundos.
    "ejemplos": [],
    # nombre: opciones de cmake (sin pruebas ni benchmarks: no traen sus dependencias)
    "ninja": ["-DBUILD_TESTING=OFF"],
    "leveldb": ["-DLEVELDB_BUILD_TESTS=OFF", "-DLEVELDB_BUILD_BENCHMARKS=OFF"],
    "yaml-cpp": ["-DYAML_CPP_BUILD_TESTS=OFF", "-DYAML_CPP_BUILD_TOOLS=OFF"],
    # El proyecto grande: ~700 archivos .cc, STL en todas partes.
    "rocksdb": ["-DWITH_TESTS=OFF", "-DWITH_ALL_TESTS=OFF", "-DWITH_BENCHMARK_TOOLS=OFF",
                "-DWITH_TOOLS=OFF", "-DWITH_CORE_TOOLS=OFF", "-DWITH_TRACE_TOOLS=OFF",
                "-DWITH_GFLAGS=OFF", "-DFAIL_ON_WARNINGS=OFF", "-DPORTABLE=1"],
}
AVISO = re.compile(r"^(?P<file>[^:\s]+):(?P<line>\d+):(?P<col>\d+): (?P<kind>warning|note): (?P<msg>.*?)(?: \[(?P<chk>[\w.]+)\])?$")


def configurar(raiz: Path, nombre: str) -> list[dict]:
    # ejemplos/ está en el repositorio: su build va a build/, que no se versiona.
    build = RAIZ / "build" / "ejemplos" if nombre == "ejemplos" else raiz / f"{nombre}-build"
    subprocess.run(["cmake", "-S", str(raiz / nombre), "-B", str(build), "-G", "Ninja",
                    "-DCMAKE_EXPORT_COMPILE_COMMANDS=ON", "-DCMAKE_CXX_COMPILER=clang++",
                    "-DCMAKE_C_COMPILER=clang", *PROYECTOS[nombre]],
                   check=True, capture_output=True, text=True)
    # Encabezados generados (p. ej. leveldb/port_config.h) se crean al configurar.
    return json.loads((build / "compile_commands.json").read_text())


def analizar(entrada: dict, modo: str, inlining: str = "noredundancy") -> dict:
    args = entrada.get("arguments") or shlex.split(entrada["command"])
    archivo = entrada["file"]
    if not archivo.endswith((".cc", ".cpp", ".cxx")):
        return {"file": archivo, "omitido": True}
    # Quitar el compilador, -o y -c; agregar el análisis.
    resto, saltar = [], False
    for a in args[1:]:
        if saltar:
            saltar = False
            continue
        if a in ("-o", "-c"):
            saltar = a == "-o"
            continue
        if a == archivo or a.endswith(Path(archivo).name) and not a.startswith("-"):
            continue
        resto.append(a)
    # Sin color: la salida se interpreta con una expresión regular.
    resto = [a for a in resto if not a.startswith("-fdiagnostics-color") and a != "-fcolor-diagnostics"]
    cmd = ["clang++", *resto, "-fno-color-diagnostics", "--analyze", "-o", "/dev/null",
           "-Xclang", "-load", "-Xclang", str(PLUGIN),
           "-Xclang", "-analyzer-checker=ucsm.ContainerInvalidation",
           "-Xclang", "-analyzer-config", "-Xclang", f"ucsm.ContainerInvalidation:PolicyMode={modo}",
           "-Xclang", "-analyzer-output=text",
           # noredundancy (por defecto en CSA) no vuelve a analizar como raíz una
           # función ya inlinada: si el presupuesto cortó ese camino, no se ve.
           "-Xclang", f"-analyzer-inlining-mode={inlining}", archivo]
    t0 = time.time()
    p = subprocess.run(cmd, cwd=entrada["directory"], capture_output=True, text=True, timeout=900)
    avisos: list[dict] = []
    actual: dict | None = None
    for linea in p.stderr.splitlines():
        m = AVISO.match(linea)
        if not m:
            continue
        if m["kind"] == "warning" and m["chk"] == "ucsm.ContainerInvalidation":
            nuevo: dict = {"file": m["file"], "line": int(m["line"]), "msg": m["msg"],
                           "clase": "posible" if "posiblemente" in m["msg"] else "confirmado", "ruta": []}
            avisos.append(nuevo)
            actual = nuevo
        elif m["kind"] == "warning":
            actual = None
        elif actual is not None:
            actual["ruta"].append(f'{m["file"]}:{m["line"]}: {m["msg"]}')
    return {"file": archivo, "segundos": round(time.time() - t0, 2), "codigo": p.returncode,
            "error": p.stderr[-2000:] if p.returncode else "", "avisos": avisos}


def main() -> int:
    raiz, salida = Path(sys.argv[1]), Path(sys.argv[2])
    modo = sys.argv[3] if len(sys.argv) > 3 else "Possibly"
    inlining = sys.argv[4] if len(sys.argv) > 4 else "noredundancy"
    elegidos = sys.argv[5].split(",") if len(sys.argv) > 5 else [p for p in PROYECTOS if p != "ejemplos"]
    proyectos: dict[str, dict] = {}
    informe = {"modo": modo, "inlining": inlining, "proyectos": proyectos}
    for nombre in elegidos:
        entradas = configurar(raiz, nombre)
        with ThreadPoolExecutor(max_workers=12) as pool:
            res = list(pool.map(lambda e: analizar(e, modo, inlining), entradas))
        res = [r for r in res if not r.get("omitido")]
        rev = subprocess.run(["git", "-C", str(raiz / nombre), "rev-parse", "HEAD"],
                             capture_output=True, text=True).stdout.strip()
        proyectos[nombre] = {"commit": rev, "unidades": len(res),
                                        "fallos": sum(r["codigo"] != 0 for r in res),
                                        "segundos": round(sum(r["segundos"] for r in res), 1),
                                        "resultados": res}
        n = sum(len(r["avisos"]) for r in res)
        print(f"{nombre}: {len(res)} TU, {n} avisos, "
              f"{proyectos[nombre]['fallos']} TU con error, "
              f"{proyectos[nombre]['segundos']} s", flush=True)
    salida.write_text(json.dumps(informe, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
