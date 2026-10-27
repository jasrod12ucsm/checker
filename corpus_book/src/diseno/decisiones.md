# Decisiones de diseño

> Cada decisión responde una pregunta: **¿qué error vuelve imposible?** Si la
> respuesta es «ninguno, pero queda ordenado», no es una decisión, es una
> preferencia. La columna «Estado» dice si la decisión está **aplicada** (con
> su evidencia), es **firme** (vale para todo el diseño) o fue **reemplazada**.
> Las decisiones son del equipo; las del banco se tomaron antes de sellar
> `banco-1` (20-10-2026).

## Servicio Centinela C++

Tabla: Decisiones de diseño del servicio

| ID | Decisión | Alternativa descartada | Qué error evita | Estado |
|---|---|---|---|---|
| DS-01 | **Servicio web** que revisa los *pull requests* llamando al checker | Una acción de GitHub o un paso de CI que cada equipo configura | Que cada equipo tenga que instalar LLVM 21 y el plugin en su CI; perder entre revisiones los falsos positivos ya marcados y la política del repositorio | **Aplicada** (`sistema/`) |
| DS-02 | El *webhook* **solo encola**: la revisión y su trabajo se guardan en la misma transacción y un trabajador aparte analiza | Analizar dentro de la petición del *webhook* | Que GitHub corte la petición mientras `clang` analiza; perder una revisión si el servicio cae entre aceptar el evento y guardarlo (RNF-S03, RNF-S04) | **Aplicada** |
| DS-03 | **Sin usuarios predefinidos**: la primera cuenta registrada administra; las demás esperan aprobación | Un administrador creado por variables de entorno o con una clave de fábrica | Una clave conocida de antemano en cada instalación (RN-S01) | **Aplicada** |
| DS-04 | Los permisos son un **testigo** `Autorizado<P>` que cada operación del dominio exige | Un *middleware* que revisa permisos por ruta | Agregar una ruta u operación y olvidar comprobar el permiso: sin testigo, no compila | **Aplicada** |
| DS-05 | `Revision<E>` lleva su **estado en el tipo**; errores de negocio como valores (`Resultado<T, E>`) | Un campo `estado: string` y excepciones | Publicar una revisión que no está en análisis; un error de negocio que se escapa como un 500 | **Aplicada** |
| DS-06 | Un commit se revisa **una sola vez**; repetir es reintentar la misma revisión | Una revisión nueva por cada evento | Comentarios duplicados en el PR cuando GitHub reenvía el evento (RN-S02) | **Aplicada**: `UNIQUE (repositorio_id, numero_pr, sha_cabeza)` |
| DS-07 | El falso positivo se recuerda por **huella** del archivo y el mensaje sin el número de línea | Recordar archivo y línea | Que un falso positivo vuelva a aparecer porque el código se movió unas líneas (RN-S03) | **Aplicada** |
| DS-08 | **SQLite** detrás de un puerto `Almacen` | PostgreSQL desde el inicio | Operar un servidor de base de datos para un servicio de un solo equipo; el adaptador permite cambiarlo sin tocar el dominio | **Aplicada** |
| DS-09 | **TypeScript** estricto con Fastify y zod | Python o C++ para el servicio | Estados y permisos sin comprobar al compilar; datos sin validar en las fronteras | **Aplicada** |

## Motor de análisis

Tabla: Decisiones de diseño del motor

| ID | Decisión | Alternativa descartada | Qué error evita | Estado |
|---|---|---|---|---|
| D-01 | **Checker de CSA**, no AST matchers | Un prototipo con *AST matchers* de LibTooling | Avisar sin saber qué pasó antes en el camino; no distinguir `if (x) c.clear();` de `c.clear();` | Firme |
| D-02 | **Plugin `.so`** cargado con `-Xclang -load` | Checker dentro del árbol de LLVM (recompilar Clang) | Horas de compilación por cambio; una tesis atada a un fork de LLVM | **Aplicada**: el `clang` 21 de apt.llvm.org carga el plugin (`registro.cpp`) |
| D-03 | **Modelo propio** de contenedores, iteradores y elementos | Leer el estado de `IteratorModeling` / `ContainerModeling` | No es posible: sus rasgos de estado no son API pública. Depender de ellos ataría el plugin a cabeceras internas | Firme |
| D-04 | **Núcleo puro** sin `#include` de Clang, en un *target* de CMake aparte | Toda la lógica dentro de los callbacks | Lógica de la norma imposible de probar sin compilar C++ con CSA; reglas repartidas entre callbacks | Firme |
| D-05 | **Fuente única** `norma/matriz.json` → tabla C++ generada + etiquetas generadas | Tabla a mano en C++ y etiquetas a mano en Python | Que el banco mida la diferencia entre dos copias de la norma | **Aplicada**: `gen_tabla.py` → `NormTable.inc`; `etiquetar.py` |
| D-06 | Handle = **región del elemento** (`const MemRegion*`), no la variable | Indexar por `VarDecl` | Revivir handles al reasignar; no ver que `r` y `&r` son el mismo elemento (leyes, contradicciones 2 y 3) | Firme |
| D-07 | `Validity` con **tres valores** y `JOIN` | `bool válido` | Presentar «no sé» como «seguro» (RN-003); perder la causa de la invalidación | Firme |
| D-08 | **Dos clases de aviso**: confirmado y posible; el posible se controla con `PolicyMode` | Un solo aviso | Mezclar en la precisión los casos que dependen del estado (`POLICY`) | **Aplicada** (`PolicyMode=Silent`/`Possibly`) |
| D-09 | La capacidad y el factor de carga **se preguntan al solver** en la mutación; no se guardan como entero | `capacidad: Integer [0..1]` | Un número inventado donde CSA sólo tiene un símbolo | **Reemplazada por D-16 y D-19** |
| D-10 | Las notas de ruta con **`NoteTag`** al invalidar | `BugReporterVisitor` que reconstruye la historia | Notas que no coinciden con la transición que de verdad invalidó | **Aplicada**: notas en la obtención y en la mutación (`rutas.cpp`) |
| D-11 | El arnés es **otro contexto**: sólo invoca `clang` y lee plist/SARIF | El arnés importa o enlaza el plugin | Que la medición dependa de la implementación medida | Firme |
| D-12 | **Conteos** como monoide; métricas al final; `Undefined` ≠ 0 | Promediar precisiones por grupo | Promedio de promedios; un 0/0 presentado como 0 % | Firme |
| D-13 | Un **fallo** de ejecución es una incidencia, nunca un VN | Contar «sin avisos» | Que un *crash* del checker mejore la precisión | Firme |
| D-14 | Identificadores en **inglés** (convención LLVM), documentación en **español** | Todo en español | Mezclar nombres con la API de CSA, que está en inglés | Firme |
| D-15 | **Una invocación de `clang` por caso** (`-analyze-function=<caso>`) | Un solo `clang` sobre los 750 casos | Que una caída del checker borre los resultados de todos los casos; no poder medir tiempo y memoria por caso (RNF-04/05) | **Aplicada** (D-24): 3 000 invocaciones, tiempo y memoria por caso |
| D-16 | En la v1, **sin modelo propio de tamaño ni capacidad**: `Ask` responde `Both` salvo que el camino ya lo fije | Conjurar símbolos de tamaño y capacidad por contenedor | Inventar un estado que el código analizado no da. Consecuencia: todo `POLICY` del banco da, a lo sumo, aviso **posible** | **Reemplazada por D-19** |
| D-17 | `ExperimentPair = base + plugin` como **un solo tipo** | Dos configuraciones sueltas que se comparan | Que las condiciones difieran en algo más que el plugin (RN-002): no se puede escribir | Firme |
| D-18 | Corregir 27 etiquetas del banco **antes** de congelar `banco-1`: 21 por la contradicción 4 y 6 por la 6 (la 5 cambió una sentencia, no una etiqueta) | Medir con el banco actual | Contar como falso negativo un aviso «posible» que es la respuesta correcta | **Aplicada** (`bench/etiquetar.py`), 20-10-2026 |
| D-19 | **Crédito de garantía** por contenedor: `reserve(c.size() + k)` da `k` inserciones sin reubicar ni *rehash*; cada inserción gasta 1; lo no contado lo borra | D-16 tal cual (sin modelo) | Avisar «posible» en código correcto que hizo `reserve`: un FP que el banco actual no mediría | **Aplicada**: 0 avisos en 54 casos con `reserve` |
| D-20 | El banco gana el eje **`Guarantee`** (`NoGuarantee`, `Reserved`, `ReturnedHandle`): casos `SAFE` de buen uso de lo que puede fallar | En el banco de 684, sólo los 246 `SAFE` de mutaciones que nunca invalidan | Precisión perfecta para un checker que avise en todo `push_back` | **Aplicada**: 54 `Reserved` + 12 `ReturnedHandle`, 20-10-2026 |
| D-21 | Un **escape** (llamada opaca que recibe el contenedor o el objeto que lo contiene) **olvida** los handles `Valid` y `Unresolved`; los `Invalidated` se conservan | Pasarlos a `Unresolved(EscapedToOpaqueCode)` | 8 avisos posibles en ninja por `printf("%p", edge)` y similares: ruido que nadie corrige. Lo que ya se invalidó no lo arregla ninguna llamada | Firme |
| D-22 | En código real, y en el servicio Centinela, se analiza con `-analyzer-inlining-mode=all` | El modo por defecto `noredundancy` | `noredundancy` no vuelve a analizar como raíz una función que ya se inlinó; si el presupuesto cortó ese camino, el defecto no se ve (semillas S7 y S8). Cuesta ~40 % más de tiempo y no añadió ningún aviso nuevo sin semilla | **Aplicada** en `bench/codigo_real.py` y en el analizador del servicio (`clang.ts`) |
| D-23 | `erase(first, last)` es la **misma** mutación que `erase(first)`, con la relación tomada frente al rango semiabierto | Filas nuevas de rango en la norma | Un FP confirmado en RocksDB (`range_tombstone_fragmenter.cc`): `last` sobrevive. La norma ya tenía la respuesta correcta; faltaba la geometría | Firme |
| D-24 | El experimento corre **una invocación de `clang` por caso y condición** y coteja **por sitio**: el aviso acierta si cae sobre un handle que la norma da por inválido | Un análisis del archivo entero con atribución por función | Que un caso tape a otro (presupuesto compartido), y contar como acierto un aviso sobre un handle válido | Firme |
| D-25 | Cuarta condición `Plugin-Possibly`: `core` + `cplusplus` + plugin, **sin** `alpha.cplusplus` | Medir el plugin sólo dentro de base + plugin | `InvalidatedIterator` corta el camino en el mismo uso: en base + plugin, 54 casos tenían sólo el aviso de CSA y el aporte del plugin no se veía | Firme |

## Riesgos que las decisiones no eliminan

| Riesgo | Señal temprana | Mitigación |
|---|---|---|
| Se filtra el token de GitHub del servicio | actividad en GitHub que el equipo no hizo | el token vive solo en `.env` (no versionado) y en el entorno del contenedor; se usa un token con permisos mínimos sobre los repositorios conectados y se revoca en GitHub |
| GitHub limita las peticiones de la API | respuestas 403 o 429 de GitHub | cada revisión hace unas pocas peticiones; si falla, la revisión queda `Fallida` con el mensaje de GitHub y se reintenta |
| La URL pública del servicio no está disponible | GitHub marca la entrega del *webhook* como fallida | «Revisar un PR ahora» pide la revisión a mano; GitHub permite reenviar la entrega |
| Un archivo del cliente no compila sin su base de compilación | revisiones con «no analizados» | se informa como no analizado, nunca como limpio (RN-S05) |
| El `clang` empaquetado no carga plugins de *analyzer* | `-load` falla o el checker no aparece en `-analyzer-checker-help` | **No ocurrió**: I0 comprobó que el `clang` 21 de apt.llvm.org carga el plugin (D-02). El plan B era compilar sólo `clang` con `CLANG_PLUGIN_SUPPORT=ON` |
| CSA conjura regiones distintas para `*it` en cada evaluación | Pérdida de seguimiento en forma `bucle` | Es aceptable (cada obtención es otro handle, D-06). Se mide por forma |
| La API de CSA cambia entre versiones | No compila al subir LLVM | Versión **fijada** (LLVM 21) en el Dockerfile; registro de versión en cada ejecución |
| El presupuesto de CSA (`max-nodes`, inlining) corta caminos | FN en forma `llamada` o `bucle` | Mismas opciones en todas las condiciones (RN-002); se reportan los cortes. **Ocurrió**: S7 y S8 → D-22 |
| El resultado de CSA depende de la versión de libstdc++ | **Ocurrió**: la condición de referencia detecta 109 UB con libstdc++ 16 y 48 con libstdc++ 13, sobre el mismo banco | La imagen fija la biblioteca (Ubuntu 24.04, libstdc++ 13); la versión entra en el registro de cada ejecución |
| Caminos imposibles por no modelar el **contenido** del contenedor | Aviso posible tras un `find` que en la realidad siempre acierta (ninja, `PathExistsBetween`) | Sólo produce avisos **posibles**, nunca confirmados; se cuentan aparte en código real |
| Un checker de CSA corta el camino antes que el nuestro | **Ocurrió**: `InvalidatedIterator` genera un nodo de error fatal en el mismo `*it` | D-25: se mide también sin los checkers `alpha.cplusplus` |
| El plugin aborta `clang` en código que el banco no tiene | **Ocurrió** en RocksDB (constante de 64 bits en `c[i]`) | Cada unidad que no termina es un `Incident`, nunca un TN; prueba `huge_index` en `lit` |
