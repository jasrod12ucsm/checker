#!/usr/bin/env python3
"""Genera corpus_book/: un mdbook con el corpus completo y los resultados.

Lee solo artefactos ya producidos por los demas scripts de bench/:
  test/corpus.cpp, test/corpus_truth.json, test/corpus_results.json,
  test/corpus_fallos.json, test/experimento/metricas.json (bench/experimento.py), test/runtime_validation_results.json,
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
experimento = load("test/experimento/metricas.json")
# Código real: copia de build/real/avisos_all.json e inyeccion_all.json (build/ no se versiona).
real = load("test/codigo_real/avisos.json") if os.path.exists("test/codigo_real/avisos.json") else None
inyeccion = load("test/codigo_real/inyeccion.json") if os.path.exists("test/codigo_real/inyeccion.json") else None
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
        return "✅ detectado" if a else "❌ no detectado"
    if e == "SAFE":
        return "❌ falsa alarma" if a else "✅ correcto, sin aviso"
    return "⚪ avisa (depende del estado)" if a else "⚪ sin aviso (depende del estado)"

VEREDICTO_PLUGIN = {"TP": "✅ detectado", "FN": "❌ no detectado", "FP": "❌ falsa alarma",
                    "TN": "✅ correcto, sin aviso", "PolicyWarned": "⚪ aviso posible",
                    "PolicySilent": "⚪ sin aviso", "Incident": "⚠️ incidente"}

def en_palabras(cn, op):
    frase = {"UB": "queda **inválido**: usarlo después es un bug (UB)",
             "SAFE": "sigue siendo **válido**: usarlo después es correcto",
             "POLICY": "**puede** quedar inválido según el estado del contenedor "
                       "(capacidad o factor de carga)"}
    e_it = truth[f"f_{cn}_{op}_it_recto"]["esperado"]; e_rf = truth[f"f_{cn}_{op}_ref_recto"]["esperado"]
    txt = (f"después de `{mutar[f'{cn}_{op}']}` sobre un `{NOMBRE[cn]}`, un iterador guardado "
           f"{frase[e_it]}; una referencia o puntero guardado {frase[e_rf]}.")
    if e_it != "UB" and any(truth[f"f_{cn}_{op}_{so}_bucle"]["esperado"] == "UB" for so in SOSTIENE):
        txt += (" En forma `bucle` el caso es UB igualmente: la mutación se repite en cada vuelta "
                "y termina invalidando lo que se guardó.")
    elif e_it == "UB" and e_rf != "UB":
        txt += (" Ojo: en forma `bucle` todos son UB, porque el iterador de control del `for` "
                "(`++it`) queda inválido aunque la referencia siga bien.")
    return txt

def tipo_dinamico(s):
    m = (re.search(r"AddressSanitizer: ([\w-]+)", s) or re.search(r"Error: (.*?)\.?$", s, re.M)
         or re.search(r"runtime error: (.*)", s))
    return m.group(1) if m else ""

def det(r, k):
    return r[k]["estado"] == "DETECTADO"

def pagina_op(cn, op):
    return f"casos/{cn}/{op}.md"

def con_garantia(fn):
    return truth[fn].get("garantia", "ninguna") != "ninguna"

def enlace_caso(fn, desde_raiz=True):
    t = truth[fn]
    if con_garantia(fn):
        return f"[`{fn}`]({'' if desde_raiz else '../../'}casos/garantias.md#{fn})"
    p = pagina_op(t["contenedor"], t["op"])
    return f"[`{fn}`]({p}#{fn})" if desde_raiz else f"[`{fn}`]({t['op']}.md#{fn})"

def write(rel, text):
    path = os.path.join(SRC, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w").write(text.rstrip() + "\n")


# ---- agrupaciones -------------------------------------------------------------
# Los casos de buen uso (D-20) van en su propia página: no forman la rejilla
# operación × handle × forma de las páginas de operación.
ops = collections.OrderedDict()
for fn, t in truth.items():
    if con_garantia(fn):
        continue
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
title = "Checker de invalidación de handles para Clang Static Analyzer — diseño, banco y resultados"
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
AVISO_DIN = "" if rt["cobertura_protocolo"] == "COMPLETA" else (
    f"> ⚠️ **Resultados dinámicos incompletos**: `test/runtime_validation_results.json` "
    f"solo tiene {rt['casos_base']} de {len(truth)} casos ({rt['ejecuciones']} ejecuciones). "
    f"Restaurar con `git checkout test/runtime_validation_results.json` o volver a correr "
    f"`python3 bench/run_runtime_validation.py --timeout 5`, y regenerar el libro.\n")
n_pares = sum(len(v) for v in ops.values())
write("README.md", f"""
# Corpus de invalidación de iteradores

{AVISO_DIN}
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

write("guia.md", f"""
# Cómo leer este libro

## El problema que estudia el corpus

En C++ puedes guardar un **iterador**, una **referencia** o un **puntero** a un
elemento de un contenedor (`vector`, `map`, ...). Si después **modificas el
contenedor** (insertas, borras, limpias), lo que guardaste puede quedar **roto**:
el elemento se movió de lugar o dejó de existir.

```cpp
std::vector<int> v = {{1, 2, 3}};
auto it = v.begin();   // guardo un iterador al primer elemento
v.clear();             // modifico el contenedor: el elemento ya no existe
std::cout << *it;      // uso lo guardado -> BUG
```

Usar algo roto es **comportamiento indefinido** (*Undefined Behavior*, **UB**):
el estándar no dice qué pasa. Puede crashear, imprimir basura o, peor, parecer
que funciona. Que no explote no significa que esté bien.

Si se rompe o no depende del contenedor y de la operación. En `std::list`, por
ejemplo, `push_back` no rompe nada; en `std::vector` puede romperlo todo.

## Qué es un caso

Cada caso es una función pequeña con ese patrón: **guardar, modificar, usar**.
Su nombre dice exactamente qué prueba:

```text
f_deque_push_back_ref_bucle
  │     │         │    └── forma: cómo está escrito el código (recto, guarda, bucle, llamada)
  │     │         └─────── qué se guarda: it (iterador), ref (referencia), ptr (puntero)
  │     └───────────────── operación que modifica el contenedor
  └─────────────────────── contenedor
```

Las cuatro formas sintácticas prueban **el mismo bug escrito de cuatro maneras**,
para ver si la herramienta depende de cómo se escribe el código:

{chr(10).join(f"- **`{f}`**: {d}" for f, d in FORMA_DESC.items())}

## La etiqueta: la respuesta correcta

Cada caso tiene una **etiqueta** que dice, según las reglas del estándar C++17,
si el programa tiene el bug o no. Es la "respuesta del examen":

| Etiqueta | Significa |
|---|---|
| 🔴 `UB` | **Hay bug**: se usa algo que quedó roto. |
| 🟢 `SAFE` | **No hay bug**: lo guardado sigue siendo válido. |
| 🟡 `POLICY` | **Depende del estado**: p. ej. `vector::push_back` solo rompe los iteradores si el vector se queda sin capacidad y se muda de memoria. |

## Lo que hizo el analizador estático

La herramienta evaluada es el **Clang Static Analyzer**: lee el código sin
ejecutarlo y avisa si cree que hay un bug. Para cada caso pueden pasar cuatro
cosas. **El color es la respuesta correcta; el texto, lo que hizo la herramienta:**

| Etiqueta | Clang | Se muestra | ¿Bien o mal? |
|---|---|---|---|
| 🔴 `UB` | avisa | ✅ detectado | Bien: encontró el bug. |
| 🔴 `UB` | no avisa | ❌ no detectado | **Mal**: había bug y no lo vio (*falso negativo*). |
| 🟢 `SAFE` | no avisa | ✅ correcto, sin aviso | Bien: no había bug y no dijo nada. |
| 🟢 `SAFE` | avisa | ❌ falsa alarma | Mal: avisó de un bug inexistente (*falso positivo*). |
| 🟡 `POLICY` | — | ⚪ depende del estado | No se puntúa: la respuesta depende de la ejecución. |

Entonces un 🟢 sin aviso **es un acierto**. Los que importan son los 🔴 ❌.

**Resultado:** Clang detecta {sum(map(avisa, UB))} de {len(UB)} bugs
({pct(sum(map(avisa, UB)), len(UB))}) y no da ninguna falsa alarma. Se le escapan
casi todos, y en especial **todos** los casos en que lo guardado es una referencia
o un puntero.

## Lo que pasó al ejecutar (validación dinámica)

Para comprobar que los bugs son reales, cada caso también **se ejecuta** con dos
herramientas que vigilan el programa mientras corre:

| Herramienta | Qué detecta | Mensaje típico |
|---|---|---|
| **libstdc++ Debug Mode** | Uso de un iterador roto (la biblioteca lleva la cuenta de qué iteradores siguen vigentes). | `attempt to dereference a singular iterator` (*singular* = roto) |
| **ASan/UBSan** | Acceso a memoria que ya fue liberada. | `heap-use-after-free` |

Si estas herramientas no te suenan, lee primero
[Las herramientas de ejecución](herramientas.md): las explica desde cero.

En las tablas de cada caso:

- 🛑 **detectado**: la herramienta vio el bug al ejecutar.
- **sin detección**: el programa terminó sin que la herramienta notara nada.

Un caso 🔴 `UB` **sin detección** sigue siendo un bug: a veces la memoria rota
todavía contiene el valor viejo y el programa "funciona" por suerte. Por eso la
etiqueta la decide el estándar y no la ejecución. Los casos 🟢 `SAFE` nunca
produjeron una detección, lo que respalda que están bien etiquetados.

Los casos 🟡 `POLICY` se ejecutan dos veces: **`force`** (preparando el
contenedor para que la operación sí rompa lo guardado) y **`preserve`**
(preparándolo para que no lo rompa). En el resto de casos el escenario es
**`natural`** (un contenedor ordinario `{{1, 2, 3}}`).

## Recorrido sugerido

1. Lee un caso fácil: [`std::vector` → `clear`](casos/vector/clear.md). Todo es
   🔴 UB, y se ve qué detecta cada herramienta.
2. Compáralo con [`std::list` → `push_back`](casos/list/push_back.md), donde casi
   todo es 🟢 SAFE.
3. Mira un caso mixto: [`std::deque` → `push_back`](casos/deque/push_back.md),
   donde el iterador se rompe pero la referencia no.
4. Luego ve a los resultados: [Análisis estático](resultados/estatico.md) y el
   [catálogo de por qué Clang no detecta](resultados/fallos.md).
""")

write("herramientas.md", """
# Las herramientas de ejecución

Las dos son **herramientas que vigilan un programa mientras se ejecuta** y lo
detienen apenas hace algo prohibido.

## El problema que resuelven

Cuando un programa C++ usa un iterador roto, normalmente **no pasa nada
visible**: lee un número viejo que seguía en esa memoria y continúa. El bug está,
pero escondido. Es como cruzar un semáforo en rojo sin que pase un auto: hiciste
algo prohibido, pero no te enteras.

Estas herramientas **ponen un policía en el semáforo**: cada vez que el programa
hace algo prohibido, lo paran y dicen exactamente qué hizo.

## libstdc++ Debug Mode — vigila los iteradores

**libstdc++** es la biblioteca estándar de C++ que trae `g++`: el código que
implementa `std::vector`, `std::map`, etc. **Debug Mode** es una versión
"vigilada" de esa misma biblioteca. Se activa al compilar:

```bash
g++ -D_GLIBCXX_DEBUG programa.cpp
```

En esa versión **cada contenedor lleva una lista de sus iteradores**. Cuando
modificas el contenedor, marca como rotos los iteradores que el estándar dice que
se rompen. Cuando usas un iterador, primero revisa si está marcado y, si lo está,
detiene el programa:

```cpp
std::vector<int> v = {1, 2, 3};
auto it = v.begin();
v.clear();          // Debug Mode: "it ahora está roto"
int x = *it;        // Debug Mode: ¡alto!
```

```text
Error: attempt to dereference a singular iterator.
```

*Singular iterator* es la forma técnica de decir "iterador roto". También aparece
`attempt to increment a singular iterator`, cuando se hace `++it` sobre uno roto.

**Límite:** solo vigila **iteradores**. Una referencia (`const int& r = v[0]`) o
un puntero (`int* p = &v[0]`) son tipos básicos del lenguaje, no de la
biblioteca, así que Debug Mode no puede seguirlos.

## AddressSanitizer (ASan) — vigila la memoria

Es una herramienta del compilador (`clang++` o `g++`):

```bash
clang++ -fsanitize=address programa.cpp
```

No sabe nada de iteradores: **vigila la memoria**. Cuando el programa libera
memoria (por ejemplo, un vector que se muda a otro lugar y suelta el espacio
viejo), ASan marca ese espacio como prohibido. Si después el programa lo lee o lo
escribe, lo detiene:

```cpp
std::vector<int> v = {1, 2, 3};
int* p = &v[0];      // puntero al primer elemento
v.push_back(4);      // sin espacio: el vector se muda y libera la memoria vieja
int x = *p;          // p apunta a memoria liberada: ASan dice ¡alto!
```

```text
ERROR: AddressSanitizer: heap-use-after-free
```

*Heap-use-after-free* = usaste memoria después de liberarla.

**Límite:** solo ve el bug si la memoria **realmente se liberó**. Si el
contenedor invalida algo pero conserva la memoria (por ejemplo, `vector::clear`
destruye los elementos pero no suelta el espacio), para ASan el acceso es legal.

## UBSan (Undefined Behavior Sanitizer)

Se activa junto con ASan (`-fsanitize=address,undefined`) y vigila **otros**
tipos de comportamiento indefinido: división por cero, desbordamiento de enteros,
etc. En este corpus no aportó detecciones propias (todas las de esta compilación
fueron `heap-use-after-free` de ASan); se activa porque no cuesta nada.

## Por qué se usan las dos

Ven cosas distintas, y a veces solo una nota el bug:

| Situación | Debug Mode | ASan |
|---|---|---|
| Iterador roto **y** memoria liberada | ✅ lo ve | ✅ lo ve |
| Iterador roto, memoria **no** liberada | ✅ lo ve | ❌ la memoria sigue siendo "legal" |
| Referencia o puntero a memoria liberada | ❌ no sigue referencias | ✅ lo ve |
| Referencia o puntero roto, memoria **no** liberada | ❌ | ❌ **nadie lo ve** |

La última fila explica la mayoría de los casos UB que ninguna herramienta
detectó: ver [¿Coincide con el estándar?](resultados/dinamica.md#coincide-con-el-estándar).

## Pruébalo tú

```cpp
// prueba.cpp
#include <vector>
#include <cstdio>
int main() {
    std::vector<int> v = {1, 2, 3};
    auto it = v.begin();
    v.clear();
    std::printf("%d\\n", *it);
}
```

```bash
g++ prueba.cpp -o normal && ./normal                      # imprime algo y "funciona"
g++ -D_GLIBCXX_DEBUG prueba.cpp -o debug && ./debug       # Debug Mode lo detiene
clang++ -fsanitize=address prueba.cpp -o asan && ./asan   # ASan probablemente NO lo ve
```

El tercero probablemente no diga nada, porque `clear()` no libera la memoria del
vector: es justo la diferencia entre las dos herramientas.
""")

write("metodologia.md", f"""
# Metodología

## Dimensiones

Cada caso es una tupla `(contenedor, operación, sostiene, forma, garantía)`:

| Dimensión | Valores |
|---|---|
| Contenedor | {", ".join(f"`{NOMBRE[c]}`" for c in contenedores)} |
| Operación mutadora | {n_pares} pares contenedor–operación |
| Sostiene (handle retenido) | `it` iterador, `ref` referencia, `ptr` puntero |
| Forma sintáctica | {", ".join(f"`{f}`" for f in FORMAS)} |
| Garantía (D-20) | `ninguna`; `reserva`: `reserve(size() + k)` antes; `devuelto`: el handle que devuelve la mutación |

Total: {n_pares} pares × 3 handles × 4 formas = **{n_pares * 12} casos** sin garantía,
más **{len(fns) - n_pares * 12}** casos de buen uso con garantía = **{len(fns)} casos**.

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
python3 bench/experimento.py      # dentro de la imagen checker:llvm21
python3 bench/pruebas_evaluacion.py
```

Una invocación de `clang++ --analyze -std=c++17` **por caso y por condición**
(`-analyze-function=<firma>`), con salida SARIF. La condición de referencia usa
los checkers

```text
{CHK}
```

y `aggressive-binary-operation-simplification=true`; las experimentales, los
mismos más el plugin. Ver [Experimento](resultados/experimento.md).

**Cotejo por sitio.** Un aviso se atribuye al caso cuya función lo contiene, y
al **handle** sobre el que cae: el sostenido (la línea de `sink(...)`) o el
iterador de control (la cabecera del `for`). En un caso `UB`, el aviso acierta
sólo si cae sobre un handle que la norma da por inválido.

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

Detectados / total de casos `UB` en cada celda, **por caso**: en `bucle` con
referencia o puntero cuenta el aviso sobre el iterador del `for`, que también
es inválido. Sobre el handle sostenido, CSA no detecta ninguna referencia ni
ningún puntero: ver [Experimento](experimento.md).

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


# ---- resultados: experimento ---------------------------------------------------
def fila_cond(nombre, a):
    pc = lambda x: "—" if x is None else f"{100 * x:.1f}%"
    return (f"| {nombre} | {a['tp']} | {a['fn']} | **{pc(a['recall'])}** | {pc(a['recallSostenido'])} | "
            f"{a['fp']} | {pc(a['precision'])} | {a['policyWarned']}/{a['policyWarned'] + a['policySilent']} | "
            f"{a['posiblesSobreSAFE']} | {a['incidents']} |")

def tabla_grupo(clave, valores, fmt=lambda v: f"`{v}`"):
    conds = ["Reference", "Plugin-Possibly"]
    filas = ["| Valor | UB | CSA | Plugin | CSA sobre el sostenido | SAFE | FP CSA | FP plugin |",
             "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for v in valores:
        r, q = (experimento["metricas"][c][clave].get(v) for c in conds)
        if not r:
            continue
        ub = r["tp"] + r["fn"]
        filas.append(f"| {fmt(v)} | {ub} | {r['tp']} | {q['tp']} | {r['ubEnSostenido']}/{r['ubSostenidoTotal']} | "
                     f"{r['fp'] + r['tn']} | {r['fp']} | {q['fp']} |")
    return "\n".join(filas)

em, et = experimento["meta"], experimento["tiempos"]
DESC_COND = {"Reference": "CSA: los checkers de base",
             "Experimental-Silent": "base + plugin, `PolicyMode=Silent`",
             "Experimental-Possibly": "base + plugin, `PolicyMode=Possibly`",
             "Plugin-Possibly": "`core`, `cplusplus` + plugin (sin `alpha.cplusplus`)"}
write("resultados/experimento.md", f"""
# Experimento: CSA frente al plugin

Generado por `bench/experimento.py` (el workflow «Ejecutar el experimento» de la
[Evaluación](../diseno/dsl/evaluacion.md)). Una invocación de `clang` por caso
y por condición; {len(fns)} casos × {len(et)} condiciones en {em['segundos_total']} s.

| Entorno | |
|---|---|
| Compilador | `{em['clang']}` |
| libstdc++ | `{em['libstdcxx']}` |
| Plugin (sha256) | `{em['plugin_sha256'][:16]}…` |
| Banco (sha256) | `{em['banco_sha256'][:16]}…` |
| Banco congelado | {em['banco_congelado'] or "**no**: `banco-1` espera el visto bueno del asesor (D-18, D-20)"} |

## Totales

| Condición | TP | FN | Cobertura por caso | Cobertura sobre el sostenido | FP | Precisión | `POLICY` con aviso | Posibles sobre `SAFE` | Incidentes |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
{chr(10).join(fila_cond(f"{n}<br><small>{DESC_COND[n]}</small>", experimento['metricas'][n]['All']) for n in et)}

- **Cobertura por caso:** el caso `UB` recibe un aviso confirmado sobre algún
  handle que la norma da por inválido. En `bucle` con referencia, puede ser el
  iterador del `for`.
- **Cobertura sobre el sostenido:** el aviso cae sobre el handle que el caso
  declara (la referencia, el puntero o el iterador). Es la que mide el dominio
  de referencias: CSA no avisa nunca sobre una referencia.
- Un aviso **posible** nunca es TP ni FP: se cuenta aparte.

**Por qué hay una condición `Plugin-Possibly`.** `alpha.cplusplus.InvalidatedIterator`
termina el camino (nodo de error fatal) en el mismo uso que vigila el plugin.
En base + plugin, el aviso de esos casos lo da CSA y el del plugin no llega a
emitirse: en la primera corrida, 54 casos `UB` sólo tenían el aviso de CSA.
Sin los checkers `alpha.cplusplus`, el plugin solo da la cifra de la última fila.

## Por forma

{tabla_grupo("forma", FORMAS)}

## Por handle

{tabla_grupo("sostiene", list(SOSTIENE), lambda v: f"`{v}` ({SOSTIENE[v]})")}

## Por contenedor

{tabla_grupo("contenedor", contenedores, lambda v: f"[`{NOMBRE[v]}`](../casos/{v}/index.md)")}

## Por garantía

{tabla_grupo("garantia", ["ninguna", "reserva", "devuelto"])}

## Ejecuciones

| Condición | Segundos (suma) | Completed | CompileError | Crash | Timeout | Unreadable |
|---|---:|---:|---:|---:|---:|---:|
{chr(10).join(f"| {n} | {v['segundos']} | " + " | ".join(str(v['outcomes'][o]) for o in ('Completed', 'CompileError', 'Crash', 'Timeout', 'Unreadable')) + " |" for n, v in et.items())}
""")


# ---- resultados: código real -----------------------------------------------------
if real:
    filas = ["| Proyecto | *Commit* | Unidades | Sin terminar | Confirmados | Posibles | Segundos (suma) |",
             "|---|---|---:|---:|---:|---:|---:|"]
    detalle = []
    for nombre, v in real["proyectos"].items():
        avs = [a for r in v["resultados"] for a in r["avisos"]]
        filas.append(f"| {nombre} | `{v['commit'][:7]}` | {v['unidades']} | {v['fallos']} | "
                     f"{sum(a['clase'] == 'confirmado' for a in avs)} | {sum(a['clase'] == 'posible' for a in avs)} | "
                     f"{v['segundos']} |")
        for r in v["resultados"]:
            rel = r["file"].split(f"/{nombre}/", 1)[-1]
            if r["codigo"]:
                causa = next((l for l in r["error"].splitlines() if "error" in l or "Assertion" in l), "")
                detalle.append(f"- **{nombre}** `{rel}`: no terminó. `{causa.strip()[:160]}`")
            vistos = set()
            for a in r["avisos"]:
                k = (a["line"], a["msg"])
                if k in vistos:  # la misma unidad compilada dos veces (biblioteca estática y compartida)
                    continue
                vistos.add(k)
                arch = a["file"].split(f"/{nombre}/", 1)[-1]
                detalle.append(f"- **{nombre}** `{arch}:{a['line']}` ({a['clase']}): {a['msg']}")
    sem = []
    if inyeccion:
        sem = ["| Id | Proyecto | Archivo | Mecanismo | Espera | Obtiene | |", "|---|---|---|---|---|---|---|"]
        sem += [f"| {x['id']} | {x['proyecto']} | `{x['archivo']}` | {x['mecanismo']} | {x['espera']} | "
                f"{x['obtenido']} | {'✔' if x['acierto'] else '✘'} |" for x in inyeccion]
    write("resultados/codigo-real.md", f"""
# Código real

Generado desde `test/codigo_real/` (`bench/codigo_real.py` y `bench/inyeccion.py`).
`PolicyMode={real['modo']}`, `-analyzer-inlining-mode={real['inlining']}` (D-22).
Sólo se guardan los avisos de `ucsm.ContainerInvalidation`.

{chr(10).join(filas)}

## Avisos y unidades que no terminaron

Cada aviso se revisó a mano; la revisión está en
[7.7 Estado actual](../construccion/7-7-estado.md).

{chr(10).join(detalle) or "Ninguno."}

## Defectos sembrados

{chr(10).join(sem)}
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


# ¿la ejecucion contradice alguna etiqueta?
alguno = lambda r: det(r, "libstdcxx_debug") or det(r, "asan_ubsan")
contra = [r for r in res if r["modo"] in ("natural", "preserve")
          and r["etiqueta_normativa"] in ("SAFE", "POLICY") and alguno(r)]
ub_nada = [r for r in res if r["etiqueta_normativa"] == "UB" and not alguno(r)]
force_nada = [r for r in res if r["modo"] == "force" and not alguno(r)]
def grupos_sin_det(rows):
    g = collections.OrderedDict()
    for r in rows:
        g.setdefault((r["contenedor"], r["op"], r["sostiene"]), []).append(r["fn"])
    filas = ["| Contenedor | Operación | Sostiene | Casos |", "|---|---|---|---|"]
    for (c, o, so), l in g.items():
        filas.append(f"| `{NOMBRE[c]}` | [`{o}`](../{pagina_op(c, o)}) | {SOSTIENE[so]} | {len(l)} |")
    return chr(10).join(filas)
n = lambda e, m: sum(1 for r in res if r["etiqueta_normativa"] == e and r["modo"] == m)
nd = lambda e, m: sum(1 for r in res if r["etiqueta_normativa"] == e and r["modo"] == m and alguno(r))
COINCIDE = f"""
## ¿Coincide con el estándar?

Las etiquetas salen del estándar C++17; la ejecución es una segunda opinión.
Las preguntas son dos: si la ejecución **contradice** alguna etiqueta y si
**confirma** las de bug.

### ¿Contradice alguna etiqueta?

Habría contradicción si un caso que llamamos seguro (`SAFE`, o `POLICY` en el
escenario `preserve`) mostrara un bug al ejecutarse.

| Grupo | Ejecuciones | Con detección |
|---|---:|---:|
| 🟢 `SAFE` | {n("SAFE", "natural")} | **{nd("SAFE", "natural")}** |
| 🟡 `POLICY` · `preserve` (no debería romperse) | {n("POLICY", "preserve")} | **{nd("POLICY", "preserve")}** |

**Contradicciones: {len(contra)}.** {"Ningún caso que el estándar considera seguro falló al ejecutarse." if not contra else "Hay casos que revisar: " + ", ".join(f"`{r['fn']}` ({r['modo']})" for r in contra)}

### ¿Confirma los bugs?

| Grupo | Ejecuciones | Detectados | Sin detección |
|---|---:|---:|---:|
| 🔴 `UB` | {n("UB", "natural")} | {nd("UB", "natural")} | {n("UB", "natural") - nd("UB", "natural")} |
| 🟡 `POLICY` · `force` (debería romperse) | {n("POLICY", "force")} | {nd("POLICY", "force")} | {n("POLICY", "force") - nd("POLICY", "force")} |

Los casos sin detección **no** contradicen al estándar. Que un bug no se
manifieste está permitido: es la definición de comportamiento indefinido. Lo que
muestran son los **límites de las herramientas** (ver
[Las herramientas de ejecución](../herramientas.md#por-qué-se-usan-las-dos)):

- **Referencias y punteros sin memoria liberada.** Por ejemplo, `vector::erase`,
  `vector::clear` o `deque::pop_front`: el estándar invalida la referencia, pero
  el contenedor conserva la memoria. Debug Mode no sigue referencias y ASan no ve
  memoria liberada, así que nadie lo nota.
- **Iteradores que Debug Mode no marca y cuya memoria no se libera.** Por
  ejemplo, `rehash`/`reserve` en contenedores `unordered`: el estándar invalida
  los iteradores, pero los nodos siguen en su sitio.

<details>
<summary>Casos UB sin detección dinámica, agrupados ({len(ub_nada)})</summary>

{grupos_sin_det(ub_nada)}

</details>

<details>
<summary>Casos POLICY · force sin detección, agrupados ({len(force_nada)})</summary>

{grupos_sin_det(force_nada)}

</details>

**Conclusión:** la ejecución no contradice ninguna etiqueta. Confirma
{nd("UB", "natural")} de {n("UB", "natural")} casos `UB`, y los no confirmados
corresponden a límites conocidos de las herramientas, no a errores del corpus.
"""
write("resultados/dinamica.md", f"""
# Validación dinámica

{AVISO_DIN}
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

{COINCIDE}

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
           f"| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |", "|---|---|---|---|---|",
           f"| {SOSTIENE[t['sostiene']]} | `{t['forma']}` | {etiqueta(t['esperado'])} | {veredicto_estatico(fn)} | "
           f"{VEREDICTO_PLUGIN[s['plugin']]} |", "",
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
                    cel.append("sin detección")
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

{len(lst_c)} casos ({len(ops[cn])} operaciones × 3 handles × 4 formas{f", más {len(lst_c) - len(ops[cn]) * 12} de buen uso con garantía" if len(lst_c) > len(ops[cn]) * 12 else ""}).
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
                  f"- Casos `UB` detectados estáticamente: {sum(map(avisa, u))}/{len(u)}", "",
                  "**En palabras:** " + en_palabras(cn, op), "",
                  "Mapa de los 12 casos. Cada celda muestra la respuesta correcta (etiqueta) y, debajo, "
                  "lo que hizo el analizador estático de Clang. Clic para ir al caso. "
                  "Ver [Cómo leer este libro](../../guia.md).", ""]
        mapa = ["| | " + " | ".join(f"`{f}`" for f in FORMAS) + " |", "|---|" + "---|" * 4]
        for so in SOSTIENE:
            celdas = []
            for fo in FORMAS:
                f = f"f_{cn}_{op}_{so}_{fo}"
                celdas.append(f"[{etiqueta(truth[f]['esperado'])}<br>{veredicto_estatico(f)}](#{f})")
            mapa.append(f"| **{SOSTIENE[so]}** | " + " | ".join(celdas) + " |")
        cuerpo += mapa + [""]
        for so in SOSTIENE:
            cuerpo += [f"## Handle: {SOSTIENE[so]}", ""]
            cuerpo += [bloque_caso(f"f_{cn}_{op}_{so}_{fo}") for fo in FORMAS]
        write(pagina_op(cn, op), "\n".join(cuerpo))
        summary_casos.append(f"    - [`{op}`]({pagina_op(cn, op)})")

GARANTIA = {"reserva": "`reserve(c.size() + k)` antes de las inserciones",
            "devuelto": "se usa el iterador que devuelve la mutación"}
cuerpo = ["# Casos de buen uso (garantías)", "",
          "Casos `SAFE` sobre mutaciones que **pueden** invalidar, escritos como lo haría "
          "quien conoce la norma ([D-20](../diseno/decisiones.md)). Miden los falsos positivos "
          "de un checker que avisara en todo `push_back` o todo `erase`.", ""]
for g, frase in GARANTIA.items():
    lst = [f for f in fns if truth[f].get("garantia") == g]
    cuerpo += [f"## `{g}`: {frase}", "", f"{len(lst)} casos; con aviso estático: {sum(map(avisa, lst))}.", "",
               "| Caso | Contenedor | Operación | Sostiene | Forma | Estático |", "|---|---|---|---|---|---|"]
    cuerpo += [f"| [`{f}`](#{f}) | `{truth[f]['contenedor']}` | `{truth[f]['op']}` | `{truth[f]['sostiene']}` | "
               f"`{truth[f]['forma']}` | {veredicto_estatico(f)} |" for f in lst]
    cuerpo += [""] + [bloque_caso(f) for f in lst]
write("casos/garantias.md", "\n".join(cuerpo))
summary_casos.append("  - [Buen uso (garantías)](casos/garantias.md)")

filas_idx = ["| # | Caso | Contenedor | Operación | Sostiene | Forma | Etiqueta | Estático | Dinámico |",
             "|---:|---|---|---|---|---|---|---|---|"]
for i, f in enumerate(fns, 1):
    t = truth[f]
    d = "🛑" if any(det(r, k) for r in dyn[f] for k in INSTR) else "—"
    filas_idx.append(f"| {i} | {enlace_caso(f)} | `{t['contenedor']}` | `{t['op']}` | `{t['sostiene']}` | "
                     f"`{t['forma']}` | {etiqueta(t['esperado'])} | {veredicto_estatico(f)} | {d} |")
write("indice.md", f"# Índice de casos\n\nLos {len(fns)} casos del corpus. *Dinámico* 🛑 = algún instrumento detectó el defecto en alguna ejecución.\n\n" + "\n".join(filas_idx))

write("SUMMARY.md", "\n".join([
    "# Resumen", "", "[Introducción](README.md)", "",
    "# Guía de uso", "",
    "- [En dos minutos](uso/index.md)",
    "  - [Levantar el checker](uso/checker.md)",
    "  - [Correr los bench](uso/bench.md)",
    "  - [Usar el corpus](uso/corpus.md)",
    "  - [Libro, informe y artículo](uso/documentos.md)",
    "  - [Dónde se valida cada requerimiento](uso/requerimientos.md)",
    "", "# Sistema: Centinela C++", "",
    "- [Qué es y cómo probarlo](sistema/index.md)",
    "  - [Requerimientos y casos de uso](sistema/requerimientos.md)",
    "  - [Modelo funcional del dominio](sistema/modelado.md)",
    "  - [Arquitectura](sistema/arquitectura.md)",
    "  - [Tipos que impiden errores](sistema/tipos.md)",
    "  - [Dónde va cada cosa](sistema/donde-va.md)",
    "  - [API HTTP](sistema/api.md)",
    "  - [Base de datos](sistema/datos.md)",
    "  - [El panel web](sistema/panel.md)",
    "  - [Pruebas](sistema/pruebas.md)",
    "  - [Ponerlo en marcha con GitHub](sistema/despliegue.md)",
    "", "# El corpus y su lectura", "", "- [Cómo leer este libro](guia.md)", "  - [Las herramientas de ejecución](herramientas.md)", "- [Metodología](metodologia.md)",
    "", "# Diseño del checker", "",
    "- [Por qué se rehízo el diseño](diseno/critica.md)",
    "- [La lógica de la detección](diseno/logica.md)",
    "- [Modelo del dominio (DSL)](diseno/dsl/index.md)",
    "  - [Norma](diseno/dsl/norma.md)",
    "  - [Detección](diseno/dsl/deteccion.md)",
    "  - [Evaluación](diseno/dsl/evaluacion.md)",
    "  - [Validación dinámica](diseno/dsl/validacion-dinamica.md)",
    "- [Significado y leyes](diseno/leyes.md)",
    "- [Decisiones de diseño](diseno/decisiones.md)",
    "- [Dónde va cada cosa](diseno/donde-va.md)",
    "- [Casos de uso del motor](diseno/casos-de-uso-motor.md)",
    "- [Portada, resumen y abstract](informe/portada.md)",
    "- [Capítulo 1 — Introducción y objetivos](informe/cap1.md)",
    "- [Capítulo 2 — Marco teórico, metodología y plan](informe/cap2.md)",
    "- [Capítulo 3 — Costo beneficio](informe/cap3.md)",
    "- [Capítulo 4 — Requerimientos](diseno/cap4/index.md)",
    "  - [4.1 Funcionales](diseno/cap4/4-1-funcionales.md)",
    "  - [4.2 No funcionales](diseno/cap4/4-2-no-funcionales.md)",
    "- [Capítulo 5 — Arquitectura](diseno/cap5/index.md)",
    "  - [5.1 Casos de uso](diseno/cap5/5-1-casos-de-uso.md)",
    "  - [5.2 Colaboración](diseno/cap5/5-2-colaboracion.md)",
    "  - [5.3 Paquetes](diseno/cap5/5-3-paquetes.md)",
    "  - [5.4 Clases](diseno/cap5/5-4-clases.md)",
    "  - [5.5 Estados](diseno/cap5/5-5-estados.md)",
    "  - [5.6 Arquitectura lógica](diseno/cap5/5-6-arquitectura-logica.md)",
    "  - [5.7 Arquitectura física](diseno/cap5/5-7-arquitectura-fisica.md)",
    "- [Capítulo 6 — Interfaces y datos](diseno/cap6/index.md)",
    "  - [6.1 Interfaz de usuario](diseno/cap6/6-1-interfaz.md)",
    "  - [6.2 Navegación](diseno/cap6/6-2-navegacion.md)",
    "  - [6.3 Mockups](diseno/cap6/6-3-mockups.md)",
    "  - [6.4 Descripción de la interfaz](diseno/cap6/6-4-descripcion-ui.md)",
    "  - [6.5 Interfaz de servicios](diseno/cap6/6-5-servicios.md)",
    "  - [6.6 Diagrama de servicios](diseno/cap6/6-6-diagrama-servicios.md)",
    "  - [6.7 Descripción de los servicios](diseno/cap6/6-7-descripcion-servicios.md)",
    "  - [6.8 Servicios consumidos](diseno/cap6/6-8-consumidos.md)",
    "  - [6.9 Modelo de base de datos](diseno/cap6/6-9-datos.md)",
    "- [Capítulo 7 — Construcción](construccion/index.md)",
    "  - [7.1 Código](construccion/7-1-codigo.md)",
    "  - [7.2 Base de datos](construccion/7-2-datos.md)",
    "  - [7.3 Control de versiones](construccion/7-3-versiones.md)",
    "  - [7.4 Calidad](construccion/7-4-calidad.md)",
    "  - [7.5 Componentes](construccion/7-5-componentes.md)",
    "  - [7.6 Plan de incrementos](construccion/7-6-incrementos.md)",
    "  - [7.7 Estado actual](construccion/7-7-estado.md)",
    "- [Capítulo 8 — Pruebas del software](pruebas/index.md)",
    "  - [8.1 Entorno de ejecución](pruebas/8-1-entorno.md)",
    "  - [8.2 Pruebas funcionales](pruebas/8-2-funcionales.md)",
    "  - [8.3 Casos de prueba](pruebas/8-3-casos-de-prueba.md)",
    "  - [8.4 Pruebas no funcionales](pruebas/8-4-no-funcionales.md)",
    "  - [8.5 Estrategia de despliegue](pruebas/8-5-despliegue.md)",
    "- [Glosario](informe/glosario.md)",
    "- [Referencias](informe/referencias.md)",
    "", "# Artículo", "",
    "- [Estructura y fuentes](articulo/index.md)",
    "  - [Trabajos relacionados y aporte](articulo/aportes.md)",
    "  - [El modelo en una figura](articulo/modelo.md)",
    "", "# El banco", "",
    "- [Reglas y escenarios](banco/reglas-escenarios.md)",
    "- [Protocolo de validación dinámica](banco/protocolo-dinamico.md)",
    "", "# Resultados", "",
    "- [Experimento: CSA frente al plugin](resultados/experimento.md)",
    *(["- [Código real](resultados/codigo-real.md)"] if real else []),
    "- [Análisis estático](resultados/estatico.md)",
    "  - [Catálogo de falsos negativos](resultados/fallos.md)",
    "- [Validación dinámica](resultados/dinamica.md)",
    "- [Matriz normativa](resultados/matriz.md)",
    *[f"  - [`{NOMBRE[c]}`](matriz/{c}.md)" for c in mcont],
    "", "# Casos del corpus", "",
    "- [Índice de casos](indice.md)",
    *summary_casos,
]))

# ---- paginas escritas a mano (libro/) y diagramas -------------------------------
# Una línea «{{codigo RUTA SÍMBOLO}}» se reemplaza por el fragmento del código
# fuente: la función, el TEST(Suite, Nombre) o el rango de líneas «10-20». Así
# el libro muestra siempre el código vigente, y si el símbolo desaparece el
# libro no se genera.
REPO_URL = "https://github.com/jasrod12ucsm/checker/blob/main"
LENGUAJE = {".cpp": "cpp", ".h": "cpp", ".py": "python", ".sh": "bash", ".txt": "cmake", ".yml": "yaml", ".json": "json",
            ".ts": "typescript", ".tsx": "typescript", ".sql": "sql"}


from fragmentos import fragmento  # noqa: E402


def con_codigo(texto):
    def reemplazo(m):
        ruta, simbolo = m.group(1), m.group(2).strip()
        ini, cuerpo = fragmento(ruta, simbolo)
        fin = ini + len(cuerpo) - 1
        lang = LENGUAJE.get(os.path.splitext(ruta)[1], "")
        if os.path.basename(ruta) == "CMakeLists.txt":
            lang = "cmake"
        return (f"[`{ruta}:{ini}`]({REPO_URL}/{ruta}#L{ini}-L{fin})\n\n"
                f"```{lang}\n" + "\n".join(cuerpo) + "\n```")
    return re.sub(r"^\{\{codigo (\S+) (.+?)\}\}$", reemplazo, texto, flags=re.M)


for raiz, _, archivos in os.walk("libro"):
    if raiz.startswith(os.path.join("libro", "diagramas")):
        continue
    for a in archivos:
        if a.endswith(".md"):
            dst = os.path.join(SRC, os.path.relpath(os.path.join(raiz, a), "libro"))
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            write_md = open(os.path.join(raiz, a), encoding="utf-8").read()
            open(dst, "w", encoding="utf-8").write(con_codigo(write_md))
svg = os.path.join("libro", "diagramas", "svg")
if os.path.isdir(svg):
    shutil.copytree(svg, os.path.join(SRC, "diagramas"))
mockups = os.path.join("libro", "mockups")
if os.path.isdir(mockups):
    shutil.copytree(mockups, os.path.join(SRC, "mockups"))
capturas = os.path.join("libro", "capturas")
if os.path.isdir(capturas):
    shutil.copytree(capturas, os.path.join(SRC, "capturas"))

print(f"{OUT}/src -> {len(fns)} casos, {n_pares} páginas de operación, {len(mcont)} páginas de matriz")
print(f"  mdbook serve {OUT} --open")
