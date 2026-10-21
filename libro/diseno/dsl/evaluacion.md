# DSL — Evaluación

> Experta en **medir**: generar el banco desde la norma, ejecutarlo en dos
> condiciones, cotejar los avisos con las etiquetas y contar. Dueña de casos,
> ejecuciones, cotejos y conteos. **No ve el `ProgramState`**: sólo la salida
> de `clang`. Vive en `bench/` (Python).

## 1. Comandos y eventos

```
command "Generar el banco"         → BankGenerated of list of Case
command "Congelar el banco"        → BankFrozen of BankVersion            // tag banco-N; desde aquí no se edita
command "Ejecutar el experimento"  → RunRecorded × (caso, condición)
                                     → WarningsNormalized → CasesMatched → MetricsComputed
command "Publicar el experimento"  → ExperimentPublished of RunId         // tag exp-…, resultados como release asset
```

## 2. Datos

```
context: Evaluación

// ── el banco ─────────────────────────────────────────────────
data Form = Straight OR Guard OR Loop OR Call          // recto, guarda, bucle, llamada
data Label = SAFE OR POLICY OR UB                       // orden: SAFE ⊑ POLICY ⊑ UB

data Precondition =
    NonEmpty                                            // recto: c.begin() se desreferencia sin mirar
    OR None                                             // guarda, llamada: comparan con end()
                                                        // bucle: el for no entra si está vacío

data Handle = Held of HandleCategory                    // el que declara el caso
              OR ControlIterator                        // el iterador del for, sólo en Loop

data Case = CaseId AND Mutation AND HandleCategory AND Form AND Precondition AND Label
data CaseId = text like "f_vector_erase_begin_ref_recto"   // nombre de la función; único
data BankVersion = integer at least 1

// ── las condiciones experimentales ───────────────────────────
data BaseConfig = ClangVersion AND list of Checker AND list of AnalyzerOption AND Timeout
data PluginBuild = path AND sha256 AND PolicyMode
data ExperimentPair = BaseConfig AND PluginBuild
    // la condición de referencia ES base; la experimental ES base + plugin.
    // «las dos difieren sólo en el plugin» (RN-002) no se valida: no se puede escribir otra cosa

data Configuration = Reference OR Experimental of PolicyMode     // las dos caras de un ExperimentPair
                    OR PluginOnly of PolicyMode                  // D-25: core + cplusplus + plugin

// ── lo que pasó al ejecutar ──────────────────────────────────
data Outcome =
    Completed of RawOutput AND Seconds AND MaxRss
    OR CompileError of Stderr
    OR Crash of Stderr
    OR Timeout of Seconds
    OR Unreadable of Stderr                             // terminó pero su SARIF no se pudo leer

data Run = RunId AND CaseId AND Configuration AND Outcome

data WarningClass = Confirmed OR Possible OR Other     // Other: de un checker de CSA, no del nuestro
data Warning = file AND line AND CheckerName AND WarningClass AND Message

// ── el cotejo ────────────────────────────────────────────────
data Verdict =
    TP OR FP OR FN OR TN                                // casos UB y SAFE, con avisos confirmados
    OR PolicyWarned OR PolicySilent                      // casos POLICY: aparte, nunca en precisión
    OR Incident of Outcome                               // un fallo NUNCA es TN

data Site = Held OR Control OR Elsewhere               // sobre qué handle del caso cae el aviso
data Match = CaseId AND Configuration AND Verdict AND list of (Warning AND Site)
data Counts = tp AND fp AND fn AND tn AND policyWarned AND policySilent AND incidents   // todos ≥ 0
data GroupKey = ByContainer OR ByOperation OR ByCategory OR ByForm OR ByLabel OR All
data Metric = Defined of Ratio OR Undefined             // 0/0 no es 0
```

**Qué significa una etiqueta.** Es lo que la norma dice del caso **para
toda entrada que cumple su precondición**:

| Etiqueta | Para toda entrada válida… |
|---|---|
| `UB` | **toda** ejecución usa un handle inválido |
| `SAFE` | **ninguna** ejecución lo hace |
| `POLICY` | depende de la entrada (capacidad, factor de carga, tamaño) |

Las funciones del banco reciben `c` por referencia, **sin estado conocido**.
CSA también lo ve así: no sabe la capacidad ni el tamaño de `c`. La etiqueta
tiene que hablar de esa misma función, no de la entrada que después elige la
validación dinámica.

## 3. Significado

```
meaning Bank    = finite set of Case, keyed by CaseId
meaning Label   = the JOIN, over the handles of the case and the mutations each one sees,
                  of the norm's effects read as labels (Preserves→SAFE, DependsOn→POLICY, Invalidates→UB)
meaning Counts  = multiset of Verdict, observed through its seven counts
meaning Metric  = function of Counts; Undefined where the denominator is 0
```

## 4. Constructores y observaciones

| Pieza | Constructores | Observaciones |
|---|---|---|
| `Case` | `generate(norm, mutation, category, form)` | `label`, `precondition`, `source` |
| `Counts` | `empty`, `of(verdict)`, `combine` | los siete conteos |
| `Metric` | — (derivada) | `precision`, `recall`, `f1`, `policyRate` |

## 5. Leyes

```
law "la etiqueta es el JOIN de sus handles" =
    for all case:
    label(case) = JOIN over h in handles(case) of labelOf(effects seen by h)
    // Loop tiene dos handles: Held y ControlIterator

law "repetir una mutación no cambia la etiqueta" =
    labelOf([e, e, e]) = labelOf([e])                   // JOIN es idempotente
    // en particular: tres push_back que DEPENDEN siguen dependiendo, no pasan a UB

law "la etiqueta sale de la norma" =
    for all case with form ∈ {Straight, Guard, Call}:
    label(case) = labelOf(effect(mutation(case), category(case), relation at First))

law "cada caso del banco es único" =
    for all c1, c2 in bank: id(c1) = id(c2) => c1 = c2

law "los conteos se suman por partes" =
    counts(A ++ B) = counts(A) + counts(B)   and   counts([]) = 0

law "una métrica sin denominador no es cero" =
    when tp + fp = 0 => precision = Undefined

law "un fallo nunca es un verdadero negativo" =
    when outcome(run) ∉ Completed => verdict(run) = Incident(outcome)

law "POLICY no entra en la precisión" =
    precision(counts) depends only on tp, fp      // policyWarned y policySilent se informan aparte

law "normalizar dos veces es normalizar una" =
    normalize(normalize(x)) = normalize(x)

law "cada caso recibe exactamente un veredicto por condición" =
    for all bank, configuration: |matches| = |bank|

law "un aviso pertenece a lo más a un caso" =
    for all w: |{case | w is inside case}| ≤ 1     // los de fuera se informan como no atribuidos

law "los conteos se reconstruyen desde el cotejo" =
    counts(group) = Σ of(verdict) over matches of group

law "ida y vuelta de los resultados" =
    read(write(run)) = run                          // ejecucion.json, cotejo.json
```

## 6. Workflows

```
workflow "Generar el banco" =
    triggered by:  el tesista, después de corregir la norma
    primary input: NormMatrix AND list of (Mutation, HandleCategory, Form)   // 57 × 3 × 4 = 684, + 66 de Guarantee = 750
    output events: BankGenerated of list of Case  (corpus.cpp + corpus_truth.json)
    errors:        BankFrozen                     // no se regenera un banco congelado: se crea banco-N+1

    for each template:
        do WriteSource        // la función C++ de la forma
        do Label              // la ley «la etiqueta es el JOIN de sus handles»
    return BankGenerated
```

```
workflow "Ejecutar el experimento" =
    triggered by:  el evaluador o el CI
    primary input: BankVersion (congelada) AND ExperimentPair
    output events: RunRecorded × 2·|bank|, WarningsNormalized, CasesMatched, MetricsComputed
    errors:        BankNotFrozen
                   OR PluginNotLoadable of Stderr      // se prueba ANTES de ejecutar los 1368 casos
                   // un fallo de un caso NO es un error del workflow: es Incident

    do VerifyInputs     // banco congelado; el plugin carga y el checker aparece en -analyzer-checker-help
    for each case, for each configuration:
        do Run          // una invocación de clang por caso con -analyze-function=<case> (D-15)
    do Normalize        // SARIF → list of Warning
    do Attribute        // Warning → CaseId por el rango de líneas de la función
    do Match            // (Case, Outcome, warnings) → Verdict
    do Aggregate        // Counts por GroupKey; métricas al final
    return events
```

```
substep "Match" =
    input:  Case AND Outcome AND list of Warning (de nuestro checker y de CSA)
    output: Verdict
    when outcome is not Completed          → Incident(outcome)
    confirmed = warnings with class Confirmed (o, en Reference, cualquier aviso alpha.cplusplus.*)
    good      = confirmed whose site's handle has label UB      // cotejo por sitio (D-24)
    match label(case):
        UB     → TP if good else FN                              // un aviso sobre un handle válido no acierta
        SAFE   → FP if confirmed else TN
        POLICY → PolicyWarned if any warning (Confirmed o Possible) else PolicySilent
    // los avisos Possible sobre casos UB/SAFE se cuentan aparte, no cambian TP/FP
```

Además de la cobertura **por caso**, se publica la cobertura **sobre el
sostenido**: casos `UB` cuyo handle declarado es `UB` y recibe el aviso. Es la
que separa «CSA ve el caso por el iterador del `for`» de «CSA ve la referencia».

## Implementación

| Pieza del DSL | Dónde |
|---|---|
| `VerifyInputs` (plugin cargable, versiones, sha256, banco congelado) | `bench/experimento.py: verificar` |
| `Run` → `Outcome` (con `MaxRss` por `wait4`) | `ejecutar` |
| `Normalize` (SARIF → `Warning`) | `normalizar` |
| `Attribute` (función y sitio) | `atribuir`, `sitio` |
| `Match` | `cotejar` |
| `Counts` (monoide) y `Metric` (`None` = `Undefined`) | `Counts`, `metricas` |
| Leyes de §5 | `bench/pruebas_evaluacion.py` (11 pruebas) y aserciones al final de `main` |

## 7. Preguntas

**Errores del banco actual, encontrados al escribir este DSL** (detalle en
[leyes, contradicciones 4 y 5](../leyes.md#contradicción-4--el-bucle-convierte-depende-en-ub)):

| # | Casos | Hoy | Por la norma | Corrección propuesta |
|---|---:|---|---|---|
| 4 | 21: `bucle` de `vector` (`push_back`, `emplace_back`, `insert_end`, `resize_grow`, `reserve`, `pop_back`) × 3 categorías, y `bucle` de `uset::insert`, `umap::insert`, `umap::subscript` con iterador | `UB` | `POLICY` | regla del bucle en `gen_corpus.py` |
| 6 | 6: `bucle` de `uset::insert`, `umap::insert`, `umap::subscript` con referencia o puntero | `SAFE` | `POLICY` (el iterador del `for` depende del *rehash*) | la regla del bucle debe ser el JOIN de los dos handles |
| 5 | 6: `deque::insert_middle` con referencia o puntero, formas `recto`, `guarda`, `llamada` | `UB` | `SAFE` (la sentencia inserta en el **frente**) | cambiar la sentencia a `c.insert(c.begin() + 1, 1)`, que sí es interior; la etiqueta `UB` queda correcta |

- `// PREGUNTA (asesor):` 18 casos más a revisar: `rehash`/`reserve` de
  `unordered_set` y `rehash` de `unordered_map` con iterador (y su `bucle`).
  Están etiquetados `UB`; si el contenedor ya tiene cubetas suficientes, la
  norma no garantiza que haya *rehash*. *Propuesta:* `POLICY`.
- `// PREGUNTA (asesor):` ¿los avisos «posibles» entran en las métricas
  principales? *Propuesta:* no; se publican como `policyRate` y como
  «posibles sobre UB/SAFE». **Así está implementado.**
- Corregir el banco cambia sus cifras. **Hecho** (D-18, D-20): 750 casos, 342
  `UB`; la referencia y la validación dinámica se volvieron a correr. Falta
  congelar `banco-1` con el visto bueno del asesor.
