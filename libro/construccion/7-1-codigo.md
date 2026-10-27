# 7.1 Construcción del código

## a) Preparación previa

### Entorno

El servicio y el motor comparten una sola imagen de Docker: la del servicio
(`sistema/Dockerfile`) parte de la del motor (`checker:llvm21`), así que
`clang` y el plugin que usa Centinela son los mismos que se midieron.

| Herramienta | Versión | Para qué |
|---|---|---|
| Node.js | 22 (imagen) | ejecutar el servicio Centinela C++ |
| TypeScript | 5.9, `strict`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes` | el código del servicio |
| Fastify | 5 | servidor HTTP del servicio |
| better-sqlite3 | 12 | base de datos SQLite del servicio |
| zod | 4 | validación de toda entrada HTTP y de toda fila de la base |
| Vitest + `@vitest/coverage-v8` | 3.2 | pruebas y cobertura del servicio |
| Docker y `docker compose` | — | levantar el servicio, sus pruebas y el motor con una orden |
| Imagen `checker:llvm21` | Ubuntu 24.04 + LLVM/Clang 21 | compilar y ejecutar el plugin con la misma API que el experimento |
| CMake + Ninja | ≥ 3.20 | construir los tres *targets* del motor (dominio, plugin, pruebas) |
| `clangd` | 21 | navegación y diagnósticos en el editor, desde `compile_commands.json` |
| GoogleTest | de la distribución | pruebas del núcleo del motor |
| `lit` + `FileCheck` | los de LLVM 21 | pruebas del checker con `-verify` (la convención de CSA) |
| Python | 3.12 | arnés, sin dependencias externas; leyes en `bench/pruebas_evaluacion.py` |
| mdbook + PlantUML (jar) | 0.5 / 1.2024 | libro y figuras |

### Estándares de codificación

Servicio (TypeScript):

| Regla de codificación | Cómo se cumple |
|---|---|
| Los errores de negocio son valores (`Resultado<T, E>`), no excepciones | prueba de arquitectura: el dominio no usa `throw` |
| El dominio no lee el reloj ni genera azar | puertos `Reloj` y `GeneradorIds`; prueba de arquitectura |
| Nombres del lenguaje ubicuo, en español | `solicitar`, `iniciar`, `publicar`, `reintentar`, `clasificar` |
| Sin `any` | prueba de arquitectura |
| Un estado nunca es un `boolean` suelto ni un texto libre | uniones etiquetadas (`Pendiente │ EnAnalisis │ Publicada │ Fallida`) y `switch` exhaustivo con `inalcanzable(never)` |
| Cada capa importa solo lo que su capa permite | `pruebas/arquitectura.test.ts` |

Motor (C++ y Python):

| Tema | Estándar | Cómo se verifica | Estado |
|---|---|---|---|
| Estilo C++ | *LLVM Coding Standards* | `.clang-format` (`BasedOnStyle: LLVM`, 110 columnas); `clang-format --dry-run -Werror` en `calidad` | aplicado: 0 diferencias |
| Nombres | identificadores en inglés, `CamelCase` para tipos, como CSA; comentarios y documentación en español | revisión | aplicado |
| Estados | nunca `bool` ni texto para un estado: `enum class` o `std::variant` | revisión | aplicado (`Validity`, `Effect`, `Outcome`) |
| `switch` sobre enums del dominio | **sin `default:`**; `-Werror=switch` | el compilador | aplicado |
| Errores | sin excepciones ni RTTI (como LLVM); `std::optional` | `-fno-exceptions -fno-rtti` en `ucsm_dominio` y el plugin | aplicado |
| Inmutabilidad | los valores del dominio sólo tienen métodos `const` | revisión | aplicado |
| Python | anotaciones de tipo, `dataclass(frozen=True)`, `subprocess` con lista de argumentos | `mypy` en `calidad` | aplicado: 0 errores en 10 archivos |

### Planificación modular

Las responsabilidades están en el capítulo 5: el servicio en paquetes por
capa (`kernel` → contextos → `producto` → adaptadores → `app`) y el motor en
tres capas (núcleo, anticorrupción, cáscara). Las dos reglas que más protegen
son que **el dominio del servicio no importa Fastify, SQLite ni Node**, y que
**una regla de invalidación sólo se escribe en `norma/matriz.json`**.

## b) Escritura del código: en incrementos

El motor se construyó en los incrementos I0 a I6 y el servicio en I7
(sección 7.6). Cada incremento del motor **terminó con el banco corrido** y
sus resultados versionados; cada parte del servicio entró con las pruebas de
su requisito (RF-S01 a RF-S05).

Buenas prácticas aplicadas:

- **Cargar, decidir, efectos.** Cada caso de uso del servicio carga lo que
  necesita del almacén, decide con una función pura del dominio y después
  guarda o llama a GitHub. Los callbacks del motor hacen lo mismo en cuatro
  líneas: cargar, traducir, decidir, aplicar.
- **DRY de verdad:** la norma existe una sola vez (D-05); la tabla C++ y las
  etiquetas se generan. En el servicio, el mapa de errores a códigos HTTP
  está en un solo archivo (`errores.ts`).
- **Reutilizar en vez de reimplementar:** el servicio no reimplementa el
  análisis, llama al mismo `clang` con el plugin; el plugin reutiliza CSA
  (`CallDescriptionMap`, `NoteTag`, `REGISTER_MAP_WITH_PROGRAMSTATE`,
  `SymbolReaper`).

## c) Pruebas durante la codificación

Servicio (Vitest, 140 pruebas en la imagen Docker; fuera de ella, 139 y 1 omitida, la de `clang` real):

| Nivel (servicio) | Qué prueba | Archivos |
|---|---|---|
| Dominio | las reglas, con valores en memoria | `contextos/*/src/*.test.ts` |
| Garantías de tipos | lo que **no** debe compilar (`@ts-expect-error`) | `*/garantias.test.ts`, con `npm run tipos` |
| Casos de uso | cada requisito con dobles de los puertos | `producto/src/casos.test.ts` |
| Adaptadores | SQLite real, scrypt y HMAC reales, GitHub simulado en un puerto local, `clang` real dentro de Docker | `adaptadores/*/src/*.test.ts` |
| API | HTTP completo con `inject` | `pruebas/api.test.ts` |
| Arquitectura | importaciones permitidas por capa y reglas de código | `pruebas/arquitectura.test.ts` |
| Sistema | servicio compuesto: servidor, trabajador y base | `app/src/componer.test.ts`, `demo/demostrar.ts` |

Motor:

| Nivel (motor) | Qué prueba | Herramienta | Cuándo |
|---|---|---|---|
| Leyes de la norma | cuatro leyes sobre `matriz.json` al generar la tabla, y cuatro gtests `Norma.*` | `norma/gen_tabla.py` y GoogleTest | cada cambio en la matriz |
| Leyes del núcleo | 24 gtests `Deteccion.*` y 9 `Posicion.*`, una por ley | GoogleTest | TDD: la prueba de la ley antes que la decisión |
| Checker | cinco `.cpp` con `// expected-warning{{…}}` y `expected-note` (30 avisos y 9 notas) | `clang --analyze -load … -verify` vía `lit` | cada cambio en `acl/` o `checker/` |
| Integración | el banco completo en las cuatro condiciones | `bench/experimento.py` | cada incremento |
| Leyes del arnés | las once leyes de la evaluación | `bench/pruebas_evaluacion.py` | cada cambio en `bench/experimento.py` |

**Depuración.** En el servicio, la bitácora JSON del servidor y del
trabajador y la demostración con un GitHub simulado
(`demo/demostrar.ts`). En el motor, las herramientas de CSA:

- `-analyzer-checker=debug.ExprInspection` con `clang_analyzer_dump(x)`;
- `-analyzer-dump-egraph` para ver el `ExplodedGraph`;
- `-analyzer-config ucsm.ContainerInvalidation:Debug=true` para
  volcar los mapas del estado en cada nodo.

## d) Revisión del código

Hasta el 21-10-2026 el equipo trabajó directamente sobre `main`, y la
revisión fue la ejecución de las pruebas y del banco antes de cada *commit*,
no un *pull request*. Desde el incremento I7 la política es otra: cada
cambio entra por una rama y un *pull request* revisado por la otra
integrante (sección 7.3), con esta lista:

1. ¿Las pruebas del servicio y del motor pasan en la imagen Docker?
2. ¿Algún estado del dominio escrito como `boolean`, texto o `default:`?
3. ¿El dominio del servicio importa Fastify, SQLite o Node? ¿El núcleo del
   motor incluye algo de Clang? (Si compila o si pasa la prueba de
   arquitectura, no.)
4. ¿Cada regla nueva tiene la prueba de su ley o de su requisito?
5. ¿Alguna regla de invalidación fuera de `matriz.json`? Si el cambio toca
   el motor, ¿el PR adjunta la tabla del banco antes y después?

## e) Integración continua

`.github/workflows/ci.yml` corre en GitHub Actions con la misma imagen
(sección 7.3) los servicios de `docker compose`:

| Paso | Servicio | Qué falla |
|---|---|---|
| construir y probar el motor | `plugin` | el plugin no compila; un gtest o un `lit` falla |
| calidad del motor | `calidad` (`plugin/tests/calidad.sh`) | formato distinto del de `.clang-format`; un error de `mypy`; una ley del arnés; cobertura de líneas del núcleo < 90 % |
| banco | `experimento` (`bench/experimento.py` + `bench/regresion.py`) | un caso `SAFE` gana un aviso confirmado, un `UB` que se detectaba deja de detectarse, o hay un incidente |
| pruebas del servicio | `sistema-pruebas` (`npm test` en la imagen de Centinela) | una prueba de Vitest falla o la cobertura baja de los umbrales (90 % de líneas y funciones, 80 % de ramas) |
| demostración del servicio | `sistema` con `demo/demostrar.ts --salir` | la revisión del PR de ejemplo no publica los dos hallazgos esperados de `src/cache.cpp` |

Los tres pasos del motor pasaron en GitHub Actions el 21-10-2026 (ejecución
39588114053). Los dos pasos del servicio se agregaron con I7.

## f) Documentación del código

| Qué | Dónde | Cómo se mantiene al día |
|---|---|---|
| Comentarios de documentación en español sobre cada tipo, función pública y puerto | el código del servicio (`/** … */`) y del motor (`///`) | revisión |
| Significado y leyes de cada pieza | `libro/diseno/` (sección 5.9) | las leyes se prueban; si cambian, cambia la prueba |
| Fragmentos de código en la documentación | el libro del proyecto | se extraen del código al generarlo (`{{codigo RUTA SÍMBOLO}}`): si el símbolo cambia de nombre, el libro no se genera |
| Guía de uso, API y despliegue | `README.md` y el libro (*Sistema*) | se regeneran con `bench/gen_book.py` |
| Diagramas | `libro/diagramas/*.puml` | se renderizan con `bench/render_diagramas.py` |

## g) Optimización y refactorización

**Optimización, sólo medida.** En el motor, tiempo y memoria máxima por caso
frente a la condición de referencia (RNF-04, RNF-05): +0,3 % de tiempo
mediano y +0,7 % de memoria. En el servicio, el tiempo de una revisión: en
la demostración, una revisión de dos archivos tarda 0,28 s desde que se
encola hasta que se publica (tres corridas: 0,281, 0,282 y 0,284 s). Con
esos números no hizo falta un perfilador.

**Refactorización**, siempre con las pruebas en verde antes y después:

| Refactorización | Por qué | Qué la protegió |
|---|---|---|
| El arnés pasó de `run_corpus.py` a la tubería ejecutar → normalizar → cotejar → agregar (`bench/experimento.py`) | la atribución por línea en un solo archivo dejaba que un caso tapara a otro (D-24) | las once leyes del arnés |
| El escape del motor pasó de `Unresolved` a olvidar lo válido (D-21) | ruido en código real | los `lit` y el banco |
| El registro del servicio dejó de tener un administrador predefinido: la primera cuenta registrada administra | ninguna clave conocida de antemano | pruebas de identidad y de la API |
| `bench/fragmentos.py` se separó de `bench/gen_book.py` | lo usan el libro y el informe | el libro se genera |
