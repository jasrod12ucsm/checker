#!/usr/bin/env python3
"""Figuras del capítulo V de la tesis y prueba de Wilcoxon del costo.

Lee los registros del repositorio (no ejecuta clang), comprueba que cada cifra coincida con la
que publica la tesis y escribe bench/tesis/fig/png/f5-*.png. Además escribe
test/experimento/costo.json con la prueba de Wilcoxon de rangos con signo y la de Shapiro-Wilk
sobre los tiempos pareados por caso.

Estilo APA 7: sin título dentro de la imagen (el número y el título van en el documento),
ejes rotulados con su unidad, leyenda dentro de la figura, fuente sin serifa, decimales con coma.

Requiere matplotlib y scipy:
  python3 bench/tesis/graficos.py
"""
from __future__ import annotations

import json
import math
import random
import statistics as st
import sys
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402
from scipy import stats  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "bench"))
import analisis_estadistico as A  # noqa: E402

SALIDA = RAIZ / "bench/tesis/fig/png"
EXP = RAIZ / "test/experimento"
ANCHO = 6.25  # pulgadas: el ancho útil de la página de la tesis

# Paleta categórica validada (dataviz/validate_palette.js): B y C conservan su color en todas las figuras.
AZUL, NARANJA, AGUA, VIOLETA = "#2a78d6", "#eb6834", "#1baf7a", "#6250d6"
TINTA, TINTA2, REJILLA = "#0b0b0b", "#52514e", "#dcdcd8"

plt.rcParams.update({
    "font.family": "Liberation Sans", "font.size": 10, "axes.labelsize": 10, "xtick.labelsize": 9,
    "ytick.labelsize": 9, "legend.fontsize": 9, "axes.edgecolor": TINTA2, "axes.labelcolor": TINTA,
    "xtick.color": TINTA2, "ytick.color": TINTA2, "text.color": TINTA, "axes.spines.top": False,
    "axes.spines.right": False, "axes.grid": True, "axes.grid.axis": "y", "grid.color": REJILLA,
    "grid.linewidth": 0.6, "axes.axisbelow": True, "legend.frameon": False, "savefig.dpi": 300,
    "hatch.linewidth": 0.6, "hatch.color": "white",
})


def coma(x: float, dec: int = 1) -> str:
    return f"{x:,.{dec}f}".replace(",", " ").replace(".", ",")


def pct(a: int, n: int) -> float:
    return 100 * a / n


def eje_pct(ax, eje="y"):
    f = FuncFormatter(lambda v, _: f"{coma(v, 0)} %")
    (ax.yaxis if eje == "y" else ax.xaxis).set_major_formatter(f)


def guardar(fig, nombre: str) -> None:
    fig.savefig(SALIDA / f"{nombre}.png", facecolor="white", bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    print(f"  {nombre}.png")


def barras(ax, xs, series, etiquetas, colores, texto, ancho=0.8, tramas=None):
    """Barras agrupadas con el valor sobre cada una; tramas para leerlas en blanco y negro."""
    k = len(series)
    w = ancho / k
    for j, (vals, et, col) in enumerate(zip(series, etiquetas, colores)):
        pos = [x - ancho / 2 + w * (j + 0.5) for x in xs]
        h = tramas[j] if tramas else None
        bs = ax.bar(pos, vals, w * 0.92, color=col, label=et, hatch=h, edgecolor="white", linewidth=0.6)
        for b, t in zip(bs, texto[j]):
            ax.annotate(t, (b.get_x() + b.get_width() / 2, b.get_height()), xytext=(0, 2),
                        textcoords="offset points", ha="center", va="bottom", fontsize=7.5, color=TINTA)


# ── datos ───────────────────────────────────────────────────────────────────
VERDAD = json.loads((RAIZ / "test/corpus_truth.json").read_text())
POR: dict[str, dict[str, str]] = {c: {} for c in A.CONDICIONES}
for m in json.loads((EXP / "cotejo.json").read_text())["matches"]:
    POR[m["condicion"]][m["case"]] = m["verdict"]
UB = sorted(k for k, v in VERDAD.items() if v["esperado"] == "UB")
SAFE = sorted(k for k, v in VERDAD.items() if v["esperado"] == "SAFE")
B, C, CP = "Reference", "Experimental-Silent", "Experimental-Possibly"
HANDLES = [("it", "Iterador"), ("ref", "Referencia"), ("ptr", "Puntero")]
FORMAS = [("recto", "Recta"), ("guarda", "Con guarda"), ("bucle", "Bucle"), ("llamada", "Con llamada")]
CONTENEDORES = [("vector", "vector"), ("deque", "deque"), ("list", "list"), ("flist", "forward_list"),
                ("set", "set"), ("mset", "multiset"), ("map", "map"), ("mmap", "multimap"),
                ("uset", "unordered_set"), ("umap", "unordered_map")]


def detectados(cond: str, campo: str, valor: str) -> tuple[int, int]:
    casos = [k for k in UB if VERDAD[k][campo] == valor]
    return sum(POR[cond][k] == "TP" for k in casos), len(casos)


# ── 5.1 validación dinámica ─────────────────────────────────────────────────
def f_validacion() -> None:
    res = json.loads((RAIZ / "test/runtime_validation_results.json").read_text())["resultados"]
    ub = [r for r in res if r["etiqueta_normativa"] == "UB"]
    det = lambda r, h: r[h]["estado"] == "DETECTADO"
    filas = []
    for h, _ in HANDLES:
        rs = [r for r in ub if r["sostiene"] == h]
        filas.append((len(rs), sum(det(r, "libstdcxx_debug") for r in rs), sum(det(r, "asan_ubsan") for r in rs),
                      sum(det(r, "libstdcxx_debug") or det(r, "asan_ubsan") for r in rs)))
    assert filas == [(128, 116, 69, 116), (107, 29, 69, 80), (107, 29, 69, 80)], filas
    fig, ax = plt.subplots(figsize=(ANCHO, 3.0))
    xs = range(3)
    series = [[pct(f[i], f[0]) for f in filas] for i in (1, 2, 3)]
    texto = [[f"{f[i]}" for f in filas] for i in (1, 2, 3)]
    barras(ax, xs, series, ["libstdc++ Debug", "ASan y UBSan", "Alguna herramienta"], [AZUL, NARANJA, AGUA], texto,
           tramas=[None, "///", None])
    ax.set_xticks(list(xs), [f"{e}\n(n = {f[0]})" for (_, e), f in zip(HANDLES, filas)])
    ax.set_ylabel("Casos UB con defecto observado")
    ax.set_ylim(0, 110)
    ax.set_yticks(range(0, 101, 20))
    eje_pct(ax)
    ax.legend(loc="upper right", ncol=3, bbox_to_anchor=(1, 1.1))
    guardar(fig, "f5-validacion")


# ── 5.2 línea base ──────────────────────────────────────────────────────────
def f_causas() -> None:
    fallos = json.loads((RAIZ / "test/corpus_fallos.json").read_text())
    n = Counter(f["causa"][0] for f in fallos)
    assert [n[c] for c in "1234"] == [182, 32, 33, 15] and len(fallos) == 262, n
    nombres = ["1. Referencias y punteros\nno modelados", "2. Sin comparación previa\ncontra end()",
               "3. El borrado no alcanza\nla posición", "4. La inserción o realocación\nno alcanza la posición"]
    vals = [n[c] for c in "1234"]
    fig, ax = plt.subplots(figsize=(ANCHO, 2.6))
    ys = list(range(4))[::-1]
    bs = ax.barh(ys, vals, 0.62, color=AZUL)
    for b, v in zip(bs, vals):
        ax.annotate(f"{v} ({coma(pct(v, 262))} %)", (v, b.get_y() + b.get_height() / 2), xytext=(4, 0),
                    textcoords="offset points", va="center", fontsize=8.5)
    ax.set_yticks(ys, nombres)
    ax.set_xlabel("Omisiones de la configuración B (n = 262)")
    ax.set_xlim(0, 220)
    ax.grid(axis="x")
    ax.grid(axis="y", visible=False)
    guardar(fig, "f5-causas")


def f_base_contenedor() -> None:
    d = [detectados(B, "contenedor", c) for c, _ in CONTENEDORES]
    assert d == [(10, 48), (30, 72), (5, 36), (5, 24), (5, 24), (5, 24), (5, 24), (5, 24), (5, 36), (5, 30)], d
    fig, ax = plt.subplots(figsize=(ANCHO, 2.9))
    xs = range(len(d))
    bs = ax.bar(xs, [pct(a, n) for a, n in d], 0.62, color=AZUL)
    for b, (a, n) in zip(bs, d):
        ax.annotate(f"{a}/{n}", (b.get_x() + b.get_width() / 2, b.get_height()), xytext=(0, 2),
                    textcoords="offset points", ha="center", fontsize=8)
    ax.set_xticks(list(xs), [e for _, e in CONTENEDORES], rotation=35, ha="right")
    ax.set_ylabel("Casos UB detectados por B")
    ax.set_ylim(0, 50)
    eje_pct(ax)
    guardar(fig, "f5-base-contenedor")


# ── 5.4 política ────────────────────────────────────────────────────────────
def f_politica() -> None:
    pol = [k for k, v in VERDAD.items() if v["esperado"] == "POLICY"]
    seg = [k for k in SAFE if VERDAD[k]["garantia"] == "ninguna"]
    gar = [k for k in SAFE if VERDAD[k]["garantia"] != "ninguna"]
    grupos = [("POLICY", pol, "PolicyWarned"), ("SAFE de la matriz", seg, "FP"), ("Buen uso con garantía", gar, "FP")]
    cot = {(m["condicion"], m["case"]): m for m in json.loads((EXP / "cotejo.json").read_text())["matches"]}
    def con_aviso(cond, casos):
        return sum(cot[(cond, k)]["posibles"] > 0 for k in casos)
    vs = [[con_aviso(c, g[1]) for g in grupos] for c in (C, CP)]
    assert vs == [[0, 0, 0], [102, 0, 0]] and [len(g[1]) for g in grupos] == [102, 240, 66], vs
    fig, ax = plt.subplots(figsize=(ANCHO, 2.8))
    xs = range(3)
    barras(ax, xs, vs, ["C-Silent", "C-Possibly"], [AGUA, VIOLETA], [[str(v) for v in s] for s in vs],
           ancho=0.6, tramas=["///", None])
    ax.set_xticks(list(xs), [f"{g[0]}\n(n = {len(g[1])})" for g in grupos])
    ax.set_ylabel("Casos con algún aviso posible")
    ax.set_ylim(0, 120)
    ax.legend(loc="upper right")
    guardar(fig, "f5-politica")


# ── 5.5 comparación ─────────────────────────────────────────────────────────
def f_condiciones() -> None:
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(ANCHO, 3.1), gridspec_kw={"width_ratios": [3, 4]}, sharey=True)
    for ax, grupos, campo, letra in ((a1, HANDLES, "sostiene", "a"), (a2, FORMAS, "forma", "b")):
        db = [detectados(B, campo, g) for g, _ in grupos]
        dc = [detectados(C, campo, g) for g, _ in grupos]
        assert all(a == n for a, n in dc)
        xs = range(len(grupos))
        barras(ax, xs, [[pct(a, n) for a, n in db], [pct(a, n) for a, n in dc]], ["B", "C"], [AZUL, NARANJA],
               [[str(a) for a, _ in db], [str(a) for a, _ in dc]], ancho=0.74, tramas=["///", None])
        ax.set_xticks(list(xs), [f"{e}\n(n = {n})" for (_, e), (_, n) in zip(grupos, db)], fontsize=8.5)
        ax.set_title(f"({letra}) Por {'clase de handle' if letra == 'a' else 'forma sintáctica'}",
                     fontsize=9.5, loc="left", fontstyle="italic")
        ax.set_ylim(0, 115)
        ax.set_yticks(range(0, 101, 20))
    assert [detectados(B, "sostiene", h)[0] for h, _ in HANDLES] == [48, 16, 16]
    assert [detectados(B, "forma", f)[0] for f, _ in FORMAS] == [0, 16, 48, 16]
    a1.set_ylabel("Casos UB detectados")
    eje_pct(a1)
    fig.tight_layout(w_pad=1.2, rect=(0, 0, 1, 0.92))
    h, l = a2.get_legend_handles_labels()
    fig.legend(h, l, loc="upper center", ncol=2, bbox_to_anchor=(0.5, 1.0))
    guardar(fig, "f5-condiciones")


def f_bootstrap() -> None:
    azar = random.Random(A.SEMILLA)
    def f(cond, u, s):
        tp = sum(POR[cond][k] == "TP" for k in u)
        return A.f1(tp, sum(POR[cond][k] == "FP" for k in s), sum(POR[cond][k] == "FN" for k in u))
    d = sorted(f(C, u, s) - f(B, u, s) for u, s in
               ((azar.choices(UB, k=len(UB)), azar.choices(SAFE, k=len(SAFE))) for _ in range(A.REPLICAS)))
    obs = f(C, UB, SAFE) - f(B, UB, SAFE)
    ic = [d[int(0.025 * A.REPLICAS)], d[int(0.975 * A.REPLICAS) - 1]]
    pub = json.loads((EXP / "contraste.json").read_text())["bootstrap"]
    assert math.isclose(obs, pub["dF1"]) and all(math.isclose(a, b) for a, b in zip(ic, pub["ic95"])), (obs, ic)
    fig, ax = plt.subplots(figsize=(ANCHO, 2.9))
    paso = 0.005
    ax.hist(d, bins=[0.52 + paso * i for i in range(41)], color=AZUL, edgecolor="white", linewidth=0.5)
    for x, estilo in ((ic[0], (0, (4, 3))), (ic[1], (0, (4, 3))), (obs, "solid")):
        ax.axvline(x, color=TINTA, linewidth=1.1, linestyle=estilo)
    top = ax.get_ylim()[1] * 1.2
    ax.set_ylim(0, top)
    ax.annotate(f"Límite inferior\n{coma(ic[0], 3)}", (ic[0], top * 0.97), xytext=(-4, 0), textcoords="offset points",
                ha="right", va="top", fontsize=8)
    ax.annotate(f"Límite superior\n{coma(ic[1], 3)}", (ic[1], top * 0.97), xytext=(4, 0), textcoords="offset points",
                ha="left", va="top", fontsize=8)
    ax.annotate(f"Observado\n{coma(obs, 3)}", (obs, top * 0.97), xytext=(4, 0), textcoords="offset points",
                ha="left", va="top", fontsize=8)
    ax.set_xlabel("ΔF1 (C − B) en cada réplica")
    ax.set_ylabel("Frecuencia")
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: coma(v, 2)))
    ax.set_xlim(0.52, 0.72)
    ax.set_xticks([0.52 + 0.02 * i for i in range(11)])
    guardar(fig, "f5-bootstrap")


def costo() -> None:
    runs = json.loads((EXP / "ejecucion.json").read_text())["runs"]
    t = {c: {r["case"]: r["segundos"] for r in runs if r["condicion"] == c and r["outcome"] == "Completed"}
         for c in (B, CP)}
    ks = sorted(t[B])
    assert ks == sorted(t[CP]) and len(ks) == 750
    a, b = [t[B][k] for k in ks], [t[CP][k] for k in ks]
    dif = [y - x for x, y in zip(a, b)]
    w = stats.wilcoxon(b, a, zero_method="wilcox", method="approx")
    n = sum(x != 0 for x in dif)
    sw = stats.shapiro(dif)
    res = {"base": B, "con": CP, "casos": 750, "diferencias_no_nulas": n,
           "mediana_base_s": st.median(a), "mediana_con_s": st.median(b), "mediana_diferencia_s": st.median(dif),
           "wilcoxon": {"W": float(w.statistic), "z": float(w.zstatistic), "p": float(w.pvalue),
                        "r": abs(float(w.zstatistic)) / math.sqrt(n), "metodo": "aproximación normal, ceros excluidos"},
           "shapiro_diferencias": {"W": float(sw.statistic), "p": float(sw.pvalue)},
           "scipy": __import__("scipy").__version__}
    (EXP / "costo.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
    assert (round(res["mediana_base_s"], 3), round(res["mediana_con_s"], 3)) == (0.650, 0.652)
    fig, ax = plt.subplots(figsize=(ANCHO, 2.9))
    bp = ax.boxplot([a, b], orientation="horizontal", widths=0.5, patch_artist=True, showfliers=True,
                    medianprops={"color": TINTA, "linewidth": 1.4},
                    flierprops={"marker": "o", "markersize": 2.5, "markerfacecolor": TINTA2, "markeredgecolor": "none"})
    for caja, col, h in zip(bp["boxes"], (AZUL, NARANJA), ("///", None)):
        caja.set(facecolor=col, edgecolor=TINTA2, hatch=h, alpha=0.9)
    ax.set_yticks([1, 2], ["B\n(n = 750)", "C-Possibly\n(n = 750)"])
    ax.set_xlabel("Tiempo de análisis por caso (s)")
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: coma(v, 2)))
    ax.grid(axis="x")
    ax.grid(axis="y", visible=False)
    guardar(fig, "f5-tiempo")
    print(f"  Wilcoxon W = {w.statistic}, z = {w.zstatistic:.3f}, p = {w.pvalue:.3f}, r = {res['wilcoxon']['r']:.3f}; "
          f"Shapiro W = {sw.statistic:.3f}, p = {sw.pvalue:.2e}")


# ── 5.6 código real ─────────────────────────────────────────────────────────
def f_codigo_real() -> None:
    p = json.loads((RAIZ / "test/codigo_real/avisos.json").read_text())["proyectos"]
    orden = ["ninja", "leveldb", "yaml-cpp", "rocksdb"]
    datos = [[r["segundos"] for r in p[k]["resultados"] if r["codigo"] == 0 and not r["error"]] for k in orden]
    assert [len(x) for x in datos] == [28, 39, 31, 682], [len(x) for x in datos]
    fig, ax = plt.subplots(figsize=(ANCHO, 2.8))
    bp = ax.boxplot(datos[::-1], orientation="horizontal", widths=0.5, patch_artist=True,
                    medianprops={"color": TINTA, "linewidth": 1.4},
                    flierprops={"marker": "o", "markersize": 2.5, "markerfacecolor": TINTA2, "markeredgecolor": "none"})
    for caja in bp["boxes"]:
        caja.set(facecolor=AZUL, edgecolor=TINTA2, alpha=0.9)
    ax.set_yticks(range(1, 5), [f"{k}\n(n = {len(x)})" for k, x in zip(orden[::-1], datos[::-1])])
    ax.set_xscale("log")
    ax.set_xlabel("Tiempo de análisis por unidad (s, escala logarítmica)")
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: coma(v, 2 if v < 1 else 0)))
    ax.grid(axis="x")
    ax.grid(axis="y", visible=False)
    guardar(fig, "f5-codigo-real")
    for k, x in zip(orden, datos):
        print(f"  {k}: mediana {st.median(x):.2f} s, máximo {max(x):.1f} s")


def main() -> int:
    SALIDA.mkdir(parents=True, exist_ok=True)
    for f in (f_validacion, f_causas, f_base_contenedor, f_politica, f_condiciones, f_bootstrap, costo, f_codigo_real):
        f()
    return 0


if __name__ == "__main__":
    sys.exit(main())
