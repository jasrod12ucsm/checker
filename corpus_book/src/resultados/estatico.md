
# Análisis estático (Clang Static Analyzer)

## Totales

| Etiqueta | Casos | Con aviso | Sin aviso | Lectura |
|---|---:|---:|---:|---|
| 🔴 `UB` | 363 | 109 | 254 | cobertura **30.0%** |
| 🟢 `SAFE` | 246 | 0 | 246 | 0 falsos positivos |
| 🟡 `POLICY` | 75 | 0 | 75 | optimista: nunca avisa |

## UB detectados: forma × handle

Detectados / total de casos `UB` en cada celda.

| Forma \ Sostiene | iterador | referencia | puntero |
|---|---:|---:|---:|
| `recto` | 27/32 | 0/25 | 0/25 |
| `guarda` | 27/32 | 0/25 | 0/25 |
| `bucle` | 28/41 | 0/38 | 0/38 |
| `llamada` | 27/32 | 0/25 | 0/25 |

## Por forma sintáctica

| Valor | Casos | UB | Detectados | Falsos negativos | Cobertura | SAFE | Falsos positivos | POLICY con aviso |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `recto` | 171 | 82 | 27 | 55 | 32.9% | 65 | 0 | 0/24 |
| `guarda` | 171 | 82 | 27 | 55 | 32.9% | 65 | 0 | 0/24 |
| `bucle` | 171 | 117 | 28 | 89 | 23.9% | 51 | 0 | 0/3 |
| `llamada` | 171 | 82 | 27 | 55 | 32.9% | 65 | 0 | 0/24 |

## Por handle retenido

| Valor | Casos | UB | Detectados | Falsos negativos | Cobertura | SAFE | Falsos positivos | POLICY con aviso |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `it` (iterador) | 228 | 137 | 109 | 28 | 79.6% | 60 | 0 | 0/31 |
| `ref` (referencia) | 228 | 113 | 0 | 113 | 0.0% | 93 | 0 | 0/22 |
| `ptr` (puntero) | 228 | 113 | 0 | 113 | 0.0% | 93 | 0 | 0/22 |

## Por contenedor

| Valor | Casos | UB | Detectados | Falsos negativos | Cobertura | SAFE | Falsos positivos | POLICY con aviso |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| [`std::vector`](../casos/vector/index.md) | 132 | 66 | 16 | 50 | 24.2% | 0 | 0 | 0/66 |
| [`std::deque`](../casos/deque/index.md) | 96 | 72 | 28 | 44 | 38.9% | 24 | 0 | 0/0 |
| [`std::list`](../casos/list/index.md) | 108 | 36 | 12 | 24 | 33.3% | 72 | 0 | 0/0 |
| [`std::forward_list`](../casos/flist/index.md) | 48 | 24 | 5 | 19 | 20.8% | 24 | 0 | 0/0 |
| [`std::set`](../casos/set/index.md) | 48 | 24 | 8 | 16 | 33.3% | 24 | 0 | 0/0 |
| [`std::multiset`](../casos/mset/index.md) | 36 | 24 | 8 | 16 | 33.3% | 12 | 0 | 0/0 |
| [`std::map`](../casos/map/index.md) | 60 | 24 | 8 | 16 | 33.3% | 36 | 0 | 0/0 |
| [`std::multimap`](../casos/mmap/index.md) | 36 | 24 | 8 | 16 | 33.3% | 12 | 0 | 0/0 |
| [`std::unordered_set`](../casos/uset/index.md) | 60 | 37 | 8 | 29 | 21.6% | 20 | 0 | 0/3 |
| [`std::unordered_map`](../casos/umap/index.md) | 60 | 32 | 8 | 24 | 25.0% | 22 | 0 | 0/6 |

## Por operación

| Contenedor | Operación | UB | Detectados | Cobertura | SAFE | FP | POLICY |
|---|---|---:|---:|---:|---:|---:|---:|
| `vector` | [`push_back`](../casos/vector/push_back.md) | 3 | 0 | 0.0% | 0 | 0 | 9 |
| `vector` | [`emplace_back`](../casos/vector/emplace_back.md) | 3 | 0 | 0.0% | 0 | 0 | 9 |
| `vector` | [`insert_begin`](../casos/vector/insert_begin.md) | 12 | 4 | 33.3% | 0 | 0 | 0 |
| `vector` | [`insert_end`](../casos/vector/insert_end.md) | 3 | 0 | 0.0% | 0 | 0 | 9 |
| `vector` | [`erase_begin`](../casos/vector/erase_begin.md) | 12 | 4 | 33.3% | 0 | 0 | 0 |
| `vector` | [`clear`](../casos/vector/clear.md) | 12 | 4 | 33.3% | 0 | 0 | 0 |
| `vector` | [`resize_grow`](../casos/vector/resize_grow.md) | 3 | 0 | 0.0% | 0 | 0 | 9 |
| `vector` | [`reserve`](../casos/vector/reserve.md) | 3 | 0 | 0.0% | 0 | 0 | 9 |
| `vector` | [`shrink_to_fit`](../casos/vector/shrink_to_fit.md) | 0 | 0 | — | 0 | 0 | 12 |
| `vector` | [`assign`](../casos/vector/assign.md) | 12 | 4 | 33.3% | 0 | 0 | 0 |
| `vector` | [`pop_back`](../casos/vector/pop_back.md) | 3 | 0 | 0.0% | 0 | 0 | 9 |
| `deque` | [`push_back`](../casos/deque/push_back.md) | 6 | 4 | 66.7% | 6 | 0 | 0 |
| `deque` | [`push_front`](../casos/deque/push_front.md) | 6 | 4 | 66.7% | 6 | 0 | 0 |
| `deque` | [`emplace_back`](../casos/deque/emplace_back.md) | 6 | 4 | 66.7% | 6 | 0 | 0 |
| `deque` | [`insert_middle`](../casos/deque/insert_middle.md) | 12 | 4 | 33.3% | 0 | 0 | 0 |
| `deque` | [`erase_begin`](../casos/deque/erase_begin.md) | 12 | 4 | 33.3% | 0 | 0 | 0 |
| `deque` | [`clear`](../casos/deque/clear.md) | 12 | 4 | 33.3% | 0 | 0 | 0 |
| `deque` | [`resize_grow`](../casos/deque/resize_grow.md) | 6 | 0 | 0.0% | 6 | 0 | 0 |
| `deque` | [`pop_front`](../casos/deque/pop_front.md) | 12 | 4 | 33.3% | 0 | 0 | 0 |
| `list` | [`push_back`](../casos/list/push_back.md) | 0 | 0 | — | 12 | 0 | 0 |
| `list` | [`push_front`](../casos/list/push_front.md) | 0 | 0 | — | 12 | 0 | 0 |
| `list` | [`insert`](../casos/list/insert.md) | 0 | 0 | — | 12 | 0 | 0 |
| `list` | [`erase_begin`](../casos/list/erase_begin.md) | 12 | 4 | 33.3% | 0 | 0 | 0 |
| `list` | [`clear`](../casos/list/clear.md) | 12 | 4 | 33.3% | 0 | 0 | 0 |
| `list` | [`resize_grow`](../casos/list/resize_grow.md) | 0 | 0 | — | 12 | 0 | 0 |
| `list` | [`pop_front`](../casos/list/pop_front.md) | 12 | 4 | 33.3% | 0 | 0 | 0 |
| `list` | [`reverse`](../casos/list/reverse.md) | 0 | 0 | — | 12 | 0 | 0 |
| `list` | [`sort`](../casos/list/sort.md) | 0 | 0 | — | 12 | 0 | 0 |
| `flist` | [`push_front`](../casos/flist/push_front.md) | 0 | 0 | — | 12 | 0 | 0 |
| `flist` | [`insert_after`](../casos/flist/insert_after.md) | 0 | 0 | — | 12 | 0 | 0 |
| `flist` | [`erase_after`](../casos/flist/erase_after.md) | 12 | 1 | 8.3% | 0 | 0 | 0 |
| `flist` | [`clear`](../casos/flist/clear.md) | 12 | 4 | 33.3% | 0 | 0 | 0 |
| `set` | [`insert`](../casos/set/insert.md) | 0 | 0 | — | 12 | 0 | 0 |
| `set` | [`emplace`](../casos/set/emplace.md) | 0 | 0 | — | 12 | 0 | 0 |
| `set` | [`erase_begin`](../casos/set/erase_begin.md) | 12 | 4 | 33.3% | 0 | 0 | 0 |
| `set` | [`clear`](../casos/set/clear.md) | 12 | 4 | 33.3% | 0 | 0 | 0 |
| `mset` | [`insert`](../casos/mset/insert.md) | 0 | 0 | — | 12 | 0 | 0 |
| `mset` | [`erase_begin`](../casos/mset/erase_begin.md) | 12 | 4 | 33.3% | 0 | 0 | 0 |
| `mset` | [`clear`](../casos/mset/clear.md) | 12 | 4 | 33.3% | 0 | 0 | 0 |
| `map` | [`insert`](../casos/map/insert.md) | 0 | 0 | — | 12 | 0 | 0 |
| `map` | [`emplace`](../casos/map/emplace.md) | 0 | 0 | — | 12 | 0 | 0 |
| `map` | [`subscript`](../casos/map/subscript.md) | 0 | 0 | — | 12 | 0 | 0 |
| `map` | [`erase_begin`](../casos/map/erase_begin.md) | 12 | 4 | 33.3% | 0 | 0 | 0 |
| `map` | [`clear`](../casos/map/clear.md) | 12 | 4 | 33.3% | 0 | 0 | 0 |
| `mmap` | [`insert`](../casos/mmap/insert.md) | 0 | 0 | — | 12 | 0 | 0 |
| `mmap` | [`erase_begin`](../casos/mmap/erase_begin.md) | 12 | 4 | 33.3% | 0 | 0 | 0 |
| `mmap` | [`clear`](../casos/mmap/clear.md) | 12 | 4 | 33.3% | 0 | 0 | 0 |
| `uset` | [`insert`](../casos/uset/insert.md) | 1 | 0 | 0.0% | 8 | 0 | 3 |
| `uset` | [`erase_begin`](../casos/uset/erase_begin.md) | 12 | 4 | 33.3% | 0 | 0 | 0 |
| `uset` | [`clear`](../casos/uset/clear.md) | 12 | 4 | 33.3% | 0 | 0 | 0 |
| `uset` | [`rehash`](../casos/uset/rehash.md) | 6 | 0 | 0.0% | 6 | 0 | 0 |
| `uset` | [`reserve`](../casos/uset/reserve.md) | 6 | 0 | 0.0% | 6 | 0 | 0 |
| `umap` | [`insert`](../casos/umap/insert.md) | 1 | 0 | 0.0% | 8 | 0 | 3 |
| `umap` | [`subscript`](../casos/umap/subscript.md) | 1 | 0 | 0.0% | 8 | 0 | 3 |
| `umap` | [`erase_begin`](../casos/umap/erase_begin.md) | 12 | 4 | 33.3% | 0 | 0 | 0 |
| `umap` | [`clear`](../casos/umap/clear.md) | 12 | 4 | 33.3% | 0 | 0 | 0 |
| `umap` | [`rehash`](../casos/umap/rehash.md) | 6 | 0 | 0.0% | 6 | 0 | 0 |

## Casos detectados

Los 109 casos `UB` en los que el analizador emitió aviso:

- [`f_vector_insert_begin_it_recto`](../casos/vector/insert_begin.md#f_vector_insert_begin_it_recto)
- [`f_vector_insert_begin_it_guarda`](../casos/vector/insert_begin.md#f_vector_insert_begin_it_guarda)
- [`f_vector_insert_begin_it_bucle`](../casos/vector/insert_begin.md#f_vector_insert_begin_it_bucle)
- [`f_vector_insert_begin_it_llamada`](../casos/vector/insert_begin.md#f_vector_insert_begin_it_llamada)
- [`f_vector_erase_begin_it_recto`](../casos/vector/erase_begin.md#f_vector_erase_begin_it_recto)
- [`f_vector_erase_begin_it_guarda`](../casos/vector/erase_begin.md#f_vector_erase_begin_it_guarda)
- [`f_vector_erase_begin_it_bucle`](../casos/vector/erase_begin.md#f_vector_erase_begin_it_bucle)
- [`f_vector_erase_begin_it_llamada`](../casos/vector/erase_begin.md#f_vector_erase_begin_it_llamada)
- [`f_vector_clear_it_recto`](../casos/vector/clear.md#f_vector_clear_it_recto)
- [`f_vector_clear_it_guarda`](../casos/vector/clear.md#f_vector_clear_it_guarda)
- [`f_vector_clear_it_bucle`](../casos/vector/clear.md#f_vector_clear_it_bucle)
- [`f_vector_clear_it_llamada`](../casos/vector/clear.md#f_vector_clear_it_llamada)
- [`f_vector_assign_it_recto`](../casos/vector/assign.md#f_vector_assign_it_recto)
- [`f_vector_assign_it_guarda`](../casos/vector/assign.md#f_vector_assign_it_guarda)
- [`f_vector_assign_it_bucle`](../casos/vector/assign.md#f_vector_assign_it_bucle)
- [`f_vector_assign_it_llamada`](../casos/vector/assign.md#f_vector_assign_it_llamada)
- [`f_deque_push_back_it_recto`](../casos/deque/push_back.md#f_deque_push_back_it_recto)
- [`f_deque_push_back_it_guarda`](../casos/deque/push_back.md#f_deque_push_back_it_guarda)
- [`f_deque_push_back_it_bucle`](../casos/deque/push_back.md#f_deque_push_back_it_bucle)
- [`f_deque_push_back_it_llamada`](../casos/deque/push_back.md#f_deque_push_back_it_llamada)
- [`f_deque_push_front_it_recto`](../casos/deque/push_front.md#f_deque_push_front_it_recto)
- [`f_deque_push_front_it_guarda`](../casos/deque/push_front.md#f_deque_push_front_it_guarda)
- [`f_deque_push_front_it_bucle`](../casos/deque/push_front.md#f_deque_push_front_it_bucle)
- [`f_deque_push_front_it_llamada`](../casos/deque/push_front.md#f_deque_push_front_it_llamada)
- [`f_deque_emplace_back_it_recto`](../casos/deque/emplace_back.md#f_deque_emplace_back_it_recto)
- [`f_deque_emplace_back_it_guarda`](../casos/deque/emplace_back.md#f_deque_emplace_back_it_guarda)
- [`f_deque_emplace_back_it_bucle`](../casos/deque/emplace_back.md#f_deque_emplace_back_it_bucle)
- [`f_deque_emplace_back_it_llamada`](../casos/deque/emplace_back.md#f_deque_emplace_back_it_llamada)
- [`f_deque_insert_middle_it_recto`](../casos/deque/insert_middle.md#f_deque_insert_middle_it_recto)
- [`f_deque_insert_middle_it_guarda`](../casos/deque/insert_middle.md#f_deque_insert_middle_it_guarda)
- [`f_deque_insert_middle_it_bucle`](../casos/deque/insert_middle.md#f_deque_insert_middle_it_bucle)
- [`f_deque_insert_middle_it_llamada`](../casos/deque/insert_middle.md#f_deque_insert_middle_it_llamada)
- [`f_deque_erase_begin_it_recto`](../casos/deque/erase_begin.md#f_deque_erase_begin_it_recto)
- [`f_deque_erase_begin_it_guarda`](../casos/deque/erase_begin.md#f_deque_erase_begin_it_guarda)
- [`f_deque_erase_begin_it_bucle`](../casos/deque/erase_begin.md#f_deque_erase_begin_it_bucle)
- [`f_deque_erase_begin_it_llamada`](../casos/deque/erase_begin.md#f_deque_erase_begin_it_llamada)
- [`f_deque_clear_it_recto`](../casos/deque/clear.md#f_deque_clear_it_recto)
- [`f_deque_clear_it_guarda`](../casos/deque/clear.md#f_deque_clear_it_guarda)
- [`f_deque_clear_it_bucle`](../casos/deque/clear.md#f_deque_clear_it_bucle)
- [`f_deque_clear_it_llamada`](../casos/deque/clear.md#f_deque_clear_it_llamada)
- [`f_deque_pop_front_it_recto`](../casos/deque/pop_front.md#f_deque_pop_front_it_recto)
- [`f_deque_pop_front_it_guarda`](../casos/deque/pop_front.md#f_deque_pop_front_it_guarda)
- [`f_deque_pop_front_it_bucle`](../casos/deque/pop_front.md#f_deque_pop_front_it_bucle)
- [`f_deque_pop_front_it_llamada`](../casos/deque/pop_front.md#f_deque_pop_front_it_llamada)
- [`f_list_erase_begin_it_recto`](../casos/list/erase_begin.md#f_list_erase_begin_it_recto)
- [`f_list_erase_begin_it_guarda`](../casos/list/erase_begin.md#f_list_erase_begin_it_guarda)
- [`f_list_erase_begin_it_bucle`](../casos/list/erase_begin.md#f_list_erase_begin_it_bucle)
- [`f_list_erase_begin_it_llamada`](../casos/list/erase_begin.md#f_list_erase_begin_it_llamada)
- [`f_list_clear_it_recto`](../casos/list/clear.md#f_list_clear_it_recto)
- [`f_list_clear_it_guarda`](../casos/list/clear.md#f_list_clear_it_guarda)
- [`f_list_clear_it_bucle`](../casos/list/clear.md#f_list_clear_it_bucle)
- [`f_list_clear_it_llamada`](../casos/list/clear.md#f_list_clear_it_llamada)
- [`f_list_pop_front_it_recto`](../casos/list/pop_front.md#f_list_pop_front_it_recto)
- [`f_list_pop_front_it_guarda`](../casos/list/pop_front.md#f_list_pop_front_it_guarda)
- [`f_list_pop_front_it_bucle`](../casos/list/pop_front.md#f_list_pop_front_it_bucle)
- [`f_list_pop_front_it_llamada`](../casos/list/pop_front.md#f_list_pop_front_it_llamada)
- [`f_flist_erase_after_it_bucle`](../casos/flist/erase_after.md#f_flist_erase_after_it_bucle)
- [`f_flist_clear_it_recto`](../casos/flist/clear.md#f_flist_clear_it_recto)
- [`f_flist_clear_it_guarda`](../casos/flist/clear.md#f_flist_clear_it_guarda)
- [`f_flist_clear_it_bucle`](../casos/flist/clear.md#f_flist_clear_it_bucle)
- [`f_flist_clear_it_llamada`](../casos/flist/clear.md#f_flist_clear_it_llamada)
- [`f_set_erase_begin_it_recto`](../casos/set/erase_begin.md#f_set_erase_begin_it_recto)
- [`f_set_erase_begin_it_guarda`](../casos/set/erase_begin.md#f_set_erase_begin_it_guarda)
- [`f_set_erase_begin_it_bucle`](../casos/set/erase_begin.md#f_set_erase_begin_it_bucle)
- [`f_set_erase_begin_it_llamada`](../casos/set/erase_begin.md#f_set_erase_begin_it_llamada)
- [`f_set_clear_it_recto`](../casos/set/clear.md#f_set_clear_it_recto)
- [`f_set_clear_it_guarda`](../casos/set/clear.md#f_set_clear_it_guarda)
- [`f_set_clear_it_bucle`](../casos/set/clear.md#f_set_clear_it_bucle)
- [`f_set_clear_it_llamada`](../casos/set/clear.md#f_set_clear_it_llamada)
- [`f_mset_erase_begin_it_recto`](../casos/mset/erase_begin.md#f_mset_erase_begin_it_recto)
- [`f_mset_erase_begin_it_guarda`](../casos/mset/erase_begin.md#f_mset_erase_begin_it_guarda)
- [`f_mset_erase_begin_it_bucle`](../casos/mset/erase_begin.md#f_mset_erase_begin_it_bucle)
- [`f_mset_erase_begin_it_llamada`](../casos/mset/erase_begin.md#f_mset_erase_begin_it_llamada)
- [`f_mset_clear_it_recto`](../casos/mset/clear.md#f_mset_clear_it_recto)
- [`f_mset_clear_it_guarda`](../casos/mset/clear.md#f_mset_clear_it_guarda)
- [`f_mset_clear_it_bucle`](../casos/mset/clear.md#f_mset_clear_it_bucle)
- [`f_mset_clear_it_llamada`](../casos/mset/clear.md#f_mset_clear_it_llamada)
- [`f_map_erase_begin_it_recto`](../casos/map/erase_begin.md#f_map_erase_begin_it_recto)
- [`f_map_erase_begin_it_guarda`](../casos/map/erase_begin.md#f_map_erase_begin_it_guarda)
- [`f_map_erase_begin_it_bucle`](../casos/map/erase_begin.md#f_map_erase_begin_it_bucle)
- [`f_map_erase_begin_it_llamada`](../casos/map/erase_begin.md#f_map_erase_begin_it_llamada)
- [`f_map_clear_it_recto`](../casos/map/clear.md#f_map_clear_it_recto)
- [`f_map_clear_it_guarda`](../casos/map/clear.md#f_map_clear_it_guarda)
- [`f_map_clear_it_bucle`](../casos/map/clear.md#f_map_clear_it_bucle)
- [`f_map_clear_it_llamada`](../casos/map/clear.md#f_map_clear_it_llamada)
- [`f_mmap_erase_begin_it_recto`](../casos/mmap/erase_begin.md#f_mmap_erase_begin_it_recto)
- [`f_mmap_erase_begin_it_guarda`](../casos/mmap/erase_begin.md#f_mmap_erase_begin_it_guarda)
- [`f_mmap_erase_begin_it_bucle`](../casos/mmap/erase_begin.md#f_mmap_erase_begin_it_bucle)
- [`f_mmap_erase_begin_it_llamada`](../casos/mmap/erase_begin.md#f_mmap_erase_begin_it_llamada)
- [`f_mmap_clear_it_recto`](../casos/mmap/clear.md#f_mmap_clear_it_recto)
- [`f_mmap_clear_it_guarda`](../casos/mmap/clear.md#f_mmap_clear_it_guarda)
- [`f_mmap_clear_it_bucle`](../casos/mmap/clear.md#f_mmap_clear_it_bucle)
- [`f_mmap_clear_it_llamada`](../casos/mmap/clear.md#f_mmap_clear_it_llamada)
- [`f_uset_erase_begin_it_recto`](../casos/uset/erase_begin.md#f_uset_erase_begin_it_recto)
- [`f_uset_erase_begin_it_guarda`](../casos/uset/erase_begin.md#f_uset_erase_begin_it_guarda)
- [`f_uset_erase_begin_it_bucle`](../casos/uset/erase_begin.md#f_uset_erase_begin_it_bucle)
- [`f_uset_erase_begin_it_llamada`](../casos/uset/erase_begin.md#f_uset_erase_begin_it_llamada)
- [`f_uset_clear_it_recto`](../casos/uset/clear.md#f_uset_clear_it_recto)
- [`f_uset_clear_it_guarda`](../casos/uset/clear.md#f_uset_clear_it_guarda)
- [`f_uset_clear_it_bucle`](../casos/uset/clear.md#f_uset_clear_it_bucle)
- [`f_uset_clear_it_llamada`](../casos/uset/clear.md#f_uset_clear_it_llamada)
- [`f_umap_erase_begin_it_recto`](../casos/umap/erase_begin.md#f_umap_erase_begin_it_recto)
- [`f_umap_erase_begin_it_guarda`](../casos/umap/erase_begin.md#f_umap_erase_begin_it_guarda)
- [`f_umap_erase_begin_it_bucle`](../casos/umap/erase_begin.md#f_umap_erase_begin_it_bucle)
- [`f_umap_erase_begin_it_llamada`](../casos/umap/erase_begin.md#f_umap_erase_begin_it_llamada)
- [`f_umap_clear_it_recto`](../casos/umap/clear.md#f_umap_clear_it_recto)
- [`f_umap_clear_it_guarda`](../casos/umap/clear.md#f_umap_clear_it_guarda)
- [`f_umap_clear_it_bucle`](../casos/umap/clear.md#f_umap_clear_it_bucle)
- [`f_umap_clear_it_llamada`](../casos/umap/clear.md#f_umap_clear_it_llamada)
