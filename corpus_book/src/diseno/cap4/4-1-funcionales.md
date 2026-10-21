# 4.1 Requerimientos funcionales

## Requerimientos de software

### a) Propósito

Especificar las capacidades del checker `ucsm.ContainerInvalidation`, de la
norma que lo alimenta y del banco y el arnés que lo evalúan, tal como están
construidos. Cada requisito se acompaña de la orden o la prueba que lo
demuestra y de la evidencia registrada.

### b) Componentes

| Componente | Qué es | Quién lo usa |
|---|---|---|
| **Checker** `ucsm.ContainerInvalidation` | plugin de Clang Static Analyzer (LLVM 21) que avisa del uso de un iterador, una referencia o un puntero a un elemento después de una mutación que lo invalida según C++17 | Desarrollador de C++ |
| **Norma** `norma/matriz.json` | las reglas de invalidación de C++17 como datos: 101 mutaciones, 348 reglas, cada una con su cláusula | Mantenedor |
| **Banco y arnés** `bench/` | 750 casos etiquetados desde la norma, su validación dinámica y el experimento que compara CSA con CSA + checker | Evaluador |
| **Motor de CSA** | plataforma reutilizada: explora los caminos y guarda el estado; no se reimplementa | — |

### c) Alcance del producto

El checker cubre `vector`, `deque`, `list`, `forward_list`, `set`,
`multiset`, `map`, `multimap`, `unordered_set` y `unordered_map`, con las
mutaciones de C++17 de la norma. Sigue iteradores, referencias y punteros a
elementos dentro de una unidad de traducción. No cubre `std::string`,
`std::array`, los adaptadores, las operaciones de C++20, el *aliasing* entre
contenedores distintos (`swap`, `splice`) ni el análisis entre unidades.

### d) Referencias

Los requisitos derivan de los objetivos (sección 1.4), de la especificación
de C++17 (N4659, cláusulas de contenedores), de la regla SEI CERT CTR51-CPP y
del protocolo del banco. La API de checkers de LLVM 21 condiciona la
implementación.

### e) Funcionalidades del producto

| Grupo | Requisitos | Casos de uso |
|---|---|---|
| Analizar código | RF-01 a RF-04 | CU-01, CU-02, CU-03 |
| Seguir handles | RF-05 a RF-07 | CU-01 |
| Aplicar la norma | RF-08 a RF-10 | CU-01, CU-03 |
| Diagnosticar | RF-11, RF-12 | CU-04 |
| Medir | RF-13 a RF-15 | CU-05, CU-06 |
| Mantener | RF-16, RF-17 | CU-07, CU-08 |

### f) Clases y características de usuarios

| Usuario | Qué hace con el sistema | Qué necesita saber |
|---|---|---|
| Desarrollador de C++ | analiza su código y corrige lo que el checker avisa | contenedores de la STL, línea de comandos de `clang` |
| Evaluador | genera el banco, corre el experimento y lee las métricas | el protocolo del banco, Python |
| Mantenedor | construye el plugin, corrige o amplía la norma | C++, CMake, la API de CSA |

### g) Entorno operativo

| Elemento | Especificación (fijada en la imagen `checker:llvm21`) |
|---|---|
| Sistema | GNU/Linux x86-64, Ubuntu 24.04 en Docker |
| Analizador | Clang/LLVM 21.1.8, Clang Static Analyzer |
| Biblioteca estándar | libstdc++ 13.3 |
| Lenguaje analizado | C++17 (N4659) |
| Construcción | CMake + Ninja, GoogleTest, `lit` |
| Arnés | Python 3.12, sin dependencias externas |

## Especificación de los requerimientos funcionales

### RF-01 Registrar el checker

| Campo | Especificación |
|---|---|
| Descripción | El checker se carga en `clang` como plugin y aparece en el catálogo de CSA con el nombre `ucsm.ContainerInvalidation` y sus opciones `PolicyMode` y `Debug` |
| Precondición | `libContainerInvalidation.so` construido contra el mismo LLVM 21 de la imagen |
| Flujo normal | `clang -cc1 -load libContainerInvalidation.so -analyzer-checker-help` |
| Postcondición | el checker figura en la lista con su descripción |
| Excepciones | versión de API distinta: `clang` rechaza el plugin con un error; nunca analiza en silencio sin él |
| Prioridad | Alta |
| Objetivo | OE2 |
| Cómo se demuestra | prueba `lit` `registro.cpp` |
| Evidencia | `registro.cpp` en verde |

### RF-02 Activar y desactivar el checker

| Campo | Especificación |
|---|---|
| Descripción | El checker se activa o se deja fuera con `-analyzer-checker`, sin recompilar `clang` |
| Precondición | RF-01 |
| Flujo normal | la misma orden de `clang` con y sin `ucsm.ContainerInvalidation` en `-analyzer-checker` |
| Postcondición | sólo la corrida con el checker da sus avisos; el resto de la configuración es idéntico |
| Excepciones | nombre de checker mal escrito: `clang` informa el error |
| Prioridad | Alta |
| Objetivo | OE2, OE3 |
| Cómo se demuestra | condiciones `Reference` y `Experimental` del experimento (RF-13) |
| Evidencia | `meta.condiciones` de `test/experimento/metricas.json`: difieren sólo en el checker |

### RF-03 Analizar un proyecto desde su base de compilación

| Campo | Especificación |
|---|---|
| Descripción | El checker analiza un proyecto entero a partir de su `compile_commands.json`, una unidad de traducción por invocación |
| Precondición | el proyecto genera `compile_commands.json` (CMake) |
| Flujo normal | `bench/codigo_real.py` lee la base, invoca `clang` con el checker por unidad y guarda los avisos |
| Postcondición | un registro por unidad: avisos, tiempo y código de salida |
| Excepciones | una unidad que no compila se registra como fallo, no como «sin avisos» |
| Prioridad | Alta |
| Objetivo | OE2 |
| Cómo se demuestra | `bench/codigo_real.py` sobre ninja, leveldb, yaml-cpp y RocksDB |
| Evidencia | 781 unidades, 0 caídas de `clang`, 0 avisos falsos confirmados (`test/codigo_real/avisos.json`) |

### RF-04 Elegir la política ante lo que depende del estado

| Campo | Especificación |
|---|---|
| Descripción | El usuario elige con `PolicyMode=Silent` (por omisión: sólo avisos confirmados) o `PolicyMode=Possibly` (también avisos posibles) |
| Precondición | RF-02 |
| Flujo normal | `-analyzer-config ucsm.ContainerInvalidation:PolicyMode=Possibly` |
| Postcondición | lo que depende del estado da aviso posible sólo con `Possibly`; los confirmados no cambian |
| Excepciones | valor no reconocido: se usa `Silent` |
| Prioridad | Alta |
| Objetivo | OE2 |
| Cómo se demuestra | `lit` `garantias.cpp`; condiciones `Experimental-Silent` y `Experimental-Possibly` |
| Evidencia | 102/102 casos `POLICY` con aviso posible en `Possibly`, 0/102 en `Silent` |

### RF-05 Seguir iteradores

| Campo | Especificación |
|---|---|
| Descripción | El checker sigue los iteradores obtenidos con `begin`, `find`, `lower_bound`, `upper_bound`, `insert` y `emplace` (también el `.first` del par), sus copias y sus movimientos (`++`, `--`, `+ k`, `std::next`, `std::advance`) |
| Precondición | RF-02 |
| Flujo normal | obtención → mutación → uso del iterador |
| Postcondición | aviso si la mutación lo invalida según la norma |
| Excepciones | iterador de origen desconocido: no se sigue (no se inventa un contenedor) |
| Prioridad | Alta |
| Objetivo | OE2 |
| Cómo se demuestra | `lit` `iteradores.cpp` (20 funciones) |
| Evidencia | `iteradores.cpp` en verde; banco: 128/128 UB de iterador |

### RF-06 Seguir referencias y punteros a elementos

| Campo | Especificación |
|---|---|
| Descripción | El checker sigue las referencias y los punteros obtenidos con `*it`, `it->`, `c[i]`, `at`, `front`, `back`, `data` y `&` |
| Precondición | RF-02 |
| Flujo normal | obtención → mutación → lectura, escritura, llamada a un método o paso por referencia del elemento |
| Postcondición | aviso si la mutación invalida la referencia según la norma |
| Excepciones | ninguna propia |
| Prioridad | Alta |
| Objetivo | OE2 |
| Cómo se demuestra | `lit` `referencias.cpp` (20 funciones); banco |
| Evidencia | 214/214 UB con referencia o puntero (CSA solo: 0 sobre el handle sostenido) |

### RF-07 No avisar en los usos válidos

| Campo | Especificación |
|---|---|
| Descripción | El checker no avisa en el iterador que devuelve la mutación (`it = c.erase(it)`), en uno obtenido de nuevo, en uno de otro contenedor ni al pasar un puntero por valor |
| Precondición | RF-05, RF-06 |
| Flujo normal | la mutación reemplaza la validez del handle reasignado |
| Postcondición | ningún aviso |
| Excepciones | — |
| Prioridad | Alta |
| Objetivo | OE2 |
| Cómo se demuestra | casos `SAFE` del banco; `lit` |
| Evidencia | 0 avisos en 306 casos `SAFE`, incluidos 12 de iterador devuelto |

### RF-08 Aplicar la regla de C++17

| Campo | Especificación |
|---|---|
| Descripción | Ante cada mutación, el checker aplica la regla que corresponde a la operación, al contenedor, a la categoría del handle y a la posición del elemento frente al punto de la mutación (antes, en, después, fin, dentro de un rango) |
| Precondición | la tabla normativa generada desde `matriz.json` (RF-17) |
| Flujo normal | reconocer la mutación → buscar la regla → actualizar la validez de cada handle del contenedor |
| Postcondición | cada handle queda válido, inválido o no resuelto |
| Excepciones | posición desconocida: el handle queda no resuelto, nunca válido por omisión |
| Prioridad | Alta |
| Objetivo | OE2 |
| Cómo se demuestra | gtest `Banco.ElVeredictoDelNucleoEsLaEtiqueta`; experimento |
| Evidencia | el núcleo coincide con la norma celda por celda; 342/342 UB detectados |

### RF-09 Tratar lo que depende del estado

| Campo | Especificación |
|---|---|
| Descripción | Cuando la invalidación depende de la capacidad o del factor de carga, el checker no la da por confirmada; un `reserve(c.size() + k)` previo cubre `k` inserciones |
| Precondición | RF-08 |
| Flujo normal | la regla dice «depende» → se gasta el crédito de `reserve` si lo hay; si no, el handle queda no resuelto |
| Postcondición | aviso posible (con `Possibly`) o ningún aviso (con la garantía) |
| Excepciones | `shrink_to_fit` nunca se garantiza |
| Prioridad | Alta |
| Objetivo | OE2 |
| Cómo se demuestra | `lit` `garantias.cpp`; casos con `reserve` del banco |
| Evidencia | 0 avisos en 54 casos con `reserve`; gtests de crédito |

### RF-10 Tratar las llamadas opacas

| Campo | Especificación |
|---|---|
| Descripción | Una llamada opaca que recibe el contenedor (o el objeto que lo contiene) hace olvidar los handles válidos; uno ya invalidado sigue invalidado |
| Precondición | RF-08 |
| Flujo normal | CSA notifica el escape → el checker borra los handles válidos de ese contenedor |
| Postcondición | sin aviso tras la llamada; aviso si el handle ya era inválido |
| Excepciones | — |
| Prioridad | Media |
| Objetivo | OE2 |
| Cómo se demuestra | `lit` `garantias.cpp` (`opaque`, `escaped_after_invalid`) |
| Evidencia | en verde; evitó falsos positivos en RocksDB |

### RF-11 Explicar la causa en el aviso

| Campo | Especificación |
|---|---|
| Descripción | El aviso dice la categoría del handle, el contenedor, la operación y su línea, y si es confirmado o posible; el posible dice qué garantía falta |
| Precondición | un uso inválido o no resuelto |
| Flujo normal | el checker arma el texto con los datos de la causa guardada en el estado |
| Postcondición | un aviso por handle y camino |
| Excepciones | — |
| Prioridad | Alta |
| Objetivo | OE2 |
| Cómo se demuestra | `expected-warning` en las pruebas `lit` |
| Evidencia | 30 avisos comprobados palabra por palabra en `lit` |

### RF-12 Mostrar la ruta del defecto

| Campo | Especificación |
|---|---|
| Descripción | El diagnóstico trae una nota donde se obtuvo el handle y otra en la mutación que lo invalidó, además de las notas de CSA hasta el uso |
| Precondición | RF-11 |
| Flujo normal | `-analyzer-output=text` o SARIF |
| Postcondición | la ruta *obtención → mutación → uso* visible en la salida |
| Excepciones | un handle copiado muestra la nota de la copia, no la de la obtención original |
| Prioridad | Media |
| Objetivo | OE2 |
| Cómo se demuestra | `lit` `rutas.cpp` con `-analyzer-output=text` y `expected-note` |
| Evidencia | 9 notas comprobadas en `rutas.cpp` |

### RF-13 Ejecutar el experimento

| Campo | Especificación |
|---|---|
| Descripción | El arnés corre cada caso del banco en cuatro condiciones: CSA; CSA + checker `Silent`; CSA + checker `Possibly`; checker sin los `alpha.cplusplus`. Una invocación por caso y condición |
| Precondición | plugin construido (RF-16) y banco generado (RF-15) |
| Flujo normal | `python3 bench/experimento.py` |
| Postcondición | `test/experimento/{ejecucion,cotejo,metricas}.json` con versiones y sha256 |
| Excepciones | compilación fallida, caída, tiempo agotado o salida ilegible: incidente registrado |
| Prioridad | Alta |
| Objetivo | OE1, OE3 |
| Cómo se demuestra | la ejecución misma |
| Evidencia | 3 000 ejecuciones, 0 incidentes |

### RF-14 Cotejar por sitio

| Campo | Especificación |
|---|---|
| Descripción | El arnés coteja cada aviso con el sitio: acierta sólo si cae sobre un handle que la norma da por inválido; separa confirmados, posibles e incidentes, y una caída nunca cuenta como acierto |
| Precondición | RF-13 |
| Flujo normal | normalizar SARIF → atribuir a función y sitio → cotejar → agregar |
| Postcondición | conteos TP/FP/FN/TN, posibles e incidentes por contenedor, operación, categoría y forma |
| Excepciones | denominador 0: métrica indefinida, no 0 % |
| Prioridad | Alta |
| Objetivo | OE3 |
| Cómo se demuestra | `python3 bench/pruebas_evaluacion.py` |
| Evidencia | 11 leyes de la evaluación en verde |

### RF-15 Generar y validar el banco

| Campo | Especificación |
|---|---|
| Descripción | El banco se genera desde la norma y sus etiquetas se validan ejecutando cada caso con libstdc++ Debug y con ASan/UBSan |
| Precondición | `norma/matriz.json` válida |
| Flujo normal | `bench/gen_corpus.py` → `bench/run_runtime_validation.py` |
| Postcondición | `test/corpus.cpp`, `test/corpus_truth.json` y los resultados de la validación |
| Excepciones | una ejecución contradice la etiqueta: el banco no se publica |
| Prioridad | Alta |
| Objetivo | OE1 |
| Cómo se demuestra | las dos órdenes |
| Evidencia | 750 casos; 852 ejecuciones, 0 contradicciones |

### RF-16 Construir y verificar el plugin

| Campo | Especificación |
|---|---|
| Descripción | El plugin se construye y se prueba en la imagen fijada con una sola orden |
| Precondición | Docker con la imagen `checker:llvm21` |
| Flujo normal | `docker compose run --rm plugin` (CMake, gtest, `lit`) |
| Postcondición | `libContainerInvalidation.so` y las pruebas en verde |
| Excepciones | una prueba falla: la orden termina con error |
| Prioridad | Alta |
| Objetivo | OE2 |
| Cómo se demuestra | la orden |
| Evidencia | 40 gtests y 5 archivos `lit` en verde; `calidad` en verde |

### RF-17 Mantener la norma como datos

| Campo | Especificación |
|---|---|
| Descripción | Corregir una regla en `matriz.json` regenera la tabla del plugin; `gen_tabla.py` rechaza una norma que rompe sus leyes |
| Precondición | RF-16 |
| Flujo normal | editar `matriz.json` → construir (RF-16) → regenerar el banco (RF-15) |
| Postcondición | checker y etiquetas dicen lo mismo |
| Excepciones | falta la cláusula o el efecto no es válido: no se genera la tabla |
| Prioridad | Media |
| Objetivo | OE1, OE2 |
| Cómo se demuestra | gtests `Norma.*` y comprobaciones de `gen_tabla.py` |
| Evidencia | `Norma.LaTablaEsTotal`, `Norma.InvalidarODependerCitaSuClausula` en verde |

## Matriz de trazabilidad de requerimientos

| Requisito | Objetivo | Caso de uso | Componente | Evidencia |
|---|---|---|---|---|
| RF-01, RF-02 | OE2 | CU-01, CU-07 | `plugin/registro` | `registro.cpp`; condiciones del experimento |
| RF-03 | OE2 | CU-02 | `bench/codigo_real.py` | 781 unidades, 0 avisos falsos confirmados |
| RF-04 | OE2 | CU-03 | `plugin/registro`, `plugin/dominio` | `garantias.cpp`; 102/102 `POLICY` |
| RF-05 a RF-07 | OE2 | CU-01 | `plugin/acl`, `plugin/checker` | `iteradores.cpp`, `referencias.cpp`; 0 FP |
| RF-08 a RF-10 | OE2 | CU-01, CU-03 | `plugin/dominio` | gtests; 342/342 UB |
| RF-11, RF-12 | OE2 | CU-04 | `plugin/checker/Messages.cpp` | `lit`; SARIF |
| RF-13, RF-14 | OE1, OE3 | CU-06 | `bench/experimento.py` | `metricas.json`; 11 leyes |
| RF-15 | OE1 | CU-05 | `bench/gen_corpus.py`, `bench/etiquetar.py` | 852 ejecuciones, 0 contradicciones |
| RF-16, RF-17 | OE2 | CU-07, CU-08 | `plugin/CMakeLists.txt`, `norma/` | gtests, `lit` |

## Reglas de negocio

| ID | Regla |
|---|---|
| RN-001 | La etiqueta de un caso sale de la norma: es el peor efecto que la norma da a cualquiera de sus handles (el sostenido y, en `bucle`, el iterador de control) |
| RN-002 | Las condiciones de referencia y experimental difieren sólo en el checker; la cuarta condición quita además los `alpha.cplusplus` y se informa aparte |
| RN-003 | Nada que dependa del estado se informa como confirmado, y nada no resuelto se da por válido sin una garantía |
| RN-004 | Un aviso posible nunca cuenta como acierto ni como falso positivo: se publica aparte |
| RN-005 | Una compilación fallida, una caída o un tiempo agotado es un incidente, nunca un verdadero negativo |
| RN-006 | Un aviso acierta sólo si cae sobre un handle que la norma da por inválido (cotejo por sitio) |
| RN-007 | Cada resultado lleva la versión de `clang`, de libstdc++ y el sha256 del plugin y del banco |

## Requerimientos de interfaces

| ID | Interfaz | Qué pasa por ella |
|---|---|---|
| INT-001 | API de checkers de CSA (LLVM 21) | `checkPostCall`, `checkPreCall`, `checkLocation`, `checkBind`, `checkPointerEscape`, `checkDeadSymbols`; `ProgramState` |
| INT-002 | Línea de comandos de `clang` | `-Xclang -load`, `-analyzer-checker`, `-analyzer-config ucsm.ContainerInvalidation:PolicyMode=…` |
| INT-003 | Base de compilación | `compile_commands.json` del proyecto analizado |
| INT-004 | Salida | avisos de CSA en texto, plist o SARIF; el arnés lee SARIF |
| INT-005 | Norma | `norma/matriz.json` → `NormTable.inc` generado en la construcción |
| INT-006 | Resultados | `test/experimento/ejecucion.json`, `cotejo.json`, `metricas.json` |

El checker no lee `compile_commands.json`: lo lee quien lo invoca
(`bench/codigo_real.py` o el sistema de construcción del usuario), que pasa a
`clang` las opciones de cada unidad.
