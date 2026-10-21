# Dónde se valida cada requerimiento

Cada requerimiento del [capítulo 4](../diseno/cap4/index.md) está en una
parte del código y se demuestra con una prueba que se puede correr. Esta
página muestra las dos cosas, con el código tal como está hoy en el
repositorio: los fragmentos se copian del código fuente cada vez que se
genera el libro.

Todos se comprueban juntos con:

```bash
docker compose run --rm verificar
```

## Tres tipos de prueba

| Tipo | Dónde | Qué prueba | Cómo se corre |
|---|---|---|---|
| **gtest** (C++) | `plugin/tests/dominio/LeyesTest.cpp` | el núcleo puro: la norma, las posiciones, la validez, las garantías. 40 pruebas | `./build/plugin/dominio_tests` |
| **lit** (C++ dentro de `clang`) | `plugin/tests/lit/*.cpp` | el checker de verdad, cargado en `clang`: cada `// expected-warning {{…}}` dice el aviso exacto que debe salir en esa línea, y una línea sin comentario no debe dar aviso (`-verify`). 5 archivos, 30 avisos | `lit build/plugin/tests/lit` |
| **arnés** (Python) | `bench/` | lo que no es un caso suelto sino una **medición**: correr el banco de 750 casos, contar aciertos, comparar con CSA solo, medir tiempo y memoria | `python3 bench/experimento.py` y los scripts de abajo |

Los requerimientos de lo que hace el checker (RF-01 a RF-12, RF-17) se
demuestran con gtest y `lit`. Los de la evaluación y la calidad medida (RF-13
a RF-15, RNF-01 a RNF-05) no se pueden escribir como un test de un caso: se
demuestran midiendo, con el arnés.

## Resumen

| Requerimiento | Se implementa en | Se demuestra con |
|---|---|---|
| [RF-01](#rf-01-registrar-el-checker) | `plugin/registro/Plugin.cpp` | `lit` `registro.cpp` |
| [RF-02](#rf-02-activar-y-desactivar-el-checker) | `bench/experimento.py` `Condicion` | experimento: las condiciones difieren solo en el checker |
| [RF-03](#rf-03-analizar-un-proyecto-desde-su-base-de-compilación) | `bench/codigo_real.py` `analizar` | `ejemplos/` en `verificar`; los 4 proyectos reales |
| [RF-04](#rf-04-elegir-la-política-ante-lo-que-depende-del-estado) | `Plugin.cpp` `registerInvalidation`, `Decisions.cpp` `onUse` | gtest `NoResueltoNuncaSeInformaComoConfirmado`; `lit` `garantias.cpp` |
| [RF-05](#rf-05-seguir-iteradores) | `acl/ClangRecognizer.cpp`, `checker/InvalidationChecker.cpp` | `lit` `iteradores.cpp` |
| [RF-06](#rf-06-seguir-referencias-y-punteros-a-elementos) | `ClangRecognizer.cpp` `elementAccess`, `InvalidationChecker::checkLocation` | `lit` `referencias.cpp` |
| [RF-07](#rf-07-no-avisar-en-los-usos-válidos) | `Decisions.cpp` `onUse` | gtest `LoValidoNoSeReporta`; `lit`; `ejemplos/buen_uso.cpp` |
| [RF-08](#rf-08-aplicar-la-regla-de-c17) | `NormTable.cpp` `effectOf`, `Decisions.cpp` `apply` | gtest `Banco.ElVeredictoDelNucleoEsLaEtiqueta` |
| [RF-09](#rf-09-tratar-lo-que-depende-del-estado) | `Decisions.cpp` `answer`, `consume`; `ClangRecognizer.cpp` `sizePlus` | gtest `ConGarantiaDependerEsPreservar`; `lit` `garantias.cpp` |
| [RF-10](#rf-10-tratar-las-llamadas-opacas) | `Decisions.cpp` `escape`, `InvalidationChecker::checkRegionChanges` | gtest `EscaparOlvidaLoQueNoEstaInvalidado`; `lit` `garantias.cpp` |
| [RF-11](#rf-11-explicar-la-causa-en-el-aviso) | `checker/Messages.cpp` | el texto de cada `expected-warning` |
| [RF-12](#rf-12-mostrar-la-ruta-del-defecto) | `InvalidationChecker.cpp` `transition` | `lit` `rutas.cpp` |
| [RF-13](#rf-13-ejecutar-el-experimento) | `bench/experimento.py` `ejecutar` | el experimento (muestra en `verificar`) |
| [RF-14](#rf-14-cotejar-por-sitio) | `experimento.py` `atribuir`, `cotejar` | `bench/pruebas_evaluacion.py` |
| [RF-15](#rf-15-generar-y-validar-el-banco) | `bench/gen_corpus.py`, `bench/run_runtime_validation.py` | sello `banco-1.json`; validación dinámica |
| [RF-16](#rf-16-construir-y-verificar-el-plugin) | `plugin/CMakeLists.txt` | el build y sus pruebas |
| [RF-17](#rf-17-mantener-la-norma-como-datos) | `norma/matriz.json`, `norma/gen_tabla.py` | `gen_tabla.py` al construir; gtests `Norma.*` |
| [RNF-01 a RNF-03](#rnf-01-a-rnf-03-precisión-cobertura-y-robustez) | todo el checker | `bench/regresion.py` sobre el experimento |
| [RNF-04 y RNF-05](#rnf-04-y-rnf-05-tiempo-y-memoria) | — | `bench/rendimiento.py` |
| [RNF-06](#rnf-06-claridad-del-diagnóstico) | `checker/Messages.cpp` | gtest `CadaRazonDeNoResueltoDiceQueFalta`; `lit` |
| [RNF-07](#rnf-07-mantenibilidad) | `plugin/CMakeLists.txt` | el núcleo compila sin Clang |
| [RNF-08](#rnf-08-reproducibilidad) | `experimento.py` `verificar` | `meta` de `metricas.json` |
| [RN-001 a RN-007](#reglas-de-negocio) | `bench/etiquetar.py`, `bench/experimento.py` | `bench/pruebas_evaluacion.py` |

---

## Requerimientos funcionales

### RF-01 Registrar el checker

El plugin se carga en `clang` y aparece en el catálogo de CSA como
`ucsm.ContainerInvalidation`, con sus opciones `PolicyMode` y `Debug`.

**Se implementa en:**

{{codigo plugin/registro/Plugin.cpp clang_registerCheckers}}

**Se demuestra con** la prueba `lit` `registro.cpp`, que pide a `clang` la
lista de checkers y de opciones y busca el nombre con `FileCheck`:

{{codigo plugin/tests/lit/registro.cpp 1-5}}

### RF-02 Activar y desactivar el checker

El checker se activa con `-analyzer-checker` y se carga con `-load`, sin
recompilar `clang`. En el experimento, las condiciones con y sin checker
**solo** difieren en esas opciones (RN-002):

{{codigo bench/experimento.py Condicion}}

**Se demuestra con** el experimento: `metricas.json` guarda en
`meta.condiciones` la línea de órdenes de cada condición, y las cuatro
condiciones corren sobre el mismo banco con el mismo `clang`. En `verificar`,
el paso del experimento lo hace sobre una muestra.

### RF-03 Analizar un proyecto desde su base de compilación

Para cada entrada de `compile_commands.json`, una invocación de `clang` con
las mismas opciones del proyecto más el checker:

{{codigo bench/codigo_real.py analizar}}

**Se demuestra con** `ejemplos/`, un proyecto CMake de dos archivos que
`verificar` analiza así. Debe dar un aviso confirmado y uno posible en
`prueba.cpp`, y ninguno en `buen_uso.cpp`:

```bash
python3 bench/codigo_real.py . build/verificacion/ejemplos.json Possibly noredundancy ejemplos
# ejemplos: 2 TU, 2 avisos, 0 TU con error, 0.5 s
```

A escala, con los cuatro proyectos reales (781 unidades): ver
[Correr los bench](bench.md#código-real).

### RF-04 Elegir la política ante lo que depende del estado

`PolicyMode=Silent` (por omisión) solo da avisos confirmados;
`PolicyMode=Possibly` da también los posibles. La opción se lee al registrar
el checker:

{{codigo plugin/registro/Plugin.cpp registerInvalidation}}

y decide el veredicto al usar un handle no resuelto:

{{codigo plugin/dominio/Decisions.cpp onUse}}

**Se demuestra con** el gtest:

{{codigo plugin/tests/dominio/LeyesTest.cpp Deteccion, NoResueltoNuncaSeInformaComoConfirmado}}

y con `lit` `garantias.cpp`, que corre con `PolicyMode=Possibly` (`%possibly`
en su línea `RUN`):

{{codigo plugin/tests/lit/garantias.cpp no_guarantee}}

### RF-05 Seguir iteradores

El checker registra un iterador al obtenerlo (`begin()`, `find()`,
`insert().first`…) y lo vigila al desreferenciarlo, moverlo o compararlo.

{{codigo plugin/acl/ClangRecognizer.cpp iteratorObtention}}

{{codigo plugin/checker/InvalidationChecker.cpp InvalidationChecker::use}}

**Se demuestra con** `lit` `iteradores.cpp`:

{{codigo plugin/tests/lit/iteradores.cpp vector_iter_deref}}

{{codigo plugin/tests/lit/iteradores.cpp copy_carries_state}}

### RF-06 Seguir referencias y punteros a elementos

Una referencia o un puntero a un elemento se registra al obtenerlo (`*it`,
`&*it`, `c[i]`, `front()`) y se vigila cuando se lee la memoria del elemento:

{{codigo plugin/acl/ClangRecognizer.cpp elementAccess}}

{{codigo plugin/checker/InvalidationChecker.cpp InvalidationChecker::checkLocation}}

**Se demuestra con** `lit` `referencias.cpp`. CSA solo no detecta ninguno de
estos:

{{codigo plugin/tests/lit/referencias.cpp vector_erase_ref}}

{{codigo plugin/tests/lit/referencias.cpp vector_clear_ptr}}

### RF-07 No avisar en los usos válidos

Un handle válido no produce aviso en ningún modo (primera línea de `onUse`,
en [RF-04](#rf-04-elegir-la-política-ante-lo-que-depende-del-estado)).

**Se demuestra con** el gtest:

{{codigo plugin/tests/dominio/LeyesTest.cpp Deteccion, LoValidoNoSeReporta}}

con las funciones de `lit` sin `expected-warning` (con `-verify`, un aviso
no esperado hace fallar la prueba):

{{codigo plugin/tests/lit/iteradores.cpp erase_idiom}}

y con `ejemplos/buen_uso.cpp`, que `verificar` analiza y debe quedar sin
avisos:

{{codigo ejemplos/buen_uso.cpp lista_estable}}

En el banco: 0 avisos confirmados en los 306 casos `SAFE`.

### RF-08 Aplicar la regla de C++17

El efecto de una mutación sobre un handle sale de la tabla generada desde
`norma/matriz.json`, según contenedor, operación, categoría y relación con el
punto:

{{codigo plugin/dominio/NormTable.cpp effectOf}}

{{codigo plugin/dominio/Decisions.cpp apply}}

**Se demuestra con** el gtest que recorre todas las celdas del banco (57
pares × 3 categorías + 12 con `reserve`) y compara el veredicto del núcleo
con la etiqueta que calcula `bench/etiquetar.py`, la otra implementación de
la norma:

{{codigo plugin/tests/dominio/LeyesTest.cpp Banco, ElVeredictoDelNucleoEsLaEtiqueta}}

### RF-09 Tratar lo que depende del estado

Cuando la norma dice «depende de la capacidad» o «del *rehash*», el checker
no inventa la capacidad: busca una garantía. `c.reserve(c.size() + k)` da
crédito para `k` inserciones:

{{codigo plugin/acl/ClangRecognizer.cpp sizePlus}}

{{codigo plugin/dominio/Decisions.cpp answer}}

{{codigo plugin/dominio/Decisions.cpp consume}}

**Se demuestra con** los gtests de crédito:

{{codigo plugin/tests/dominio/LeyesTest.cpp Deteccion, ConGarantiaDependerEsPreservar}}

{{codigo plugin/tests/dominio/LeyesTest.cpp Deteccion, UnaInsercionGastaUnCredito}}

y con `lit`: dos inserciones con crédito para una dan aviso posible en la
segunda:

{{codigo plugin/tests/lit/garantias.cpp reserved}}

{{codigo plugin/tests/lit/garantias.cpp reserved_too_little}}

### RF-10 Tratar las llamadas opacas

Si el contenedor pasa a una función cuyo cuerpo no se analiza, los handles
válidos o no resueltos dejan de seguirse; uno ya inválido sigue avisando:

{{codigo plugin/dominio/Decisions.cpp escape}}

{{codigo plugin/checker/InvalidationChecker.cpp InvalidationChecker::checkRegionChanges}}

**Se demuestra con:**

{{codigo plugin/tests/dominio/LeyesTest.cpp Deteccion, EscaparOlvidaLoQueNoEstaInvalidado}}

{{codigo plugin/tests/lit/garantias.cpp escaped}}

{{codigo plugin/tests/lit/garantias.cpp escaped_after_invalid}}

### RF-11 Explicar la causa en el aviso

El aviso nombra la categoría del handle, la operación que lo invalidó y su
línea; el posible dice además qué garantía falta:

{{codigo plugin/checker/Messages.cpp confirmed}}

{{codigo plugin/checker/Messages.cpp possibly}}

**Se demuestra con** el texto de cada `expected-warning` en `lit`, que se
compara palabra por palabra. Por ejemplo:

{{codigo plugin/tests/lit/garantias.cpp pop_back_first}}

### RF-12 Mostrar la ruta del defecto

Cada paso relevante deja una nota en la ruta (`NoteTag`): dónde se obtuvo el
handle y qué lo invalidó:

{{codigo plugin/checker/InvalidationChecker.cpp transition}}

**Se demuestra con** `lit` `rutas.cpp`, que corre con
`-analyzer-output=text` y comprueba cada nota con `expected-note`:

{{codigo plugin/tests/lit/rutas.cpp ruta_iterador}}

### RF-13 Ejecutar el experimento

Una invocación de `clang` por caso y condición, con tiempo límite y medición
de memoria; cada resultado es un `Completed` o un incidente:

{{codigo bench/experimento.py ejecutar}}

**Se demuestra con** la ejecución misma: `verificar` corre 81 casos × 4
condiciones; `docker compose run --rm experimento` los 750 (3 000
ejecuciones, 0 incidentes).

### RF-14 Cotejar por sitio

Un aviso cuenta solo si cae en la función del caso, y acierta solo si cae
sobre un handle que la norma da por inválido (RN-006):

{{codigo bench/experimento.py atribuir}}

{{codigo bench/experimento.py cotejar}}

**Se demuestra con** las 11 leyes de `bench/pruebas_evaluacion.py`, que
prueban el cotejo con datos escritos a mano, sin `clang`:

{{codigo bench/pruebas_evaluacion.py "cotejo por sitio: el aviso sobre el control cuenta si el control es UB"}}

{{codigo bench/pruebas_evaluacion.py "cotejo por sitio: el aviso sobre un handle SAFE no es un acierto"}}

### RF-15 Generar y validar el banco

El banco se genera desde la norma (ver [Usar el corpus](corpus.md)):

{{codigo bench/gen_corpus.py cuerpo}}

y cada caso se ejecuta con los dos oráculos dinámicos:

{{codigo bench/run_runtime_validation.py observe}}

**Se demuestra con** dos pasos. `verificar` regenera el banco y comprueba que
su sha256 es el del sello `test/banco-1.json`. `verificar --completo` corre
la validación dinámica (852 ejecuciones) y falla si algún caso `SAFE` tiene
una detección.

### RF-16 Construir y verificar el plugin

{{codigo plugin/CMakeLists.txt 21-33}}

**Se demuestra con** el primer paso de `verificar` (o
`docker compose run --rm plugin`): construye el plugin y corre las 40 gtests
y los 5 `lit`.

### RF-17 Mantener la norma como datos

Las reglas viven en `norma/matriz.json`, cada una con su cláusula de C++17.
`gen_tabla.py` comprueba sus leyes antes de generar la tabla y, si una se
rompe, no la genera:

{{codigo norma/gen_tabla.py check_leyes}}

**Se demuestra con** el build (que llama a `gen_tabla.py`) y con los gtests
`Norma.*`:

{{codigo plugin/tests/dominio/LeyesTest.cpp Norma, LaTablaEsTotal}}

{{codigo plugin/tests/dominio/LeyesTest.cpp Norma, InvalidarODependerCitaSuClausula}}

---

## Requerimientos no funcionales

### RNF-01 a RNF-03: precisión, cobertura y robustez

| | Criterio |
|---|---|
| RNF-01 | 0 avisos confirmados sobre casos `SAFE` |
| RNF-02 | detectar más que CSA solo, en el caso y sobre el handle retenido |
| RNF-03 | `clang` nunca aborta; lo que no termina se registra como incidente |

**Se demuestra con** `bench/regresion.py`. Sobre el banco completo exige los
mínimos de `bench/regresion.json` (342 UB, 328 sobre el handle retenido, 0
falsos positivos, 0 incidentes):

{{codigo bench/regresion.py banco_completo}}

y sobre la muestra de `verificar`, que con el checker no quede ningún UB sin
detectar, ningún falso positivo ni incidente, y que los `POLICY` reciban
aviso posible solo en `Possibly`:

{{codigo bench/regresion.py muestra}}

### RNF-04 y RNF-05: tiempo y memoria

El checker no puede subir la mediana del tiempo por caso más de 10 % ni la
memoria residente máxima más de 5 %, frente a CSA sin él.

**Se demuestra con** `bench/rendimiento.py`, que lee las ejecuciones que
guardó el experimento (`test/experimento/ejecucion.json`):

{{codigo bench/rendimiento.py main}}

```text
RNF-04 tiempo mediano por caso: 0.650 s → 0.652 s (+0.3 %, umbral 10 %)
RNF-05 memoria residente máxima: 119.1 MB → 119.9 MB (+0.7 %, umbral 5 %)
```

### RNF-06: claridad del diagnóstico

Todo aviso nombra handle, contenedor, operación y línea (RF-11); el posible
dice qué falta.

**Se demuestra con:**

{{codigo plugin/tests/dominio/LeyesTest.cpp Deteccion, CadaRazonDeNoResueltoDiceQueFalta}}

### RNF-07: mantenibilidad

El núcleo no conoce Clang: el *target* `ucsm_dominio` no recibe las
cabeceras de Clang, así que un `#include` de Clang en `plugin/dominio/` no
compila. Corregir una regla es editar `matriz.json`, sin tocar C++.

{{codigo plugin/CMakeLists.txt 29-33}}

**Se demuestra con** el build mismo y con los gtests, que enlazan solo contra
`ucsm_dominio`.

### RNF-08: reproducibilidad

Cada ejecución del experimento registra las versiones de `clang` y de
libstdc++ y el sha256 del plugin y del banco, y se niega a correr con un
banco sin sello:

{{codigo bench/experimento.py verificar}}

---

## Reglas de negocio

| Regla | Se implementa en | Se demuestra con |
|---|---|---|
| RN-001 La etiqueta es el peor efecto de los handles del caso | `bench/etiquetar.py` `por_handle`, `etiqueta` | ley «la etiqueta es el JOIN de sus handles» |
| RN-002 Las condiciones difieren solo en el checker | `experimento.py` `Condicion` | `meta.condiciones` de `metricas.json` |
| RN-003 Lo que depende del estado nunca es confirmado | `Decisions.cpp` `onUse` | gtest `NoResueltoNuncaSeInformaComoConfirmado` |
| RN-004 Un aviso posible no es acierto ni falso positivo | `experimento.py` `cotejar` | ley «un aviso posible no es un acierto ni un falso positivo» |
| RN-005 Un fallo es un incidente, no un verdadero negativo | `experimento.py` `ejecutar`, `cotejar` | ley «un fallo nunca es un verdadero negativo» |
| RN-006 Un aviso acierta solo sobre un handle inválido | `experimento.py` `cotejar` | leyes de cotejo por sitio |
| RN-007 Cada resultado lleva versiones y sha256 | `experimento.py` `verificar` | `meta` de `metricas.json` |

Las leyes de RN-001, RN-004 y RN-005:

{{codigo bench/pruebas_evaluacion.py "la etiqueta es el JOIN de sus handles (matriz completa)"}}

{{codigo bench/pruebas_evaluacion.py "un aviso posible no es un acierto ni un falso positivo"}}

{{codigo bench/pruebas_evaluacion.py "un fallo nunca es un verdadero negativo"}}
