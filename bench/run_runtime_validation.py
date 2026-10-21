#!/usr/bin/env python3
"""Ejecuta el corpus bajo oráculos dinámicos y conserva la evidencia observada.

Una ejecución limpia no redefine la etiqueta normativa: UB puede no manifestarse
en una implementación concreta. Por ello el informe llama a los resultados
"evidencia dinámica", nunca a una reclasificación de UB/SAFE/POLICY.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path


def run(cmd, **kwargs):
    return subprocess.run(cmd, text=True, capture_output=True, **kwargs)


def build(compiler: str, flags: list[str], runner: Path, binary: Path) -> None:
    result = run([compiler, "-std=c++17", "-O0", "-g", *flags, str(runner), "-o", str(binary)])
    if result.returncode:
        raise RuntimeError(f"No se pudo compilar {' '.join(flags)}:\n{result.stderr}")


def compiler_version(compiler: str) -> str:
    result = run([compiler, "--version"])
    return result.stdout.splitlines()[0] if result.stdout else compiler


def observe(binary: Path, case: str, mode: str, timeout: float) -> dict:
    try:
        environment = os.environ.copy()
        # LeakSanitizer no puede iniciarse bajo algunos sandboxes/ptrace. No
        # medimos fugas en este experimento: medimos invalidación temporal.
        environment["ASAN_OPTIONS"] = "detect_leaks=0"
        result = run([str(binary), case, mode], timeout=timeout, env=environment)
    except subprocess.TimeoutExpired:
        return {"estado": "TIMEOUT", "codigo": None, "stderr": ""}
    stderr = result.stderr[-4000:]
    text = stderr.lower()
    markers = ("addresssanitizer", "undefinedbehaviorsanitizer", "error: attempt",
               "error: dereference", "error: increment", "error: comparing")
    if any(marker in text for marker in markers):
        state = "DETECTADO"
    elif result.returncode == 0:
        state = "SIN_DETECCION"
    else:
        state = "ABORTO_SIN_CLASIFICAR"
    return {"estado": state, "codigo": result.returncode, "stderr": stderr}


def scenario(meta: dict, mode: str) -> dict:
    """Condición experimental explícita, trazable por cada fila POLICY."""
    if meta["esperado"] != "POLICY":
        return {"tipo": "natural", "precondicion": "estado inicial ordinario"}
    container, op = meta["contenedor"], meta["op"]
    if op == "shrink_to_fit":
        return {
            "tipo": "observado_no_vinculante",
            "precondicion": ("holgura de capacidad" if mode == "force"
                              else "capacidad previamente ajustada al tamaño"),
            "nota": "shrink_to_fit es una solicitud no vinculante; el resultado se registra, no se presupone.",
        }
    if container in {"vector", "string"}:
        if mode == "force":
            condition = "capacidad agotada antes de la mutación"
        elif op in {"reserve", "resize_grow"}:
            condition = "capacidad 512, suficiente para size()+100 tres veces"
        elif op == "pop_back":
            condition = "8 elementos: tres rondas de pop_back no alcanzan al iterador"
        else:
            condition = "capacidad 512, con espacio para la mutación"
        return {"tipo": "controlado", "precondicion": condition}
    if container in {"uset", "umap", "umset"}:
        return {"tipo": "controlado", "precondicion": (
            "factor de carga alcanzado; la inserción dispara rehash" if mode == "force"
            else "reserve(256), sin rehash para la inserción evaluada"
        )}
    return {"tipo": "controlado", "precondicion": "configuración específica del caso"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--truth", default="test/corpus_truth.json")
    parser.add_argument("--runner", default="test/runtime_runner.cpp")
    parser.add_argument("--output", default="test/runtime_validation_results.json")
    parser.add_argument("--build-dir", default="build/runtime")
    parser.add_argument("--timeout", type=float, default=2.0)
    parser.add_argument("--limit", type=int, default=0, help="solo para depuración")
    parser.add_argument("--start", type=int, default=0, help="índice inicial para ejecutar por lotes")
    parser.add_argument("--append", action="store_true", help="reemplaza este lote dentro del informe existente")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    truth_path = root / args.truth
    runner = root / args.runner
    output = root / args.output
    build_dir = Path(args.build_dir)
    build_dir.mkdir(parents=True, exist_ok=True)

    generator = root / "bench/gen_runtime_harness.py"
    generated = run([sys.executable, str(generator), "--truth", str(truth_path), "--output", str(runner)])
    if generated.returncode:
        raise RuntimeError(generated.stderr)

    gcc = shutil.which("g++")
    clang = shutil.which("clang++")
    if not gcc or not clang:
        raise RuntimeError("Se requieren g++ (libstdc++ Debug Mode) y clang++ (ASan).")

    debug_binary = build_dir / "runtime_debug"
    asan_binary = build_dir / "runtime_asan"
    build(gcc, ["-D_GLIBCXX_DEBUG"], runner, debug_binary)
    build(clang, ["-fsanitize=address,undefined", "-fno-omit-frame-pointer"], runner, asan_binary)

    truth = json.loads(truth_path.read_text())
    all_cases = list(truth.items())
    end = args.start + args.limit if args.limit else None
    cases = all_cases[args.start:end]
    rows = []
    for index, (case, meta) in enumerate(cases, 1):
        modes = ["natural"] if meta["esperado"] != "POLICY" else ["force", "preserve"]
        for mode in modes:
            rows.append({
                "fn": case, "modo": mode, "etiqueta_normativa": meta["esperado"],
                "contenedor": meta["contenedor"], "op": meta["op"],
                "sostiene": meta["sostiene"], "forma": meta["forma"],
                "escenario": scenario(meta, mode),
                "libstdcxx_debug": observe(debug_binary, case, mode, args.timeout),
                "asan_ubsan": observe(asan_binary, case, mode, args.timeout),
            })
        if index % 50 == 0:
            print(f"{index}/{len(cases)} casos ejecutados", flush=True)

    if args.append and output.exists():
        refreshed = {case for case, _ in cases}
        previous = json.loads(output.read_text())
        rows = [row for row in previous.get("resultados", []) if row["fn"] not in refreshed] + rows
        rows.sort(key=lambda row: (list(truth).index(row["fn"]), row["modo"]))

    summary = {}
    for oracle in ("libstdcxx_debug", "asan_ubsan"):
        summary[oracle] = dict(Counter(row[oracle]["estado"] for row in rows))
    report = {
        "descripcion": "Validación dinámica reproducible por escenarios; no sustituye el oráculo normativo.",
        "casos_base": len({row["fn"] for row in rows}), "ejecuciones": len(rows),
        "timeout_segundos": args.timeout, "resumen": summary, "resultados": rows,
        "entorno": {
            "gxx": compiler_version(gcc),
            "clangxx": compiler_version(clang),
            "estandar": "C++17",
            "modo_debug": "-D_GLIBCXX_DEBUG",
            "sanitizadores": "-fsanitize=address,undefined",
        },
    }
    expected_runs = sum(2 if meta["esperado"] == "POLICY" else 1 for meta in truth.values())
    if len(rows) == expected_runs and {row["fn"] for row in rows} == set(truth):
        report["cobertura_protocolo"] = "COMPLETA"
    else:
        report["cobertura_protocolo"] = "INCOMPLETA"
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"casos_base": len({row["fn"] for row in rows}), "ejecuciones": len(rows), "resumen": summary}, indent=2))


if __name__ == "__main__":
    main()
