# DSL — Norma

> Experta en **qué dice C++17** de cada mutación. Dueña de `norma/matriz.json`.
> No sabe nada de Clang, de caminos ni de Python. Es la fuente única (D-05):
> la tabla del checker y las etiquetas del banco **salen de aquí**.

## 1. Comandos y eventos

```
command "Corregir una regla" =
    by:      tesista
    input:   Rule con su Clause
    event:   RuleCorrected of Rule
    después: Generar la tabla (Norma) y Generar el banco (Evaluación)

command "Generar la tabla" =
    by:      CMake, como paso de construcción del plugin
    input:   el texto de matriz.json
    event:   TableGenerated of NormTable
```

## 2. Datos

```
context: Norma

data ContainerKind = Vector OR Deque OR List OR ForwardList OR Set OR Multiset
                     OR Map OR Multimap OR UnorderedSet OR UnorderedMap
data HandleCategory = Iterator OR Reference OR Pointer

data Operation = PushBack OR EmplaceBack OR PushFront OR EmplaceFront
                 OR Insert OR InsertAfter OR Emplace OR Subscript
                 OR Erase OR EraseAfter OR PopBack OR PopFront OR Clear OR Assign
                 OR Resize OR Reserve OR ShrinkToFit OR Rehash
                 OR Reverse OR Sort
                                                   // cerrada: una operación nueva es una variante nueva

data Point = Front OR Back OR Interior OR Whole    // dónde actúa la operación
                                                   // Whole: clear, assign, rehash, sort, reverse…

data Mutation = ContainerKind AND Operation AND Point
                                                   // los 57 «pares» del banco son 57 mutaciones

data Relation = Same OR Before OR After OR Any     // el elemento del handle frente al punto
                                                   // Any: el punto es Whole y la relación no importa

data Condition = CapacityReached                   // vector: size() == capacity()
                 OR RehashTriggered                // unordered: la inserción supera el factor de carga
                 OR NonBinding                     // shrink_to_fit: la implementación decide

data Clause = text like "[vector.modifiers]/3"     // no vacía

data Effect =
    Preserves
    OR Invalidates of Clause
    OR DependsOn of Condition AND Clause

data Growth = One                                  // inserta un elemento: push_back, emplace, insert(x)
              OR None                              // reverse, sort, subscript sin inserción
              OR Shrinks                           // erase, pop_*: el tamaño baja, la capacidad no
              OR Unknown                           // resize, insert de rango: no se cuenta
              OR Reset                             // clear, assign, shrink_to_fit, rehash: la capacidad puede cambiar
                                                   // la usa la Detección para gastar el crédito de reserve

data Rule = Mutation AND HandleCategory AND Relation AND Effect
data NormMatrix = non-empty list of Rule
```

**Por qué `Point` y `Relation` y no «erase_begin».** El banco nombra
`erase_begin`, `insert_end`, `insert_middle`: el punto va escrito en el
nombre. La norma no habla de nombres: dice «invalida lo que está **en o
después** del punto». Con `Point` + `Relation` la misma regla sirve para el
banco (handle siempre en el primer elemento) y para código real (handle en
cualquier sitio). Correspondencia con el banco:

| Par del banco | Mutation | Relación del handle (en `First`) |
|---|---|---|
| `vector::erase_begin` | `Vector, Erase, Front` | `Same` |
| `vector::insert_begin` | `Vector, Insert, Front` | `Same` (queda en o después del punto) |
| `vector::insert_end` | `Vector, Insert, Back` | `Before` |
| `vector::pop_back` | `Vector, PopBack, Back` | `Before`, **o `Same` si `size() == 1`** → se decide en la detección |
| `deque::insert_middle` | `Deque, Insert, Interior` | `Before` (ver contradicción 5: hoy el banco inserta en `Front`) |
| `list::sort`, `vector::clear` | `…, Whole` | `Any` |
| `set::erase(first, last)` | `Set, Erase, Front` (el punto de `first`) | `Same` dentro de `[first, last)`, `After` desde `last` |

**Rangos.** `erase(first, last)` no tiene fila propia: es la misma mutación,
leída en el punto de `first`. Lo que cambia es la relación de cada handle,
que se toma frente al **rango semiabierto** (`relateRange` en la detección):
`Before` antes de `first`, `Same` dentro, `After` en `last` o después. La
norma ya dice lo correcto para cada contenedor con esa lectura: en `vector`,
`After` invalida (incluido `last`); en los contenedores de nodos, `After`
preserva. Un rango vacío (`first == last`) no tiene nada en `Same`.

## 3. Significado

```
meaning NormTable = total function from (Mutation, HandleCategory, Relation) to Effect
meaning Effect    = a point in the chain  Preserves ⊑ DependsOn ⊑ Invalidates
```

El orden de `Effect` es el mismo de `Validity` en la detección y de `Label`
en la evaluación. Los tres contextos hablan de **la misma cadena** con
nombres propios.

## 4. Constructores y observaciones

| | |
|---|---|
| Constructores | `parse(texto de matriz.json) → NormMatrix OR list of RuleBroken` (no hay otro) |
| Observaciones | `growth(m) → Growth`, `effect(m, cat, rel) → Effect`, `clause(m, cat, rel) → Clause`, `render(matrix) → NormTable.inc` |

## 5. Leyes

```
law "una referencia y un puntero al mismo elemento siguen la misma regla" =
    for all m, rel:
    effect(m, Reference, rel) = effect(m, Pointer, rel)

law "un iterador nunca está mejor que una referencia al mismo elemento" =
    for all m, rel:
    effect(m, Iterator, rel) ⊒ effect(m, Reference, rel)
    // generaliza «lo que invalida referencias invalida iteradores»:
    // deque::push_back (Invalidates ⊒ Preserves), unordered insert (DependsOn ⊒ Preserves)

law "insertar en un contenedor de nodos no invalida nada" =
    for all c in {List, ForwardList, Set, Multiset, Map, Multimap},
            op in {Insert, InsertAfter, Emplace, PushBack, PushFront, Subscript}, p, cat, rel:
    effect((c, op, p), cat, rel) = Preserves

law "lo que está antes del punto sobrevive en un vector sin reubicar" =
    for all op in {Insert, Erase, PopBack, Resize}, p, cat:
    effect((Vector, op, p), cat, Before) ∈ {Preserves, DependsOn CapacityReached _}

law "una mutación de todo no depende de la relación" =
    for all m with point(m) = Whole, cat, r1, r2:
    effect(m, cat, r1) = effect(m, cat, r2)

law "la tabla es total" =
    for all m in the 57 mutations, cat, rel admissible for point(m):
    effect(m, cat, rel) is defined                     // un hueco es un FN silencioso

law "cada efecto que invalida o depende cita su cláusula" =
    // por construcción: Invalidates y DependsOn llevan Clause; no hay ley que probar

law "ida y vuelta" =
    for all matrix: parse(print(matrix)) = matrix

law "la tabla generada dice lo mismo que la matriz" =
    for all m, cat, rel:
    NormTable.inc::effect(m, cat, rel) = effect(parse(matriz.json), m, cat, rel)
    // §18.4: la versión C++ generada se compara con la de referencia (Python)
```

## 6. Workflow

```
workflow "Generar la tabla" =
    triggered by:  cmake --build (regla personalizada sobre matriz.json)
    primary input: texto de norma/matriz.json
    output events: TableGenerated of NormTable
    errors:        MatrixInvalid of non-empty list of RuleBroken     // se juntan TODOS (aplicativo)
                   OR TableNotTotal of non-empty list of (Mutation, HandleCategory, Relation)
                   OR LawBroken of non-empty list of LawName

    do Parse          // forma y valores cerrados; junta todos los errores
    do CheckTotal     // la ley «la tabla es total»
    do CheckLaws      // las demás leyes de §5; un fallo detiene la construcción
    do Render         // NormTable.inc: constexpr, un switch sin default: por variante
    return TableGenerated

data RuleBroken =
    UnknownContainer of text OR UnknownOperation of text OR UnknownPoint of text
    OR EmptyClause of Mutation
    OR DuplicateRule of Mutation AND HandleCategory AND Relation
```

La construcción **falla** si la matriz rompe una ley. Así una regla mal
escrita no llega ni al checker ni al banco.

## 7. Preguntas

- `// PREGUNTA:` el iterador `end()` (lo que `push_back` siempre invalida) no
  es un handle a un elemento. *Propuesta:* fuera del alcance; el banco nunca
  retiene `end()`.
- `// PREGUNTA:` `rehash(n)` y `reserve(n)` en contenedores *unordered*: si el
  contenedor ya tiene `n` cubetas o más, ¿hay *rehash*? La norma sólo dice que
  **el rehash** invalida iteradores. *Propuesta:* `DependsOn RehashTriggered`
  para iteradores (ver [Evaluación §7](evaluacion.md#7-preguntas)).
- `test/matrix.cpp` (114 casos, N4950) es el antecedente de esta matriz. Queda
  como historia en el libro; no se mantiene como segundo banco.
