#!/usr/bin/env python3
"""Contraste de la hipótesis de la tesis y hoja de cálculo de resultados.

Lee test/experimento/cotejo.json y test/corpus_truth.json (no ejecuta clang) y escribe:
  test/experimento/contraste.json   prueba exacta de McNemar y bootstrap de ΔF1
  test/experimento/resultados.xlsx  conteos y métricas por condición y por grupo

  python3 bench/analisis_estadistico.py
"""
from __future__ import annotations

import json
import random
import zipfile
from math import comb
from pathlib import Path
from xml.sax.saxutils import escape

RAIZ = Path(__file__).resolve().parent.parent
EXP = RAIZ / "test" / "experimento"
B, C = "Reference", "Experimental-Silent"
CONDICIONES = [B, "Experimental-Silent", "Experimental-Possibly", "Plugin-Possibly"]
REPLICAS, SEMILLA = 10_000, 20261020
GRUPOS = {"Contenedor": "contenedor", "Operación": "op", "Handle": "sostiene", "Forma": "forma"}


def mcnemar_exacta(b: int, c: int) -> float:
    """Valor p bilateral: bajo H0, b ~ Binomial(b + c, 0,5)."""
    n = b + c
    if n == 0:
        return 1.0
    return min(1.0, 2 * sum(comb(n, k) for k in range(min(b, c) + 1)) / 2 ** n)


def f1(tp: int, fp: int, fn: int) -> float:
    return 2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else 0.0


def razon(a: int, d: int) -> float | None:
    return a / d if d else None


def conteos(verdictos: list[str]) -> dict:
    n = {v: verdictos.count(v) for v in ("TP", "FP", "FN", "TN", "PolicyWarned", "PolicySilent", "Incident")}
    return {**n, "precision": razon(n["TP"], n["TP"] + n["FP"]), "exhaustividad": razon(n["TP"], n["TP"] + n["FN"]),
            "f1": f1(n["TP"], n["FP"], n["FN"])}


def pares(casos: list[str], por: dict, correcto: str) -> dict:
    """b: C acierta y B no; c: B acierta y C no."""
    b = sum(por[C][k] == correcto and por[B][k] != correcto for k in casos)
    c = sum(por[B][k] == correcto and por[C][k] != correcto for k in casos)
    return {"casos": len(casos), "b": b, "c": c, "p": mcnemar_exacta(b, c),
            "proporcion_discordantes": (b + c) / len(casos) if casos else 0.0}


def bootstrap(ub: list[str], safe: list[str], por: dict) -> dict:
    """IC 95 % de ΔF1 por percentiles, remuestreando casos dentro de cada etiqueta."""
    azar = random.Random(SEMILLA)
    def delta(u: list[str], s: list[str]) -> float:
        def f(cond: str) -> float:
            tp = sum(por[cond][k] == "TP" for k in u)
            return f1(tp, sum(por[cond][k] == "FP" for k in s), sum(por[cond][k] == "FN" for k in u))
        return f(C) - f(B)
    d = sorted(delta(azar.choices(ub, k=len(ub)), azar.choices(safe, k=len(safe))) for _ in range(REPLICAS))
    return {"replicas": REPLICAS, "semilla": SEMILLA, "dF1": delta(ub, safe),
            "ic95": [d[int(0.025 * REPLICAS)], d[int(0.975 * REPLICAS) - 1]]}


# ── xlsx mínimo con la biblioteca estándar: el arnés no tiene dependencias externas ──
def columna(i: int) -> str:
    s = ""
    i += 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


def hoja(filas: list[list]) -> str:
    out = []
    for f, fila in enumerate(filas, 1):
        cel = []
        for c, v in enumerate(fila):
            ref = f"{columna(c)}{f}"
            if v is None:
                continue
            if isinstance(v, (int, float)):
                cel.append(f'<c r="{ref}"><v>{v}</v></c>')
            else:
                cel.append(f'<c r="{ref}" t="inlineStr"><is><t>{escape(str(v))}</t></is></c>')
        out.append(f'<row r="{f}">{"".join(cel)}</row>')
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><worksheet xmlns="http://schemas.openxmlformats.org/'
            f'spreadsheetml/2006/main"><sheetData>{"".join(out)}</sheetData></worksheet>')


def escribir_xlsx(ruta: Path, hojas: dict[str, list[list]]) -> None:
    ns = "http://schemas.openxmlformats.org/"
    with zipfile.ZipFile(ruta, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml",
                   f'<?xml version="1.0" encoding="UTF-8"?><Types xmlns="{ns}package/2006/content-types">'
                   '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                   '<Default Extension="xml" ContentType="application/xml"/>'
                   '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
                   + "".join(f'<Override PartName="/xl/worksheets/s{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
                             for i in range(1, len(hojas) + 1)) + "</Types>")
        z.writestr("_rels/.rels", f'<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="{ns}package/2006/relationships">'
                   f'<Relationship Id="r1" Type="{ns}officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>')
        z.writestr("xl/workbook.xml", f'<?xml version="1.0" encoding="UTF-8"?><workbook xmlns="{ns}spreadsheetml/2006/main" '
                   f'xmlns:r="{ns}officeDocument/2006/relationships"><sheets>'
                   + "".join(f'<sheet name="{escape(n)}" sheetId="{i}" r:id="r{i}"/>' for i, n in enumerate(hojas, 1))
                   + "</sheets></workbook>")
        z.writestr("xl/_rels/workbook.xml.rels", f'<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="{ns}package/2006/relationships">'
                   + "".join(f'<Relationship Id="r{i}" Type="{ns}officeDocument/2006/relationships/worksheet" Target="worksheets/s{i}.xml"/>'
                             for i in range(1, len(hojas) + 1)) + "</Relationships>")
        for i, filas in enumerate(hojas.values(), 1):
            z.writestr(f"xl/worksheets/s{i}.xml", hoja(filas))


def main() -> int:
    verdad = json.loads((RAIZ / "test" / "corpus_truth.json").read_text())
    por: dict[str, dict[str, str]] = {c: {} for c in CONDICIONES}
    for m in json.loads((EXP / "cotejo.json").read_text())["matches"]:
        por[m["condicion"]][m["case"]] = m["verdict"]
    ub = sorted(k for k, v in verdad.items() if v["esperado"] == "UB")
    safe = sorted(k for k, v in verdad.items() if v["esperado"] == "SAFE")
    # La política no debe cambiar los avisos confirmados (sección 4.7 de la tesis).
    igual = all(por["Experimental-Silent"][k] == por["Experimental-Possibly"][k] for k in ub + safe)
    contraste = {"B": B, "C": C, "confirmados_iguales_entre_politicas": igual,
                 "metricas": {c: conteos([por[c][k] for k in verdad]) for c in CONDICIONES},
                 "mcnemar": {"UB": pares(ub, por, "TP"), "SAFE": pares(safe, por, "TN")},
                 "bootstrap": bootstrap(ub, safe, por)}
    (EXP / "contraste.json").write_text(json.dumps(contraste, indent=1, ensure_ascii=False))

    cab = ["Grupo", "Valor", "Condición", "VP", "FP", "FN", "VN", "POLICY con aviso", "POLICY sin aviso", "Incidentes",
           "Precisión", "Exhaustividad", "F1"]
    def fila(g: str, v: str, c: str, casos: list[str]) -> list:
        n = conteos([por[c][k] for k in casos])
        return [g, v, c, n["TP"], n["FP"], n["FN"], n["TN"], n["PolicyWarned"], n["PolicySilent"], n["Incident"],
                n["precision"], n["exhaustividad"], n["f1"]]
    hojas = {"Por condición": [cab] + [fila("Banco", "Todos", c, list(verdad)) for c in CONDICIONES]}
    for nombre, campo in GRUPOS.items():
        valores = sorted({v[campo] for v in verdad.values()})
        hojas[nombre] = [cab] + [fila(nombre, x, c, [k for k, v in verdad.items() if v[campo] == x])
                                 for x in valores for c in CONDICIONES]
    hojas["Contraste"] = [["Prueba", "Casos", "b (C acierta, B no)", "c (B acierta, C no)", "p exacto", "Proporción discordante"]] + [
        [f"McNemar {e}", d["casos"], d["b"], d["c"], d["p"], d["proporcion_discordantes"]] for e, d in contraste["mcnemar"].items()]
    hojas["Contraste"] += [[], ["ΔF1", contraste["bootstrap"]["dF1"]], ["IC 95 % inferior", contraste["bootstrap"]["ic95"][0]],
                           ["IC 95 % superior", contraste["bootstrap"]["ic95"][1]], ["Réplicas", REPLICAS]]
    escribir_xlsx(EXP / "resultados.xlsx", hojas)
    print(json.dumps({k: contraste[k] for k in ("confirmados_iguales_entre_politicas", "mcnemar", "bootstrap")}, ensure_ascii=False))
    print({c: {k: contraste["metricas"][c][k] for k in ("TP", "FP", "FN", "TN", "Incident", "f1")} for c in CONDICIONES})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
