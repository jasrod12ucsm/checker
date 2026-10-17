
# Validación dinámica

Validación dinámica reproducible por escenarios; no sustituye el oráculo normativo.

- Casos base: **684**; ejecuciones: **759**
  (una por caso `UB`/`SAFE`, dos por caso `POLICY`).
- Timeout por ejecución: 1 s.
- Cobertura del protocolo: `COMPLETA`.

## Resumen por instrumento

| Instrumento | Detectado | Sin detección |
|---|---:|---:|
| libstdc++ Debug | 222 | 537 |
| ASan/UBSan | 279 | 480 |

## Por etiqueta normativa y escenario

| Etiqueta (modo) | Ejecuciones | libstdc++ Debug | ASan/UBSan | Alguno | Ninguno |
|---|---:|---:|---:|---:|---:|
| `UB` (natural) | 363 | 192 | 222 | 294 | 69 |
| `SAFE` (natural) | 246 | 0 | 0 | 0 | 246 |
| `POLICY` (force) | 75 | 30 | 57 | 66 | 9 |
| `POLICY` (preserve) | 75 | 0 | 0 | 0 | 75 |

Casos `SAFE` con alguna detección dinámica: **0**.

## Tipo de error observado

| Instrumento | Diagnóstico | Ejecuciones |
|---|---|---:|
| ASan/UBSan | `heap-use-after-free` | 279 |
| libstdc++ Debug | `attempt to dereference a singular iterator` | 150 |
| libstdc++ Debug | `attempt to increment a singular iterator` | 72 |

## Por contenedor (todas las ejecuciones)

| Contenedor | Ejecuciones | libstdc++ Debug | ASan/UBSan | Alguno | Ninguno |
|---|---:|---:|---:|---:|---:|
| `std::vector` | 198 | 66 | 75 | 102 | 96 |
| `std::deque` | 96 | 48 | 0 | 48 | 48 |
| `std::list` | 108 | 18 | 36 | 36 | 72 |
| `std::forward_list` | 48 | 12 | 24 | 24 | 24 |
| `std::set` | 48 | 12 | 24 | 24 | 24 |
| `std::multiset` | 36 | 12 | 24 | 24 | 12 |
| `std::map` | 60 | 12 | 24 | 24 | 36 |
| `std::multimap` | 36 | 12 | 24 | 24 | 12 |
| `std::unordered_set` | 63 | 15 | 24 | 27 | 36 |
| `std::unordered_map` | 66 | 15 | 24 | 27 | 39 |

## Casos `UB` por forma

| Forma | Ejecuciones | libstdc++ Debug | ASan/UBSan | Alguno | Ninguno |
|---|---:|---:|---:|---:|---:|
| `recto` | 82 | 29 | 51 | 63 | 19 |
| `guarda` | 82 | 29 | 51 | 63 | 19 |
| `bucle` | 117 | 105 | 69 | 105 | 12 |
| `llamada` | 82 | 29 | 51 | 63 | 19 |

## Casos `UB` por handle

| Sostiene | Ejecuciones | libstdc++ Debug | ASan/UBSan | Alguno | Ninguno |
|---|---:|---:|---:|---:|---:|
| `it` | 137 | 122 | 74 | 122 | 15 |
| `ref` | 113 | 35 | 74 | 86 | 27 |
| `ptr` | 113 | 35 | 74 | 86 | 27 |

## Cruce estático × dinámico (casos `UB`)

| | Dinámica detecta | Dinámica no detecta |
|---|---:|---:|
| **Estático avisa** | 109 | 0 |
| **Estático calla** | 185 | 69 |

Los 185 casos de la celda *estático calla / dinámica detecta* son
evidencia de que el defecto es real y observable, pero invisible para el
analizador estático.

<details>
<summary>Casos UB detectados solo dinámicamente (185)</summary>

- [`f_vector_push_back_it_bucle`](../casos/vector/push_back.md#f_vector_push_back_it_bucle)
- [`f_vector_push_back_ref_bucle`](../casos/vector/push_back.md#f_vector_push_back_ref_bucle)
- [`f_vector_push_back_ptr_bucle`](../casos/vector/push_back.md#f_vector_push_back_ptr_bucle)
- [`f_vector_emplace_back_it_bucle`](../casos/vector/emplace_back.md#f_vector_emplace_back_it_bucle)
- [`f_vector_emplace_back_ref_bucle`](../casos/vector/emplace_back.md#f_vector_emplace_back_ref_bucle)
- [`f_vector_emplace_back_ptr_bucle`](../casos/vector/emplace_back.md#f_vector_emplace_back_ptr_bucle)
- [`f_vector_insert_begin_ref_bucle`](../casos/vector/insert_begin.md#f_vector_insert_begin_ref_bucle)
- [`f_vector_insert_begin_ptr_bucle`](../casos/vector/insert_begin.md#f_vector_insert_begin_ptr_bucle)
- [`f_vector_insert_end_it_bucle`](../casos/vector/insert_end.md#f_vector_insert_end_it_bucle)
- [`f_vector_insert_end_ref_bucle`](../casos/vector/insert_end.md#f_vector_insert_end_ref_bucle)
- [`f_vector_insert_end_ptr_bucle`](../casos/vector/insert_end.md#f_vector_insert_end_ptr_bucle)
- [`f_vector_erase_begin_ref_bucle`](../casos/vector/erase_begin.md#f_vector_erase_begin_ref_bucle)
- [`f_vector_erase_begin_ptr_bucle`](../casos/vector/erase_begin.md#f_vector_erase_begin_ptr_bucle)
- [`f_vector_clear_ref_bucle`](../casos/vector/clear.md#f_vector_clear_ref_bucle)
- [`f_vector_clear_ptr_bucle`](../casos/vector/clear.md#f_vector_clear_ptr_bucle)
- [`f_vector_resize_grow_it_bucle`](../casos/vector/resize_grow.md#f_vector_resize_grow_it_bucle)
- [`f_vector_resize_grow_ref_bucle`](../casos/vector/resize_grow.md#f_vector_resize_grow_ref_bucle)
- [`f_vector_resize_grow_ptr_bucle`](../casos/vector/resize_grow.md#f_vector_resize_grow_ptr_bucle)
- [`f_vector_reserve_it_bucle`](../casos/vector/reserve.md#f_vector_reserve_it_bucle)
- [`f_vector_reserve_ref_bucle`](../casos/vector/reserve.md#f_vector_reserve_ref_bucle)
- [`f_vector_reserve_ptr_bucle`](../casos/vector/reserve.md#f_vector_reserve_ptr_bucle)
- [`f_vector_assign_ref_bucle`](../casos/vector/assign.md#f_vector_assign_ref_bucle)
- [`f_vector_assign_ptr_bucle`](../casos/vector/assign.md#f_vector_assign_ptr_bucle)
- [`f_vector_pop_back_it_bucle`](../casos/vector/pop_back.md#f_vector_pop_back_it_bucle)
- [`f_vector_pop_back_ref_bucle`](../casos/vector/pop_back.md#f_vector_pop_back_ref_bucle)
- [`f_vector_pop_back_ptr_bucle`](../casos/vector/pop_back.md#f_vector_pop_back_ptr_bucle)
- [`f_deque_push_back_ref_bucle`](../casos/deque/push_back.md#f_deque_push_back_ref_bucle)
- [`f_deque_push_back_ptr_bucle`](../casos/deque/push_back.md#f_deque_push_back_ptr_bucle)
- [`f_deque_push_front_ref_bucle`](../casos/deque/push_front.md#f_deque_push_front_ref_bucle)
- [`f_deque_push_front_ptr_bucle`](../casos/deque/push_front.md#f_deque_push_front_ptr_bucle)
- [`f_deque_emplace_back_ref_bucle`](../casos/deque/emplace_back.md#f_deque_emplace_back_ref_bucle)
- [`f_deque_emplace_back_ptr_bucle`](../casos/deque/emplace_back.md#f_deque_emplace_back_ptr_bucle)
- [`f_deque_insert_middle_ref_bucle`](../casos/deque/insert_middle.md#f_deque_insert_middle_ref_bucle)
- [`f_deque_insert_middle_ptr_bucle`](../casos/deque/insert_middle.md#f_deque_insert_middle_ptr_bucle)
- [`f_deque_erase_begin_ref_bucle`](../casos/deque/erase_begin.md#f_deque_erase_begin_ref_bucle)
- [`f_deque_erase_begin_ptr_bucle`](../casos/deque/erase_begin.md#f_deque_erase_begin_ptr_bucle)
- [`f_deque_clear_ref_bucle`](../casos/deque/clear.md#f_deque_clear_ref_bucle)
- [`f_deque_clear_ptr_bucle`](../casos/deque/clear.md#f_deque_clear_ptr_bucle)
- [`f_deque_resize_grow_it_recto`](../casos/deque/resize_grow.md#f_deque_resize_grow_it_recto)
- [`f_deque_resize_grow_it_guarda`](../casos/deque/resize_grow.md#f_deque_resize_grow_it_guarda)
- [`f_deque_resize_grow_it_bucle`](../casos/deque/resize_grow.md#f_deque_resize_grow_it_bucle)
- [`f_deque_resize_grow_it_llamada`](../casos/deque/resize_grow.md#f_deque_resize_grow_it_llamada)
- [`f_deque_resize_grow_ref_bucle`](../casos/deque/resize_grow.md#f_deque_resize_grow_ref_bucle)
- [`f_deque_resize_grow_ptr_bucle`](../casos/deque/resize_grow.md#f_deque_resize_grow_ptr_bucle)
- [`f_deque_pop_front_ref_bucle`](../casos/deque/pop_front.md#f_deque_pop_front_ref_bucle)
- [`f_deque_pop_front_ptr_bucle`](../casos/deque/pop_front.md#f_deque_pop_front_ptr_bucle)
- [`f_list_erase_begin_ref_recto`](../casos/list/erase_begin.md#f_list_erase_begin_ref_recto)
- [`f_list_erase_begin_ref_guarda`](../casos/list/erase_begin.md#f_list_erase_begin_ref_guarda)
- [`f_list_erase_begin_ref_bucle`](../casos/list/erase_begin.md#f_list_erase_begin_ref_bucle)
- [`f_list_erase_begin_ref_llamada`](../casos/list/erase_begin.md#f_list_erase_begin_ref_llamada)
- [`f_list_erase_begin_ptr_recto`](../casos/list/erase_begin.md#f_list_erase_begin_ptr_recto)
- [`f_list_erase_begin_ptr_guarda`](../casos/list/erase_begin.md#f_list_erase_begin_ptr_guarda)
- [`f_list_erase_begin_ptr_bucle`](../casos/list/erase_begin.md#f_list_erase_begin_ptr_bucle)
- [`f_list_erase_begin_ptr_llamada`](../casos/list/erase_begin.md#f_list_erase_begin_ptr_llamada)
- [`f_list_clear_ref_recto`](../casos/list/clear.md#f_list_clear_ref_recto)
- [`f_list_clear_ref_guarda`](../casos/list/clear.md#f_list_clear_ref_guarda)
- [`f_list_clear_ref_bucle`](../casos/list/clear.md#f_list_clear_ref_bucle)
- [`f_list_clear_ref_llamada`](../casos/list/clear.md#f_list_clear_ref_llamada)
- [`f_list_clear_ptr_recto`](../casos/list/clear.md#f_list_clear_ptr_recto)
- [`f_list_clear_ptr_guarda`](../casos/list/clear.md#f_list_clear_ptr_guarda)
- [`f_list_clear_ptr_bucle`](../casos/list/clear.md#f_list_clear_ptr_bucle)
- [`f_list_clear_ptr_llamada`](../casos/list/clear.md#f_list_clear_ptr_llamada)
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
- [`f_flist_erase_after_it_llamada`](../casos/flist/erase_after.md#f_flist_erase_after_it_llamada)
- [`f_flist_erase_after_ref_recto`](../casos/flist/erase_after.md#f_flist_erase_after_ref_recto)
- [`f_flist_erase_after_ref_guarda`](../casos/flist/erase_after.md#f_flist_erase_after_ref_guarda)
- [`f_flist_erase_after_ref_bucle`](../casos/flist/erase_after.md#f_flist_erase_after_ref_bucle)
- [`f_flist_erase_after_ref_llamada`](../casos/flist/erase_after.md#f_flist_erase_after_ref_llamada)
- [`f_flist_erase_after_ptr_recto`](../casos/flist/erase_after.md#f_flist_erase_after_ptr_recto)
- [`f_flist_erase_after_ptr_guarda`](../casos/flist/erase_after.md#f_flist_erase_after_ptr_guarda)
- [`f_flist_erase_after_ptr_bucle`](../casos/flist/erase_after.md#f_flist_erase_after_ptr_bucle)
- [`f_flist_erase_after_ptr_llamada`](../casos/flist/erase_after.md#f_flist_erase_after_ptr_llamada)
- [`f_flist_clear_ref_recto`](../casos/flist/clear.md#f_flist_clear_ref_recto)
- [`f_flist_clear_ref_guarda`](../casos/flist/clear.md#f_flist_clear_ref_guarda)
- [`f_flist_clear_ref_bucle`](../casos/flist/clear.md#f_flist_clear_ref_bucle)
- [`f_flist_clear_ref_llamada`](../casos/flist/clear.md#f_flist_clear_ref_llamada)
- [`f_flist_clear_ptr_recto`](../casos/flist/clear.md#f_flist_clear_ptr_recto)
- [`f_flist_clear_ptr_guarda`](../casos/flist/clear.md#f_flist_clear_ptr_guarda)
- [`f_flist_clear_ptr_bucle`](../casos/flist/clear.md#f_flist_clear_ptr_bucle)
- [`f_flist_clear_ptr_llamada`](../casos/flist/clear.md#f_flist_clear_ptr_llamada)
- [`f_set_erase_begin_ref_recto`](../casos/set/erase_begin.md#f_set_erase_begin_ref_recto)
- [`f_set_erase_begin_ref_guarda`](../casos/set/erase_begin.md#f_set_erase_begin_ref_guarda)
- [`f_set_erase_begin_ref_bucle`](../casos/set/erase_begin.md#f_set_erase_begin_ref_bucle)
- [`f_set_erase_begin_ref_llamada`](../casos/set/erase_begin.md#f_set_erase_begin_ref_llamada)
- [`f_set_erase_begin_ptr_recto`](../casos/set/erase_begin.md#f_set_erase_begin_ptr_recto)
- [`f_set_erase_begin_ptr_guarda`](../casos/set/erase_begin.md#f_set_erase_begin_ptr_guarda)
- [`f_set_erase_begin_ptr_bucle`](../casos/set/erase_begin.md#f_set_erase_begin_ptr_bucle)
- [`f_set_erase_begin_ptr_llamada`](../casos/set/erase_begin.md#f_set_erase_begin_ptr_llamada)
- [`f_set_clear_ref_recto`](../casos/set/clear.md#f_set_clear_ref_recto)
- [`f_set_clear_ref_guarda`](../casos/set/clear.md#f_set_clear_ref_guarda)
- [`f_set_clear_ref_bucle`](../casos/set/clear.md#f_set_clear_ref_bucle)
- [`f_set_clear_ref_llamada`](../casos/set/clear.md#f_set_clear_ref_llamada)
- [`f_set_clear_ptr_recto`](../casos/set/clear.md#f_set_clear_ptr_recto)
- [`f_set_clear_ptr_guarda`](../casos/set/clear.md#f_set_clear_ptr_guarda)
- [`f_set_clear_ptr_bucle`](../casos/set/clear.md#f_set_clear_ptr_bucle)
- [`f_set_clear_ptr_llamada`](../casos/set/clear.md#f_set_clear_ptr_llamada)
- [`f_mset_erase_begin_ref_recto`](../casos/mset/erase_begin.md#f_mset_erase_begin_ref_recto)
- [`f_mset_erase_begin_ref_guarda`](../casos/mset/erase_begin.md#f_mset_erase_begin_ref_guarda)
- [`f_mset_erase_begin_ref_bucle`](../casos/mset/erase_begin.md#f_mset_erase_begin_ref_bucle)
- [`f_mset_erase_begin_ref_llamada`](../casos/mset/erase_begin.md#f_mset_erase_begin_ref_llamada)
- [`f_mset_erase_begin_ptr_recto`](../casos/mset/erase_begin.md#f_mset_erase_begin_ptr_recto)
- [`f_mset_erase_begin_ptr_guarda`](../casos/mset/erase_begin.md#f_mset_erase_begin_ptr_guarda)
- [`f_mset_erase_begin_ptr_bucle`](../casos/mset/erase_begin.md#f_mset_erase_begin_ptr_bucle)
- [`f_mset_erase_begin_ptr_llamada`](../casos/mset/erase_begin.md#f_mset_erase_begin_ptr_llamada)
- [`f_mset_clear_ref_recto`](../casos/mset/clear.md#f_mset_clear_ref_recto)
- [`f_mset_clear_ref_guarda`](../casos/mset/clear.md#f_mset_clear_ref_guarda)
- [`f_mset_clear_ref_bucle`](../casos/mset/clear.md#f_mset_clear_ref_bucle)
- [`f_mset_clear_ref_llamada`](../casos/mset/clear.md#f_mset_clear_ref_llamada)
- [`f_mset_clear_ptr_recto`](../casos/mset/clear.md#f_mset_clear_ptr_recto)
- [`f_mset_clear_ptr_guarda`](../casos/mset/clear.md#f_mset_clear_ptr_guarda)
- [`f_mset_clear_ptr_bucle`](../casos/mset/clear.md#f_mset_clear_ptr_bucle)
- [`f_mset_clear_ptr_llamada`](../casos/mset/clear.md#f_mset_clear_ptr_llamada)
- [`f_map_erase_begin_ref_recto`](../casos/map/erase_begin.md#f_map_erase_begin_ref_recto)
- [`f_map_erase_begin_ref_guarda`](../casos/map/erase_begin.md#f_map_erase_begin_ref_guarda)
- [`f_map_erase_begin_ref_bucle`](../casos/map/erase_begin.md#f_map_erase_begin_ref_bucle)
- [`f_map_erase_begin_ref_llamada`](../casos/map/erase_begin.md#f_map_erase_begin_ref_llamada)
- [`f_map_erase_begin_ptr_recto`](../casos/map/erase_begin.md#f_map_erase_begin_ptr_recto)
- [`f_map_erase_begin_ptr_guarda`](../casos/map/erase_begin.md#f_map_erase_begin_ptr_guarda)
- [`f_map_erase_begin_ptr_bucle`](../casos/map/erase_begin.md#f_map_erase_begin_ptr_bucle)
- [`f_map_erase_begin_ptr_llamada`](../casos/map/erase_begin.md#f_map_erase_begin_ptr_llamada)
- [`f_map_clear_ref_recto`](../casos/map/clear.md#f_map_clear_ref_recto)
- [`f_map_clear_ref_guarda`](../casos/map/clear.md#f_map_clear_ref_guarda)
- [`f_map_clear_ref_bucle`](../casos/map/clear.md#f_map_clear_ref_bucle)
- [`f_map_clear_ref_llamada`](../casos/map/clear.md#f_map_clear_ref_llamada)
- [`f_map_clear_ptr_recto`](../casos/map/clear.md#f_map_clear_ptr_recto)
- [`f_map_clear_ptr_guarda`](../casos/map/clear.md#f_map_clear_ptr_guarda)
- [`f_map_clear_ptr_bucle`](../casos/map/clear.md#f_map_clear_ptr_bucle)
- [`f_map_clear_ptr_llamada`](../casos/map/clear.md#f_map_clear_ptr_llamada)
- [`f_mmap_erase_begin_ref_recto`](../casos/mmap/erase_begin.md#f_mmap_erase_begin_ref_recto)
- [`f_mmap_erase_begin_ref_guarda`](../casos/mmap/erase_begin.md#f_mmap_erase_begin_ref_guarda)
- [`f_mmap_erase_begin_ref_bucle`](../casos/mmap/erase_begin.md#f_mmap_erase_begin_ref_bucle)
- [`f_mmap_erase_begin_ref_llamada`](../casos/mmap/erase_begin.md#f_mmap_erase_begin_ref_llamada)
- [`f_mmap_erase_begin_ptr_recto`](../casos/mmap/erase_begin.md#f_mmap_erase_begin_ptr_recto)
- [`f_mmap_erase_begin_ptr_guarda`](../casos/mmap/erase_begin.md#f_mmap_erase_begin_ptr_guarda)
- [`f_mmap_erase_begin_ptr_bucle`](../casos/mmap/erase_begin.md#f_mmap_erase_begin_ptr_bucle)
- [`f_mmap_erase_begin_ptr_llamada`](../casos/mmap/erase_begin.md#f_mmap_erase_begin_ptr_llamada)
- [`f_mmap_clear_ref_recto`](../casos/mmap/clear.md#f_mmap_clear_ref_recto)
- [`f_mmap_clear_ref_guarda`](../casos/mmap/clear.md#f_mmap_clear_ref_guarda)
- [`f_mmap_clear_ref_bucle`](../casos/mmap/clear.md#f_mmap_clear_ref_bucle)
- [`f_mmap_clear_ref_llamada`](../casos/mmap/clear.md#f_mmap_clear_ref_llamada)
- [`f_mmap_clear_ptr_recto`](../casos/mmap/clear.md#f_mmap_clear_ptr_recto)
- [`f_mmap_clear_ptr_guarda`](../casos/mmap/clear.md#f_mmap_clear_ptr_guarda)
- [`f_mmap_clear_ptr_bucle`](../casos/mmap/clear.md#f_mmap_clear_ptr_bucle)
- [`f_mmap_clear_ptr_llamada`](../casos/mmap/clear.md#f_mmap_clear_ptr_llamada)
- [`f_uset_erase_begin_ref_recto`](../casos/uset/erase_begin.md#f_uset_erase_begin_ref_recto)
- [`f_uset_erase_begin_ref_guarda`](../casos/uset/erase_begin.md#f_uset_erase_begin_ref_guarda)
- [`f_uset_erase_begin_ref_bucle`](../casos/uset/erase_begin.md#f_uset_erase_begin_ref_bucle)
- [`f_uset_erase_begin_ref_llamada`](../casos/uset/erase_begin.md#f_uset_erase_begin_ref_llamada)
- [`f_uset_erase_begin_ptr_recto`](../casos/uset/erase_begin.md#f_uset_erase_begin_ptr_recto)
- [`f_uset_erase_begin_ptr_guarda`](../casos/uset/erase_begin.md#f_uset_erase_begin_ptr_guarda)
- [`f_uset_erase_begin_ptr_bucle`](../casos/uset/erase_begin.md#f_uset_erase_begin_ptr_bucle)
- [`f_uset_erase_begin_ptr_llamada`](../casos/uset/erase_begin.md#f_uset_erase_begin_ptr_llamada)
- [`f_uset_clear_ref_recto`](../casos/uset/clear.md#f_uset_clear_ref_recto)
- [`f_uset_clear_ref_guarda`](../casos/uset/clear.md#f_uset_clear_ref_guarda)
- [`f_uset_clear_ref_bucle`](../casos/uset/clear.md#f_uset_clear_ref_bucle)
- [`f_uset_clear_ref_llamada`](../casos/uset/clear.md#f_uset_clear_ref_llamada)
- [`f_uset_clear_ptr_recto`](../casos/uset/clear.md#f_uset_clear_ptr_recto)
- [`f_uset_clear_ptr_guarda`](../casos/uset/clear.md#f_uset_clear_ptr_guarda)
- [`f_uset_clear_ptr_bucle`](../casos/uset/clear.md#f_uset_clear_ptr_bucle)
- [`f_uset_clear_ptr_llamada`](../casos/uset/clear.md#f_uset_clear_ptr_llamada)
- [`f_umap_erase_begin_ref_recto`](../casos/umap/erase_begin.md#f_umap_erase_begin_ref_recto)
- [`f_umap_erase_begin_ref_guarda`](../casos/umap/erase_begin.md#f_umap_erase_begin_ref_guarda)
- [`f_umap_erase_begin_ref_bucle`](../casos/umap/erase_begin.md#f_umap_erase_begin_ref_bucle)
- [`f_umap_erase_begin_ref_llamada`](../casos/umap/erase_begin.md#f_umap_erase_begin_ref_llamada)
- [`f_umap_erase_begin_ptr_recto`](../casos/umap/erase_begin.md#f_umap_erase_begin_ptr_recto)
- [`f_umap_erase_begin_ptr_guarda`](../casos/umap/erase_begin.md#f_umap_erase_begin_ptr_guarda)
- [`f_umap_erase_begin_ptr_bucle`](../casos/umap/erase_begin.md#f_umap_erase_begin_ptr_bucle)
- [`f_umap_erase_begin_ptr_llamada`](../casos/umap/erase_begin.md#f_umap_erase_begin_ptr_llamada)
- [`f_umap_clear_ref_recto`](../casos/umap/clear.md#f_umap_clear_ref_recto)
- [`f_umap_clear_ref_guarda`](../casos/umap/clear.md#f_umap_clear_ref_guarda)
- [`f_umap_clear_ref_bucle`](../casos/umap/clear.md#f_umap_clear_ref_bucle)
- [`f_umap_clear_ref_llamada`](../casos/umap/clear.md#f_umap_clear_ref_llamada)
- [`f_umap_clear_ptr_recto`](../casos/umap/clear.md#f_umap_clear_ptr_recto)
- [`f_umap_clear_ptr_guarda`](../casos/umap/clear.md#f_umap_clear_ptr_guarda)
- [`f_umap_clear_ptr_bucle`](../casos/umap/clear.md#f_umap_clear_ptr_bucle)
- [`f_umap_clear_ptr_llamada`](../casos/umap/clear.md#f_umap_clear_ptr_llamada)

</details>

<details>
<summary>Casos UB sin manifestación dinámica en ningún instrumento (69)</summary>

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
- [`f_uset_insert_it_bucle`](../casos/uset/insert.md#f_uset_insert_it_bucle)
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
- [`f_umap_insert_it_bucle`](../casos/umap/insert.md#f_umap_insert_it_bucle)
- [`f_umap_subscript_it_bucle`](../casos/umap/subscript.md#f_umap_subscript_it_bucle)
- [`f_umap_rehash_it_recto`](../casos/umap/rehash.md#f_umap_rehash_it_recto)
- [`f_umap_rehash_it_guarda`](../casos/umap/rehash.md#f_umap_rehash_it_guarda)
- [`f_umap_rehash_it_bucle`](../casos/umap/rehash.md#f_umap_rehash_it_bucle)
- [`f_umap_rehash_it_llamada`](../casos/umap/rehash.md#f_umap_rehash_it_llamada)
- [`f_umap_rehash_ref_bucle`](../casos/umap/rehash.md#f_umap_rehash_ref_bucle)
- [`f_umap_rehash_ptr_bucle`](../casos/umap/rehash.md#f_umap_rehash_ptr_bucle)

</details>
