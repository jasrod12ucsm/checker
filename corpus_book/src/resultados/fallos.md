
# Catálogo de falsos negativos

Los 254 casos `UB` sobre los que el analizador estático calla,
clasificados por la causa que los explica (con precedencia: se asigna la
primera que aplica). Fuente: `test/corpus_fallos.json`.

| Causa | Casos | % |
|---|---:|---:|
| 1. El dominio de referencias y punteros no esta modelado | 226 | 89.0% |
| 2. Sin comparacion previa contra end(), el modelado no se activa | 5 | 2.0% |
| 3. Se invalida por identidad del iterador, no por posicion | 3 | 1.2% |
| 4. La invalidacion por insercion/realojamiento no esta modelada | 20 | 7.9% |

## 1. El dominio de referencias y punteros no esta modelado

226 casos.

| Caso | Contenedor | Operación | Sostiene | Forma |
|---|---|---|---|---|
| [`f_vector_push_back_ref_bucle`](../casos/vector/push_back.md#f_vector_push_back_ref_bucle) | `vector` | `push_back` | `ref` | `bucle` |
| [`f_vector_push_back_ptr_bucle`](../casos/vector/push_back.md#f_vector_push_back_ptr_bucle) | `vector` | `push_back` | `ptr` | `bucle` |
| [`f_vector_emplace_back_ref_bucle`](../casos/vector/emplace_back.md#f_vector_emplace_back_ref_bucle) | `vector` | `emplace_back` | `ref` | `bucle` |
| [`f_vector_emplace_back_ptr_bucle`](../casos/vector/emplace_back.md#f_vector_emplace_back_ptr_bucle) | `vector` | `emplace_back` | `ptr` | `bucle` |
| [`f_vector_insert_begin_ref_recto`](../casos/vector/insert_begin.md#f_vector_insert_begin_ref_recto) | `vector` | `insert_begin` | `ref` | `recto` |
| [`f_vector_insert_begin_ref_guarda`](../casos/vector/insert_begin.md#f_vector_insert_begin_ref_guarda) | `vector` | `insert_begin` | `ref` | `guarda` |
| [`f_vector_insert_begin_ref_bucle`](../casos/vector/insert_begin.md#f_vector_insert_begin_ref_bucle) | `vector` | `insert_begin` | `ref` | `bucle` |
| [`f_vector_insert_begin_ref_llamada`](../casos/vector/insert_begin.md#f_vector_insert_begin_ref_llamada) | `vector` | `insert_begin` | `ref` | `llamada` |
| [`f_vector_insert_begin_ptr_recto`](../casos/vector/insert_begin.md#f_vector_insert_begin_ptr_recto) | `vector` | `insert_begin` | `ptr` | `recto` |
| [`f_vector_insert_begin_ptr_guarda`](../casos/vector/insert_begin.md#f_vector_insert_begin_ptr_guarda) | `vector` | `insert_begin` | `ptr` | `guarda` |
| [`f_vector_insert_begin_ptr_bucle`](../casos/vector/insert_begin.md#f_vector_insert_begin_ptr_bucle) | `vector` | `insert_begin` | `ptr` | `bucle` |
| [`f_vector_insert_begin_ptr_llamada`](../casos/vector/insert_begin.md#f_vector_insert_begin_ptr_llamada) | `vector` | `insert_begin` | `ptr` | `llamada` |
| [`f_vector_insert_end_ref_bucle`](../casos/vector/insert_end.md#f_vector_insert_end_ref_bucle) | `vector` | `insert_end` | `ref` | `bucle` |
| [`f_vector_insert_end_ptr_bucle`](../casos/vector/insert_end.md#f_vector_insert_end_ptr_bucle) | `vector` | `insert_end` | `ptr` | `bucle` |
| [`f_vector_erase_begin_ref_recto`](../casos/vector/erase_begin.md#f_vector_erase_begin_ref_recto) | `vector` | `erase_begin` | `ref` | `recto` |
| [`f_vector_erase_begin_ref_guarda`](../casos/vector/erase_begin.md#f_vector_erase_begin_ref_guarda) | `vector` | `erase_begin` | `ref` | `guarda` |
| [`f_vector_erase_begin_ref_bucle`](../casos/vector/erase_begin.md#f_vector_erase_begin_ref_bucle) | `vector` | `erase_begin` | `ref` | `bucle` |
| [`f_vector_erase_begin_ref_llamada`](../casos/vector/erase_begin.md#f_vector_erase_begin_ref_llamada) | `vector` | `erase_begin` | `ref` | `llamada` |
| [`f_vector_erase_begin_ptr_recto`](../casos/vector/erase_begin.md#f_vector_erase_begin_ptr_recto) | `vector` | `erase_begin` | `ptr` | `recto` |
| [`f_vector_erase_begin_ptr_guarda`](../casos/vector/erase_begin.md#f_vector_erase_begin_ptr_guarda) | `vector` | `erase_begin` | `ptr` | `guarda` |
| [`f_vector_erase_begin_ptr_bucle`](../casos/vector/erase_begin.md#f_vector_erase_begin_ptr_bucle) | `vector` | `erase_begin` | `ptr` | `bucle` |
| [`f_vector_erase_begin_ptr_llamada`](../casos/vector/erase_begin.md#f_vector_erase_begin_ptr_llamada) | `vector` | `erase_begin` | `ptr` | `llamada` |
| [`f_vector_clear_ref_recto`](../casos/vector/clear.md#f_vector_clear_ref_recto) | `vector` | `clear` | `ref` | `recto` |
| [`f_vector_clear_ref_guarda`](../casos/vector/clear.md#f_vector_clear_ref_guarda) | `vector` | `clear` | `ref` | `guarda` |
| [`f_vector_clear_ref_bucle`](../casos/vector/clear.md#f_vector_clear_ref_bucle) | `vector` | `clear` | `ref` | `bucle` |
| [`f_vector_clear_ref_llamada`](../casos/vector/clear.md#f_vector_clear_ref_llamada) | `vector` | `clear` | `ref` | `llamada` |
| [`f_vector_clear_ptr_recto`](../casos/vector/clear.md#f_vector_clear_ptr_recto) | `vector` | `clear` | `ptr` | `recto` |
| [`f_vector_clear_ptr_guarda`](../casos/vector/clear.md#f_vector_clear_ptr_guarda) | `vector` | `clear` | `ptr` | `guarda` |
| [`f_vector_clear_ptr_bucle`](../casos/vector/clear.md#f_vector_clear_ptr_bucle) | `vector` | `clear` | `ptr` | `bucle` |
| [`f_vector_clear_ptr_llamada`](../casos/vector/clear.md#f_vector_clear_ptr_llamada) | `vector` | `clear` | `ptr` | `llamada` |
| [`f_vector_resize_grow_ref_bucle`](../casos/vector/resize_grow.md#f_vector_resize_grow_ref_bucle) | `vector` | `resize_grow` | `ref` | `bucle` |
| [`f_vector_resize_grow_ptr_bucle`](../casos/vector/resize_grow.md#f_vector_resize_grow_ptr_bucle) | `vector` | `resize_grow` | `ptr` | `bucle` |
| [`f_vector_reserve_ref_bucle`](../casos/vector/reserve.md#f_vector_reserve_ref_bucle) | `vector` | `reserve` | `ref` | `bucle` |
| [`f_vector_reserve_ptr_bucle`](../casos/vector/reserve.md#f_vector_reserve_ptr_bucle) | `vector` | `reserve` | `ptr` | `bucle` |
| [`f_vector_assign_ref_recto`](../casos/vector/assign.md#f_vector_assign_ref_recto) | `vector` | `assign` | `ref` | `recto` |
| [`f_vector_assign_ref_guarda`](../casos/vector/assign.md#f_vector_assign_ref_guarda) | `vector` | `assign` | `ref` | `guarda` |
| [`f_vector_assign_ref_bucle`](../casos/vector/assign.md#f_vector_assign_ref_bucle) | `vector` | `assign` | `ref` | `bucle` |
| [`f_vector_assign_ref_llamada`](../casos/vector/assign.md#f_vector_assign_ref_llamada) | `vector` | `assign` | `ref` | `llamada` |
| [`f_vector_assign_ptr_recto`](../casos/vector/assign.md#f_vector_assign_ptr_recto) | `vector` | `assign` | `ptr` | `recto` |
| [`f_vector_assign_ptr_guarda`](../casos/vector/assign.md#f_vector_assign_ptr_guarda) | `vector` | `assign` | `ptr` | `guarda` |
| [`f_vector_assign_ptr_bucle`](../casos/vector/assign.md#f_vector_assign_ptr_bucle) | `vector` | `assign` | `ptr` | `bucle` |
| [`f_vector_assign_ptr_llamada`](../casos/vector/assign.md#f_vector_assign_ptr_llamada) | `vector` | `assign` | `ptr` | `llamada` |
| [`f_vector_pop_back_ref_bucle`](../casos/vector/pop_back.md#f_vector_pop_back_ref_bucle) | `vector` | `pop_back` | `ref` | `bucle` |
| [`f_vector_pop_back_ptr_bucle`](../casos/vector/pop_back.md#f_vector_pop_back_ptr_bucle) | `vector` | `pop_back` | `ptr` | `bucle` |
| [`f_deque_push_back_ref_bucle`](../casos/deque/push_back.md#f_deque_push_back_ref_bucle) | `deque` | `push_back` | `ref` | `bucle` |
| [`f_deque_push_back_ptr_bucle`](../casos/deque/push_back.md#f_deque_push_back_ptr_bucle) | `deque` | `push_back` | `ptr` | `bucle` |
| [`f_deque_push_front_ref_bucle`](../casos/deque/push_front.md#f_deque_push_front_ref_bucle) | `deque` | `push_front` | `ref` | `bucle` |
| [`f_deque_push_front_ptr_bucle`](../casos/deque/push_front.md#f_deque_push_front_ptr_bucle) | `deque` | `push_front` | `ptr` | `bucle` |
| [`f_deque_emplace_back_ref_bucle`](../casos/deque/emplace_back.md#f_deque_emplace_back_ref_bucle) | `deque` | `emplace_back` | `ref` | `bucle` |
| [`f_deque_emplace_back_ptr_bucle`](../casos/deque/emplace_back.md#f_deque_emplace_back_ptr_bucle) | `deque` | `emplace_back` | `ptr` | `bucle` |
| [`f_deque_insert_middle_ref_recto`](../casos/deque/insert_middle.md#f_deque_insert_middle_ref_recto) | `deque` | `insert_middle` | `ref` | `recto` |
| [`f_deque_insert_middle_ref_guarda`](../casos/deque/insert_middle.md#f_deque_insert_middle_ref_guarda) | `deque` | `insert_middle` | `ref` | `guarda` |
| [`f_deque_insert_middle_ref_bucle`](../casos/deque/insert_middle.md#f_deque_insert_middle_ref_bucle) | `deque` | `insert_middle` | `ref` | `bucle` |
| [`f_deque_insert_middle_ref_llamada`](../casos/deque/insert_middle.md#f_deque_insert_middle_ref_llamada) | `deque` | `insert_middle` | `ref` | `llamada` |
| [`f_deque_insert_middle_ptr_recto`](../casos/deque/insert_middle.md#f_deque_insert_middle_ptr_recto) | `deque` | `insert_middle` | `ptr` | `recto` |
| [`f_deque_insert_middle_ptr_guarda`](../casos/deque/insert_middle.md#f_deque_insert_middle_ptr_guarda) | `deque` | `insert_middle` | `ptr` | `guarda` |
| [`f_deque_insert_middle_ptr_bucle`](../casos/deque/insert_middle.md#f_deque_insert_middle_ptr_bucle) | `deque` | `insert_middle` | `ptr` | `bucle` |
| [`f_deque_insert_middle_ptr_llamada`](../casos/deque/insert_middle.md#f_deque_insert_middle_ptr_llamada) | `deque` | `insert_middle` | `ptr` | `llamada` |
| [`f_deque_erase_begin_ref_recto`](../casos/deque/erase_begin.md#f_deque_erase_begin_ref_recto) | `deque` | `erase_begin` | `ref` | `recto` |
| [`f_deque_erase_begin_ref_guarda`](../casos/deque/erase_begin.md#f_deque_erase_begin_ref_guarda) | `deque` | `erase_begin` | `ref` | `guarda` |
| [`f_deque_erase_begin_ref_bucle`](../casos/deque/erase_begin.md#f_deque_erase_begin_ref_bucle) | `deque` | `erase_begin` | `ref` | `bucle` |
| [`f_deque_erase_begin_ref_llamada`](../casos/deque/erase_begin.md#f_deque_erase_begin_ref_llamada) | `deque` | `erase_begin` | `ref` | `llamada` |
| [`f_deque_erase_begin_ptr_recto`](../casos/deque/erase_begin.md#f_deque_erase_begin_ptr_recto) | `deque` | `erase_begin` | `ptr` | `recto` |
| [`f_deque_erase_begin_ptr_guarda`](../casos/deque/erase_begin.md#f_deque_erase_begin_ptr_guarda) | `deque` | `erase_begin` | `ptr` | `guarda` |
| [`f_deque_erase_begin_ptr_bucle`](../casos/deque/erase_begin.md#f_deque_erase_begin_ptr_bucle) | `deque` | `erase_begin` | `ptr` | `bucle` |
| [`f_deque_erase_begin_ptr_llamada`](../casos/deque/erase_begin.md#f_deque_erase_begin_ptr_llamada) | `deque` | `erase_begin` | `ptr` | `llamada` |
| [`f_deque_clear_ref_recto`](../casos/deque/clear.md#f_deque_clear_ref_recto) | `deque` | `clear` | `ref` | `recto` |
| [`f_deque_clear_ref_guarda`](../casos/deque/clear.md#f_deque_clear_ref_guarda) | `deque` | `clear` | `ref` | `guarda` |
| [`f_deque_clear_ref_bucle`](../casos/deque/clear.md#f_deque_clear_ref_bucle) | `deque` | `clear` | `ref` | `bucle` |
| [`f_deque_clear_ref_llamada`](../casos/deque/clear.md#f_deque_clear_ref_llamada) | `deque` | `clear` | `ref` | `llamada` |
| [`f_deque_clear_ptr_recto`](../casos/deque/clear.md#f_deque_clear_ptr_recto) | `deque` | `clear` | `ptr` | `recto` |
| [`f_deque_clear_ptr_guarda`](../casos/deque/clear.md#f_deque_clear_ptr_guarda) | `deque` | `clear` | `ptr` | `guarda` |
| [`f_deque_clear_ptr_bucle`](../casos/deque/clear.md#f_deque_clear_ptr_bucle) | `deque` | `clear` | `ptr` | `bucle` |
| [`f_deque_clear_ptr_llamada`](../casos/deque/clear.md#f_deque_clear_ptr_llamada) | `deque` | `clear` | `ptr` | `llamada` |
| [`f_deque_resize_grow_ref_bucle`](../casos/deque/resize_grow.md#f_deque_resize_grow_ref_bucle) | `deque` | `resize_grow` | `ref` | `bucle` |
| [`f_deque_resize_grow_ptr_bucle`](../casos/deque/resize_grow.md#f_deque_resize_grow_ptr_bucle) | `deque` | `resize_grow` | `ptr` | `bucle` |
| [`f_deque_pop_front_ref_recto`](../casos/deque/pop_front.md#f_deque_pop_front_ref_recto) | `deque` | `pop_front` | `ref` | `recto` |
| [`f_deque_pop_front_ref_guarda`](../casos/deque/pop_front.md#f_deque_pop_front_ref_guarda) | `deque` | `pop_front` | `ref` | `guarda` |
| [`f_deque_pop_front_ref_bucle`](../casos/deque/pop_front.md#f_deque_pop_front_ref_bucle) | `deque` | `pop_front` | `ref` | `bucle` |
| [`f_deque_pop_front_ref_llamada`](../casos/deque/pop_front.md#f_deque_pop_front_ref_llamada) | `deque` | `pop_front` | `ref` | `llamada` |
| [`f_deque_pop_front_ptr_recto`](../casos/deque/pop_front.md#f_deque_pop_front_ptr_recto) | `deque` | `pop_front` | `ptr` | `recto` |
| [`f_deque_pop_front_ptr_guarda`](../casos/deque/pop_front.md#f_deque_pop_front_ptr_guarda) | `deque` | `pop_front` | `ptr` | `guarda` |
| [`f_deque_pop_front_ptr_bucle`](../casos/deque/pop_front.md#f_deque_pop_front_ptr_bucle) | `deque` | `pop_front` | `ptr` | `bucle` |
| [`f_deque_pop_front_ptr_llamada`](../casos/deque/pop_front.md#f_deque_pop_front_ptr_llamada) | `deque` | `pop_front` | `ptr` | `llamada` |
| [`f_list_erase_begin_ref_recto`](../casos/list/erase_begin.md#f_list_erase_begin_ref_recto) | `list` | `erase_begin` | `ref` | `recto` |
| [`f_list_erase_begin_ref_guarda`](../casos/list/erase_begin.md#f_list_erase_begin_ref_guarda) | `list` | `erase_begin` | `ref` | `guarda` |
| [`f_list_erase_begin_ref_bucle`](../casos/list/erase_begin.md#f_list_erase_begin_ref_bucle) | `list` | `erase_begin` | `ref` | `bucle` |
| [`f_list_erase_begin_ref_llamada`](../casos/list/erase_begin.md#f_list_erase_begin_ref_llamada) | `list` | `erase_begin` | `ref` | `llamada` |
| [`f_list_erase_begin_ptr_recto`](../casos/list/erase_begin.md#f_list_erase_begin_ptr_recto) | `list` | `erase_begin` | `ptr` | `recto` |
| [`f_list_erase_begin_ptr_guarda`](../casos/list/erase_begin.md#f_list_erase_begin_ptr_guarda) | `list` | `erase_begin` | `ptr` | `guarda` |
| [`f_list_erase_begin_ptr_bucle`](../casos/list/erase_begin.md#f_list_erase_begin_ptr_bucle) | `list` | `erase_begin` | `ptr` | `bucle` |
| [`f_list_erase_begin_ptr_llamada`](../casos/list/erase_begin.md#f_list_erase_begin_ptr_llamada) | `list` | `erase_begin` | `ptr` | `llamada` |
| [`f_list_clear_ref_recto`](../casos/list/clear.md#f_list_clear_ref_recto) | `list` | `clear` | `ref` | `recto` |
| [`f_list_clear_ref_guarda`](../casos/list/clear.md#f_list_clear_ref_guarda) | `list` | `clear` | `ref` | `guarda` |
| [`f_list_clear_ref_bucle`](../casos/list/clear.md#f_list_clear_ref_bucle) | `list` | `clear` | `ref` | `bucle` |
| [`f_list_clear_ref_llamada`](../casos/list/clear.md#f_list_clear_ref_llamada) | `list` | `clear` | `ref` | `llamada` |
| [`f_list_clear_ptr_recto`](../casos/list/clear.md#f_list_clear_ptr_recto) | `list` | `clear` | `ptr` | `recto` |
| [`f_list_clear_ptr_guarda`](../casos/list/clear.md#f_list_clear_ptr_guarda) | `list` | `clear` | `ptr` | `guarda` |
| [`f_list_clear_ptr_bucle`](../casos/list/clear.md#f_list_clear_ptr_bucle) | `list` | `clear` | `ptr` | `bucle` |
| [`f_list_clear_ptr_llamada`](../casos/list/clear.md#f_list_clear_ptr_llamada) | `list` | `clear` | `ptr` | `llamada` |
| [`f_list_pop_front_ref_recto`](../casos/list/pop_front.md#f_list_pop_front_ref_recto) | `list` | `pop_front` | `ref` | `recto` |
| [`f_list_pop_front_ref_guarda`](../casos/list/pop_front.md#f_list_pop_front_ref_guarda) | `list` | `pop_front` | `ref` | `guarda` |
| [`f_list_pop_front_ref_bucle`](../casos/list/pop_front.md#f_list_pop_front_ref_bucle) | `list` | `pop_front` | `ref` | `bucle` |
| [`f_list_pop_front_ref_llamada`](../casos/list/pop_front.md#f_list_pop_front_ref_llamada) | `list` | `pop_front` | `ref` | `llamada` |
| [`f_list_pop_front_ptr_recto`](../casos/list/pop_front.md#f_list_pop_front_ptr_recto) | `list` | `pop_front` | `ptr` | `recto` |
| [`f_list_pop_front_ptr_guarda`](../casos/list/pop_front.md#f_list_pop_front_ptr_guarda) | `list` | `pop_front` | `ptr` | `guarda` |
| [`f_list_pop_front_ptr_bucle`](../casos/list/pop_front.md#f_list_pop_front_ptr_bucle) | `list` | `pop_front` | `ptr` | `bucle` |
| [`f_list_pop_front_ptr_llamada`](../casos/list/pop_front.md#f_list_pop_front_ptr_llamada) | `list` | `pop_front` | `ptr` | `llamada` |
| [`f_flist_erase_after_ref_recto`](../casos/flist/erase_after.md#f_flist_erase_after_ref_recto) | `flist` | `erase_after` | `ref` | `recto` |
| [`f_flist_erase_after_ref_guarda`](../casos/flist/erase_after.md#f_flist_erase_after_ref_guarda) | `flist` | `erase_after` | `ref` | `guarda` |
| [`f_flist_erase_after_ref_bucle`](../casos/flist/erase_after.md#f_flist_erase_after_ref_bucle) | `flist` | `erase_after` | `ref` | `bucle` |
| [`f_flist_erase_after_ref_llamada`](../casos/flist/erase_after.md#f_flist_erase_after_ref_llamada) | `flist` | `erase_after` | `ref` | `llamada` |
| [`f_flist_erase_after_ptr_recto`](../casos/flist/erase_after.md#f_flist_erase_after_ptr_recto) | `flist` | `erase_after` | `ptr` | `recto` |
| [`f_flist_erase_after_ptr_guarda`](../casos/flist/erase_after.md#f_flist_erase_after_ptr_guarda) | `flist` | `erase_after` | `ptr` | `guarda` |
| [`f_flist_erase_after_ptr_bucle`](../casos/flist/erase_after.md#f_flist_erase_after_ptr_bucle) | `flist` | `erase_after` | `ptr` | `bucle` |
| [`f_flist_erase_after_ptr_llamada`](../casos/flist/erase_after.md#f_flist_erase_after_ptr_llamada) | `flist` | `erase_after` | `ptr` | `llamada` |
| [`f_flist_clear_ref_recto`](../casos/flist/clear.md#f_flist_clear_ref_recto) | `flist` | `clear` | `ref` | `recto` |
| [`f_flist_clear_ref_guarda`](../casos/flist/clear.md#f_flist_clear_ref_guarda) | `flist` | `clear` | `ref` | `guarda` |
| [`f_flist_clear_ref_bucle`](../casos/flist/clear.md#f_flist_clear_ref_bucle) | `flist` | `clear` | `ref` | `bucle` |
| [`f_flist_clear_ref_llamada`](../casos/flist/clear.md#f_flist_clear_ref_llamada) | `flist` | `clear` | `ref` | `llamada` |
| [`f_flist_clear_ptr_recto`](../casos/flist/clear.md#f_flist_clear_ptr_recto) | `flist` | `clear` | `ptr` | `recto` |
| [`f_flist_clear_ptr_guarda`](../casos/flist/clear.md#f_flist_clear_ptr_guarda) | `flist` | `clear` | `ptr` | `guarda` |
| [`f_flist_clear_ptr_bucle`](../casos/flist/clear.md#f_flist_clear_ptr_bucle) | `flist` | `clear` | `ptr` | `bucle` |
| [`f_flist_clear_ptr_llamada`](../casos/flist/clear.md#f_flist_clear_ptr_llamada) | `flist` | `clear` | `ptr` | `llamada` |
| [`f_set_erase_begin_ref_recto`](../casos/set/erase_begin.md#f_set_erase_begin_ref_recto) | `set` | `erase_begin` | `ref` | `recto` |
| [`f_set_erase_begin_ref_guarda`](../casos/set/erase_begin.md#f_set_erase_begin_ref_guarda) | `set` | `erase_begin` | `ref` | `guarda` |
| [`f_set_erase_begin_ref_bucle`](../casos/set/erase_begin.md#f_set_erase_begin_ref_bucle) | `set` | `erase_begin` | `ref` | `bucle` |
| [`f_set_erase_begin_ref_llamada`](../casos/set/erase_begin.md#f_set_erase_begin_ref_llamada) | `set` | `erase_begin` | `ref` | `llamada` |
| [`f_set_erase_begin_ptr_recto`](../casos/set/erase_begin.md#f_set_erase_begin_ptr_recto) | `set` | `erase_begin` | `ptr` | `recto` |
| [`f_set_erase_begin_ptr_guarda`](../casos/set/erase_begin.md#f_set_erase_begin_ptr_guarda) | `set` | `erase_begin` | `ptr` | `guarda` |
| [`f_set_erase_begin_ptr_bucle`](../casos/set/erase_begin.md#f_set_erase_begin_ptr_bucle) | `set` | `erase_begin` | `ptr` | `bucle` |
| [`f_set_erase_begin_ptr_llamada`](../casos/set/erase_begin.md#f_set_erase_begin_ptr_llamada) | `set` | `erase_begin` | `ptr` | `llamada` |
| [`f_set_clear_ref_recto`](../casos/set/clear.md#f_set_clear_ref_recto) | `set` | `clear` | `ref` | `recto` |
| [`f_set_clear_ref_guarda`](../casos/set/clear.md#f_set_clear_ref_guarda) | `set` | `clear` | `ref` | `guarda` |
| [`f_set_clear_ref_bucle`](../casos/set/clear.md#f_set_clear_ref_bucle) | `set` | `clear` | `ref` | `bucle` |
| [`f_set_clear_ref_llamada`](../casos/set/clear.md#f_set_clear_ref_llamada) | `set` | `clear` | `ref` | `llamada` |
| [`f_set_clear_ptr_recto`](../casos/set/clear.md#f_set_clear_ptr_recto) | `set` | `clear` | `ptr` | `recto` |
| [`f_set_clear_ptr_guarda`](../casos/set/clear.md#f_set_clear_ptr_guarda) | `set` | `clear` | `ptr` | `guarda` |
| [`f_set_clear_ptr_bucle`](../casos/set/clear.md#f_set_clear_ptr_bucle) | `set` | `clear` | `ptr` | `bucle` |
| [`f_set_clear_ptr_llamada`](../casos/set/clear.md#f_set_clear_ptr_llamada) | `set` | `clear` | `ptr` | `llamada` |
| [`f_mset_erase_begin_ref_recto`](../casos/mset/erase_begin.md#f_mset_erase_begin_ref_recto) | `mset` | `erase_begin` | `ref` | `recto` |
| [`f_mset_erase_begin_ref_guarda`](../casos/mset/erase_begin.md#f_mset_erase_begin_ref_guarda) | `mset` | `erase_begin` | `ref` | `guarda` |
| [`f_mset_erase_begin_ref_bucle`](../casos/mset/erase_begin.md#f_mset_erase_begin_ref_bucle) | `mset` | `erase_begin` | `ref` | `bucle` |
| [`f_mset_erase_begin_ref_llamada`](../casos/mset/erase_begin.md#f_mset_erase_begin_ref_llamada) | `mset` | `erase_begin` | `ref` | `llamada` |
| [`f_mset_erase_begin_ptr_recto`](../casos/mset/erase_begin.md#f_mset_erase_begin_ptr_recto) | `mset` | `erase_begin` | `ptr` | `recto` |
| [`f_mset_erase_begin_ptr_guarda`](../casos/mset/erase_begin.md#f_mset_erase_begin_ptr_guarda) | `mset` | `erase_begin` | `ptr` | `guarda` |
| [`f_mset_erase_begin_ptr_bucle`](../casos/mset/erase_begin.md#f_mset_erase_begin_ptr_bucle) | `mset` | `erase_begin` | `ptr` | `bucle` |
| [`f_mset_erase_begin_ptr_llamada`](../casos/mset/erase_begin.md#f_mset_erase_begin_ptr_llamada) | `mset` | `erase_begin` | `ptr` | `llamada` |
| [`f_mset_clear_ref_recto`](../casos/mset/clear.md#f_mset_clear_ref_recto) | `mset` | `clear` | `ref` | `recto` |
| [`f_mset_clear_ref_guarda`](../casos/mset/clear.md#f_mset_clear_ref_guarda) | `mset` | `clear` | `ref` | `guarda` |
| [`f_mset_clear_ref_bucle`](../casos/mset/clear.md#f_mset_clear_ref_bucle) | `mset` | `clear` | `ref` | `bucle` |
| [`f_mset_clear_ref_llamada`](../casos/mset/clear.md#f_mset_clear_ref_llamada) | `mset` | `clear` | `ref` | `llamada` |
| [`f_mset_clear_ptr_recto`](../casos/mset/clear.md#f_mset_clear_ptr_recto) | `mset` | `clear` | `ptr` | `recto` |
| [`f_mset_clear_ptr_guarda`](../casos/mset/clear.md#f_mset_clear_ptr_guarda) | `mset` | `clear` | `ptr` | `guarda` |
| [`f_mset_clear_ptr_bucle`](../casos/mset/clear.md#f_mset_clear_ptr_bucle) | `mset` | `clear` | `ptr` | `bucle` |
| [`f_mset_clear_ptr_llamada`](../casos/mset/clear.md#f_mset_clear_ptr_llamada) | `mset` | `clear` | `ptr` | `llamada` |
| [`f_map_erase_begin_ref_recto`](../casos/map/erase_begin.md#f_map_erase_begin_ref_recto) | `map` | `erase_begin` | `ref` | `recto` |
| [`f_map_erase_begin_ref_guarda`](../casos/map/erase_begin.md#f_map_erase_begin_ref_guarda) | `map` | `erase_begin` | `ref` | `guarda` |
| [`f_map_erase_begin_ref_bucle`](../casos/map/erase_begin.md#f_map_erase_begin_ref_bucle) | `map` | `erase_begin` | `ref` | `bucle` |
| [`f_map_erase_begin_ref_llamada`](../casos/map/erase_begin.md#f_map_erase_begin_ref_llamada) | `map` | `erase_begin` | `ref` | `llamada` |
| [`f_map_erase_begin_ptr_recto`](../casos/map/erase_begin.md#f_map_erase_begin_ptr_recto) | `map` | `erase_begin` | `ptr` | `recto` |
| [`f_map_erase_begin_ptr_guarda`](../casos/map/erase_begin.md#f_map_erase_begin_ptr_guarda) | `map` | `erase_begin` | `ptr` | `guarda` |
| [`f_map_erase_begin_ptr_bucle`](../casos/map/erase_begin.md#f_map_erase_begin_ptr_bucle) | `map` | `erase_begin` | `ptr` | `bucle` |
| [`f_map_erase_begin_ptr_llamada`](../casos/map/erase_begin.md#f_map_erase_begin_ptr_llamada) | `map` | `erase_begin` | `ptr` | `llamada` |
| [`f_map_clear_ref_recto`](../casos/map/clear.md#f_map_clear_ref_recto) | `map` | `clear` | `ref` | `recto` |
| [`f_map_clear_ref_guarda`](../casos/map/clear.md#f_map_clear_ref_guarda) | `map` | `clear` | `ref` | `guarda` |
| [`f_map_clear_ref_bucle`](../casos/map/clear.md#f_map_clear_ref_bucle) | `map` | `clear` | `ref` | `bucle` |
| [`f_map_clear_ref_llamada`](../casos/map/clear.md#f_map_clear_ref_llamada) | `map` | `clear` | `ref` | `llamada` |
| [`f_map_clear_ptr_recto`](../casos/map/clear.md#f_map_clear_ptr_recto) | `map` | `clear` | `ptr` | `recto` |
| [`f_map_clear_ptr_guarda`](../casos/map/clear.md#f_map_clear_ptr_guarda) | `map` | `clear` | `ptr` | `guarda` |
| [`f_map_clear_ptr_bucle`](../casos/map/clear.md#f_map_clear_ptr_bucle) | `map` | `clear` | `ptr` | `bucle` |
| [`f_map_clear_ptr_llamada`](../casos/map/clear.md#f_map_clear_ptr_llamada) | `map` | `clear` | `ptr` | `llamada` |
| [`f_mmap_erase_begin_ref_recto`](../casos/mmap/erase_begin.md#f_mmap_erase_begin_ref_recto) | `mmap` | `erase_begin` | `ref` | `recto` |
| [`f_mmap_erase_begin_ref_guarda`](../casos/mmap/erase_begin.md#f_mmap_erase_begin_ref_guarda) | `mmap` | `erase_begin` | `ref` | `guarda` |
| [`f_mmap_erase_begin_ref_bucle`](../casos/mmap/erase_begin.md#f_mmap_erase_begin_ref_bucle) | `mmap` | `erase_begin` | `ref` | `bucle` |
| [`f_mmap_erase_begin_ref_llamada`](../casos/mmap/erase_begin.md#f_mmap_erase_begin_ref_llamada) | `mmap` | `erase_begin` | `ref` | `llamada` |
| [`f_mmap_erase_begin_ptr_recto`](../casos/mmap/erase_begin.md#f_mmap_erase_begin_ptr_recto) | `mmap` | `erase_begin` | `ptr` | `recto` |
| [`f_mmap_erase_begin_ptr_guarda`](../casos/mmap/erase_begin.md#f_mmap_erase_begin_ptr_guarda) | `mmap` | `erase_begin` | `ptr` | `guarda` |
| [`f_mmap_erase_begin_ptr_bucle`](../casos/mmap/erase_begin.md#f_mmap_erase_begin_ptr_bucle) | `mmap` | `erase_begin` | `ptr` | `bucle` |
| [`f_mmap_erase_begin_ptr_llamada`](../casos/mmap/erase_begin.md#f_mmap_erase_begin_ptr_llamada) | `mmap` | `erase_begin` | `ptr` | `llamada` |
| [`f_mmap_clear_ref_recto`](../casos/mmap/clear.md#f_mmap_clear_ref_recto) | `mmap` | `clear` | `ref` | `recto` |
| [`f_mmap_clear_ref_guarda`](../casos/mmap/clear.md#f_mmap_clear_ref_guarda) | `mmap` | `clear` | `ref` | `guarda` |
| [`f_mmap_clear_ref_bucle`](../casos/mmap/clear.md#f_mmap_clear_ref_bucle) | `mmap` | `clear` | `ref` | `bucle` |
| [`f_mmap_clear_ref_llamada`](../casos/mmap/clear.md#f_mmap_clear_ref_llamada) | `mmap` | `clear` | `ref` | `llamada` |
| [`f_mmap_clear_ptr_recto`](../casos/mmap/clear.md#f_mmap_clear_ptr_recto) | `mmap` | `clear` | `ptr` | `recto` |
| [`f_mmap_clear_ptr_guarda`](../casos/mmap/clear.md#f_mmap_clear_ptr_guarda) | `mmap` | `clear` | `ptr` | `guarda` |
| [`f_mmap_clear_ptr_bucle`](../casos/mmap/clear.md#f_mmap_clear_ptr_bucle) | `mmap` | `clear` | `ptr` | `bucle` |
| [`f_mmap_clear_ptr_llamada`](../casos/mmap/clear.md#f_mmap_clear_ptr_llamada) | `mmap` | `clear` | `ptr` | `llamada` |
| [`f_uset_erase_begin_ref_recto`](../casos/uset/erase_begin.md#f_uset_erase_begin_ref_recto) | `uset` | `erase_begin` | `ref` | `recto` |
| [`f_uset_erase_begin_ref_guarda`](../casos/uset/erase_begin.md#f_uset_erase_begin_ref_guarda) | `uset` | `erase_begin` | `ref` | `guarda` |
| [`f_uset_erase_begin_ref_bucle`](../casos/uset/erase_begin.md#f_uset_erase_begin_ref_bucle) | `uset` | `erase_begin` | `ref` | `bucle` |
| [`f_uset_erase_begin_ref_llamada`](../casos/uset/erase_begin.md#f_uset_erase_begin_ref_llamada) | `uset` | `erase_begin` | `ref` | `llamada` |
| [`f_uset_erase_begin_ptr_recto`](../casos/uset/erase_begin.md#f_uset_erase_begin_ptr_recto) | `uset` | `erase_begin` | `ptr` | `recto` |
| [`f_uset_erase_begin_ptr_guarda`](../casos/uset/erase_begin.md#f_uset_erase_begin_ptr_guarda) | `uset` | `erase_begin` | `ptr` | `guarda` |
| [`f_uset_erase_begin_ptr_bucle`](../casos/uset/erase_begin.md#f_uset_erase_begin_ptr_bucle) | `uset` | `erase_begin` | `ptr` | `bucle` |
| [`f_uset_erase_begin_ptr_llamada`](../casos/uset/erase_begin.md#f_uset_erase_begin_ptr_llamada) | `uset` | `erase_begin` | `ptr` | `llamada` |
| [`f_uset_clear_ref_recto`](../casos/uset/clear.md#f_uset_clear_ref_recto) | `uset` | `clear` | `ref` | `recto` |
| [`f_uset_clear_ref_guarda`](../casos/uset/clear.md#f_uset_clear_ref_guarda) | `uset` | `clear` | `ref` | `guarda` |
| [`f_uset_clear_ref_bucle`](../casos/uset/clear.md#f_uset_clear_ref_bucle) | `uset` | `clear` | `ref` | `bucle` |
| [`f_uset_clear_ref_llamada`](../casos/uset/clear.md#f_uset_clear_ref_llamada) | `uset` | `clear` | `ref` | `llamada` |
| [`f_uset_clear_ptr_recto`](../casos/uset/clear.md#f_uset_clear_ptr_recto) | `uset` | `clear` | `ptr` | `recto` |
| [`f_uset_clear_ptr_guarda`](../casos/uset/clear.md#f_uset_clear_ptr_guarda) | `uset` | `clear` | `ptr` | `guarda` |
| [`f_uset_clear_ptr_bucle`](../casos/uset/clear.md#f_uset_clear_ptr_bucle) | `uset` | `clear` | `ptr` | `bucle` |
| [`f_uset_clear_ptr_llamada`](../casos/uset/clear.md#f_uset_clear_ptr_llamada) | `uset` | `clear` | `ptr` | `llamada` |
| [`f_uset_rehash_ref_bucle`](../casos/uset/rehash.md#f_uset_rehash_ref_bucle) | `uset` | `rehash` | `ref` | `bucle` |
| [`f_uset_rehash_ptr_bucle`](../casos/uset/rehash.md#f_uset_rehash_ptr_bucle) | `uset` | `rehash` | `ptr` | `bucle` |
| [`f_uset_reserve_ref_bucle`](../casos/uset/reserve.md#f_uset_reserve_ref_bucle) | `uset` | `reserve` | `ref` | `bucle` |
| [`f_uset_reserve_ptr_bucle`](../casos/uset/reserve.md#f_uset_reserve_ptr_bucle) | `uset` | `reserve` | `ptr` | `bucle` |
| [`f_umap_erase_begin_ref_recto`](../casos/umap/erase_begin.md#f_umap_erase_begin_ref_recto) | `umap` | `erase_begin` | `ref` | `recto` |
| [`f_umap_erase_begin_ref_guarda`](../casos/umap/erase_begin.md#f_umap_erase_begin_ref_guarda) | `umap` | `erase_begin` | `ref` | `guarda` |
| [`f_umap_erase_begin_ref_bucle`](../casos/umap/erase_begin.md#f_umap_erase_begin_ref_bucle) | `umap` | `erase_begin` | `ref` | `bucle` |
| [`f_umap_erase_begin_ref_llamada`](../casos/umap/erase_begin.md#f_umap_erase_begin_ref_llamada) | `umap` | `erase_begin` | `ref` | `llamada` |
| [`f_umap_erase_begin_ptr_recto`](../casos/umap/erase_begin.md#f_umap_erase_begin_ptr_recto) | `umap` | `erase_begin` | `ptr` | `recto` |
| [`f_umap_erase_begin_ptr_guarda`](../casos/umap/erase_begin.md#f_umap_erase_begin_ptr_guarda) | `umap` | `erase_begin` | `ptr` | `guarda` |
| [`f_umap_erase_begin_ptr_bucle`](../casos/umap/erase_begin.md#f_umap_erase_begin_ptr_bucle) | `umap` | `erase_begin` | `ptr` | `bucle` |
| [`f_umap_erase_begin_ptr_llamada`](../casos/umap/erase_begin.md#f_umap_erase_begin_ptr_llamada) | `umap` | `erase_begin` | `ptr` | `llamada` |
| [`f_umap_clear_ref_recto`](../casos/umap/clear.md#f_umap_clear_ref_recto) | `umap` | `clear` | `ref` | `recto` |
| [`f_umap_clear_ref_guarda`](../casos/umap/clear.md#f_umap_clear_ref_guarda) | `umap` | `clear` | `ref` | `guarda` |
| [`f_umap_clear_ref_bucle`](../casos/umap/clear.md#f_umap_clear_ref_bucle) | `umap` | `clear` | `ref` | `bucle` |
| [`f_umap_clear_ref_llamada`](../casos/umap/clear.md#f_umap_clear_ref_llamada) | `umap` | `clear` | `ref` | `llamada` |
| [`f_umap_clear_ptr_recto`](../casos/umap/clear.md#f_umap_clear_ptr_recto) | `umap` | `clear` | `ptr` | `recto` |
| [`f_umap_clear_ptr_guarda`](../casos/umap/clear.md#f_umap_clear_ptr_guarda) | `umap` | `clear` | `ptr` | `guarda` |
| [`f_umap_clear_ptr_bucle`](../casos/umap/clear.md#f_umap_clear_ptr_bucle) | `umap` | `clear` | `ptr` | `bucle` |
| [`f_umap_clear_ptr_llamada`](../casos/umap/clear.md#f_umap_clear_ptr_llamada) | `umap` | `clear` | `ptr` | `llamada` |
| [`f_umap_rehash_ref_bucle`](../casos/umap/rehash.md#f_umap_rehash_ref_bucle) | `umap` | `rehash` | `ref` | `bucle` |
| [`f_umap_rehash_ptr_bucle`](../casos/umap/rehash.md#f_umap_rehash_ptr_bucle) | `umap` | `rehash` | `ptr` | `bucle` |
## 2. Sin comparacion previa contra end(), el modelado no se activa

5 casos.

| Caso | Contenedor | Operación | Sostiene | Forma |
|---|---|---|---|---|
| [`f_deque_resize_grow_it_recto`](../casos/deque/resize_grow.md#f_deque_resize_grow_it_recto) | `deque` | `resize_grow` | `it` | `recto` |
| [`f_flist_erase_after_it_recto`](../casos/flist/erase_after.md#f_flist_erase_after_it_recto) | `flist` | `erase_after` | `it` | `recto` |
| [`f_uset_rehash_it_recto`](../casos/uset/rehash.md#f_uset_rehash_it_recto) | `uset` | `rehash` | `it` | `recto` |
| [`f_uset_reserve_it_recto`](../casos/uset/reserve.md#f_uset_reserve_it_recto) | `uset` | `reserve` | `it` | `recto` |
| [`f_umap_rehash_it_recto`](../casos/umap/rehash.md#f_umap_rehash_it_recto) | `umap` | `rehash` | `it` | `recto` |
## 3. Se invalida por identidad del iterador, no por posicion

3 casos.

| Caso | Contenedor | Operación | Sostiene | Forma |
|---|---|---|---|---|
| [`f_vector_pop_back_it_bucle`](../casos/vector/pop_back.md#f_vector_pop_back_it_bucle) | `vector` | `pop_back` | `it` | `bucle` |
| [`f_flist_erase_after_it_guarda`](../casos/flist/erase_after.md#f_flist_erase_after_it_guarda) | `flist` | `erase_after` | `it` | `guarda` |
| [`f_flist_erase_after_it_llamada`](../casos/flist/erase_after.md#f_flist_erase_after_it_llamada) | `flist` | `erase_after` | `it` | `llamada` |
## 4. La invalidacion por insercion/realojamiento no esta modelada

20 casos.

| Caso | Contenedor | Operación | Sostiene | Forma |
|---|---|---|---|---|
| [`f_vector_push_back_it_bucle`](../casos/vector/push_back.md#f_vector_push_back_it_bucle) | `vector` | `push_back` | `it` | `bucle` |
| [`f_vector_emplace_back_it_bucle`](../casos/vector/emplace_back.md#f_vector_emplace_back_it_bucle) | `vector` | `emplace_back` | `it` | `bucle` |
| [`f_vector_insert_end_it_bucle`](../casos/vector/insert_end.md#f_vector_insert_end_it_bucle) | `vector` | `insert_end` | `it` | `bucle` |
| [`f_vector_resize_grow_it_bucle`](../casos/vector/resize_grow.md#f_vector_resize_grow_it_bucle) | `vector` | `resize_grow` | `it` | `bucle` |
| [`f_vector_reserve_it_bucle`](../casos/vector/reserve.md#f_vector_reserve_it_bucle) | `vector` | `reserve` | `it` | `bucle` |
| [`f_deque_resize_grow_it_guarda`](../casos/deque/resize_grow.md#f_deque_resize_grow_it_guarda) | `deque` | `resize_grow` | `it` | `guarda` |
| [`f_deque_resize_grow_it_bucle`](../casos/deque/resize_grow.md#f_deque_resize_grow_it_bucle) | `deque` | `resize_grow` | `it` | `bucle` |
| [`f_deque_resize_grow_it_llamada`](../casos/deque/resize_grow.md#f_deque_resize_grow_it_llamada) | `deque` | `resize_grow` | `it` | `llamada` |
| [`f_uset_insert_it_bucle`](../casos/uset/insert.md#f_uset_insert_it_bucle) | `uset` | `insert` | `it` | `bucle` |
| [`f_uset_rehash_it_guarda`](../casos/uset/rehash.md#f_uset_rehash_it_guarda) | `uset` | `rehash` | `it` | `guarda` |
| [`f_uset_rehash_it_bucle`](../casos/uset/rehash.md#f_uset_rehash_it_bucle) | `uset` | `rehash` | `it` | `bucle` |
| [`f_uset_rehash_it_llamada`](../casos/uset/rehash.md#f_uset_rehash_it_llamada) | `uset` | `rehash` | `it` | `llamada` |
| [`f_uset_reserve_it_guarda`](../casos/uset/reserve.md#f_uset_reserve_it_guarda) | `uset` | `reserve` | `it` | `guarda` |
| [`f_uset_reserve_it_bucle`](../casos/uset/reserve.md#f_uset_reserve_it_bucle) | `uset` | `reserve` | `it` | `bucle` |
| [`f_uset_reserve_it_llamada`](../casos/uset/reserve.md#f_uset_reserve_it_llamada) | `uset` | `reserve` | `it` | `llamada` |
| [`f_umap_insert_it_bucle`](../casos/umap/insert.md#f_umap_insert_it_bucle) | `umap` | `insert` | `it` | `bucle` |
| [`f_umap_subscript_it_bucle`](../casos/umap/subscript.md#f_umap_subscript_it_bucle) | `umap` | `subscript` | `it` | `bucle` |
| [`f_umap_rehash_it_guarda`](../casos/umap/rehash.md#f_umap_rehash_it_guarda) | `umap` | `rehash` | `it` | `guarda` |
| [`f_umap_rehash_it_bucle`](../casos/umap/rehash.md#f_umap_rehash_it_bucle) | `umap` | `rehash` | `it` | `bucle` |
| [`f_umap_rehash_it_llamada`](../casos/umap/rehash.md#f_umap_rehash_it_llamada) | `umap` | `rehash` | `it` | `llamada` |
