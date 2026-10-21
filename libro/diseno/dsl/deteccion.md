# DSL — Detección (el motor)

> Experta en **seguir handles por un camino** de la ejecución simbólica y
> decidir si un uso es inválido. Vive dentro de `clang`, como plugin de CSA.
> Dueña de `HandleState`, de los **hechos del contenedor** (el crédito de
> capacidad) y de sus decisiones. No sabe de métricas, del banco ni de
> archivos. Consulta a la Norma sólo por `NormTable` (generada).
>
> Esta versión incorpora [la lógica de la detección](../logica.md): las seis
> premisas, las garantías y el handle que devuelve una mutación.

## 0. Qué tiene que demostrar el motor

Un aviso **confirmado** es un camino factible donde valen las seis premisas
de [la lógica §1](../logica.md#1-la-norma-sola-no-demuestra-nada). Cada
premisa la establece una pieza distinta del motor:

| Premisa | La establece | Con |
|---|---|---|
| P1 Obtención | `acl/` reconoce la llamada; el núcleo crea el `HandleState` | `Obtention` |
| P2 Mutación del **mismo** contenedor | la **región** del contenedor: CSA resuelve `auto& d = c` y `C* p = &c` a la misma región | `ContainerId` |
| P3 Relación | `relate(posición del handle, punto de la mutación)` | `Position`, `Point` |
| P4 Norma | `NormTable.effect` | la tabla generada |
| P5 Identidad | el estado vive en la **región** del handle; una asignación lo reemplaza | `Copy` |
| P6 Uso | `checkLocation` (lectura o escritura); operaciones y comparaciones de un iterador; un iterador pasado a un método del contenedor; un método llamado **sobre** el elemento (`p->m()`); el elemento ligado a un parámetro **referencia**. Pasar un puntero **por valor** no es uso | `Use`, `IteratorMove` |
| Factibilidad | el motor de CSA: sólo explora caminos que el *solver* no descarta | — |

Un aviso **posible** es el mismo camino con P4 = `DependsOn c` y **sin
garantía** que haga falsa `c`.

## 1. Eventos de entrada y de salida

No hay comandos de personas: el motor de CSA produce eventos, y la capa
anticorrupción (`acl/`) los traduce a este idioma.

| Evento del motor (CSA) | Traducido a (`Recognized`) | Ejemplo |
|---|---|---|
| `checkPostCall` de `begin()`, `cbegin()`, `end()` | `Obtention` de un iterador | `auto it = c.begin();` |
| `checkPostCall` de `find`, `lower_bound`, `upper_bound` | `Obtention` de un iterador en `Unknown` | `auto it = s.find(3);` |
| `checkPostCall` de `operator*` / `operator->` sobre un iterador **seguido** | `Use` del iterador **y luego** `Obtention` de un elemento | `const auto& h = *it;` |
| `checkPostCall` de `front()`, `back()`, `operator[]`, `at()`, `data()` | `Obtention` de un elemento | `int& r = c[0];` |
| `checkPostCall` de un mutador reconocido | `Mutation`, y si devuelve iterador, **después** `Obtention` del devuelto | `it = c.erase(it);` |
| `checkPostCall` de `reserve(c.size() + k)` | `Mutation` **y** `Guarantee(c, k)` | `v.reserve(v.size() + 1);` |
| `checkPostCall` del constructor de copia / `operator=` de un iterador, o `checkBind` de un iterador trivial | `Copy(desde, hacia)` | `auto it2 = it;` / `it = c.erase(it);` |
| `checkPreCall` de `operator++`, `--`, `+`, `+=`, `std::next` sobre un iterador seguido | `IteratorMove` | `++it` |
| `checkPreCall` de `==`, `!=`, `<` con un iterador seguido como argumento | `Use` del iterador | `it != c.end()` |
| `checkLocation` (carga o almacenamiento) en una región de elemento seguida o en una subregión suya | `Use` del elemento | `sink(h);`, `sink(h->second);` |
| `checkPointerEscape` del contenedor por una llamada **no reconocida** | `Escape` | `opaca(c);` |
| `checkDeadSymbols` | `Death` | el handle salió de alcance |
| cualquier otra cosa | `NotOurs` | — |

**Una llamada reconocida no es un escape.** Cuando CSA no entra en
`c.push_back(1)`, invalida la región de `c` y avisa `checkPointerEscape`.
Esa llamada ya se tradujo a `Mutation`. Contarla también como escape haría
`Unresolved` todo handle tras cualquier mutación.

| Evento de salida | Lo produce | Lo ve el usuario como |
|---|---|---|
| `HandleObtained` | Obtain | — (estado interno) |
| `HandleInvalidated of MutationEvent` | Apply | **nota** en la ruta: «`h` quedó inválido por `erase` (línea N)» |
| `HandleUnresolved of UnresolvedReason` | Apply / Escape | nota sólo con `PolicyMode=Possibly` |
| `GuaranteeRecorded of Credit` | Guarantee | nota sólo con `PolicyMode=Possibly`: «`reserve` garantiza k inserciones» |
| `InvalidUseDiagnosed` | OnUse | **aviso confirmado** |
| `PossibleUseDiagnosed` | OnUse | **aviso posible** (sólo con `PolicyMode=Possibly`), con la garantía que falta |

## 2. Datos

```
context: Detección

// ── lo que viene de la Norma (generado) ──────────────────────
data Mutation, HandleCategory, Relation, Effect, Condition, Point    // ver Norma
data Growth                                                         // ver Norma: cuánto crece size()

// ── identidades: opacas para el núcleo ───────────────────────
data ContainerId = identidad de la región del contenedor      // envuelve const MemRegion*, como const void*
                                                              // alias por referencia o puntero: la MISMA región
data HandleRef   = identidad de la región del handle
                   // iterador: región del OBJETO iterador (la variable, el temporal)
                   // elemento: región del elemento (D-06); ref y ptr al mismo elemento son uno
data SourceRef   = archivo AND línea AND columna

// ── la posición del elemento en el contenedor ────────────────
data Position =
    First OR Last OR PastEnd
    OR Offset of Position AND integer                       // ++it, it + n
    OR Unknown                                              // find, std::next(it, n) con n simbólico

data HandleKind = IteratorObject OR Element

data Origin = ContainerId AND HandleKind AND Position AND SourceRef

// ── lo que el motor sabe de un handle ────────────────────────
data Validity =
    Valid
    OR Unresolved of UnresolvedReason
    OR UnresolvedDiagnosed of UnresolvedReason              // ya se dio el aviso POSIBLE
    OR Invalidated of MutationEvent                         // la causa viaja con el estado
    OR Diagnosed of MutationEvent                           // ya se dio el aviso confirmado

data UnresolvedReason =
    DependsOnState of Condition AND MutationEvent           // POLICY sin garantía; la mutación, para el mensaje
    OR RelationUnknown of MutationEvent                     // pop_back y el handle puede ser el último
    OR EscapedToOpaqueCode of SourceRef

data HandleState = Origin AND Validity                      // inmutable; vive en ProgramState

data MutationEvent = ContainerId AND Mutation AND PointAt AND SourceRef
data PointAt = Point AND Position                           // Front/Back/Interior/Whole + dónde, si se sabe

// ── lo que el motor sabe de un contenedor ────────────────────
data Credit = Known of natural OR Unknown                   // inserciones garantizadas sin reubicar / sin rehash
data ContainerFacts = Credit                                // ausente del mapa = Unknown

// ── lo que entra al núcleo, ya traducido ─────────────────────
data Recognized =
    Obtention of HandleRef AND Origin
    OR Mutation of MutationEvent
    OR Guarantee of ContainerId AND natural                 // reserve(c.size() + k) → k
    OR Copy of HandleRef AND HandleRef                      // desde, hacia
    OR IteratorMove of HandleRef AND Step AND SourceRef
    OR Use of HandleRef AND HandleCategory AND SourceRef    // la categoría se OBSERVA en el sitio de uso
    OR Escape of ContainerId AND SourceRef
    OR Death of list of HandleRef AND list of ContainerId
    OR NotOurs

data Step = Increment OR Decrement OR Advance of integer OR UnknownStep

// ── la pregunta por una condición ────────────────────────────
data Question = CapacityReached OR RehashTriggered OR SizeIsOne
data SolverAnswer = OnlyYes OR OnlyNo OR Both               // qué es factible en ESTE camino

// ── lo que sale del núcleo ───────────────────────────────────
data UseVerdict =
    Fine
    OR Confirmed of MutationEvent AND HandleCategory
    OR Possibly of UnresolvedReason AND HandleCategory AND MissingGuarantee

data MissingGuarantee =                                     // lo que el mensaje propone
    ReserveBefore                                           // CapacityReached, RehashTriggered
    OR SizeAtLeastTwo                                       // RelationUnknown de pop_back
    OR ReobtainAfter                                        // NonBinding, escape

data Effect' =                                              // efecto de la decisión, no de la norma
    Note of NoteKind AND HandleRef
    OR Report of UseVerdict AND SourceRef

data NoteKind = InvalidatedBy of MutationEvent OR UnresolvedBy of UnresolvedReason OR Guaranteed of Credit

data Decision = list of (HandleRef, optional HandleState)   // optional vacío = se borra del mapa
                AND list of (ContainerId, optional ContainerFacts)
                AND list of Effect'

data PolicyMode = Silent OR Possibly                        // opción del checker
```

**Lo que no está, a propósito:**

- **Ni la capacidad ni el tamaño como número.** El motor sólo guarda el
  **crédito**: lo que el código **garantizó** con `reserve`. No inventa
  estado (D-19).
- **Ni un `bool reported`.** Haber avisado es un estado: `Diagnosed`.
- **Ni el nombre del contenedor en el núcleo.** El núcleo ve `ContainerId`; el
  mensaje lo pone la cáscara.

## 3. Significado

```
meaning Validity    = a point in the chain
                      Valid ⊑ Unresolved ⊑ UnresolvedDiagnosed ⊑ Invalidated ⊑ Diagnosed
                      // UnresolvedDiagnosed está ANTES de Invalidated: un aviso posible
                      // no tapa el confirmado de una invalidación posterior
meaning HandleState = the JOIN of the effects of every mutation of its container
                      since the handle was obtained, along ONE path
meaning Credit      = how many more single insertions the program GUARANTEED
                      without reallocation (vector) or rehash (unordered), along ONE path
meaning Decision    = the change of ProgramState that ONE event causes, plus what the user sees
```

## 4. Constructores y observaciones

| Pieza | Constructores | Observaciones |
|---|---|---|
| `HandleState` | `obtain`, `apply`, `copy`, `move`, `escape`, `diagnose` | `onUse`, `cause`, `position` |
| `Position` | `First`, `Last`, `PastEnd`, `Offset`, `Unknown` | `relate(position, pointAt) → Relation OR Ambiguous of Question`; `transport(m, position)` |
| `Credit` | `guarantee(k)`, `consume(growth)`, `forget` | `answer(question, credit) → SolverAnswer` |
| `Decision` | `decide(event, state, facts, table, mode)` | los cambios y los efectos |

## 5. Leyes

```
// ── obtener y copiar ─────────────────────────────────────────
law "obtener da un handle válido" =
    for all o: validity(obtain(o)) = Valid

law "re-obtener no revive" =
    no decide(...) turns an Invalidated or Diagnosed state of a HandleRef into Valid,
    except Copy into that HandleRef
    // obtener un elemento de nuevo da OTRA región (CSA conjura un símbolo por llamada)

law "asignar reemplaza el handle" =
    after decide(Copy(from, to)): state(to) = state(from)          // si from no se sigue, to se borra
    // así `it = c.erase(it)` deja a `it` válido: no revive el viejo, liga uno nuevo

law "lo que devuelve una mutación es válido" =
    for all m returning an iterator:
    validity(state of the returned handle after decide(Mutation m)) = Valid

// ── aplicar una mutación ─────────────────────────────────────
law "preservar no cambia la validez" =
    when effect(...) = Preserves => validity(apply(m, h)) = validity(h)

law "preservar transporta la posición" =
    when effect(...) = Preserves => position(apply(m, h)) = transport(m, position(h))

law "inválido es absorbente" =
    when validity(h) ∈ {Invalidated _, Diagnosed _} => apply(m, h) = h     // la causa original se conserva

law "aplicar es idempotente en la validez" =
    validity(apply(m, apply(m, h))) ⊑ validity(apply(m, h)) JOIN validity(apply(m, h))

law "otro contenedor no toca" =
    when container(m) ≠ container(h) => apply(m, h) = h

law "un alias es el mismo contenedor" =
    for all c and r = alias of c (referencia o puntero): ContainerId(r) = ContainerId(c)
    // la da CSA; se prueba con lit, no en el núcleo

// ── garantías ────────────────────────────────────────────────
law "sin garantía, depender es posible" =
    when effect(...) = DependsOn c and credit(container) ∈ {Unknown, Known 0}
    => validity(apply(m, h)) = validity(h) JOIN Unresolved(DependsOnState c m)

law "con garantía, depender es preservar" =
    when effect(...) = DependsOn c, c ∈ {CapacityReached, RehashTriggered}, credit = Known k, k ≥ 1
    => apply(m, h) = apply as Preserves

law "una inserción gasta un crédito" =
    when growth(m) = One and credit = Known k, k ≥ 1 => credit' = Known (k − 1)

law "lo que no se cuenta borra el crédito" =
    when growth(m) ∈ {Unknown, Reset} or event = Escape => credit' = Unknown

law "lo que reduce el tamaño no gasta" =
    when growth(m) = Shrinks => credit' = credit
    // conservador: la capacidad no baja; el crédito real podría subir, no se cuenta

law "shrink_to_fit nunca se garantiza" =
    when condition = NonBinding => apply(m, h) = validity(h) JOIN Unresolved(DependsOnState NonBinding m)

// ── usar ─────────────────────────────────────────────────────
law "lo válido no se reporta" =
    when validity(h) = Valid => onUse(h) = Fine

law "no resuelto nunca se informa como confirmado" =
    when validity(h) = Unresolved r => onUse(h) = Possibly(r, cat, missing(r))

law "un aviso posible no tapa uno confirmado posterior" =
    when validity(h) = UnresolvedDiagnosed r and effect(m) = Invalidates
    => onUse(apply(m, h)) = Confirmed m

law "se avisa una vez por handle y camino" =
    when validity(h) = Invalidated m => onUse(h) = Confirmed m  and  after it, validity = Diagnosed m
    when validity(h) = Diagnosed _  => onUse(h) = Fine

law "mover un iterador es usarlo" =
    decide(IteratorMove(h, s), state) reports exactly what decide(Use(h, Iterator), state) reports

law "desreferenciar un iterador es usarlo" =
    the Obtention of an element from *it is preceded by Use(it, Iterator)

law "la categoría del mensaje es la del sitio de uso" =
    onUse(h, cat) = Confirmed(m, cat)       // nunca la de la obtención (contradicción 3)

// ── olvidar ──────────────────────────────────────────────────
law "el estado muere con su región" =
    after decide(Death(hs, cs), state): no h in hs, no c in cs is in the maps

// ── la referencia ────────────────────────────────────────────
law "la decisión es la de referencia" =
    for all event sequences es:
    fold(decide, es) = reference(es)
    // reference: para cada handle, recorrer la lista desde su obtain y tomar el JOIN,
    // con el crédito recalculado desde el último Guarantee
```

## 6. Workflows

```
workflow "Seguir un handle" =                      // cada callback de CSA
    triggered by:  un evento del ExprEngine
    primary input: el evento, traducido por acl/  (Recognized, o una lista de ellos)
    other input:   HandleMap, IteratorMap, ContainerMap del ProgramState; NormTable; PolicyMode
    output:        Decision
    errors:        ninguno de dominio              // lo que no se reconoce es NotOurs

    match Recognized:
        Obtention h o        → do Obtain
        Mutation m           → for each handle of container(m): do Apply
                               then do Consume
        Guarantee c k        → do Guarantee
        Copy from to         → do Copy
        IteratorMove h s     → do OnUse(h, Iterator) then do Move
        Use h cat            → do OnUse
        Escape c             → for each handle of c: do Escape; facts(c) ↦ Unknown
        Death hs cs          → do Forget
        NotOurs              → empty Decision
    return Decision                                // la cáscara: addTransition(state', NoteTag) + emitReport
```

Una llamada produce **varios** `Recognized`, y el orden importa:

| Llamada | Secuencia |
|---|---|
| `*it` | `Use(it)`, `Obtention(elemento)` |
| `c.erase(it)` | `Use(it)` (el argumento), `Mutation`, `Obtention(devuelto)` |
| `it = c.erase(it)` | lo anterior, y luego `Copy(devuelto, it)` |
| `v.reserve(v.size() + k)` | `Mutation(reserve)`, `Guarantee(v, k)` |

```
substep "Obtain" =
    input:  HandleRef AND Origin
    output: Decision with h ↦ HandleState(Origin, Valid)
```

```
substep "Apply" =
    input:        MutationEvent AND HandleState AND ContainerFacts
    output:       HandleState' AND optional Note
    dependencies: EffectOf (NormTable)

    when validity(h) ∈ {Invalidated, Diagnosed}: return h                 // absorbente
    relation = relate(position(h), pointAt(m))
        // Ambiguous SizeIsOne (pop_back y First puede ser Last):
        //   answer = Both en la v1 → Unresolved(RelationUnknown m)
    effect = EffectOf(mutation(m), category(h), relation)
        // category(h): IteratorObject → Iterator; Element → Reference (ley de la norma ref = ptr)
    match effect:
        Preserves              → h with position transport(m, position(h))
        Invalidates _          → h with Invalidated(m), Note
        DependsOn c _          → match answer(question(c), credit):
                                     OnlyNo  → h transported              // hay garantía
                                     OnlyYes → h with Invalidated(m), Note
                                     Both    → h JOIN Unresolved(DependsOnState c m), Note
```

```
substep "answer" =                                 // la v1: sin modelo de tamaño ni capacidad
    CapacityReached, RehashTriggered:
        credit = Known k, k ≥ 1 → OnlyNo
        otherwise               → Both
    SizeIsOne                    → Both
    NonBinding                   → Both            // ninguna garantía la hace falsa
    // OnlyYes no sale en la v1: confirmar «capacidad agotada» exige saber la capacidad.
    // Cuando exista (después de I4), la cáscara preguntará a ConstraintManager::assume.
```

```
substep "Consume" =
    input:  MutationEvent AND ContainerFacts
    output: ContainerFacts'
    match growth(mutation(m)):
        One      → Known k ↦ Known (k − 1)  (Known 0 se queda en 0); Unknown se queda
        Shrinks  → igual
        None     → igual
        Unknown  → Unknown                // resize, insert de rango
        Reset    → Unknown                // clear, assign, shrink_to_fit, rehash, swap
    // reserve(c.size() + k) se consume ANTES y Guarantee fija el crédito DESPUÉS
```

```
substep "Guarantee" =
    input:  ContainerId AND natural k
    output: facts(c) ↦ Known k, Note Guaranteed
```

```
substep "Copy" =
    input:  HandleRef from AND HandleRef to
    output: to ↦ state(from), or to removed if from is not tracked
```

```
substep "Move" =
    input:  HandleState (iterador) AND Step
    output: HandleState with position Offset(position, n), or Unknown
    // si el iterador estaba inválido, OnUse ya avisó antes; Move no lo revive
```

```
substep "OnUse" =
    input:  HandleState AND HandleCategory AND SourceRef AND PolicyMode
    output: UseVerdict AND HandleState'
    Valid                  → Fine
    Unresolved r           → Possibly(r, cat, missing(r)), y pasa a UnresolvedDiagnosed r
                             — sólo si PolicyMode = Possibly; si no, Fine
    UnresolvedDiagnosed _  → Fine
    Invalidated m          → Confirmed(m, cat), y el handle pasa a Diagnosed(m)
    Diagnosed _            → Fine
```

```
substep "Escape" =
    input:  HandleState
    output: Option of HandleState
    // D-21: Valid, Unresolved, UnresolvedDiagnosed → None (se olvida)
    //       Invalidated, Diagnosed               → Some (se conserva)
```

Antes era `HandleState JOIN Unresolved(EscapedToOpaqueCode)`. En ninja eso dio
8 avisos posibles por llamadas como `printf("%p", edge)`, que reciben el objeto
que contiene el contenedor. Nadie corrige un aviso así, y lo que ya estaba
invalidado sigue invalidado haga lo que haga la llamada.

```
substep "Forget" =
    input:  list of HandleRef AND list of ContainerId
    output: Decision que los borra de los mapas
```

## 7. La cáscara: qué guarda el `ProgramState`

| Mapa | Clave | Valor | Muere cuando |
|---|---|---|---|
| `HandleMap` | región del elemento | `HandleState` | su símbolo base muere |
| `IteratorMap` | región del objeto iterador | `HandleState` | la región deja de estar viva |
| `ContainerMap` | región del contenedor | `ContainerFacts` | la región deja de estar viva |

Los tres son `REGISTER_MAP_WITH_PROGRAMSTATE`. El núcleo nunca los ve: recibe
los valores y devuelve una `Decision`, y la cáscara la aplica.

## 8. Preguntas

- `// PREGUNTA (asesor):` con `Both`, ¿bifurcar el camino en dos estados en vez
  de No resuelto? *Propuesta:* no. Bifurcar convertiría todo `POLICY` en un
  aviso confirmado, y la [lógica §3](../logica.md#3-cuando-el-fallo-depende-del-estado-la-garantía)
  pide separar «falla» de «puede fallar».
- `// PREGUNTA:` `reserve(n)` con `n` literal sobre un contenedor recién
  construido vacío. Necesita saber que el tamaño es 0. *Propuesta:* después de
  I4, con un hecho `Fresh` en `ContainerFacts`.
- `// PREGUNTA:` `if (v.size() < v.capacity())` como garantía. Necesita
  modelar `size()` y `capacity()` como símbolos. *Propuesta:* después de I4.
- **Comprobado en código real (RocksDB):** `erase(first, last)` se leía como
  `erase(first)`; en el camino donde `last == begin()` el plugin daba por
  borrado un `last` que sobrevive. `MutationEvent` gana `RangeEnd`, y la
  relación se toma con `relateRange` (D-23). Una constante entera que no cabe
  en `int` (`size_t(-1)` en un camino) abortaba `clang` dentro del ACL: ahora
  es una distancia desconocida.
- **Comprobado en I3** (código real): una posición que el motor no sabe
  medir (`std::next(it)`, el retorno de una función) recibe un **ancla**,
  `Anchor(id)+n` con un símbolo nuevo. Dos handles con la misma ancla se
  relacionan; con anclas distintas la relación es desconocida. El
  `pair<iterator,bool>` de `insert` y `emplace` en `map` se sigue por el
  campo `.first` del temporal. Un iterador pasado por valor a
  `erase(const_iterator)` cae en la región del **parámetro** de la llamada
  (`getParameterLocation`), no en la del argumento.
- **Comprobado en I2** (sonda `plugin/tests/sondas/regiones.cpp`, LLVM 21):
  `begin()` construye el iterador directo en la región de la variable (copia
  elidida); `auto it2 = it` es otra región y llega por `checkBind` (copia
  trivial); cada `*it` conjura una región de elemento nueva; `auto& d = c` da
  la misma región que `c`; `p->second` es subregión del elemento.
