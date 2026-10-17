# Índice de casos

Los 684 casos del corpus. *Dinámico* 🛑 = algún instrumento detectó el defecto en alguna ejecución.

| # | Caso | Contenedor | Operación | Sostiene | Forma | Etiqueta | Estático | Dinámico |
|---:|---|---|---|---|---|---|---|---|
| 1 | [`f_vector_push_back_it_recto`](casos/vector/push_back.md#f_vector_push_back_it_recto) | `vector` | `push_back` | `it` | `recto` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 2 | [`f_vector_push_back_it_guarda`](casos/vector/push_back.md#f_vector_push_back_it_guarda) | `vector` | `push_back` | `it` | `guarda` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 3 | [`f_vector_push_back_it_bucle`](casos/vector/push_back.md#f_vector_push_back_it_bucle) | `vector` | `push_back` | `it` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 4 | [`f_vector_push_back_it_llamada`](casos/vector/push_back.md#f_vector_push_back_it_llamada) | `vector` | `push_back` | `it` | `llamada` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 5 | [`f_vector_push_back_ref_recto`](casos/vector/push_back.md#f_vector_push_back_ref_recto) | `vector` | `push_back` | `ref` | `recto` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 6 | [`f_vector_push_back_ref_guarda`](casos/vector/push_back.md#f_vector_push_back_ref_guarda) | `vector` | `push_back` | `ref` | `guarda` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 7 | [`f_vector_push_back_ref_bucle`](casos/vector/push_back.md#f_vector_push_back_ref_bucle) | `vector` | `push_back` | `ref` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 8 | [`f_vector_push_back_ref_llamada`](casos/vector/push_back.md#f_vector_push_back_ref_llamada) | `vector` | `push_back` | `ref` | `llamada` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 9 | [`f_vector_push_back_ptr_recto`](casos/vector/push_back.md#f_vector_push_back_ptr_recto) | `vector` | `push_back` | `ptr` | `recto` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 10 | [`f_vector_push_back_ptr_guarda`](casos/vector/push_back.md#f_vector_push_back_ptr_guarda) | `vector` | `push_back` | `ptr` | `guarda` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 11 | [`f_vector_push_back_ptr_bucle`](casos/vector/push_back.md#f_vector_push_back_ptr_bucle) | `vector` | `push_back` | `ptr` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 12 | [`f_vector_push_back_ptr_llamada`](casos/vector/push_back.md#f_vector_push_back_ptr_llamada) | `vector` | `push_back` | `ptr` | `llamada` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 13 | [`f_vector_emplace_back_it_recto`](casos/vector/emplace_back.md#f_vector_emplace_back_it_recto) | `vector` | `emplace_back` | `it` | `recto` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 14 | [`f_vector_emplace_back_it_guarda`](casos/vector/emplace_back.md#f_vector_emplace_back_it_guarda) | `vector` | `emplace_back` | `it` | `guarda` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 15 | [`f_vector_emplace_back_it_bucle`](casos/vector/emplace_back.md#f_vector_emplace_back_it_bucle) | `vector` | `emplace_back` | `it` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 16 | [`f_vector_emplace_back_it_llamada`](casos/vector/emplace_back.md#f_vector_emplace_back_it_llamada) | `vector` | `emplace_back` | `it` | `llamada` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 17 | [`f_vector_emplace_back_ref_recto`](casos/vector/emplace_back.md#f_vector_emplace_back_ref_recto) | `vector` | `emplace_back` | `ref` | `recto` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 18 | [`f_vector_emplace_back_ref_guarda`](casos/vector/emplace_back.md#f_vector_emplace_back_ref_guarda) | `vector` | `emplace_back` | `ref` | `guarda` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 19 | [`f_vector_emplace_back_ref_bucle`](casos/vector/emplace_back.md#f_vector_emplace_back_ref_bucle) | `vector` | `emplace_back` | `ref` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 20 | [`f_vector_emplace_back_ref_llamada`](casos/vector/emplace_back.md#f_vector_emplace_back_ref_llamada) | `vector` | `emplace_back` | `ref` | `llamada` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 21 | [`f_vector_emplace_back_ptr_recto`](casos/vector/emplace_back.md#f_vector_emplace_back_ptr_recto) | `vector` | `emplace_back` | `ptr` | `recto` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 22 | [`f_vector_emplace_back_ptr_guarda`](casos/vector/emplace_back.md#f_vector_emplace_back_ptr_guarda) | `vector` | `emplace_back` | `ptr` | `guarda` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 23 | [`f_vector_emplace_back_ptr_bucle`](casos/vector/emplace_back.md#f_vector_emplace_back_ptr_bucle) | `vector` | `emplace_back` | `ptr` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 24 | [`f_vector_emplace_back_ptr_llamada`](casos/vector/emplace_back.md#f_vector_emplace_back_ptr_llamada) | `vector` | `emplace_back` | `ptr` | `llamada` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 25 | [`f_vector_insert_begin_it_recto`](casos/vector/insert_begin.md#f_vector_insert_begin_it_recto) | `vector` | `insert_begin` | `it` | `recto` | 🔴 `UB` | ✅ detectado | 🛑 |
| 26 | [`f_vector_insert_begin_it_guarda`](casos/vector/insert_begin.md#f_vector_insert_begin_it_guarda) | `vector` | `insert_begin` | `it` | `guarda` | 🔴 `UB` | ✅ detectado | 🛑 |
| 27 | [`f_vector_insert_begin_it_bucle`](casos/vector/insert_begin.md#f_vector_insert_begin_it_bucle) | `vector` | `insert_begin` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 28 | [`f_vector_insert_begin_it_llamada`](casos/vector/insert_begin.md#f_vector_insert_begin_it_llamada) | `vector` | `insert_begin` | `it` | `llamada` | 🔴 `UB` | ✅ detectado | 🛑 |
| 29 | [`f_vector_insert_begin_ref_recto`](casos/vector/insert_begin.md#f_vector_insert_begin_ref_recto) | `vector` | `insert_begin` | `ref` | `recto` | 🔴 `UB` | ❌ falso negativo | — |
| 30 | [`f_vector_insert_begin_ref_guarda`](casos/vector/insert_begin.md#f_vector_insert_begin_ref_guarda) | `vector` | `insert_begin` | `ref` | `guarda` | 🔴 `UB` | ❌ falso negativo | — |
| 31 | [`f_vector_insert_begin_ref_bucle`](casos/vector/insert_begin.md#f_vector_insert_begin_ref_bucle) | `vector` | `insert_begin` | `ref` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 32 | [`f_vector_insert_begin_ref_llamada`](casos/vector/insert_begin.md#f_vector_insert_begin_ref_llamada) | `vector` | `insert_begin` | `ref` | `llamada` | 🔴 `UB` | ❌ falso negativo | — |
| 33 | [`f_vector_insert_begin_ptr_recto`](casos/vector/insert_begin.md#f_vector_insert_begin_ptr_recto) | `vector` | `insert_begin` | `ptr` | `recto` | 🔴 `UB` | ❌ falso negativo | — |
| 34 | [`f_vector_insert_begin_ptr_guarda`](casos/vector/insert_begin.md#f_vector_insert_begin_ptr_guarda) | `vector` | `insert_begin` | `ptr` | `guarda` | 🔴 `UB` | ❌ falso negativo | — |
| 35 | [`f_vector_insert_begin_ptr_bucle`](casos/vector/insert_begin.md#f_vector_insert_begin_ptr_bucle) | `vector` | `insert_begin` | `ptr` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 36 | [`f_vector_insert_begin_ptr_llamada`](casos/vector/insert_begin.md#f_vector_insert_begin_ptr_llamada) | `vector` | `insert_begin` | `ptr` | `llamada` | 🔴 `UB` | ❌ falso negativo | — |
| 37 | [`f_vector_insert_end_it_recto`](casos/vector/insert_end.md#f_vector_insert_end_it_recto) | `vector` | `insert_end` | `it` | `recto` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 38 | [`f_vector_insert_end_it_guarda`](casos/vector/insert_end.md#f_vector_insert_end_it_guarda) | `vector` | `insert_end` | `it` | `guarda` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 39 | [`f_vector_insert_end_it_bucle`](casos/vector/insert_end.md#f_vector_insert_end_it_bucle) | `vector` | `insert_end` | `it` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 40 | [`f_vector_insert_end_it_llamada`](casos/vector/insert_end.md#f_vector_insert_end_it_llamada) | `vector` | `insert_end` | `it` | `llamada` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 41 | [`f_vector_insert_end_ref_recto`](casos/vector/insert_end.md#f_vector_insert_end_ref_recto) | `vector` | `insert_end` | `ref` | `recto` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 42 | [`f_vector_insert_end_ref_guarda`](casos/vector/insert_end.md#f_vector_insert_end_ref_guarda) | `vector` | `insert_end` | `ref` | `guarda` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 43 | [`f_vector_insert_end_ref_bucle`](casos/vector/insert_end.md#f_vector_insert_end_ref_bucle) | `vector` | `insert_end` | `ref` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 44 | [`f_vector_insert_end_ref_llamada`](casos/vector/insert_end.md#f_vector_insert_end_ref_llamada) | `vector` | `insert_end` | `ref` | `llamada` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 45 | [`f_vector_insert_end_ptr_recto`](casos/vector/insert_end.md#f_vector_insert_end_ptr_recto) | `vector` | `insert_end` | `ptr` | `recto` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 46 | [`f_vector_insert_end_ptr_guarda`](casos/vector/insert_end.md#f_vector_insert_end_ptr_guarda) | `vector` | `insert_end` | `ptr` | `guarda` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 47 | [`f_vector_insert_end_ptr_bucle`](casos/vector/insert_end.md#f_vector_insert_end_ptr_bucle) | `vector` | `insert_end` | `ptr` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 48 | [`f_vector_insert_end_ptr_llamada`](casos/vector/insert_end.md#f_vector_insert_end_ptr_llamada) | `vector` | `insert_end` | `ptr` | `llamada` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 49 | [`f_vector_erase_begin_it_recto`](casos/vector/erase_begin.md#f_vector_erase_begin_it_recto) | `vector` | `erase_begin` | `it` | `recto` | 🔴 `UB` | ✅ detectado | 🛑 |
| 50 | [`f_vector_erase_begin_it_guarda`](casos/vector/erase_begin.md#f_vector_erase_begin_it_guarda) | `vector` | `erase_begin` | `it` | `guarda` | 🔴 `UB` | ✅ detectado | 🛑 |
| 51 | [`f_vector_erase_begin_it_bucle`](casos/vector/erase_begin.md#f_vector_erase_begin_it_bucle) | `vector` | `erase_begin` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 52 | [`f_vector_erase_begin_it_llamada`](casos/vector/erase_begin.md#f_vector_erase_begin_it_llamada) | `vector` | `erase_begin` | `it` | `llamada` | 🔴 `UB` | ✅ detectado | 🛑 |
| 53 | [`f_vector_erase_begin_ref_recto`](casos/vector/erase_begin.md#f_vector_erase_begin_ref_recto) | `vector` | `erase_begin` | `ref` | `recto` | 🔴 `UB` | ❌ falso negativo | — |
| 54 | [`f_vector_erase_begin_ref_guarda`](casos/vector/erase_begin.md#f_vector_erase_begin_ref_guarda) | `vector` | `erase_begin` | `ref` | `guarda` | 🔴 `UB` | ❌ falso negativo | — |
| 55 | [`f_vector_erase_begin_ref_bucle`](casos/vector/erase_begin.md#f_vector_erase_begin_ref_bucle) | `vector` | `erase_begin` | `ref` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 56 | [`f_vector_erase_begin_ref_llamada`](casos/vector/erase_begin.md#f_vector_erase_begin_ref_llamada) | `vector` | `erase_begin` | `ref` | `llamada` | 🔴 `UB` | ❌ falso negativo | — |
| 57 | [`f_vector_erase_begin_ptr_recto`](casos/vector/erase_begin.md#f_vector_erase_begin_ptr_recto) | `vector` | `erase_begin` | `ptr` | `recto` | 🔴 `UB` | ❌ falso negativo | — |
| 58 | [`f_vector_erase_begin_ptr_guarda`](casos/vector/erase_begin.md#f_vector_erase_begin_ptr_guarda) | `vector` | `erase_begin` | `ptr` | `guarda` | 🔴 `UB` | ❌ falso negativo | — |
| 59 | [`f_vector_erase_begin_ptr_bucle`](casos/vector/erase_begin.md#f_vector_erase_begin_ptr_bucle) | `vector` | `erase_begin` | `ptr` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 60 | [`f_vector_erase_begin_ptr_llamada`](casos/vector/erase_begin.md#f_vector_erase_begin_ptr_llamada) | `vector` | `erase_begin` | `ptr` | `llamada` | 🔴 `UB` | ❌ falso negativo | — |
| 61 | [`f_vector_clear_it_recto`](casos/vector/clear.md#f_vector_clear_it_recto) | `vector` | `clear` | `it` | `recto` | 🔴 `UB` | ✅ detectado | 🛑 |
| 62 | [`f_vector_clear_it_guarda`](casos/vector/clear.md#f_vector_clear_it_guarda) | `vector` | `clear` | `it` | `guarda` | 🔴 `UB` | ✅ detectado | 🛑 |
| 63 | [`f_vector_clear_it_bucle`](casos/vector/clear.md#f_vector_clear_it_bucle) | `vector` | `clear` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 64 | [`f_vector_clear_it_llamada`](casos/vector/clear.md#f_vector_clear_it_llamada) | `vector` | `clear` | `it` | `llamada` | 🔴 `UB` | ✅ detectado | 🛑 |
| 65 | [`f_vector_clear_ref_recto`](casos/vector/clear.md#f_vector_clear_ref_recto) | `vector` | `clear` | `ref` | `recto` | 🔴 `UB` | ❌ falso negativo | — |
| 66 | [`f_vector_clear_ref_guarda`](casos/vector/clear.md#f_vector_clear_ref_guarda) | `vector` | `clear` | `ref` | `guarda` | 🔴 `UB` | ❌ falso negativo | — |
| 67 | [`f_vector_clear_ref_bucle`](casos/vector/clear.md#f_vector_clear_ref_bucle) | `vector` | `clear` | `ref` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 68 | [`f_vector_clear_ref_llamada`](casos/vector/clear.md#f_vector_clear_ref_llamada) | `vector` | `clear` | `ref` | `llamada` | 🔴 `UB` | ❌ falso negativo | — |
| 69 | [`f_vector_clear_ptr_recto`](casos/vector/clear.md#f_vector_clear_ptr_recto) | `vector` | `clear` | `ptr` | `recto` | 🔴 `UB` | ❌ falso negativo | — |
| 70 | [`f_vector_clear_ptr_guarda`](casos/vector/clear.md#f_vector_clear_ptr_guarda) | `vector` | `clear` | `ptr` | `guarda` | 🔴 `UB` | ❌ falso negativo | — |
| 71 | [`f_vector_clear_ptr_bucle`](casos/vector/clear.md#f_vector_clear_ptr_bucle) | `vector` | `clear` | `ptr` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 72 | [`f_vector_clear_ptr_llamada`](casos/vector/clear.md#f_vector_clear_ptr_llamada) | `vector` | `clear` | `ptr` | `llamada` | 🔴 `UB` | ❌ falso negativo | — |
| 73 | [`f_vector_resize_grow_it_recto`](casos/vector/resize_grow.md#f_vector_resize_grow_it_recto) | `vector` | `resize_grow` | `it` | `recto` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 74 | [`f_vector_resize_grow_it_guarda`](casos/vector/resize_grow.md#f_vector_resize_grow_it_guarda) | `vector` | `resize_grow` | `it` | `guarda` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 75 | [`f_vector_resize_grow_it_bucle`](casos/vector/resize_grow.md#f_vector_resize_grow_it_bucle) | `vector` | `resize_grow` | `it` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 76 | [`f_vector_resize_grow_it_llamada`](casos/vector/resize_grow.md#f_vector_resize_grow_it_llamada) | `vector` | `resize_grow` | `it` | `llamada` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 77 | [`f_vector_resize_grow_ref_recto`](casos/vector/resize_grow.md#f_vector_resize_grow_ref_recto) | `vector` | `resize_grow` | `ref` | `recto` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 78 | [`f_vector_resize_grow_ref_guarda`](casos/vector/resize_grow.md#f_vector_resize_grow_ref_guarda) | `vector` | `resize_grow` | `ref` | `guarda` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 79 | [`f_vector_resize_grow_ref_bucle`](casos/vector/resize_grow.md#f_vector_resize_grow_ref_bucle) | `vector` | `resize_grow` | `ref` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 80 | [`f_vector_resize_grow_ref_llamada`](casos/vector/resize_grow.md#f_vector_resize_grow_ref_llamada) | `vector` | `resize_grow` | `ref` | `llamada` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 81 | [`f_vector_resize_grow_ptr_recto`](casos/vector/resize_grow.md#f_vector_resize_grow_ptr_recto) | `vector` | `resize_grow` | `ptr` | `recto` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 82 | [`f_vector_resize_grow_ptr_guarda`](casos/vector/resize_grow.md#f_vector_resize_grow_ptr_guarda) | `vector` | `resize_grow` | `ptr` | `guarda` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 83 | [`f_vector_resize_grow_ptr_bucle`](casos/vector/resize_grow.md#f_vector_resize_grow_ptr_bucle) | `vector` | `resize_grow` | `ptr` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 84 | [`f_vector_resize_grow_ptr_llamada`](casos/vector/resize_grow.md#f_vector_resize_grow_ptr_llamada) | `vector` | `resize_grow` | `ptr` | `llamada` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 85 | [`f_vector_reserve_it_recto`](casos/vector/reserve.md#f_vector_reserve_it_recto) | `vector` | `reserve` | `it` | `recto` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 86 | [`f_vector_reserve_it_guarda`](casos/vector/reserve.md#f_vector_reserve_it_guarda) | `vector` | `reserve` | `it` | `guarda` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 87 | [`f_vector_reserve_it_bucle`](casos/vector/reserve.md#f_vector_reserve_it_bucle) | `vector` | `reserve` | `it` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 88 | [`f_vector_reserve_it_llamada`](casos/vector/reserve.md#f_vector_reserve_it_llamada) | `vector` | `reserve` | `it` | `llamada` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 89 | [`f_vector_reserve_ref_recto`](casos/vector/reserve.md#f_vector_reserve_ref_recto) | `vector` | `reserve` | `ref` | `recto` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 90 | [`f_vector_reserve_ref_guarda`](casos/vector/reserve.md#f_vector_reserve_ref_guarda) | `vector` | `reserve` | `ref` | `guarda` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 91 | [`f_vector_reserve_ref_bucle`](casos/vector/reserve.md#f_vector_reserve_ref_bucle) | `vector` | `reserve` | `ref` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 92 | [`f_vector_reserve_ref_llamada`](casos/vector/reserve.md#f_vector_reserve_ref_llamada) | `vector` | `reserve` | `ref` | `llamada` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 93 | [`f_vector_reserve_ptr_recto`](casos/vector/reserve.md#f_vector_reserve_ptr_recto) | `vector` | `reserve` | `ptr` | `recto` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 94 | [`f_vector_reserve_ptr_guarda`](casos/vector/reserve.md#f_vector_reserve_ptr_guarda) | `vector` | `reserve` | `ptr` | `guarda` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 95 | [`f_vector_reserve_ptr_bucle`](casos/vector/reserve.md#f_vector_reserve_ptr_bucle) | `vector` | `reserve` | `ptr` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 96 | [`f_vector_reserve_ptr_llamada`](casos/vector/reserve.md#f_vector_reserve_ptr_llamada) | `vector` | `reserve` | `ptr` | `llamada` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 97 | [`f_vector_shrink_to_fit_it_recto`](casos/vector/shrink_to_fit.md#f_vector_shrink_to_fit_it_recto) | `vector` | `shrink_to_fit` | `it` | `recto` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 98 | [`f_vector_shrink_to_fit_it_guarda`](casos/vector/shrink_to_fit.md#f_vector_shrink_to_fit_it_guarda) | `vector` | `shrink_to_fit` | `it` | `guarda` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 99 | [`f_vector_shrink_to_fit_it_bucle`](casos/vector/shrink_to_fit.md#f_vector_shrink_to_fit_it_bucle) | `vector` | `shrink_to_fit` | `it` | `bucle` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 100 | [`f_vector_shrink_to_fit_it_llamada`](casos/vector/shrink_to_fit.md#f_vector_shrink_to_fit_it_llamada) | `vector` | `shrink_to_fit` | `it` | `llamada` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 101 | [`f_vector_shrink_to_fit_ref_recto`](casos/vector/shrink_to_fit.md#f_vector_shrink_to_fit_ref_recto) | `vector` | `shrink_to_fit` | `ref` | `recto` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 102 | [`f_vector_shrink_to_fit_ref_guarda`](casos/vector/shrink_to_fit.md#f_vector_shrink_to_fit_ref_guarda) | `vector` | `shrink_to_fit` | `ref` | `guarda` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 103 | [`f_vector_shrink_to_fit_ref_bucle`](casos/vector/shrink_to_fit.md#f_vector_shrink_to_fit_ref_bucle) | `vector` | `shrink_to_fit` | `ref` | `bucle` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 104 | [`f_vector_shrink_to_fit_ref_llamada`](casos/vector/shrink_to_fit.md#f_vector_shrink_to_fit_ref_llamada) | `vector` | `shrink_to_fit` | `ref` | `llamada` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 105 | [`f_vector_shrink_to_fit_ptr_recto`](casos/vector/shrink_to_fit.md#f_vector_shrink_to_fit_ptr_recto) | `vector` | `shrink_to_fit` | `ptr` | `recto` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 106 | [`f_vector_shrink_to_fit_ptr_guarda`](casos/vector/shrink_to_fit.md#f_vector_shrink_to_fit_ptr_guarda) | `vector` | `shrink_to_fit` | `ptr` | `guarda` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 107 | [`f_vector_shrink_to_fit_ptr_bucle`](casos/vector/shrink_to_fit.md#f_vector_shrink_to_fit_ptr_bucle) | `vector` | `shrink_to_fit` | `ptr` | `bucle` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 108 | [`f_vector_shrink_to_fit_ptr_llamada`](casos/vector/shrink_to_fit.md#f_vector_shrink_to_fit_ptr_llamada) | `vector` | `shrink_to_fit` | `ptr` | `llamada` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 109 | [`f_vector_assign_it_recto`](casos/vector/assign.md#f_vector_assign_it_recto) | `vector` | `assign` | `it` | `recto` | 🔴 `UB` | ✅ detectado | 🛑 |
| 110 | [`f_vector_assign_it_guarda`](casos/vector/assign.md#f_vector_assign_it_guarda) | `vector` | `assign` | `it` | `guarda` | 🔴 `UB` | ✅ detectado | 🛑 |
| 111 | [`f_vector_assign_it_bucle`](casos/vector/assign.md#f_vector_assign_it_bucle) | `vector` | `assign` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 112 | [`f_vector_assign_it_llamada`](casos/vector/assign.md#f_vector_assign_it_llamada) | `vector` | `assign` | `it` | `llamada` | 🔴 `UB` | ✅ detectado | 🛑 |
| 113 | [`f_vector_assign_ref_recto`](casos/vector/assign.md#f_vector_assign_ref_recto) | `vector` | `assign` | `ref` | `recto` | 🔴 `UB` | ❌ falso negativo | — |
| 114 | [`f_vector_assign_ref_guarda`](casos/vector/assign.md#f_vector_assign_ref_guarda) | `vector` | `assign` | `ref` | `guarda` | 🔴 `UB` | ❌ falso negativo | — |
| 115 | [`f_vector_assign_ref_bucle`](casos/vector/assign.md#f_vector_assign_ref_bucle) | `vector` | `assign` | `ref` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 116 | [`f_vector_assign_ref_llamada`](casos/vector/assign.md#f_vector_assign_ref_llamada) | `vector` | `assign` | `ref` | `llamada` | 🔴 `UB` | ❌ falso negativo | — |
| 117 | [`f_vector_assign_ptr_recto`](casos/vector/assign.md#f_vector_assign_ptr_recto) | `vector` | `assign` | `ptr` | `recto` | 🔴 `UB` | ❌ falso negativo | — |
| 118 | [`f_vector_assign_ptr_guarda`](casos/vector/assign.md#f_vector_assign_ptr_guarda) | `vector` | `assign` | `ptr` | `guarda` | 🔴 `UB` | ❌ falso negativo | — |
| 119 | [`f_vector_assign_ptr_bucle`](casos/vector/assign.md#f_vector_assign_ptr_bucle) | `vector` | `assign` | `ptr` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 120 | [`f_vector_assign_ptr_llamada`](casos/vector/assign.md#f_vector_assign_ptr_llamada) | `vector` | `assign` | `ptr` | `llamada` | 🔴 `UB` | ❌ falso negativo | — |
| 121 | [`f_vector_pop_back_it_recto`](casos/vector/pop_back.md#f_vector_pop_back_it_recto) | `vector` | `pop_back` | `it` | `recto` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 122 | [`f_vector_pop_back_it_guarda`](casos/vector/pop_back.md#f_vector_pop_back_it_guarda) | `vector` | `pop_back` | `it` | `guarda` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 123 | [`f_vector_pop_back_it_bucle`](casos/vector/pop_back.md#f_vector_pop_back_it_bucle) | `vector` | `pop_back` | `it` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 124 | [`f_vector_pop_back_it_llamada`](casos/vector/pop_back.md#f_vector_pop_back_it_llamada) | `vector` | `pop_back` | `it` | `llamada` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 125 | [`f_vector_pop_back_ref_recto`](casos/vector/pop_back.md#f_vector_pop_back_ref_recto) | `vector` | `pop_back` | `ref` | `recto` | 🟡 `POLICY` | silencio (optimista) | — |
| 126 | [`f_vector_pop_back_ref_guarda`](casos/vector/pop_back.md#f_vector_pop_back_ref_guarda) | `vector` | `pop_back` | `ref` | `guarda` | 🟡 `POLICY` | silencio (optimista) | — |
| 127 | [`f_vector_pop_back_ref_bucle`](casos/vector/pop_back.md#f_vector_pop_back_ref_bucle) | `vector` | `pop_back` | `ref` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 128 | [`f_vector_pop_back_ref_llamada`](casos/vector/pop_back.md#f_vector_pop_back_ref_llamada) | `vector` | `pop_back` | `ref` | `llamada` | 🟡 `POLICY` | silencio (optimista) | — |
| 129 | [`f_vector_pop_back_ptr_recto`](casos/vector/pop_back.md#f_vector_pop_back_ptr_recto) | `vector` | `pop_back` | `ptr` | `recto` | 🟡 `POLICY` | silencio (optimista) | — |
| 130 | [`f_vector_pop_back_ptr_guarda`](casos/vector/pop_back.md#f_vector_pop_back_ptr_guarda) | `vector` | `pop_back` | `ptr` | `guarda` | 🟡 `POLICY` | silencio (optimista) | — |
| 131 | [`f_vector_pop_back_ptr_bucle`](casos/vector/pop_back.md#f_vector_pop_back_ptr_bucle) | `vector` | `pop_back` | `ptr` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 132 | [`f_vector_pop_back_ptr_llamada`](casos/vector/pop_back.md#f_vector_pop_back_ptr_llamada) | `vector` | `pop_back` | `ptr` | `llamada` | 🟡 `POLICY` | silencio (optimista) | — |
| 133 | [`f_deque_push_back_it_recto`](casos/deque/push_back.md#f_deque_push_back_it_recto) | `deque` | `push_back` | `it` | `recto` | 🔴 `UB` | ✅ detectado | 🛑 |
| 134 | [`f_deque_push_back_it_guarda`](casos/deque/push_back.md#f_deque_push_back_it_guarda) | `deque` | `push_back` | `it` | `guarda` | 🔴 `UB` | ✅ detectado | 🛑 |
| 135 | [`f_deque_push_back_it_bucle`](casos/deque/push_back.md#f_deque_push_back_it_bucle) | `deque` | `push_back` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 136 | [`f_deque_push_back_it_llamada`](casos/deque/push_back.md#f_deque_push_back_it_llamada) | `deque` | `push_back` | `it` | `llamada` | 🔴 `UB` | ✅ detectado | 🛑 |
| 137 | [`f_deque_push_back_ref_recto`](casos/deque/push_back.md#f_deque_push_back_ref_recto) | `deque` | `push_back` | `ref` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 138 | [`f_deque_push_back_ref_guarda`](casos/deque/push_back.md#f_deque_push_back_ref_guarda) | `deque` | `push_back` | `ref` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 139 | [`f_deque_push_back_ref_bucle`](casos/deque/push_back.md#f_deque_push_back_ref_bucle) | `deque` | `push_back` | `ref` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 140 | [`f_deque_push_back_ref_llamada`](casos/deque/push_back.md#f_deque_push_back_ref_llamada) | `deque` | `push_back` | `ref` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 141 | [`f_deque_push_back_ptr_recto`](casos/deque/push_back.md#f_deque_push_back_ptr_recto) | `deque` | `push_back` | `ptr` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 142 | [`f_deque_push_back_ptr_guarda`](casos/deque/push_back.md#f_deque_push_back_ptr_guarda) | `deque` | `push_back` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 143 | [`f_deque_push_back_ptr_bucle`](casos/deque/push_back.md#f_deque_push_back_ptr_bucle) | `deque` | `push_back` | `ptr` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 144 | [`f_deque_push_back_ptr_llamada`](casos/deque/push_back.md#f_deque_push_back_ptr_llamada) | `deque` | `push_back` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 145 | [`f_deque_push_front_it_recto`](casos/deque/push_front.md#f_deque_push_front_it_recto) | `deque` | `push_front` | `it` | `recto` | 🔴 `UB` | ✅ detectado | 🛑 |
| 146 | [`f_deque_push_front_it_guarda`](casos/deque/push_front.md#f_deque_push_front_it_guarda) | `deque` | `push_front` | `it` | `guarda` | 🔴 `UB` | ✅ detectado | 🛑 |
| 147 | [`f_deque_push_front_it_bucle`](casos/deque/push_front.md#f_deque_push_front_it_bucle) | `deque` | `push_front` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 148 | [`f_deque_push_front_it_llamada`](casos/deque/push_front.md#f_deque_push_front_it_llamada) | `deque` | `push_front` | `it` | `llamada` | 🔴 `UB` | ✅ detectado | 🛑 |
| 149 | [`f_deque_push_front_ref_recto`](casos/deque/push_front.md#f_deque_push_front_ref_recto) | `deque` | `push_front` | `ref` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 150 | [`f_deque_push_front_ref_guarda`](casos/deque/push_front.md#f_deque_push_front_ref_guarda) | `deque` | `push_front` | `ref` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 151 | [`f_deque_push_front_ref_bucle`](casos/deque/push_front.md#f_deque_push_front_ref_bucle) | `deque` | `push_front` | `ref` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 152 | [`f_deque_push_front_ref_llamada`](casos/deque/push_front.md#f_deque_push_front_ref_llamada) | `deque` | `push_front` | `ref` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 153 | [`f_deque_push_front_ptr_recto`](casos/deque/push_front.md#f_deque_push_front_ptr_recto) | `deque` | `push_front` | `ptr` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 154 | [`f_deque_push_front_ptr_guarda`](casos/deque/push_front.md#f_deque_push_front_ptr_guarda) | `deque` | `push_front` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 155 | [`f_deque_push_front_ptr_bucle`](casos/deque/push_front.md#f_deque_push_front_ptr_bucle) | `deque` | `push_front` | `ptr` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 156 | [`f_deque_push_front_ptr_llamada`](casos/deque/push_front.md#f_deque_push_front_ptr_llamada) | `deque` | `push_front` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 157 | [`f_deque_emplace_back_it_recto`](casos/deque/emplace_back.md#f_deque_emplace_back_it_recto) | `deque` | `emplace_back` | `it` | `recto` | 🔴 `UB` | ✅ detectado | 🛑 |
| 158 | [`f_deque_emplace_back_it_guarda`](casos/deque/emplace_back.md#f_deque_emplace_back_it_guarda) | `deque` | `emplace_back` | `it` | `guarda` | 🔴 `UB` | ✅ detectado | 🛑 |
| 159 | [`f_deque_emplace_back_it_bucle`](casos/deque/emplace_back.md#f_deque_emplace_back_it_bucle) | `deque` | `emplace_back` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 160 | [`f_deque_emplace_back_it_llamada`](casos/deque/emplace_back.md#f_deque_emplace_back_it_llamada) | `deque` | `emplace_back` | `it` | `llamada` | 🔴 `UB` | ✅ detectado | 🛑 |
| 161 | [`f_deque_emplace_back_ref_recto`](casos/deque/emplace_back.md#f_deque_emplace_back_ref_recto) | `deque` | `emplace_back` | `ref` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 162 | [`f_deque_emplace_back_ref_guarda`](casos/deque/emplace_back.md#f_deque_emplace_back_ref_guarda) | `deque` | `emplace_back` | `ref` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 163 | [`f_deque_emplace_back_ref_bucle`](casos/deque/emplace_back.md#f_deque_emplace_back_ref_bucle) | `deque` | `emplace_back` | `ref` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 164 | [`f_deque_emplace_back_ref_llamada`](casos/deque/emplace_back.md#f_deque_emplace_back_ref_llamada) | `deque` | `emplace_back` | `ref` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 165 | [`f_deque_emplace_back_ptr_recto`](casos/deque/emplace_back.md#f_deque_emplace_back_ptr_recto) | `deque` | `emplace_back` | `ptr` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 166 | [`f_deque_emplace_back_ptr_guarda`](casos/deque/emplace_back.md#f_deque_emplace_back_ptr_guarda) | `deque` | `emplace_back` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 167 | [`f_deque_emplace_back_ptr_bucle`](casos/deque/emplace_back.md#f_deque_emplace_back_ptr_bucle) | `deque` | `emplace_back` | `ptr` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 168 | [`f_deque_emplace_back_ptr_llamada`](casos/deque/emplace_back.md#f_deque_emplace_back_ptr_llamada) | `deque` | `emplace_back` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 169 | [`f_deque_insert_middle_it_recto`](casos/deque/insert_middle.md#f_deque_insert_middle_it_recto) | `deque` | `insert_middle` | `it` | `recto` | 🔴 `UB` | ✅ detectado | 🛑 |
| 170 | [`f_deque_insert_middle_it_guarda`](casos/deque/insert_middle.md#f_deque_insert_middle_it_guarda) | `deque` | `insert_middle` | `it` | `guarda` | 🔴 `UB` | ✅ detectado | 🛑 |
| 171 | [`f_deque_insert_middle_it_bucle`](casos/deque/insert_middle.md#f_deque_insert_middle_it_bucle) | `deque` | `insert_middle` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 172 | [`f_deque_insert_middle_it_llamada`](casos/deque/insert_middle.md#f_deque_insert_middle_it_llamada) | `deque` | `insert_middle` | `it` | `llamada` | 🔴 `UB` | ✅ detectado | 🛑 |
| 173 | [`f_deque_insert_middle_ref_recto`](casos/deque/insert_middle.md#f_deque_insert_middle_ref_recto) | `deque` | `insert_middle` | `ref` | `recto` | 🔴 `UB` | ❌ falso negativo | — |
| 174 | [`f_deque_insert_middle_ref_guarda`](casos/deque/insert_middle.md#f_deque_insert_middle_ref_guarda) | `deque` | `insert_middle` | `ref` | `guarda` | 🔴 `UB` | ❌ falso negativo | — |
| 175 | [`f_deque_insert_middle_ref_bucle`](casos/deque/insert_middle.md#f_deque_insert_middle_ref_bucle) | `deque` | `insert_middle` | `ref` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 176 | [`f_deque_insert_middle_ref_llamada`](casos/deque/insert_middle.md#f_deque_insert_middle_ref_llamada) | `deque` | `insert_middle` | `ref` | `llamada` | 🔴 `UB` | ❌ falso negativo | — |
| 177 | [`f_deque_insert_middle_ptr_recto`](casos/deque/insert_middle.md#f_deque_insert_middle_ptr_recto) | `deque` | `insert_middle` | `ptr` | `recto` | 🔴 `UB` | ❌ falso negativo | — |
| 178 | [`f_deque_insert_middle_ptr_guarda`](casos/deque/insert_middle.md#f_deque_insert_middle_ptr_guarda) | `deque` | `insert_middle` | `ptr` | `guarda` | 🔴 `UB` | ❌ falso negativo | — |
| 179 | [`f_deque_insert_middle_ptr_bucle`](casos/deque/insert_middle.md#f_deque_insert_middle_ptr_bucle) | `deque` | `insert_middle` | `ptr` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 180 | [`f_deque_insert_middle_ptr_llamada`](casos/deque/insert_middle.md#f_deque_insert_middle_ptr_llamada) | `deque` | `insert_middle` | `ptr` | `llamada` | 🔴 `UB` | ❌ falso negativo | — |
| 181 | [`f_deque_erase_begin_it_recto`](casos/deque/erase_begin.md#f_deque_erase_begin_it_recto) | `deque` | `erase_begin` | `it` | `recto` | 🔴 `UB` | ✅ detectado | 🛑 |
| 182 | [`f_deque_erase_begin_it_guarda`](casos/deque/erase_begin.md#f_deque_erase_begin_it_guarda) | `deque` | `erase_begin` | `it` | `guarda` | 🔴 `UB` | ✅ detectado | 🛑 |
| 183 | [`f_deque_erase_begin_it_bucle`](casos/deque/erase_begin.md#f_deque_erase_begin_it_bucle) | `deque` | `erase_begin` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 184 | [`f_deque_erase_begin_it_llamada`](casos/deque/erase_begin.md#f_deque_erase_begin_it_llamada) | `deque` | `erase_begin` | `it` | `llamada` | 🔴 `UB` | ✅ detectado | 🛑 |
| 185 | [`f_deque_erase_begin_ref_recto`](casos/deque/erase_begin.md#f_deque_erase_begin_ref_recto) | `deque` | `erase_begin` | `ref` | `recto` | 🔴 `UB` | ❌ falso negativo | — |
| 186 | [`f_deque_erase_begin_ref_guarda`](casos/deque/erase_begin.md#f_deque_erase_begin_ref_guarda) | `deque` | `erase_begin` | `ref` | `guarda` | 🔴 `UB` | ❌ falso negativo | — |
| 187 | [`f_deque_erase_begin_ref_bucle`](casos/deque/erase_begin.md#f_deque_erase_begin_ref_bucle) | `deque` | `erase_begin` | `ref` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 188 | [`f_deque_erase_begin_ref_llamada`](casos/deque/erase_begin.md#f_deque_erase_begin_ref_llamada) | `deque` | `erase_begin` | `ref` | `llamada` | 🔴 `UB` | ❌ falso negativo | — |
| 189 | [`f_deque_erase_begin_ptr_recto`](casos/deque/erase_begin.md#f_deque_erase_begin_ptr_recto) | `deque` | `erase_begin` | `ptr` | `recto` | 🔴 `UB` | ❌ falso negativo | — |
| 190 | [`f_deque_erase_begin_ptr_guarda`](casos/deque/erase_begin.md#f_deque_erase_begin_ptr_guarda) | `deque` | `erase_begin` | `ptr` | `guarda` | 🔴 `UB` | ❌ falso negativo | — |
| 191 | [`f_deque_erase_begin_ptr_bucle`](casos/deque/erase_begin.md#f_deque_erase_begin_ptr_bucle) | `deque` | `erase_begin` | `ptr` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 192 | [`f_deque_erase_begin_ptr_llamada`](casos/deque/erase_begin.md#f_deque_erase_begin_ptr_llamada) | `deque` | `erase_begin` | `ptr` | `llamada` | 🔴 `UB` | ❌ falso negativo | — |
| 193 | [`f_deque_clear_it_recto`](casos/deque/clear.md#f_deque_clear_it_recto) | `deque` | `clear` | `it` | `recto` | 🔴 `UB` | ✅ detectado | 🛑 |
| 194 | [`f_deque_clear_it_guarda`](casos/deque/clear.md#f_deque_clear_it_guarda) | `deque` | `clear` | `it` | `guarda` | 🔴 `UB` | ✅ detectado | 🛑 |
| 195 | [`f_deque_clear_it_bucle`](casos/deque/clear.md#f_deque_clear_it_bucle) | `deque` | `clear` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 196 | [`f_deque_clear_it_llamada`](casos/deque/clear.md#f_deque_clear_it_llamada) | `deque` | `clear` | `it` | `llamada` | 🔴 `UB` | ✅ detectado | 🛑 |
| 197 | [`f_deque_clear_ref_recto`](casos/deque/clear.md#f_deque_clear_ref_recto) | `deque` | `clear` | `ref` | `recto` | 🔴 `UB` | ❌ falso negativo | — |
| 198 | [`f_deque_clear_ref_guarda`](casos/deque/clear.md#f_deque_clear_ref_guarda) | `deque` | `clear` | `ref` | `guarda` | 🔴 `UB` | ❌ falso negativo | — |
| 199 | [`f_deque_clear_ref_bucle`](casos/deque/clear.md#f_deque_clear_ref_bucle) | `deque` | `clear` | `ref` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 200 | [`f_deque_clear_ref_llamada`](casos/deque/clear.md#f_deque_clear_ref_llamada) | `deque` | `clear` | `ref` | `llamada` | 🔴 `UB` | ❌ falso negativo | — |
| 201 | [`f_deque_clear_ptr_recto`](casos/deque/clear.md#f_deque_clear_ptr_recto) | `deque` | `clear` | `ptr` | `recto` | 🔴 `UB` | ❌ falso negativo | — |
| 202 | [`f_deque_clear_ptr_guarda`](casos/deque/clear.md#f_deque_clear_ptr_guarda) | `deque` | `clear` | `ptr` | `guarda` | 🔴 `UB` | ❌ falso negativo | — |
| 203 | [`f_deque_clear_ptr_bucle`](casos/deque/clear.md#f_deque_clear_ptr_bucle) | `deque` | `clear` | `ptr` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 204 | [`f_deque_clear_ptr_llamada`](casos/deque/clear.md#f_deque_clear_ptr_llamada) | `deque` | `clear` | `ptr` | `llamada` | 🔴 `UB` | ❌ falso negativo | — |
| 205 | [`f_deque_resize_grow_it_recto`](casos/deque/resize_grow.md#f_deque_resize_grow_it_recto) | `deque` | `resize_grow` | `it` | `recto` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 206 | [`f_deque_resize_grow_it_guarda`](casos/deque/resize_grow.md#f_deque_resize_grow_it_guarda) | `deque` | `resize_grow` | `it` | `guarda` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 207 | [`f_deque_resize_grow_it_bucle`](casos/deque/resize_grow.md#f_deque_resize_grow_it_bucle) | `deque` | `resize_grow` | `it` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 208 | [`f_deque_resize_grow_it_llamada`](casos/deque/resize_grow.md#f_deque_resize_grow_it_llamada) | `deque` | `resize_grow` | `it` | `llamada` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 209 | [`f_deque_resize_grow_ref_recto`](casos/deque/resize_grow.md#f_deque_resize_grow_ref_recto) | `deque` | `resize_grow` | `ref` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 210 | [`f_deque_resize_grow_ref_guarda`](casos/deque/resize_grow.md#f_deque_resize_grow_ref_guarda) | `deque` | `resize_grow` | `ref` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 211 | [`f_deque_resize_grow_ref_bucle`](casos/deque/resize_grow.md#f_deque_resize_grow_ref_bucle) | `deque` | `resize_grow` | `ref` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 212 | [`f_deque_resize_grow_ref_llamada`](casos/deque/resize_grow.md#f_deque_resize_grow_ref_llamada) | `deque` | `resize_grow` | `ref` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 213 | [`f_deque_resize_grow_ptr_recto`](casos/deque/resize_grow.md#f_deque_resize_grow_ptr_recto) | `deque` | `resize_grow` | `ptr` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 214 | [`f_deque_resize_grow_ptr_guarda`](casos/deque/resize_grow.md#f_deque_resize_grow_ptr_guarda) | `deque` | `resize_grow` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 215 | [`f_deque_resize_grow_ptr_bucle`](casos/deque/resize_grow.md#f_deque_resize_grow_ptr_bucle) | `deque` | `resize_grow` | `ptr` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 216 | [`f_deque_resize_grow_ptr_llamada`](casos/deque/resize_grow.md#f_deque_resize_grow_ptr_llamada) | `deque` | `resize_grow` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 217 | [`f_deque_pop_front_it_recto`](casos/deque/pop_front.md#f_deque_pop_front_it_recto) | `deque` | `pop_front` | `it` | `recto` | 🔴 `UB` | ✅ detectado | 🛑 |
| 218 | [`f_deque_pop_front_it_guarda`](casos/deque/pop_front.md#f_deque_pop_front_it_guarda) | `deque` | `pop_front` | `it` | `guarda` | 🔴 `UB` | ✅ detectado | 🛑 |
| 219 | [`f_deque_pop_front_it_bucle`](casos/deque/pop_front.md#f_deque_pop_front_it_bucle) | `deque` | `pop_front` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 220 | [`f_deque_pop_front_it_llamada`](casos/deque/pop_front.md#f_deque_pop_front_it_llamada) | `deque` | `pop_front` | `it` | `llamada` | 🔴 `UB` | ✅ detectado | 🛑 |
| 221 | [`f_deque_pop_front_ref_recto`](casos/deque/pop_front.md#f_deque_pop_front_ref_recto) | `deque` | `pop_front` | `ref` | `recto` | 🔴 `UB` | ❌ falso negativo | — |
| 222 | [`f_deque_pop_front_ref_guarda`](casos/deque/pop_front.md#f_deque_pop_front_ref_guarda) | `deque` | `pop_front` | `ref` | `guarda` | 🔴 `UB` | ❌ falso negativo | — |
| 223 | [`f_deque_pop_front_ref_bucle`](casos/deque/pop_front.md#f_deque_pop_front_ref_bucle) | `deque` | `pop_front` | `ref` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 224 | [`f_deque_pop_front_ref_llamada`](casos/deque/pop_front.md#f_deque_pop_front_ref_llamada) | `deque` | `pop_front` | `ref` | `llamada` | 🔴 `UB` | ❌ falso negativo | — |
| 225 | [`f_deque_pop_front_ptr_recto`](casos/deque/pop_front.md#f_deque_pop_front_ptr_recto) | `deque` | `pop_front` | `ptr` | `recto` | 🔴 `UB` | ❌ falso negativo | — |
| 226 | [`f_deque_pop_front_ptr_guarda`](casos/deque/pop_front.md#f_deque_pop_front_ptr_guarda) | `deque` | `pop_front` | `ptr` | `guarda` | 🔴 `UB` | ❌ falso negativo | — |
| 227 | [`f_deque_pop_front_ptr_bucle`](casos/deque/pop_front.md#f_deque_pop_front_ptr_bucle) | `deque` | `pop_front` | `ptr` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 228 | [`f_deque_pop_front_ptr_llamada`](casos/deque/pop_front.md#f_deque_pop_front_ptr_llamada) | `deque` | `pop_front` | `ptr` | `llamada` | 🔴 `UB` | ❌ falso negativo | — |
| 229 | [`f_list_push_back_it_recto`](casos/list/push_back.md#f_list_push_back_it_recto) | `list` | `push_back` | `it` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 230 | [`f_list_push_back_it_guarda`](casos/list/push_back.md#f_list_push_back_it_guarda) | `list` | `push_back` | `it` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 231 | [`f_list_push_back_it_bucle`](casos/list/push_back.md#f_list_push_back_it_bucle) | `list` | `push_back` | `it` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 232 | [`f_list_push_back_it_llamada`](casos/list/push_back.md#f_list_push_back_it_llamada) | `list` | `push_back` | `it` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 233 | [`f_list_push_back_ref_recto`](casos/list/push_back.md#f_list_push_back_ref_recto) | `list` | `push_back` | `ref` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 234 | [`f_list_push_back_ref_guarda`](casos/list/push_back.md#f_list_push_back_ref_guarda) | `list` | `push_back` | `ref` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 235 | [`f_list_push_back_ref_bucle`](casos/list/push_back.md#f_list_push_back_ref_bucle) | `list` | `push_back` | `ref` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 236 | [`f_list_push_back_ref_llamada`](casos/list/push_back.md#f_list_push_back_ref_llamada) | `list` | `push_back` | `ref` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 237 | [`f_list_push_back_ptr_recto`](casos/list/push_back.md#f_list_push_back_ptr_recto) | `list` | `push_back` | `ptr` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 238 | [`f_list_push_back_ptr_guarda`](casos/list/push_back.md#f_list_push_back_ptr_guarda) | `list` | `push_back` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 239 | [`f_list_push_back_ptr_bucle`](casos/list/push_back.md#f_list_push_back_ptr_bucle) | `list` | `push_back` | `ptr` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 240 | [`f_list_push_back_ptr_llamada`](casos/list/push_back.md#f_list_push_back_ptr_llamada) | `list` | `push_back` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 241 | [`f_list_push_front_it_recto`](casos/list/push_front.md#f_list_push_front_it_recto) | `list` | `push_front` | `it` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 242 | [`f_list_push_front_it_guarda`](casos/list/push_front.md#f_list_push_front_it_guarda) | `list` | `push_front` | `it` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 243 | [`f_list_push_front_it_bucle`](casos/list/push_front.md#f_list_push_front_it_bucle) | `list` | `push_front` | `it` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 244 | [`f_list_push_front_it_llamada`](casos/list/push_front.md#f_list_push_front_it_llamada) | `list` | `push_front` | `it` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 245 | [`f_list_push_front_ref_recto`](casos/list/push_front.md#f_list_push_front_ref_recto) | `list` | `push_front` | `ref` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 246 | [`f_list_push_front_ref_guarda`](casos/list/push_front.md#f_list_push_front_ref_guarda) | `list` | `push_front` | `ref` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 247 | [`f_list_push_front_ref_bucle`](casos/list/push_front.md#f_list_push_front_ref_bucle) | `list` | `push_front` | `ref` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 248 | [`f_list_push_front_ref_llamada`](casos/list/push_front.md#f_list_push_front_ref_llamada) | `list` | `push_front` | `ref` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 249 | [`f_list_push_front_ptr_recto`](casos/list/push_front.md#f_list_push_front_ptr_recto) | `list` | `push_front` | `ptr` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 250 | [`f_list_push_front_ptr_guarda`](casos/list/push_front.md#f_list_push_front_ptr_guarda) | `list` | `push_front` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 251 | [`f_list_push_front_ptr_bucle`](casos/list/push_front.md#f_list_push_front_ptr_bucle) | `list` | `push_front` | `ptr` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 252 | [`f_list_push_front_ptr_llamada`](casos/list/push_front.md#f_list_push_front_ptr_llamada) | `list` | `push_front` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 253 | [`f_list_insert_it_recto`](casos/list/insert.md#f_list_insert_it_recto) | `list` | `insert` | `it` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 254 | [`f_list_insert_it_guarda`](casos/list/insert.md#f_list_insert_it_guarda) | `list` | `insert` | `it` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 255 | [`f_list_insert_it_bucle`](casos/list/insert.md#f_list_insert_it_bucle) | `list` | `insert` | `it` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 256 | [`f_list_insert_it_llamada`](casos/list/insert.md#f_list_insert_it_llamada) | `list` | `insert` | `it` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 257 | [`f_list_insert_ref_recto`](casos/list/insert.md#f_list_insert_ref_recto) | `list` | `insert` | `ref` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 258 | [`f_list_insert_ref_guarda`](casos/list/insert.md#f_list_insert_ref_guarda) | `list` | `insert` | `ref` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 259 | [`f_list_insert_ref_bucle`](casos/list/insert.md#f_list_insert_ref_bucle) | `list` | `insert` | `ref` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 260 | [`f_list_insert_ref_llamada`](casos/list/insert.md#f_list_insert_ref_llamada) | `list` | `insert` | `ref` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 261 | [`f_list_insert_ptr_recto`](casos/list/insert.md#f_list_insert_ptr_recto) | `list` | `insert` | `ptr` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 262 | [`f_list_insert_ptr_guarda`](casos/list/insert.md#f_list_insert_ptr_guarda) | `list` | `insert` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 263 | [`f_list_insert_ptr_bucle`](casos/list/insert.md#f_list_insert_ptr_bucle) | `list` | `insert` | `ptr` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 264 | [`f_list_insert_ptr_llamada`](casos/list/insert.md#f_list_insert_ptr_llamada) | `list` | `insert` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 265 | [`f_list_erase_begin_it_recto`](casos/list/erase_begin.md#f_list_erase_begin_it_recto) | `list` | `erase_begin` | `it` | `recto` | 🔴 `UB` | ✅ detectado | 🛑 |
| 266 | [`f_list_erase_begin_it_guarda`](casos/list/erase_begin.md#f_list_erase_begin_it_guarda) | `list` | `erase_begin` | `it` | `guarda` | 🔴 `UB` | ✅ detectado | 🛑 |
| 267 | [`f_list_erase_begin_it_bucle`](casos/list/erase_begin.md#f_list_erase_begin_it_bucle) | `list` | `erase_begin` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 268 | [`f_list_erase_begin_it_llamada`](casos/list/erase_begin.md#f_list_erase_begin_it_llamada) | `list` | `erase_begin` | `it` | `llamada` | 🔴 `UB` | ✅ detectado | 🛑 |
| 269 | [`f_list_erase_begin_ref_recto`](casos/list/erase_begin.md#f_list_erase_begin_ref_recto) | `list` | `erase_begin` | `ref` | `recto` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 270 | [`f_list_erase_begin_ref_guarda`](casos/list/erase_begin.md#f_list_erase_begin_ref_guarda) | `list` | `erase_begin` | `ref` | `guarda` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 271 | [`f_list_erase_begin_ref_bucle`](casos/list/erase_begin.md#f_list_erase_begin_ref_bucle) | `list` | `erase_begin` | `ref` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 272 | [`f_list_erase_begin_ref_llamada`](casos/list/erase_begin.md#f_list_erase_begin_ref_llamada) | `list` | `erase_begin` | `ref` | `llamada` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 273 | [`f_list_erase_begin_ptr_recto`](casos/list/erase_begin.md#f_list_erase_begin_ptr_recto) | `list` | `erase_begin` | `ptr` | `recto` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 274 | [`f_list_erase_begin_ptr_guarda`](casos/list/erase_begin.md#f_list_erase_begin_ptr_guarda) | `list` | `erase_begin` | `ptr` | `guarda` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 275 | [`f_list_erase_begin_ptr_bucle`](casos/list/erase_begin.md#f_list_erase_begin_ptr_bucle) | `list` | `erase_begin` | `ptr` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 276 | [`f_list_erase_begin_ptr_llamada`](casos/list/erase_begin.md#f_list_erase_begin_ptr_llamada) | `list` | `erase_begin` | `ptr` | `llamada` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 277 | [`f_list_clear_it_recto`](casos/list/clear.md#f_list_clear_it_recto) | `list` | `clear` | `it` | `recto` | 🔴 `UB` | ✅ detectado | 🛑 |
| 278 | [`f_list_clear_it_guarda`](casos/list/clear.md#f_list_clear_it_guarda) | `list` | `clear` | `it` | `guarda` | 🔴 `UB` | ✅ detectado | 🛑 |
| 279 | [`f_list_clear_it_bucle`](casos/list/clear.md#f_list_clear_it_bucle) | `list` | `clear` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 280 | [`f_list_clear_it_llamada`](casos/list/clear.md#f_list_clear_it_llamada) | `list` | `clear` | `it` | `llamada` | 🔴 `UB` | ✅ detectado | 🛑 |
| 281 | [`f_list_clear_ref_recto`](casos/list/clear.md#f_list_clear_ref_recto) | `list` | `clear` | `ref` | `recto` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 282 | [`f_list_clear_ref_guarda`](casos/list/clear.md#f_list_clear_ref_guarda) | `list` | `clear` | `ref` | `guarda` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 283 | [`f_list_clear_ref_bucle`](casos/list/clear.md#f_list_clear_ref_bucle) | `list` | `clear` | `ref` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 284 | [`f_list_clear_ref_llamada`](casos/list/clear.md#f_list_clear_ref_llamada) | `list` | `clear` | `ref` | `llamada` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 285 | [`f_list_clear_ptr_recto`](casos/list/clear.md#f_list_clear_ptr_recto) | `list` | `clear` | `ptr` | `recto` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 286 | [`f_list_clear_ptr_guarda`](casos/list/clear.md#f_list_clear_ptr_guarda) | `list` | `clear` | `ptr` | `guarda` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 287 | [`f_list_clear_ptr_bucle`](casos/list/clear.md#f_list_clear_ptr_bucle) | `list` | `clear` | `ptr` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 288 | [`f_list_clear_ptr_llamada`](casos/list/clear.md#f_list_clear_ptr_llamada) | `list` | `clear` | `ptr` | `llamada` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 289 | [`f_list_resize_grow_it_recto`](casos/list/resize_grow.md#f_list_resize_grow_it_recto) | `list` | `resize_grow` | `it` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 290 | [`f_list_resize_grow_it_guarda`](casos/list/resize_grow.md#f_list_resize_grow_it_guarda) | `list` | `resize_grow` | `it` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 291 | [`f_list_resize_grow_it_bucle`](casos/list/resize_grow.md#f_list_resize_grow_it_bucle) | `list` | `resize_grow` | `it` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 292 | [`f_list_resize_grow_it_llamada`](casos/list/resize_grow.md#f_list_resize_grow_it_llamada) | `list` | `resize_grow` | `it` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 293 | [`f_list_resize_grow_ref_recto`](casos/list/resize_grow.md#f_list_resize_grow_ref_recto) | `list` | `resize_grow` | `ref` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 294 | [`f_list_resize_grow_ref_guarda`](casos/list/resize_grow.md#f_list_resize_grow_ref_guarda) | `list` | `resize_grow` | `ref` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 295 | [`f_list_resize_grow_ref_bucle`](casos/list/resize_grow.md#f_list_resize_grow_ref_bucle) | `list` | `resize_grow` | `ref` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 296 | [`f_list_resize_grow_ref_llamada`](casos/list/resize_grow.md#f_list_resize_grow_ref_llamada) | `list` | `resize_grow` | `ref` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 297 | [`f_list_resize_grow_ptr_recto`](casos/list/resize_grow.md#f_list_resize_grow_ptr_recto) | `list` | `resize_grow` | `ptr` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 298 | [`f_list_resize_grow_ptr_guarda`](casos/list/resize_grow.md#f_list_resize_grow_ptr_guarda) | `list` | `resize_grow` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 299 | [`f_list_resize_grow_ptr_bucle`](casos/list/resize_grow.md#f_list_resize_grow_ptr_bucle) | `list` | `resize_grow` | `ptr` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 300 | [`f_list_resize_grow_ptr_llamada`](casos/list/resize_grow.md#f_list_resize_grow_ptr_llamada) | `list` | `resize_grow` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 301 | [`f_list_pop_front_it_recto`](casos/list/pop_front.md#f_list_pop_front_it_recto) | `list` | `pop_front` | `it` | `recto` | 🔴 `UB` | ✅ detectado | 🛑 |
| 302 | [`f_list_pop_front_it_guarda`](casos/list/pop_front.md#f_list_pop_front_it_guarda) | `list` | `pop_front` | `it` | `guarda` | 🔴 `UB` | ✅ detectado | 🛑 |
| 303 | [`f_list_pop_front_it_bucle`](casos/list/pop_front.md#f_list_pop_front_it_bucle) | `list` | `pop_front` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 304 | [`f_list_pop_front_it_llamada`](casos/list/pop_front.md#f_list_pop_front_it_llamada) | `list` | `pop_front` | `it` | `llamada` | 🔴 `UB` | ✅ detectado | 🛑 |
| 305 | [`f_list_pop_front_ref_recto`](casos/list/pop_front.md#f_list_pop_front_ref_recto) | `list` | `pop_front` | `ref` | `recto` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 306 | [`f_list_pop_front_ref_guarda`](casos/list/pop_front.md#f_list_pop_front_ref_guarda) | `list` | `pop_front` | `ref` | `guarda` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 307 | [`f_list_pop_front_ref_bucle`](casos/list/pop_front.md#f_list_pop_front_ref_bucle) | `list` | `pop_front` | `ref` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 308 | [`f_list_pop_front_ref_llamada`](casos/list/pop_front.md#f_list_pop_front_ref_llamada) | `list` | `pop_front` | `ref` | `llamada` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 309 | [`f_list_pop_front_ptr_recto`](casos/list/pop_front.md#f_list_pop_front_ptr_recto) | `list` | `pop_front` | `ptr` | `recto` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 310 | [`f_list_pop_front_ptr_guarda`](casos/list/pop_front.md#f_list_pop_front_ptr_guarda) | `list` | `pop_front` | `ptr` | `guarda` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 311 | [`f_list_pop_front_ptr_bucle`](casos/list/pop_front.md#f_list_pop_front_ptr_bucle) | `list` | `pop_front` | `ptr` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 312 | [`f_list_pop_front_ptr_llamada`](casos/list/pop_front.md#f_list_pop_front_ptr_llamada) | `list` | `pop_front` | `ptr` | `llamada` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 313 | [`f_list_reverse_it_recto`](casos/list/reverse.md#f_list_reverse_it_recto) | `list` | `reverse` | `it` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 314 | [`f_list_reverse_it_guarda`](casos/list/reverse.md#f_list_reverse_it_guarda) | `list` | `reverse` | `it` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 315 | [`f_list_reverse_it_bucle`](casos/list/reverse.md#f_list_reverse_it_bucle) | `list` | `reverse` | `it` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 316 | [`f_list_reverse_it_llamada`](casos/list/reverse.md#f_list_reverse_it_llamada) | `list` | `reverse` | `it` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 317 | [`f_list_reverse_ref_recto`](casos/list/reverse.md#f_list_reverse_ref_recto) | `list` | `reverse` | `ref` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 318 | [`f_list_reverse_ref_guarda`](casos/list/reverse.md#f_list_reverse_ref_guarda) | `list` | `reverse` | `ref` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 319 | [`f_list_reverse_ref_bucle`](casos/list/reverse.md#f_list_reverse_ref_bucle) | `list` | `reverse` | `ref` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 320 | [`f_list_reverse_ref_llamada`](casos/list/reverse.md#f_list_reverse_ref_llamada) | `list` | `reverse` | `ref` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 321 | [`f_list_reverse_ptr_recto`](casos/list/reverse.md#f_list_reverse_ptr_recto) | `list` | `reverse` | `ptr` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 322 | [`f_list_reverse_ptr_guarda`](casos/list/reverse.md#f_list_reverse_ptr_guarda) | `list` | `reverse` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 323 | [`f_list_reverse_ptr_bucle`](casos/list/reverse.md#f_list_reverse_ptr_bucle) | `list` | `reverse` | `ptr` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 324 | [`f_list_reverse_ptr_llamada`](casos/list/reverse.md#f_list_reverse_ptr_llamada) | `list` | `reverse` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 325 | [`f_list_sort_it_recto`](casos/list/sort.md#f_list_sort_it_recto) | `list` | `sort` | `it` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 326 | [`f_list_sort_it_guarda`](casos/list/sort.md#f_list_sort_it_guarda) | `list` | `sort` | `it` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 327 | [`f_list_sort_it_bucle`](casos/list/sort.md#f_list_sort_it_bucle) | `list` | `sort` | `it` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 328 | [`f_list_sort_it_llamada`](casos/list/sort.md#f_list_sort_it_llamada) | `list` | `sort` | `it` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 329 | [`f_list_sort_ref_recto`](casos/list/sort.md#f_list_sort_ref_recto) | `list` | `sort` | `ref` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 330 | [`f_list_sort_ref_guarda`](casos/list/sort.md#f_list_sort_ref_guarda) | `list` | `sort` | `ref` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 331 | [`f_list_sort_ref_bucle`](casos/list/sort.md#f_list_sort_ref_bucle) | `list` | `sort` | `ref` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 332 | [`f_list_sort_ref_llamada`](casos/list/sort.md#f_list_sort_ref_llamada) | `list` | `sort` | `ref` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 333 | [`f_list_sort_ptr_recto`](casos/list/sort.md#f_list_sort_ptr_recto) | `list` | `sort` | `ptr` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 334 | [`f_list_sort_ptr_guarda`](casos/list/sort.md#f_list_sort_ptr_guarda) | `list` | `sort` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 335 | [`f_list_sort_ptr_bucle`](casos/list/sort.md#f_list_sort_ptr_bucle) | `list` | `sort` | `ptr` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 336 | [`f_list_sort_ptr_llamada`](casos/list/sort.md#f_list_sort_ptr_llamada) | `list` | `sort` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 337 | [`f_flist_push_front_it_recto`](casos/flist/push_front.md#f_flist_push_front_it_recto) | `flist` | `push_front` | `it` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 338 | [`f_flist_push_front_it_guarda`](casos/flist/push_front.md#f_flist_push_front_it_guarda) | `flist` | `push_front` | `it` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 339 | [`f_flist_push_front_it_bucle`](casos/flist/push_front.md#f_flist_push_front_it_bucle) | `flist` | `push_front` | `it` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 340 | [`f_flist_push_front_it_llamada`](casos/flist/push_front.md#f_flist_push_front_it_llamada) | `flist` | `push_front` | `it` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 341 | [`f_flist_push_front_ref_recto`](casos/flist/push_front.md#f_flist_push_front_ref_recto) | `flist` | `push_front` | `ref` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 342 | [`f_flist_push_front_ref_guarda`](casos/flist/push_front.md#f_flist_push_front_ref_guarda) | `flist` | `push_front` | `ref` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 343 | [`f_flist_push_front_ref_bucle`](casos/flist/push_front.md#f_flist_push_front_ref_bucle) | `flist` | `push_front` | `ref` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 344 | [`f_flist_push_front_ref_llamada`](casos/flist/push_front.md#f_flist_push_front_ref_llamada) | `flist` | `push_front` | `ref` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 345 | [`f_flist_push_front_ptr_recto`](casos/flist/push_front.md#f_flist_push_front_ptr_recto) | `flist` | `push_front` | `ptr` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 346 | [`f_flist_push_front_ptr_guarda`](casos/flist/push_front.md#f_flist_push_front_ptr_guarda) | `flist` | `push_front` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 347 | [`f_flist_push_front_ptr_bucle`](casos/flist/push_front.md#f_flist_push_front_ptr_bucle) | `flist` | `push_front` | `ptr` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 348 | [`f_flist_push_front_ptr_llamada`](casos/flist/push_front.md#f_flist_push_front_ptr_llamada) | `flist` | `push_front` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 349 | [`f_flist_insert_after_it_recto`](casos/flist/insert_after.md#f_flist_insert_after_it_recto) | `flist` | `insert_after` | `it` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 350 | [`f_flist_insert_after_it_guarda`](casos/flist/insert_after.md#f_flist_insert_after_it_guarda) | `flist` | `insert_after` | `it` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 351 | [`f_flist_insert_after_it_bucle`](casos/flist/insert_after.md#f_flist_insert_after_it_bucle) | `flist` | `insert_after` | `it` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 352 | [`f_flist_insert_after_it_llamada`](casos/flist/insert_after.md#f_flist_insert_after_it_llamada) | `flist` | `insert_after` | `it` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 353 | [`f_flist_insert_after_ref_recto`](casos/flist/insert_after.md#f_flist_insert_after_ref_recto) | `flist` | `insert_after` | `ref` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 354 | [`f_flist_insert_after_ref_guarda`](casos/flist/insert_after.md#f_flist_insert_after_ref_guarda) | `flist` | `insert_after` | `ref` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 355 | [`f_flist_insert_after_ref_bucle`](casos/flist/insert_after.md#f_flist_insert_after_ref_bucle) | `flist` | `insert_after` | `ref` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 356 | [`f_flist_insert_after_ref_llamada`](casos/flist/insert_after.md#f_flist_insert_after_ref_llamada) | `flist` | `insert_after` | `ref` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 357 | [`f_flist_insert_after_ptr_recto`](casos/flist/insert_after.md#f_flist_insert_after_ptr_recto) | `flist` | `insert_after` | `ptr` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 358 | [`f_flist_insert_after_ptr_guarda`](casos/flist/insert_after.md#f_flist_insert_after_ptr_guarda) | `flist` | `insert_after` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 359 | [`f_flist_insert_after_ptr_bucle`](casos/flist/insert_after.md#f_flist_insert_after_ptr_bucle) | `flist` | `insert_after` | `ptr` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 360 | [`f_flist_insert_after_ptr_llamada`](casos/flist/insert_after.md#f_flist_insert_after_ptr_llamada) | `flist` | `insert_after` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 361 | [`f_flist_erase_after_it_recto`](casos/flist/erase_after.md#f_flist_erase_after_it_recto) | `flist` | `erase_after` | `it` | `recto` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 362 | [`f_flist_erase_after_it_guarda`](casos/flist/erase_after.md#f_flist_erase_after_it_guarda) | `flist` | `erase_after` | `it` | `guarda` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 363 | [`f_flist_erase_after_it_bucle`](casos/flist/erase_after.md#f_flist_erase_after_it_bucle) | `flist` | `erase_after` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 364 | [`f_flist_erase_after_it_llamada`](casos/flist/erase_after.md#f_flist_erase_after_it_llamada) | `flist` | `erase_after` | `it` | `llamada` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 365 | [`f_flist_erase_after_ref_recto`](casos/flist/erase_after.md#f_flist_erase_after_ref_recto) | `flist` | `erase_after` | `ref` | `recto` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 366 | [`f_flist_erase_after_ref_guarda`](casos/flist/erase_after.md#f_flist_erase_after_ref_guarda) | `flist` | `erase_after` | `ref` | `guarda` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 367 | [`f_flist_erase_after_ref_bucle`](casos/flist/erase_after.md#f_flist_erase_after_ref_bucle) | `flist` | `erase_after` | `ref` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 368 | [`f_flist_erase_after_ref_llamada`](casos/flist/erase_after.md#f_flist_erase_after_ref_llamada) | `flist` | `erase_after` | `ref` | `llamada` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 369 | [`f_flist_erase_after_ptr_recto`](casos/flist/erase_after.md#f_flist_erase_after_ptr_recto) | `flist` | `erase_after` | `ptr` | `recto` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 370 | [`f_flist_erase_after_ptr_guarda`](casos/flist/erase_after.md#f_flist_erase_after_ptr_guarda) | `flist` | `erase_after` | `ptr` | `guarda` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 371 | [`f_flist_erase_after_ptr_bucle`](casos/flist/erase_after.md#f_flist_erase_after_ptr_bucle) | `flist` | `erase_after` | `ptr` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 372 | [`f_flist_erase_after_ptr_llamada`](casos/flist/erase_after.md#f_flist_erase_after_ptr_llamada) | `flist` | `erase_after` | `ptr` | `llamada` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 373 | [`f_flist_clear_it_recto`](casos/flist/clear.md#f_flist_clear_it_recto) | `flist` | `clear` | `it` | `recto` | 🔴 `UB` | ✅ detectado | 🛑 |
| 374 | [`f_flist_clear_it_guarda`](casos/flist/clear.md#f_flist_clear_it_guarda) | `flist` | `clear` | `it` | `guarda` | 🔴 `UB` | ✅ detectado | 🛑 |
| 375 | [`f_flist_clear_it_bucle`](casos/flist/clear.md#f_flist_clear_it_bucle) | `flist` | `clear` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 376 | [`f_flist_clear_it_llamada`](casos/flist/clear.md#f_flist_clear_it_llamada) | `flist` | `clear` | `it` | `llamada` | 🔴 `UB` | ✅ detectado | 🛑 |
| 377 | [`f_flist_clear_ref_recto`](casos/flist/clear.md#f_flist_clear_ref_recto) | `flist` | `clear` | `ref` | `recto` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 378 | [`f_flist_clear_ref_guarda`](casos/flist/clear.md#f_flist_clear_ref_guarda) | `flist` | `clear` | `ref` | `guarda` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 379 | [`f_flist_clear_ref_bucle`](casos/flist/clear.md#f_flist_clear_ref_bucle) | `flist` | `clear` | `ref` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 380 | [`f_flist_clear_ref_llamada`](casos/flist/clear.md#f_flist_clear_ref_llamada) | `flist` | `clear` | `ref` | `llamada` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 381 | [`f_flist_clear_ptr_recto`](casos/flist/clear.md#f_flist_clear_ptr_recto) | `flist` | `clear` | `ptr` | `recto` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 382 | [`f_flist_clear_ptr_guarda`](casos/flist/clear.md#f_flist_clear_ptr_guarda) | `flist` | `clear` | `ptr` | `guarda` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 383 | [`f_flist_clear_ptr_bucle`](casos/flist/clear.md#f_flist_clear_ptr_bucle) | `flist` | `clear` | `ptr` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 384 | [`f_flist_clear_ptr_llamada`](casos/flist/clear.md#f_flist_clear_ptr_llamada) | `flist` | `clear` | `ptr` | `llamada` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 385 | [`f_set_insert_it_recto`](casos/set/insert.md#f_set_insert_it_recto) | `set` | `insert` | `it` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 386 | [`f_set_insert_it_guarda`](casos/set/insert.md#f_set_insert_it_guarda) | `set` | `insert` | `it` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 387 | [`f_set_insert_it_bucle`](casos/set/insert.md#f_set_insert_it_bucle) | `set` | `insert` | `it` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 388 | [`f_set_insert_it_llamada`](casos/set/insert.md#f_set_insert_it_llamada) | `set` | `insert` | `it` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 389 | [`f_set_insert_ref_recto`](casos/set/insert.md#f_set_insert_ref_recto) | `set` | `insert` | `ref` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 390 | [`f_set_insert_ref_guarda`](casos/set/insert.md#f_set_insert_ref_guarda) | `set` | `insert` | `ref` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 391 | [`f_set_insert_ref_bucle`](casos/set/insert.md#f_set_insert_ref_bucle) | `set` | `insert` | `ref` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 392 | [`f_set_insert_ref_llamada`](casos/set/insert.md#f_set_insert_ref_llamada) | `set` | `insert` | `ref` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 393 | [`f_set_insert_ptr_recto`](casos/set/insert.md#f_set_insert_ptr_recto) | `set` | `insert` | `ptr` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 394 | [`f_set_insert_ptr_guarda`](casos/set/insert.md#f_set_insert_ptr_guarda) | `set` | `insert` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 395 | [`f_set_insert_ptr_bucle`](casos/set/insert.md#f_set_insert_ptr_bucle) | `set` | `insert` | `ptr` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 396 | [`f_set_insert_ptr_llamada`](casos/set/insert.md#f_set_insert_ptr_llamada) | `set` | `insert` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 397 | [`f_set_emplace_it_recto`](casos/set/emplace.md#f_set_emplace_it_recto) | `set` | `emplace` | `it` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 398 | [`f_set_emplace_it_guarda`](casos/set/emplace.md#f_set_emplace_it_guarda) | `set` | `emplace` | `it` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 399 | [`f_set_emplace_it_bucle`](casos/set/emplace.md#f_set_emplace_it_bucle) | `set` | `emplace` | `it` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 400 | [`f_set_emplace_it_llamada`](casos/set/emplace.md#f_set_emplace_it_llamada) | `set` | `emplace` | `it` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 401 | [`f_set_emplace_ref_recto`](casos/set/emplace.md#f_set_emplace_ref_recto) | `set` | `emplace` | `ref` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 402 | [`f_set_emplace_ref_guarda`](casos/set/emplace.md#f_set_emplace_ref_guarda) | `set` | `emplace` | `ref` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 403 | [`f_set_emplace_ref_bucle`](casos/set/emplace.md#f_set_emplace_ref_bucle) | `set` | `emplace` | `ref` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 404 | [`f_set_emplace_ref_llamada`](casos/set/emplace.md#f_set_emplace_ref_llamada) | `set` | `emplace` | `ref` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 405 | [`f_set_emplace_ptr_recto`](casos/set/emplace.md#f_set_emplace_ptr_recto) | `set` | `emplace` | `ptr` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 406 | [`f_set_emplace_ptr_guarda`](casos/set/emplace.md#f_set_emplace_ptr_guarda) | `set` | `emplace` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 407 | [`f_set_emplace_ptr_bucle`](casos/set/emplace.md#f_set_emplace_ptr_bucle) | `set` | `emplace` | `ptr` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 408 | [`f_set_emplace_ptr_llamada`](casos/set/emplace.md#f_set_emplace_ptr_llamada) | `set` | `emplace` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 409 | [`f_set_erase_begin_it_recto`](casos/set/erase_begin.md#f_set_erase_begin_it_recto) | `set` | `erase_begin` | `it` | `recto` | 🔴 `UB` | ✅ detectado | 🛑 |
| 410 | [`f_set_erase_begin_it_guarda`](casos/set/erase_begin.md#f_set_erase_begin_it_guarda) | `set` | `erase_begin` | `it` | `guarda` | 🔴 `UB` | ✅ detectado | 🛑 |
| 411 | [`f_set_erase_begin_it_bucle`](casos/set/erase_begin.md#f_set_erase_begin_it_bucle) | `set` | `erase_begin` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 412 | [`f_set_erase_begin_it_llamada`](casos/set/erase_begin.md#f_set_erase_begin_it_llamada) | `set` | `erase_begin` | `it` | `llamada` | 🔴 `UB` | ✅ detectado | 🛑 |
| 413 | [`f_set_erase_begin_ref_recto`](casos/set/erase_begin.md#f_set_erase_begin_ref_recto) | `set` | `erase_begin` | `ref` | `recto` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 414 | [`f_set_erase_begin_ref_guarda`](casos/set/erase_begin.md#f_set_erase_begin_ref_guarda) | `set` | `erase_begin` | `ref` | `guarda` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 415 | [`f_set_erase_begin_ref_bucle`](casos/set/erase_begin.md#f_set_erase_begin_ref_bucle) | `set` | `erase_begin` | `ref` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 416 | [`f_set_erase_begin_ref_llamada`](casos/set/erase_begin.md#f_set_erase_begin_ref_llamada) | `set` | `erase_begin` | `ref` | `llamada` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 417 | [`f_set_erase_begin_ptr_recto`](casos/set/erase_begin.md#f_set_erase_begin_ptr_recto) | `set` | `erase_begin` | `ptr` | `recto` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 418 | [`f_set_erase_begin_ptr_guarda`](casos/set/erase_begin.md#f_set_erase_begin_ptr_guarda) | `set` | `erase_begin` | `ptr` | `guarda` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 419 | [`f_set_erase_begin_ptr_bucle`](casos/set/erase_begin.md#f_set_erase_begin_ptr_bucle) | `set` | `erase_begin` | `ptr` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 420 | [`f_set_erase_begin_ptr_llamada`](casos/set/erase_begin.md#f_set_erase_begin_ptr_llamada) | `set` | `erase_begin` | `ptr` | `llamada` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 421 | [`f_set_clear_it_recto`](casos/set/clear.md#f_set_clear_it_recto) | `set` | `clear` | `it` | `recto` | 🔴 `UB` | ✅ detectado | 🛑 |
| 422 | [`f_set_clear_it_guarda`](casos/set/clear.md#f_set_clear_it_guarda) | `set` | `clear` | `it` | `guarda` | 🔴 `UB` | ✅ detectado | 🛑 |
| 423 | [`f_set_clear_it_bucle`](casos/set/clear.md#f_set_clear_it_bucle) | `set` | `clear` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 424 | [`f_set_clear_it_llamada`](casos/set/clear.md#f_set_clear_it_llamada) | `set` | `clear` | `it` | `llamada` | 🔴 `UB` | ✅ detectado | 🛑 |
| 425 | [`f_set_clear_ref_recto`](casos/set/clear.md#f_set_clear_ref_recto) | `set` | `clear` | `ref` | `recto` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 426 | [`f_set_clear_ref_guarda`](casos/set/clear.md#f_set_clear_ref_guarda) | `set` | `clear` | `ref` | `guarda` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 427 | [`f_set_clear_ref_bucle`](casos/set/clear.md#f_set_clear_ref_bucle) | `set` | `clear` | `ref` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 428 | [`f_set_clear_ref_llamada`](casos/set/clear.md#f_set_clear_ref_llamada) | `set` | `clear` | `ref` | `llamada` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 429 | [`f_set_clear_ptr_recto`](casos/set/clear.md#f_set_clear_ptr_recto) | `set` | `clear` | `ptr` | `recto` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 430 | [`f_set_clear_ptr_guarda`](casos/set/clear.md#f_set_clear_ptr_guarda) | `set` | `clear` | `ptr` | `guarda` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 431 | [`f_set_clear_ptr_bucle`](casos/set/clear.md#f_set_clear_ptr_bucle) | `set` | `clear` | `ptr` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 432 | [`f_set_clear_ptr_llamada`](casos/set/clear.md#f_set_clear_ptr_llamada) | `set` | `clear` | `ptr` | `llamada` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 433 | [`f_mset_insert_it_recto`](casos/mset/insert.md#f_mset_insert_it_recto) | `mset` | `insert` | `it` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 434 | [`f_mset_insert_it_guarda`](casos/mset/insert.md#f_mset_insert_it_guarda) | `mset` | `insert` | `it` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 435 | [`f_mset_insert_it_bucle`](casos/mset/insert.md#f_mset_insert_it_bucle) | `mset` | `insert` | `it` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 436 | [`f_mset_insert_it_llamada`](casos/mset/insert.md#f_mset_insert_it_llamada) | `mset` | `insert` | `it` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 437 | [`f_mset_insert_ref_recto`](casos/mset/insert.md#f_mset_insert_ref_recto) | `mset` | `insert` | `ref` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 438 | [`f_mset_insert_ref_guarda`](casos/mset/insert.md#f_mset_insert_ref_guarda) | `mset` | `insert` | `ref` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 439 | [`f_mset_insert_ref_bucle`](casos/mset/insert.md#f_mset_insert_ref_bucle) | `mset` | `insert` | `ref` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 440 | [`f_mset_insert_ref_llamada`](casos/mset/insert.md#f_mset_insert_ref_llamada) | `mset` | `insert` | `ref` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 441 | [`f_mset_insert_ptr_recto`](casos/mset/insert.md#f_mset_insert_ptr_recto) | `mset` | `insert` | `ptr` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 442 | [`f_mset_insert_ptr_guarda`](casos/mset/insert.md#f_mset_insert_ptr_guarda) | `mset` | `insert` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 443 | [`f_mset_insert_ptr_bucle`](casos/mset/insert.md#f_mset_insert_ptr_bucle) | `mset` | `insert` | `ptr` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 444 | [`f_mset_insert_ptr_llamada`](casos/mset/insert.md#f_mset_insert_ptr_llamada) | `mset` | `insert` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 445 | [`f_mset_erase_begin_it_recto`](casos/mset/erase_begin.md#f_mset_erase_begin_it_recto) | `mset` | `erase_begin` | `it` | `recto` | 🔴 `UB` | ✅ detectado | 🛑 |
| 446 | [`f_mset_erase_begin_it_guarda`](casos/mset/erase_begin.md#f_mset_erase_begin_it_guarda) | `mset` | `erase_begin` | `it` | `guarda` | 🔴 `UB` | ✅ detectado | 🛑 |
| 447 | [`f_mset_erase_begin_it_bucle`](casos/mset/erase_begin.md#f_mset_erase_begin_it_bucle) | `mset` | `erase_begin` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 448 | [`f_mset_erase_begin_it_llamada`](casos/mset/erase_begin.md#f_mset_erase_begin_it_llamada) | `mset` | `erase_begin` | `it` | `llamada` | 🔴 `UB` | ✅ detectado | 🛑 |
| 449 | [`f_mset_erase_begin_ref_recto`](casos/mset/erase_begin.md#f_mset_erase_begin_ref_recto) | `mset` | `erase_begin` | `ref` | `recto` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 450 | [`f_mset_erase_begin_ref_guarda`](casos/mset/erase_begin.md#f_mset_erase_begin_ref_guarda) | `mset` | `erase_begin` | `ref` | `guarda` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 451 | [`f_mset_erase_begin_ref_bucle`](casos/mset/erase_begin.md#f_mset_erase_begin_ref_bucle) | `mset` | `erase_begin` | `ref` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 452 | [`f_mset_erase_begin_ref_llamada`](casos/mset/erase_begin.md#f_mset_erase_begin_ref_llamada) | `mset` | `erase_begin` | `ref` | `llamada` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 453 | [`f_mset_erase_begin_ptr_recto`](casos/mset/erase_begin.md#f_mset_erase_begin_ptr_recto) | `mset` | `erase_begin` | `ptr` | `recto` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 454 | [`f_mset_erase_begin_ptr_guarda`](casos/mset/erase_begin.md#f_mset_erase_begin_ptr_guarda) | `mset` | `erase_begin` | `ptr` | `guarda` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 455 | [`f_mset_erase_begin_ptr_bucle`](casos/mset/erase_begin.md#f_mset_erase_begin_ptr_bucle) | `mset` | `erase_begin` | `ptr` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 456 | [`f_mset_erase_begin_ptr_llamada`](casos/mset/erase_begin.md#f_mset_erase_begin_ptr_llamada) | `mset` | `erase_begin` | `ptr` | `llamada` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 457 | [`f_mset_clear_it_recto`](casos/mset/clear.md#f_mset_clear_it_recto) | `mset` | `clear` | `it` | `recto` | 🔴 `UB` | ✅ detectado | 🛑 |
| 458 | [`f_mset_clear_it_guarda`](casos/mset/clear.md#f_mset_clear_it_guarda) | `mset` | `clear` | `it` | `guarda` | 🔴 `UB` | ✅ detectado | 🛑 |
| 459 | [`f_mset_clear_it_bucle`](casos/mset/clear.md#f_mset_clear_it_bucle) | `mset` | `clear` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 460 | [`f_mset_clear_it_llamada`](casos/mset/clear.md#f_mset_clear_it_llamada) | `mset` | `clear` | `it` | `llamada` | 🔴 `UB` | ✅ detectado | 🛑 |
| 461 | [`f_mset_clear_ref_recto`](casos/mset/clear.md#f_mset_clear_ref_recto) | `mset` | `clear` | `ref` | `recto` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 462 | [`f_mset_clear_ref_guarda`](casos/mset/clear.md#f_mset_clear_ref_guarda) | `mset` | `clear` | `ref` | `guarda` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 463 | [`f_mset_clear_ref_bucle`](casos/mset/clear.md#f_mset_clear_ref_bucle) | `mset` | `clear` | `ref` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 464 | [`f_mset_clear_ref_llamada`](casos/mset/clear.md#f_mset_clear_ref_llamada) | `mset` | `clear` | `ref` | `llamada` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 465 | [`f_mset_clear_ptr_recto`](casos/mset/clear.md#f_mset_clear_ptr_recto) | `mset` | `clear` | `ptr` | `recto` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 466 | [`f_mset_clear_ptr_guarda`](casos/mset/clear.md#f_mset_clear_ptr_guarda) | `mset` | `clear` | `ptr` | `guarda` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 467 | [`f_mset_clear_ptr_bucle`](casos/mset/clear.md#f_mset_clear_ptr_bucle) | `mset` | `clear` | `ptr` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 468 | [`f_mset_clear_ptr_llamada`](casos/mset/clear.md#f_mset_clear_ptr_llamada) | `mset` | `clear` | `ptr` | `llamada` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 469 | [`f_map_insert_it_recto`](casos/map/insert.md#f_map_insert_it_recto) | `map` | `insert` | `it` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 470 | [`f_map_insert_it_guarda`](casos/map/insert.md#f_map_insert_it_guarda) | `map` | `insert` | `it` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 471 | [`f_map_insert_it_bucle`](casos/map/insert.md#f_map_insert_it_bucle) | `map` | `insert` | `it` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 472 | [`f_map_insert_it_llamada`](casos/map/insert.md#f_map_insert_it_llamada) | `map` | `insert` | `it` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 473 | [`f_map_insert_ref_recto`](casos/map/insert.md#f_map_insert_ref_recto) | `map` | `insert` | `ref` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 474 | [`f_map_insert_ref_guarda`](casos/map/insert.md#f_map_insert_ref_guarda) | `map` | `insert` | `ref` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 475 | [`f_map_insert_ref_bucle`](casos/map/insert.md#f_map_insert_ref_bucle) | `map` | `insert` | `ref` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 476 | [`f_map_insert_ref_llamada`](casos/map/insert.md#f_map_insert_ref_llamada) | `map` | `insert` | `ref` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 477 | [`f_map_insert_ptr_recto`](casos/map/insert.md#f_map_insert_ptr_recto) | `map` | `insert` | `ptr` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 478 | [`f_map_insert_ptr_guarda`](casos/map/insert.md#f_map_insert_ptr_guarda) | `map` | `insert` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 479 | [`f_map_insert_ptr_bucle`](casos/map/insert.md#f_map_insert_ptr_bucle) | `map` | `insert` | `ptr` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 480 | [`f_map_insert_ptr_llamada`](casos/map/insert.md#f_map_insert_ptr_llamada) | `map` | `insert` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 481 | [`f_map_emplace_it_recto`](casos/map/emplace.md#f_map_emplace_it_recto) | `map` | `emplace` | `it` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 482 | [`f_map_emplace_it_guarda`](casos/map/emplace.md#f_map_emplace_it_guarda) | `map` | `emplace` | `it` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 483 | [`f_map_emplace_it_bucle`](casos/map/emplace.md#f_map_emplace_it_bucle) | `map` | `emplace` | `it` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 484 | [`f_map_emplace_it_llamada`](casos/map/emplace.md#f_map_emplace_it_llamada) | `map` | `emplace` | `it` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 485 | [`f_map_emplace_ref_recto`](casos/map/emplace.md#f_map_emplace_ref_recto) | `map` | `emplace` | `ref` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 486 | [`f_map_emplace_ref_guarda`](casos/map/emplace.md#f_map_emplace_ref_guarda) | `map` | `emplace` | `ref` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 487 | [`f_map_emplace_ref_bucle`](casos/map/emplace.md#f_map_emplace_ref_bucle) | `map` | `emplace` | `ref` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 488 | [`f_map_emplace_ref_llamada`](casos/map/emplace.md#f_map_emplace_ref_llamada) | `map` | `emplace` | `ref` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 489 | [`f_map_emplace_ptr_recto`](casos/map/emplace.md#f_map_emplace_ptr_recto) | `map` | `emplace` | `ptr` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 490 | [`f_map_emplace_ptr_guarda`](casos/map/emplace.md#f_map_emplace_ptr_guarda) | `map` | `emplace` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 491 | [`f_map_emplace_ptr_bucle`](casos/map/emplace.md#f_map_emplace_ptr_bucle) | `map` | `emplace` | `ptr` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 492 | [`f_map_emplace_ptr_llamada`](casos/map/emplace.md#f_map_emplace_ptr_llamada) | `map` | `emplace` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 493 | [`f_map_subscript_it_recto`](casos/map/subscript.md#f_map_subscript_it_recto) | `map` | `subscript` | `it` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 494 | [`f_map_subscript_it_guarda`](casos/map/subscript.md#f_map_subscript_it_guarda) | `map` | `subscript` | `it` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 495 | [`f_map_subscript_it_bucle`](casos/map/subscript.md#f_map_subscript_it_bucle) | `map` | `subscript` | `it` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 496 | [`f_map_subscript_it_llamada`](casos/map/subscript.md#f_map_subscript_it_llamada) | `map` | `subscript` | `it` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 497 | [`f_map_subscript_ref_recto`](casos/map/subscript.md#f_map_subscript_ref_recto) | `map` | `subscript` | `ref` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 498 | [`f_map_subscript_ref_guarda`](casos/map/subscript.md#f_map_subscript_ref_guarda) | `map` | `subscript` | `ref` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 499 | [`f_map_subscript_ref_bucle`](casos/map/subscript.md#f_map_subscript_ref_bucle) | `map` | `subscript` | `ref` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 500 | [`f_map_subscript_ref_llamada`](casos/map/subscript.md#f_map_subscript_ref_llamada) | `map` | `subscript` | `ref` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 501 | [`f_map_subscript_ptr_recto`](casos/map/subscript.md#f_map_subscript_ptr_recto) | `map` | `subscript` | `ptr` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 502 | [`f_map_subscript_ptr_guarda`](casos/map/subscript.md#f_map_subscript_ptr_guarda) | `map` | `subscript` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 503 | [`f_map_subscript_ptr_bucle`](casos/map/subscript.md#f_map_subscript_ptr_bucle) | `map` | `subscript` | `ptr` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 504 | [`f_map_subscript_ptr_llamada`](casos/map/subscript.md#f_map_subscript_ptr_llamada) | `map` | `subscript` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 505 | [`f_map_erase_begin_it_recto`](casos/map/erase_begin.md#f_map_erase_begin_it_recto) | `map` | `erase_begin` | `it` | `recto` | 🔴 `UB` | ✅ detectado | 🛑 |
| 506 | [`f_map_erase_begin_it_guarda`](casos/map/erase_begin.md#f_map_erase_begin_it_guarda) | `map` | `erase_begin` | `it` | `guarda` | 🔴 `UB` | ✅ detectado | 🛑 |
| 507 | [`f_map_erase_begin_it_bucle`](casos/map/erase_begin.md#f_map_erase_begin_it_bucle) | `map` | `erase_begin` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 508 | [`f_map_erase_begin_it_llamada`](casos/map/erase_begin.md#f_map_erase_begin_it_llamada) | `map` | `erase_begin` | `it` | `llamada` | 🔴 `UB` | ✅ detectado | 🛑 |
| 509 | [`f_map_erase_begin_ref_recto`](casos/map/erase_begin.md#f_map_erase_begin_ref_recto) | `map` | `erase_begin` | `ref` | `recto` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 510 | [`f_map_erase_begin_ref_guarda`](casos/map/erase_begin.md#f_map_erase_begin_ref_guarda) | `map` | `erase_begin` | `ref` | `guarda` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 511 | [`f_map_erase_begin_ref_bucle`](casos/map/erase_begin.md#f_map_erase_begin_ref_bucle) | `map` | `erase_begin` | `ref` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 512 | [`f_map_erase_begin_ref_llamada`](casos/map/erase_begin.md#f_map_erase_begin_ref_llamada) | `map` | `erase_begin` | `ref` | `llamada` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 513 | [`f_map_erase_begin_ptr_recto`](casos/map/erase_begin.md#f_map_erase_begin_ptr_recto) | `map` | `erase_begin` | `ptr` | `recto` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 514 | [`f_map_erase_begin_ptr_guarda`](casos/map/erase_begin.md#f_map_erase_begin_ptr_guarda) | `map` | `erase_begin` | `ptr` | `guarda` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 515 | [`f_map_erase_begin_ptr_bucle`](casos/map/erase_begin.md#f_map_erase_begin_ptr_bucle) | `map` | `erase_begin` | `ptr` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 516 | [`f_map_erase_begin_ptr_llamada`](casos/map/erase_begin.md#f_map_erase_begin_ptr_llamada) | `map` | `erase_begin` | `ptr` | `llamada` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 517 | [`f_map_clear_it_recto`](casos/map/clear.md#f_map_clear_it_recto) | `map` | `clear` | `it` | `recto` | 🔴 `UB` | ✅ detectado | 🛑 |
| 518 | [`f_map_clear_it_guarda`](casos/map/clear.md#f_map_clear_it_guarda) | `map` | `clear` | `it` | `guarda` | 🔴 `UB` | ✅ detectado | 🛑 |
| 519 | [`f_map_clear_it_bucle`](casos/map/clear.md#f_map_clear_it_bucle) | `map` | `clear` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 520 | [`f_map_clear_it_llamada`](casos/map/clear.md#f_map_clear_it_llamada) | `map` | `clear` | `it` | `llamada` | 🔴 `UB` | ✅ detectado | 🛑 |
| 521 | [`f_map_clear_ref_recto`](casos/map/clear.md#f_map_clear_ref_recto) | `map` | `clear` | `ref` | `recto` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 522 | [`f_map_clear_ref_guarda`](casos/map/clear.md#f_map_clear_ref_guarda) | `map` | `clear` | `ref` | `guarda` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 523 | [`f_map_clear_ref_bucle`](casos/map/clear.md#f_map_clear_ref_bucle) | `map` | `clear` | `ref` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 524 | [`f_map_clear_ref_llamada`](casos/map/clear.md#f_map_clear_ref_llamada) | `map` | `clear` | `ref` | `llamada` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 525 | [`f_map_clear_ptr_recto`](casos/map/clear.md#f_map_clear_ptr_recto) | `map` | `clear` | `ptr` | `recto` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 526 | [`f_map_clear_ptr_guarda`](casos/map/clear.md#f_map_clear_ptr_guarda) | `map` | `clear` | `ptr` | `guarda` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 527 | [`f_map_clear_ptr_bucle`](casos/map/clear.md#f_map_clear_ptr_bucle) | `map` | `clear` | `ptr` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 528 | [`f_map_clear_ptr_llamada`](casos/map/clear.md#f_map_clear_ptr_llamada) | `map` | `clear` | `ptr` | `llamada` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 529 | [`f_mmap_insert_it_recto`](casos/mmap/insert.md#f_mmap_insert_it_recto) | `mmap` | `insert` | `it` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 530 | [`f_mmap_insert_it_guarda`](casos/mmap/insert.md#f_mmap_insert_it_guarda) | `mmap` | `insert` | `it` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 531 | [`f_mmap_insert_it_bucle`](casos/mmap/insert.md#f_mmap_insert_it_bucle) | `mmap` | `insert` | `it` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 532 | [`f_mmap_insert_it_llamada`](casos/mmap/insert.md#f_mmap_insert_it_llamada) | `mmap` | `insert` | `it` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 533 | [`f_mmap_insert_ref_recto`](casos/mmap/insert.md#f_mmap_insert_ref_recto) | `mmap` | `insert` | `ref` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 534 | [`f_mmap_insert_ref_guarda`](casos/mmap/insert.md#f_mmap_insert_ref_guarda) | `mmap` | `insert` | `ref` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 535 | [`f_mmap_insert_ref_bucle`](casos/mmap/insert.md#f_mmap_insert_ref_bucle) | `mmap` | `insert` | `ref` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 536 | [`f_mmap_insert_ref_llamada`](casos/mmap/insert.md#f_mmap_insert_ref_llamada) | `mmap` | `insert` | `ref` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 537 | [`f_mmap_insert_ptr_recto`](casos/mmap/insert.md#f_mmap_insert_ptr_recto) | `mmap` | `insert` | `ptr` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 538 | [`f_mmap_insert_ptr_guarda`](casos/mmap/insert.md#f_mmap_insert_ptr_guarda) | `mmap` | `insert` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 539 | [`f_mmap_insert_ptr_bucle`](casos/mmap/insert.md#f_mmap_insert_ptr_bucle) | `mmap` | `insert` | `ptr` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 540 | [`f_mmap_insert_ptr_llamada`](casos/mmap/insert.md#f_mmap_insert_ptr_llamada) | `mmap` | `insert` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 541 | [`f_mmap_erase_begin_it_recto`](casos/mmap/erase_begin.md#f_mmap_erase_begin_it_recto) | `mmap` | `erase_begin` | `it` | `recto` | 🔴 `UB` | ✅ detectado | 🛑 |
| 542 | [`f_mmap_erase_begin_it_guarda`](casos/mmap/erase_begin.md#f_mmap_erase_begin_it_guarda) | `mmap` | `erase_begin` | `it` | `guarda` | 🔴 `UB` | ✅ detectado | 🛑 |
| 543 | [`f_mmap_erase_begin_it_bucle`](casos/mmap/erase_begin.md#f_mmap_erase_begin_it_bucle) | `mmap` | `erase_begin` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 544 | [`f_mmap_erase_begin_it_llamada`](casos/mmap/erase_begin.md#f_mmap_erase_begin_it_llamada) | `mmap` | `erase_begin` | `it` | `llamada` | 🔴 `UB` | ✅ detectado | 🛑 |
| 545 | [`f_mmap_erase_begin_ref_recto`](casos/mmap/erase_begin.md#f_mmap_erase_begin_ref_recto) | `mmap` | `erase_begin` | `ref` | `recto` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 546 | [`f_mmap_erase_begin_ref_guarda`](casos/mmap/erase_begin.md#f_mmap_erase_begin_ref_guarda) | `mmap` | `erase_begin` | `ref` | `guarda` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 547 | [`f_mmap_erase_begin_ref_bucle`](casos/mmap/erase_begin.md#f_mmap_erase_begin_ref_bucle) | `mmap` | `erase_begin` | `ref` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 548 | [`f_mmap_erase_begin_ref_llamada`](casos/mmap/erase_begin.md#f_mmap_erase_begin_ref_llamada) | `mmap` | `erase_begin` | `ref` | `llamada` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 549 | [`f_mmap_erase_begin_ptr_recto`](casos/mmap/erase_begin.md#f_mmap_erase_begin_ptr_recto) | `mmap` | `erase_begin` | `ptr` | `recto` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 550 | [`f_mmap_erase_begin_ptr_guarda`](casos/mmap/erase_begin.md#f_mmap_erase_begin_ptr_guarda) | `mmap` | `erase_begin` | `ptr` | `guarda` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 551 | [`f_mmap_erase_begin_ptr_bucle`](casos/mmap/erase_begin.md#f_mmap_erase_begin_ptr_bucle) | `mmap` | `erase_begin` | `ptr` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 552 | [`f_mmap_erase_begin_ptr_llamada`](casos/mmap/erase_begin.md#f_mmap_erase_begin_ptr_llamada) | `mmap` | `erase_begin` | `ptr` | `llamada` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 553 | [`f_mmap_clear_it_recto`](casos/mmap/clear.md#f_mmap_clear_it_recto) | `mmap` | `clear` | `it` | `recto` | 🔴 `UB` | ✅ detectado | 🛑 |
| 554 | [`f_mmap_clear_it_guarda`](casos/mmap/clear.md#f_mmap_clear_it_guarda) | `mmap` | `clear` | `it` | `guarda` | 🔴 `UB` | ✅ detectado | 🛑 |
| 555 | [`f_mmap_clear_it_bucle`](casos/mmap/clear.md#f_mmap_clear_it_bucle) | `mmap` | `clear` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 556 | [`f_mmap_clear_it_llamada`](casos/mmap/clear.md#f_mmap_clear_it_llamada) | `mmap` | `clear` | `it` | `llamada` | 🔴 `UB` | ✅ detectado | 🛑 |
| 557 | [`f_mmap_clear_ref_recto`](casos/mmap/clear.md#f_mmap_clear_ref_recto) | `mmap` | `clear` | `ref` | `recto` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 558 | [`f_mmap_clear_ref_guarda`](casos/mmap/clear.md#f_mmap_clear_ref_guarda) | `mmap` | `clear` | `ref` | `guarda` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 559 | [`f_mmap_clear_ref_bucle`](casos/mmap/clear.md#f_mmap_clear_ref_bucle) | `mmap` | `clear` | `ref` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 560 | [`f_mmap_clear_ref_llamada`](casos/mmap/clear.md#f_mmap_clear_ref_llamada) | `mmap` | `clear` | `ref` | `llamada` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 561 | [`f_mmap_clear_ptr_recto`](casos/mmap/clear.md#f_mmap_clear_ptr_recto) | `mmap` | `clear` | `ptr` | `recto` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 562 | [`f_mmap_clear_ptr_guarda`](casos/mmap/clear.md#f_mmap_clear_ptr_guarda) | `mmap` | `clear` | `ptr` | `guarda` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 563 | [`f_mmap_clear_ptr_bucle`](casos/mmap/clear.md#f_mmap_clear_ptr_bucle) | `mmap` | `clear` | `ptr` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 564 | [`f_mmap_clear_ptr_llamada`](casos/mmap/clear.md#f_mmap_clear_ptr_llamada) | `mmap` | `clear` | `ptr` | `llamada` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 565 | [`f_uset_insert_it_recto`](casos/uset/insert.md#f_uset_insert_it_recto) | `uset` | `insert` | `it` | `recto` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 566 | [`f_uset_insert_it_guarda`](casos/uset/insert.md#f_uset_insert_it_guarda) | `uset` | `insert` | `it` | `guarda` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 567 | [`f_uset_insert_it_bucle`](casos/uset/insert.md#f_uset_insert_it_bucle) | `uset` | `insert` | `it` | `bucle` | 🔴 `UB` | ❌ falso negativo | — |
| 568 | [`f_uset_insert_it_llamada`](casos/uset/insert.md#f_uset_insert_it_llamada) | `uset` | `insert` | `it` | `llamada` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 569 | [`f_uset_insert_ref_recto`](casos/uset/insert.md#f_uset_insert_ref_recto) | `uset` | `insert` | `ref` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 570 | [`f_uset_insert_ref_guarda`](casos/uset/insert.md#f_uset_insert_ref_guarda) | `uset` | `insert` | `ref` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 571 | [`f_uset_insert_ref_bucle`](casos/uset/insert.md#f_uset_insert_ref_bucle) | `uset` | `insert` | `ref` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 572 | [`f_uset_insert_ref_llamada`](casos/uset/insert.md#f_uset_insert_ref_llamada) | `uset` | `insert` | `ref` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 573 | [`f_uset_insert_ptr_recto`](casos/uset/insert.md#f_uset_insert_ptr_recto) | `uset` | `insert` | `ptr` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 574 | [`f_uset_insert_ptr_guarda`](casos/uset/insert.md#f_uset_insert_ptr_guarda) | `uset` | `insert` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 575 | [`f_uset_insert_ptr_bucle`](casos/uset/insert.md#f_uset_insert_ptr_bucle) | `uset` | `insert` | `ptr` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 576 | [`f_uset_insert_ptr_llamada`](casos/uset/insert.md#f_uset_insert_ptr_llamada) | `uset` | `insert` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 577 | [`f_uset_erase_begin_it_recto`](casos/uset/erase_begin.md#f_uset_erase_begin_it_recto) | `uset` | `erase_begin` | `it` | `recto` | 🔴 `UB` | ✅ detectado | 🛑 |
| 578 | [`f_uset_erase_begin_it_guarda`](casos/uset/erase_begin.md#f_uset_erase_begin_it_guarda) | `uset` | `erase_begin` | `it` | `guarda` | 🔴 `UB` | ✅ detectado | 🛑 |
| 579 | [`f_uset_erase_begin_it_bucle`](casos/uset/erase_begin.md#f_uset_erase_begin_it_bucle) | `uset` | `erase_begin` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 580 | [`f_uset_erase_begin_it_llamada`](casos/uset/erase_begin.md#f_uset_erase_begin_it_llamada) | `uset` | `erase_begin` | `it` | `llamada` | 🔴 `UB` | ✅ detectado | 🛑 |
| 581 | [`f_uset_erase_begin_ref_recto`](casos/uset/erase_begin.md#f_uset_erase_begin_ref_recto) | `uset` | `erase_begin` | `ref` | `recto` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 582 | [`f_uset_erase_begin_ref_guarda`](casos/uset/erase_begin.md#f_uset_erase_begin_ref_guarda) | `uset` | `erase_begin` | `ref` | `guarda` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 583 | [`f_uset_erase_begin_ref_bucle`](casos/uset/erase_begin.md#f_uset_erase_begin_ref_bucle) | `uset` | `erase_begin` | `ref` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 584 | [`f_uset_erase_begin_ref_llamada`](casos/uset/erase_begin.md#f_uset_erase_begin_ref_llamada) | `uset` | `erase_begin` | `ref` | `llamada` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 585 | [`f_uset_erase_begin_ptr_recto`](casos/uset/erase_begin.md#f_uset_erase_begin_ptr_recto) | `uset` | `erase_begin` | `ptr` | `recto` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 586 | [`f_uset_erase_begin_ptr_guarda`](casos/uset/erase_begin.md#f_uset_erase_begin_ptr_guarda) | `uset` | `erase_begin` | `ptr` | `guarda` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 587 | [`f_uset_erase_begin_ptr_bucle`](casos/uset/erase_begin.md#f_uset_erase_begin_ptr_bucle) | `uset` | `erase_begin` | `ptr` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 588 | [`f_uset_erase_begin_ptr_llamada`](casos/uset/erase_begin.md#f_uset_erase_begin_ptr_llamada) | `uset` | `erase_begin` | `ptr` | `llamada` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 589 | [`f_uset_clear_it_recto`](casos/uset/clear.md#f_uset_clear_it_recto) | `uset` | `clear` | `it` | `recto` | 🔴 `UB` | ✅ detectado | 🛑 |
| 590 | [`f_uset_clear_it_guarda`](casos/uset/clear.md#f_uset_clear_it_guarda) | `uset` | `clear` | `it` | `guarda` | 🔴 `UB` | ✅ detectado | 🛑 |
| 591 | [`f_uset_clear_it_bucle`](casos/uset/clear.md#f_uset_clear_it_bucle) | `uset` | `clear` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 592 | [`f_uset_clear_it_llamada`](casos/uset/clear.md#f_uset_clear_it_llamada) | `uset` | `clear` | `it` | `llamada` | 🔴 `UB` | ✅ detectado | 🛑 |
| 593 | [`f_uset_clear_ref_recto`](casos/uset/clear.md#f_uset_clear_ref_recto) | `uset` | `clear` | `ref` | `recto` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 594 | [`f_uset_clear_ref_guarda`](casos/uset/clear.md#f_uset_clear_ref_guarda) | `uset` | `clear` | `ref` | `guarda` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 595 | [`f_uset_clear_ref_bucle`](casos/uset/clear.md#f_uset_clear_ref_bucle) | `uset` | `clear` | `ref` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 596 | [`f_uset_clear_ref_llamada`](casos/uset/clear.md#f_uset_clear_ref_llamada) | `uset` | `clear` | `ref` | `llamada` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 597 | [`f_uset_clear_ptr_recto`](casos/uset/clear.md#f_uset_clear_ptr_recto) | `uset` | `clear` | `ptr` | `recto` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 598 | [`f_uset_clear_ptr_guarda`](casos/uset/clear.md#f_uset_clear_ptr_guarda) | `uset` | `clear` | `ptr` | `guarda` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 599 | [`f_uset_clear_ptr_bucle`](casos/uset/clear.md#f_uset_clear_ptr_bucle) | `uset` | `clear` | `ptr` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 600 | [`f_uset_clear_ptr_llamada`](casos/uset/clear.md#f_uset_clear_ptr_llamada) | `uset` | `clear` | `ptr` | `llamada` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 601 | [`f_uset_rehash_it_recto`](casos/uset/rehash.md#f_uset_rehash_it_recto) | `uset` | `rehash` | `it` | `recto` | 🔴 `UB` | ❌ falso negativo | — |
| 602 | [`f_uset_rehash_it_guarda`](casos/uset/rehash.md#f_uset_rehash_it_guarda) | `uset` | `rehash` | `it` | `guarda` | 🔴 `UB` | ❌ falso negativo | — |
| 603 | [`f_uset_rehash_it_bucle`](casos/uset/rehash.md#f_uset_rehash_it_bucle) | `uset` | `rehash` | `it` | `bucle` | 🔴 `UB` | ❌ falso negativo | — |
| 604 | [`f_uset_rehash_it_llamada`](casos/uset/rehash.md#f_uset_rehash_it_llamada) | `uset` | `rehash` | `it` | `llamada` | 🔴 `UB` | ❌ falso negativo | — |
| 605 | [`f_uset_rehash_ref_recto`](casos/uset/rehash.md#f_uset_rehash_ref_recto) | `uset` | `rehash` | `ref` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 606 | [`f_uset_rehash_ref_guarda`](casos/uset/rehash.md#f_uset_rehash_ref_guarda) | `uset` | `rehash` | `ref` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 607 | [`f_uset_rehash_ref_bucle`](casos/uset/rehash.md#f_uset_rehash_ref_bucle) | `uset` | `rehash` | `ref` | `bucle` | 🔴 `UB` | ❌ falso negativo | — |
| 608 | [`f_uset_rehash_ref_llamada`](casos/uset/rehash.md#f_uset_rehash_ref_llamada) | `uset` | `rehash` | `ref` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 609 | [`f_uset_rehash_ptr_recto`](casos/uset/rehash.md#f_uset_rehash_ptr_recto) | `uset` | `rehash` | `ptr` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 610 | [`f_uset_rehash_ptr_guarda`](casos/uset/rehash.md#f_uset_rehash_ptr_guarda) | `uset` | `rehash` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 611 | [`f_uset_rehash_ptr_bucle`](casos/uset/rehash.md#f_uset_rehash_ptr_bucle) | `uset` | `rehash` | `ptr` | `bucle` | 🔴 `UB` | ❌ falso negativo | — |
| 612 | [`f_uset_rehash_ptr_llamada`](casos/uset/rehash.md#f_uset_rehash_ptr_llamada) | `uset` | `rehash` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 613 | [`f_uset_reserve_it_recto`](casos/uset/reserve.md#f_uset_reserve_it_recto) | `uset` | `reserve` | `it` | `recto` | 🔴 `UB` | ❌ falso negativo | — |
| 614 | [`f_uset_reserve_it_guarda`](casos/uset/reserve.md#f_uset_reserve_it_guarda) | `uset` | `reserve` | `it` | `guarda` | 🔴 `UB` | ❌ falso negativo | — |
| 615 | [`f_uset_reserve_it_bucle`](casos/uset/reserve.md#f_uset_reserve_it_bucle) | `uset` | `reserve` | `it` | `bucle` | 🔴 `UB` | ❌ falso negativo | — |
| 616 | [`f_uset_reserve_it_llamada`](casos/uset/reserve.md#f_uset_reserve_it_llamada) | `uset` | `reserve` | `it` | `llamada` | 🔴 `UB` | ❌ falso negativo | — |
| 617 | [`f_uset_reserve_ref_recto`](casos/uset/reserve.md#f_uset_reserve_ref_recto) | `uset` | `reserve` | `ref` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 618 | [`f_uset_reserve_ref_guarda`](casos/uset/reserve.md#f_uset_reserve_ref_guarda) | `uset` | `reserve` | `ref` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 619 | [`f_uset_reserve_ref_bucle`](casos/uset/reserve.md#f_uset_reserve_ref_bucle) | `uset` | `reserve` | `ref` | `bucle` | 🔴 `UB` | ❌ falso negativo | — |
| 620 | [`f_uset_reserve_ref_llamada`](casos/uset/reserve.md#f_uset_reserve_ref_llamada) | `uset` | `reserve` | `ref` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 621 | [`f_uset_reserve_ptr_recto`](casos/uset/reserve.md#f_uset_reserve_ptr_recto) | `uset` | `reserve` | `ptr` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 622 | [`f_uset_reserve_ptr_guarda`](casos/uset/reserve.md#f_uset_reserve_ptr_guarda) | `uset` | `reserve` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 623 | [`f_uset_reserve_ptr_bucle`](casos/uset/reserve.md#f_uset_reserve_ptr_bucle) | `uset` | `reserve` | `ptr` | `bucle` | 🔴 `UB` | ❌ falso negativo | — |
| 624 | [`f_uset_reserve_ptr_llamada`](casos/uset/reserve.md#f_uset_reserve_ptr_llamada) | `uset` | `reserve` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 625 | [`f_umap_insert_it_recto`](casos/umap/insert.md#f_umap_insert_it_recto) | `umap` | `insert` | `it` | `recto` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 626 | [`f_umap_insert_it_guarda`](casos/umap/insert.md#f_umap_insert_it_guarda) | `umap` | `insert` | `it` | `guarda` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 627 | [`f_umap_insert_it_bucle`](casos/umap/insert.md#f_umap_insert_it_bucle) | `umap` | `insert` | `it` | `bucle` | 🔴 `UB` | ❌ falso negativo | — |
| 628 | [`f_umap_insert_it_llamada`](casos/umap/insert.md#f_umap_insert_it_llamada) | `umap` | `insert` | `it` | `llamada` | 🟡 `POLICY` | silencio (optimista) | 🛑 |
| 629 | [`f_umap_insert_ref_recto`](casos/umap/insert.md#f_umap_insert_ref_recto) | `umap` | `insert` | `ref` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 630 | [`f_umap_insert_ref_guarda`](casos/umap/insert.md#f_umap_insert_ref_guarda) | `umap` | `insert` | `ref` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 631 | [`f_umap_insert_ref_bucle`](casos/umap/insert.md#f_umap_insert_ref_bucle) | `umap` | `insert` | `ref` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 632 | [`f_umap_insert_ref_llamada`](casos/umap/insert.md#f_umap_insert_ref_llamada) | `umap` | `insert` | `ref` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 633 | [`f_umap_insert_ptr_recto`](casos/umap/insert.md#f_umap_insert_ptr_recto) | `umap` | `insert` | `ptr` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 634 | [`f_umap_insert_ptr_guarda`](casos/umap/insert.md#f_umap_insert_ptr_guarda) | `umap` | `insert` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 635 | [`f_umap_insert_ptr_bucle`](casos/umap/insert.md#f_umap_insert_ptr_bucle) | `umap` | `insert` | `ptr` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 636 | [`f_umap_insert_ptr_llamada`](casos/umap/insert.md#f_umap_insert_ptr_llamada) | `umap` | `insert` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 637 | [`f_umap_subscript_it_recto`](casos/umap/subscript.md#f_umap_subscript_it_recto) | `umap` | `subscript` | `it` | `recto` | 🟡 `POLICY` | silencio (optimista) | — |
| 638 | [`f_umap_subscript_it_guarda`](casos/umap/subscript.md#f_umap_subscript_it_guarda) | `umap` | `subscript` | `it` | `guarda` | 🟡 `POLICY` | silencio (optimista) | — |
| 639 | [`f_umap_subscript_it_bucle`](casos/umap/subscript.md#f_umap_subscript_it_bucle) | `umap` | `subscript` | `it` | `bucle` | 🔴 `UB` | ❌ falso negativo | — |
| 640 | [`f_umap_subscript_it_llamada`](casos/umap/subscript.md#f_umap_subscript_it_llamada) | `umap` | `subscript` | `it` | `llamada` | 🟡 `POLICY` | silencio (optimista) | — |
| 641 | [`f_umap_subscript_ref_recto`](casos/umap/subscript.md#f_umap_subscript_ref_recto) | `umap` | `subscript` | `ref` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 642 | [`f_umap_subscript_ref_guarda`](casos/umap/subscript.md#f_umap_subscript_ref_guarda) | `umap` | `subscript` | `ref` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 643 | [`f_umap_subscript_ref_bucle`](casos/umap/subscript.md#f_umap_subscript_ref_bucle) | `umap` | `subscript` | `ref` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 644 | [`f_umap_subscript_ref_llamada`](casos/umap/subscript.md#f_umap_subscript_ref_llamada) | `umap` | `subscript` | `ref` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 645 | [`f_umap_subscript_ptr_recto`](casos/umap/subscript.md#f_umap_subscript_ptr_recto) | `umap` | `subscript` | `ptr` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 646 | [`f_umap_subscript_ptr_guarda`](casos/umap/subscript.md#f_umap_subscript_ptr_guarda) | `umap` | `subscript` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 647 | [`f_umap_subscript_ptr_bucle`](casos/umap/subscript.md#f_umap_subscript_ptr_bucle) | `umap` | `subscript` | `ptr` | `bucle` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 648 | [`f_umap_subscript_ptr_llamada`](casos/umap/subscript.md#f_umap_subscript_ptr_llamada) | `umap` | `subscript` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 649 | [`f_umap_erase_begin_it_recto`](casos/umap/erase_begin.md#f_umap_erase_begin_it_recto) | `umap` | `erase_begin` | `it` | `recto` | 🔴 `UB` | ✅ detectado | 🛑 |
| 650 | [`f_umap_erase_begin_it_guarda`](casos/umap/erase_begin.md#f_umap_erase_begin_it_guarda) | `umap` | `erase_begin` | `it` | `guarda` | 🔴 `UB` | ✅ detectado | 🛑 |
| 651 | [`f_umap_erase_begin_it_bucle`](casos/umap/erase_begin.md#f_umap_erase_begin_it_bucle) | `umap` | `erase_begin` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 652 | [`f_umap_erase_begin_it_llamada`](casos/umap/erase_begin.md#f_umap_erase_begin_it_llamada) | `umap` | `erase_begin` | `it` | `llamada` | 🔴 `UB` | ✅ detectado | 🛑 |
| 653 | [`f_umap_erase_begin_ref_recto`](casos/umap/erase_begin.md#f_umap_erase_begin_ref_recto) | `umap` | `erase_begin` | `ref` | `recto` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 654 | [`f_umap_erase_begin_ref_guarda`](casos/umap/erase_begin.md#f_umap_erase_begin_ref_guarda) | `umap` | `erase_begin` | `ref` | `guarda` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 655 | [`f_umap_erase_begin_ref_bucle`](casos/umap/erase_begin.md#f_umap_erase_begin_ref_bucle) | `umap` | `erase_begin` | `ref` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 656 | [`f_umap_erase_begin_ref_llamada`](casos/umap/erase_begin.md#f_umap_erase_begin_ref_llamada) | `umap` | `erase_begin` | `ref` | `llamada` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 657 | [`f_umap_erase_begin_ptr_recto`](casos/umap/erase_begin.md#f_umap_erase_begin_ptr_recto) | `umap` | `erase_begin` | `ptr` | `recto` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 658 | [`f_umap_erase_begin_ptr_guarda`](casos/umap/erase_begin.md#f_umap_erase_begin_ptr_guarda) | `umap` | `erase_begin` | `ptr` | `guarda` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 659 | [`f_umap_erase_begin_ptr_bucle`](casos/umap/erase_begin.md#f_umap_erase_begin_ptr_bucle) | `umap` | `erase_begin` | `ptr` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 660 | [`f_umap_erase_begin_ptr_llamada`](casos/umap/erase_begin.md#f_umap_erase_begin_ptr_llamada) | `umap` | `erase_begin` | `ptr` | `llamada` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 661 | [`f_umap_clear_it_recto`](casos/umap/clear.md#f_umap_clear_it_recto) | `umap` | `clear` | `it` | `recto` | 🔴 `UB` | ✅ detectado | 🛑 |
| 662 | [`f_umap_clear_it_guarda`](casos/umap/clear.md#f_umap_clear_it_guarda) | `umap` | `clear` | `it` | `guarda` | 🔴 `UB` | ✅ detectado | 🛑 |
| 663 | [`f_umap_clear_it_bucle`](casos/umap/clear.md#f_umap_clear_it_bucle) | `umap` | `clear` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 664 | [`f_umap_clear_it_llamada`](casos/umap/clear.md#f_umap_clear_it_llamada) | `umap` | `clear` | `it` | `llamada` | 🔴 `UB` | ✅ detectado | 🛑 |
| 665 | [`f_umap_clear_ref_recto`](casos/umap/clear.md#f_umap_clear_ref_recto) | `umap` | `clear` | `ref` | `recto` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 666 | [`f_umap_clear_ref_guarda`](casos/umap/clear.md#f_umap_clear_ref_guarda) | `umap` | `clear` | `ref` | `guarda` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 667 | [`f_umap_clear_ref_bucle`](casos/umap/clear.md#f_umap_clear_ref_bucle) | `umap` | `clear` | `ref` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 668 | [`f_umap_clear_ref_llamada`](casos/umap/clear.md#f_umap_clear_ref_llamada) | `umap` | `clear` | `ref` | `llamada` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 669 | [`f_umap_clear_ptr_recto`](casos/umap/clear.md#f_umap_clear_ptr_recto) | `umap` | `clear` | `ptr` | `recto` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 670 | [`f_umap_clear_ptr_guarda`](casos/umap/clear.md#f_umap_clear_ptr_guarda) | `umap` | `clear` | `ptr` | `guarda` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 671 | [`f_umap_clear_ptr_bucle`](casos/umap/clear.md#f_umap_clear_ptr_bucle) | `umap` | `clear` | `ptr` | `bucle` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 672 | [`f_umap_clear_ptr_llamada`](casos/umap/clear.md#f_umap_clear_ptr_llamada) | `umap` | `clear` | `ptr` | `llamada` | 🔴 `UB` | ❌ falso negativo | 🛑 |
| 673 | [`f_umap_rehash_it_recto`](casos/umap/rehash.md#f_umap_rehash_it_recto) | `umap` | `rehash` | `it` | `recto` | 🔴 `UB` | ❌ falso negativo | — |
| 674 | [`f_umap_rehash_it_guarda`](casos/umap/rehash.md#f_umap_rehash_it_guarda) | `umap` | `rehash` | `it` | `guarda` | 🔴 `UB` | ❌ falso negativo | — |
| 675 | [`f_umap_rehash_it_bucle`](casos/umap/rehash.md#f_umap_rehash_it_bucle) | `umap` | `rehash` | `it` | `bucle` | 🔴 `UB` | ❌ falso negativo | — |
| 676 | [`f_umap_rehash_it_llamada`](casos/umap/rehash.md#f_umap_rehash_it_llamada) | `umap` | `rehash` | `it` | `llamada` | 🔴 `UB` | ❌ falso negativo | — |
| 677 | [`f_umap_rehash_ref_recto`](casos/umap/rehash.md#f_umap_rehash_ref_recto) | `umap` | `rehash` | `ref` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 678 | [`f_umap_rehash_ref_guarda`](casos/umap/rehash.md#f_umap_rehash_ref_guarda) | `umap` | `rehash` | `ref` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 679 | [`f_umap_rehash_ref_bucle`](casos/umap/rehash.md#f_umap_rehash_ref_bucle) | `umap` | `rehash` | `ref` | `bucle` | 🔴 `UB` | ❌ falso negativo | — |
| 680 | [`f_umap_rehash_ref_llamada`](casos/umap/rehash.md#f_umap_rehash_ref_llamada) | `umap` | `rehash` | `ref` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 681 | [`f_umap_rehash_ptr_recto`](casos/umap/rehash.md#f_umap_rehash_ptr_recto) | `umap` | `rehash` | `ptr` | `recto` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 682 | [`f_umap_rehash_ptr_guarda`](casos/umap/rehash.md#f_umap_rehash_ptr_guarda) | `umap` | `rehash` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ silencio correcto | — |
| 683 | [`f_umap_rehash_ptr_bucle`](casos/umap/rehash.md#f_umap_rehash_ptr_bucle) | `umap` | `rehash` | `ptr` | `bucle` | 🔴 `UB` | ❌ falso negativo | — |
| 684 | [`f_umap_rehash_ptr_llamada`](casos/umap/rehash.md#f_umap_rehash_ptr_llamada) | `umap` | `rehash` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ silencio correcto | — |
