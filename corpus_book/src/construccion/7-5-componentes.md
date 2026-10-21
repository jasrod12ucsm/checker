# 7.5 Desarrollo de componentes

![Componentes](../diagramas/7-componentes.svg)

| Componente | Responsabilidad única | Interfaz que ofrece | Depende de | Se prueba con |
|---|---|---|---|---|
| **TablaNormativa** | decir el efecto de la norma | `effect(c, op, cat, rel) → Effect` (`constexpr`) | `matriz.json` (al generar) | leyes de la norma |
| **NucleoInvalidacion** | decidir la validez | `obtain`, `apply`, `onUse`, `escape`, `transport` | TablaNormativa | leyes de la detección |
| **ReconocedorClang** | traducir Clang al lenguaje ubicuo | `recognize(CallEvent, State) → Recognized` | AST/SVal de Clang, Núcleo (tipos) | `lit` |
| **CheckerCSA** | conectar callbacks con el núcleo | `Checker<…>` | Reconocedor, Núcleo, CSA | `lit` + banco |
| **RegistroPlugin** | registrar el checker y sus opciones | `clang_registerCheckers` | CheckerCSA | `lit` `registro.cpp` (RF-01) |
| **GeneradorBanco** | escribir casos y etiquetas desde la norma | `corpus.cpp`, `corpus_truth.json` | `matriz.json` | coherencia norma–banco |
| **Ejecutor** | correr un caso en una condición y registrar su `Outcome` | `Run` | `clang`, plugin (como proceso) | leyes del arnés |
| **Normalizador** | SARIF → `Warning` (confirmado, posible u otro) | `Warning` en memoria | Ejecutor | clase por el texto del aviso |
| **Cotejador** | `Warning` → función y sitio → veredicto | `cotejo.json` | Normalizador, GeneradorBanco | un veredicto por caso y condición; acierto sólo en sitio inválido |
| **Agregador** | conteos y métricas por grupo | `metricas.json` | Cotejador | monoide; `Undefined` |
| **ValidadorDinamico** | confirmar etiquetas ejecutando | `runtime_validation_results.json` | GeneradorBanco | 0 contradicciones |
| **CodigoReal** | correr el checker sobre un proyecto desde su `compile_commands.json` | `test/codigo_real/avisos.json` | `clang`, plugin (como proceso) | 0 caídas; defectos sembrados detectados (`inyeccion.py`) |
| **GeneradorLibro** | publicar todo en el mdbook | `corpus_book/` | `test/experimento/`, `test/codigo_real/` | se construye sin errores |

Cómo se cumplen las características de la práctica:

- **Modularidad:** cada componente tiene una sola responsabilidad.
- **Reutilización:** el núcleo no sabe de CSA. Podría alimentarse desde otro
  motor, y la tabla normativa la usan el checker y el generador del banco.
- **Desacoplamiento:** la evaluación no enlaza el plugin. El checker no sabe
  que existe un banco.
- **Interoperabilidad:** la salida es la estándar de CSA (texto, plist, SARIF).
  SARIF lo leen GitHub y los IDE.
- **Encapsulamiento:** los valores del dominio tienen campos privados y
  constructores que validan. El estado del checker sólo se toca con
  `addTransition`.
