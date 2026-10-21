# Decisiones de diseño

> Cada decisión responde una pregunta: **¿qué error vuelve imposible?** Si la
> respuesta es «ninguno, pero queda ordenado», no es una decisión, es una
> preferencia (`bodega-arquitectura` §0). «Estado» es *propuesta* hasta que el
> piloto la confirme.

| ID | Decisión | Alternativa descartada | Qué error evita | Estado |
|---|---|---|---|---|
| D-01 | **Checker de CSA**, no AST matchers | Seguir con `mi-linter` (LibTooling) | Avisar sin saber qué pasó antes en el camino; no distinguir `if (x) c.clear();` de `c.clear();` | Firme |
| D-02 | **Plugin `.so`** cargado con `-Xclang -load` | Checker dentro del árbol de LLVM (recompilar Clang) | Horas de compilación por cambio; una tesis atada a un fork de LLVM | **Aplicada**: el `clang` 21 de apt.llvm.org carga el plugin (`registro.cpp`) |
| D-03 | **Modelo propio** de contenedores, iteradores y elementos | Leer el estado de `IteratorModeling` / `ContainerModeling` | No es posible: sus rasgos de estado no son API pública. Depender de ellos ataría el plugin a cabeceras internas | Firme |
| D-04 | **Núcleo puro** sin `#include` de Clang, en un *target* de CMake aparte | Toda la lógica dentro de los callbacks | Lógica de la norma imposible de probar sin compilar C++ con CSA; reglas repartidas entre callbacks | Firme |
| D-05 | **Fuente única** `norma/matriz.json` → tabla C++ generada + etiquetas generadas | Tabla a mano en C++ y etiquetas a mano en Python | Que el banco mida la diferencia entre dos copias de la norma | **Aplicada**: `gen_tabla.py` → `NormTable.inc`; `etiquetar.py` |
| D-06 | Handle = **región del elemento** (`const MemRegion*`), no la variable | Indexar por `VarDecl` | Revivir handles al reasignar; no ver que `r` y `&r` son el mismo elemento (leyes, contradicciones 2 y 3) | Firme |
| D-07 | `Validity` con **tres valores** y `JOIN` | `bool válido` | Presentar «no sé» como «seguro» (RN-003); perder la causa de la invalidación | Firme |
| D-08 | **Dos clases de aviso**: confirmado y posible; el posible se controla con `PolicyMode` | Un solo aviso | Mezclar en la precisión los casos que dependen del estado (`POLICY`) | **Aplicada** (`PolicyMode=Silent`/`Possibly`); falta el visto bueno del asesor |
| D-09 | La capacidad y el factor de carga **se preguntan al solver** en la mutación; no se guardan como entero | `capacidad: Integer [0..1]` | Un número inventado donde CSA sólo tiene un símbolo | **Reemplazada por D-16 y D-19** |
| D-10 | Las notas de ruta con **`NoteTag`** al invalidar | `BugReporterVisitor` que reconstruye la historia | Notas que no coinciden con la transición que de verdad invalidó | **Aplicada**: notas en la obtención y en la mutación (`rutas.cpp`) |
| D-11 | El arnés es **otro contexto**: sólo invoca `clang` y lee plist/SARIF | El arnés importa o enlaza el plugin | Que la medición dependa de la implementación medida | Firme |
| D-12 | **Conteos** como monoide; métricas al final; `Undefined` ≠ 0 | Promediar precisiones por grupo | Promedio de promedios; un 0/0 presentado como 0 % | Firme |
| D-13 | Un **fallo** de ejecución es una incidencia, nunca un VN | Contar «sin avisos» | Que un *crash* del checker mejore la precisión | Firme |
| D-14 | Identificadores en **inglés** (convención LLVM), documentación en **español** | Todo en español | Mezclar nombres con la API de CSA, que está en inglés | Firme |
| D-15 | **Una invocación de `clang` por caso** (`-analyze-function=<caso>`) | Un solo `clang` sobre los 750 casos | Que una caída del checker borre los resultados de todos los casos; no poder medir tiempo y memoria por caso (RNF-04/05) | **Aplicada** (D-24): 3 000 invocaciones, tiempo y memoria por caso |
| D-16 | En la v1, **sin modelo propio de tamaño ni capacidad**: `Ask` responde `Both` salvo que el camino ya lo fije | Conjurar símbolos de tamaño y capacidad por contenedor | Inventar un estado que el código analizado no da. Consecuencia: todo `POLICY` del banco da, a lo sumo, aviso **posible** | **Reemplazada por D-19** |
| D-17 | `ExperimentPair = base + plugin` como **un solo tipo** | Dos configuraciones sueltas que se comparan | Que las condiciones difieran en algo más que el plugin (RN-002): no se puede escribir | Firme |
| D-18 | Corregir 27 etiquetas del banco **antes** de congelar `banco-1` (contradicciones 4 y 5) | Medir con el banco actual | Contar como falso negativo un aviso «posible» que es la respuesta correcta | **Aplicada** (`bench/etiquetar.py`); falta el visto bueno del asesor |
| D-19 | **Crédito de garantía** por contenedor: `reserve(c.size() + k)` da `k` inserciones sin reubicar ni *rehash*; cada inserción gasta 1; lo no contado lo borra | D-16 tal cual (sin modelo) | Avisar «posible» en código correcto que hizo `reserve`: un FP que el banco actual no mediría ([lógica §3](logica.md#3-cuando-el-fallo-depende-del-estado-la-garantía)) | **Aplicada**: 0 avisos en 54 casos con `reserve` |
| D-20 | El banco gana el eje **`Guarantee`** (`NoGuarantee`, `Reserved`, `ReturnedHandle`): casos `SAFE` de buen uso de lo que puede fallar | En el banco de 684, sólo los 246 `SAFE` de mutaciones que nunca invalidan | Precisión perfecta para un checker que avise en todo `push_back` | **Aplicada**: 54 `Reserved` + 12 `ReturnedHandle`; falta el visto bueno del asesor |
| D-21 | Un **escape** (llamada opaca que recibe el contenedor o el objeto que lo contiene) **olvida** los handles `Valid` y `Unresolved`; los `Invalidated` se conservan | Pasarlos a `Unresolved(EscapedToOpaqueCode)` | 8 avisos posibles en ninja por `printf("%p", edge)` y similares: ruido que nadie corrige. Lo que ya se invalidó no lo arregla ninguna llamada | Firme |
| D-22 | En código real se analiza con `-analyzer-inlining-mode=all` | El modo por defecto `noredundancy` | `noredundancy` no vuelve a analizar como raíz una función que ya se inlinó; si el presupuesto cortó ese camino, el defecto no se ve (semillas S7 y S8). Cuesta ~40 % más de tiempo y no añadió ningún aviso nuevo sin semilla | Firme |
| D-23 | `erase(first, last)` es la **misma** mutación que `erase(first)`, con la relación tomada frente al rango semiabierto | Filas nuevas de rango en la norma | Un FP confirmado en RocksDB (`range_tombstone_fragmenter.cc`): `last` sobrevive. La norma ya tenía la respuesta correcta; faltaba la geometría | Firme |
| D-24 | El experimento corre **una invocación de `clang` por caso y condición** y coteja **por sitio**: el aviso acierta si cae sobre un handle que la norma da por inválido | Un análisis del archivo entero con atribución por función | Que un caso tape a otro (presupuesto compartido), y contar como acierto un aviso sobre un handle válido | Firme |
| D-25 | Cuarta condición `Plugin-Possibly`: `core` + `cplusplus` + plugin, **sin** `alpha.cplusplus` | Medir el plugin sólo dentro de base + plugin | `InvalidatedIterator` corta el camino en el mismo uso: en base + plugin, 54 casos tenían sólo el aviso de CSA y el aporte del plugin no se veía | Firme |

## Riesgos que las decisiones no eliminan

| Riesgo | Señal temprana | Mitigación |
|---|---|---|
| El `clang` empaquetado no carga plugins de *analyzer* | `-load` falla o el checker no aparece en `-analyzer-checker-help` | Incremento I0 lo prueba primero. Plan B: compilar sólo `clang` con `CLANG_PLUGIN_SUPPORT=ON` en la imagen |
| CSA conjura regiones distintas para `*it` en cada evaluación | Pérdida de seguimiento en forma `bucle` | Es aceptable (cada obtención es otro handle, D-06). Se mide por forma |
| La API de CSA cambia entre versiones | No compila al subir LLVM | Versión **fijada** (LLVM 21) en el Dockerfile; registro de versión en cada ejecución |
| El presupuesto de CSA (`max-nodes`, inlining) corta caminos | FN en forma `llamada` o `bucle` | Mismas opciones en las dos condiciones (RN-002); se reportan los cortes. **Ocurrió**: S7 y S8 → D-22 |
| El resultado de CSA depende de la versión de libstdc++ | **Ocurrió**: la condición de referencia detecta 109 UB con libstdc++ 16 y 48 con libstdc++ 13, sobre el mismo banco | La imagen fija la biblioteca (Ubuntu 24.04, libstdc++ 13); la versión entra en el registro de cada ejecución |
| Caminos imposibles por no modelar el **contenido** del contenedor | Aviso posible tras un `find` que en la realidad siempre acierta (ninja, `PathExistsBetween`) | Sólo produce avisos **posibles**, nunca confirmados; se cuentan aparte en código real |
| Un checker de CSA corta el camino antes que el nuestro | **Ocurrió**: `InvalidatedIterator` genera un nodo de error fatal en el mismo `*it` | D-25: se mide también sin los checkers `alpha.cplusplus` |
| El plugin aborta `clang` en código que el banco no tiene | **Ocurrió** en RocksDB (constante de 64 bits en `c[i]`) | Cada unidad que no termina es un `Incident`, nunca un TN; prueba `huge_index` en `lit` |
