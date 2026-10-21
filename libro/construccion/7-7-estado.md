# 7.7 Estado actual (2026-10-20)

| Pieza | Estado | Dónde |
|---|---|---|
| Banco de 750 casos con etiquetas C++17 | **hecho**: 27 etiquetas corregidas (D-18) y 66 casos de buen uso (D-20) | `test/corpus.cpp`, `test/corpus_truth.json`, `bench/gen_corpus.py`, `bench/etiquetar.py` |
| Medición de CSA (condición de referencia) | **hecho**: 80 de 342 UB por caso (23.4 %), 48 sobre el handle sostenido (14.6 %), 0 FP, con libstdc++ 13 | `bench/experimento.py`, [Experimento](../resultados/experimento.md) |
| Validación dinámica de las etiquetas | **hecho**: 852 ejecuciones, 0 contradicciones | `bench/run_runtime_validation.py`, [Validación dinámica](../resultados/dinamica.md) |
| Libro único (mdbook) | **hecho** | `corpus_book/` (generado) + `libro/` |
| Diseño del checker (capítulos 5 y 7, DSL, lógica) | **hecho** | `libro/diseno/` |
| **I0** imagen `checker:llvm21`, plugin registrado, `lit` | **hecho** | `Dockerfile`, `plugin/registro/`, `plugin/tests/lit/registro.cpp` |
| **I1** `norma/matriz.json` + `gen_tabla.py` + núcleo + leyes | **hecho**: 101 mutaciones, 348 reglas, 40 pruebas en verde; 92.5 % de líneas del núcleo cubiertas | `norma/`, `plugin/dominio/`, `plugin/tests/dominio/` |
| **I2** referencias y punteros desde `*it`, `c[i]`, `front()` | **hecho** | `plugin/acl/`, `plugin/checker/` |
| **I3** posiciones, anclas, `++it`, copia, `it = c.erase(it)`, `erase(first, last)` (D-23) | **hecho**, probado en código real | `plugin/tests/lit/iteradores.cpp` |
| **I4** crédito de `reserve`, `PolicyMode=Possibly`, escape (D-21) | **hecho** | `plugin/tests/lit/garantias.cpp` |
| **I5** notas de ruta | **hecho**: nota en la obtención y en la mutación (obtención → mutación → uso) | `plugin/checker/Messages.cpp`, `plugin/tests/lit/rutas.cpp` |
| Código real con defectos sembrados | **hecho**: 10 de 10 semillas con D-22; 4 proyectos, 781 unidades | `bench/codigo_real.py`, `bench/inyeccion.py`, [Código real](../resultados/codigo-real.md) |
| Arnés por etapas con SARIF y cotejo por sitio | **hecho** (D-24, D-25): 750 casos × 4 condiciones, 11 leyes probadas | `bench/experimento.py`, `bench/pruebas_evaluacion.py` |
| CI en GitHub Actions | **hecho**: plugin, calidad (formato, `mypy`, cobertura) y banco con regla de regresión; los tres pasos pasan con la misma imagen en local | `.github/workflows/ci.yml`, `docker-compose.yml`, `bench/regresion.py` |
| Verificación de los requerimientos en un paso | **hecho**: `docker compose run --rm verificar` construye el plugin y demuestra RF-01 a RF-17, RNF-01 a RNF-08 y RN-001 a RN-007 en unos 30 s; `--completo` corre el banco entero y la validación dinámica. RNF-04 y RNF-05 tienen ahora su comprobación automática | `verificar.sh`, `bench/rendimiento.py`, [Dónde se valida cada requerimiento](../uso/requerimientos.md) |
| Banco congelado `banco-1` | **hecho**: sello sha256 en `test/banco-1.json`, verificado en cada experimento; falta el visto bueno del asesor a D-18 y D-20 | `test/banco-1.json` |

## El banco corregido

`bench/experimento.py`: una invocación de `clang` por caso y por condición,
SARIF, cotejo por sitio (D-24). Imagen `checker:llvm21`:

| Condición | UB por caso | UB sobre el sostenido | FP sobre SAFE | `POLICY` con aviso posible | posibles sobre SAFE |
|---|---:|---:|---:|---:|---:|
| CSA (referencia) | 80/342 (23.4 %) | 48/328 (14.6 %) | 0 | — | — |
| base + plugin, `Silent` | **342/342** | **328/328** | **0** | 0 de 102 | 0 |
| base + plugin, `Possibly` | **342/342** | **328/328** | **0** | **102 de 102** | **0** |
| plugin sin `alpha.cplusplus` (D-25) | **342/342** | **328/328** | **0** | **102 de 102** | **0** |

Los 66 casos de buen uso (54 con `reserve(c.size() + k)`, 12 con el iterador
devuelto) no reciben ningún aviso, ni siquiera posible.

**Por qué CSA pasó de 48 a 80.** El banco no cambió: cambió el cotejo. Los 32
casos de diferencia son `bucle` con referencia o puntero donde la mutación
invalida **también** el iterador del `for`. CSA avisa sobre ese iterador. El
caso es `UB` por la norma (la etiqueta es el JOIN de sus handles), así que el
aviso acierta. Pero CSA sigue sin ver la referencia: sobre el handle
sostenido, la cifra es la de siempre, 48.

**Qué significa:** el plugin cumple la norma sobre el banco. **No** demuestra
que funcione en código ajeno: el banco lo escribimos nosotros, con las mismas
formas que el plugin sabe reconocer. Por eso existen las dos pruebas que siguen.

**Sensibilidad a la biblioteca.** Con libstdc++ 16, CSA detecta 109 UB en el
cotejo viejo; con libstdc++ 13, 48. La imagen fija la biblioteca, y la versión
queda en `test/experimento/metricas.json` ([riesgos](../diseno/decisiones.md#riesgos-que-las-decisiones-no-eliminan)).

## Código real

Cuatro proyectos, cada uno en un *commit* fijo, analizados unidad por unidad
con su `compile_commands.json`, `PolicyMode=Possibly` e inlining `all` (D-22).
**RocksDB** es el proyecto grande: 682 unidades, STL por todas partes. El
kernel de Linux no sirve para esta prueba: está escrito en C y no tiene
contenedores de la STL, así que daría 0 avisos sin probar nada.

| Proyecto | *Commit* | Unidades | Sin compilar | Confirmados | Posibles | Tiempo (`all`) |
|---|---|---:|---:|---:|---:|---:|
| ninja 1.12.1 | `2daa09b` | 29 | 1 | 0 | 1 | 130 s |
| leveldb 1.23 | `99b3c03` | 39 | 0 | 0 | 0 | 72 s |
| yaml-cpp 0.8.0 | `f732014` | 31 | 0 | 0 | 0 | 82 s |
| **RocksDB 9.7.4** | `3c27a3d` | **682** | 0 | 0 | 0 | 9 451 s (~14 min con 12 procesos) |

`browse.cc` necesita una cabecera que genera el *build*. El único aviso, en
`MissingDependencyScanner::PathExistsBetween`, es un **falso positivo
posible**: la llamada recursiva repite `find(from)`, y el motor no sabe que
`from` ya se insertó. Por eso explora un `insert` que en la realidad nunca
ocurre. Es un camino imposible porque no modelamos el contenido del contenedor.

Las corridas en código real destaparon errores que el banco no tenía:

| Síntoma en código real | Causa | Arreglo |
|---|---|---|
| FP en yaml-cpp con `c.erase(std::next(it))` | la copia del argumento cae en el parámetro de `erase` | buscar el iterador en `getParameterLocation`; anclas para posiciones que no se saben medir |
| 8 posibles en ninja por `printf("%p", edge)` | el escape por el objeto contenedor pasaba todo a `Unresolved` | D-21: el escape olvida lo válido |
| S7 y S8 sin aviso | `noredundancy` no reanaliza lo ya inlinado | D-22: `-analyzer-inlining-mode=all` |
| S8 sin aviso aun con `all` | `p->m()` y `f(p->x)` con parámetro referencia no contaban como uso | dos usos nuevos en `preCall` |
| RocksDB: 4 avisos confirmados en `range_tombstone_fragmenter.cc`, **falsos** | `erase(begin, it)` se leía como `erase(begin)`; con `it == begin()`, `it` «se borraba» | D-23: relación frente al rango semiabierto |
| RocksDB: 4 unidades abortan `clang` | `c[i]` con una constante que no cabe en `int64` (`getExtValue`) | `smallConstantOf`: distancia desconocida |

## Defectos sembrados

Cada semilla cambia unas pocas líneas de un proyecto real. Se analiza el
archivo antes y después, y se atribuye el aviso **nuevo**:

| Id | Proyecto | Mecanismo | Espera | `noredundancy` | `all` |
|---|---|---|---|---|---|
| S1 | ninja `build.cc` | `map::erase` libera el nodo y luego se lee `e->second` (M5) | confirmado | ✔ | ✔ |
| S2 | ninja `build.cc` | `map::erase` y lectura posterior por el iterador (M5) | confirmado | ✔ | ✔ |
| S3 | ninja `missing_deps.cc` | `unordered_map::clear` tras `insert(...).first` (M5) | confirmado | ✔ | ✔ |
| S4 | ninja `graph.cc` | referencia al frente de un `deque` y `pop_front` (M5) | confirmado | ✔ | ✔ |
| S5 | ninja `build_log.cc` | `unordered_map::erase` en el recorrido y `++i` (M5) | confirmado | ✔ | ✔ |
| S6 | yaml-cpp `node_data.cpp` | `list::erase` y `++it` sobre el borrado (M5) | confirmado | ✔ | ✔ |
| S7 | leveldb `db_impl.cc` | puntero a elemento de `vector` y `push_back` sin `reserve` (M1) | posible | ✔ | ✔ |
| S8 | ninja `graph.cc` | puntero a `back()` y `pop_back` (M3) | confirmado | ✘ | ✔ |
| B1 | leveldb `db_impl.cc` | S7 con `reserve(size() + 1)` antes | nada | ✔ | ✔ |
| B2 | ninja `build_log.cc` | `i = erase(i)` | nada | ✔ | ✔ |

**Límite de esta prueba:** las semillas también las escribimos nosotros. Lo
que muestran es que el plugin **sigue funcionando** dentro de código que no
diseñamos, con sus macros, su herencia y su presupuesto de CSA. No es una tasa
de detección sobre defectos reales.
