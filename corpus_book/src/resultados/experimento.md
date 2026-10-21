
# Experimento: CSA frente al plugin

Generado por `bench/experimento.py` (el workflow «Ejecutar el experimento» de la
[Evaluación](../diseno/dsl/evaluacion.md)). Una invocación de `clang` por caso
y por condición; 750 casos × 4 condiciones en 130.8 s.

| Entorno | |
|---|---|
| Compilador | `Ubuntu clang version 21.1.8 (++20251221032922+2078da43e25a-1~exp1~20251221153059.70)` |
| libstdc++ | `13.3.0-6ubuntu2~24.04.1` |
| Plugin (sha256) | `0f7594b4983005a9…` |
| Banco (sha256) | `efe9a7f0c3d473fe…` |
| Banco congelado | banco-1 |

## Totales

| Condición | TP | FN | Cobertura por caso | Cobertura sobre el sostenido | FP | Precisión | `POLICY` con aviso | Posibles sobre `SAFE` | Incidentes |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Reference<br><small>CSA: los checkers de base</small> | 80 | 262 | **23.4%** | 14.6% | 0 | 100.0% | 0/102 | 0 | 0 |
| Experimental-Silent<br><small>base + plugin, `PolicyMode=Silent`</small> | 342 | 0 | **100.0%** | 100.0% | 0 | 100.0% | 0/102 | 0 | 0 |
| Experimental-Possibly<br><small>base + plugin, `PolicyMode=Possibly`</small> | 342 | 0 | **100.0%** | 100.0% | 0 | 100.0% | 102/102 | 0 | 0 |
| Plugin-Possibly<br><small>`core`, `cplusplus` + plugin (sin `alpha.cplusplus`)</small> | 342 | 0 | **100.0%** | 100.0% | 0 | 100.0% | 102/102 | 0 | 0 |

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

| Valor | UB | CSA | Plugin | CSA sobre el sostenido | SAFE | FP CSA | FP plugin |
|---|---:|---:|---:|---:|---:|---:|---:|
| `recto` | 82 | 0 | 82 | 0/82 | 77 | 0 | 0 |
| `guarda` | 82 | 16 | 82 | 16/82 | 77 | 0 | 0 |
| `bucle` | 96 | 48 | 96 | 16/82 | 75 | 0 | 0 |
| `llamada` | 82 | 16 | 82 | 16/82 | 77 | 0 | 0 |

## Por handle

| Valor | UB | CSA | Plugin | CSA sobre el sostenido | SAFE | FP CSA | FP plugin |
|---|---:|---:|---:|---:|---:|---:|---:|
| `it` (iterador) | 128 | 48 | 128 | 48/128 | 96 | 0 | 0 |
| `ref` (referencia) | 107 | 16 | 107 | 0/100 | 105 | 0 | 0 |
| `ptr` (puntero) | 107 | 16 | 107 | 0/100 | 105 | 0 | 0 |

## Por contenedor

| Valor | UB | CSA | Plugin | CSA sobre el sostenido | SAFE | FP CSA | FP plugin |
|---|---:|---:|---:|---:|---:|---:|---:|
| [`std::vector`](../casos/vector/index.md) | 48 | 10 | 48 | 6/48 | 38 | 0 | 0 |
| [`std::deque`](../casos/deque/index.md) | 72 | 30 | 72 | 18/64 | 26 | 0 | 0 |
| [`std::list`](../casos/list/index.md) | 36 | 5 | 36 | 3/36 | 74 | 0 | 0 |
| [`std::forward_list`](../casos/flist/index.md) | 24 | 5 | 24 | 3/24 | 24 | 0 | 0 |
| [`std::set`](../casos/set/index.md) | 24 | 5 | 24 | 3/24 | 25 | 0 | 0 |
| [`std::multiset`](../casos/mset/index.md) | 24 | 5 | 24 | 3/24 | 13 | 0 | 0 |
| [`std::map`](../casos/map/index.md) | 24 | 5 | 24 | 3/24 | 37 | 0 | 0 |
| [`std::multimap`](../casos/mmap/index.md) | 24 | 5 | 24 | 3/24 | 13 | 0 | 0 |
| [`std::unordered_set`](../casos/uset/index.md) | 36 | 5 | 36 | 3/32 | 25 | 0 | 0 |
| [`std::unordered_map`](../casos/umap/index.md) | 30 | 5 | 30 | 3/28 | 31 | 0 | 0 |

## Por garantía

| Valor | UB | CSA | Plugin | CSA sobre el sostenido | SAFE | FP CSA | FP plugin |
|---|---:|---:|---:|---:|---:|---:|---:|
| `ninguna` | 342 | 80 | 342 | 48/328 | 240 | 0 | 0 |
| `reserva` | 0 | 0 | 0 | 0/0 | 54 | 0 | 0 |
| `devuelto` | 0 | 0 | 0 | 0/0 | 12 | 0 | 0 |

## Ejecuciones

| Condición | Segundos (suma) | Completed | CompileError | Crash | Timeout | Unreadable |
|---|---:|---:|---:|---:|---:|---:|
| Reference | 521.7 | 750 | 0 | 0 | 0 | 0 |
| Experimental-Silent | 523.7 | 750 | 0 | 0 | 0 | 0 |
| Experimental-Possibly | 522.4 | 750 | 0 | 0 | 0 | 0 |
| Plugin-Possibly | 519.7 | 750 | 0 | 0 | 0 | 0 |
