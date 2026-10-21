# Modelo del dominio (DSL)

> Método: `modelado-funcional` (Wlaschin, con Elliott y Maguire). **El DSL
> manda sobre el código**: si discrepan, uno de los dos está mal y se decide
> cuál. Lo que no se sabe se escribe como `// PREGUNTA`, no se inventa.
>
> Hay un DSL por contexto. Cada uno sigue el mismo orden: **comandos y
> eventos → datos → significado → constructores y observaciones → leyes →
> workflows → preguntas**.

| Contexto | DSL | Experto en | Estado del código |
|---|---|---|---|
| **Norma** | [norma.md](norma.md) | qué dice C++17 de cada mutación | `norma/matriz.json` + `norma/gen_tabla.py` (tabla generada para el plugin) |
| **Detección** | [deteccion.md](deteccion.md) | seguir handles por un camino y decidir su validez | `plugin/` (I0–I4 hechos) |
| **Evaluación** | [evaluacion.md](evaluacion.md) | generar el banco, ejecutarlo, cotejar y contar | `gen_corpus.py`, `etiquetar.py`, `experimento.py` (una invocación por caso, SARIF, cotejo por sitio), `pruebas_evaluacion.py` |
| **Validación dinámica** | [validacion-dinamica.md](validacion-dinamica.md) | confirmar las etiquetas ejecutando | `gen_runtime_harness.py`, `run_runtime_validation.py` |

## 1. Mapa de contextos

```
                 Norma  (norma/matriz.json, fuente única)
            ↙           ↓                 ↘
     Detección      Evaluación      Validación dinámica
   (dentro de clang)  (Python)          (Python)
          ↖_______________↙
     sólo por la salida de clang (SARIF/plist), como proceso
```

| Relación | Tipo (Wlaschin §11) | Cómo se cumple |
|---|---|---|
| Detección → Norma | cliente/proveedor | la tabla C++ **se genera** de la matriz; la detección no la edita |
| Evaluación → Norma | cliente/proveedor | las etiquetas **se generan** de la matriz |
| Validación dinámica → Evaluación | conformista | lee los casos y etiquetas tal como el banco los define |
| Evaluación → Detección | **ninguna en código** | la evaluación invoca `clang` como proceso y lee SARIF. Es la capa anticorrupción del lado de la medición (D-11) |

## 2. Todos los comandos y sus eventos

| Contexto | Comando (lo pide alguien) | Quién | Evento (lo que pasó) |
|---|---|---|---|
| Norma | **Corregir una regla** | tesista, con la cláusula | `RuleCorrected` |
| Norma | **Generar la tabla** | CMake (paso de construcción) | `TableGenerated` |
| Evaluación | **Generar el banco** | tesista | `BankGenerated` |
| Evaluación | **Congelar el banco** | tesista | `BankFrozen` (tag `banco-N`) |
| Evaluación | **Ejecutar el experimento** | evaluador / CI | `RunRecorded` × caso × condición → `WarningsNormalized` → `CasesMatched` → `MetricsComputed` |
| Evaluación | **Publicar el experimento** | evaluador | `ExperimentPublished` (tag `exp-…`) |
| Validación dinámica | **Generar el arnés** | tesista | `HarnessGenerated` |
| Validación dinámica | **Validar las etiquetas** | tesista / CI | `RunObserved` × caso × escenario × instrumento → `ContradictionsComputed` |
| Detección | **Analizar código** | desarrollador (`clang --analyze`) | por cada camino: `HandleObtained`, `HandleInvalidated`, `HandleUnresolved`, `InvalidUseDiagnosed`, `PossibleUseDiagnosed` |

La Detección es distinta de los otros tres: **no recibe comandos de una
persona**, recibe **eventos del motor** de CSA (una llamada, una carga, un
enlace). Por eso su DSL empieza por los eventos de entrada.

## 3. Lenguaje ubicuo

| Término | Significa | En el código | Nunca se dice |
|---|---|---|---|
| **Contenedor** | un objeto de los 10 tipos del alcance | `ContainerKind`, `ContainerId` | «colección», «objeto» |
| **Operación** | un método del contenedor (`erase`, `push_back`…) | `Operation` | «función» suelta |
| **Punto** | dónde actúa la operación: frente, fondo, interior, todo | `Point` | «posición» (es otra cosa) |
| **Mutación** | una operación en un punto, sobre un contenedor | `Mutation`, `MutationEvent` | «modificación» |
| **Handle** | iterador, referencia o puntero a un elemento | `HandleState` | «identificador» (el informe anterior lo usaba) |
| **Categoría** | iterador │ referencia │ puntero | `HandleCategory` | «tipo de handle» |
| **Obtención** | el momento en que un handle queda ligado a un elemento | `Origin` | «registro» |
| **Posición** | dónde está el elemento del handle en el contenedor | `Position` | «índice» |
| **Relación** | dónde está el handle respecto del **punto** de la mutación | `Relation` | — |
| **Efecto** | lo que la norma dice de una mutación para un handle | `Effect` | «resultado de la regla» |
| **Condición** | de qué estado depende un efecto (capacidad, rehash, no vinculante) | `Condition` | «política» suelta |
| **Validez** | lo que el checker sabe del handle en este camino | `Validity` | «estado» a secas |
| **Uso** | leer o escribir a través del handle, o mover un iterador | `Use` | — |
| **Aviso confirmado / posible** | las dos clases de diagnóstico | `UseVerdict` | «warning» suelto |
| **Caso** | una función del banco: (contenedor, mutación, categoría, forma) | `Case` | «test» |
| **Forma** | cómo está escrito el caso: recto, guarda, bucle, llamada | `Form` | — |
| **Etiqueta** | lo que la norma dice del caso **para toda entrada válida**: `UB`, `SAFE`, `POLICY` | `Label` | «esperado» |
| **Condición experimental** | `referencia` (CSA solo) o `experimental` (CSA + plugin) | `Configuration` | «modo» (choca con «escenario») |
| **Escenario** | el estado inicial que fija la validación dinámica: natural, force, preserve | `Scenario` | «modo» |
| **Instrumento** | libstdc++ Debug o ASan/UBSan | `Instrument` | «sanitizador» a secas |
| **Cotejo** | relacionar avisos con casos etiquetados | `Match` | «comparación» |
| **Incidencia** | una ejecución que no terminó (error, caída, *timeout*) | `Incident` | «sin avisos» |

## 4. Lo que el modelado encontró antes de programar

Al escribir estos DSL salieron **dos errores en las etiquetas del banco
actual** y una revisión pendiente. Están en
[Significado y leyes, contradicciones 4 y 5](../leyes.md#contradicción-4--el-bucle-convierte-depende-en-ub)
y en [Evaluación §7](evaluacion.md#7-preguntas). Se corrigen **antes** de
congelar `banco-1`.
