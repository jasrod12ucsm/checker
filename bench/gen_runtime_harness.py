#!/usr/bin/env python3
"""Genera un ejecutable por despacho para validar dinámicamente el corpus.

El corpus principal conserva su objetivo: medir herramientas estáticas. Este
archivo genera un *harness* distinto que invoca una función por proceso para
que un aborto de ASan o de los iteradores seguros no interrumpa los demás casos.
"""
import argparse
import json
from pathlib import Path


TYPE = {
    "vector": "std::vector<int>",
    "deque": "std::deque<int>",
    "list": "std::list<int>",
    "flist": "std::forward_list<int>",
    "set": "std::set<int>",
    "mset": "std::multiset<int>",
    "map": "std::map<int, int>",
    "mmap": "std::multimap<int, int>",
    "uset": "std::unordered_set<int>",
    "umap": "std::unordered_map<int, int>",
}


def prelude(corpus_include: str) -> str:
    return f'''// GENERADO por bench/gen_runtime_harness.py — no editar a mano
#include <cstdlib>
#include <cstring>
#include <string_view>

volatile int runtime_sink = 0;
void sink(int value) {{ runtime_sink ^= value; }}
void sink(char value) {{ runtime_sink ^= static_cast<unsigned char>(value); }}
void sink(const void *value) {{ runtime_sink ^= value != nullptr; }}

#include "{corpus_include}"

enum class Mode {{ Natural, ForceInvalidation, PreserveValidity }};

Mode parse_mode(const char *arg) {{
  if (std::strcmp(arg, "force") == 0) return Mode::ForceInvalidation;
  if (std::strcmp(arg, "preserve") == 0) return Mode::PreserveValidity;
  return Mode::Natural;
}}

std::vector<int> make_vector(Mode mode, std::string_view op) {{
  std::vector<int> c;
  if (mode == Mode::ForceInvalidation && op == "pop_back") {{ c.push_back(1); return c; }}
  // shrink_to_fit es una solicitud no vinculante: se prepara holgura para
  // observar la decisión de esta implementación, no para imponerla.
  if (op == "shrink_to_fit") {{
    if (mode == Mode::ForceInvalidation) c.reserve(256);
    c.push_back(1); c.push_back(2); c.push_back(3);
    if (mode == Mode::PreserveValidity) c.shrink_to_fit();
    return c;
  }}
  if (mode == Mode::ForceInvalidation) {{
    c.reserve(8);
    while (c.size() < c.capacity()) c.push_back(static_cast<int>(c.size() + 1));
    return c;
  }}
  // resize_grow y reserve solicitan size()+100; 256 hace que esa solicitud
  // no exceda la capacidad de la configuración de preservación.
  if (mode == Mode::PreserveValidity) c.reserve(256);
  c.push_back(1); c.push_back(2); c.push_back(3);
  return c;
}}

std::deque<int> make_deque(Mode, std::string_view) {{ return {{1, 2, 3}}; }}
std::list<int> make_list(Mode, std::string_view) {{ return {{1, 2, 3}}; }}
std::forward_list<int> make_flist(Mode, std::string_view) {{ return {{1, 2, 3}}; }}

std::set<int> make_set(Mode, std::string_view) {{ return {{1, 2, 3}}; }}
std::multiset<int> make_mset(Mode, std::string_view) {{ return {{1, 2, 3}}; }}
std::map<int, int> make_map(Mode, std::string_view) {{ return {{{{1,1}}, {{2,2}}, {{3,3}}}}; }}
std::multimap<int, int> make_mmap(Mode, std::string_view) {{ return {{{{1,1}}, {{2,2}}, {{3,3}}}}; }}

std::unordered_set<int> make_uset(Mode mode, std::string_view) {{
  std::unordered_set<int> c;
  if (mode == Mode::ForceInvalidation) {{
    c.max_load_factor(1.0f); c.rehash(8);
    for (std::size_t i = 0; i < c.bucket_count(); ++i) c.insert(static_cast<int>(i));
  }} else {{ c.reserve(256); c.insert(1); c.insert(2); c.insert(3); }}
  return c;
}}
std::unordered_map<int, int> make_umap(Mode mode, std::string_view) {{
  std::unordered_map<int, int> c;
  if (mode == Mode::ForceInvalidation) {{
    c.max_load_factor(1.0f); c.rehash(8);
    for (std::size_t i = 0; i < c.bucket_count(); ++i) c.emplace(static_cast<int>(i), 1);
  }} else {{ c.reserve(256); c.emplace(1,1); c.emplace(2,2); c.emplace(3,3); }}
  return c;
}}
'''


def dispatch(name: str, meta: dict) -> str:
    container = meta["contenedor"]
    return f'''  if (id == "{name}") {{
    {TYPE[container]} c = make_{container}(mode, "{meta["op"]}");
    {name}(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }}
'''


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--truth", default="test/corpus_truth.json")
    parser.add_argument("--output", default="test/runtime_runner.cpp")
    args = parser.parse_args()

    truth_path = Path(args.truth)
    output_path = Path(args.output)
    truth = json.loads(truth_path.read_text())
    corpus_include = Path("corpus.cpp").as_posix()

    output = [prelude(corpus_include)]
    output.append('''
int main(int argc, char **argv) {
  if (argc != 3) return 64;
  const std::string_view id(argv[1]);
  const Mode mode = parse_mode(argv[2]);
''')
    output.extend(dispatch(name, meta) for name, meta in truth.items())
    output.append("  return 65; // identificador de caso desconocido\n}\n")
    output_path.write_text("".join(output))
    print(f"{output_path} -> {len(truth)} despachos")


if __name__ == "__main__":
    main()
