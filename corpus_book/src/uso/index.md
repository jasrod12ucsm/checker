# Guía de uso

Esta parte es para quien descarga el repositorio y quiere ver el checker
funcionando y comprobar sus requerimientos sin leer el resto del libro.

> El producto es **Centinela C++**, el servicio web que revisa los *pull
> requests* con este checker. Para verlo funcionando:
> `docker compose up sistema-demo` y abrir `http://localhost:8080`
> ([Sistema: Centinela C++](../sistema/index.md)). Esta guía es la del
> checker que el servicio usa por dentro.

## En dos minutos

Solo necesitas **Docker** con `docker compose`. Todo lo demás (LLVM 21.1.8,
CMake, Ninja, gtest, `lit`, `clang-format`, `mypy`) viene dentro de la imagen
`checker:llvm21`.

```bash
git clone https://github.com/jasrod12ucsm/checker.git
cd checker
docker compose build                 # una sola vez: descarga LLVM 21 (imagen de unos 2 GB)
docker compose run --rm verificar    # construye el checker y verifica los requerimientos
```

La última orden tarda unos **30 segundos** (10 de ellos en compilar el
plugin) y termina con `Todo en verde`. Lo que más tarda es `docker compose
build` la primera vez, porque descarga LLVM; depende de la conexión y se
hace una sola vez. Después de eso, todo lo de esta guía corre en segundos.

Cada paso de la verificación dice qué requerimientos demuestra:

```text
== RF-16, RF-17: construir el plugin; gen_tabla.py comprueba las leyes de la norma
== RF-08, RF-09, RF-10, RF-17, RNF-07: leyes del núcleo (gtest)
[  PASSED  ] 40 tests.
== RF-01, RF-04 a RF-12, RNF-06: el checker dentro de clang (lit)
  Passed: 5 (100.00%)
== RF-14, RN-001, RN-004, RN-005, RN-006: leyes de la evaluación
== RF-15, RN-001, RN-007: regenerar el banco desde la norma y comprobar su sello (test/banco-1.json)
test/corpus.cpp: igual al sello banco-1
== RF-03, RF-07: analizar un proyecto desde su base de compilación (ejemplos/)
{'prueba.cpp': ['confirmado', 'posible'], 'buen_uso.cpp': []}
== RF-02, RF-13, RN-002, RN-003, RN-007, RNF-01 a RNF-03: experimento, muestra del banco
81 casos × 4 condiciones en 24.8 s
  Reference              TP  10 FN  20 FP  0 ...
  Experimental-Possibly  TP  30 FN   0 FP  0 ... POLICY 9/9
== RNF-04, RNF-05: costo del checker (test/experimento/ejecucion.json)
RNF-04 tiempo mediano por caso: 0.650 s → 0.652 s (+0.3 %, umbral 10 %)
RNF-05 memoria residente máxima: 119.1 MB → 119.9 MB (+0.7 %, umbral 5 %)
Todo en verde en 31 s.
```

`docker compose run --rm verificar --completo` corre además el banco entero
(750 casos × 4 condiciones) y la validación dinámica (852 ejecuciones), en unos
4 minutos con 16 núcleos. Esa versión reescribe los resultados registrados
en `test/experimento/`, que son los que cita la tesis; `git diff` muestra si
algo cambió.

## Las páginas de esta parte

| Página | Para qué |
|---|---|
| [Levantar el checker](checker.md) | construir el plugin, correr sus pruebas y usarlo sobre un archivo o un proyecto |
| [Correr los bench](bench.md) | el experimento, la validación dinámica, el código real y los controles de calidad |
| [Usar el corpus](corpus.md) | qué es un caso, cómo leer su etiqueta, cómo analizar uno solo y cómo ampliar el banco |
| [Libro, informe y artículo](documentos.md) | regenerar este libro, los diagramas, el Word del proyecto y el artículo |
| [Dónde se valida cada requerimiento](requerimientos.md) | cada RF, RNF y regla de negocio con el código que lo implementa y la prueba que lo demuestra |

## Mapa del repositorio

| Carpeta | Qué hay |
|---|---|
| `verificar.sh` | la verificación de arriba; `docker compose run --rm verificar` la corre dentro de la imagen |
| `plugin/` | el checker: `dominio/` (núcleo puro, sin Clang), `acl/` (traduce las llamadas de CSA al lenguaje del núcleo), `checker/` (los *callbacks* de CSA), `registro/` (registro del plugin), `tests/` (gtest, `lit`, calidad) |
| `norma/` | `matriz.json`, las reglas de C++17 como datos, y `gen_tabla.py`, que comprueba sus leyes y genera la tabla en C++ |
| `bench/` | generador del banco, experimento, validación dinámica, código real, inyección de defectos y el generador de este libro |
| `test/` | el banco (`corpus.cpp`, `corpus_truth.json`, sello `banco-1.json`) y los resultados (`experimento/`, `codigo_real/`, `runtime_validation_results.json`) |
| `ejemplos/` | un proyecto CMake de dos archivos para probar el checker a mano |
| `libro/` | las páginas escritas a mano de este libro y los diagramas `.puml` |
| `corpus_book/` | el libro generado; no se edita a mano |
| `articulo/` | el artículo IEEE en LaTeX y el generador de sus Word |
| `docker-compose.yml` | las órdenes: `verificar`, `plugin`, `calidad`, `experimento`, `shell` |
| `.github/workflows/ci.yml` | el CI: `plugin`, `calidad` y `experimento` en GitHub Actions |

`src/`, el `CMakeLists.txt` de la raíz y `test/catch_by_value.cpp` son del
prototipo `mi-linter`, retirado en la decisión D-01; no forman parte del
checker.
