#!/usr/bin/env python3
"""matriz.json + corpus_truth.json → BancoCasos.inc (prueba «la etiqueta sale de la norma»).

Una fila por celda del banco (contenedor, op, sostén) en formas sin bucle: la
mutación de la norma, dónde cae su punto, y la etiqueta esperada.
"""
import json, sys
matriz, truth, salida = sys.argv[1:4]
CORTO = {"vector": "vector", "deque": "deque", "list": "list", "flist": "forward_list", "set": "set",
         "mset": "multiset", "map": "map", "mmap": "multimap", "uset": "unordered_set", "umap": "unordered_map"}
camel = lambda s: "".join(p.capitalize() for p in s.split("_"))
idx = {(m["contenedor"], b): m for m in json.load(open(matriz))["mutaciones"] for b in m["banco"]}
celdas = {}
for t in json.load(open(truth)).values():
    if t["forma"] == "bucle":
        continue
    if t["garantia"] == "devuelto":
        continue  # no es una sola mutación sobre el handle: lo prueban lit y el banco
    celdas[(t["contenedor"], t["op"], t["sostiene"], t["garantia"])] = t["esperado"]
L = ["// GENERADO por gen_casos_banco.py — no editar"]
for (cn, op, hk, g), lab in sorted(celdas.items()):
    m = idx[(CORTO[cn], op)]
    p = m["punto"]
    pos = {"front": "Position::first(0)", "interior": "Position::first(1)",
           "back": "Position::last(0)" if m["crecimiento"] == "shrinks" else "Position::pastEnd()"
           }.get(p, "Position::unknown()")
    kind = "HandleKind::IteratorObject" if hk == "it" else "HandleKind::Element"
    cat = {"it": "Iterator", "ref": "Reference", "ptr": "Pointer"}[hk]
    credit = "Credit(1u)" if g == "reserva" else "Credit(std::nullopt)"
    L.append(f'{{"{cn}.{op}.{hk}.{g}", {{ContainerKind::{camel(m["contenedor"])}, Operation::{camel(m["operacion"])}, '
             f'Point::{camel(p)}}}, {pos}, {kind}, HandleCategory::{cat}, {credit}, Label::{lab.capitalize()}}},')
open(salida, "w").write("\n".join(L) + "\n")
