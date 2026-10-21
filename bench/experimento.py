#!/usr/bin/env python3
"""Ejecutar el experimento: el workflow de libro/diseno/dsl/evaluacion.md §6.

  VerifyInputs → Run (una invocación de clang por caso y condición, D-15)
  → Normalize (SARIF → Warning) → Attribute (Warning → caso y sitio)
  → Match (→ Verdict) → Aggregate (Counts por grupo, métricas).

Condiciones (un ExperimentPair, RN-002): la de referencia ES base; las
experimentales SON base + plugin, con PolicyMode Silent y Possibly. No se
puede escribir una experimental que difiera de base en otra cosa.

Una cuarta, Plugin-Possibly, quita de base los checkers alpha.cplusplus de
iteradores. Hace falta porque InvalidatedIterator corta el camino (nodo de
error fatal) en el mismo uso que nuestro checker vigila: en base + plugin no
se puede saber cuánto aporta el plugin por sí solo.

Salida en test/experimento/: ejecucion.json, cotejo.json, metricas.json.
Se corre dentro de la imagen checker:llvm21:

  python3 bench/experimento.py [--jobs N] [--solo f_vector_...]
  python3 bench/experimento.py --muestra --salida build/verificacion

Con --solo o --muestra la salida no reemplaza los resultados oficiales:
no escribe test/corpus_results.json ni test/corpus_fallos.json.
"""
from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BANCO = RAIZ / "test" / "corpus.cpp"
VERDAD = RAIZ / "test" / "corpus_truth.json"
PLUGIN = RAIZ / "build" / "plugin" / "libContainerInvalidation.so"
SALIDA = RAIZ / "test" / "experimento"
NUESTRO = "ucsm.ContainerInvalidation"
TIMEOUT = 120

# ── las condiciones ─────────────────────────────────────────────────────────
BASE_CHECKERS = ["core", "cplusplus", "alpha.cplusplus.IteratorModeling",
                 "alpha.cplusplus.ContainerModeling", "alpha.cplusplus.InvalidatedIterator",
                 "alpha.cplusplus.IteratorRange", "alpha.cplusplus.MismatchedIterator"]
BASE_OPCIONES = ["aggressive-binary-operation-simplification=true"]


@dataclass(frozen=True)
class Condicion:
    nombre: str                    # Reference | Experimental-Silent | Experimental-Possibly | Plugin-Possibly
    modo: str | None = None        # PolicyMode del plugin; None = sin plugin
    sin_alpha: bool = False        # quita alpha.cplusplus.* de base

    def argumentos(self) -> list[str]:
        checkers, opciones, carga = list(BASE_CHECKERS), list(BASE_OPCIONES), []
        if self.sin_alpha:
            checkers = [c for c in checkers if not c.startswith("alpha.")]
        if self.modo:
            carga = ["-Xclang", "-load", "-Xclang", str(PLUGIN)]
            checkers.append(NUESTRO)
            opciones.append(f"{NUESTRO}:PolicyMode={self.modo}")
        args = ["clang++", "--analyze", "--analyzer-output", "sarif", "-std=c++17", *carga,
                "-Xclang", f"-analyzer-checker={','.join(checkers)}"]
        for o in opciones:
            args += ["-Xclang", "-analyzer-config", "-Xclang", o]
        return args


CONDICIONES = [Condicion("Reference"), Condicion("Experimental-Silent", "Silent"),
               Condicion("Experimental-Possibly", "Possibly"),
               Condicion("Plugin-Possibly", "Possibly", sin_alpha=True)]

# ── datos (evaluacion.md §2) ────────────────────────────────────────────────
OUTCOMES = ("Completed", "CompileError", "Crash", "Timeout", "Unreadable")
VERDICTS = ("TP", "FP", "FN", "TN", "PolicyWarned", "PolicySilent", "Incident")


@dataclass(frozen=True)
class Warning:
    line: int
    column: int
    checker: str
    clase: str                     # Confirmed | Possible | Other
    message: str


@dataclass
class Run:
    case: str
    condicion: str
    outcome: str
    segundos: float
    max_rss_kb: int
    detalle: str = ""              # stderr si no terminó bien
    warnings: list[Warning] = field(default_factory=list)


@dataclass
class Match:
    case: str
    condicion: str
    verdict: str
    sitios: list[str]              # sitio de cada aviso confirmado atribuido: sostenido|control|otro
    en_sostenido: bool             # algún aviso confirmado sobre el handle que sostiene el caso
    fuera_de_sitio: int            # avisos confirmados en un caso UB sobre un handle que no es UB
    posibles: int                  # avisos posibles (sólo nuestro checker)


# ── Counts: un monoide (ley «los conteos se suman por partes») ───────────────
@dataclass(frozen=True)
class Counts:
    tp: int = 0
    fp: int = 0
    fn: int = 0
    tn: int = 0
    policyWarned: int = 0
    policySilent: int = 0
    incidents: int = 0
    # aparte, nunca en precisión ni cobertura:
    posiblesSobreUB: int = 0
    posiblesSobreSAFE: int = 0
    ubEnSostenido: int = 0         # casos UB cuyo handle sostenido es UB y recibió el aviso
    ubSostenidoTotal: int = 0      # casos UB cuyo handle sostenido es UB

    def __add__(self, o: "Counts") -> "Counts":
        return Counts(*(a + b for a, b in zip(dataclasses.astuple(self), dataclasses.astuple(o))))

    @staticmethod
    def of(m: Match, caso: dict) -> "Counts":
        d = {VERDICT_CAMPO[m.verdict]: 1}
        if m.verdict != "Incident":
            if caso["esperado"] == "UB" and m.posibles and m.verdict == "FN":
                d["posiblesSobreUB"] = 1
            if caso["esperado"] == "SAFE" and m.posibles:
                d["posiblesSobreSAFE"] = 1
        if caso["esperado"] == "UB" and caso["handles"]["sostenido"] == "UB":
            d["ubSostenidoTotal"] = 1
            d["ubEnSostenido"] = int(m.en_sostenido)
        return Counts(**d)


VERDICT_CAMPO = {"TP": "tp", "FP": "fp", "FN": "fn", "TN": "tn", "PolicyWarned": "policyWarned",
                 "PolicySilent": "policySilent", "Incident": "incidents"}


def razon(a: int, b: int) -> float | None:
    """Ley «una métrica sin denominador no es cero»: None es Undefined."""
    return a / b if b else None


def metricas(c: Counts) -> dict:
    p, r = razon(c.tp, c.tp + c.fp), razon(c.tp, c.tp + c.fn)
    return {"precision": p, "recall": r,
            "f1": (2 * p * r / (p + r) if p is not None and r is not None and p + r else None),
            "policyRate": razon(c.policyWarned, c.policyWarned + c.policySilent),
            "recallSostenido": razon(c.ubEnSostenido, c.ubSostenidoTotal)}


# ── VerifyInputs ────────────────────────────────────────────────────────────
def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def firmas() -> dict[str, str]:
    """Nombre de la función → firma que acepta -analyze-function (la de CSA)."""
    p = subprocess.run(["clang++", "--analyze", "-std=c++17", "-o", "/dev/null",
                        "-Xclang", "-analyzer-checker=core", "-Xclang", "-analyzer-display-progress",
                        str(BANCO)], capture_output=True, text=True)
    out = {}
    for m in re.finditer(r"ANALYZE \(Syntax\): \S+ ((f_\w+)\(.*?\)) :", p.stderr):
        out[m.group(2)] = m.group(1)
    return out


def verificar() -> dict:
    if not PLUGIN.exists():
        sys.exit(f"PluginNotLoadable: no existe {PLUGIN}")
    p = subprocess.run(["clang", "-cc1", "-load", str(PLUGIN), "-analyzer-checker-help"],
                       capture_output=True, text=True)
    if NUESTRO not in p.stdout:
        sys.exit(f"PluginNotLoadable:\n{p.stderr[-2000:]}")
    version = subprocess.run(["clang++", "--version"], capture_output=True, text=True).stdout.splitlines()[0]
    libstdcxx = subprocess.run(["sh", "-c", "dpkg-query -W -f='${Version}' libstdc++-13-dev 2>/dev/null"],
                               capture_output=True, text=True).stdout
    congelado = None
    for sello in sorted((RAIZ / "test").glob("banco-*.json")):
        s = json.loads(sello.read_text())
        if (s["corpus.cpp"], s["corpus_truth.json"]) == (sha256(BANCO), sha256(VERDAD)):
            congelado = s["banco"]
    if congelado is None and list((RAIZ / "test").glob("banco-*.json")):
        sys.exit("BankNotFrozen: el banco no coincide con ningún sello test/banco-*.json")
    return {"clang": version, "libstdcxx": libstdcxx or "desconocida",
            "plugin_sha256": sha256(PLUGIN), "banco_sha256": sha256(BANCO),
            "verdad_sha256": sha256(VERDAD),
            "banco_congelado": congelado,
            "condiciones": {c.nombre: c.argumentos() for c in CONDICIONES},
            "timeout": TIMEOUT}


# ── Run ─────────────────────────────────────────────────────────────────────
def ejecutar(case: str, firma: str, cond: Condicion, tmp: Path) -> tuple[Run, dict | None]:
    sarif = tmp / f"{case}.{cond.nombre}.sarif"
    cmd = [*cond.argumentos(), "-Xclang", f"-analyze-function={firma}", "-o", str(sarif), str(BANCO)]
    t0 = time.time()
    with open(tmp / f"{case}.{cond.nombre}.err", "w+") as errf:
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=errf)
        reloj = threading.Timer(TIMEOUT, proc.kill)
        reloj.start()
        # wait4 da el máximo de memoria residente de ESTE clang, no del grupo.
        _, status, uso = os.wait4(proc.pid, 0)
        reloj.cancel()
        proc.returncode = os.waitstatus_to_exitcode(status)
        errf.seek(0)
        err = errf.read()
    rss = uso.ru_maxrss
    if time.time() - t0 >= TIMEOUT:
        return Run(case, cond.nombre, "Timeout", TIMEOUT, rss), None
    dt = round(time.time() - t0, 3)
    if proc.returncode < 0 or "PLEASE submit a bug report" in err:
        return Run(case, cond.nombre, "Crash", dt, rss, err[-3000:]), None
    if proc.returncode != 0:
        return Run(case, cond.nombre, "CompileError", dt, rss, err[-3000:]), None
    try:
        doc = json.loads(sarif.read_text())
        sarif.unlink()
    except (OSError, json.JSONDecodeError) as e:
        return Run(case, cond.nombre, "Unreadable", dt, rss, f"{e}\n{err[-2000:]}"), None
    return Run(case, cond.nombre, "Completed", dt, rss), doc


# ── Normalize ───────────────────────────────────────────────────────────────
def clase_de(checker: str, mensaje: str) -> str:
    if checker == NUESTRO:
        # El texto lo fija plugin/checker/Messages.cpp: el posible siempre dice «posiblemente».
        return "Possible" if "posiblemente" in mensaje else "Confirmed"
    if checker.startswith("alpha.cplusplus."):
        return "Confirmed"
    return "Other"


def normalizar(doc: dict | list) -> list[Warning]:
    """SARIF → avisos. Aplicado a una lista de Warning la devuelve igual
    (ley «normalizar dos veces es normalizar una»)."""
    if isinstance(doc, list):
        return sorted(set(doc), key=lambda w: (w.line, w.column, w.checker, w.message))
    out = set()
    for run in doc.get("runs", []):
        for r in run.get("results", []):
            reg = r["locations"][0]["physicalLocation"]["region"]
            msg = r["message"]["text"]
            out.add(Warning(reg["startLine"], reg.get("startColumn", 0), r["ruleId"],
                            clase_de(r["ruleId"], msg), msg))
    return normalizar(list(out))


# ── Attribute ───────────────────────────────────────────────────────────────
def rangos() -> dict[str, tuple[int, int]]:
    """Caso → [primera, última] línea de su función en corpus.cpp."""
    src = BANCO.read_text().splitlines()
    out, actual, inicio = {}, None, 0
    for i, l in enumerate(src, 1):
        m = re.match(r"^void (f_\w+)\(", l)
        if m:
            actual, inicio = m.group(1), i
        elif actual and l == "}":
            out[actual] = (inicio, i)
            actual = None
    return out


def sitio(caso: dict, linea: str) -> str:
    """¿Sobre qué handle del caso cae un aviso? Lo decide la línea del uso."""
    t = linea.strip()
    if t.startswith("for ("):
        return "sostenido" if caso["sostiene"] == "it" else "control"
    if "sink(" in t or caso["sostiene"] == "it":
        return "sostenido"
    return "otro"


def atribuir(case: str, ws: list[Warning], rango: dict, src: list[str], caso: dict
             ) -> tuple[list[tuple[Warning, str]], list[Warning]]:
    """Ley «un aviso pertenece a lo más a un caso»: el de la función que lo contiene."""
    a, b = rango[case]
    dentro: list[Warning] = []
    fuera: list[Warning] = []
    for w in ws:
        (dentro if a <= w.line <= b else fuera).append(w)
    return [(w, sitio(caso, src[w.line - 1])) for w in dentro], fuera


# ── Match (evaluacion.md §6, con cotejo por sitio) ──────────────────────────
def cotejar(case: str, caso: dict, run: Run, avisos: list[tuple[Warning, str]]) -> Match:
    if run.outcome != "Completed":
        # Ley «un fallo nunca es un verdadero negativo».
        return Match(case, run.condicion, "Incident", [], False, 0, 0)
    conf = [(w, s) for w, s in avisos if w.clase == "Confirmed"]
    posibles = sum(w.clase == "Possible" for w, _ in avisos)
    etiqueta_de = {"sostenido": caso["handles"]["sostenido"], "control": caso["handles"]["control"]}
    # Un aviso acierta en un caso UB sólo si cae sobre un handle que la norma da por inválido.
    buenos = [s for _, s in conf if etiqueta_de.get(s) == "UB"]
    e = caso["esperado"]
    if e == "UB":
        v = "TP" if buenos else "FN"
    elif e == "SAFE":
        v = "FP" if conf else "TN"
    else:
        v = "PolicyWarned" if conf or posibles else "PolicySilent"
    return Match(case, run.condicion, v, [s for _, s in conf],
                 any(s == "sostenido" for s in buenos),
                 len(conf) - len(buenos) if e == "UB" else 0, posibles)


# ── Aggregate ───────────────────────────────────────────────────────────────
GRUPOS = ("contenedor", "op", "sostiene", "forma", "esperado", "garantia")


def agregar(matches: list[Match], verdad: dict) -> dict:
    """Ley «los conteos se reconstruyen desde el cotejo»."""
    total = Counts()
    out: dict[str, dict[str, Counts]] = {g: {} for g in GRUPOS}
    for m in matches:
        c = Counts.of(m, verdad[m.case])
        total = total + c
        for g in GRUPOS:
            k = verdad[m.case][g]
            out[g][k] = out[g].get(k, Counts()) + c
    serial = lambda c: {**dataclasses.asdict(c), **metricas(c)}
    return {"All": serial(total),
            **{g: {k: serial(v) for k, v in sorted(out[g].items())} for g in GRUPOS}}


# ── catálogo causal de los FN de la referencia (antes en run_corpus.py) ─────
INSERCIONES = {"push_back", "emplace_back", "push_front", "insert", "insert_begin", "insert_end",
               "insert_middle", "insert_after", "append", "emplace", "subscript", "resize_grow",
               "reserve", "rehash"}


def causa(caso: dict) -> str:
    """Por qué calla CSA, con precedencia: la primera que aplica."""
    if caso["sostiene"] in ("ref", "ptr"):
        return "1. El dominio de referencias y punteros no esta modelado"
    if caso["forma"] == "recto":
        return "2. Sin comparacion previa contra end(), el modelado no se activa"
    if "erase" in caso["op"] or caso["op"] in ("pop_front", "pop_back", "clear"):
        return "3. Se invalida por identidad del iterador, no por posicion"
    if caso["op"] in INSERCIONES:
        return "4. La invalidacion por insercion/realojamiento no esta modelada"
    return "5. Operacion no modelada"


# ── ida y vuelta (ley «read(write(run)) = run») ─────────────────────────────
def escribir_runs(runs: list[Run]) -> list[dict]:
    return [dataclasses.asdict(r) for r in runs]


def leer_runs(datos: list[dict]) -> list[Run]:
    return [Run(**{**d, "warnings": [Warning(**w) for w in d["warnings"]]}) for d in datos]


# ── el workflow ─────────────────────────────────────────────────────────────
FORMAS = ("recto", "guarda", "llamada", "bucle")


def muestra(verdad: dict) -> list[str]:
    """Un caso por contenedor, etiqueta, garantía y handle sostenido, rotando la forma.

    Cubre los diez contenedores, las tres etiquetas, las garantías y las tres
    categorías de handle en una fracción del banco (verificar.sh)."""
    grupos: dict[tuple, list[str]] = {}
    for k in sorted(verdad):
        v = verdad[k]
        grupos.setdefault((v["contenedor"], v["esperado"], v["garantia"], v["sostiene"]), []).append(k)
    elegidos = []
    for i, (_, casos) in enumerate(sorted(grupos.items())):
        forma = FORMAS[i % len(FORMAS)]
        elegidos.append(next((c for c in casos if verdad[c]["forma"] == forma), casos[0]))
    return elegidos


def main() -> int:
    global SALIDA
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=os.cpu_count())
    ap.add_argument("--solo", nargs="*", help="limitar a estos casos (depuración)")
    ap.add_argument("--muestra", action="store_true", help="un caso por grupo del banco (verificación rápida)")
    ap.add_argument("--salida", type=Path, help=f"carpeta de salida (por omisión {SALIDA})")
    args = ap.parse_args()
    parcial = bool(args.solo or args.muestra)
    if args.salida:
        SALIDA = args.salida

    meta = verificar()
    verdad = json.loads(VERDAD.read_text())
    fs, rango, src = firmas(), rangos(), BANCO.read_text().splitlines()
    casos = args.solo or (muestra(verdad) if args.muestra else list(verdad))
    faltan = [c for c in casos if c not in fs or c not in rango]
    if faltan:
        sys.exit(f"sin firma o sin rango en corpus.cpp: {faltan[:5]}")

    trabajos = [(c, cond) for cond in CONDICIONES for c in casos]
    t0 = time.time()
    with tempfile.TemporaryDirectory() as d, ThreadPoolExecutor(max_workers=args.jobs) as pool:
        res = list(pool.map(lambda t: ejecutar(t[0], fs[t[0]], t[1], Path(d)), trabajos))
    meta["segundos_total"] = round(time.time() - t0, 1)

    runs, matches, no_atribuidos = [], [], []
    for run, doc in res:
        if doc is not None:
            run.warnings = normalizar(doc)
        caso = verdad[run.case]
        dentro, fuera = atribuir(run.case, run.warnings, rango, src, caso)
        no_atribuidos += [{"case": run.case, "condicion": run.condicion, **dataclasses.asdict(w)}
                          for w in fuera]
        runs.append(run)
        matches.append(cotejar(run.case, caso, run, dentro))

    # Ley «cada caso recibe exactamente un veredicto por condición».
    for cond in CONDICIONES:
        assert sum(m.condicion == cond.nombre for m in matches) == len(casos), cond.nombre
    # Ley «ida y vuelta de los resultados».
    assert leer_runs(json.loads(json.dumps(escribir_runs(runs)))) == runs

    metr = {cond.nombre: agregar([m for m in matches if m.condicion == cond.nombre], verdad)
            for cond in CONDICIONES}
    tiempos = {cond.nombre: {"segundos": round(sum(r.segundos for r in runs if r.condicion == cond.nombre), 1),
                             "outcomes": {o: sum(r.outcome == o for r in runs if r.condicion == cond.nombre)
                                          for o in OUTCOMES}}
               for cond in CONDICIONES}

    SALIDA.mkdir(parents=True, exist_ok=True)
    (SALIDA / "ejecucion.json").write_text(json.dumps(
        {"meta": meta, "tiempos": tiempos, "runs": escribir_runs(runs)}, indent=1, ensure_ascii=False))
    (SALIDA / "cotejo.json").write_text(json.dumps(
        {"matches": [dataclasses.asdict(m) for m in matches],
         "no_atribuidos": no_atribuidos}, indent=1, ensure_ascii=False))
    (SALIDA / "metricas.json").write_text(json.dumps(
        {"meta": meta, "tiempos": tiempos, "metricas": metr}, indent=1, ensure_ascii=False))

    pct = lambda x: "—" if x is None else f"{100 * x:.1f}%"
    print(f"{len(casos)} casos × {len(CONDICIONES)} condiciones en {meta['segundos_total']} s")
    for nombre, m in metr.items():
        a = m["All"]
        print(f"  {nombre:36} TP {a['tp']:3} FN {a['fn']:3} FP {a['fp']:2} TN {a['tn']:3} "
              f"POLICY {a['policyWarned']:3}/{a['policyWarned'] + a['policySilent']:3} "
              f"inc {a['incidents']} | cob {pct(a['recall'])} prec {pct(a['precision'])} "
              f"sostenido {pct(a['recallSostenido'])} | pos/UB {a['posiblesSobreUB']} pos/SAFE {a['posiblesSobreSAFE']}")
    print(f"  avisos fuera de los casos: {len(no_atribuidos)}")
    if parcial:
        return 0

    # Vistas por caso que lee bench/gen_book.py: la referencia y el plugin.
    por = lambda nombre: {m.case: m for m in matches if m.condicion == nombre}
    ref, plug = por("Reference"), por("Experimental-Possibly")
    avisa = lambda m: m.verdict in ("TP", "FP", "PolicyWarned")
    (RAIZ / "test" / "corpus_results.json").write_text(json.dumps(
        [dict(fn=k, avisa=avisa(ref[k]), en_sostenido=ref[k].en_sostenido, veredicto=ref[k].verdict,
              plugin=plug[k].verdict, plugin_avisa=avisa(plug[k]), **verdad[k]) for k in casos], indent=1))
    (RAIZ / "test" / "corpus_fallos.json").write_text(json.dumps(
        [dict(fn=k, **verdad[k], causa=causa(verdad[k])) for k in casos if ref[k].verdict == "FN"], indent=1))

    return 0


if __name__ == "__main__":
    sys.exit(main())
