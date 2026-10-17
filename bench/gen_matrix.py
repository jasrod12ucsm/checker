#!/usr/bin/env python3
"""Genera el benchmark matricial contenedor x operacion x dominio.

Para cada celda emite dos funciones:
  it_<c>_<op>  : toma un iterador, muta, y lo desreferencia
  rf_<c>_<op>  : toma una referencia a un elemento, muta, y la lee

Verdad de campo segun ISO C++ N4950:
  UB     -> la operacion SIEMPRE invalida lo que tomamos
  SAFE   -> NUNCA lo invalida
  POLICY -> depende del estado en ejecucion (realloc / rehash / tamano)
"""
import json

# read_it : expresion que desreferencia el iterador `it`
# read_rf : expresion que lee la referencia `r`
# ref_src : como obtener la referencia
C = {
 "vector": dict(t="std::vector<int>", h="vector",
                read_it="sink(*it);", ref2="const int& r = *it;", ref="const int& r = *c.begin();", read_rf="sink(r);"),
 "deque": dict(t="std::deque<int>", h="deque",
                read_it="sink(*it);", ref2="const int& r = *it;", ref="const int& r = *c.begin();", read_rf="sink(r);"),
 "list": dict(t="std::list<int>", h="list",
                read_it="sink(*it);", ref2="const int& r = *it;", ref="const int& r = *c.begin();", read_rf="sink(r);"),
 "flist": dict(t="std::forward_list<int>", h="forward_list",
                read_it="sink(*it);", ref2="const int& r = *it;", ref="const int& r = *c.begin();", read_rf="sink(r);"),
 "set": dict(t="std::set<int>", h="set",
                read_it="sink(*it);", ref2="const int& r = *it;", ref="const int& r = *c.begin();", read_rf="sink(r);"),
 "map": dict(t="std::map<int,int>", h="map",
                read_it="sink(it->second);", ref2="const int& r = it->second;", ref="const int& r = c.begin()->second;", read_rf="sink(r);"),
 "uset": dict(t="std::unordered_set<int>", h="unordered_set",
                read_it="sink(*it);", ref2="const int& r = *it;", ref="const int& r = *c.begin();", read_rf="sink(r);"),
 "umap": dict(t="std::unordered_map<int,int>", h="unordered_map",
                read_it="sink(it->second);", ref2="const int& r = it->second;", ref="const int& r = c.begin()->second;", read_rf="sink(r);"),
 "string": dict(t="std::string", h="string",
                read_it="sink(*it);", ref2="const char& r = *it;", ref="const char& r = *c.begin();", read_rf="sink(r);"),
}

# (op, sentencia, esperado_iterador, esperado_referencia)
OPS = {
 "vector": [
   ("push_back",      "c.push_back(1);",              "POLICY","POLICY"),
   ("emplace_back",   "c.emplace_back(1);",           "POLICY","POLICY"),
   ("insert_begin",   "c.insert(c.begin(), 1);",      "UB","UB"),
   ("insert_end",     "c.insert(c.end(), 1);",        "POLICY","POLICY"),
   ("erase_begin",    "c.erase(c.begin());",          "UB","UB"),
   ("clear",          "c.clear();",                   "UB","UB"),
   ("resize_grow",    "c.resize(c.size() + 100);",    "POLICY","POLICY"),
   ("reserve",        "c.reserve(c.size() + 100);",   "POLICY","POLICY"),
   ("shrink_to_fit",  "c.shrink_to_fit();",           "POLICY","POLICY"),
   ("assign",         "c.assign(3, 7);",              "UB","UB"),
   ("pop_back",       "c.pop_back();",                "POLICY","POLICY"),
 ],
 "deque": [
   ("push_back",      "c.push_back(1);",              "UB","SAFE"),
   ("push_front",     "c.push_front(1);",             "UB","SAFE"),
   ("emplace_back",   "c.emplace_back(1);",           "UB","SAFE"),
   ("insert_middle",  "c.insert(c.begin(), 1);",      "UB","UB"),
   ("erase_begin",    "c.erase(c.begin());",          "UB","UB"),
   ("clear",          "c.clear();",                   "UB","UB"),
   ("resize_grow",    "c.resize(c.size() + 100);",    "UB","SAFE"),
   ("pop_front",      "c.pop_front();",               "UB","UB"),
 ],
 "list": [
   ("push_back",      "c.push_back(1);",              "SAFE","SAFE"),
   ("push_front",     "c.push_front(1);",             "SAFE","SAFE"),
   ("insert",         "c.insert(c.begin(), 1);",      "SAFE","SAFE"),
   ("erase_begin",    "c.erase(c.begin());",          "UB","UB"),
   ("clear",          "c.clear();",                   "UB","UB"),
   ("resize_grow",    "c.resize(c.size() + 100);",    "SAFE","SAFE"),
   ("pop_front",      "c.pop_front();",               "UB","UB"),
   ("reverse",        "c.reverse();",                 "SAFE","SAFE"),
 ],
 "flist": [
   ("push_front",     "c.push_front(1);",             "SAFE","SAFE"),
   ("insert_after",   "c.insert_after(c.before_begin(), 1);", "SAFE","SAFE"),
   ("erase_after",    "c.erase_after(c.before_begin());",     "UB","UB"),
   ("clear",          "c.clear();",                   "UB","UB"),
 ],
 "set": [
   ("insert",         "c.insert(99);",                "SAFE","SAFE"),
   ("emplace",        "c.emplace(98);",               "SAFE","SAFE"),
   ("erase_begin",    "c.erase(c.begin());",          "UB","UB"),
   ("clear",          "c.clear();",                   "UB","UB"),
 ],
 "map": [
   ("insert",         "c.insert({99, 1});",           "SAFE","SAFE"),
   ("emplace",        "c.emplace(98, 1);",            "SAFE","SAFE"),
   ("subscript",      "c[97] = 1;",                   "SAFE","SAFE"),
   ("erase_begin",    "c.erase(c.begin());",          "UB","UB"),
   ("clear",          "c.clear();",                   "UB","UB"),
 ],
 "uset": [
   ("insert",         "c.insert(99);",                "POLICY","SAFE"),
   ("erase_begin",    "c.erase(c.begin());",          "UB","UB"),
   ("clear",          "c.clear();",                   "UB","UB"),
   ("rehash",         "c.rehash(1024);",              "UB","SAFE"),
   ("reserve",        "c.reserve(1024);",             "UB","SAFE"),
 ],
 "umap": [
   ("insert",         "c.insert({99, 1});",           "POLICY","SAFE"),
   ("subscript",      "c[97] = 1;",                   "POLICY","SAFE"),
   ("erase_begin",    "c.erase(c.begin());",          "UB","UB"),
   ("clear",          "c.clear();",                   "UB","UB"),
   ("rehash",         "c.rehash(1024);",              "UB","SAFE"),
 ],
 "string": [
   ("push_back",      "c.push_back('x');",            "POLICY","POLICY"),
   ("append",         "c.append(\"xyz\");",           "POLICY","POLICY"),
   ("insert_begin",   "c.insert(c.begin(), 'x');",    "UB","UB"),
   ("erase_begin",    "c.erase(c.begin());",          "UB","UB"),
   ("clear",          "c.clear();",                   "UB","UB"),
   ("reserve",        "c.reserve(c.size() + 100);",   "POLICY","POLICY"),
   ("resize_grow",    "c.resize(c.size() + 100);",    "POLICY","POLICY"),
 ],
}

hdrs = sorted({v["h"] for v in C.values()})
out = ["// GENERADO por bench/gen_matrix.py -- no editar a mano",
       "// Matriz contenedor x operacion x dominio (iterador / referencia)."]
out += [f"#include <{h}>" for h in hdrs]
out += ["", "void sink(int);", "void sink(char);", ""]

truth = {}
for cname, cfg in C.items():
    for op, stmt, exp_it, exp_rf in OPS[cname]:
        fn = f"it_{cname}_{op}"
        out += [f"void {fn}({cfg['t']}& c) {{",
                f"  auto it = c.begin();",
                f"  if (it == c.end()) return;   // guarda: activa el modelado",
                f"  {stmt}",
                f"  {cfg['read_it']}",
                "}"]
        truth[fn] = dict(container=cname, op=op, domain="iterador", expected=exp_it)

        fn = f"rf_{cname}_{op}"
        out += [f"void {fn}({cfg['t']}& c) {{",
                f"  auto it = c.begin();",
                f"  if (it == c.end()) return;   // guarda: activa el modelado",
                f"  {cfg['ref2']}",
                f"  {stmt}",
                f"  {cfg['read_rf']}",
                "}"]
        truth[fn] = dict(container=cname, op=op, domain="referencia", expected=exp_rf)

open("test/matrix.cpp","w").write("\n".join(out) + "\n")
json.dump(truth, open("test/matrix_truth.json","w"), indent=1)
print(f"generado test/matrix.cpp  ->  {len(truth)} funciones "
      f"({len(truth)//2} celdas x 2 dominios)")
