# DSL — Validación dinámica

> Experta en **confirmar las etiquetas ejecutando**. Es un segundo oráculo,
> independiente de la norma escrita y del checker: corre cada caso con
> libstdc++ Debug y con ASan/UBSan, en un proceso aparte. Ya existe
> (`gen_runtime_harness.py`, `run_runtime_validation.py`). Este DSL lo pone
> por escrito.

## 1. Comandos y eventos

```
command "Generar el arnés"     → HarnessGenerated   (runtime_runner.cpp: un main que despacha por nombre de caso)
command "Validar las etiquetas" → RunObserved × (caso, escenario, instrumento)
                                  → ContradictionsComputed
```

## 2. Datos

```
context: Validación dinámica

data Instrument = LibstdcxxDebug OR AsanUbsan

data Scenario =
    Natural                                     // estado inicial ordinario: {1, 2, 3}
    OR Force of Precondition                    // POLICY: se fuerza lo que invalida (capacidad agotada, rehash)
    OR Preserve of Precondition                 // POLICY: se fuerza lo que preserva (reserve(256))
    OR ObservedNonBinding of Precondition       // shrink_to_fit: se registra, no se presupone

data Expectation =
    MustNotDetect                               // SAFE en Natural; POLICY en Preserve
    OR MayDetect                                // UB en Natural; POLICY en Force
                                                // la ausencia de detección NUNCA contradice UB

data Observation =
    Detected of Marker                          // el instrumento informó el uso inválido
    OR NoDetection
    OR UnclassifiedAbort of ExitCode            // terminó mal sin un mensaje reconocible
    OR TimedOut

data RuntimeRun = CaseId AND Scenario AND Instrument AND Observation AND Evidence
data Evidence = text                            // los últimos 4000 caracteres de stderr
data Environment = GxxVersion AND ClangxxVersion AND Standard AND Flags
```

## 3. Significado

```
meaning Validation  = multiset of RuntimeRun, together with the Environment that produced it
meaning Expectation = what the label PROMISES for that scenario, never what the run shows
```

## 4. Leyes

```
law "los escenarios salen de la etiqueta" =
    scenarios(SAFE) = scenarios(UB) = [Natural]
    scenarios(POLICY) = [Force, Preserve]                 // shrink_to_fit: ObservedNonBinding × 2

law "la cobertura es completa" =
    |runs| = Σ over cases of |scenarios(label(case))|, y cada run se observa con los 2 instrumentos
    // banco-1: 648 × 1 + 102 × 2 = 852 ejecuciones

law "una contradicción es una detección donde la norma garantiza validez" =
    contradiction(run) ⇔ expectation(run) = MustNotDetect ∧ observation(run) = Detected _

law "no detectar no contradice" =
    when expectation(run) = MayDetect => run is never a contradiction

law "un aborto sin clasificar no es una detección" =
    UnclassifiedAbort se informa aparte para revisarlo a mano; no confirma ni contradice

law "cada ejecución en su proceso" =
    una caída de un caso no cambia la observación de otro
```

## 5. Workflow

```
workflow "Validar las etiquetas" =
    triggered by:  el tesista o el CI, después de Generar el banco
    primary input: list of Case AND Environment
    output events: RunObserved × |runs|, ContradictionsComputed of list of RuntimeRun
    errors:        HarnessDoesNotCompile of Instrument AND Stderr
                   OR CoverageIncomplete of list of CaseId      // no se publica un resultado parcial como completo

    do BuildHarness    // una vez por instrumento: g++ -D_GLIBCXX_DEBUG ; clang++ -fsanitize=address,undefined
    for each case, for each scenario(label), for each instrument:
        do Observe     // proceso aparte, timeout, ASAN_OPTIONS=detect_leaks=0
    do Contradictions
    return events
```

## 6. Lo que este oráculo dice y lo que no

- **Confirma** que ninguna etiqueta `SAFE` (ni `POLICY` en `Preserve`) es
  falsa **para la entrada que eligió el arnés**. Hoy: 0 contradicciones.
- **No confirma** que un `SAFE` sea seguro para **toda** entrada. Para eso
  está la norma.
- **No sirve para corregir etiquetas `UB` → `POLICY`.** Los 21 casos de la
  contradicción 4 dieron `DETECTADO` en `Natural` porque `{1, 2, 3}` agota la
  capacidad. Con la etiqueta corregida pasan a correr en `Force` y en
  `Preserve`, que es lo que corresponde.

## 7. Preguntas

- `// PREGUNTA:` el entorno registrado de la última corrida (GCC 16, Clang 23)
  no es el de la imagen Docker (LLVM 21). *Propuesta:* volver a correr dentro
  de la imagen al congelar `banco-1`, para que las dos validaciones compartan
  entorno.
- Sigue abierta la decisión de `ASAN_OPTIONS=symbolize=0`, que acorta la
  evidencia guardada.
