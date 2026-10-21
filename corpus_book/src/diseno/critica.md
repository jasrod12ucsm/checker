# Por qué se rehízo el diseño

> **Estado:** propuesta de diseño, 2026-10-18. Todavía no hay código del
> checker. Lo que este capítulo afirma del analizador de referencia sale del
> corpus ya ejecutado; lo que afirma del checker son decisiones por comprobar.

Había **dos diseños**, y ninguno era el del proyecto:

| Documento | Qué diseñaba | Problema de fondo |
|---|---|---|
| Libro de diagramas (`book/`, PlantUML) | `mi-linter`: un ejecutable con **LibTooling y AST matchers** cuya única regla es `catch` por valor | No es el producto. La tesis es un **checker de Clang Static Analyzer** (CSA) |
| Capítulo 5 del informe (Word) | Un checker de CSA, pero con **clases conceptuales genéricas** | Las clases no podían existir dentro de CSA, y los estados ilegales se podían escribir |

## 1. El libro de diagramas diseñaba otra herramienta

`mi-linter` recorre el AST con `MatchFinder` y emite un *warning* por cada
coincidencia. Eso sirve para patrones **locales** (un `catch` mal escrito),
pero la invalidación no es un patrón local. Hace falta saber **qué pasó antes
en el mismo camino de ejecución**:

```cpp
auto it = c.begin();
const auto& h = *it;      // 1. h apunta al primer elemento de c
if (cond) c.erase(c.begin());   // 2. sólo en un camino
sink(h);                  // 3. UB en un camino, válido en el otro
```

Un AST matcher ve tres sentencias sueltas. No puede responder «¿en este
camino hubo un `erase` entre la obtención y el uso?» ni «¿`h` y `*it` son el
mismo elemento?». CSA sí: ejecuta el programa de forma **simbólica, camino
por camino**, y en cada camino lleva un `ProgramState` inmutable donde un
checker puede guardar lo que sabe.

Por eso **el diseño de `mi-linter` no se reutiliza**. El prototipo queda en
el repositorio como antecedente (`src/MiLinter.cpp`) y se retira cuando
exista el plugin.

## 2. El capítulo 5 del Word era de CSA, pero estaba mal modelado

El capítulo 5 nombraba bien las piezas (motor, checker, estado del camino,
arnés), pero sus diagramas no se podían implementar tal como estaban. Los
problemas, uno por figura:

### Figura 5.4 — clases

| Lo que decía | Por qué está mal | Lo que se propone |
|---|---|---|
| `validez: String` («válido, inválido o no resuelto») | Un `String` admite `"valido "`, `"Valido"` o `"x"`. Es un estado que se escribe con texto | `Validity` = **suma** `Valid │ Unresolved{razón} │ Invalidated{causa}` |
| `categoria: String`, `contenedor: String`, `operacion: String` | Lo mismo: cualquier texto pasa | `HandleCategory`, `ContainerKind`, `Mutation`: **enums cerrados**, sin `default:` en los `switch` |
| `RegistroContenedor.capacidad: Integer [0..1]` | En CSA la capacidad **no es un entero**: es un valor simbólico sobre el que se pregunta al *solver* | La capacidad no se guarda: se **pregunta** (`assume(size == capacity)`) en el momento de la mutación |
| `ReglaInvalidacion.evaluarCondiciones(): String` | Una regla de la norma no es un objeto con estado ni devuelve texto: es una **función** | `NormTable::effect(contenedor, op, categoría, relación) → Effect`, **generada** de una matriz versionada |
| `CheckerInvalidacion.registrarObtencion(): void`, `actualizarValidez(): void` | `void` esconde lo que cambia. En CSA un callback **no muta**: produce un estado nuevo con `addTransition` | Funciones puras `(estado, evento) → (estado', efectos)`; la cáscara aplica los efectos |
| Clases sin relación con la API real | Ninguna aparecía en `ProgramState`, `CallEvent` ni `MemRegion` | Se separa **dominio puro** de **anticorrupción** (traduce Clang) y de **cáscara** (habla con CSA) |

### Figura 5.5 — estados

- Faltaba **qué pasa al usar** cada estado (el aviso es la salida del modelo).
- «No resuelto → Inválido por *invalidez establecida*» no decía qué evento la
  establecía.
- No decía que **Inválido es absorbente** ni cómo un handle *re-obtenido* se
  distingue del viejo. Sin esa regla, `h = *c.begin()` después de un `clear`
  reviviría el handle anterior.
- No modelaba la **bifurcación de caminos**, que es exactamente cómo CSA
  resuelve los casos `POLICY` (capacidad, factor de carga).

### Figuras 5.2, 5.3, 5.6 y 5.7

- **Colaboración:** «Checker atiende eventos» no nombra **cuáles**
  (`checkPostCall`, `checkLocation`, `checkBind`…). Sin eso no se sabe si el
  diseño detecta el uso de una referencia, que no es una llamada.
- **Paquetes:** no aparecía la **matriz normativa** como fuente única. Hoy las
  etiquetas del banco viven en Python (`gen_corpus.py`), y si el checker
  escribe su propia tabla a mano, las dos se van a separar.
- **Lógica y física:** no decían **cómo entra el checker a Clang**. Recompilar
  LLVM no es viable para una tesis. La propuesta es un **plugin** (`.so`)
  cargado con `-load`, construido en la misma imagen Docker LLVM 21 que ya
  usa el repositorio.

## 3. Lo que el corpus ya dice, y que el diseño anterior ignoraba

> Esta crítica se escribió con el banco anterior de 684 casos. El banco
> congelado `banco-1` tiene 750 (342 `UB`, 306 `SAFE`, 102 `POLICY`); sus
> resultados están en el capítulo 7.

El banco de 684 casos ya se ejecutó contra los checkers `alpha.cplusplus.*`
de CSA ([Análisis estático](../resultados/estatico.md)):

| Handle retenido | Casos `UB` | Detectados por CSA hoy |
|---|---:|---:|
| iterador | 137 | **79.6 %** |
| referencia | 113 | **0 %** |
| puntero | 113 | **0 %** |

Y los 75 casos `POLICY` nunca dan aviso, porque CSA asume que nunca hubo
reubicación. Esto **decide el alcance**:

1. **El aporte está en referencias y punteros a elementos.** Ahí CSA no ve
   nada. Es el primer incremento, no el último.
2. Los iteradores ya están bastante cubiertos. El checker los modela igual,
   porque **toda referencia del banco sale de un iterador** (`*it`, `&*it`),
   pero no compite por ellos.
3. Los casos `POLICY` necesitan una **política explícita** (RF-04, RF-09), no
   silencio.

Hay una restricción técnica que el diseño anterior no veía: los rasgos de
estado de `IteratorModeling` y `ContainerModeling` **no son API pública** de
Clang (viven en `lib/StaticAnalyzer/Checkers/Iterator.h`). Un plugin no puede
leerlos. **El checker tiene que llevar su propio modelo** de contenedores,
iteradores y elementos. En términos de DDD, es un contexto dueño de sus datos.

## 4. Cómo se rehízo

Se siguió el método de las skills de diseño del proyecto hermano
(`modelado-funcional`, `bodega-arquitectura`, `rust-trinity`, `donde-va`),
traducido a C++ y a CSA:

1. **Eventos y lenguaje ubicuo** → [Modelo del dominio](dsl/index.md), un DSL por contexto.
2. **Significado y leyes** de cada pieza, y contradicciones resueltas antes de
   programar → [Significado y leyes](leyes.md).
3. **Tipos que hacen irrepresentable lo ilegal** → [5.4 Clases](cap5/5-4-clases.md).
4. **Núcleo puro, bordes tontos**: cargar → decidir → aplicar efectos →
   [5.6 Arquitectura lógica](cap5/5-6-arquitectura-logica.md).
5. **Una frontera que el compilador hace cumplir**: el núcleo es un *target*
   de CMake **sin** los directorios de cabeceras de Clang. Si alguien escribe
   `#include "clang/…"` en el dominio, **no compila** →
   [Dónde va cada cosa](donde-va.md).
