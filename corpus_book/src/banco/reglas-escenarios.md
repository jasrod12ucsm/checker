# Matriz de reglas y escenarios del corpus

## Decisión previa al corpus

El banco se define a partir de reglas de invalidez de la biblioteca estándar de
C++17, antes de generar programas concretos. Cada programa es una instancia
controlada de una regla, no una muestra arbitraria de código. La matriz usa
cuatro dimensiones:

| Dimensión | Valores | Propósito |
|---|---|---|
| Contenedor | 10 tipos STL | Determina la regla de invalidez aplicable. |
| Operación mutadora | 57 pares contenedor--operación | Introduce el posible cambio de estado. |
| Handle retenido | iterador, referencia, puntero | Distingue qué identidad puede invalidarse. |
| Forma sintáctica | recto, guarda, bucle, llamada | Verifica que la regla no dependa solo de una escritura superficial. |

La línea base es C++17: ofrece las familias de contenedores y mutadores
necesarias para estudiar invalidación sin incorporar las operaciones adicionales
de C++20 y C++23, que exigirían reglas y escenarios propios.

## Subconjunto de operaciones modelado

El alcance no es «todas las operaciones de la STL». El corpus actual selecciona
**57 pares contenedor--operación** sobre **10 contenedores**. Una operación se
incluye solo cuando: (1) existe una regla de invalidez que puede expresarse para
el handle retenido, (2) se puede construir un estado inicial válido y (3) se
puede ejecutar y comprobar el escenario resultante. La tabla es, por tanto, el
contrato de cobertura que deberá implementar el checker, no una promesa de
cobertura total de la biblioteca.

| Contenedor | Operaciones seleccionadas | Pares |
|---|---|---:|
| `vector` | `push_back`, `emplace_back`, `insert_begin`, `insert_end`, `erase_begin`, `clear`, `resize_grow`, `reserve`, `shrink_to_fit`, `assign`, `pop_back` | 11 |
| `deque` | `push_back`, `push_front`, `emplace_back`, `insert_middle`, `erase_begin`, `clear`, `resize_grow`, `pop_front` | 8 |
| `list` | `push_back`, `push_front`, `insert`, `erase_begin`, `clear`, `resize_grow`, `pop_front`, `reverse`, `sort` | 9 |
| `forward_list` | `push_front`, `insert_after`, `erase_after`, `clear` | 4 |
| `set` | `insert`, `emplace`, `erase_begin`, `clear` | 4 |
| `multiset` | `insert`, `erase_begin`, `clear` | 3 |
| `map` | `insert`, `emplace`, `subscript`, `erase_begin`, `clear` | 5 |
| `multimap` | `insert`, `erase_begin`, `clear` | 3 |
| `unordered_set` | `insert`, `erase_begin`, `clear`, `rehash`, `reserve` | 5 |
| `unordered_map` | `insert`, `subscript`, `erase_begin`, `clear`, `rehash` | 5 |
| **Total** |  | **57** |

Los nombres `insert_begin`, `insert_end`, `erase_begin` e `insert_middle`
describen una posición de prueba concreta; no son nombres literales de la API.
Esa posición importa porque las reglas de invalidez pueden depender de ella.

### Operaciones excluidas deliberadamente

`std::basic_string`, `std::unordered_multiset`, `swap`, `splice`, `merge` y las
operaciones por rangos de C++23 no forman parte del corpus. También se excluye
`resize` de reducción como caso independiente.
`basic_string` posee una semántica propia de la biblioteca de cadenas;
`unordered_multiset` no aporta una regla de invalidación adicional frente a
`unordered_set` para las operaciones seleccionadas. Las demás operaciones
excluidas pueden depender de dos contenedores, de la identidad del nodo
transferido, de comparadores, asignadores o reglas adicionales que no se han
modelado ni validado en el protocolo actual. Incluirlas sin un escenario y
oráculo específicos convertiría la cobertura en una afirmación no demostrable.

`shrink_to_fit` se conserva como excepción controlada: se etiqueta `POLICY`,
se ejecuta con y sin holgura y su efecto se registra como observado, ya que la
solicitud no es vinculante.

## Unidad de conteo

Un **caso analítico** es una tupla
`(contenedor, operación, handle, forma sintáctica)`. Cuenta una sola vez en el
corpus, incluso cuando se ejecuta en más de una configuración de estado.

| Resultado contado | Unidad | Total |
|---|---:|---:|
| Casos analíticos | Una función del corpus | 750 |
| `UB` normativo | Caso analítico | 342 |
| `SAFE` normativo | Caso analítico | 306 |
| `POLICY` normativo | Caso analítico | 102 |
| Ejecuciones dinámicas | Caso + escenario de estado | 852 |

Los casos `UB` y `SAFE` se ejecutan una vez en su estado ordinario. Cada caso
`POLICY` se ejecuta dos veces: `force`, que satisface la condición de
invalidación, y `preserve`, que satisface la condición de conservación. Por eso
el total dinámico es `342 + 306 + (102 × 2) = 852`. Los conteos de detecciones
de cada instrumento son conteos de **ejecuciones observadas por ese
instrumento**, no una reclasificación de los casos normativos.

## Ejemplos trazables

### Caso válido: `std::list::push_back`

```cpp
std::list<int> c{1, 2, 3};
auto it = c.begin();
c.push_back(4);
sink(*it);                 // SAFE
```

**Regla C++17.** La inserción en `list` no afecta la validez de iteradores ni
referencias a elementos ya existentes (`[list.modifiers]`). Como `it` apunta al
primer elemento, y `push_back` agrega otro elemento, el uso posterior es válido.

**Representación en la matriz.** `list × push_back × iterador × recto` produce
un caso `SAFE`. Sus formas `guarda`, `bucle` y `llamada`, así como los handles
referencia y puntero, son casos distintos porque cambian el recorrido o el
objeto cuya validez se conserva.

### Caso inválido: `std::vector::erase`

```cpp
std::vector<int> c{1, 2, 3};
auto it = c.begin();
c.erase(c.begin());
sink(*it);                 // UB
```

**Regla C++17.** Al borrar un elemento de un `vector`, se invalidan los
iteradores, referencias y punteros situados en el punto de borrado o después de
él (`[vector.modifiers]`). El handle retenido designaba exactamente el elemento
borrado; su desreferenciación posterior es comportamiento indefinido.

**Representación en la matriz.** `vector × erase_begin × iterador × recto` es
un caso `UB`. La misma regla se instancia también para referencia, puntero y
las demás formas sintácticas: son programas diferentes, pero todos conservan la
misma razón semántica de invalidez.

### Caso condicionado por estado: `std::vector::push_back`

`push_back` tiene dos escenarios porque la regla depende de la realocación.

| Escenario | Preparación controlada | Regla aplicada | Etiqueta |
|---|---|---|---|
| `force` | Capacidad agotada antes de insertar | Si hay realocación, se invalidan todos los iteradores, referencias y punteros. | `UB` al usar el handle. |
| `preserve` | `reserve(256)` y pocos elementos | Sin realocación, los handles a elementos anteriores permanecen válidos; solo `end()` cambia. | `SAFE` para el handle a un elemento existente. |

```cpp
// force: size() == capacity()
std::vector<int> c;
c.reserve(8);
while (c.size() < c.capacity()) c.push_back(int(c.size()));
auto it = c.begin();
c.push_back(4);             // fuerza realocación
sink(*it);                  // UB

// preserve: hay capacidad disponible
std::vector<int> d;
d.reserve(256);
d.push_back(1); d.push_back(2); d.push_back(3);
auto jt = d.begin();
d.push_back(4);             // no realoca
sink(*jt);                  // SAFE
```

**Regla C++17.** La diferencia no es el texto de `push_back`, sino el estado de
capacidad que determina si ocurre realocación (`[vector.modifiers]`). Por eso
la etiqueta base es `POLICY`: no se puede asignar `SAFE` o `UB` sin declarar el
estado de ejecución.

### Caso condicionado por estado: `std::unordered_set::insert`

```cpp
// force: se alcanza el umbral de carga y la inserción hace rehash
std::unordered_set<int> c;
c.max_load_factor(1.0f);
c.rehash(8);
for (std::size_t i = 0; i < c.bucket_count(); ++i) c.insert(int(i));
auto it = c.begin();
c.insert(99);               // rehash
sink(*it);                  // UB: iterador invalidado

// preserve: el umbral no se alcanza
std::unordered_set<int> d;
d.reserve(256);
d.insert(1); d.insert(2); d.insert(3);
auto jt = d.begin();
d.insert(99);               // sin rehash
sink(*jt);                  // SAFE
```

**Regla C++17.** La inserción puede invalidar iteradores si provoca `rehash`;
las referencias y punteros a elementos no se invalidan por ese `rehash`
(`[unord.req]`). Por ello la matriz distingue `iterador` (`POLICY`) de
`referencia` y `puntero` (`SAFE`) para esta operación.

## Demostración de relevancia de cada programa

Cada entrada de `test/corpus_truth.json` conserva el contenedor, la operación,
el handle, la forma y la etiqueta normativa. El generador
`bench/gen_corpus.py` produce el programa a partir de esa tupla y de la tabla
de reglas; por tanto, se puede rastrear cualquier función del corpus hasta una
regla concreta de invalidez.

La demostración se cierra con la ejecución dinámica descrita en
[Validación dinámica del corpus](protocolo-dinamico.md): el harness ejecuta
cada caso de manera aislada y ejecuta ambos escenarios de cada `POLICY`. El
archivo `runtime_validation_results.json` registra, por ejecución, la
precondición aplicada en `escenario`, la etiqueta normativa y la observación de
libstdc++ Debug Mode y ASan/UBSan.

Esta evidencia demuestra que los escenarios se prepararon y ejecutaron; no
convierte la ausencia de un fallo visible en prueba de seguridad. La validez de
la etiqueta continúa dada por la regla C++17, mientras que la ejecución
instrumentada corrobora que el programa representa el escenario declarado.
