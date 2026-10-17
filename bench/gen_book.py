#!/usr/bin/env python3
"""Genera corpus_book/: un mdbook con el corpus completo y los resultados.

Lee solo artefactos ya producidos por los demas scripts de bench/:
  test/corpus.cpp, test/corpus_truth.json, test/corpus_results.json,
  test/corpus_fallos.json, test/runtime_validation_results.json,
  test/matrix.cpp, test/matrix_results.json

Uso:
  python3 bench/gen_book.py
  mdbook serve corpus_book --open
"""
import collections, json, os, re, shutil

OUT = "corpus_book"
SRC = os.path.join(OUT, "src")

NOMBRE = {
 "vector": "std::vector", "deque": "std::deque", "list": "std::list",
 "flist": "std::forward_list", "set": "std::set", "mset": "std::multiset",
 "map": "std::map", "mmap": "std::multimap", "uset": "std::unordered_set",
 "umap": "std::unordered_map", "string": "std::string",
}
ORDEN_C = list(NOMBRE)
SOSTIENE = {"it": "iterador", "ref": "referencia", "ptr": "puntero"}
FORMAS = ["recto", "guarda", "bucle", "llamada"]
FORMA_DESC = {
 "recto":   "handle obtenido, mutación directa y uso, sin comparación contra `end()`.",
 "guarda":  "igual que `recto`, pero con `if (it == c.end()) return;` antes de mutar.",
 "bucle":   "mutación dentro de un `for` acotado a tres rondas; también participa el iterador de control.",
 "llamada": "la mutación ocurre dentro de una función auxiliar `mutar_*` (cruza una llamada).",
}
INSTR = {"libstdcxx_debug": "libstdc++ Debug", "asan_ubsan": "ASan/UBSan"}
CHK = ("core, cplusplus, alpha.cplusplus.IteratorModeling, alpha.cplusplus.ContainerModeling, "
       "alpha.cplusplus.InvalidatedIterator, alpha.cplusplus.IteratorRange, "
       "alpha.cplusplus.MismatchedIterator")

load = lambda p: json.load(open(p))
truth = load("test/corpus_truth.json")
static = {r["fn"]: r for r in load("test/corpus_results.json")}
fallos = {r["fn"]: r["causa"] for r in load("test/corpus_fallos.json")}
rt = load("test/runtime_validation_results.json")
dyn = collections.defaultdict(list)
for r in rt["resultados"]:
    dyn[r["fn"]].append(r)
matrix = load("test/matrix_results.json")


def funciones(path, patron):
    """nombre -> cuerpo de cada funcion de nivel superior que casa con patron."""
    lines = open(path).read().splitlines()
    out, i = {}, 0
    while i < len(lines):
        m = re.match(patron, lines[i])
        if m:
            j = i
            while lines[j] != "}":
                j += 1
            out[m.group(1)] = "\n".join(lines[i:j + 1])
            i = j
        i += 1
    return out

code = funciones("test/corpus.cpp", r"^void (f_\w+)\(")
mutar = {}
for l in open("test/corpus.cpp"):
    m = re.match(r"^void mutar_(\w+)\(.*\{ (.*) \}$", l)
    if m:
        mutar[m.group(1)] = m.group(2)
mcode = funciones("test/matrix.cpp", r"^void ((?:it|rf)_\w+)\(")


def pct(a, b):
    return f"{100 * a / b:.1f}%" if b else "—"

def etiqueta(e):
    return {"UB": "🔴 `UB`", "SAFE": "🟢 `SAFE`", "POLICY": "🟡 `POLICY`"}[e]

def veredicto_estatico(fn):
    r = static[fn]
    e, a = r["esperado"], r["avisa"]
    if e == "UB":
        return "✅ detectado" if a else "❌ falso negativo"
    if e == "SAFE":
        return "⚠️ falso positivo" if a else "✅ silencio correcto"
    return "avisa (conservador)" if a else "silencio (optimista)"

def tipo_dinamico(s):
    m = (re.search(r"AddressSanitizer: ([\w-]+)", s) or re.search(r"Error: (.*?)\.?$", s, re.M)
         or re.search(r"runtime error: (.*)", s))
    return m.group(1) if m else ""

def det(r, k):
    return r[k]["estado"] == "DETECTADO"

def pagina_op(cn, op):
    return f"casos/{cn}/{op}.md"

def enlace_caso(fn, desde_raiz=True):
    t = truth[fn]
    p = pagina_op(t["contenedor"], t["op"])
    return f"[`{fn}`]({p}#{fn})" if desde_raiz else f"[`{fn}`]({t['op']}.md#{fn})"

def write(rel, text):
    path = os.path.join(SRC, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w").write(text.rstrip() + "\n")


# ---- agrupaciones -------------------------------------------------------------
ops = collections.OrderedDict()
for fn, t in truth.items():
    ops.setdefault(t["contenedor"], collections.OrderedDict()).setdefault(t["op"], []).append(fn)
contenedores = [c for c in ORDEN_C if c in ops]
fns = list(truth)
UB = [f for f in fns if truth[f]["esperado"] == "UB"]
SAFE = [f for f in fns if truth[f]["esperado"] == "SAFE"]
POL = [f for f in fns if truth[f]["esperado"] == "POLICY"]
avisa = lambda f: static[f]["avisa"]


def tabla_cobertura(clave, valores, fmt=lambda v: f"`{v}`"):
    filas = ["| Valor | Casos | UB | Detectados | Falsos negativos | Cobertura | SAFE | Falsos positivos | POLICY con aviso |",
             "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for v in valores:
        sub = [f for f in fns if truth[f][clave] == v]
        u = [f for f in sub if f in UB]; s = [f for f in sub if f in SAFE]; p = [f for f in sub if f in POL]
        d = sum(map(avisa, u)); fp = sum(map(avisa, s))
        filas.append(f"| {fmt(v)} | {len(sub)} | {len(u)} | {d} | {len(u)-d} | {pct(d, len(u))} | "
                     f"{len(s)} | {fp} | {sum(map(avisa, p))}/{len(p)} |")
    return "\n".join(filas)


# ---- limpiar y book.toml ---------------------------------------------------------
if os.path.isdir(SRC):
    shutil.rmtree(SRC)
os.makedirs(SRC)
open(os.path.join(OUT, "book.toml"), "w").write("""[book]
title = "Corpus de invalidación de iteradores — casos y benchmark"
authors = ["rodriguezwilbert613"]
language = "es"
src = "src"

[build]
build-dir = "book"

[output.html]
default-theme = "light"
preferred-dark-theme = "ayu"

[output.html.fold]
enable = true
level = 1

[output.html.search]
limit-results = 50
""")
open(os.path.join(OUT, ".gitignore"), "w").write("book\n")


# ---- introduccion -------------------------------------------------------------
n_pares = sum(len(v) for v in ops.values())
write("README.md", f"""
# Corpus de invalidación de iteradores

Este libro documenta **todos los casos** del corpus de invalidación de
iteradores, referencias y punteros de contenedores STL (C++17), junto con los
resultados de cada benchmark ejecutado sobre él.

> Generado automáticamente por `bench/gen_book.py` a partir de los artefactos de
> `test/`. No editar a mano: regenerar con `python3 bench/gen_book.py`.

## Cifras

| | |
|---|---:|
| Casos analíticos (funciones en `test/corpus.cpp`) | **{len(fns)}** |
| Contenedores | {len(contenedores)} |
| Pares contenedor–operación | {n_pares} |
| Casos `UB` normativo | {len(UB)} |
| Casos `SAFE` normativo | {len(SAFE)} |
| Casos `POLICY` (depende del estado) | {len(POL)} |
| Ejecuciones dinámicas | {rt['ejecuciones']} |
| Cobertura del protocolo dinámico | `{rt['cobertura_protocolo']}` |
| Casos de la matriz normativa (`test/matrix.cpp`) | {len(matrix)} |

## Resultado principal del análisis estático

El Clang Static Analyzer (checkers `alpha.cplusplus.*`) detecta
**{sum(map(avisa, UB))} de {len(UB)}** casos `UB` ({pct(sum(map(avisa, UB)), len(UB))}),
con **{sum(map(avisa, SAFE))}** falsos positivos sobre {len(SAFE)} casos `SAFE`.
Ver [Análisis estático](resultados/estatico.md) y
[Catálogo de falsos negativos](resultados/fallos.md).

## Cómo leer el libro

- **Metodología**: dimensiones del corpus, etiquetas y protocolo.
- **Resultados**: benchmark estático, validación dinámica y matriz normativa.
- **Casos del corpus**: un capítulo por contenedor y una página por operación,
  con el código de cada uno de los {len(fns)} casos, su etiqueta normativa, lo que
  dijo el analizador estático y lo que observaron los instrumentos dinámicos.
- **Índice de casos**: tabla plana de los {len(fns)} casos con enlaces.

La búsqueda (tecla `s`) acepta nombres de función, p. ej. `f_deque_push_back_ref_bucle`.
""")

write("metodologia.md", f"""
# Metodología

## Dimensiones

Cada caso es una tupla `(contenedor, operación, sostiene, forma)`:

| Dimensión | Valores |
|---|---|
| Contenedor | {", ".join(f"`{NOMBRE[c]}`" for c in contenedores)} |
| Operación mutadora | {n_pares} pares contenedor–operación |
| Sostiene (handle retenido) | `it` iterador, `ref` referencia, `ptr` puntero |
| Forma sintáctica | {", ".join(f"`{f}`" for f in FORMAS)} |

Total: {n_pares} pares × 3 handles × 4 formas = **{len(fns)} casos**.

### Formas sintácticas

{chr(10).join(f"- **`{f}`**: {d}" for f, d in FORMA_DESC.items())}

La etiqueta depende del contenedor, la operación y el handle; la forma solo
cambia si el analizador *ve* el defecto. Excepción: en `bucle` el iterador de
control también se usa tras la mutación, de modo que si la operación invalida
iteradores el caso es `UB` aunque la referencia retenida siga siendo válida.

## Etiquetas normativas

- 🔴 **`UB`**: según las reglas de invalidación de C++17, el uso posterior es
  comportamiento indefinido.
- 🟢 **`SAFE`**: el handle sigue siendo válido tras la mutación.
- 🟡 **`POLICY`**: depende del estado (capacidad de un `vector`, factor de carga
  de un contenedor `unordered`). Se ejecuta dinámicamente en dos escenarios:
  `force` (fuerza la invalidación) y `preserve` (la evita).

## Benchmark estático

```bash
python3 bench/gen_corpus.py
python3 bench/run_corpus.py
```

Ejecuta `clang++ --analyze -std=c++17` con los checkers

```text
{CHK}
```

y `aggressive-binary-operation-simplification=true`. Un aviso se atribuye a un
caso si cae en una línea de su función; en forma `bucle`, un aviso sobre la
cabecera del `for` solo cuenta cuando el handle retenido es el iterador.

## Validación dinámica

```bash
python3 bench/run_runtime_validation.py --timeout {rt['timeout_segundos']:g}
```

Cada caso se ejecuta en un proceso aislado con dos instrumentos:

| Instrumento | Compilador | Flags |
|---|---|---|
| libstdc++ Debug Mode | `{rt['entorno']['gxx']}` | `{rt['entorno']['modo_debug']}` |
| ASan + UBSan | `{rt['entorno']['clangxx']}` | `{rt['entorno']['sanitizadores']}` |

Estándar: {rt['entorno']['estandar']}. Una ejecución sin detección **no**
reclasifica un caso `UB` como seguro: C++ no exige que el defecto se manifieste.

## Matriz normativa

```bash
python3 bench/gen_matrix.py
python3 bench/run_matrix.py
```

Benchmark previo y más pequeño ({len(matrix)} casos): una celda por
contenedor × operación × dominio (iterador / referencia), siempre en forma
`guarda`.
""")


# ---- resultados: estatico -----------------------------------------------------
d_ub = sum(map(avisa, UB)); fp = sum(map(avisa, SAFE)); pa = sum(map(avisa, POL))
filas_op = ["| Contenedor | Operación | UB | Detectados | Cobertura | SAFE | FP | POLICY |",
            "|---|---|---:|---:|---:|---:|---:|---:|"]
for cn in contenedores:
    for op, lst in ops[cn].items():
        u = [f for f in lst if f in UB]; s = [f for f in lst if f in SAFE]; p = [f for f in lst if f in POL]
        d = sum(map(avisa, u))
        filas_op.append(f"| `{cn}` | [`{op}`]({'../' + pagina_op(cn, op)}) | {len(u)} | {d} | {pct(d, len(u))} | "
                        f"{len(s)} | {sum(map(avisa, s))} | {len(p)} |")

cruce = ["| Forma \\ Sostiene | " + " | ".join(SOSTIENE.values()) + " |", "|---|" + "---:|" * 3]
for fo in FORMAS:
    celdas = []
    for so in SOSTIENE:
        u = [f for f in UB if truth[f]["forma"] == fo and truth[f]["sostiene"] == so]
        celdas.append(f"{sum(map(avisa, u))}/{len(u)}")
    cruce.append(f"| `{fo}` | " + " | ".join(celdas) + " |")

write("resultados/estatico.md", f"""
# Análisis estático (Clang Static Analyzer)

## Totales

| Etiqueta | Casos | Con aviso | Sin aviso | Lectura |
|---|---:|---:|---:|---|
| 🔴 `UB` | {len(UB)} | {d_ub} | {len(UB)-d_ub} | cobertura **{pct(d_ub, len(UB))}** |
| 🟢 `SAFE` | {len(SAFE)} | {fp} | {len(SAFE)-fp} | {fp} falsos positivos |
| 🟡 `POLICY` | {len(POL)} | {pa} | {len(POL)-pa} | {"optimista: nunca avisa" if pa == 0 else ""} |

## UB detectados: forma × handle

Detectados / total de casos `UB` en cada celda.

{chr(10).join(cruce)}

## Por forma sintáctica

{tabla_cobertura("forma", FORMAS)}

## Por handle retenido

{tabla_cobertura("sostiene", list(SOSTIENE), lambda v: f"`{v}` ({SOSTIENE[v]})")}

## Por contenedor

{tabla_cobertura("contenedor", contenedores, lambda v: f"[`{NOMBRE[v]}`](../casos/{v}/index.md)")}

## Por operación

{chr(10).join(filas_op)}

## Casos detectados

Los {d_ub} casos `UB` en los que el analizador emitió aviso:

{chr(10).join(f"- {enlace_caso(f).replace('](casos', '](../casos')}" for f in UB if avisa(f))}
""")


# ---- resultados: fallos -------------------------------------------------------
por_causa = collections.defaultdict(list)
for f, c in fallos.items():
    por_causa[c].append(f)
secciones = []
for c in sorted(por_causa):
    lst = por_causa[c]
    filas = ["| Caso | Contenedor | Operación | Sostiene | Forma |", "|---|---|---|---|---|"]
    filas += [f"| {enlace_caso(f).replace('](casos', '](../casos')} | `{truth[f]['contenedor']}` | `{truth[f]['op']}` | "
              f"`{truth[f]['sostiene']}` | `{truth[f]['forma']}` |" for f in lst]
    secciones.append(f"## {c}\n\n{len(lst)} casos.\n\n" + "\n".join(filas))
resumen_causas = "\n".join(f"| {c} | {len(l)} | {pct(len(l), len(fallos))} |" for c, l in sorted(por_causa.items()))
write("resultados/fallos.md", f"""
# Catálogo de falsos negativos

Los {len(fallos)} casos `UB` sobre los que el analizador estático calla,
clasificados por la causa que los explica (con precedencia: se asigna la
primera que aplica). Fuente: `test/corpus_fallos.json`.

| Causa | Casos | % |
|---|---:|---:|
{resumen_causas}

{chr(10).join(secciones)}
""")


# ---- resultados: dinamica -----------------------------------------------------
res = rt["resultados"]
def tabla_din(filtro_nombre, grupos):
    filas = [f"| {filtro_nombre} | Ejecuciones | libstdc++ Debug | ASan/UBSan | Alguno | Ninguno |",
             "|---|---:|---:|---:|---:|---:|"]
    for nombre, sub in grupos:
        a = sum(det(r, "libstdcxx_debug") for r in sub); b = sum(det(r, "asan_ubsan") for r in sub)
        al = sum(det(r, "libstdcxx_debug") or det(r, "asan_ubsan") for r in sub)
        filas.append(f"| {nombre} | {len(sub)} | {a} | {b} | {al} | {len(sub)-al} |")
    return "\n".join(filas)

g_etq = [(f"`{e}` ({m})", [r for r in res if r["etiqueta_normativa"] == e and r["modo"] == m])
         for e, m in (("UB", "natural"), ("SAFE", "natural"), ("POLICY", "force"), ("POLICY", "preserve"))]
g_cont = [(f"`{NOMBRE[c]}`", [r for r in res if r["contenedor"] == c]) for c in contenedores]
g_forma = [(f"`{fo}`", [r for r in res if r["forma"] == fo and r["etiqueta_normativa"] == "UB"]) for fo in FORMAS]
g_sost = [(f"`{s}`", [r for r in res if r["sostiene"] == s and r["etiqueta_normativa"] == "UB"]) for s in SOSTIENE]
tipos = collections.Counter((INSTR[k], tipo_dinamico(r[k]["stderr"])) for r in res for k in INSTR if det(r, k))

# cruce estatico x dinamico sobre UB
dyn_ub = {f: any(det(r, k) for r in dyn[f] for k in INSTR) for f in UB}
cr = collections.Counter((avisa(f), dyn_ub[f]) for f in UB)
solo_din = [f for f in UB if dyn_ub[f] and not avisa(f)]
ub_mudo = [f for f in UB if not dyn_ub[f]]
safe_det = [r["fn"] for r in res if r["etiqueta_normativa"] == "SAFE" and any(det(r, k) for k in INSTR)]

write("resultados/dinamica.md", f"""
# Validación dinámica

{rt['descripcion']}

- Casos base: **{rt['casos_base']}**; ejecuciones: **{rt['ejecuciones']}**
  (una por caso `UB`/`SAFE`, dos por caso `POLICY`).
- Timeout por ejecución: {rt['timeout_segundos']:g} s.
- Cobertura del protocolo: `{rt['cobertura_protocolo']}`.

## Resumen por instrumento

| Instrumento | Detectado | Sin detección |
|---|---:|---:|
{chr(10).join(f"| {INSTR[k]} | {v.get('DETECTADO', 0)} | {v.get('SIN_DETECCION', 0)} |" for k, v in rt['resumen'].items())}

## Por etiqueta normativa y escenario

{tabla_din("Etiqueta (modo)", g_etq)}

Casos `SAFE` con alguna detección dinámica: **{len(safe_det)}**.

## Tipo de error observado

| Instrumento | Diagnóstico | Ejecuciones |
|---|---|---:|
{chr(10).join(f"| {i} | `{t or '—'}` | {n} |" for (i, t), n in sorted(tipos.items()))}

## Por contenedor (todas las ejecuciones)

{tabla_din("Contenedor", g_cont)}

## Casos `UB` por forma

{tabla_din("Forma", g_forma)}

## Casos `UB` por handle

{tabla_din("Sostiene", g_sost)}

## Cruce estático × dinámico (casos `UB`)

| | Dinámica detecta | Dinámica no detecta |
|---|---:|---:|
| **Estático avisa** | {cr[(True, True)]} | {cr[(True, False)]} |
| **Estático calla** | {cr[(False, True)]} | {cr[(False, False)]} |

Los {len(solo_din)} casos de la celda *estático calla / dinámica detecta* son
evidencia de que el defecto es real y observable, pero invisible para el
analizador estático.

<details>
<summary>Casos UB detectados solo dinámicamente ({len(solo_din)})</summary>

{chr(10).join(f"- {enlace_caso(f).replace('](casos', '](../casos')}" for f in solo_din)}

</details>

<details>
<summary>Casos UB sin manifestación dinámica en ningún instrumento ({len(ub_mudo)})</summary>

Siguen siendo `UB` por su regla normativa: la implementación no está obligada a
manifestar el defecto.

{chr(10).join(f"- {enlace_caso(f).replace('](casos', '](../casos')}" for f in ub_mudo)}

</details>
""")


# ---- resultados: matriz -------------------------------------------------------
buckets = collections.Counter(r["bucket"] for r in matrix)
mcont = [c for c in ORDEN_C if any(r["container"] == c for r in matrix)]
filas_m = ["| Contenedor | Dominio | UB | Detectados | Huecos | SAFE | FP | POLICY |", "|---|---|---:|---:|---:|---:|---:|---:|"]
for c in mcont:
    for dom in ("iterador", "referencia"):
        sub = [r for r in matrix if r["container"] == c and r["domain"] == dom]
        if not sub:
            continue
        u = [r for r in sub if r["expected"] == "UB"]; s = [r for r in sub if r["expected"] == "SAFE"]
        d = sum(r["warned"] for r in u)
        filas_m.append(f"| [`{NOMBRE[c]}`](../matriz/{c}.md) | {dom} | {len(u)} | {d} | {len(u)-d} | {len(s)} | "
                       f"{sum(r['warned'] for r in s)} | {sum(r['expected'] == 'POLICY' for r in sub)} |")
mu = [r for r in matrix if r["expected"] == "UB"]; md = sum(r["warned"] for r in mu)
write("resultados/matriz.md", f"""
# Matriz normativa

Benchmark preliminar de {len(matrix)} casos (`test/matrix.cpp`): una celda por
contenedor × operación × dominio, todas en forma `guarda`.

## Totales

| Clasificación | Casos |
|---|---:|
{chr(10).join(f"| {b} | {n} |" for b, n in sorted(buckets.items()))}

Exhaustividad global sobre `UB`: **{md}/{len(mu)} = {pct(md, len(mu))}**.

## Por contenedor y dominio

{chr(10).join(filas_m)}
""")

for c in mcont:
    partes = [f"# Matriz: `{NOMBRE[c]}`\n"]
    for r in [r for r in matrix if r["container"] == c]:
        partes.append(f"## {r['fn']}\n\n| Operación | Dominio | Esperado | Aviso | Clasificación |\n|---|---|---|---|---|\n"
                      f"| `{r['op']}` | {r['domain']} | {etiqueta(r['expected'])} | {'sí' if r['warned'] else 'no'} | {r['bucket']} |\n\n"
                      f"```cpp\n{mcode.get(r['fn'], '// (código no encontrado)')}\n```\n")
    write(f"matriz/{c}.md", "\n".join(partes))


# ---- casos --------------------------------------------------------------------
def bloque_caso(fn):
    t = truth[fn]; s = static[fn]
    out = [f"### {fn}", "",
           f"| Handle | Forma | Etiqueta | Análisis estático |", "|---|---|---|---|",
           f"| {SOSTIENE[t['sostiene']]} | `{t['forma']}` | {etiqueta(t['esperado'])} | {veredicto_estatico(fn)} |", "",
           f"```cpp\n{code[fn]}\n```", ""]
    if fn in fallos:
        out += [f"> **Causa del falso negativo:** {fallos[fn]}", ""]
    runs = dyn.get(fn, [])
    if runs:
        out += ["| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |", "|---|---|---|---|"]
        for r in runs:
            cel = []
            for k in INSTR:
                if det(r, k):
                    tp = tipo_dinamico(r[k]["stderr"])
                    cel.append(f"🛑 {tp}" if tp else "🛑 detectado")
                else:
                    cel.append(f"— (código {r[k]['codigo']})")
            out.append(f"| `{r['modo']}` | {r['escenario']['precondicion']} | {cel[0]} | {cel[1]} |")
        out.append("")
        for r in runs:
            for k in INSTR:
                if r[k]["stderr"].strip():
                    out += [f"<details>\n<summary>stderr {INSTR[k]} · <code>{r['modo']}</code></summary>\n",
                            f"````text\n{r[k]['stderr'].rstrip()}\n````\n", "</details>\n"]
    return "\n".join(out)

summary_casos = []
for cn in contenedores:
    filas = ["| Operación | Mutación | Iterador | Ref/Ptr | UB | Detectados (estático) | Detectados (dinámico) |",
             "|---|---|---|---|---:|---:|---:|"]
    for op, lst in ops[cn].items():
        e_it = truth[f"f_{cn}_{op}_it_recto"]["esperado"]; e_rf = truth[f"f_{cn}_{op}_ref_recto"]["esperado"]
        u = [f for f in lst if f in UB]
        filas.append(f"| [`{op}`]({op}.md) | `{mutar[f'{cn}_{op}']}` | {etiqueta(e_it)} | {etiqueta(e_rf)} | {len(u)} | "
                     f"{sum(map(avisa, u))} | {sum(dyn_ub[f] for f in u)} |")
    lst_c = [f for f in fns if truth[f]["contenedor"] == cn]
    u = [f for f in lst_c if f in UB]
    write(f"casos/{cn}/index.md", f"""
# `{NOMBRE[cn]}`

{len(lst_c)} casos ({len(ops[cn])} operaciones × 3 handles × 4 formas).
`UB`: {len(u)} · detectados estáticamente: {sum(map(avisa, u))} ({pct(sum(map(avisa, u)), len(u))}).

Las columnas *Iterador* y *Ref/Ptr* indican la etiqueta en forma `recto`; en
forma `bucle` puede pasar a `UB` por el iterador de control.

{chr(10).join(filas)}
""")
    summary_casos.append(f"  - [`{NOMBRE[cn]}`](casos/{cn}/index.md)")
    for op, lst in ops[cn].items():
        u = [f for f in lst if f in UB]
        cuerpo = [f"# `{NOMBRE[cn]}::{op}`", "",
                  f"Mutación: `{mutar[f'{cn}_{op}']}`", "",
                  f"- Iterador retenido: {etiqueta(truth[f'f_{cn}_{op}_it_recto']['esperado'])}",
                  f"- Referencia/puntero retenido: {etiqueta(truth[f'f_{cn}_{op}_ref_recto']['esperado'])}",
                  f"- Casos `UB` detectados estáticamente: {sum(map(avisa, u))}/{len(u)}", ""]
        mapa = ["| | " + " | ".join(f"`{f}`" for f in FORMAS) + " |", "|---|" + "---|" * 4]
        for so in SOSTIENE:
            celdas = []
            for fo in FORMAS:
                f = f"f_{cn}_{op}_{so}_{fo}"
                ic = {"UB": "🔴", "SAFE": "🟢", "POLICY": "🟡"}[truth[f]["esperado"]]
                celdas.append(f"[{ic} {'avisa' if avisa(f) else 'calla'}](#{f})")
            mapa.append(f"| **{SOSTIENE[so]}** | " + " | ".join(celdas) + " |")
        cuerpo += mapa + [""]
        for so in SOSTIENE:
            cuerpo += [f"## Handle: {SOSTIENE[so]}", ""]
            cuerpo += [bloque_caso(f"f_{cn}_{op}_{so}_{fo}") for fo in FORMAS]
        write(pagina_op(cn, op), "\n".join(cuerpo))
        summary_casos.append(f"    - [`{op}`]({pagina_op(cn, op)})")

filas_idx = ["| # | Caso | Contenedor | Operación | Sostiene | Forma | Etiqueta | Estático | Dinámico |",
             "|---:|---|---|---|---|---|---|---|---|"]
for i, f in enumerate(fns, 1):
    t = truth[f]
    d = "🛑" if any(det(r, k) for r in dyn[f] for k in INSTR) else "—"
    filas_idx.append(f"| {i} | {enlace_caso(f)} | `{t['contenedor']}` | `{t['op']}` | `{t['sostiene']}` | "
                     f"`{t['forma']}` | {etiqueta(t['esperado'])} | {veredicto_estatico(f)} | {d} |")
write("indice.md", f"# Índice de casos\n\nLos {len(fns)} casos del corpus. *Dinámico* 🛑 = algún instrumento detectó el defecto en alguna ejecución.\n\n" + "\n".join(filas_idx))

write("SUMMARY.md", "\n".join([
    "# Resumen", "", "[Introducción](README.md)", "", "- [Metodología](metodologia.md)",
    "", "# Resultados", "",
    "- [Análisis estático](resultados/estatico.md)",
    "  - [Catálogo de falsos negativos](resultados/fallos.md)",
    "- [Validación dinámica](resultados/dinamica.md)",
    "- [Matriz normativa](resultados/matriz.md)",
    *[f"  - [`{NOMBRE[c]}`](matriz/{c}.md)" for c in mcont],
    "", "# Casos del corpus", "",
    "- [Índice de casos](indice.md)",
    *summary_casos,
]))

print(f"{OUT}/src -> {len(fns)} casos, {n_pares} páginas de operación, {len(mcont)} páginas de matriz")
print(f"  mdbook serve {OUT} --open")
