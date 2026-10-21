#!/usr/bin/env python3
"""Leyes de la Evaluación (libro/diseno/dsl/evaluacion.md §5) sobre el arnés.

Sin clang: prueban el cotejo y los conteos con datos escritos a mano.
  python3 bench/pruebas_evaluacion.py
"""
import dataclasses
import json
import random

from etiquetar import cargar, etiqueta, join, por_handle
from experimento import (Counts, Match, Run, Warning, agregar, cotejar, escribir_runs, leer_runs,
                         metricas, normalizar)

UB_REF_BUCLE = {"contenedor": "vector", "op": "erase_begin", "sostiene": "ref", "forma": "bucle",
                "esperado": "UB", "garantia": "ninguna",
                "handles": {"sostenido": "UB", "control": "UB"}}
UB_SOLO_CONTROL = {**UB_REF_BUCLE, "esperado": "UB", "handles": {"sostenido": "SAFE", "control": "UB"}}
SAFE = {**UB_REF_BUCLE, "forma": "recto", "esperado": "SAFE",
        "handles": {"sostenido": "SAFE", "control": None}}
POLICY = {**SAFE, "esperado": "POLICY", "handles": {"sostenido": "POLICY", "control": None}}

ok = lambda: Run("f", "Experimental-Possibly", "Completed", 1.0, 1)
conf = Warning(10, 5, "ucsm.ContainerInvalidation", "Confirmed", "Uso de una referencia invalidada")
pos = Warning(10, 5, "ucsm.ContainerInvalidation", "Possible", "Uso de una referencia posiblemente invalidada")
csa = Warning(8, 60, "alpha.cplusplus.InvalidatedIterator", "Confirmed", "Invalidated iterator accessed")


def prueba(nombre):
    def deco(f):
        f()
        print(f"  ok  {nombre}")
        return f
    return deco


@prueba("un fallo nunca es un verdadero negativo")
def _():
    for o in ("CompileError", "Crash", "Timeout", "Unreadable"):
        r = Run("f", "Reference", o, 1.0, 1)
        assert cotejar("f", SAFE, r, []).verdict == "Incident"


@prueba("cotejo por sitio: el aviso sobre el control cuenta si el control es UB")
def _():
    m = cotejar("f", UB_SOLO_CONTROL, ok(), [(csa, "control")])
    assert m.verdict == "TP" and not m.en_sostenido


@prueba("cotejo por sitio: el aviso sobre un handle SAFE no es un acierto")
def _():
    caso = {**UB_REF_BUCLE, "handles": {"sostenido": "UB", "control": "SAFE"}}
    m = cotejar("f", caso, ok(), [(csa, "control")])
    assert m.verdict == "FN" and m.fuera_de_sitio == 1


@prueba("un aviso posible no es un acierto ni un falso positivo")
def _():
    assert cotejar("f", UB_REF_BUCLE, ok(), [(pos, "sostenido")]).verdict == "FN"
    assert cotejar("f", SAFE, ok(), [(pos, "sostenido")]).verdict == "TN"
    assert cotejar("f", POLICY, ok(), [(pos, "sostenido")]).verdict == "PolicyWarned"


@prueba("POLICY no entra en la precisión")
def _():
    a = Counts(tp=3, fp=1)
    assert metricas(a)["precision"] == metricas(a + Counts(policyWarned=9, policySilent=4))["precision"]


@prueba("una métrica sin denominador no es cero")
def _():
    assert metricas(Counts(fn=3))["precision"] is None
    assert metricas(Counts())["recall"] is None


@prueba("los conteos se suman por partes (monoide)")
def _():
    rnd = random.Random(7)
    campos = len(dataclasses.fields(Counts))
    xs = [Counts(*(rnd.randint(0, 9) for _ in range(campos))) for _ in range(30)]
    for a, b, c in zip(xs, xs[1:], xs[2:]):
        assert (a + b) + c == a + (b + c)
        assert a + Counts() == a == Counts() + a


@prueba("los conteos se reconstruyen desde el cotejo")
def _():
    verdad = {"a": UB_REF_BUCLE, "b": SAFE, "c": POLICY}
    ms = [Match("a", "X", "TP", ["sostenido"], True, 0, 0), Match("b", "X", "TN", [], False, 0, 0),
          Match("c", "X", "PolicySilent", [], False, 0, 0)]
    g = agregar(ms, verdad)
    assert (g["All"]["tp"], g["All"]["tn"], g["All"]["policySilent"]) == (1, 1, 1)
    assert sum(v["tp"] + v["tn"] + v["policySilent"] for v in g["esperado"].values()) == 3


@prueba("normalizar dos veces es normalizar una")
def _():
    sarif = {"runs": [{"results": [
        {"ruleId": w.checker, "message": {"text": w.message},
         "locations": [{"physicalLocation": {"region": {"startLine": w.line, "startColumn": w.column}}}]}
        for w in (conf, pos, csa, conf)]}]}
    una = normalizar(sarif)
    assert normalizar(una) == una and len(una) == 3


@prueba("ida y vuelta de los resultados")
def _():
    rs = [Run("f", "Reference", "Completed", 0.5, 100, "", [conf, csa])]
    assert leer_runs(json.loads(json.dumps(escribir_runs(rs)))) == rs


@prueba("la etiqueta es el JOIN de sus handles (matriz completa)")
def _():
    for m in cargar().values():
        for so in ("it", "ref", "ptr"):
            for fo in ("recto", "guarda", "bucle", "llamada"):
                h = por_handle(m, so, fo)
                assert etiqueta(m, so, fo) == join(*(l for l in h.values() if l))
