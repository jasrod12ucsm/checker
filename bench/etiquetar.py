#!/usr/bin/env python3
"""La etiqueta de un caso del banco, calculada desde norma/matriz.json.

Implementación de referencia en Python de las leyes de la Evaluación
(libro/diseno/dsl/evaluacion.md §5). El núcleo C++ es la otra implementación:
plugin/tests/dominio compara las dos celda por celda.

  - «la etiqueta sale de la norma»: efecto de la mutación sobre un handle en
    el PRIMER elemento, en la relación que da la geometría del punto.
  - Si la geometría deja varias relaciones con efectos distintos: POLICY.
  - «la etiqueta es el JOIN de sus handles»: en bucle cuenta también el
    iterador de control.
  - Con garantía (reserve(c.size() + k), k ≥ 1): un DependsOn de capacidad o
    rehash en una inserción de un elemento es Preserves.
"""
from __future__ import annotations

import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CORTO = {"vector": "vector", "deque": "deque", "list": "list", "flist": "forward_list", "set": "set",
         "mset": "multiset", "map": "map", "mmap": "multimap", "uset": "unordered_set",
         "umap": "unordered_map"}
ORDEN = ["SAFE", "POLICY", "UB"]
LABEL = {"preserves": "SAFE", "depends": "POLICY", "invalidates": "UB"}


def cargar(path: Path = RAIZ / "norma" / "matriz.json") -> dict[tuple[str, str], dict]:
    """(contenedor del banco, par del banco) → mutación de la norma."""
    inverso = {v: k for k, v in CORTO.items()}
    idx = {}
    for m in json.loads(path.read_text(encoding="utf-8"))["mutaciones"]:
        for par in m["banco"]:
            idx[(inverso[m["contenedor"]], par)] = m
    return idx


def relaciones(m: dict) -> set[str]:
    """Geometría: relaciones posibles de First+0 frente al punto del banco."""
    p = m["punto"]
    if any(r["relacion"] == "any" for r in m["reglas"]):
        return {"any"}
    if p == "front":
        return {"same"}
    if p == "back":
        return {"before", "same"} if m["crecimiento"] == "shrinks" else {"before"}
    if p == "interior":
        return {"before"}  # el banco inserta/borra en begin() + 1
    return {"before", "same", "after"}  # by_key: no se sabe dónde cae


def efecto(m: dict, cat: str, credito: bool) -> str:
    cat = "reference" if cat in ("ref", "ptr", "reference") else "iterator"
    reglas = [r for r in m["reglas"] if r["categoria"] == cat and r["relacion"] in relaciones(m)]
    efs = set()
    for r in reglas:
        e = r["efecto"]
        if (e == "depends" and credito and m["crecimiento"] == "one"
                and r.get("condicion") in ("capacity_reached", "rehash_triggered")):
            e = "preserves"
        efs.add(e)
    if len(efs) > 1:
        return "depends"  # la relación decide: POLICY
    return efs.pop()


def join(*labels: str) -> str:
    return max(labels, key=ORDEN.index)


def por_handle(m: dict, sostiene: str, forma: str, credito: bool = False) -> dict:
    """La etiqueta de cada handle del caso. El cotejo por sitio la necesita: un
    aviso acierta sólo si cae sobre un handle que la norma da por inválido.
    En bucle con iterador, el sostenido ES el de control."""
    h = {"sostenido": LABEL[efecto(m, sostiene, credito)], "control": None}
    if forma == "bucle" and sostiene != "it":
        h["control"] = LABEL[efecto(m, "it", credito)]
    return h


def etiqueta(m: dict, sostiene: str, forma: str, credito: bool = False) -> str:
    return join(*(l for l in por_handle(m, sostiene, forma, credito).values() if l))


def depende_de_capacidad(m: dict) -> bool:
    """¿Un reserve(c.size() + k) puede convertir esta mutación en segura?"""
    return m["crecimiento"] == "one" and any(
        r.get("condicion") in ("capacity_reached", "rehash_triggered") for r in m["reglas"])
