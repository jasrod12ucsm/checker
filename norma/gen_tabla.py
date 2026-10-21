#!/usr/bin/env python3
"""norma/matriz.json → plugin/dominio/generado/NormTable.inc

Workflow «Generar la tabla» (DSL Norma §6): Parse → CheckTotal → CheckLaws → Render.
Junta TODOS los errores antes de fallar; si la matriz rompe una ley, no se escribe la tabla.

Uso: python3 norma/gen_tabla.py <matriz.json> <salida.inc>   (CMake la llama con build/generado/)
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path

CONTENEDORES = ["vector", "deque", "list", "forward_list", "set", "multiset", "map", "multimap",
                "unordered_set", "unordered_map"]
NODOS = {"list", "forward_list", "set", "multiset", "map", "multimap"}
OPERACIONES = ["push_back", "emplace_back", "push_front", "emplace_front", "insert", "insert_after",
               "emplace", "subscript", "erase", "erase_after", "pop_back", "pop_front", "clear", "assign",
               "resize", "reserve", "shrink_to_fit", "rehash", "reverse", "sort"]
INSERCIONES = {"push_back", "emplace_back", "push_front", "emplace_front", "insert", "insert_after",
               "emplace", "subscript"}
PUNTOS = ["front", "back", "interior", "whole", "by_key"]
CRECIMIENTOS = ["one", "none", "shrinks", "unknown", "reset"]
CATEGORIAS = ["iterator", "reference"]  # pointer = reference, por construcción
RELACIONES = ["same", "before", "after", "any"]
EFECTOS = ["preserves", "depends", "invalidates"]
CONDICIONES = ["capacity_reached", "rehash_triggered", "non_binding"]
ORDEN = {"preserves": 0, "depends": 1, "invalidates": 2}


@dataclass(frozen=True)
class Regla:
    mutacion: str
    categoria: str
    relacion: str
    efecto: str
    condicion: str | None
    clausula: str | None


@dataclass(frozen=True)
class Mutacion:
    id: str
    contenedor: str
    operacion: str
    punto: str
    crecimiento: str
    reglas: tuple[Regla, ...]


def camel(s: str) -> str:
    return "".join(p.capitalize() for p in s.split("_"))


def parse(doc: dict) -> tuple[list[Mutacion], list[str]]:
    errores: list[str] = []
    out: list[Mutacion] = []
    vistos: set[str] = set()
    for m in doc.get("mutaciones", []):
        mid = m.get("id", "?")
        for campo, valores in (("contenedor", CONTENEDORES), ("operacion", OPERACIONES),
                               ("punto", PUNTOS), ("crecimiento", CRECIMIENTOS)):
            if m.get(campo) not in valores:
                errores.append(f"{mid}: {campo} desconocido: {m.get(campo)!r}")
        clave = f"{m.get('contenedor')}.{m.get('operacion')}.{m.get('punto')}"
        if clave != mid:
            errores.append(f"{mid}: el id debe ser {clave}")
        if mid in vistos:
            errores.append(f"{mid}: mutación duplicada")
        vistos.add(mid)
        reglas: list[Regla] = []
        claves: set[tuple[str, str]] = set()
        for x in m.get("reglas", []):
            cat, rel, ef = x.get("categoria"), x.get("relacion"), x.get("efecto")
            cond, cl = x.get("condicion"), x.get("clausula")
            if cat not in CATEGORIAS: errores.append(f"{mid}: categoría desconocida {cat!r}")
            if rel not in RELACIONES: errores.append(f"{mid}: relación desconocida {rel!r}")
            if ef not in EFECTOS: errores.append(f"{mid}: efecto desconocido {ef!r}")
            if ef == "depends" and cond not in CONDICIONES:
                errores.append(f"{mid}/{cat}/{rel}: 'depends' sin condición válida")
            if ef != "depends" and cond is not None:
                errores.append(f"{mid}/{cat}/{rel}: condición en un efecto que no depende")
            if ef in ("depends", "invalidates") and not cl:
                errores.append(f"{mid}/{cat}/{rel}: falta la cláusula")
            if (cat, rel) in claves:
                errores.append(f"{mid}/{cat}/{rel}: regla duplicada")
            claves.add((cat, rel))
            reglas.append(Regla(mid, cat, rel, ef, cond, cl))
        out.append(Mutacion(mid, m.get("contenedor"), m.get("operacion"), m.get("punto"),
                            m.get("crecimiento"), tuple(reglas)))
    return out, errores


def efecto(m: Mutacion, cat: str, rel: str) -> Regla | None:
    return next((r for r in m.reglas if r.categoria == cat and r.relacion == rel), None)


def check_total(ms: list[Mutacion]) -> list[str]:
    errores = []
    for m in ms:
        rels = {cat: {r.relacion for r in m.reglas if r.categoria == cat} for cat in CATEGORIAS}
        if not rels["iterator"]:
            errores.append(f"{m.id}: sin reglas")
        if rels["iterator"] != rels["reference"]:
            errores.append(f"{m.id}: iterador y referencia cubren relaciones distintas")
    return errores


def check_leyes(ms: list[Mutacion]) -> list[str]:
    errores = []
    for m in ms:
        for r in m.reglas:
            if r.categoria != "iterator":
                continue
            ref = efecto(m, "reference", r.relacion)
            # «un iterador nunca está mejor que una referencia al mismo elemento»
            if ref and ORDEN[r.efecto] < ORDEN[ref.efecto]:
                errores.append(f"ley iterador ⊒ referencia: {m.id}/{r.relacion}")
        for r in m.reglas:
            # «insertar en un contenedor de nodos no invalida nada» (salvo resize, que puede recortar)
            if m.contenedor in NODOS and m.operacion in INSERCIONES and r.efecto != "preserves":
                errores.append(f"ley inserción en nodos: {m.id}/{r.categoria}/{r.relacion}")
            # «lo que está antes del punto sobrevive en un vector sin reubicar»
            if m.contenedor == "vector" and r.relacion == "before" and not (
                    r.efecto == "preserves" or r.condicion == "capacity_reached"):
                errores.append(f"ley antes del punto en vector: {m.id}/{r.categoria}")
            # «una mutación de todo no depende de la relación»
            if (m.punto in ("whole",) or (m.punto == "by_key" and m.operacion in INSERCIONES)) \
                    and r.relacion != "any":
                errores.append(f"ley mutación de todo: {m.id}/{r.categoria}/{r.relacion}")
            if r.relacion == "any" and m.punto not in ("whole", "by_key"):
                errores.append(f"'any' sólo en whole/by_key: {m.id}")
    return errores


def render(ms: list[Mutacion]) -> str:
    L = ["// GENERADO por norma/gen_tabla.py desde norma/matriz.json — NO EDITAR A MANO.",
         "// Se incluye desde dominio/NormTable.cpp, dentro de namespace ucsm::dominio.",
         "",
         f"inline constexpr std::size_t MutationCount = {len(ms)};",
         "inline constexpr MutationRow Mutations[] = {"]
    for m in ms:
        L.append(f"    {{ContainerKind::{camel(m.contenedor)}, Operation::{camel(m.operacion)}, "
                 f"Point::{camel(m.punto)}, Growth::{camel(m.crecimiento)}}},")
    L += ["};", "", "inline constexpr RuleRow Rules[] = {"]
    for m in ms:
        for r in m.reglas:
            cond = f"Condition::{camel(r.condicion)}" if r.condicion else "Condition::None"
            cl = json.dumps(r.clausula or "")
            L.append(f"    {{{{ContainerKind::{camel(m.contenedor)}, Operation::{camel(m.operacion)}, "
                     f"Point::{camel(m.punto)}}}, HandleCategory::{camel(r.categoria)}, "
                     f"Relation::{camel(r.relacion)}, EffectKind::{camel(r.efecto)}, {cond}, {cl}}},")
    L += ["};", ""]
    return "\n".join(L)


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    entrada, salida = Path(sys.argv[1]), Path(sys.argv[2])
    ms, errores = parse(json.loads(entrada.read_text(encoding="utf-8")))
    if errores:
        print("MatrixInvalid:", *errores, sep="\n  ", file=sys.stderr)
        return 1
    for nombre, chequeo in (("TableNotTotal", check_total), ("LawBroken", check_leyes)):
        errores = chequeo(ms)
        if errores:
            print(f"{nombre}:", *errores, sep="\n  ", file=sys.stderr)
            return 1
    salida.parent.mkdir(parents=True, exist_ok=True)
    texto = render(ms)
    if not salida.exists() or salida.read_text(encoding="utf-8") != texto:
        salida.write_text(texto, encoding="utf-8")
    print(f"TableGenerated: {len(ms)} mutaciones, {sum(len(m.reglas) for m in ms)} reglas → {salida}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
