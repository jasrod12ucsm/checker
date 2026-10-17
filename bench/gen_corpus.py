#!/usr/bin/env python3
"""Corpus matricial de invalidacion — cinco ejes.

  A  contenedor            12
  B  operacion mutadora    69 pares (A,B)
  C  que se sostiene       iterador | referencia | puntero
  D  forma sintactica      recto | guarda | bucle | llamada

La verdad de campo depende de (A,B,C) — NO de D.
D solo cambia si el analizador LO VE. Por eso D aisla el silencio:
la misma celda, mismo bug, cuatro escrituras.

Correspondencia con el Documento 01:
  D=bucle    + insercion  -> Caso 1 (range-for + insertar)
  D=bucle    + erase      -> Casos 2 y 3
  C=referencia            -> Caso 4
  D=llamada               -> Caso 6
  esperado=POLICY         -> Caso 8
"""
import json

# ---- EJE A: contenedores -------------------------------------------------
# usa_par: el elemento es un pair (map-likes) -> hay que leer .second
C = {
 "vector":     ("std::vector<int>",              "vector",             False),
 "deque":      ("std::deque<int>",               "deque",              False),
 "list":       ("std::list<int>",                "list",               False),
 "flist":      ("std::forward_list<int>",        "forward_list",       False),
 "set":        ("std::set<int>",                 "set",                False),
 "mset":       ("std::multiset<int>",            "set",                False),
 "map":        ("std::map<int,int>",             "map",                True),
 "mmap":       ("std::multimap<int,int>",        "map",                True),
 "uset":       ("std::unordered_set<int>",       "unordered_set",      False),
 "umap":       ("std::unordered_map<int,int>",   "unordered_map",      True),
}

# ---- EJE B: operaciones. (nombre, sentencia, exp_iterador, exp_referencia)
# exp_puntero == exp_referencia: el estandar los trata juntos.
# Se excluyen adrede swap y resize_shrink: su regla no es inequivoca.
OPS = {
 "vector": [
   ("push_back",     "c.push_back(1);",             "POLICY","POLICY"),
   ("emplace_back",  "c.emplace_back(1);",          "POLICY","POLICY"),
   ("insert_begin",  "c.insert(c.begin(),1);",      "UB","UB"),
   ("insert_end",    "c.insert(c.end(),1);",        "POLICY","POLICY"),
   ("erase_begin",   "c.erase(c.begin());",         "UB","UB"),
   ("clear",         "c.clear();",                  "UB","UB"),
   ("resize_grow",   "c.resize(c.size()+100);",     "POLICY","POLICY"),
   ("reserve",       "c.reserve(c.size()+100);",    "POLICY","POLICY"),
   ("shrink_to_fit", "c.shrink_to_fit();",          "POLICY","POLICY"),
   ("assign",        "c.assign(3,7);",              "UB","UB"),
   ("pop_back",      "c.pop_back();",               "POLICY","POLICY"),
 ],
 "deque": [
   ("push_back",     "c.push_back(1);",             "UB","SAFE"),
   ("push_front",    "c.push_front(1);",            "UB","SAFE"),
   ("emplace_back",  "c.emplace_back(1);",          "UB","SAFE"),
   ("insert_middle", "c.insert(c.begin(),1);",      "UB","UB"),
   ("erase_begin",   "c.erase(c.begin());",         "UB","UB"),
   ("clear",         "c.clear();",                  "UB","UB"),
   ("resize_grow",   "c.resize(c.size()+100);",     "UB","SAFE"),
   ("pop_front",     "c.pop_front();",              "UB","UB"),
 ],
 "list": [
   ("push_back",     "c.push_back(1);",             "SAFE","SAFE"),
   ("push_front",    "c.push_front(1);",            "SAFE","SAFE"),
   ("insert",        "c.insert(c.begin(),1);",      "SAFE","SAFE"),
   ("erase_begin",   "c.erase(c.begin());",         "UB","UB"),
   ("clear",         "c.clear();",                  "UB","UB"),
   ("resize_grow",   "c.resize(c.size()+100);",     "SAFE","SAFE"),
   ("pop_front",     "c.pop_front();",              "UB","UB"),
   ("reverse",       "c.reverse();",                "SAFE","SAFE"),
   ("sort",          "c.sort();",                   "SAFE","SAFE"),
 ],
 "flist": [
   ("push_front",    "c.push_front(1);",            "SAFE","SAFE"),
   ("insert_after",  "c.insert_after(c.before_begin(),1);", "SAFE","SAFE"),
   ("erase_after",   "c.erase_after(c.before_begin());",    "UB","UB"),
   ("clear",         "c.clear();",                  "UB","UB"),
 ],
 "set":   [("insert","c.insert(99);","SAFE","SAFE"), ("emplace","c.emplace(98);","SAFE","SAFE"),
           ("erase_begin","c.erase(c.begin());","UB","UB"), ("clear","c.clear();","UB","UB")],
 "mset":  [("insert","c.insert(99);","SAFE","SAFE"),
           ("erase_begin","c.erase(c.begin());","UB","UB"), ("clear","c.clear();","UB","UB")],
 "map":   [("insert","c.insert({99,1});","SAFE","SAFE"), ("emplace","c.emplace(98,1);","SAFE","SAFE"),
           ("subscript","c[97]=1;","SAFE","SAFE"),
           ("erase_begin","c.erase(c.begin());","UB","UB"), ("clear","c.clear();","UB","UB")],
 "mmap":  [("insert","c.insert({99,1});","SAFE","SAFE"),
           ("erase_begin","c.erase(c.begin());","UB","UB"), ("clear","c.clear();","UB","UB")],
 "uset":  [("insert","c.insert(99);","POLICY","SAFE"),
           ("erase_begin","c.erase(c.begin());","UB","UB"), ("clear","c.clear();","UB","UB"),
           ("rehash","c.rehash(1024);","UB","SAFE"), ("reserve","c.reserve(1024);","UB","SAFE")],
 "umap":  [("insert","c.insert({99,1});","POLICY","SAFE"), ("subscript","c[97]=1;","POLICY","SAFE"),
           ("erase_begin","c.erase(c.begin());","UB","UB"), ("clear","c.clear();","UB","UB"),
           ("rehash","c.rehash(1024);","UB","SAFE")],
}

INSERCION = {"push_back","emplace_back","push_front","emplace_front","insert","insert_begin",
             "insert_end","insert_middle","insert_after","append","emplace","subscript",
             "resize_grow","reserve","rehash"}

# ---- EJE C: que se sostiene ---------------------------------------------
def holder(kind, par):
    if kind == "it":  return ("",                        "sink(it->second);" if par else "sink(*it);")
    if kind == "ref": return ("const auto& h = *it;",    "sink(h.second);"   if par else "sink(h);")
    if kind == "ptr": return ("const auto* h = &*it;",   "sink(h->second);"  if par else "sink(*h);")

hdrs = sorted({v[1] for v in C.values()})
out = ["// GENERADO por bench/gen_corpus.py — no editar a mano"]
out += [f"#include <{h}>" for h in hdrs]
out += ["", "void sink(int);", "void sink(char);", "void sink(const void*);", ""]

truth = {}
# mutadores para el eje D=llamada (Caso 6: la mutacion cruza una llamada)
for cn,(ct,_,_) in C.items():
    for op, stmt, _, _ in OPS[cn]:
        out += [f"void mutar_{cn}_{op}({ct}& c) {{ {stmt} }}"]
out += [""]

for cn,(ct,_,par) in C.items():
    for op, stmt, exp_it, exp_rf in OPS[cn]:
        for hk in ("it","ref","ptr"):
            decl, use = holder(hk, par)
            exp = exp_it if hk == "it" else exp_rf
            for ctx in ("recto","guarda","bucle","llamada"):
                fn = f"f_{cn}_{op}_{hk}_{ctx}"
                # En un bucle hay dos handles: el declarado por el eje C y el
                # iterador de control `it`. Si la operación invalida el
                # iterador, el incremento/chequeo de la siguiente vuelta ya es
                # UB aunque una referencia o puntero al elemento conserve su
                # validez. Para inserciones condicionales, el crecimiento
                # repetido del bucle termina forzando el caso invalidante; con
                # pop_back, las rondas sucesivas terminan eliminando el
                # elemento retenido.
                e = ("UB" if ctx == "bucle" and
                     (exp_it == "UB" or
                      (op in INSERCION and exp == "POLICY") or
                      (op == "pop_back" and exp == "POLICY"))
                     else exp)
                if ctx == "bucle":
                    body = [f"void {fn}({ct}& c) {{",
                            # La cota conserva el patrón de mutar durante la
                            # iteración, pero evita que los contenedores cuyos
                            # iteradores permanecen válidos recorran para
                            # siempre los elementos recién insertados.
                            "  int rondas = 0;",
                            f"  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {{"]
                    if decl: body.append(f"    {decl}")
                    body += [f"    {stmt}", f"    {use}", "  }", "}"]
                else:
                    body = [f"void {fn}({ct}& c) {{", "  auto it = c.begin();"]
                    if ctx in ("guarda","llamada"):
                        body.append("  if (it == c.end()) return;")
                    if decl: body.append(f"  {decl}")
                    body.append(f"  mutar_{cn}_{op}(c);" if ctx == "llamada" else f"  {stmt}")
                    body += [f"  {use}", "}"]
                out += body
                truth[fn] = dict(contenedor=cn, op=op, sostiene=hk, forma=ctx, esperado=e)

open("test/corpus.cpp","w").write("\n".join(out)+"\n")
json.dump(truth, open("test/corpus_truth.json","w"), indent=1)
pares = sum(len(v) for v in OPS.values())
print(f"test/corpus.cpp -> {len(truth)} casos")
print(f"  {len(C)} contenedores x {pares} pares (contenedor,operacion) x 3 sostenes x 4 formas")
