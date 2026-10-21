#!/usr/bin/env python3
"""Inyección de defectos en código real: ¿el checker los encuentra?

Cada semilla reemplaza un fragmento EXACTO de un proyecto por una versión con
un defecto de invalidación (o por un uso correcto que no debe avisar), corre
el plugin sólo sobre esa unidad de traducción y restaura el archivo.

Uso (dentro de checker:llvm21): python3 bench/inyeccion.py build/real salida.json
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from codigo_real import analizar  # noqa: E402


@dataclass(frozen=True)
class Semilla:
    id: str
    proyecto: str
    archivo: str
    original: str
    defecto: str
    espera: str        # "confirmado" | "posible" | "nada"
    mecanismo: str


SEMILLAS = [
    Semilla("S1", "ninja", "src/build.cc",
            "  result->edge = e->second;\n  subproc_to_edge_.erase(e);\n",
            "  subproc_to_edge_.erase(e);\n  result->edge = e->second;\n",
            "confirmado", "map::erase libera el nodo y luego se lee e->second (M5)"),
    Semilla("S2", "ninja", "src/build.cc",
            "  start_time_millis = it->second;\n  end_time_millis = GetTimeMillis() - start_time_millis_;\n  running_edges_.erase(it);\n",
            "  running_edges_.erase(it);\n  start_time_millis = it->second;\n  end_time_millis = GetTimeMillis() - start_time_millis_;\n",
            "confirmado", "map::erase y lectura posterior por el iterador (M5)"),
    # (La primera S3 caía en `#ifdef _WIN32` de disk_interface.cc: no se compila en Linux.)
    Semilla("S3", "ninja", "src/missing_deps.cc",
            "  it->second.insert(std::make_pair(to, found));\n  return found;\n",
            "  if (found) adjacency_map_.clear();\n  it->second.insert(std::make_pair(to, found));\n  return found;\n",
            "confirmado", "unordered_map::clear y uso de un iterador obtenido con insert(...).first (M5)"),
    Semilla("S4", "ninja", "src/graph.cc",
            "    Node* node = nodes.front();\n    nodes.pop_front();\n",
            "    Node* const& node = nodes.front();\n    nodes.pop_front();\n",
            "confirmado", "referencia al frente de un deque y pop_front (M5)"),
    Semilla("S5", "ninja", "src/build_log.cc",
            "    if (user.IsPathDead(i->first)) {\n      dead_outputs.push_back(i->first);\n      continue;\n    }\n",
            "    if (user.IsPathDead(i->first)) {\n      entries_.erase(i);\n      continue;\n    }\n",
            "confirmado", "unordered_map::erase dentro del recorrido y ++i (M5)"),
    Semilla("S6", "yaml-cpp", "src/node_data.cpp",
            "    auto jt = std::next(it);\n    if (it->first->is_defined() && it->second->is_defined())\n      m_undefinedPairs.erase(it);\n    it = jt;\n",
            "    if (it->first->is_defined() && it->second->is_defined())\n      m_undefinedPairs.erase(it);\n    ++it;\n",
            "confirmado", "list::erase y ++it sobre el borrado (M5)"),
    Semilla("S7", "leveldb", "db/db_impl.cc",
            "    compact->outputs.push_back(out);\n    mutex_.Unlock();\n",
            "    CompactionState::Output* first =\n        compact->outputs.empty() ? nullptr : &compact->outputs[0];\n"
            "    compact->outputs.push_back(out);\n    if (first != nullptr) pending_outputs_.insert(first->number);\n    mutex_.Unlock();\n",
            "posible", "puntero a un elemento de vector y push_back sin reserve (M1)"),
    Semilla("S8", "ninja", "src/graph.cc",
            "  if (record_varname)\n    lookups_.pop_back();\n  return result;\n",
            "  const std::string* mine = record_varname ? &lookups_.back() : nullptr;\n"
            "  if (record_varname)\n    lookups_.pop_back();\n  if (mine && mine->empty()) return result;\n  return result;\n",
            "confirmado", "puntero a back() de un vector y pop_back (M3)"),
    # ── buen uso: no debe avisar ──
    Semilla("B1", "leveldb", "db/db_impl.cc",
            "    compact->outputs.push_back(out);\n    mutex_.Unlock();\n",
            "    compact->outputs.reserve(compact->outputs.size() + 1);\n    CompactionState::Output* first =\n"
            "        compact->outputs.empty() ? nullptr : &compact->outputs[0];\n"
            "    compact->outputs.push_back(out);\n    if (first != nullptr) pending_outputs_.insert(first->number);\n    mutex_.Unlock();\n",
            "nada", "la misma S7 con reserve(size() + 1) antes: garantía"),
    Semilla("B2", "ninja", "src/build_log.cc",
            "  for (Entries::iterator i = entries_.begin(); i != entries_.end(); ++i) {\n    if (user.IsPathDead(i->first)) {\n      dead_outputs.push_back(i->first);\n      continue;\n    }\n",
            "  for (Entries::iterator i = entries_.begin(); i != entries_.end(); ++i) {\n    if (user.IsPathDead(i->first)) {\n      i = entries_.erase(i);\n      if (i == entries_.end()) break;\n      continue;\n    }\n",
            "nada", "i = erase(i): el iterador devuelto es válido"),
]


def main() -> int:
    raiz, salida = Path(sys.argv[1]), Path(sys.argv[2])
    inlining = sys.argv[3] if len(sys.argv) > 3 else "noredundancy"
    comandos = {}
    for p in {s.proyecto for s in SEMILLAS}:
        for e in json.loads((raiz / f"{p}-build" / "compile_commands.json").read_text()):
            comandos[Path(e["file"]).resolve()] = e
    filas = []
    for s in SEMILLAS:
        f = (raiz / s.proyecto / s.archivo).resolve()
        texto = f.read_text()
        assert texto.count(s.original) == 1, f"{s.id}: el fragmento original no aparece una sola vez"
        base = [a for a in analizar(comandos[f], "Possibly", inlining)["avisos"] if Path(a["file"]).resolve() == f]
        try:
            f.write_text(texto.replace(s.original, s.defecto))
            r = analizar(comandos[f], "Possibly", inlining)
        finally:
            f.write_text(texto)
        # Cuentan los avisos NUEVOS frente a la misma unidad sin la semilla; las
        # líneas posteriores al fragmento se corren lo que creció el fragmento.
        fin_original = texto[: texto.index(s.original)].count("\n") + s.original.count("\n")
        delta = s.defecto.count("\n") - s.original.count("\n")
        vistos = {(a["line"] + (delta if a["line"] > fin_original else 0), a["msg"]) for a in base}
        avisos = [a for a in r["avisos"] if Path(a["file"]).resolve() == f
                  and (a["line"], a["msg"]) not in vistos]
        clases = {a["clase"] for a in avisos}
        obtenido = "confirmado" if "confirmado" in clases else "posible" if "posible" in clases else "nada"
        filas.append({"id": s.id, "proyecto": s.proyecto, "archivo": s.archivo, "mecanismo": s.mecanismo,
                      "espera": s.espera, "obtenido": obtenido, "acierto": obtenido == s.espera,
                      "codigo": r["codigo"], "avisos": avisos})
        print(f"{s.id} {s.proyecto:9} espera {s.espera:10} obtiene {obtenido:10} "
              f"{'OK' if obtenido == s.espera else 'FALLA'}  ({len(avisos)} avisos)", flush=True)
    salida.write_text(json.dumps(filas, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
