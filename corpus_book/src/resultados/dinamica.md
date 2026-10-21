
# Validación dinámica


Validación dinámica reproducible por escenarios; no sustituye el oráculo normativo.

- Casos base: **750**; ejecuciones: **852**
  (una por caso `UB`/`SAFE`, dos por caso `POLICY`).
- Timeout por ejecución: 2 s.
- Cobertura del protocolo: `COMPLETA`.

## Resumen por instrumento

| Instrumento | Detectado | Sin detección |
|---|---:|---:|
| libstdc++ Debug | 228 | 624 |
| ASan/UBSan | 282 | 570 |

## Por etiqueta normativa y escenario

| Etiqueta (modo) | Ejecuciones | libstdc++ Debug | ASan/UBSan | Alguno | Ninguno |
|---|---:|---:|---:|---:|---:|
| `UB` (natural) | 342 | 174 | 207 | 276 | 66 |
| `SAFE` (natural) | 306 | 0 | 0 | 0 | 306 |
| `POLICY` (force) | 102 | 54 | 75 | 90 | 12 |
| `POLICY` (preserve) | 102 | 0 | 0 | 0 | 102 |

Casos `SAFE` con alguna detección dinámica: **0**.

## Tipo de error observado

| Instrumento | Diagnóstico | Ejecuciones |
|---|---|---:|
| ASan/UBSan | `heap-buffer-overflow` | 3 |
| ASan/UBSan | `heap-use-after-free` | 279 |
| libstdc++ Debug | `attempt to dereference a singular iterator` | 152 |
| libstdc++ Debug | `attempt to increment a singular iterator` | 76 |

## Por contenedor (todas las ejecuciones)

| Contenedor | Ejecuciones | libstdc++ Debug | ASan/UBSan | Alguno | Ninguno |
|---|---:|---:|---:|---:|---:|
| `std::vector` | 254 | 66 | 78 | 102 | 152 |
| `std::deque` | 98 | 48 | 0 | 48 | 50 |
| `std::list` | 110 | 18 | 36 | 36 | 74 |
| `std::forward_list` | 48 | 12 | 24 | 24 | 24 |
| `std::set` | 49 | 12 | 24 | 24 | 25 |
| `std::multiset` | 37 | 12 | 24 | 24 | 13 |
| `std::map` | 61 | 12 | 24 | 24 | 37 |
| `std::multimap` | 37 | 12 | 24 | 24 | 13 |
| `std::unordered_set` | 73 | 18 | 24 | 30 | 43 |
| `std::unordered_map` | 85 | 18 | 24 | 30 | 55 |

## Casos `UB` por forma

| Forma | Ejecuciones | libstdc++ Debug | ASan/UBSan | Alguno | Ninguno |
|---|---:|---:|---:|---:|---:|
| `recto` | 82 | 29 | 51 | 63 | 19 |
| `guarda` | 82 | 29 | 51 | 63 | 19 |
| `bucle` | 96 | 87 | 54 | 87 | 9 |
| `llamada` | 82 | 29 | 51 | 63 | 19 |

## Casos `UB` por handle

| Sostiene | Ejecuciones | libstdc++ Debug | ASan/UBSan | Alguno | Ninguno |
|---|---:|---:|---:|---:|---:|
| `it` | 128 | 116 | 69 | 116 | 12 |
| `ref` | 107 | 29 | 69 | 80 | 27 |
| `ptr` | 107 | 29 | 69 | 80 | 27 |


## ¿Coincide con el estándar?

Las etiquetas salen del estándar C++17; la ejecución es una segunda opinión.
Las preguntas son dos: si la ejecución **contradice** alguna etiqueta y si
**confirma** las de bug.

### ¿Contradice alguna etiqueta?

Habría contradicción si un caso que llamamos seguro (`SAFE`, o `POLICY` en el
escenario `preserve`) mostrara un bug al ejecutarse.

| Grupo | Ejecuciones | Con detección |
|---|---:|---:|
| 🟢 `SAFE` | 306 | **0** |
| 🟡 `POLICY` · `preserve` (no debería romperse) | 102 | **0** |

**Contradicciones: 0.** Ningún caso que el estándar considera seguro falló al ejecutarse.

### ¿Confirma los bugs?

| Grupo | Ejecuciones | Detectados | Sin detección |
|---|---:|---:|---:|
| 🔴 `UB` | 342 | 276 | 66 |
| 🟡 `POLICY` · `force` (debería romperse) | 102 | 90 | 12 |

Los casos sin detección **no** contradicen al estándar. Que un bug no se
manifieste está permitido: es la definición de comportamiento indefinido. Lo que
muestran son los **límites de las herramientas** (ver
[Las herramientas de ejecución](../herramientas.md#por-qué-se-usan-las-dos)):

- **Referencias y punteros sin memoria liberada.** Por ejemplo, `vector::erase`,
  `vector::clear` o `deque::pop_front`: el estándar invalida la referencia, pero
  el contenedor conserva la memoria. Debug Mode no sigue referencias y ASan no ve
  memoria liberada, así que nadie lo nota.
- **Iteradores que Debug Mode no marca y cuya memoria no se libera.** Por
  ejemplo, `rehash`/`reserve` en contenedores `unordered`: el estándar invalida
  los iteradores, pero los nodos siguen en su sitio.

<details>
<summary>Casos UB sin detección dinámica, agrupados (66)</summary>

| Contenedor | Operación | Sostiene | Casos |
|---|---|---|---|
| `std::vector` | [`insert_begin`](../casos/vector/insert_begin.md) | referencia | 3 |
| `std::vector` | [`insert_begin`](../casos/vector/insert_begin.md) | puntero | 3 |
| `std::vector` | [`erase_begin`](../casos/vector/erase_begin.md) | referencia | 3 |
| `std::vector` | [`erase_begin`](../casos/vector/erase_begin.md) | puntero | 3 |
| `std::vector` | [`clear`](../casos/vector/clear.md) | referencia | 3 |
| `std::vector` | [`clear`](../casos/vector/clear.md) | puntero | 3 |
| `std::vector` | [`assign`](../casos/vector/assign.md) | referencia | 3 |
| `std::vector` | [`assign`](../casos/vector/assign.md) | puntero | 3 |
| `std::deque` | [`insert_middle`](../casos/deque/insert_middle.md) | referencia | 3 |
| `std::deque` | [`insert_middle`](../casos/deque/insert_middle.md) | puntero | 3 |
| `std::deque` | [`erase_begin`](../casos/deque/erase_begin.md) | referencia | 3 |
| `std::deque` | [`erase_begin`](../casos/deque/erase_begin.md) | puntero | 3 |
| `std::deque` | [`clear`](../casos/deque/clear.md) | referencia | 3 |
| `std::deque` | [`clear`](../casos/deque/clear.md) | puntero | 3 |
| `std::deque` | [`pop_front`](../casos/deque/pop_front.md) | referencia | 3 |
| `std::deque` | [`pop_front`](../casos/deque/pop_front.md) | puntero | 3 |
| `std::unordered_set` | [`rehash`](../casos/uset/rehash.md) | iterador | 4 |
| `std::unordered_set` | [`rehash`](../casos/uset/rehash.md) | referencia | 1 |
| `std::unordered_set` | [`rehash`](../casos/uset/rehash.md) | puntero | 1 |
| `std::unordered_set` | [`reserve`](../casos/uset/reserve.md) | iterador | 4 |
| `std::unordered_set` | [`reserve`](../casos/uset/reserve.md) | referencia | 1 |
| `std::unordered_set` | [`reserve`](../casos/uset/reserve.md) | puntero | 1 |
| `std::unordered_map` | [`rehash`](../casos/umap/rehash.md) | iterador | 4 |
| `std::unordered_map` | [`rehash`](../casos/umap/rehash.md) | referencia | 1 |
| `std::unordered_map` | [`rehash`](../casos/umap/rehash.md) | puntero | 1 |

</details>

<details>
<summary>Casos POLICY · force sin detección, agrupados (12)</summary>

| Contenedor | Operación | Sostiene | Casos |
|---|---|---|---|
| `std::vector` | [`pop_back`](../casos/vector/pop_back.md) | referencia | 3 |
| `std::vector` | [`pop_back`](../casos/vector/pop_back.md) | puntero | 3 |
| `std::unordered_map` | [`subscript`](../casos/umap/subscript.md) | iterador | 4 |
| `std::unordered_map` | [`subscript`](../casos/umap/subscript.md) | referencia | 1 |
| `std::unordered_map` | [`subscript`](../casos/umap/subscript.md) | puntero | 1 |

</details>

**Conclusión:** la ejecución no contradice ninguna etiqueta. Confirma
276 de 342 casos `UB`, y los no confirmados
corresponden a límites conocidos de las herramientas, no a errores del corpus.


## Cruce estático × dinámico (casos `UB`)

| | Dinámica detecta | Dinámica no detecta |
|---|---:|---:|
| **Estático avisa** | 80 | 0 |
| **Estático calla** | 196 | 66 |

Los 196 casos de la celda *estático calla / dinámica detecta* son
evidencia de que el defecto es real y observable, pero invisible para el
analizador estático.

<details>
<summary>Casos UB detectados solo dinámicamente (196)</summary>

- [`f_vector_insert_begin_it_recto`](../casos/vector/insert_begin.md#f_vector_insert_begin_it_recto)
- [`f_vector_insert_begin_it_guarda`](../casos/vector/insert_begin.md#f_vector_insert_begin_it_guarda)
- [`f_vector_insert_begin_it_bucle`](../casos/vector/insert_begin.md#f_vector_insert_begin_it_bucle)
- [`f_vector_insert_begin_it_llamada`](../casos/vector/insert_begin.md#f_vector_insert_begin_it_llamada)
- [`f_vector_insert_begin_ref_bucle`](../casos/vector/insert_begin.md#f_vector_insert_begin_ref_bucle)
- [`f_vector_insert_begin_ptr_bucle`](../casos/vector/insert_begin.md#f_vector_insert_begin_ptr_bucle)
- [`f_vector_erase_begin_it_recto`](../casos/vector/erase_begin.md#f_vector_erase_begin_it_recto)
- [`f_vector_erase_begin_it_guarda`](../casos/vector/erase_begin.md#f_vector_erase_begin_it_guarda)
- [`f_vector_erase_begin_it_bucle`](../casos/vector/erase_begin.md#f_vector_erase_begin_it_bucle)
- [`f_vector_erase_begin_it_llamada`](../casos/vector/erase_begin.md#f_vector_erase_begin_it_llamada)
- [`f_vector_erase_begin_ref_bucle`](../casos/vector/erase_begin.md#f_vector_erase_begin_ref_bucle)
- [`f_vector_erase_begin_ptr_bucle`](../casos/vector/erase_begin.md#f_vector_erase_begin_ptr_bucle)
- [`f_vector_clear_it_recto`](../casos/vector/clear.md#f_vector_clear_it_recto)
- [`f_vector_assign_it_recto`](../casos/vector/assign.md#f_vector_assign_it_recto)
- [`f_deque_push_back_it_recto`](../casos/deque/push_back.md#f_deque_push_back_it_recto)
- [`f_deque_push_front_it_recto`](../casos/deque/push_front.md#f_deque_push_front_it_recto)
- [`f_deque_emplace_back_it_recto`](../casos/deque/emplace_back.md#f_deque_emplace_back_it_recto)
- [`f_deque_insert_middle_it_recto`](../casos/deque/insert_middle.md#f_deque_insert_middle_it_recto)
- [`f_deque_erase_begin_it_recto`](../casos/deque/erase_begin.md#f_deque_erase_begin_it_recto)
- [`f_deque_clear_it_recto`](../casos/deque/clear.md#f_deque_clear_it_recto)
- [`f_deque_resize_grow_it_recto`](../casos/deque/resize_grow.md#f_deque_resize_grow_it_recto)
- [`f_deque_resize_grow_it_guarda`](../casos/deque/resize_grow.md#f_deque_resize_grow_it_guarda)
- [`f_deque_resize_grow_it_bucle`](../casos/deque/resize_grow.md#f_deque_resize_grow_it_bucle)
- [`f_deque_resize_grow_it_llamada`](../casos/deque/resize_grow.md#f_deque_resize_grow_it_llamada)
- [`f_deque_resize_grow_ref_bucle`](../casos/deque/resize_grow.md#f_deque_resize_grow_ref_bucle)
- [`f_deque_resize_grow_ptr_bucle`](../casos/deque/resize_grow.md#f_deque_resize_grow_ptr_bucle)
- [`f_deque_pop_front_it_recto`](../casos/deque/pop_front.md#f_deque_pop_front_it_recto)
- [`f_deque_pop_front_it_guarda`](../casos/deque/pop_front.md#f_deque_pop_front_it_guarda)
- [`f_deque_pop_front_it_bucle`](../casos/deque/pop_front.md#f_deque_pop_front_it_bucle)
- [`f_deque_pop_front_it_llamada`](../casos/deque/pop_front.md#f_deque_pop_front_it_llamada)
- [`f_deque_pop_front_ref_bucle`](../casos/deque/pop_front.md#f_deque_pop_front_ref_bucle)
- [`f_deque_pop_front_ptr_bucle`](../casos/deque/pop_front.md#f_deque_pop_front_ptr_bucle)
- [`f_list_erase_begin_it_recto`](../casos/list/erase_begin.md#f_list_erase_begin_it_recto)
- [`f_list_erase_begin_it_guarda`](../casos/list/erase_begin.md#f_list_erase_begin_it_guarda)
- [`f_list_erase_begin_it_bucle`](../casos/list/erase_begin.md#f_list_erase_begin_it_bucle)
- [`f_list_erase_begin_it_llamada`](../casos/list/erase_begin.md#f_list_erase_begin_it_llamada)
- [`f_list_erase_begin_ref_recto`](../casos/list/erase_begin.md#f_list_erase_begin_ref_recto)
- [`f_list_erase_begin_ref_guarda`](../casos/list/erase_begin.md#f_list_erase_begin_ref_guarda)
- [`f_list_erase_begin_ref_bucle`](../casos/list/erase_begin.md#f_list_erase_begin_ref_bucle)
- [`f_list_erase_begin_ref_llamada`](../casos/list/erase_begin.md#f_list_erase_begin_ref_llamada)
- [`f_list_erase_begin_ptr_recto`](../casos/list/erase_begin.md#f_list_erase_begin_ptr_recto)
- [`f_list_erase_begin_ptr_guarda`](../casos/list/erase_begin.md#f_list_erase_begin_ptr_guarda)
- [`f_list_erase_begin_ptr_bucle`](../casos/list/erase_begin.md#f_list_erase_begin_ptr_bucle)
- [`f_list_erase_begin_ptr_llamada`](../casos/list/erase_begin.md#f_list_erase_begin_ptr_llamada)
- [`f_list_clear_it_recto`](../casos/list/clear.md#f_list_clear_it_recto)
- [`f_list_clear_ref_recto`](../casos/list/clear.md#f_list_clear_ref_recto)
- [`f_list_clear_ref_guarda`](../casos/list/clear.md#f_list_clear_ref_guarda)
- [`f_list_clear_ref_llamada`](../casos/list/clear.md#f_list_clear_ref_llamada)
- [`f_list_clear_ptr_recto`](../casos/list/clear.md#f_list_clear_ptr_recto)
- [`f_list_clear_ptr_guarda`](../casos/list/clear.md#f_list_clear_ptr_guarda)
- [`f_list_clear_ptr_llamada`](../casos/list/clear.md#f_list_clear_ptr_llamada)
- [`f_list_pop_front_it_recto`](../casos/list/pop_front.md#f_list_pop_front_it_recto)
- [`f_list_pop_front_it_guarda`](../casos/list/pop_front.md#f_list_pop_front_it_guarda)
- [`f_list_pop_front_it_bucle`](../casos/list/pop_front.md#f_list_pop_front_it_bucle)
- [`f_list_pop_front_it_llamada`](../casos/list/pop_front.md#f_list_pop_front_it_llamada)
- [`f_list_pop_front_ref_recto`](../casos/list/pop_front.md#f_list_pop_front_ref_recto)
- [`f_list_pop_front_ref_guarda`](../casos/list/pop_front.md#f_list_pop_front_ref_guarda)
- [`f_list_pop_front_ref_bucle`](../casos/list/pop_front.md#f_list_pop_front_ref_bucle)
- [`f_list_pop_front_ref_llamada`](../casos/list/pop_front.md#f_list_pop_front_ref_llamada)
- [`f_list_pop_front_ptr_recto`](../casos/list/pop_front.md#f_list_pop_front_ptr_recto)
- [`f_list_pop_front_ptr_guarda`](../casos/list/pop_front.md#f_list_pop_front_ptr_guarda)
- [`f_list_pop_front_ptr_bucle`](../casos/list/pop_front.md#f_list_pop_front_ptr_bucle)
- [`f_list_pop_front_ptr_llamada`](../casos/list/pop_front.md#f_list_pop_front_ptr_llamada)
- [`f_flist_erase_after_it_recto`](../casos/flist/erase_after.md#f_flist_erase_after_it_recto)
- [`f_flist_erase_after_it_guarda`](../casos/flist/erase_after.md#f_flist_erase_after_it_guarda)
- [`f_flist_erase_after_it_bucle`](../casos/flist/erase_after.md#f_flist_erase_after_it_bucle)
- [`f_flist_erase_after_it_llamada`](../casos/flist/erase_after.md#f_flist_erase_after_it_llamada)
- [`f_flist_erase_after_ref_recto`](../casos/flist/erase_after.md#f_flist_erase_after_ref_recto)
- [`f_flist_erase_after_ref_guarda`](../casos/flist/erase_after.md#f_flist_erase_after_ref_guarda)
- [`f_flist_erase_after_ref_bucle`](../casos/flist/erase_after.md#f_flist_erase_after_ref_bucle)
- [`f_flist_erase_after_ref_llamada`](../casos/flist/erase_after.md#f_flist_erase_after_ref_llamada)
- [`f_flist_erase_after_ptr_recto`](../casos/flist/erase_after.md#f_flist_erase_after_ptr_recto)
- [`f_flist_erase_after_ptr_guarda`](../casos/flist/erase_after.md#f_flist_erase_after_ptr_guarda)
- [`f_flist_erase_after_ptr_bucle`](../casos/flist/erase_after.md#f_flist_erase_after_ptr_bucle)
- [`f_flist_erase_after_ptr_llamada`](../casos/flist/erase_after.md#f_flist_erase_after_ptr_llamada)
- [`f_flist_clear_it_recto`](../casos/flist/clear.md#f_flist_clear_it_recto)
- [`f_flist_clear_ref_recto`](../casos/flist/clear.md#f_flist_clear_ref_recto)
- [`f_flist_clear_ref_guarda`](../casos/flist/clear.md#f_flist_clear_ref_guarda)
- [`f_flist_clear_ref_llamada`](../casos/flist/clear.md#f_flist_clear_ref_llamada)
- [`f_flist_clear_ptr_recto`](../casos/flist/clear.md#f_flist_clear_ptr_recto)
- [`f_flist_clear_ptr_guarda`](../casos/flist/clear.md#f_flist_clear_ptr_guarda)
- [`f_flist_clear_ptr_llamada`](../casos/flist/clear.md#f_flist_clear_ptr_llamada)
- [`f_set_erase_begin_it_recto`](../casos/set/erase_begin.md#f_set_erase_begin_it_recto)
- [`f_set_erase_begin_it_guarda`](../casos/set/erase_begin.md#f_set_erase_begin_it_guarda)
- [`f_set_erase_begin_it_bucle`](../casos/set/erase_begin.md#f_set_erase_begin_it_bucle)
- [`f_set_erase_begin_it_llamada`](../casos/set/erase_begin.md#f_set_erase_begin_it_llamada)
- [`f_set_erase_begin_ref_recto`](../casos/set/erase_begin.md#f_set_erase_begin_ref_recto)
- [`f_set_erase_begin_ref_guarda`](../casos/set/erase_begin.md#f_set_erase_begin_ref_guarda)
- [`f_set_erase_begin_ref_bucle`](../casos/set/erase_begin.md#f_set_erase_begin_ref_bucle)
- [`f_set_erase_begin_ref_llamada`](../casos/set/erase_begin.md#f_set_erase_begin_ref_llamada)
- [`f_set_erase_begin_ptr_recto`](../casos/set/erase_begin.md#f_set_erase_begin_ptr_recto)
- [`f_set_erase_begin_ptr_guarda`](../casos/set/erase_begin.md#f_set_erase_begin_ptr_guarda)
- [`f_set_erase_begin_ptr_bucle`](../casos/set/erase_begin.md#f_set_erase_begin_ptr_bucle)
- [`f_set_erase_begin_ptr_llamada`](../casos/set/erase_begin.md#f_set_erase_begin_ptr_llamada)
- [`f_set_clear_it_recto`](../casos/set/clear.md#f_set_clear_it_recto)
- [`f_set_clear_ref_recto`](../casos/set/clear.md#f_set_clear_ref_recto)
- [`f_set_clear_ref_guarda`](../casos/set/clear.md#f_set_clear_ref_guarda)
- [`f_set_clear_ref_llamada`](../casos/set/clear.md#f_set_clear_ref_llamada)
- [`f_set_clear_ptr_recto`](../casos/set/clear.md#f_set_clear_ptr_recto)
- [`f_set_clear_ptr_guarda`](../casos/set/clear.md#f_set_clear_ptr_guarda)
- [`f_set_clear_ptr_llamada`](../casos/set/clear.md#f_set_clear_ptr_llamada)
- [`f_mset_erase_begin_it_recto`](../casos/mset/erase_begin.md#f_mset_erase_begin_it_recto)
- [`f_mset_erase_begin_it_guarda`](../casos/mset/erase_begin.md#f_mset_erase_begin_it_guarda)
- [`f_mset_erase_begin_it_bucle`](../casos/mset/erase_begin.md#f_mset_erase_begin_it_bucle)
- [`f_mset_erase_begin_it_llamada`](../casos/mset/erase_begin.md#f_mset_erase_begin_it_llamada)
- [`f_mset_erase_begin_ref_recto`](../casos/mset/erase_begin.md#f_mset_erase_begin_ref_recto)
- [`f_mset_erase_begin_ref_guarda`](../casos/mset/erase_begin.md#f_mset_erase_begin_ref_guarda)
- [`f_mset_erase_begin_ref_bucle`](../casos/mset/erase_begin.md#f_mset_erase_begin_ref_bucle)
- [`f_mset_erase_begin_ref_llamada`](../casos/mset/erase_begin.md#f_mset_erase_begin_ref_llamada)
- [`f_mset_erase_begin_ptr_recto`](../casos/mset/erase_begin.md#f_mset_erase_begin_ptr_recto)
- [`f_mset_erase_begin_ptr_guarda`](../casos/mset/erase_begin.md#f_mset_erase_begin_ptr_guarda)
- [`f_mset_erase_begin_ptr_bucle`](../casos/mset/erase_begin.md#f_mset_erase_begin_ptr_bucle)
- [`f_mset_erase_begin_ptr_llamada`](../casos/mset/erase_begin.md#f_mset_erase_begin_ptr_llamada)
- [`f_mset_clear_it_recto`](../casos/mset/clear.md#f_mset_clear_it_recto)
- [`f_mset_clear_ref_recto`](../casos/mset/clear.md#f_mset_clear_ref_recto)
- [`f_mset_clear_ref_guarda`](../casos/mset/clear.md#f_mset_clear_ref_guarda)
- [`f_mset_clear_ref_llamada`](../casos/mset/clear.md#f_mset_clear_ref_llamada)
- [`f_mset_clear_ptr_recto`](../casos/mset/clear.md#f_mset_clear_ptr_recto)
- [`f_mset_clear_ptr_guarda`](../casos/mset/clear.md#f_mset_clear_ptr_guarda)
- [`f_mset_clear_ptr_llamada`](../casos/mset/clear.md#f_mset_clear_ptr_llamada)
- [`f_map_erase_begin_it_recto`](../casos/map/erase_begin.md#f_map_erase_begin_it_recto)
- [`f_map_erase_begin_it_guarda`](../casos/map/erase_begin.md#f_map_erase_begin_it_guarda)
- [`f_map_erase_begin_it_bucle`](../casos/map/erase_begin.md#f_map_erase_begin_it_bucle)
- [`f_map_erase_begin_it_llamada`](../casos/map/erase_begin.md#f_map_erase_begin_it_llamada)
- [`f_map_erase_begin_ref_recto`](../casos/map/erase_begin.md#f_map_erase_begin_ref_recto)
- [`f_map_erase_begin_ref_guarda`](../casos/map/erase_begin.md#f_map_erase_begin_ref_guarda)
- [`f_map_erase_begin_ref_bucle`](../casos/map/erase_begin.md#f_map_erase_begin_ref_bucle)
- [`f_map_erase_begin_ref_llamada`](../casos/map/erase_begin.md#f_map_erase_begin_ref_llamada)
- [`f_map_erase_begin_ptr_recto`](../casos/map/erase_begin.md#f_map_erase_begin_ptr_recto)
- [`f_map_erase_begin_ptr_guarda`](../casos/map/erase_begin.md#f_map_erase_begin_ptr_guarda)
- [`f_map_erase_begin_ptr_bucle`](../casos/map/erase_begin.md#f_map_erase_begin_ptr_bucle)
- [`f_map_erase_begin_ptr_llamada`](../casos/map/erase_begin.md#f_map_erase_begin_ptr_llamada)
- [`f_map_clear_it_recto`](../casos/map/clear.md#f_map_clear_it_recto)
- [`f_map_clear_ref_recto`](../casos/map/clear.md#f_map_clear_ref_recto)
- [`f_map_clear_ref_guarda`](../casos/map/clear.md#f_map_clear_ref_guarda)
- [`f_map_clear_ref_llamada`](../casos/map/clear.md#f_map_clear_ref_llamada)
- [`f_map_clear_ptr_recto`](../casos/map/clear.md#f_map_clear_ptr_recto)
- [`f_map_clear_ptr_guarda`](../casos/map/clear.md#f_map_clear_ptr_guarda)
- [`f_map_clear_ptr_llamada`](../casos/map/clear.md#f_map_clear_ptr_llamada)
- [`f_mmap_erase_begin_it_recto`](../casos/mmap/erase_begin.md#f_mmap_erase_begin_it_recto)
- [`f_mmap_erase_begin_it_guarda`](../casos/mmap/erase_begin.md#f_mmap_erase_begin_it_guarda)
- [`f_mmap_erase_begin_it_bucle`](../casos/mmap/erase_begin.md#f_mmap_erase_begin_it_bucle)
- [`f_mmap_erase_begin_it_llamada`](../casos/mmap/erase_begin.md#f_mmap_erase_begin_it_llamada)
- [`f_mmap_erase_begin_ref_recto`](../casos/mmap/erase_begin.md#f_mmap_erase_begin_ref_recto)
- [`f_mmap_erase_begin_ref_guarda`](../casos/mmap/erase_begin.md#f_mmap_erase_begin_ref_guarda)
- [`f_mmap_erase_begin_ref_bucle`](../casos/mmap/erase_begin.md#f_mmap_erase_begin_ref_bucle)
- [`f_mmap_erase_begin_ref_llamada`](../casos/mmap/erase_begin.md#f_mmap_erase_begin_ref_llamada)
- [`f_mmap_erase_begin_ptr_recto`](../casos/mmap/erase_begin.md#f_mmap_erase_begin_ptr_recto)
- [`f_mmap_erase_begin_ptr_guarda`](../casos/mmap/erase_begin.md#f_mmap_erase_begin_ptr_guarda)
- [`f_mmap_erase_begin_ptr_bucle`](../casos/mmap/erase_begin.md#f_mmap_erase_begin_ptr_bucle)
- [`f_mmap_erase_begin_ptr_llamada`](../casos/mmap/erase_begin.md#f_mmap_erase_begin_ptr_llamada)
- [`f_mmap_clear_it_recto`](../casos/mmap/clear.md#f_mmap_clear_it_recto)
- [`f_mmap_clear_ref_recto`](../casos/mmap/clear.md#f_mmap_clear_ref_recto)
- [`f_mmap_clear_ref_guarda`](../casos/mmap/clear.md#f_mmap_clear_ref_guarda)
- [`f_mmap_clear_ref_llamada`](../casos/mmap/clear.md#f_mmap_clear_ref_llamada)
- [`f_mmap_clear_ptr_recto`](../casos/mmap/clear.md#f_mmap_clear_ptr_recto)
- [`f_mmap_clear_ptr_guarda`](../casos/mmap/clear.md#f_mmap_clear_ptr_guarda)
- [`f_mmap_clear_ptr_llamada`](../casos/mmap/clear.md#f_mmap_clear_ptr_llamada)
- [`f_uset_erase_begin_it_recto`](../casos/uset/erase_begin.md#f_uset_erase_begin_it_recto)
- [`f_uset_erase_begin_it_guarda`](../casos/uset/erase_begin.md#f_uset_erase_begin_it_guarda)
- [`f_uset_erase_begin_it_bucle`](../casos/uset/erase_begin.md#f_uset_erase_begin_it_bucle)
- [`f_uset_erase_begin_it_llamada`](../casos/uset/erase_begin.md#f_uset_erase_begin_it_llamada)
- [`f_uset_erase_begin_ref_recto`](../casos/uset/erase_begin.md#f_uset_erase_begin_ref_recto)
- [`f_uset_erase_begin_ref_guarda`](../casos/uset/erase_begin.md#f_uset_erase_begin_ref_guarda)
- [`f_uset_erase_begin_ref_bucle`](../casos/uset/erase_begin.md#f_uset_erase_begin_ref_bucle)
- [`f_uset_erase_begin_ref_llamada`](../casos/uset/erase_begin.md#f_uset_erase_begin_ref_llamada)
- [`f_uset_erase_begin_ptr_recto`](../casos/uset/erase_begin.md#f_uset_erase_begin_ptr_recto)
- [`f_uset_erase_begin_ptr_guarda`](../casos/uset/erase_begin.md#f_uset_erase_begin_ptr_guarda)
- [`f_uset_erase_begin_ptr_bucle`](../casos/uset/erase_begin.md#f_uset_erase_begin_ptr_bucle)
- [`f_uset_erase_begin_ptr_llamada`](../casos/uset/erase_begin.md#f_uset_erase_begin_ptr_llamada)
- [`f_uset_clear_it_recto`](../casos/uset/clear.md#f_uset_clear_it_recto)
- [`f_uset_clear_ref_recto`](../casos/uset/clear.md#f_uset_clear_ref_recto)
- [`f_uset_clear_ref_guarda`](../casos/uset/clear.md#f_uset_clear_ref_guarda)
- [`f_uset_clear_ref_llamada`](../casos/uset/clear.md#f_uset_clear_ref_llamada)
- [`f_uset_clear_ptr_recto`](../casos/uset/clear.md#f_uset_clear_ptr_recto)
- [`f_uset_clear_ptr_guarda`](../casos/uset/clear.md#f_uset_clear_ptr_guarda)
- [`f_uset_clear_ptr_llamada`](../casos/uset/clear.md#f_uset_clear_ptr_llamada)
- [`f_umap_erase_begin_it_recto`](../casos/umap/erase_begin.md#f_umap_erase_begin_it_recto)
- [`f_umap_erase_begin_it_guarda`](../casos/umap/erase_begin.md#f_umap_erase_begin_it_guarda)
- [`f_umap_erase_begin_it_bucle`](../casos/umap/erase_begin.md#f_umap_erase_begin_it_bucle)
- [`f_umap_erase_begin_it_llamada`](../casos/umap/erase_begin.md#f_umap_erase_begin_it_llamada)
- [`f_umap_erase_begin_ref_recto`](../casos/umap/erase_begin.md#f_umap_erase_begin_ref_recto)
- [`f_umap_erase_begin_ref_guarda`](../casos/umap/erase_begin.md#f_umap_erase_begin_ref_guarda)
- [`f_umap_erase_begin_ref_bucle`](../casos/umap/erase_begin.md#f_umap_erase_begin_ref_bucle)
- [`f_umap_erase_begin_ref_llamada`](../casos/umap/erase_begin.md#f_umap_erase_begin_ref_llamada)
- [`f_umap_erase_begin_ptr_recto`](../casos/umap/erase_begin.md#f_umap_erase_begin_ptr_recto)
- [`f_umap_erase_begin_ptr_guarda`](../casos/umap/erase_begin.md#f_umap_erase_begin_ptr_guarda)
- [`f_umap_erase_begin_ptr_bucle`](../casos/umap/erase_begin.md#f_umap_erase_begin_ptr_bucle)
- [`f_umap_erase_begin_ptr_llamada`](../casos/umap/erase_begin.md#f_umap_erase_begin_ptr_llamada)
- [`f_umap_clear_it_recto`](../casos/umap/clear.md#f_umap_clear_it_recto)
- [`f_umap_clear_ref_recto`](../casos/umap/clear.md#f_umap_clear_ref_recto)
- [`f_umap_clear_ref_guarda`](../casos/umap/clear.md#f_umap_clear_ref_guarda)
- [`f_umap_clear_ref_llamada`](../casos/umap/clear.md#f_umap_clear_ref_llamada)
- [`f_umap_clear_ptr_recto`](../casos/umap/clear.md#f_umap_clear_ptr_recto)
- [`f_umap_clear_ptr_guarda`](../casos/umap/clear.md#f_umap_clear_ptr_guarda)
- [`f_umap_clear_ptr_llamada`](../casos/umap/clear.md#f_umap_clear_ptr_llamada)

</details>

<details>
<summary>Casos UB sin manifestación dinámica en ningún instrumento (66)</summary>

Siguen siendo `UB` por su regla normativa: la implementación no está obligada a
manifestar el defecto.

- [`f_vector_insert_begin_ref_recto`](../casos/vector/insert_begin.md#f_vector_insert_begin_ref_recto)
- [`f_vector_insert_begin_ref_guarda`](../casos/vector/insert_begin.md#f_vector_insert_begin_ref_guarda)
- [`f_vector_insert_begin_ref_llamada`](../casos/vector/insert_begin.md#f_vector_insert_begin_ref_llamada)
- [`f_vector_insert_begin_ptr_recto`](../casos/vector/insert_begin.md#f_vector_insert_begin_ptr_recto)
- [`f_vector_insert_begin_ptr_guarda`](../casos/vector/insert_begin.md#f_vector_insert_begin_ptr_guarda)
- [`f_vector_insert_begin_ptr_llamada`](../casos/vector/insert_begin.md#f_vector_insert_begin_ptr_llamada)
- [`f_vector_erase_begin_ref_recto`](../casos/vector/erase_begin.md#f_vector_erase_begin_ref_recto)
- [`f_vector_erase_begin_ref_guarda`](../casos/vector/erase_begin.md#f_vector_erase_begin_ref_guarda)
- [`f_vector_erase_begin_ref_llamada`](../casos/vector/erase_begin.md#f_vector_erase_begin_ref_llamada)
- [`f_vector_erase_begin_ptr_recto`](../casos/vector/erase_begin.md#f_vector_erase_begin_ptr_recto)
- [`f_vector_erase_begin_ptr_guarda`](../casos/vector/erase_begin.md#f_vector_erase_begin_ptr_guarda)
- [`f_vector_erase_begin_ptr_llamada`](../casos/vector/erase_begin.md#f_vector_erase_begin_ptr_llamada)
- [`f_vector_clear_ref_recto`](../casos/vector/clear.md#f_vector_clear_ref_recto)
- [`f_vector_clear_ref_guarda`](../casos/vector/clear.md#f_vector_clear_ref_guarda)
- [`f_vector_clear_ref_llamada`](../casos/vector/clear.md#f_vector_clear_ref_llamada)
- [`f_vector_clear_ptr_recto`](../casos/vector/clear.md#f_vector_clear_ptr_recto)
- [`f_vector_clear_ptr_guarda`](../casos/vector/clear.md#f_vector_clear_ptr_guarda)
- [`f_vector_clear_ptr_llamada`](../casos/vector/clear.md#f_vector_clear_ptr_llamada)
- [`f_vector_assign_ref_recto`](../casos/vector/assign.md#f_vector_assign_ref_recto)
- [`f_vector_assign_ref_guarda`](../casos/vector/assign.md#f_vector_assign_ref_guarda)
- [`f_vector_assign_ref_llamada`](../casos/vector/assign.md#f_vector_assign_ref_llamada)
- [`f_vector_assign_ptr_recto`](../casos/vector/assign.md#f_vector_assign_ptr_recto)
- [`f_vector_assign_ptr_guarda`](../casos/vector/assign.md#f_vector_assign_ptr_guarda)
- [`f_vector_assign_ptr_llamada`](../casos/vector/assign.md#f_vector_assign_ptr_llamada)
- [`f_deque_insert_middle_ref_recto`](../casos/deque/insert_middle.md#f_deque_insert_middle_ref_recto)
- [`f_deque_insert_middle_ref_guarda`](../casos/deque/insert_middle.md#f_deque_insert_middle_ref_guarda)
- [`f_deque_insert_middle_ref_llamada`](../casos/deque/insert_middle.md#f_deque_insert_middle_ref_llamada)
- [`f_deque_insert_middle_ptr_recto`](../casos/deque/insert_middle.md#f_deque_insert_middle_ptr_recto)
- [`f_deque_insert_middle_ptr_guarda`](../casos/deque/insert_middle.md#f_deque_insert_middle_ptr_guarda)
- [`f_deque_insert_middle_ptr_llamada`](../casos/deque/insert_middle.md#f_deque_insert_middle_ptr_llamada)
- [`f_deque_erase_begin_ref_recto`](../casos/deque/erase_begin.md#f_deque_erase_begin_ref_recto)
- [`f_deque_erase_begin_ref_guarda`](../casos/deque/erase_begin.md#f_deque_erase_begin_ref_guarda)
- [`f_deque_erase_begin_ref_llamada`](../casos/deque/erase_begin.md#f_deque_erase_begin_ref_llamada)
- [`f_deque_erase_begin_ptr_recto`](../casos/deque/erase_begin.md#f_deque_erase_begin_ptr_recto)
- [`f_deque_erase_begin_ptr_guarda`](../casos/deque/erase_begin.md#f_deque_erase_begin_ptr_guarda)
- [`f_deque_erase_begin_ptr_llamada`](../casos/deque/erase_begin.md#f_deque_erase_begin_ptr_llamada)
- [`f_deque_clear_ref_recto`](../casos/deque/clear.md#f_deque_clear_ref_recto)
- [`f_deque_clear_ref_guarda`](../casos/deque/clear.md#f_deque_clear_ref_guarda)
- [`f_deque_clear_ref_llamada`](../casos/deque/clear.md#f_deque_clear_ref_llamada)
- [`f_deque_clear_ptr_recto`](../casos/deque/clear.md#f_deque_clear_ptr_recto)
- [`f_deque_clear_ptr_guarda`](../casos/deque/clear.md#f_deque_clear_ptr_guarda)
- [`f_deque_clear_ptr_llamada`](../casos/deque/clear.md#f_deque_clear_ptr_llamada)
- [`f_deque_pop_front_ref_recto`](../casos/deque/pop_front.md#f_deque_pop_front_ref_recto)
- [`f_deque_pop_front_ref_guarda`](../casos/deque/pop_front.md#f_deque_pop_front_ref_guarda)
- [`f_deque_pop_front_ref_llamada`](../casos/deque/pop_front.md#f_deque_pop_front_ref_llamada)
- [`f_deque_pop_front_ptr_recto`](../casos/deque/pop_front.md#f_deque_pop_front_ptr_recto)
- [`f_deque_pop_front_ptr_guarda`](../casos/deque/pop_front.md#f_deque_pop_front_ptr_guarda)
- [`f_deque_pop_front_ptr_llamada`](../casos/deque/pop_front.md#f_deque_pop_front_ptr_llamada)
- [`f_uset_rehash_it_recto`](../casos/uset/rehash.md#f_uset_rehash_it_recto)
- [`f_uset_rehash_it_guarda`](../casos/uset/rehash.md#f_uset_rehash_it_guarda)
- [`f_uset_rehash_it_bucle`](../casos/uset/rehash.md#f_uset_rehash_it_bucle)
- [`f_uset_rehash_it_llamada`](../casos/uset/rehash.md#f_uset_rehash_it_llamada)
- [`f_uset_rehash_ref_bucle`](../casos/uset/rehash.md#f_uset_rehash_ref_bucle)
- [`f_uset_rehash_ptr_bucle`](../casos/uset/rehash.md#f_uset_rehash_ptr_bucle)
- [`f_uset_reserve_it_recto`](../casos/uset/reserve.md#f_uset_reserve_it_recto)
- [`f_uset_reserve_it_guarda`](../casos/uset/reserve.md#f_uset_reserve_it_guarda)
- [`f_uset_reserve_it_bucle`](../casos/uset/reserve.md#f_uset_reserve_it_bucle)
- [`f_uset_reserve_it_llamada`](../casos/uset/reserve.md#f_uset_reserve_it_llamada)
- [`f_uset_reserve_ref_bucle`](../casos/uset/reserve.md#f_uset_reserve_ref_bucle)
- [`f_uset_reserve_ptr_bucle`](../casos/uset/reserve.md#f_uset_reserve_ptr_bucle)
- [`f_umap_rehash_it_recto`](../casos/umap/rehash.md#f_umap_rehash_it_recto)
- [`f_umap_rehash_it_guarda`](../casos/umap/rehash.md#f_umap_rehash_it_guarda)
- [`f_umap_rehash_it_bucle`](../casos/umap/rehash.md#f_umap_rehash_it_bucle)
- [`f_umap_rehash_it_llamada`](../casos/umap/rehash.md#f_umap_rehash_it_llamada)
- [`f_umap_rehash_ref_bucle`](../casos/umap/rehash.md#f_umap_rehash_ref_bucle)
- [`f_umap_rehash_ptr_bucle`](../casos/umap/rehash.md#f_umap_rehash_ptr_bucle)

</details>
