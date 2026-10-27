# Significado y leyes

> Método: primero **qué ES** cada pieza, en una línea (Wlaschin, 2018).
> Después **las igualdades que se cumplen siempre**. Después se buscan
> **contradicciones** llevando una misma expresión por dos caminos. Las seis
> contradicciones de abajo se encontraron así: las tres primeras cambiaron el
> diseño del motor antes de escribir su código; las tres últimas corrigieron
> el banco antes de sellarlo.

Esta sección es del motor de análisis. En el servicio, el mismo método se
aplicó a sus tipos: `Revision<E>` no admite un estado ilegal y
`Autorizado<P>` no admite una operación sin permiso, y lo que **no** debe
compilar se prueba con `@ts-expect-error` (sección 7.1.3).

## 1. Qué ES cada cosa

```
NormTable   ES una función de (ContainerKind, Mutation, Category, Relation) en Effect
Validity    ES un punto de la cadena  Valid ⊑ Unresolved ⊑ Invalidated
HandleState ES el pliegue (JOIN) de los efectos de cada mutación de su
            contenedor desde que se obtuvo el handle, a lo largo de UN camino
Diagnosis   ES (sitio de uso, handle, la mutación que lo causó)
Counts      ES un multiconjunto de veredictos, observado solo por sus cuatro conteos
Metric      ES una función de Counts; indefinida donde el denominador es 0
```

Dos consecuencias inmediatas:

- **La validez es un semirretículo** con `JOIN = máximo` y `Valid` como
  identidad. Juntar efectos es asociativo, conmutativo e idempotente. No hay
  que «recordar» en qué orden se aplicaron: el máximo ya lo dice.
- **Los conteos son un monoide conmutativo** (suma componente a componente,
  identidad `0`). Por eso se pueden calcular por contenedor, por forma o en
  paralelo y sumar. **Las métricas no**: una precisión no se suma ni se
  promedia. Se suman los conteos y se divide **al final**.

## 2. Constructores y observaciones

| Pieza | Constructores | Observaciones (la única salida) |
|---|---|---|
| `HandleState` | `obtain`, `apply(mutation)`, `escape`, `transport` | `onUse`, `cause` (para la nota) |
| `NormTable` | se genera de `matriz.json` | `effect(c, op, cat, rel)` |
| `Counts` | `empty`, `of(verdict)`, `combine` | `tp`, `fp`, `fn`, `tn` |
| `Metric` | — (derivada) | `precision`, `recall`, `f1` |

## 3. Las leyes

Las leyes están escritas en la especificación de cada contexto, junto a sus
datos, y se comprueban con pruebas automáticas:

| Contexto | Leyes escritas | Pruebas que las comprueban |
|---|---:|---|
| Norma | 9 | 4 comprobaciones al generar la tabla (`norma/gen_tabla.py`, `check_leyes`: la generación falla si una no vale) y 4 gtests `Norma.*` |
| Detección | 25 | 24 gtests `Deteccion.*`, 9 `Posicion.*` y 2 `Lenguaje.*`; las leyes de categoría, uso y muerte de regiones, que dependen de Clang, con los `lit` del checker |
| Evaluación | 13 | 11 leyes en `bench/pruebas_evaluacion.py` y el gtest `Banco.ElVeredictoDelNucleoEsLaEtiqueta` |
| Validación dinámica | 6 | `bench/run_runtime_validation.py`: 852 ejecuciones, 0 contradicciones |

Lo que sigue es **el razonamiento**: qué contradicciones aparecieron al
llevar las leyes por dos caminos y cómo cambiaron el diseño.

## 4. Contradicciones encontradas y cómo se resolvieron

Procedimiento: tomar una expresión chica, reescribirla con las leyes
por dos caminos y ver si dan lo mismo. Si no, **no se agrega una ley
parche**: se quita una ley o se cambia el tipo de una observación.

### Contradicción 1 — «Primero» deja de ser primero

Se guardaba la posición tal como se obtuvo (`First`). Expresión:

```cpp
std::deque<int> c = …;
const auto& h = *c.begin();     // h: First
c.push_front(0);                // deque: preserva referencias
c.erase(c.begin() + 1);         // borra el elemento de h
use(h);                          // UB
```

- Camino A, con «preservar no cambia la validez»: tras `push_front`, `h`
  sigue `Valid` en `First`. `relate(First, Offset(First,1)) = Before` → la
  norma dice `Preserves` → **no hay aviso**.
- Camino B, la semántica: el elemento de `h` **es** el borrado → UB.

Los dos caminos no coinciden. La ley «preservar no cambia la validez» es
correcta. Lo que estaba mal era la observación: **la posición describía el
índice al obtener, no el elemento**. Resolución:

```
law "preservar transporta la posición" =
    when effect(...) = Preserves =>
    position(apply(m, h)) = transport(m, position(h))

transport(push_front, First)     = Offset(First, 1)
transport(insert en contenedor ordenado, p) = Unknown(PositionUnknown)   // el orden lo decide la clave
```

Para los contenedores asociativos la posición queda **desconocida** tras una
inserción. Por eso `Relation` tiene `Unknown`, y la tabla tiene que definir
qué pasa con él (ley «la tabla es total»).

### Contradicción 2 — revivir un handle

Las leyes «inválido es absorbente» y «obtener da un handle válido» chocan si
el handle es **la variable**:

```cpp
const int* p = &*c.begin();
c.clear();                       // p: Invalidated
p = &*c.begin();                 // ¿p vuelve a Valid?  por absorbente no; por obtener sí
```

Resolución: **un handle es la región del elemento, no la variable**. Cada
obtención produce una región nueva (CSA conjura un símbolo por cada llamada
no inlineada a `operator*`), así que la segunda línea crea **otro** handle.
`p` sólo cambia a cuál apunta. Las dos leyes valen sin excepciones. Es la
razón de que `HandleMap` esté indexado por `const MemRegion*` y no por
`VarDecl`.

### Contradicción 3 — referencia y puntero al mismo elemento

```cpp
const auto& r = *it;
const auto* p = &r;              // misma región que r
```

Si el estado guarda la categoría (`Reference`), un uso de `*p` produce un
mensaje que dice «referencia». Si guarda `Pointer`, lo dice mal para `r`. Es
la misma región: **la categoría no es una propiedad del handle sino del sitio
de uso**. Resolución, apoyada en la ley de la norma «una referencia y un
puntero siguen la misma regla»:

- El estado guarda sólo `HandleKind = IteratorObject | Element`.
- El texto «referencia» o «puntero» del mensaje se **observa en el sitio de
  uso** (el tipo de la expresión), no se guarda.
- La tabla normativa conserva las tres columnas, porque la ley se **prueba**
  sobre ella. El núcleo consulta `Reference` para todo `Element`.

### Contradicción 4 — el bucle convierte «depende» en UB

`bench/gen_corpus.py` etiqueta la forma `bucle` con esta regla:

```python
e = "UB" if ctx == "bucle" and (exp_it == "UB"
        or (op in INSERCION and exp == "POLICY")
        or (op == "pop_back" and exp == "POLICY")) else exp
```

La primera parte es correcta: si la mutación invalida el iterador de control,
`++it` es UB en la primera vuelta, para toda entrada. Las otras dos no lo son.
Expresión:

```cpp
void f_vector_push_back_ref_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.push_back(1);          // DependsOn CapacityReached, tres veces
    sink(h);
  }
}
```

- Camino A, con «repetir una mutación no cambia la etiqueta» (el JOIN es
  idempotente): `POLICY ⊔ POLICY ⊔ POLICY = POLICY`.
- Camino B, con la regla del generador: `UB`.

Los dos caminos no coinciden, y **la ley tiene razón**. `c` llega por
referencia sin estado conocido. Si `capacity() ≥ size() + 3`, ninguna de las
tres inserciones reubica, `it` y `h` siguen válidos, y no hay UB. El
comentario del generador («el crecimiento repetido termina forzando el caso
invalidante») vale para la entrada `{1, 2, 3}` del arnés, no para la
función. Con `pop_back` pasa lo mismo: con `size() ≥ 6` las tres vueltas no
llegan al elemento retenido.

**Resolución:** la etiqueta del bucle es el JOIN de los dos handles (el
retenido y el de control). Son **21 casos**: 18 de `vector` y 3 de
*unordered* con iterador. Pasan de `UB` a `POLICY`, y la validación dinámica
los corre en `Force` y `Preserve`.

### Contradicción 5 — «insert_middle» inserta en el frente

```python
("insert_middle", "c.insert(c.begin(),1);", "UB", "UB")     # deque
```

- Camino A, por el nombre: inserción en el interior de un `deque` →
  invalida iteradores y referencias ([deque.modifiers]/1) → `UB`.
- Camino B, por la sentencia: `insert(begin(), x)` inserta **en un extremo** →
  invalida iteradores, pero **no** las referencias → `SAFE` para referencias
  y punteros.

El nombre y la sentencia dicen cosas distintas. La validación dinámica no lo
contradice: en las 6 ejecuciones de referencia y puntero fuera del bucle
ningún instrumento detecta nada, y eso es lo que pasa cuando el caso es
seguro. **Resolución:** la sentencia pasa a `c.insert(c.begin() + 1, 1)`,
que sí inserta en el interior. Así el caso mide lo que su nombre dice y su
etiqueta `UB` queda correcta. Con el modelo nuevo esto no puede repetirse:
el punto (`Front`, `Interior`) es un **dato** de la mutación, no parte de un
nombre.

### Contradicción 6 — el iterador de control no cuenta en `unordered` con referencia

La encontró el checker en su primera corrida del banco (`PolicyMode=Possibly`).
En `bucle` hay dos handles: el que declara el caso y el iterador del `for`.
En `f_uset_insert_ref_bucle` (y `ptr`, y `umap::insert`, `umap::subscript`) la
referencia se preserva, pero el iterador de control **depende** del *rehash*.
Por la ley «la etiqueta es el JOIN de sus handles», la etiqueta es
`JOIN(SAFE, POLICY) = POLICY`. El generador dice `SAFE`, porque su regla del
bucle sólo mira la categoría declarada cuando el iterador no es `UB`.

| Casos | Antes | Por la norma | El checker da |
|---:|---|---|---|
| 6 | `SAFE` | `POLICY` | aviso **posible** sobre el iterador del `for` |

**Resolución:** las 6 etiquetas pasan a `POLICY` (D-18). Con las 21 de la
contradicción 4 son las 27 etiquetas corregidas antes de sellar `banco-1`.

## 5. De las leyes al código

| Ley | Prueba | Dónde |
|---|---|---|
| las de la norma | comprobación sobre `matriz.json` al generar la tabla (la generación falla si una no vale) y gtests | `norma/gen_tabla.py` (`check_leyes`), `plugin/tests/dominio/LeyesTest.cpp` (`Norma.*`) |
| las de la detección | una prueba de GoogleTest por ley sobre el núcleo puro | `plugin/tests/dominio/LeyesTest.cpp` (`Deteccion.*`, `Posicion.*`) |
| las de la evaluación | una función por ley, en Python sin dependencias externas | `bench/pruebas_evaluacion.py` |
| las de la validación dinámica | ejecución de cada caso con libstdc++ Debug y ASan | `bench/run_runtime_validation.py` |

La etiqueta tiene **dos implementaciones**: la de referencia en Python
(`bench/etiquetar.py`, que calcula la etiqueta desde la norma) y el núcleo en
C++. El gtest `Banco.ElVeredictoDelNucleoEsLaEtiqueta` las compara celda por
celda sobre las 183 celdas del banco (57 pares × 3 formas de sostener el
handle, más 12 celdas con `reserve`).
