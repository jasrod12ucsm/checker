
# Análisis estático (Clang Static Analyzer)

## Totales

| Etiqueta | Casos | Con aviso | Sin aviso | Lectura |
|---|---:|---:|---:|---|
| 🔴 `UB` | 342 | 80 | 262 | cobertura **23.4%** |
| 🟢 `SAFE` | 306 | 0 | 306 | 0 falsos positivos |
| 🟡 `POLICY` | 102 | 0 | 102 | optimista: nunca avisa |

## UB detectados: forma × handle

Detectados / total de casos `UB` en cada celda, **por caso**: en `bucle` con
referencia o puntero cuenta el aviso sobre el iterador del `for`, que también
es inválido. Sobre el handle sostenido, CSA no detecta ninguna referencia ni
ningún puntero: ver [Experimento](experimento.md).

| Forma \ Sostiene | iterador | referencia | puntero |
|---|---:|---:|---:|
| `recto` | 0/32 | 0/25 | 0/25 |
| `guarda` | 16/32 | 0/25 | 0/25 |
| `bucle` | 16/32 | 16/32 | 16/32 |
| `llamada` | 16/32 | 0/25 | 0/25 |

## Por forma sintáctica

| Valor | Casos | UB | Detectados | Falsos negativos | Cobertura | SAFE | Falsos positivos | POLICY con aviso |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `recto` | 183 | 82 | 0 | 82 | 0.0% | 77 | 0 | 0/24 |
| `guarda` | 183 | 82 | 16 | 66 | 19.5% | 77 | 0 | 0/24 |
| `bucle` | 201 | 96 | 48 | 48 | 50.0% | 75 | 0 | 0/30 |
| `llamada` | 183 | 82 | 16 | 66 | 19.5% | 77 | 0 | 0/24 |

## Por handle retenido

| Valor | Casos | UB | Detectados | Falsos negativos | Cobertura | SAFE | Falsos positivos | POLICY con aviso |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `it` (iterador) | 264 | 128 | 48 | 80 | 37.5% | 96 | 0 | 0/40 |
| `ref` (referencia) | 243 | 107 | 16 | 91 | 15.0% | 105 | 0 | 0/31 |
| `ptr` (puntero) | 243 | 107 | 16 | 91 | 15.0% | 105 | 0 | 0/31 |

## Por contenedor

| Valor | Casos | UB | Detectados | Falsos negativos | Cobertura | SAFE | Falsos positivos | POLICY con aviso |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| [`std::vector`](../casos/vector/index.md) | 170 | 48 | 10 | 38 | 20.8% | 38 | 0 | 0/84 |
| [`std::deque`](../casos/deque/index.md) | 98 | 72 | 30 | 42 | 41.7% | 26 | 0 | 0/0 |
| [`std::list`](../casos/list/index.md) | 110 | 36 | 5 | 31 | 13.9% | 74 | 0 | 0/0 |
| [`std::forward_list`](../casos/flist/index.md) | 48 | 24 | 5 | 19 | 20.8% | 24 | 0 | 0/0 |
| [`std::set`](../casos/set/index.md) | 49 | 24 | 5 | 19 | 20.8% | 25 | 0 | 0/0 |
| [`std::multiset`](../casos/mset/index.md) | 37 | 24 | 5 | 19 | 20.8% | 13 | 0 | 0/0 |
| [`std::map`](../casos/map/index.md) | 61 | 24 | 5 | 19 | 20.8% | 37 | 0 | 0/0 |
| [`std::multimap`](../casos/mmap/index.md) | 37 | 24 | 5 | 19 | 20.8% | 13 | 0 | 0/0 |
| [`std::unordered_set`](../casos/uset/index.md) | 67 | 36 | 5 | 31 | 13.9% | 25 | 0 | 0/6 |
| [`std::unordered_map`](../casos/umap/index.md) | 73 | 30 | 5 | 25 | 16.7% | 31 | 0 | 0/12 |

## Por operación

| Contenedor | Operación | UB | Detectados | Cobertura | SAFE | FP | POLICY |
|---|---|---:|---:|---:|---:|---:|---:|
| `vector` | [`push_back`](../casos/vector/push_back.md) | 0 | 0 | — | 0 | 0 | 12 |
| `vector` | [`emplace_back`](../casos/vector/emplace_back.md) | 0 | 0 | — | 0 | 0 | 12 |
| `vector` | [`insert_begin`](../casos/vector/insert_begin.md) | 12 | 0 | 0.0% | 0 | 0 | 0 |
| `vector` | [`insert_end`](../casos/vector/insert_end.md) | 0 | 0 | — | 0 | 0 | 12 |
| `vector` | [`erase_begin`](../casos/vector/erase_begin.md) | 12 | 0 | 0.0% | 0 | 0 | 0 |
| `vector` | [`clear`](../casos/vector/clear.md) | 12 | 5 | 41.7% | 0 | 0 | 0 |
| `vector` | [`resize_grow`](../casos/vector/resize_grow.md) | 0 | 0 | — | 0 | 0 | 12 |
| `vector` | [`reserve`](../casos/vector/reserve.md) | 0 | 0 | — | 0 | 0 | 12 |
| `vector` | [`shrink_to_fit`](../casos/vector/shrink_to_fit.md) | 0 | 0 | — | 0 | 0 | 12 |
| `vector` | [`assign`](../casos/vector/assign.md) | 12 | 5 | 41.7% | 0 | 0 | 0 |
| `vector` | [`pop_back`](../casos/vector/pop_back.md) | 0 | 0 | — | 0 | 0 | 12 |
| `deque` | [`push_back`](../casos/deque/push_back.md) | 6 | 5 | 83.3% | 6 | 0 | 0 |
| `deque` | [`push_front`](../casos/deque/push_front.md) | 6 | 5 | 83.3% | 6 | 0 | 0 |
| `deque` | [`emplace_back`](../casos/deque/emplace_back.md) | 6 | 5 | 83.3% | 6 | 0 | 0 |
| `deque` | [`insert_middle`](../casos/deque/insert_middle.md) | 12 | 5 | 41.7% | 0 | 0 | 0 |
| `deque` | [`erase_begin`](../casos/deque/erase_begin.md) | 12 | 5 | 41.7% | 0 | 0 | 0 |
| `deque` | [`clear`](../casos/deque/clear.md) | 12 | 5 | 41.7% | 0 | 0 | 0 |
| `deque` | [`resize_grow`](../casos/deque/resize_grow.md) | 6 | 0 | 0.0% | 6 | 0 | 0 |
| `deque` | [`pop_front`](../casos/deque/pop_front.md) | 12 | 0 | 0.0% | 0 | 0 | 0 |
| `list` | [`push_back`](../casos/list/push_back.md) | 0 | 0 | — | 12 | 0 | 0 |
| `list` | [`push_front`](../casos/list/push_front.md) | 0 | 0 | — | 12 | 0 | 0 |
| `list` | [`insert`](../casos/list/insert.md) | 0 | 0 | — | 12 | 0 | 0 |
| `list` | [`erase_begin`](../casos/list/erase_begin.md) | 12 | 0 | 0.0% | 0 | 0 | 0 |
| `list` | [`clear`](../casos/list/clear.md) | 12 | 5 | 41.7% | 0 | 0 | 0 |
| `list` | [`resize_grow`](../casos/list/resize_grow.md) | 0 | 0 | — | 12 | 0 | 0 |
| `list` | [`pop_front`](../casos/list/pop_front.md) | 12 | 0 | 0.0% | 0 | 0 | 0 |
| `list` | [`reverse`](../casos/list/reverse.md) | 0 | 0 | — | 12 | 0 | 0 |
| `list` | [`sort`](../casos/list/sort.md) | 0 | 0 | — | 12 | 0 | 0 |
| `flist` | [`push_front`](../casos/flist/push_front.md) | 0 | 0 | — | 12 | 0 | 0 |
| `flist` | [`insert_after`](../casos/flist/insert_after.md) | 0 | 0 | — | 12 | 0 | 0 |
| `flist` | [`erase_after`](../casos/flist/erase_after.md) | 12 | 0 | 0.0% | 0 | 0 | 0 |
| `flist` | [`clear`](../casos/flist/clear.md) | 12 | 5 | 41.7% | 0 | 0 | 0 |
| `set` | [`insert`](../casos/set/insert.md) | 0 | 0 | — | 12 | 0 | 0 |
| `set` | [`emplace`](../casos/set/emplace.md) | 0 | 0 | — | 12 | 0 | 0 |
| `set` | [`erase_begin`](../casos/set/erase_begin.md) | 12 | 0 | 0.0% | 0 | 0 | 0 |
| `set` | [`clear`](../casos/set/clear.md) | 12 | 5 | 41.7% | 0 | 0 | 0 |
| `mset` | [`insert`](../casos/mset/insert.md) | 0 | 0 | — | 12 | 0 | 0 |
| `mset` | [`erase_begin`](../casos/mset/erase_begin.md) | 12 | 0 | 0.0% | 0 | 0 | 0 |
| `mset` | [`clear`](../casos/mset/clear.md) | 12 | 5 | 41.7% | 0 | 0 | 0 |
| `map` | [`insert`](../casos/map/insert.md) | 0 | 0 | — | 12 | 0 | 0 |
| `map` | [`emplace`](../casos/map/emplace.md) | 0 | 0 | — | 12 | 0 | 0 |
| `map` | [`subscript`](../casos/map/subscript.md) | 0 | 0 | — | 12 | 0 | 0 |
| `map` | [`erase_begin`](../casos/map/erase_begin.md) | 12 | 0 | 0.0% | 0 | 0 | 0 |
| `map` | [`clear`](../casos/map/clear.md) | 12 | 5 | 41.7% | 0 | 0 | 0 |
| `mmap` | [`insert`](../casos/mmap/insert.md) | 0 | 0 | — | 12 | 0 | 0 |
| `mmap` | [`erase_begin`](../casos/mmap/erase_begin.md) | 12 | 0 | 0.0% | 0 | 0 | 0 |
| `mmap` | [`clear`](../casos/mmap/clear.md) | 12 | 5 | 41.7% | 0 | 0 | 0 |
| `uset` | [`insert`](../casos/uset/insert.md) | 0 | 0 | — | 6 | 0 | 6 |
| `uset` | [`erase_begin`](../casos/uset/erase_begin.md) | 12 | 0 | 0.0% | 0 | 0 | 0 |
| `uset` | [`clear`](../casos/uset/clear.md) | 12 | 5 | 41.7% | 0 | 0 | 0 |
| `uset` | [`rehash`](../casos/uset/rehash.md) | 6 | 0 | 0.0% | 6 | 0 | 0 |
| `uset` | [`reserve`](../casos/uset/reserve.md) | 6 | 0 | 0.0% | 6 | 0 | 0 |
| `umap` | [`insert`](../casos/umap/insert.md) | 0 | 0 | — | 6 | 0 | 6 |
| `umap` | [`subscript`](../casos/umap/subscript.md) | 0 | 0 | — | 6 | 0 | 6 |
| `umap` | [`erase_begin`](../casos/umap/erase_begin.md) | 12 | 0 | 0.0% | 0 | 0 | 0 |
| `umap` | [`clear`](../casos/umap/clear.md) | 12 | 5 | 41.7% | 0 | 0 | 0 |
| `umap` | [`rehash`](../casos/umap/rehash.md) | 6 | 0 | 0.0% | 6 | 0 | 0 |

## Casos detectados

Los 80 casos `UB` en los que el analizador emitió aviso:

- [`f_vector_clear_it_guarda`](../casos/vector/clear.md#f_vector_clear_it_guarda)
- [`f_vector_clear_it_bucle`](../casos/vector/clear.md#f_vector_clear_it_bucle)
- [`f_vector_clear_it_llamada`](../casos/vector/clear.md#f_vector_clear_it_llamada)
- [`f_vector_clear_ref_bucle`](../casos/vector/clear.md#f_vector_clear_ref_bucle)
- [`f_vector_clear_ptr_bucle`](../casos/vector/clear.md#f_vector_clear_ptr_bucle)
- [`f_vector_assign_it_guarda`](../casos/vector/assign.md#f_vector_assign_it_guarda)
- [`f_vector_assign_it_bucle`](../casos/vector/assign.md#f_vector_assign_it_bucle)
- [`f_vector_assign_it_llamada`](../casos/vector/assign.md#f_vector_assign_it_llamada)
- [`f_vector_assign_ref_bucle`](../casos/vector/assign.md#f_vector_assign_ref_bucle)
- [`f_vector_assign_ptr_bucle`](../casos/vector/assign.md#f_vector_assign_ptr_bucle)
- [`f_deque_push_back_it_guarda`](../casos/deque/push_back.md#f_deque_push_back_it_guarda)
- [`f_deque_push_back_it_bucle`](../casos/deque/push_back.md#f_deque_push_back_it_bucle)
- [`f_deque_push_back_it_llamada`](../casos/deque/push_back.md#f_deque_push_back_it_llamada)
- [`f_deque_push_back_ref_bucle`](../casos/deque/push_back.md#f_deque_push_back_ref_bucle)
- [`f_deque_push_back_ptr_bucle`](../casos/deque/push_back.md#f_deque_push_back_ptr_bucle)
- [`f_deque_push_front_it_guarda`](../casos/deque/push_front.md#f_deque_push_front_it_guarda)
- [`f_deque_push_front_it_bucle`](../casos/deque/push_front.md#f_deque_push_front_it_bucle)
- [`f_deque_push_front_it_llamada`](../casos/deque/push_front.md#f_deque_push_front_it_llamada)
- [`f_deque_push_front_ref_bucle`](../casos/deque/push_front.md#f_deque_push_front_ref_bucle)
- [`f_deque_push_front_ptr_bucle`](../casos/deque/push_front.md#f_deque_push_front_ptr_bucle)
- [`f_deque_emplace_back_it_guarda`](../casos/deque/emplace_back.md#f_deque_emplace_back_it_guarda)
- [`f_deque_emplace_back_it_bucle`](../casos/deque/emplace_back.md#f_deque_emplace_back_it_bucle)
- [`f_deque_emplace_back_it_llamada`](../casos/deque/emplace_back.md#f_deque_emplace_back_it_llamada)
- [`f_deque_emplace_back_ref_bucle`](../casos/deque/emplace_back.md#f_deque_emplace_back_ref_bucle)
- [`f_deque_emplace_back_ptr_bucle`](../casos/deque/emplace_back.md#f_deque_emplace_back_ptr_bucle)
- [`f_deque_insert_middle_it_guarda`](../casos/deque/insert_middle.md#f_deque_insert_middle_it_guarda)
- [`f_deque_insert_middle_it_bucle`](../casos/deque/insert_middle.md#f_deque_insert_middle_it_bucle)
- [`f_deque_insert_middle_it_llamada`](../casos/deque/insert_middle.md#f_deque_insert_middle_it_llamada)
- [`f_deque_insert_middle_ref_bucle`](../casos/deque/insert_middle.md#f_deque_insert_middle_ref_bucle)
- [`f_deque_insert_middle_ptr_bucle`](../casos/deque/insert_middle.md#f_deque_insert_middle_ptr_bucle)
- [`f_deque_erase_begin_it_guarda`](../casos/deque/erase_begin.md#f_deque_erase_begin_it_guarda)
- [`f_deque_erase_begin_it_bucle`](../casos/deque/erase_begin.md#f_deque_erase_begin_it_bucle)
- [`f_deque_erase_begin_it_llamada`](../casos/deque/erase_begin.md#f_deque_erase_begin_it_llamada)
- [`f_deque_erase_begin_ref_bucle`](../casos/deque/erase_begin.md#f_deque_erase_begin_ref_bucle)
- [`f_deque_erase_begin_ptr_bucle`](../casos/deque/erase_begin.md#f_deque_erase_begin_ptr_bucle)
- [`f_deque_clear_it_guarda`](../casos/deque/clear.md#f_deque_clear_it_guarda)
- [`f_deque_clear_it_bucle`](../casos/deque/clear.md#f_deque_clear_it_bucle)
- [`f_deque_clear_it_llamada`](../casos/deque/clear.md#f_deque_clear_it_llamada)
- [`f_deque_clear_ref_bucle`](../casos/deque/clear.md#f_deque_clear_ref_bucle)
- [`f_deque_clear_ptr_bucle`](../casos/deque/clear.md#f_deque_clear_ptr_bucle)
- [`f_list_clear_it_guarda`](../casos/list/clear.md#f_list_clear_it_guarda)
- [`f_list_clear_it_bucle`](../casos/list/clear.md#f_list_clear_it_bucle)
- [`f_list_clear_it_llamada`](../casos/list/clear.md#f_list_clear_it_llamada)
- [`f_list_clear_ref_bucle`](../casos/list/clear.md#f_list_clear_ref_bucle)
- [`f_list_clear_ptr_bucle`](../casos/list/clear.md#f_list_clear_ptr_bucle)
- [`f_flist_clear_it_guarda`](../casos/flist/clear.md#f_flist_clear_it_guarda)
- [`f_flist_clear_it_bucle`](../casos/flist/clear.md#f_flist_clear_it_bucle)
- [`f_flist_clear_it_llamada`](../casos/flist/clear.md#f_flist_clear_it_llamada)
- [`f_flist_clear_ref_bucle`](../casos/flist/clear.md#f_flist_clear_ref_bucle)
- [`f_flist_clear_ptr_bucle`](../casos/flist/clear.md#f_flist_clear_ptr_bucle)
- [`f_set_clear_it_guarda`](../casos/set/clear.md#f_set_clear_it_guarda)
- [`f_set_clear_it_bucle`](../casos/set/clear.md#f_set_clear_it_bucle)
- [`f_set_clear_it_llamada`](../casos/set/clear.md#f_set_clear_it_llamada)
- [`f_set_clear_ref_bucle`](../casos/set/clear.md#f_set_clear_ref_bucle)
- [`f_set_clear_ptr_bucle`](../casos/set/clear.md#f_set_clear_ptr_bucle)
- [`f_mset_clear_it_guarda`](../casos/mset/clear.md#f_mset_clear_it_guarda)
- [`f_mset_clear_it_bucle`](../casos/mset/clear.md#f_mset_clear_it_bucle)
- [`f_mset_clear_it_llamada`](../casos/mset/clear.md#f_mset_clear_it_llamada)
- [`f_mset_clear_ref_bucle`](../casos/mset/clear.md#f_mset_clear_ref_bucle)
- [`f_mset_clear_ptr_bucle`](../casos/mset/clear.md#f_mset_clear_ptr_bucle)
- [`f_map_clear_it_guarda`](../casos/map/clear.md#f_map_clear_it_guarda)
- [`f_map_clear_it_bucle`](../casos/map/clear.md#f_map_clear_it_bucle)
- [`f_map_clear_it_llamada`](../casos/map/clear.md#f_map_clear_it_llamada)
- [`f_map_clear_ref_bucle`](../casos/map/clear.md#f_map_clear_ref_bucle)
- [`f_map_clear_ptr_bucle`](../casos/map/clear.md#f_map_clear_ptr_bucle)
- [`f_mmap_clear_it_guarda`](../casos/mmap/clear.md#f_mmap_clear_it_guarda)
- [`f_mmap_clear_it_bucle`](../casos/mmap/clear.md#f_mmap_clear_it_bucle)
- [`f_mmap_clear_it_llamada`](../casos/mmap/clear.md#f_mmap_clear_it_llamada)
- [`f_mmap_clear_ref_bucle`](../casos/mmap/clear.md#f_mmap_clear_ref_bucle)
- [`f_mmap_clear_ptr_bucle`](../casos/mmap/clear.md#f_mmap_clear_ptr_bucle)
- [`f_uset_clear_it_guarda`](../casos/uset/clear.md#f_uset_clear_it_guarda)
- [`f_uset_clear_it_bucle`](../casos/uset/clear.md#f_uset_clear_it_bucle)
- [`f_uset_clear_it_llamada`](../casos/uset/clear.md#f_uset_clear_it_llamada)
- [`f_uset_clear_ref_bucle`](../casos/uset/clear.md#f_uset_clear_ref_bucle)
- [`f_uset_clear_ptr_bucle`](../casos/uset/clear.md#f_uset_clear_ptr_bucle)
- [`f_umap_clear_it_guarda`](../casos/umap/clear.md#f_umap_clear_it_guarda)
- [`f_umap_clear_it_bucle`](../casos/umap/clear.md#f_umap_clear_it_bucle)
- [`f_umap_clear_it_llamada`](../casos/umap/clear.md#f_umap_clear_it_llamada)
- [`f_umap_clear_ref_bucle`](../casos/umap/clear.md#f_umap_clear_ref_bucle)
- [`f_umap_clear_ptr_bucle`](../casos/umap/clear.md#f_umap_clear_ptr_bucle)
