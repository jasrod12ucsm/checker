# Índice de casos

Los 750 casos del corpus. *Dinámico* 🛑 = algún instrumento detectó el defecto en alguna ejecución.

| # | Caso | Contenedor | Operación | Sostiene | Forma | Etiqueta | Estático | Dinámico |
|---:|---|---|---|---|---|---|---|---|
| 1 | [`f_vector_push_back_it_recto`](casos/vector/push_back.md#f_vector_push_back_it_recto) | `vector` | `push_back` | `it` | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 2 | [`f_vector_push_back_it_recto_reserva`](casos/garantias.md#f_vector_push_back_it_recto_reserva) | `vector` | `push_back` | `it` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 3 | [`f_vector_push_back_it_guarda`](casos/vector/push_back.md#f_vector_push_back_it_guarda) | `vector` | `push_back` | `it` | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 4 | [`f_vector_push_back_it_guarda_reserva`](casos/garantias.md#f_vector_push_back_it_guarda_reserva) | `vector` | `push_back` | `it` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 5 | [`f_vector_push_back_it_bucle`](casos/vector/push_back.md#f_vector_push_back_it_bucle) | `vector` | `push_back` | `it` | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 6 | [`f_vector_push_back_it_bucle_reserva`](casos/garantias.md#f_vector_push_back_it_bucle_reserva) | `vector` | `push_back` | `it` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 7 | [`f_vector_push_back_it_llamada`](casos/vector/push_back.md#f_vector_push_back_it_llamada) | `vector` | `push_back` | `it` | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 8 | [`f_vector_push_back_it_llamada_reserva`](casos/garantias.md#f_vector_push_back_it_llamada_reserva) | `vector` | `push_back` | `it` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 9 | [`f_vector_push_back_ref_recto`](casos/vector/push_back.md#f_vector_push_back_ref_recto) | `vector` | `push_back` | `ref` | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 10 | [`f_vector_push_back_ref_recto_reserva`](casos/garantias.md#f_vector_push_back_ref_recto_reserva) | `vector` | `push_back` | `ref` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 11 | [`f_vector_push_back_ref_guarda`](casos/vector/push_back.md#f_vector_push_back_ref_guarda) | `vector` | `push_back` | `ref` | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 12 | [`f_vector_push_back_ref_guarda_reserva`](casos/garantias.md#f_vector_push_back_ref_guarda_reserva) | `vector` | `push_back` | `ref` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 13 | [`f_vector_push_back_ref_bucle`](casos/vector/push_back.md#f_vector_push_back_ref_bucle) | `vector` | `push_back` | `ref` | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 14 | [`f_vector_push_back_ref_bucle_reserva`](casos/garantias.md#f_vector_push_back_ref_bucle_reserva) | `vector` | `push_back` | `ref` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 15 | [`f_vector_push_back_ref_llamada`](casos/vector/push_back.md#f_vector_push_back_ref_llamada) | `vector` | `push_back` | `ref` | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 16 | [`f_vector_push_back_ref_llamada_reserva`](casos/garantias.md#f_vector_push_back_ref_llamada_reserva) | `vector` | `push_back` | `ref` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 17 | [`f_vector_push_back_ptr_recto`](casos/vector/push_back.md#f_vector_push_back_ptr_recto) | `vector` | `push_back` | `ptr` | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 18 | [`f_vector_push_back_ptr_recto_reserva`](casos/garantias.md#f_vector_push_back_ptr_recto_reserva) | `vector` | `push_back` | `ptr` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 19 | [`f_vector_push_back_ptr_guarda`](casos/vector/push_back.md#f_vector_push_back_ptr_guarda) | `vector` | `push_back` | `ptr` | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 20 | [`f_vector_push_back_ptr_guarda_reserva`](casos/garantias.md#f_vector_push_back_ptr_guarda_reserva) | `vector` | `push_back` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 21 | [`f_vector_push_back_ptr_bucle`](casos/vector/push_back.md#f_vector_push_back_ptr_bucle) | `vector` | `push_back` | `ptr` | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 22 | [`f_vector_push_back_ptr_bucle_reserva`](casos/garantias.md#f_vector_push_back_ptr_bucle_reserva) | `vector` | `push_back` | `ptr` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 23 | [`f_vector_push_back_ptr_llamada`](casos/vector/push_back.md#f_vector_push_back_ptr_llamada) | `vector` | `push_back` | `ptr` | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 24 | [`f_vector_push_back_ptr_llamada_reserva`](casos/garantias.md#f_vector_push_back_ptr_llamada_reserva) | `vector` | `push_back` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 25 | [`f_vector_emplace_back_it_recto`](casos/vector/emplace_back.md#f_vector_emplace_back_it_recto) | `vector` | `emplace_back` | `it` | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 26 | [`f_vector_emplace_back_it_recto_reserva`](casos/garantias.md#f_vector_emplace_back_it_recto_reserva) | `vector` | `emplace_back` | `it` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 27 | [`f_vector_emplace_back_it_guarda`](casos/vector/emplace_back.md#f_vector_emplace_back_it_guarda) | `vector` | `emplace_back` | `it` | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 28 | [`f_vector_emplace_back_it_guarda_reserva`](casos/garantias.md#f_vector_emplace_back_it_guarda_reserva) | `vector` | `emplace_back` | `it` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 29 | [`f_vector_emplace_back_it_bucle`](casos/vector/emplace_back.md#f_vector_emplace_back_it_bucle) | `vector` | `emplace_back` | `it` | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 30 | [`f_vector_emplace_back_it_bucle_reserva`](casos/garantias.md#f_vector_emplace_back_it_bucle_reserva) | `vector` | `emplace_back` | `it` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 31 | [`f_vector_emplace_back_it_llamada`](casos/vector/emplace_back.md#f_vector_emplace_back_it_llamada) | `vector` | `emplace_back` | `it` | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 32 | [`f_vector_emplace_back_it_llamada_reserva`](casos/garantias.md#f_vector_emplace_back_it_llamada_reserva) | `vector` | `emplace_back` | `it` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 33 | [`f_vector_emplace_back_ref_recto`](casos/vector/emplace_back.md#f_vector_emplace_back_ref_recto) | `vector` | `emplace_back` | `ref` | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 34 | [`f_vector_emplace_back_ref_recto_reserva`](casos/garantias.md#f_vector_emplace_back_ref_recto_reserva) | `vector` | `emplace_back` | `ref` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 35 | [`f_vector_emplace_back_ref_guarda`](casos/vector/emplace_back.md#f_vector_emplace_back_ref_guarda) | `vector` | `emplace_back` | `ref` | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 36 | [`f_vector_emplace_back_ref_guarda_reserva`](casos/garantias.md#f_vector_emplace_back_ref_guarda_reserva) | `vector` | `emplace_back` | `ref` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 37 | [`f_vector_emplace_back_ref_bucle`](casos/vector/emplace_back.md#f_vector_emplace_back_ref_bucle) | `vector` | `emplace_back` | `ref` | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 38 | [`f_vector_emplace_back_ref_bucle_reserva`](casos/garantias.md#f_vector_emplace_back_ref_bucle_reserva) | `vector` | `emplace_back` | `ref` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 39 | [`f_vector_emplace_back_ref_llamada`](casos/vector/emplace_back.md#f_vector_emplace_back_ref_llamada) | `vector` | `emplace_back` | `ref` | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 40 | [`f_vector_emplace_back_ref_llamada_reserva`](casos/garantias.md#f_vector_emplace_back_ref_llamada_reserva) | `vector` | `emplace_back` | `ref` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 41 | [`f_vector_emplace_back_ptr_recto`](casos/vector/emplace_back.md#f_vector_emplace_back_ptr_recto) | `vector` | `emplace_back` | `ptr` | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 42 | [`f_vector_emplace_back_ptr_recto_reserva`](casos/garantias.md#f_vector_emplace_back_ptr_recto_reserva) | `vector` | `emplace_back` | `ptr` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 43 | [`f_vector_emplace_back_ptr_guarda`](casos/vector/emplace_back.md#f_vector_emplace_back_ptr_guarda) | `vector` | `emplace_back` | `ptr` | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 44 | [`f_vector_emplace_back_ptr_guarda_reserva`](casos/garantias.md#f_vector_emplace_back_ptr_guarda_reserva) | `vector` | `emplace_back` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 45 | [`f_vector_emplace_back_ptr_bucle`](casos/vector/emplace_back.md#f_vector_emplace_back_ptr_bucle) | `vector` | `emplace_back` | `ptr` | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 46 | [`f_vector_emplace_back_ptr_bucle_reserva`](casos/garantias.md#f_vector_emplace_back_ptr_bucle_reserva) | `vector` | `emplace_back` | `ptr` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 47 | [`f_vector_emplace_back_ptr_llamada`](casos/vector/emplace_back.md#f_vector_emplace_back_ptr_llamada) | `vector` | `emplace_back` | `ptr` | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 48 | [`f_vector_emplace_back_ptr_llamada_reserva`](casos/garantias.md#f_vector_emplace_back_ptr_llamada_reserva) | `vector` | `emplace_back` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 49 | [`f_vector_insert_begin_it_recto`](casos/vector/insert_begin.md#f_vector_insert_begin_it_recto) | `vector` | `insert_begin` | `it` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 50 | [`f_vector_insert_begin_it_guarda`](casos/vector/insert_begin.md#f_vector_insert_begin_it_guarda) | `vector` | `insert_begin` | `it` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 51 | [`f_vector_insert_begin_it_bucle`](casos/vector/insert_begin.md#f_vector_insert_begin_it_bucle) | `vector` | `insert_begin` | `it` | `bucle` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 52 | [`f_vector_insert_begin_it_llamada`](casos/vector/insert_begin.md#f_vector_insert_begin_it_llamada) | `vector` | `insert_begin` | `it` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 53 | [`f_vector_insert_begin_ref_recto`](casos/vector/insert_begin.md#f_vector_insert_begin_ref_recto) | `vector` | `insert_begin` | `ref` | `recto` | 🔴 `UB` | ❌ no detectado | — |
| 54 | [`f_vector_insert_begin_ref_guarda`](casos/vector/insert_begin.md#f_vector_insert_begin_ref_guarda) | `vector` | `insert_begin` | `ref` | `guarda` | 🔴 `UB` | ❌ no detectado | — |
| 55 | [`f_vector_insert_begin_ref_bucle`](casos/vector/insert_begin.md#f_vector_insert_begin_ref_bucle) | `vector` | `insert_begin` | `ref` | `bucle` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 56 | [`f_vector_insert_begin_ref_llamada`](casos/vector/insert_begin.md#f_vector_insert_begin_ref_llamada) | `vector` | `insert_begin` | `ref` | `llamada` | 🔴 `UB` | ❌ no detectado | — |
| 57 | [`f_vector_insert_begin_ptr_recto`](casos/vector/insert_begin.md#f_vector_insert_begin_ptr_recto) | `vector` | `insert_begin` | `ptr` | `recto` | 🔴 `UB` | ❌ no detectado | — |
| 58 | [`f_vector_insert_begin_ptr_guarda`](casos/vector/insert_begin.md#f_vector_insert_begin_ptr_guarda) | `vector` | `insert_begin` | `ptr` | `guarda` | 🔴 `UB` | ❌ no detectado | — |
| 59 | [`f_vector_insert_begin_ptr_bucle`](casos/vector/insert_begin.md#f_vector_insert_begin_ptr_bucle) | `vector` | `insert_begin` | `ptr` | `bucle` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 60 | [`f_vector_insert_begin_ptr_llamada`](casos/vector/insert_begin.md#f_vector_insert_begin_ptr_llamada) | `vector` | `insert_begin` | `ptr` | `llamada` | 🔴 `UB` | ❌ no detectado | — |
| 61 | [`f_vector_insert_end_it_recto`](casos/vector/insert_end.md#f_vector_insert_end_it_recto) | `vector` | `insert_end` | `it` | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 62 | [`f_vector_insert_end_it_recto_reserva`](casos/garantias.md#f_vector_insert_end_it_recto_reserva) | `vector` | `insert_end` | `it` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 63 | [`f_vector_insert_end_it_guarda`](casos/vector/insert_end.md#f_vector_insert_end_it_guarda) | `vector` | `insert_end` | `it` | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 64 | [`f_vector_insert_end_it_guarda_reserva`](casos/garantias.md#f_vector_insert_end_it_guarda_reserva) | `vector` | `insert_end` | `it` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 65 | [`f_vector_insert_end_it_bucle`](casos/vector/insert_end.md#f_vector_insert_end_it_bucle) | `vector` | `insert_end` | `it` | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 66 | [`f_vector_insert_end_it_bucle_reserva`](casos/garantias.md#f_vector_insert_end_it_bucle_reserva) | `vector` | `insert_end` | `it` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 67 | [`f_vector_insert_end_it_llamada`](casos/vector/insert_end.md#f_vector_insert_end_it_llamada) | `vector` | `insert_end` | `it` | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 68 | [`f_vector_insert_end_it_llamada_reserva`](casos/garantias.md#f_vector_insert_end_it_llamada_reserva) | `vector` | `insert_end` | `it` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 69 | [`f_vector_insert_end_ref_recto`](casos/vector/insert_end.md#f_vector_insert_end_ref_recto) | `vector` | `insert_end` | `ref` | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 70 | [`f_vector_insert_end_ref_recto_reserva`](casos/garantias.md#f_vector_insert_end_ref_recto_reserva) | `vector` | `insert_end` | `ref` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 71 | [`f_vector_insert_end_ref_guarda`](casos/vector/insert_end.md#f_vector_insert_end_ref_guarda) | `vector` | `insert_end` | `ref` | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 72 | [`f_vector_insert_end_ref_guarda_reserva`](casos/garantias.md#f_vector_insert_end_ref_guarda_reserva) | `vector` | `insert_end` | `ref` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 73 | [`f_vector_insert_end_ref_bucle`](casos/vector/insert_end.md#f_vector_insert_end_ref_bucle) | `vector` | `insert_end` | `ref` | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 74 | [`f_vector_insert_end_ref_bucle_reserva`](casos/garantias.md#f_vector_insert_end_ref_bucle_reserva) | `vector` | `insert_end` | `ref` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 75 | [`f_vector_insert_end_ref_llamada`](casos/vector/insert_end.md#f_vector_insert_end_ref_llamada) | `vector` | `insert_end` | `ref` | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 76 | [`f_vector_insert_end_ref_llamada_reserva`](casos/garantias.md#f_vector_insert_end_ref_llamada_reserva) | `vector` | `insert_end` | `ref` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 77 | [`f_vector_insert_end_ptr_recto`](casos/vector/insert_end.md#f_vector_insert_end_ptr_recto) | `vector` | `insert_end` | `ptr` | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 78 | [`f_vector_insert_end_ptr_recto_reserva`](casos/garantias.md#f_vector_insert_end_ptr_recto_reserva) | `vector` | `insert_end` | `ptr` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 79 | [`f_vector_insert_end_ptr_guarda`](casos/vector/insert_end.md#f_vector_insert_end_ptr_guarda) | `vector` | `insert_end` | `ptr` | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 80 | [`f_vector_insert_end_ptr_guarda_reserva`](casos/garantias.md#f_vector_insert_end_ptr_guarda_reserva) | `vector` | `insert_end` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 81 | [`f_vector_insert_end_ptr_bucle`](casos/vector/insert_end.md#f_vector_insert_end_ptr_bucle) | `vector` | `insert_end` | `ptr` | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 82 | [`f_vector_insert_end_ptr_bucle_reserva`](casos/garantias.md#f_vector_insert_end_ptr_bucle_reserva) | `vector` | `insert_end` | `ptr` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 83 | [`f_vector_insert_end_ptr_llamada`](casos/vector/insert_end.md#f_vector_insert_end_ptr_llamada) | `vector` | `insert_end` | `ptr` | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 84 | [`f_vector_insert_end_ptr_llamada_reserva`](casos/garantias.md#f_vector_insert_end_ptr_llamada_reserva) | `vector` | `insert_end` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 85 | [`f_vector_erase_begin_it_recto`](casos/vector/erase_begin.md#f_vector_erase_begin_it_recto) | `vector` | `erase_begin` | `it` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 86 | [`f_vector_erase_begin_it_guarda`](casos/vector/erase_begin.md#f_vector_erase_begin_it_guarda) | `vector` | `erase_begin` | `it` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 87 | [`f_vector_erase_begin_it_bucle`](casos/vector/erase_begin.md#f_vector_erase_begin_it_bucle) | `vector` | `erase_begin` | `it` | `bucle` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 88 | [`f_vector_erase_begin_it_llamada`](casos/vector/erase_begin.md#f_vector_erase_begin_it_llamada) | `vector` | `erase_begin` | `it` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 89 | [`f_vector_erase_begin_ref_recto`](casos/vector/erase_begin.md#f_vector_erase_begin_ref_recto) | `vector` | `erase_begin` | `ref` | `recto` | 🔴 `UB` | ❌ no detectado | — |
| 90 | [`f_vector_erase_begin_ref_guarda`](casos/vector/erase_begin.md#f_vector_erase_begin_ref_guarda) | `vector` | `erase_begin` | `ref` | `guarda` | 🔴 `UB` | ❌ no detectado | — |
| 91 | [`f_vector_erase_begin_ref_bucle`](casos/vector/erase_begin.md#f_vector_erase_begin_ref_bucle) | `vector` | `erase_begin` | `ref` | `bucle` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 92 | [`f_vector_erase_begin_ref_llamada`](casos/vector/erase_begin.md#f_vector_erase_begin_ref_llamada) | `vector` | `erase_begin` | `ref` | `llamada` | 🔴 `UB` | ❌ no detectado | — |
| 93 | [`f_vector_erase_begin_ptr_recto`](casos/vector/erase_begin.md#f_vector_erase_begin_ptr_recto) | `vector` | `erase_begin` | `ptr` | `recto` | 🔴 `UB` | ❌ no detectado | — |
| 94 | [`f_vector_erase_begin_ptr_guarda`](casos/vector/erase_begin.md#f_vector_erase_begin_ptr_guarda) | `vector` | `erase_begin` | `ptr` | `guarda` | 🔴 `UB` | ❌ no detectado | — |
| 95 | [`f_vector_erase_begin_ptr_bucle`](casos/vector/erase_begin.md#f_vector_erase_begin_ptr_bucle) | `vector` | `erase_begin` | `ptr` | `bucle` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 96 | [`f_vector_erase_begin_ptr_llamada`](casos/vector/erase_begin.md#f_vector_erase_begin_ptr_llamada) | `vector` | `erase_begin` | `ptr` | `llamada` | 🔴 `UB` | ❌ no detectado | — |
| 97 | [`f_vector_clear_it_recto`](casos/vector/clear.md#f_vector_clear_it_recto) | `vector` | `clear` | `it` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 98 | [`f_vector_clear_it_guarda`](casos/vector/clear.md#f_vector_clear_it_guarda) | `vector` | `clear` | `it` | `guarda` | 🔴 `UB` | ✅ detectado | 🛑 |
| 99 | [`f_vector_clear_it_bucle`](casos/vector/clear.md#f_vector_clear_it_bucle) | `vector` | `clear` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 100 | [`f_vector_clear_it_llamada`](casos/vector/clear.md#f_vector_clear_it_llamada) | `vector` | `clear` | `it` | `llamada` | 🔴 `UB` | ✅ detectado | 🛑 |
| 101 | [`f_vector_clear_ref_recto`](casos/vector/clear.md#f_vector_clear_ref_recto) | `vector` | `clear` | `ref` | `recto` | 🔴 `UB` | ❌ no detectado | — |
| 102 | [`f_vector_clear_ref_guarda`](casos/vector/clear.md#f_vector_clear_ref_guarda) | `vector` | `clear` | `ref` | `guarda` | 🔴 `UB` | ❌ no detectado | — |
| 103 | [`f_vector_clear_ref_bucle`](casos/vector/clear.md#f_vector_clear_ref_bucle) | `vector` | `clear` | `ref` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 104 | [`f_vector_clear_ref_llamada`](casos/vector/clear.md#f_vector_clear_ref_llamada) | `vector` | `clear` | `ref` | `llamada` | 🔴 `UB` | ❌ no detectado | — |
| 105 | [`f_vector_clear_ptr_recto`](casos/vector/clear.md#f_vector_clear_ptr_recto) | `vector` | `clear` | `ptr` | `recto` | 🔴 `UB` | ❌ no detectado | — |
| 106 | [`f_vector_clear_ptr_guarda`](casos/vector/clear.md#f_vector_clear_ptr_guarda) | `vector` | `clear` | `ptr` | `guarda` | 🔴 `UB` | ❌ no detectado | — |
| 107 | [`f_vector_clear_ptr_bucle`](casos/vector/clear.md#f_vector_clear_ptr_bucle) | `vector` | `clear` | `ptr` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 108 | [`f_vector_clear_ptr_llamada`](casos/vector/clear.md#f_vector_clear_ptr_llamada) | `vector` | `clear` | `ptr` | `llamada` | 🔴 `UB` | ❌ no detectado | — |
| 109 | [`f_vector_resize_grow_it_recto`](casos/vector/resize_grow.md#f_vector_resize_grow_it_recto) | `vector` | `resize_grow` | `it` | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 110 | [`f_vector_resize_grow_it_guarda`](casos/vector/resize_grow.md#f_vector_resize_grow_it_guarda) | `vector` | `resize_grow` | `it` | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 111 | [`f_vector_resize_grow_it_bucle`](casos/vector/resize_grow.md#f_vector_resize_grow_it_bucle) | `vector` | `resize_grow` | `it` | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 112 | [`f_vector_resize_grow_it_llamada`](casos/vector/resize_grow.md#f_vector_resize_grow_it_llamada) | `vector` | `resize_grow` | `it` | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 113 | [`f_vector_resize_grow_ref_recto`](casos/vector/resize_grow.md#f_vector_resize_grow_ref_recto) | `vector` | `resize_grow` | `ref` | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 114 | [`f_vector_resize_grow_ref_guarda`](casos/vector/resize_grow.md#f_vector_resize_grow_ref_guarda) | `vector` | `resize_grow` | `ref` | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 115 | [`f_vector_resize_grow_ref_bucle`](casos/vector/resize_grow.md#f_vector_resize_grow_ref_bucle) | `vector` | `resize_grow` | `ref` | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 116 | [`f_vector_resize_grow_ref_llamada`](casos/vector/resize_grow.md#f_vector_resize_grow_ref_llamada) | `vector` | `resize_grow` | `ref` | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 117 | [`f_vector_resize_grow_ptr_recto`](casos/vector/resize_grow.md#f_vector_resize_grow_ptr_recto) | `vector` | `resize_grow` | `ptr` | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 118 | [`f_vector_resize_grow_ptr_guarda`](casos/vector/resize_grow.md#f_vector_resize_grow_ptr_guarda) | `vector` | `resize_grow` | `ptr` | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 119 | [`f_vector_resize_grow_ptr_bucle`](casos/vector/resize_grow.md#f_vector_resize_grow_ptr_bucle) | `vector` | `resize_grow` | `ptr` | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 120 | [`f_vector_resize_grow_ptr_llamada`](casos/vector/resize_grow.md#f_vector_resize_grow_ptr_llamada) | `vector` | `resize_grow` | `ptr` | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 121 | [`f_vector_reserve_it_recto`](casos/vector/reserve.md#f_vector_reserve_it_recto) | `vector` | `reserve` | `it` | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 122 | [`f_vector_reserve_it_guarda`](casos/vector/reserve.md#f_vector_reserve_it_guarda) | `vector` | `reserve` | `it` | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 123 | [`f_vector_reserve_it_bucle`](casos/vector/reserve.md#f_vector_reserve_it_bucle) | `vector` | `reserve` | `it` | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 124 | [`f_vector_reserve_it_llamada`](casos/vector/reserve.md#f_vector_reserve_it_llamada) | `vector` | `reserve` | `it` | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 125 | [`f_vector_reserve_ref_recto`](casos/vector/reserve.md#f_vector_reserve_ref_recto) | `vector` | `reserve` | `ref` | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 126 | [`f_vector_reserve_ref_guarda`](casos/vector/reserve.md#f_vector_reserve_ref_guarda) | `vector` | `reserve` | `ref` | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 127 | [`f_vector_reserve_ref_bucle`](casos/vector/reserve.md#f_vector_reserve_ref_bucle) | `vector` | `reserve` | `ref` | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 128 | [`f_vector_reserve_ref_llamada`](casos/vector/reserve.md#f_vector_reserve_ref_llamada) | `vector` | `reserve` | `ref` | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 129 | [`f_vector_reserve_ptr_recto`](casos/vector/reserve.md#f_vector_reserve_ptr_recto) | `vector` | `reserve` | `ptr` | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 130 | [`f_vector_reserve_ptr_guarda`](casos/vector/reserve.md#f_vector_reserve_ptr_guarda) | `vector` | `reserve` | `ptr` | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 131 | [`f_vector_reserve_ptr_bucle`](casos/vector/reserve.md#f_vector_reserve_ptr_bucle) | `vector` | `reserve` | `ptr` | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 132 | [`f_vector_reserve_ptr_llamada`](casos/vector/reserve.md#f_vector_reserve_ptr_llamada) | `vector` | `reserve` | `ptr` | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 133 | [`f_vector_shrink_to_fit_it_recto`](casos/vector/shrink_to_fit.md#f_vector_shrink_to_fit_it_recto) | `vector` | `shrink_to_fit` | `it` | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 134 | [`f_vector_shrink_to_fit_it_guarda`](casos/vector/shrink_to_fit.md#f_vector_shrink_to_fit_it_guarda) | `vector` | `shrink_to_fit` | `it` | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 135 | [`f_vector_shrink_to_fit_it_bucle`](casos/vector/shrink_to_fit.md#f_vector_shrink_to_fit_it_bucle) | `vector` | `shrink_to_fit` | `it` | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 136 | [`f_vector_shrink_to_fit_it_llamada`](casos/vector/shrink_to_fit.md#f_vector_shrink_to_fit_it_llamada) | `vector` | `shrink_to_fit` | `it` | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 137 | [`f_vector_shrink_to_fit_ref_recto`](casos/vector/shrink_to_fit.md#f_vector_shrink_to_fit_ref_recto) | `vector` | `shrink_to_fit` | `ref` | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 138 | [`f_vector_shrink_to_fit_ref_guarda`](casos/vector/shrink_to_fit.md#f_vector_shrink_to_fit_ref_guarda) | `vector` | `shrink_to_fit` | `ref` | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 139 | [`f_vector_shrink_to_fit_ref_bucle`](casos/vector/shrink_to_fit.md#f_vector_shrink_to_fit_ref_bucle) | `vector` | `shrink_to_fit` | `ref` | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 140 | [`f_vector_shrink_to_fit_ref_llamada`](casos/vector/shrink_to_fit.md#f_vector_shrink_to_fit_ref_llamada) | `vector` | `shrink_to_fit` | `ref` | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 141 | [`f_vector_shrink_to_fit_ptr_recto`](casos/vector/shrink_to_fit.md#f_vector_shrink_to_fit_ptr_recto) | `vector` | `shrink_to_fit` | `ptr` | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 142 | [`f_vector_shrink_to_fit_ptr_guarda`](casos/vector/shrink_to_fit.md#f_vector_shrink_to_fit_ptr_guarda) | `vector` | `shrink_to_fit` | `ptr` | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 143 | [`f_vector_shrink_to_fit_ptr_bucle`](casos/vector/shrink_to_fit.md#f_vector_shrink_to_fit_ptr_bucle) | `vector` | `shrink_to_fit` | `ptr` | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 144 | [`f_vector_shrink_to_fit_ptr_llamada`](casos/vector/shrink_to_fit.md#f_vector_shrink_to_fit_ptr_llamada) | `vector` | `shrink_to_fit` | `ptr` | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 145 | [`f_vector_assign_it_recto`](casos/vector/assign.md#f_vector_assign_it_recto) | `vector` | `assign` | `it` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 146 | [`f_vector_assign_it_guarda`](casos/vector/assign.md#f_vector_assign_it_guarda) | `vector` | `assign` | `it` | `guarda` | 🔴 `UB` | ✅ detectado | 🛑 |
| 147 | [`f_vector_assign_it_bucle`](casos/vector/assign.md#f_vector_assign_it_bucle) | `vector` | `assign` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 148 | [`f_vector_assign_it_llamada`](casos/vector/assign.md#f_vector_assign_it_llamada) | `vector` | `assign` | `it` | `llamada` | 🔴 `UB` | ✅ detectado | 🛑 |
| 149 | [`f_vector_assign_ref_recto`](casos/vector/assign.md#f_vector_assign_ref_recto) | `vector` | `assign` | `ref` | `recto` | 🔴 `UB` | ❌ no detectado | — |
| 150 | [`f_vector_assign_ref_guarda`](casos/vector/assign.md#f_vector_assign_ref_guarda) | `vector` | `assign` | `ref` | `guarda` | 🔴 `UB` | ❌ no detectado | — |
| 151 | [`f_vector_assign_ref_bucle`](casos/vector/assign.md#f_vector_assign_ref_bucle) | `vector` | `assign` | `ref` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 152 | [`f_vector_assign_ref_llamada`](casos/vector/assign.md#f_vector_assign_ref_llamada) | `vector` | `assign` | `ref` | `llamada` | 🔴 `UB` | ❌ no detectado | — |
| 153 | [`f_vector_assign_ptr_recto`](casos/vector/assign.md#f_vector_assign_ptr_recto) | `vector` | `assign` | `ptr` | `recto` | 🔴 `UB` | ❌ no detectado | — |
| 154 | [`f_vector_assign_ptr_guarda`](casos/vector/assign.md#f_vector_assign_ptr_guarda) | `vector` | `assign` | `ptr` | `guarda` | 🔴 `UB` | ❌ no detectado | — |
| 155 | [`f_vector_assign_ptr_bucle`](casos/vector/assign.md#f_vector_assign_ptr_bucle) | `vector` | `assign` | `ptr` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 156 | [`f_vector_assign_ptr_llamada`](casos/vector/assign.md#f_vector_assign_ptr_llamada) | `vector` | `assign` | `ptr` | `llamada` | 🔴 `UB` | ❌ no detectado | — |
| 157 | [`f_vector_pop_back_it_recto`](casos/vector/pop_back.md#f_vector_pop_back_it_recto) | `vector` | `pop_back` | `it` | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 158 | [`f_vector_pop_back_it_guarda`](casos/vector/pop_back.md#f_vector_pop_back_it_guarda) | `vector` | `pop_back` | `it` | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 159 | [`f_vector_pop_back_it_bucle`](casos/vector/pop_back.md#f_vector_pop_back_it_bucle) | `vector` | `pop_back` | `it` | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 160 | [`f_vector_pop_back_it_llamada`](casos/vector/pop_back.md#f_vector_pop_back_it_llamada) | `vector` | `pop_back` | `it` | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 161 | [`f_vector_pop_back_ref_recto`](casos/vector/pop_back.md#f_vector_pop_back_ref_recto) | `vector` | `pop_back` | `ref` | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | — |
| 162 | [`f_vector_pop_back_ref_guarda`](casos/vector/pop_back.md#f_vector_pop_back_ref_guarda) | `vector` | `pop_back` | `ref` | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | — |
| 163 | [`f_vector_pop_back_ref_bucle`](casos/vector/pop_back.md#f_vector_pop_back_ref_bucle) | `vector` | `pop_back` | `ref` | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 164 | [`f_vector_pop_back_ref_llamada`](casos/vector/pop_back.md#f_vector_pop_back_ref_llamada) | `vector` | `pop_back` | `ref` | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | — |
| 165 | [`f_vector_pop_back_ptr_recto`](casos/vector/pop_back.md#f_vector_pop_back_ptr_recto) | `vector` | `pop_back` | `ptr` | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | — |
| 166 | [`f_vector_pop_back_ptr_guarda`](casos/vector/pop_back.md#f_vector_pop_back_ptr_guarda) | `vector` | `pop_back` | `ptr` | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | — |
| 167 | [`f_vector_pop_back_ptr_bucle`](casos/vector/pop_back.md#f_vector_pop_back_ptr_bucle) | `vector` | `pop_back` | `ptr` | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 168 | [`f_vector_pop_back_ptr_llamada`](casos/vector/pop_back.md#f_vector_pop_back_ptr_llamada) | `vector` | `pop_back` | `ptr` | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | — |
| 169 | [`f_deque_push_back_it_recto`](casos/deque/push_back.md#f_deque_push_back_it_recto) | `deque` | `push_back` | `it` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 170 | [`f_deque_push_back_it_guarda`](casos/deque/push_back.md#f_deque_push_back_it_guarda) | `deque` | `push_back` | `it` | `guarda` | 🔴 `UB` | ✅ detectado | 🛑 |
| 171 | [`f_deque_push_back_it_bucle`](casos/deque/push_back.md#f_deque_push_back_it_bucle) | `deque` | `push_back` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 172 | [`f_deque_push_back_it_llamada`](casos/deque/push_back.md#f_deque_push_back_it_llamada) | `deque` | `push_back` | `it` | `llamada` | 🔴 `UB` | ✅ detectado | 🛑 |
| 173 | [`f_deque_push_back_ref_recto`](casos/deque/push_back.md#f_deque_push_back_ref_recto) | `deque` | `push_back` | `ref` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 174 | [`f_deque_push_back_ref_guarda`](casos/deque/push_back.md#f_deque_push_back_ref_guarda) | `deque` | `push_back` | `ref` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 175 | [`f_deque_push_back_ref_bucle`](casos/deque/push_back.md#f_deque_push_back_ref_bucle) | `deque` | `push_back` | `ref` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 176 | [`f_deque_push_back_ref_llamada`](casos/deque/push_back.md#f_deque_push_back_ref_llamada) | `deque` | `push_back` | `ref` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 177 | [`f_deque_push_back_ptr_recto`](casos/deque/push_back.md#f_deque_push_back_ptr_recto) | `deque` | `push_back` | `ptr` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 178 | [`f_deque_push_back_ptr_guarda`](casos/deque/push_back.md#f_deque_push_back_ptr_guarda) | `deque` | `push_back` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 179 | [`f_deque_push_back_ptr_bucle`](casos/deque/push_back.md#f_deque_push_back_ptr_bucle) | `deque` | `push_back` | `ptr` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 180 | [`f_deque_push_back_ptr_llamada`](casos/deque/push_back.md#f_deque_push_back_ptr_llamada) | `deque` | `push_back` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 181 | [`f_deque_push_front_it_recto`](casos/deque/push_front.md#f_deque_push_front_it_recto) | `deque` | `push_front` | `it` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 182 | [`f_deque_push_front_it_guarda`](casos/deque/push_front.md#f_deque_push_front_it_guarda) | `deque` | `push_front` | `it` | `guarda` | 🔴 `UB` | ✅ detectado | 🛑 |
| 183 | [`f_deque_push_front_it_bucle`](casos/deque/push_front.md#f_deque_push_front_it_bucle) | `deque` | `push_front` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 184 | [`f_deque_push_front_it_llamada`](casos/deque/push_front.md#f_deque_push_front_it_llamada) | `deque` | `push_front` | `it` | `llamada` | 🔴 `UB` | ✅ detectado | 🛑 |
| 185 | [`f_deque_push_front_ref_recto`](casos/deque/push_front.md#f_deque_push_front_ref_recto) | `deque` | `push_front` | `ref` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 186 | [`f_deque_push_front_ref_guarda`](casos/deque/push_front.md#f_deque_push_front_ref_guarda) | `deque` | `push_front` | `ref` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 187 | [`f_deque_push_front_ref_bucle`](casos/deque/push_front.md#f_deque_push_front_ref_bucle) | `deque` | `push_front` | `ref` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 188 | [`f_deque_push_front_ref_llamada`](casos/deque/push_front.md#f_deque_push_front_ref_llamada) | `deque` | `push_front` | `ref` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 189 | [`f_deque_push_front_ptr_recto`](casos/deque/push_front.md#f_deque_push_front_ptr_recto) | `deque` | `push_front` | `ptr` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 190 | [`f_deque_push_front_ptr_guarda`](casos/deque/push_front.md#f_deque_push_front_ptr_guarda) | `deque` | `push_front` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 191 | [`f_deque_push_front_ptr_bucle`](casos/deque/push_front.md#f_deque_push_front_ptr_bucle) | `deque` | `push_front` | `ptr` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 192 | [`f_deque_push_front_ptr_llamada`](casos/deque/push_front.md#f_deque_push_front_ptr_llamada) | `deque` | `push_front` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 193 | [`f_deque_emplace_back_it_recto`](casos/deque/emplace_back.md#f_deque_emplace_back_it_recto) | `deque` | `emplace_back` | `it` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 194 | [`f_deque_emplace_back_it_guarda`](casos/deque/emplace_back.md#f_deque_emplace_back_it_guarda) | `deque` | `emplace_back` | `it` | `guarda` | 🔴 `UB` | ✅ detectado | 🛑 |
| 195 | [`f_deque_emplace_back_it_bucle`](casos/deque/emplace_back.md#f_deque_emplace_back_it_bucle) | `deque` | `emplace_back` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 196 | [`f_deque_emplace_back_it_llamada`](casos/deque/emplace_back.md#f_deque_emplace_back_it_llamada) | `deque` | `emplace_back` | `it` | `llamada` | 🔴 `UB` | ✅ detectado | 🛑 |
| 197 | [`f_deque_emplace_back_ref_recto`](casos/deque/emplace_back.md#f_deque_emplace_back_ref_recto) | `deque` | `emplace_back` | `ref` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 198 | [`f_deque_emplace_back_ref_guarda`](casos/deque/emplace_back.md#f_deque_emplace_back_ref_guarda) | `deque` | `emplace_back` | `ref` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 199 | [`f_deque_emplace_back_ref_bucle`](casos/deque/emplace_back.md#f_deque_emplace_back_ref_bucle) | `deque` | `emplace_back` | `ref` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 200 | [`f_deque_emplace_back_ref_llamada`](casos/deque/emplace_back.md#f_deque_emplace_back_ref_llamada) | `deque` | `emplace_back` | `ref` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 201 | [`f_deque_emplace_back_ptr_recto`](casos/deque/emplace_back.md#f_deque_emplace_back_ptr_recto) | `deque` | `emplace_back` | `ptr` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 202 | [`f_deque_emplace_back_ptr_guarda`](casos/deque/emplace_back.md#f_deque_emplace_back_ptr_guarda) | `deque` | `emplace_back` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 203 | [`f_deque_emplace_back_ptr_bucle`](casos/deque/emplace_back.md#f_deque_emplace_back_ptr_bucle) | `deque` | `emplace_back` | `ptr` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 204 | [`f_deque_emplace_back_ptr_llamada`](casos/deque/emplace_back.md#f_deque_emplace_back_ptr_llamada) | `deque` | `emplace_back` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 205 | [`f_deque_insert_middle_it_recto`](casos/deque/insert_middle.md#f_deque_insert_middle_it_recto) | `deque` | `insert_middle` | `it` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 206 | [`f_deque_insert_middle_it_guarda`](casos/deque/insert_middle.md#f_deque_insert_middle_it_guarda) | `deque` | `insert_middle` | `it` | `guarda` | 🔴 `UB` | ✅ detectado | 🛑 |
| 207 | [`f_deque_insert_middle_it_bucle`](casos/deque/insert_middle.md#f_deque_insert_middle_it_bucle) | `deque` | `insert_middle` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 208 | [`f_deque_insert_middle_it_llamada`](casos/deque/insert_middle.md#f_deque_insert_middle_it_llamada) | `deque` | `insert_middle` | `it` | `llamada` | 🔴 `UB` | ✅ detectado | 🛑 |
| 209 | [`f_deque_insert_middle_ref_recto`](casos/deque/insert_middle.md#f_deque_insert_middle_ref_recto) | `deque` | `insert_middle` | `ref` | `recto` | 🔴 `UB` | ❌ no detectado | — |
| 210 | [`f_deque_insert_middle_ref_guarda`](casos/deque/insert_middle.md#f_deque_insert_middle_ref_guarda) | `deque` | `insert_middle` | `ref` | `guarda` | 🔴 `UB` | ❌ no detectado | — |
| 211 | [`f_deque_insert_middle_ref_bucle`](casos/deque/insert_middle.md#f_deque_insert_middle_ref_bucle) | `deque` | `insert_middle` | `ref` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 212 | [`f_deque_insert_middle_ref_llamada`](casos/deque/insert_middle.md#f_deque_insert_middle_ref_llamada) | `deque` | `insert_middle` | `ref` | `llamada` | 🔴 `UB` | ❌ no detectado | — |
| 213 | [`f_deque_insert_middle_ptr_recto`](casos/deque/insert_middle.md#f_deque_insert_middle_ptr_recto) | `deque` | `insert_middle` | `ptr` | `recto` | 🔴 `UB` | ❌ no detectado | — |
| 214 | [`f_deque_insert_middle_ptr_guarda`](casos/deque/insert_middle.md#f_deque_insert_middle_ptr_guarda) | `deque` | `insert_middle` | `ptr` | `guarda` | 🔴 `UB` | ❌ no detectado | — |
| 215 | [`f_deque_insert_middle_ptr_bucle`](casos/deque/insert_middle.md#f_deque_insert_middle_ptr_bucle) | `deque` | `insert_middle` | `ptr` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 216 | [`f_deque_insert_middle_ptr_llamada`](casos/deque/insert_middle.md#f_deque_insert_middle_ptr_llamada) | `deque` | `insert_middle` | `ptr` | `llamada` | 🔴 `UB` | ❌ no detectado | — |
| 217 | [`f_deque_erase_begin_it_recto`](casos/deque/erase_begin.md#f_deque_erase_begin_it_recto) | `deque` | `erase_begin` | `it` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 218 | [`f_deque_erase_begin_it_guarda`](casos/deque/erase_begin.md#f_deque_erase_begin_it_guarda) | `deque` | `erase_begin` | `it` | `guarda` | 🔴 `UB` | ✅ detectado | 🛑 |
| 219 | [`f_deque_erase_begin_it_bucle`](casos/deque/erase_begin.md#f_deque_erase_begin_it_bucle) | `deque` | `erase_begin` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 220 | [`f_deque_erase_begin_it_llamada`](casos/deque/erase_begin.md#f_deque_erase_begin_it_llamada) | `deque` | `erase_begin` | `it` | `llamada` | 🔴 `UB` | ✅ detectado | 🛑 |
| 221 | [`f_deque_erase_begin_ref_recto`](casos/deque/erase_begin.md#f_deque_erase_begin_ref_recto) | `deque` | `erase_begin` | `ref` | `recto` | 🔴 `UB` | ❌ no detectado | — |
| 222 | [`f_deque_erase_begin_ref_guarda`](casos/deque/erase_begin.md#f_deque_erase_begin_ref_guarda) | `deque` | `erase_begin` | `ref` | `guarda` | 🔴 `UB` | ❌ no detectado | — |
| 223 | [`f_deque_erase_begin_ref_bucle`](casos/deque/erase_begin.md#f_deque_erase_begin_ref_bucle) | `deque` | `erase_begin` | `ref` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 224 | [`f_deque_erase_begin_ref_llamada`](casos/deque/erase_begin.md#f_deque_erase_begin_ref_llamada) | `deque` | `erase_begin` | `ref` | `llamada` | 🔴 `UB` | ❌ no detectado | — |
| 225 | [`f_deque_erase_begin_ptr_recto`](casos/deque/erase_begin.md#f_deque_erase_begin_ptr_recto) | `deque` | `erase_begin` | `ptr` | `recto` | 🔴 `UB` | ❌ no detectado | — |
| 226 | [`f_deque_erase_begin_ptr_guarda`](casos/deque/erase_begin.md#f_deque_erase_begin_ptr_guarda) | `deque` | `erase_begin` | `ptr` | `guarda` | 🔴 `UB` | ❌ no detectado | — |
| 227 | [`f_deque_erase_begin_ptr_bucle`](casos/deque/erase_begin.md#f_deque_erase_begin_ptr_bucle) | `deque` | `erase_begin` | `ptr` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 228 | [`f_deque_erase_begin_ptr_llamada`](casos/deque/erase_begin.md#f_deque_erase_begin_ptr_llamada) | `deque` | `erase_begin` | `ptr` | `llamada` | 🔴 `UB` | ❌ no detectado | — |
| 229 | [`f_deque_clear_it_recto`](casos/deque/clear.md#f_deque_clear_it_recto) | `deque` | `clear` | `it` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 230 | [`f_deque_clear_it_guarda`](casos/deque/clear.md#f_deque_clear_it_guarda) | `deque` | `clear` | `it` | `guarda` | 🔴 `UB` | ✅ detectado | 🛑 |
| 231 | [`f_deque_clear_it_bucle`](casos/deque/clear.md#f_deque_clear_it_bucle) | `deque` | `clear` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 232 | [`f_deque_clear_it_llamada`](casos/deque/clear.md#f_deque_clear_it_llamada) | `deque` | `clear` | `it` | `llamada` | 🔴 `UB` | ✅ detectado | 🛑 |
| 233 | [`f_deque_clear_ref_recto`](casos/deque/clear.md#f_deque_clear_ref_recto) | `deque` | `clear` | `ref` | `recto` | 🔴 `UB` | ❌ no detectado | — |
| 234 | [`f_deque_clear_ref_guarda`](casos/deque/clear.md#f_deque_clear_ref_guarda) | `deque` | `clear` | `ref` | `guarda` | 🔴 `UB` | ❌ no detectado | — |
| 235 | [`f_deque_clear_ref_bucle`](casos/deque/clear.md#f_deque_clear_ref_bucle) | `deque` | `clear` | `ref` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 236 | [`f_deque_clear_ref_llamada`](casos/deque/clear.md#f_deque_clear_ref_llamada) | `deque` | `clear` | `ref` | `llamada` | 🔴 `UB` | ❌ no detectado | — |
| 237 | [`f_deque_clear_ptr_recto`](casos/deque/clear.md#f_deque_clear_ptr_recto) | `deque` | `clear` | `ptr` | `recto` | 🔴 `UB` | ❌ no detectado | — |
| 238 | [`f_deque_clear_ptr_guarda`](casos/deque/clear.md#f_deque_clear_ptr_guarda) | `deque` | `clear` | `ptr` | `guarda` | 🔴 `UB` | ❌ no detectado | — |
| 239 | [`f_deque_clear_ptr_bucle`](casos/deque/clear.md#f_deque_clear_ptr_bucle) | `deque` | `clear` | `ptr` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 240 | [`f_deque_clear_ptr_llamada`](casos/deque/clear.md#f_deque_clear_ptr_llamada) | `deque` | `clear` | `ptr` | `llamada` | 🔴 `UB` | ❌ no detectado | — |
| 241 | [`f_deque_resize_grow_it_recto`](casos/deque/resize_grow.md#f_deque_resize_grow_it_recto) | `deque` | `resize_grow` | `it` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 242 | [`f_deque_resize_grow_it_guarda`](casos/deque/resize_grow.md#f_deque_resize_grow_it_guarda) | `deque` | `resize_grow` | `it` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 243 | [`f_deque_resize_grow_it_bucle`](casos/deque/resize_grow.md#f_deque_resize_grow_it_bucle) | `deque` | `resize_grow` | `it` | `bucle` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 244 | [`f_deque_resize_grow_it_llamada`](casos/deque/resize_grow.md#f_deque_resize_grow_it_llamada) | `deque` | `resize_grow` | `it` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 245 | [`f_deque_resize_grow_ref_recto`](casos/deque/resize_grow.md#f_deque_resize_grow_ref_recto) | `deque` | `resize_grow` | `ref` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 246 | [`f_deque_resize_grow_ref_guarda`](casos/deque/resize_grow.md#f_deque_resize_grow_ref_guarda) | `deque` | `resize_grow` | `ref` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 247 | [`f_deque_resize_grow_ref_bucle`](casos/deque/resize_grow.md#f_deque_resize_grow_ref_bucle) | `deque` | `resize_grow` | `ref` | `bucle` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 248 | [`f_deque_resize_grow_ref_llamada`](casos/deque/resize_grow.md#f_deque_resize_grow_ref_llamada) | `deque` | `resize_grow` | `ref` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 249 | [`f_deque_resize_grow_ptr_recto`](casos/deque/resize_grow.md#f_deque_resize_grow_ptr_recto) | `deque` | `resize_grow` | `ptr` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 250 | [`f_deque_resize_grow_ptr_guarda`](casos/deque/resize_grow.md#f_deque_resize_grow_ptr_guarda) | `deque` | `resize_grow` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 251 | [`f_deque_resize_grow_ptr_bucle`](casos/deque/resize_grow.md#f_deque_resize_grow_ptr_bucle) | `deque` | `resize_grow` | `ptr` | `bucle` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 252 | [`f_deque_resize_grow_ptr_llamada`](casos/deque/resize_grow.md#f_deque_resize_grow_ptr_llamada) | `deque` | `resize_grow` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 253 | [`f_deque_pop_front_it_recto`](casos/deque/pop_front.md#f_deque_pop_front_it_recto) | `deque` | `pop_front` | `it` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 254 | [`f_deque_pop_front_it_guarda`](casos/deque/pop_front.md#f_deque_pop_front_it_guarda) | `deque` | `pop_front` | `it` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 255 | [`f_deque_pop_front_it_bucle`](casos/deque/pop_front.md#f_deque_pop_front_it_bucle) | `deque` | `pop_front` | `it` | `bucle` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 256 | [`f_deque_pop_front_it_llamada`](casos/deque/pop_front.md#f_deque_pop_front_it_llamada) | `deque` | `pop_front` | `it` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 257 | [`f_deque_pop_front_ref_recto`](casos/deque/pop_front.md#f_deque_pop_front_ref_recto) | `deque` | `pop_front` | `ref` | `recto` | 🔴 `UB` | ❌ no detectado | — |
| 258 | [`f_deque_pop_front_ref_guarda`](casos/deque/pop_front.md#f_deque_pop_front_ref_guarda) | `deque` | `pop_front` | `ref` | `guarda` | 🔴 `UB` | ❌ no detectado | — |
| 259 | [`f_deque_pop_front_ref_bucle`](casos/deque/pop_front.md#f_deque_pop_front_ref_bucle) | `deque` | `pop_front` | `ref` | `bucle` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 260 | [`f_deque_pop_front_ref_llamada`](casos/deque/pop_front.md#f_deque_pop_front_ref_llamada) | `deque` | `pop_front` | `ref` | `llamada` | 🔴 `UB` | ❌ no detectado | — |
| 261 | [`f_deque_pop_front_ptr_recto`](casos/deque/pop_front.md#f_deque_pop_front_ptr_recto) | `deque` | `pop_front` | `ptr` | `recto` | 🔴 `UB` | ❌ no detectado | — |
| 262 | [`f_deque_pop_front_ptr_guarda`](casos/deque/pop_front.md#f_deque_pop_front_ptr_guarda) | `deque` | `pop_front` | `ptr` | `guarda` | 🔴 `UB` | ❌ no detectado | — |
| 263 | [`f_deque_pop_front_ptr_bucle`](casos/deque/pop_front.md#f_deque_pop_front_ptr_bucle) | `deque` | `pop_front` | `ptr` | `bucle` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 264 | [`f_deque_pop_front_ptr_llamada`](casos/deque/pop_front.md#f_deque_pop_front_ptr_llamada) | `deque` | `pop_front` | `ptr` | `llamada` | 🔴 `UB` | ❌ no detectado | — |
| 265 | [`f_list_push_back_it_recto`](casos/list/push_back.md#f_list_push_back_it_recto) | `list` | `push_back` | `it` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 266 | [`f_list_push_back_it_guarda`](casos/list/push_back.md#f_list_push_back_it_guarda) | `list` | `push_back` | `it` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 267 | [`f_list_push_back_it_bucle`](casos/list/push_back.md#f_list_push_back_it_bucle) | `list` | `push_back` | `it` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 268 | [`f_list_push_back_it_llamada`](casos/list/push_back.md#f_list_push_back_it_llamada) | `list` | `push_back` | `it` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 269 | [`f_list_push_back_ref_recto`](casos/list/push_back.md#f_list_push_back_ref_recto) | `list` | `push_back` | `ref` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 270 | [`f_list_push_back_ref_guarda`](casos/list/push_back.md#f_list_push_back_ref_guarda) | `list` | `push_back` | `ref` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 271 | [`f_list_push_back_ref_bucle`](casos/list/push_back.md#f_list_push_back_ref_bucle) | `list` | `push_back` | `ref` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 272 | [`f_list_push_back_ref_llamada`](casos/list/push_back.md#f_list_push_back_ref_llamada) | `list` | `push_back` | `ref` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 273 | [`f_list_push_back_ptr_recto`](casos/list/push_back.md#f_list_push_back_ptr_recto) | `list` | `push_back` | `ptr` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 274 | [`f_list_push_back_ptr_guarda`](casos/list/push_back.md#f_list_push_back_ptr_guarda) | `list` | `push_back` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 275 | [`f_list_push_back_ptr_bucle`](casos/list/push_back.md#f_list_push_back_ptr_bucle) | `list` | `push_back` | `ptr` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 276 | [`f_list_push_back_ptr_llamada`](casos/list/push_back.md#f_list_push_back_ptr_llamada) | `list` | `push_back` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 277 | [`f_list_push_front_it_recto`](casos/list/push_front.md#f_list_push_front_it_recto) | `list` | `push_front` | `it` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 278 | [`f_list_push_front_it_guarda`](casos/list/push_front.md#f_list_push_front_it_guarda) | `list` | `push_front` | `it` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 279 | [`f_list_push_front_it_bucle`](casos/list/push_front.md#f_list_push_front_it_bucle) | `list` | `push_front` | `it` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 280 | [`f_list_push_front_it_llamada`](casos/list/push_front.md#f_list_push_front_it_llamada) | `list` | `push_front` | `it` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 281 | [`f_list_push_front_ref_recto`](casos/list/push_front.md#f_list_push_front_ref_recto) | `list` | `push_front` | `ref` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 282 | [`f_list_push_front_ref_guarda`](casos/list/push_front.md#f_list_push_front_ref_guarda) | `list` | `push_front` | `ref` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 283 | [`f_list_push_front_ref_bucle`](casos/list/push_front.md#f_list_push_front_ref_bucle) | `list` | `push_front` | `ref` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 284 | [`f_list_push_front_ref_llamada`](casos/list/push_front.md#f_list_push_front_ref_llamada) | `list` | `push_front` | `ref` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 285 | [`f_list_push_front_ptr_recto`](casos/list/push_front.md#f_list_push_front_ptr_recto) | `list` | `push_front` | `ptr` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 286 | [`f_list_push_front_ptr_guarda`](casos/list/push_front.md#f_list_push_front_ptr_guarda) | `list` | `push_front` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 287 | [`f_list_push_front_ptr_bucle`](casos/list/push_front.md#f_list_push_front_ptr_bucle) | `list` | `push_front` | `ptr` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 288 | [`f_list_push_front_ptr_llamada`](casos/list/push_front.md#f_list_push_front_ptr_llamada) | `list` | `push_front` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 289 | [`f_list_insert_it_recto`](casos/list/insert.md#f_list_insert_it_recto) | `list` | `insert` | `it` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 290 | [`f_list_insert_it_guarda`](casos/list/insert.md#f_list_insert_it_guarda) | `list` | `insert` | `it` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 291 | [`f_list_insert_it_bucle`](casos/list/insert.md#f_list_insert_it_bucle) | `list` | `insert` | `it` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 292 | [`f_list_insert_it_llamada`](casos/list/insert.md#f_list_insert_it_llamada) | `list` | `insert` | `it` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 293 | [`f_list_insert_ref_recto`](casos/list/insert.md#f_list_insert_ref_recto) | `list` | `insert` | `ref` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 294 | [`f_list_insert_ref_guarda`](casos/list/insert.md#f_list_insert_ref_guarda) | `list` | `insert` | `ref` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 295 | [`f_list_insert_ref_bucle`](casos/list/insert.md#f_list_insert_ref_bucle) | `list` | `insert` | `ref` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 296 | [`f_list_insert_ref_llamada`](casos/list/insert.md#f_list_insert_ref_llamada) | `list` | `insert` | `ref` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 297 | [`f_list_insert_ptr_recto`](casos/list/insert.md#f_list_insert_ptr_recto) | `list` | `insert` | `ptr` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 298 | [`f_list_insert_ptr_guarda`](casos/list/insert.md#f_list_insert_ptr_guarda) | `list` | `insert` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 299 | [`f_list_insert_ptr_bucle`](casos/list/insert.md#f_list_insert_ptr_bucle) | `list` | `insert` | `ptr` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 300 | [`f_list_insert_ptr_llamada`](casos/list/insert.md#f_list_insert_ptr_llamada) | `list` | `insert` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 301 | [`f_list_erase_begin_it_recto`](casos/list/erase_begin.md#f_list_erase_begin_it_recto) | `list` | `erase_begin` | `it` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 302 | [`f_list_erase_begin_it_guarda`](casos/list/erase_begin.md#f_list_erase_begin_it_guarda) | `list` | `erase_begin` | `it` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 303 | [`f_list_erase_begin_it_bucle`](casos/list/erase_begin.md#f_list_erase_begin_it_bucle) | `list` | `erase_begin` | `it` | `bucle` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 304 | [`f_list_erase_begin_it_llamada`](casos/list/erase_begin.md#f_list_erase_begin_it_llamada) | `list` | `erase_begin` | `it` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 305 | [`f_list_erase_begin_ref_recto`](casos/list/erase_begin.md#f_list_erase_begin_ref_recto) | `list` | `erase_begin` | `ref` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 306 | [`f_list_erase_begin_ref_guarda`](casos/list/erase_begin.md#f_list_erase_begin_ref_guarda) | `list` | `erase_begin` | `ref` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 307 | [`f_list_erase_begin_ref_bucle`](casos/list/erase_begin.md#f_list_erase_begin_ref_bucle) | `list` | `erase_begin` | `ref` | `bucle` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 308 | [`f_list_erase_begin_ref_llamada`](casos/list/erase_begin.md#f_list_erase_begin_ref_llamada) | `list` | `erase_begin` | `ref` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 309 | [`f_list_erase_begin_ptr_recto`](casos/list/erase_begin.md#f_list_erase_begin_ptr_recto) | `list` | `erase_begin` | `ptr` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 310 | [`f_list_erase_begin_ptr_guarda`](casos/list/erase_begin.md#f_list_erase_begin_ptr_guarda) | `list` | `erase_begin` | `ptr` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 311 | [`f_list_erase_begin_ptr_bucle`](casos/list/erase_begin.md#f_list_erase_begin_ptr_bucle) | `list` | `erase_begin` | `ptr` | `bucle` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 312 | [`f_list_erase_begin_ptr_llamada`](casos/list/erase_begin.md#f_list_erase_begin_ptr_llamada) | `list` | `erase_begin` | `ptr` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 313 | [`f_list_clear_it_recto`](casos/list/clear.md#f_list_clear_it_recto) | `list` | `clear` | `it` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 314 | [`f_list_clear_it_guarda`](casos/list/clear.md#f_list_clear_it_guarda) | `list` | `clear` | `it` | `guarda` | 🔴 `UB` | ✅ detectado | 🛑 |
| 315 | [`f_list_clear_it_bucle`](casos/list/clear.md#f_list_clear_it_bucle) | `list` | `clear` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 316 | [`f_list_clear_it_llamada`](casos/list/clear.md#f_list_clear_it_llamada) | `list` | `clear` | `it` | `llamada` | 🔴 `UB` | ✅ detectado | 🛑 |
| 317 | [`f_list_clear_ref_recto`](casos/list/clear.md#f_list_clear_ref_recto) | `list` | `clear` | `ref` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 318 | [`f_list_clear_ref_guarda`](casos/list/clear.md#f_list_clear_ref_guarda) | `list` | `clear` | `ref` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 319 | [`f_list_clear_ref_bucle`](casos/list/clear.md#f_list_clear_ref_bucle) | `list` | `clear` | `ref` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 320 | [`f_list_clear_ref_llamada`](casos/list/clear.md#f_list_clear_ref_llamada) | `list` | `clear` | `ref` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 321 | [`f_list_clear_ptr_recto`](casos/list/clear.md#f_list_clear_ptr_recto) | `list` | `clear` | `ptr` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 322 | [`f_list_clear_ptr_guarda`](casos/list/clear.md#f_list_clear_ptr_guarda) | `list` | `clear` | `ptr` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 323 | [`f_list_clear_ptr_bucle`](casos/list/clear.md#f_list_clear_ptr_bucle) | `list` | `clear` | `ptr` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 324 | [`f_list_clear_ptr_llamada`](casos/list/clear.md#f_list_clear_ptr_llamada) | `list` | `clear` | `ptr` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 325 | [`f_list_resize_grow_it_recto`](casos/list/resize_grow.md#f_list_resize_grow_it_recto) | `list` | `resize_grow` | `it` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 326 | [`f_list_resize_grow_it_guarda`](casos/list/resize_grow.md#f_list_resize_grow_it_guarda) | `list` | `resize_grow` | `it` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 327 | [`f_list_resize_grow_it_bucle`](casos/list/resize_grow.md#f_list_resize_grow_it_bucle) | `list` | `resize_grow` | `it` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 328 | [`f_list_resize_grow_it_llamada`](casos/list/resize_grow.md#f_list_resize_grow_it_llamada) | `list` | `resize_grow` | `it` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 329 | [`f_list_resize_grow_ref_recto`](casos/list/resize_grow.md#f_list_resize_grow_ref_recto) | `list` | `resize_grow` | `ref` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 330 | [`f_list_resize_grow_ref_guarda`](casos/list/resize_grow.md#f_list_resize_grow_ref_guarda) | `list` | `resize_grow` | `ref` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 331 | [`f_list_resize_grow_ref_bucle`](casos/list/resize_grow.md#f_list_resize_grow_ref_bucle) | `list` | `resize_grow` | `ref` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 332 | [`f_list_resize_grow_ref_llamada`](casos/list/resize_grow.md#f_list_resize_grow_ref_llamada) | `list` | `resize_grow` | `ref` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 333 | [`f_list_resize_grow_ptr_recto`](casos/list/resize_grow.md#f_list_resize_grow_ptr_recto) | `list` | `resize_grow` | `ptr` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 334 | [`f_list_resize_grow_ptr_guarda`](casos/list/resize_grow.md#f_list_resize_grow_ptr_guarda) | `list` | `resize_grow` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 335 | [`f_list_resize_grow_ptr_bucle`](casos/list/resize_grow.md#f_list_resize_grow_ptr_bucle) | `list` | `resize_grow` | `ptr` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 336 | [`f_list_resize_grow_ptr_llamada`](casos/list/resize_grow.md#f_list_resize_grow_ptr_llamada) | `list` | `resize_grow` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 337 | [`f_list_pop_front_it_recto`](casos/list/pop_front.md#f_list_pop_front_it_recto) | `list` | `pop_front` | `it` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 338 | [`f_list_pop_front_it_guarda`](casos/list/pop_front.md#f_list_pop_front_it_guarda) | `list` | `pop_front` | `it` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 339 | [`f_list_pop_front_it_bucle`](casos/list/pop_front.md#f_list_pop_front_it_bucle) | `list` | `pop_front` | `it` | `bucle` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 340 | [`f_list_pop_front_it_llamada`](casos/list/pop_front.md#f_list_pop_front_it_llamada) | `list` | `pop_front` | `it` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 341 | [`f_list_pop_front_ref_recto`](casos/list/pop_front.md#f_list_pop_front_ref_recto) | `list` | `pop_front` | `ref` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 342 | [`f_list_pop_front_ref_guarda`](casos/list/pop_front.md#f_list_pop_front_ref_guarda) | `list` | `pop_front` | `ref` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 343 | [`f_list_pop_front_ref_bucle`](casos/list/pop_front.md#f_list_pop_front_ref_bucle) | `list` | `pop_front` | `ref` | `bucle` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 344 | [`f_list_pop_front_ref_llamada`](casos/list/pop_front.md#f_list_pop_front_ref_llamada) | `list` | `pop_front` | `ref` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 345 | [`f_list_pop_front_ptr_recto`](casos/list/pop_front.md#f_list_pop_front_ptr_recto) | `list` | `pop_front` | `ptr` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 346 | [`f_list_pop_front_ptr_guarda`](casos/list/pop_front.md#f_list_pop_front_ptr_guarda) | `list` | `pop_front` | `ptr` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 347 | [`f_list_pop_front_ptr_bucle`](casos/list/pop_front.md#f_list_pop_front_ptr_bucle) | `list` | `pop_front` | `ptr` | `bucle` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 348 | [`f_list_pop_front_ptr_llamada`](casos/list/pop_front.md#f_list_pop_front_ptr_llamada) | `list` | `pop_front` | `ptr` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 349 | [`f_list_reverse_it_recto`](casos/list/reverse.md#f_list_reverse_it_recto) | `list` | `reverse` | `it` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 350 | [`f_list_reverse_it_guarda`](casos/list/reverse.md#f_list_reverse_it_guarda) | `list` | `reverse` | `it` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 351 | [`f_list_reverse_it_bucle`](casos/list/reverse.md#f_list_reverse_it_bucle) | `list` | `reverse` | `it` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 352 | [`f_list_reverse_it_llamada`](casos/list/reverse.md#f_list_reverse_it_llamada) | `list` | `reverse` | `it` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 353 | [`f_list_reverse_ref_recto`](casos/list/reverse.md#f_list_reverse_ref_recto) | `list` | `reverse` | `ref` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 354 | [`f_list_reverse_ref_guarda`](casos/list/reverse.md#f_list_reverse_ref_guarda) | `list` | `reverse` | `ref` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 355 | [`f_list_reverse_ref_bucle`](casos/list/reverse.md#f_list_reverse_ref_bucle) | `list` | `reverse` | `ref` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 356 | [`f_list_reverse_ref_llamada`](casos/list/reverse.md#f_list_reverse_ref_llamada) | `list` | `reverse` | `ref` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 357 | [`f_list_reverse_ptr_recto`](casos/list/reverse.md#f_list_reverse_ptr_recto) | `list` | `reverse` | `ptr` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 358 | [`f_list_reverse_ptr_guarda`](casos/list/reverse.md#f_list_reverse_ptr_guarda) | `list` | `reverse` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 359 | [`f_list_reverse_ptr_bucle`](casos/list/reverse.md#f_list_reverse_ptr_bucle) | `list` | `reverse` | `ptr` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 360 | [`f_list_reverse_ptr_llamada`](casos/list/reverse.md#f_list_reverse_ptr_llamada) | `list` | `reverse` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 361 | [`f_list_sort_it_recto`](casos/list/sort.md#f_list_sort_it_recto) | `list` | `sort` | `it` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 362 | [`f_list_sort_it_guarda`](casos/list/sort.md#f_list_sort_it_guarda) | `list` | `sort` | `it` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 363 | [`f_list_sort_it_bucle`](casos/list/sort.md#f_list_sort_it_bucle) | `list` | `sort` | `it` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 364 | [`f_list_sort_it_llamada`](casos/list/sort.md#f_list_sort_it_llamada) | `list` | `sort` | `it` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 365 | [`f_list_sort_ref_recto`](casos/list/sort.md#f_list_sort_ref_recto) | `list` | `sort` | `ref` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 366 | [`f_list_sort_ref_guarda`](casos/list/sort.md#f_list_sort_ref_guarda) | `list` | `sort` | `ref` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 367 | [`f_list_sort_ref_bucle`](casos/list/sort.md#f_list_sort_ref_bucle) | `list` | `sort` | `ref` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 368 | [`f_list_sort_ref_llamada`](casos/list/sort.md#f_list_sort_ref_llamada) | `list` | `sort` | `ref` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 369 | [`f_list_sort_ptr_recto`](casos/list/sort.md#f_list_sort_ptr_recto) | `list` | `sort` | `ptr` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 370 | [`f_list_sort_ptr_guarda`](casos/list/sort.md#f_list_sort_ptr_guarda) | `list` | `sort` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 371 | [`f_list_sort_ptr_bucle`](casos/list/sort.md#f_list_sort_ptr_bucle) | `list` | `sort` | `ptr` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 372 | [`f_list_sort_ptr_llamada`](casos/list/sort.md#f_list_sort_ptr_llamada) | `list` | `sort` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 373 | [`f_flist_push_front_it_recto`](casos/flist/push_front.md#f_flist_push_front_it_recto) | `flist` | `push_front` | `it` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 374 | [`f_flist_push_front_it_guarda`](casos/flist/push_front.md#f_flist_push_front_it_guarda) | `flist` | `push_front` | `it` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 375 | [`f_flist_push_front_it_bucle`](casos/flist/push_front.md#f_flist_push_front_it_bucle) | `flist` | `push_front` | `it` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 376 | [`f_flist_push_front_it_llamada`](casos/flist/push_front.md#f_flist_push_front_it_llamada) | `flist` | `push_front` | `it` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 377 | [`f_flist_push_front_ref_recto`](casos/flist/push_front.md#f_flist_push_front_ref_recto) | `flist` | `push_front` | `ref` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 378 | [`f_flist_push_front_ref_guarda`](casos/flist/push_front.md#f_flist_push_front_ref_guarda) | `flist` | `push_front` | `ref` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 379 | [`f_flist_push_front_ref_bucle`](casos/flist/push_front.md#f_flist_push_front_ref_bucle) | `flist` | `push_front` | `ref` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 380 | [`f_flist_push_front_ref_llamada`](casos/flist/push_front.md#f_flist_push_front_ref_llamada) | `flist` | `push_front` | `ref` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 381 | [`f_flist_push_front_ptr_recto`](casos/flist/push_front.md#f_flist_push_front_ptr_recto) | `flist` | `push_front` | `ptr` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 382 | [`f_flist_push_front_ptr_guarda`](casos/flist/push_front.md#f_flist_push_front_ptr_guarda) | `flist` | `push_front` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 383 | [`f_flist_push_front_ptr_bucle`](casos/flist/push_front.md#f_flist_push_front_ptr_bucle) | `flist` | `push_front` | `ptr` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 384 | [`f_flist_push_front_ptr_llamada`](casos/flist/push_front.md#f_flist_push_front_ptr_llamada) | `flist` | `push_front` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 385 | [`f_flist_insert_after_it_recto`](casos/flist/insert_after.md#f_flist_insert_after_it_recto) | `flist` | `insert_after` | `it` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 386 | [`f_flist_insert_after_it_guarda`](casos/flist/insert_after.md#f_flist_insert_after_it_guarda) | `flist` | `insert_after` | `it` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 387 | [`f_flist_insert_after_it_bucle`](casos/flist/insert_after.md#f_flist_insert_after_it_bucle) | `flist` | `insert_after` | `it` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 388 | [`f_flist_insert_after_it_llamada`](casos/flist/insert_after.md#f_flist_insert_after_it_llamada) | `flist` | `insert_after` | `it` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 389 | [`f_flist_insert_after_ref_recto`](casos/flist/insert_after.md#f_flist_insert_after_ref_recto) | `flist` | `insert_after` | `ref` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 390 | [`f_flist_insert_after_ref_guarda`](casos/flist/insert_after.md#f_flist_insert_after_ref_guarda) | `flist` | `insert_after` | `ref` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 391 | [`f_flist_insert_after_ref_bucle`](casos/flist/insert_after.md#f_flist_insert_after_ref_bucle) | `flist` | `insert_after` | `ref` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 392 | [`f_flist_insert_after_ref_llamada`](casos/flist/insert_after.md#f_flist_insert_after_ref_llamada) | `flist` | `insert_after` | `ref` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 393 | [`f_flist_insert_after_ptr_recto`](casos/flist/insert_after.md#f_flist_insert_after_ptr_recto) | `flist` | `insert_after` | `ptr` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 394 | [`f_flist_insert_after_ptr_guarda`](casos/flist/insert_after.md#f_flist_insert_after_ptr_guarda) | `flist` | `insert_after` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 395 | [`f_flist_insert_after_ptr_bucle`](casos/flist/insert_after.md#f_flist_insert_after_ptr_bucle) | `flist` | `insert_after` | `ptr` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 396 | [`f_flist_insert_after_ptr_llamada`](casos/flist/insert_after.md#f_flist_insert_after_ptr_llamada) | `flist` | `insert_after` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 397 | [`f_flist_erase_after_it_recto`](casos/flist/erase_after.md#f_flist_erase_after_it_recto) | `flist` | `erase_after` | `it` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 398 | [`f_flist_erase_after_it_guarda`](casos/flist/erase_after.md#f_flist_erase_after_it_guarda) | `flist` | `erase_after` | `it` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 399 | [`f_flist_erase_after_it_bucle`](casos/flist/erase_after.md#f_flist_erase_after_it_bucle) | `flist` | `erase_after` | `it` | `bucle` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 400 | [`f_flist_erase_after_it_llamada`](casos/flist/erase_after.md#f_flist_erase_after_it_llamada) | `flist` | `erase_after` | `it` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 401 | [`f_flist_erase_after_ref_recto`](casos/flist/erase_after.md#f_flist_erase_after_ref_recto) | `flist` | `erase_after` | `ref` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 402 | [`f_flist_erase_after_ref_guarda`](casos/flist/erase_after.md#f_flist_erase_after_ref_guarda) | `flist` | `erase_after` | `ref` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 403 | [`f_flist_erase_after_ref_bucle`](casos/flist/erase_after.md#f_flist_erase_after_ref_bucle) | `flist` | `erase_after` | `ref` | `bucle` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 404 | [`f_flist_erase_after_ref_llamada`](casos/flist/erase_after.md#f_flist_erase_after_ref_llamada) | `flist` | `erase_after` | `ref` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 405 | [`f_flist_erase_after_ptr_recto`](casos/flist/erase_after.md#f_flist_erase_after_ptr_recto) | `flist` | `erase_after` | `ptr` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 406 | [`f_flist_erase_after_ptr_guarda`](casos/flist/erase_after.md#f_flist_erase_after_ptr_guarda) | `flist` | `erase_after` | `ptr` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 407 | [`f_flist_erase_after_ptr_bucle`](casos/flist/erase_after.md#f_flist_erase_after_ptr_bucle) | `flist` | `erase_after` | `ptr` | `bucle` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 408 | [`f_flist_erase_after_ptr_llamada`](casos/flist/erase_after.md#f_flist_erase_after_ptr_llamada) | `flist` | `erase_after` | `ptr` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 409 | [`f_flist_clear_it_recto`](casos/flist/clear.md#f_flist_clear_it_recto) | `flist` | `clear` | `it` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 410 | [`f_flist_clear_it_guarda`](casos/flist/clear.md#f_flist_clear_it_guarda) | `flist` | `clear` | `it` | `guarda` | 🔴 `UB` | ✅ detectado | 🛑 |
| 411 | [`f_flist_clear_it_bucle`](casos/flist/clear.md#f_flist_clear_it_bucle) | `flist` | `clear` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 412 | [`f_flist_clear_it_llamada`](casos/flist/clear.md#f_flist_clear_it_llamada) | `flist` | `clear` | `it` | `llamada` | 🔴 `UB` | ✅ detectado | 🛑 |
| 413 | [`f_flist_clear_ref_recto`](casos/flist/clear.md#f_flist_clear_ref_recto) | `flist` | `clear` | `ref` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 414 | [`f_flist_clear_ref_guarda`](casos/flist/clear.md#f_flist_clear_ref_guarda) | `flist` | `clear` | `ref` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 415 | [`f_flist_clear_ref_bucle`](casos/flist/clear.md#f_flist_clear_ref_bucle) | `flist` | `clear` | `ref` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 416 | [`f_flist_clear_ref_llamada`](casos/flist/clear.md#f_flist_clear_ref_llamada) | `flist` | `clear` | `ref` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 417 | [`f_flist_clear_ptr_recto`](casos/flist/clear.md#f_flist_clear_ptr_recto) | `flist` | `clear` | `ptr` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 418 | [`f_flist_clear_ptr_guarda`](casos/flist/clear.md#f_flist_clear_ptr_guarda) | `flist` | `clear` | `ptr` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 419 | [`f_flist_clear_ptr_bucle`](casos/flist/clear.md#f_flist_clear_ptr_bucle) | `flist` | `clear` | `ptr` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 420 | [`f_flist_clear_ptr_llamada`](casos/flist/clear.md#f_flist_clear_ptr_llamada) | `flist` | `clear` | `ptr` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 421 | [`f_set_insert_it_recto`](casos/set/insert.md#f_set_insert_it_recto) | `set` | `insert` | `it` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 422 | [`f_set_insert_it_guarda`](casos/set/insert.md#f_set_insert_it_guarda) | `set` | `insert` | `it` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 423 | [`f_set_insert_it_bucle`](casos/set/insert.md#f_set_insert_it_bucle) | `set` | `insert` | `it` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 424 | [`f_set_insert_it_llamada`](casos/set/insert.md#f_set_insert_it_llamada) | `set` | `insert` | `it` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 425 | [`f_set_insert_ref_recto`](casos/set/insert.md#f_set_insert_ref_recto) | `set` | `insert` | `ref` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 426 | [`f_set_insert_ref_guarda`](casos/set/insert.md#f_set_insert_ref_guarda) | `set` | `insert` | `ref` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 427 | [`f_set_insert_ref_bucle`](casos/set/insert.md#f_set_insert_ref_bucle) | `set` | `insert` | `ref` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 428 | [`f_set_insert_ref_llamada`](casos/set/insert.md#f_set_insert_ref_llamada) | `set` | `insert` | `ref` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 429 | [`f_set_insert_ptr_recto`](casos/set/insert.md#f_set_insert_ptr_recto) | `set` | `insert` | `ptr` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 430 | [`f_set_insert_ptr_guarda`](casos/set/insert.md#f_set_insert_ptr_guarda) | `set` | `insert` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 431 | [`f_set_insert_ptr_bucle`](casos/set/insert.md#f_set_insert_ptr_bucle) | `set` | `insert` | `ptr` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 432 | [`f_set_insert_ptr_llamada`](casos/set/insert.md#f_set_insert_ptr_llamada) | `set` | `insert` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 433 | [`f_set_emplace_it_recto`](casos/set/emplace.md#f_set_emplace_it_recto) | `set` | `emplace` | `it` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 434 | [`f_set_emplace_it_guarda`](casos/set/emplace.md#f_set_emplace_it_guarda) | `set` | `emplace` | `it` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 435 | [`f_set_emplace_it_bucle`](casos/set/emplace.md#f_set_emplace_it_bucle) | `set` | `emplace` | `it` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 436 | [`f_set_emplace_it_llamada`](casos/set/emplace.md#f_set_emplace_it_llamada) | `set` | `emplace` | `it` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 437 | [`f_set_emplace_ref_recto`](casos/set/emplace.md#f_set_emplace_ref_recto) | `set` | `emplace` | `ref` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 438 | [`f_set_emplace_ref_guarda`](casos/set/emplace.md#f_set_emplace_ref_guarda) | `set` | `emplace` | `ref` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 439 | [`f_set_emplace_ref_bucle`](casos/set/emplace.md#f_set_emplace_ref_bucle) | `set` | `emplace` | `ref` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 440 | [`f_set_emplace_ref_llamada`](casos/set/emplace.md#f_set_emplace_ref_llamada) | `set` | `emplace` | `ref` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 441 | [`f_set_emplace_ptr_recto`](casos/set/emplace.md#f_set_emplace_ptr_recto) | `set` | `emplace` | `ptr` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 442 | [`f_set_emplace_ptr_guarda`](casos/set/emplace.md#f_set_emplace_ptr_guarda) | `set` | `emplace` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 443 | [`f_set_emplace_ptr_bucle`](casos/set/emplace.md#f_set_emplace_ptr_bucle) | `set` | `emplace` | `ptr` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 444 | [`f_set_emplace_ptr_llamada`](casos/set/emplace.md#f_set_emplace_ptr_llamada) | `set` | `emplace` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 445 | [`f_set_erase_begin_it_recto`](casos/set/erase_begin.md#f_set_erase_begin_it_recto) | `set` | `erase_begin` | `it` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 446 | [`f_set_erase_begin_it_guarda`](casos/set/erase_begin.md#f_set_erase_begin_it_guarda) | `set` | `erase_begin` | `it` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 447 | [`f_set_erase_begin_it_bucle`](casos/set/erase_begin.md#f_set_erase_begin_it_bucle) | `set` | `erase_begin` | `it` | `bucle` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 448 | [`f_set_erase_begin_it_llamada`](casos/set/erase_begin.md#f_set_erase_begin_it_llamada) | `set` | `erase_begin` | `it` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 449 | [`f_set_erase_begin_ref_recto`](casos/set/erase_begin.md#f_set_erase_begin_ref_recto) | `set` | `erase_begin` | `ref` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 450 | [`f_set_erase_begin_ref_guarda`](casos/set/erase_begin.md#f_set_erase_begin_ref_guarda) | `set` | `erase_begin` | `ref` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 451 | [`f_set_erase_begin_ref_bucle`](casos/set/erase_begin.md#f_set_erase_begin_ref_bucle) | `set` | `erase_begin` | `ref` | `bucle` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 452 | [`f_set_erase_begin_ref_llamada`](casos/set/erase_begin.md#f_set_erase_begin_ref_llamada) | `set` | `erase_begin` | `ref` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 453 | [`f_set_erase_begin_ptr_recto`](casos/set/erase_begin.md#f_set_erase_begin_ptr_recto) | `set` | `erase_begin` | `ptr` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 454 | [`f_set_erase_begin_ptr_guarda`](casos/set/erase_begin.md#f_set_erase_begin_ptr_guarda) | `set` | `erase_begin` | `ptr` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 455 | [`f_set_erase_begin_ptr_bucle`](casos/set/erase_begin.md#f_set_erase_begin_ptr_bucle) | `set` | `erase_begin` | `ptr` | `bucle` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 456 | [`f_set_erase_begin_ptr_llamada`](casos/set/erase_begin.md#f_set_erase_begin_ptr_llamada) | `set` | `erase_begin` | `ptr` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 457 | [`f_set_clear_it_recto`](casos/set/clear.md#f_set_clear_it_recto) | `set` | `clear` | `it` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 458 | [`f_set_clear_it_guarda`](casos/set/clear.md#f_set_clear_it_guarda) | `set` | `clear` | `it` | `guarda` | 🔴 `UB` | ✅ detectado | 🛑 |
| 459 | [`f_set_clear_it_bucle`](casos/set/clear.md#f_set_clear_it_bucle) | `set` | `clear` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 460 | [`f_set_clear_it_llamada`](casos/set/clear.md#f_set_clear_it_llamada) | `set` | `clear` | `it` | `llamada` | 🔴 `UB` | ✅ detectado | 🛑 |
| 461 | [`f_set_clear_ref_recto`](casos/set/clear.md#f_set_clear_ref_recto) | `set` | `clear` | `ref` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 462 | [`f_set_clear_ref_guarda`](casos/set/clear.md#f_set_clear_ref_guarda) | `set` | `clear` | `ref` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 463 | [`f_set_clear_ref_bucle`](casos/set/clear.md#f_set_clear_ref_bucle) | `set` | `clear` | `ref` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 464 | [`f_set_clear_ref_llamada`](casos/set/clear.md#f_set_clear_ref_llamada) | `set` | `clear` | `ref` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 465 | [`f_set_clear_ptr_recto`](casos/set/clear.md#f_set_clear_ptr_recto) | `set` | `clear` | `ptr` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 466 | [`f_set_clear_ptr_guarda`](casos/set/clear.md#f_set_clear_ptr_guarda) | `set` | `clear` | `ptr` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 467 | [`f_set_clear_ptr_bucle`](casos/set/clear.md#f_set_clear_ptr_bucle) | `set` | `clear` | `ptr` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 468 | [`f_set_clear_ptr_llamada`](casos/set/clear.md#f_set_clear_ptr_llamada) | `set` | `clear` | `ptr` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 469 | [`f_mset_insert_it_recto`](casos/mset/insert.md#f_mset_insert_it_recto) | `mset` | `insert` | `it` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 470 | [`f_mset_insert_it_guarda`](casos/mset/insert.md#f_mset_insert_it_guarda) | `mset` | `insert` | `it` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 471 | [`f_mset_insert_it_bucle`](casos/mset/insert.md#f_mset_insert_it_bucle) | `mset` | `insert` | `it` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 472 | [`f_mset_insert_it_llamada`](casos/mset/insert.md#f_mset_insert_it_llamada) | `mset` | `insert` | `it` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 473 | [`f_mset_insert_ref_recto`](casos/mset/insert.md#f_mset_insert_ref_recto) | `mset` | `insert` | `ref` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 474 | [`f_mset_insert_ref_guarda`](casos/mset/insert.md#f_mset_insert_ref_guarda) | `mset` | `insert` | `ref` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 475 | [`f_mset_insert_ref_bucle`](casos/mset/insert.md#f_mset_insert_ref_bucle) | `mset` | `insert` | `ref` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 476 | [`f_mset_insert_ref_llamada`](casos/mset/insert.md#f_mset_insert_ref_llamada) | `mset` | `insert` | `ref` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 477 | [`f_mset_insert_ptr_recto`](casos/mset/insert.md#f_mset_insert_ptr_recto) | `mset` | `insert` | `ptr` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 478 | [`f_mset_insert_ptr_guarda`](casos/mset/insert.md#f_mset_insert_ptr_guarda) | `mset` | `insert` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 479 | [`f_mset_insert_ptr_bucle`](casos/mset/insert.md#f_mset_insert_ptr_bucle) | `mset` | `insert` | `ptr` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 480 | [`f_mset_insert_ptr_llamada`](casos/mset/insert.md#f_mset_insert_ptr_llamada) | `mset` | `insert` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 481 | [`f_mset_erase_begin_it_recto`](casos/mset/erase_begin.md#f_mset_erase_begin_it_recto) | `mset` | `erase_begin` | `it` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 482 | [`f_mset_erase_begin_it_guarda`](casos/mset/erase_begin.md#f_mset_erase_begin_it_guarda) | `mset` | `erase_begin` | `it` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 483 | [`f_mset_erase_begin_it_bucle`](casos/mset/erase_begin.md#f_mset_erase_begin_it_bucle) | `mset` | `erase_begin` | `it` | `bucle` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 484 | [`f_mset_erase_begin_it_llamada`](casos/mset/erase_begin.md#f_mset_erase_begin_it_llamada) | `mset` | `erase_begin` | `it` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 485 | [`f_mset_erase_begin_ref_recto`](casos/mset/erase_begin.md#f_mset_erase_begin_ref_recto) | `mset` | `erase_begin` | `ref` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 486 | [`f_mset_erase_begin_ref_guarda`](casos/mset/erase_begin.md#f_mset_erase_begin_ref_guarda) | `mset` | `erase_begin` | `ref` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 487 | [`f_mset_erase_begin_ref_bucle`](casos/mset/erase_begin.md#f_mset_erase_begin_ref_bucle) | `mset` | `erase_begin` | `ref` | `bucle` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 488 | [`f_mset_erase_begin_ref_llamada`](casos/mset/erase_begin.md#f_mset_erase_begin_ref_llamada) | `mset` | `erase_begin` | `ref` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 489 | [`f_mset_erase_begin_ptr_recto`](casos/mset/erase_begin.md#f_mset_erase_begin_ptr_recto) | `mset` | `erase_begin` | `ptr` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 490 | [`f_mset_erase_begin_ptr_guarda`](casos/mset/erase_begin.md#f_mset_erase_begin_ptr_guarda) | `mset` | `erase_begin` | `ptr` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 491 | [`f_mset_erase_begin_ptr_bucle`](casos/mset/erase_begin.md#f_mset_erase_begin_ptr_bucle) | `mset` | `erase_begin` | `ptr` | `bucle` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 492 | [`f_mset_erase_begin_ptr_llamada`](casos/mset/erase_begin.md#f_mset_erase_begin_ptr_llamada) | `mset` | `erase_begin` | `ptr` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 493 | [`f_mset_clear_it_recto`](casos/mset/clear.md#f_mset_clear_it_recto) | `mset` | `clear` | `it` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 494 | [`f_mset_clear_it_guarda`](casos/mset/clear.md#f_mset_clear_it_guarda) | `mset` | `clear` | `it` | `guarda` | 🔴 `UB` | ✅ detectado | 🛑 |
| 495 | [`f_mset_clear_it_bucle`](casos/mset/clear.md#f_mset_clear_it_bucle) | `mset` | `clear` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 496 | [`f_mset_clear_it_llamada`](casos/mset/clear.md#f_mset_clear_it_llamada) | `mset` | `clear` | `it` | `llamada` | 🔴 `UB` | ✅ detectado | 🛑 |
| 497 | [`f_mset_clear_ref_recto`](casos/mset/clear.md#f_mset_clear_ref_recto) | `mset` | `clear` | `ref` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 498 | [`f_mset_clear_ref_guarda`](casos/mset/clear.md#f_mset_clear_ref_guarda) | `mset` | `clear` | `ref` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 499 | [`f_mset_clear_ref_bucle`](casos/mset/clear.md#f_mset_clear_ref_bucle) | `mset` | `clear` | `ref` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 500 | [`f_mset_clear_ref_llamada`](casos/mset/clear.md#f_mset_clear_ref_llamada) | `mset` | `clear` | `ref` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 501 | [`f_mset_clear_ptr_recto`](casos/mset/clear.md#f_mset_clear_ptr_recto) | `mset` | `clear` | `ptr` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 502 | [`f_mset_clear_ptr_guarda`](casos/mset/clear.md#f_mset_clear_ptr_guarda) | `mset` | `clear` | `ptr` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 503 | [`f_mset_clear_ptr_bucle`](casos/mset/clear.md#f_mset_clear_ptr_bucle) | `mset` | `clear` | `ptr` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 504 | [`f_mset_clear_ptr_llamada`](casos/mset/clear.md#f_mset_clear_ptr_llamada) | `mset` | `clear` | `ptr` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 505 | [`f_map_insert_it_recto`](casos/map/insert.md#f_map_insert_it_recto) | `map` | `insert` | `it` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 506 | [`f_map_insert_it_guarda`](casos/map/insert.md#f_map_insert_it_guarda) | `map` | `insert` | `it` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 507 | [`f_map_insert_it_bucle`](casos/map/insert.md#f_map_insert_it_bucle) | `map` | `insert` | `it` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 508 | [`f_map_insert_it_llamada`](casos/map/insert.md#f_map_insert_it_llamada) | `map` | `insert` | `it` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 509 | [`f_map_insert_ref_recto`](casos/map/insert.md#f_map_insert_ref_recto) | `map` | `insert` | `ref` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 510 | [`f_map_insert_ref_guarda`](casos/map/insert.md#f_map_insert_ref_guarda) | `map` | `insert` | `ref` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 511 | [`f_map_insert_ref_bucle`](casos/map/insert.md#f_map_insert_ref_bucle) | `map` | `insert` | `ref` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 512 | [`f_map_insert_ref_llamada`](casos/map/insert.md#f_map_insert_ref_llamada) | `map` | `insert` | `ref` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 513 | [`f_map_insert_ptr_recto`](casos/map/insert.md#f_map_insert_ptr_recto) | `map` | `insert` | `ptr` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 514 | [`f_map_insert_ptr_guarda`](casos/map/insert.md#f_map_insert_ptr_guarda) | `map` | `insert` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 515 | [`f_map_insert_ptr_bucle`](casos/map/insert.md#f_map_insert_ptr_bucle) | `map` | `insert` | `ptr` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 516 | [`f_map_insert_ptr_llamada`](casos/map/insert.md#f_map_insert_ptr_llamada) | `map` | `insert` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 517 | [`f_map_emplace_it_recto`](casos/map/emplace.md#f_map_emplace_it_recto) | `map` | `emplace` | `it` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 518 | [`f_map_emplace_it_guarda`](casos/map/emplace.md#f_map_emplace_it_guarda) | `map` | `emplace` | `it` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 519 | [`f_map_emplace_it_bucle`](casos/map/emplace.md#f_map_emplace_it_bucle) | `map` | `emplace` | `it` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 520 | [`f_map_emplace_it_llamada`](casos/map/emplace.md#f_map_emplace_it_llamada) | `map` | `emplace` | `it` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 521 | [`f_map_emplace_ref_recto`](casos/map/emplace.md#f_map_emplace_ref_recto) | `map` | `emplace` | `ref` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 522 | [`f_map_emplace_ref_guarda`](casos/map/emplace.md#f_map_emplace_ref_guarda) | `map` | `emplace` | `ref` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 523 | [`f_map_emplace_ref_bucle`](casos/map/emplace.md#f_map_emplace_ref_bucle) | `map` | `emplace` | `ref` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 524 | [`f_map_emplace_ref_llamada`](casos/map/emplace.md#f_map_emplace_ref_llamada) | `map` | `emplace` | `ref` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 525 | [`f_map_emplace_ptr_recto`](casos/map/emplace.md#f_map_emplace_ptr_recto) | `map` | `emplace` | `ptr` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 526 | [`f_map_emplace_ptr_guarda`](casos/map/emplace.md#f_map_emplace_ptr_guarda) | `map` | `emplace` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 527 | [`f_map_emplace_ptr_bucle`](casos/map/emplace.md#f_map_emplace_ptr_bucle) | `map` | `emplace` | `ptr` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 528 | [`f_map_emplace_ptr_llamada`](casos/map/emplace.md#f_map_emplace_ptr_llamada) | `map` | `emplace` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 529 | [`f_map_subscript_it_recto`](casos/map/subscript.md#f_map_subscript_it_recto) | `map` | `subscript` | `it` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 530 | [`f_map_subscript_it_guarda`](casos/map/subscript.md#f_map_subscript_it_guarda) | `map` | `subscript` | `it` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 531 | [`f_map_subscript_it_bucle`](casos/map/subscript.md#f_map_subscript_it_bucle) | `map` | `subscript` | `it` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 532 | [`f_map_subscript_it_llamada`](casos/map/subscript.md#f_map_subscript_it_llamada) | `map` | `subscript` | `it` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 533 | [`f_map_subscript_ref_recto`](casos/map/subscript.md#f_map_subscript_ref_recto) | `map` | `subscript` | `ref` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 534 | [`f_map_subscript_ref_guarda`](casos/map/subscript.md#f_map_subscript_ref_guarda) | `map` | `subscript` | `ref` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 535 | [`f_map_subscript_ref_bucle`](casos/map/subscript.md#f_map_subscript_ref_bucle) | `map` | `subscript` | `ref` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 536 | [`f_map_subscript_ref_llamada`](casos/map/subscript.md#f_map_subscript_ref_llamada) | `map` | `subscript` | `ref` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 537 | [`f_map_subscript_ptr_recto`](casos/map/subscript.md#f_map_subscript_ptr_recto) | `map` | `subscript` | `ptr` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 538 | [`f_map_subscript_ptr_guarda`](casos/map/subscript.md#f_map_subscript_ptr_guarda) | `map` | `subscript` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 539 | [`f_map_subscript_ptr_bucle`](casos/map/subscript.md#f_map_subscript_ptr_bucle) | `map` | `subscript` | `ptr` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 540 | [`f_map_subscript_ptr_llamada`](casos/map/subscript.md#f_map_subscript_ptr_llamada) | `map` | `subscript` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 541 | [`f_map_erase_begin_it_recto`](casos/map/erase_begin.md#f_map_erase_begin_it_recto) | `map` | `erase_begin` | `it` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 542 | [`f_map_erase_begin_it_guarda`](casos/map/erase_begin.md#f_map_erase_begin_it_guarda) | `map` | `erase_begin` | `it` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 543 | [`f_map_erase_begin_it_bucle`](casos/map/erase_begin.md#f_map_erase_begin_it_bucle) | `map` | `erase_begin` | `it` | `bucle` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 544 | [`f_map_erase_begin_it_llamada`](casos/map/erase_begin.md#f_map_erase_begin_it_llamada) | `map` | `erase_begin` | `it` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 545 | [`f_map_erase_begin_ref_recto`](casos/map/erase_begin.md#f_map_erase_begin_ref_recto) | `map` | `erase_begin` | `ref` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 546 | [`f_map_erase_begin_ref_guarda`](casos/map/erase_begin.md#f_map_erase_begin_ref_guarda) | `map` | `erase_begin` | `ref` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 547 | [`f_map_erase_begin_ref_bucle`](casos/map/erase_begin.md#f_map_erase_begin_ref_bucle) | `map` | `erase_begin` | `ref` | `bucle` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 548 | [`f_map_erase_begin_ref_llamada`](casos/map/erase_begin.md#f_map_erase_begin_ref_llamada) | `map` | `erase_begin` | `ref` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 549 | [`f_map_erase_begin_ptr_recto`](casos/map/erase_begin.md#f_map_erase_begin_ptr_recto) | `map` | `erase_begin` | `ptr` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 550 | [`f_map_erase_begin_ptr_guarda`](casos/map/erase_begin.md#f_map_erase_begin_ptr_guarda) | `map` | `erase_begin` | `ptr` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 551 | [`f_map_erase_begin_ptr_bucle`](casos/map/erase_begin.md#f_map_erase_begin_ptr_bucle) | `map` | `erase_begin` | `ptr` | `bucle` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 552 | [`f_map_erase_begin_ptr_llamada`](casos/map/erase_begin.md#f_map_erase_begin_ptr_llamada) | `map` | `erase_begin` | `ptr` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 553 | [`f_map_clear_it_recto`](casos/map/clear.md#f_map_clear_it_recto) | `map` | `clear` | `it` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 554 | [`f_map_clear_it_guarda`](casos/map/clear.md#f_map_clear_it_guarda) | `map` | `clear` | `it` | `guarda` | 🔴 `UB` | ✅ detectado | 🛑 |
| 555 | [`f_map_clear_it_bucle`](casos/map/clear.md#f_map_clear_it_bucle) | `map` | `clear` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 556 | [`f_map_clear_it_llamada`](casos/map/clear.md#f_map_clear_it_llamada) | `map` | `clear` | `it` | `llamada` | 🔴 `UB` | ✅ detectado | 🛑 |
| 557 | [`f_map_clear_ref_recto`](casos/map/clear.md#f_map_clear_ref_recto) | `map` | `clear` | `ref` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 558 | [`f_map_clear_ref_guarda`](casos/map/clear.md#f_map_clear_ref_guarda) | `map` | `clear` | `ref` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 559 | [`f_map_clear_ref_bucle`](casos/map/clear.md#f_map_clear_ref_bucle) | `map` | `clear` | `ref` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 560 | [`f_map_clear_ref_llamada`](casos/map/clear.md#f_map_clear_ref_llamada) | `map` | `clear` | `ref` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 561 | [`f_map_clear_ptr_recto`](casos/map/clear.md#f_map_clear_ptr_recto) | `map` | `clear` | `ptr` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 562 | [`f_map_clear_ptr_guarda`](casos/map/clear.md#f_map_clear_ptr_guarda) | `map` | `clear` | `ptr` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 563 | [`f_map_clear_ptr_bucle`](casos/map/clear.md#f_map_clear_ptr_bucle) | `map` | `clear` | `ptr` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 564 | [`f_map_clear_ptr_llamada`](casos/map/clear.md#f_map_clear_ptr_llamada) | `map` | `clear` | `ptr` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 565 | [`f_mmap_insert_it_recto`](casos/mmap/insert.md#f_mmap_insert_it_recto) | `mmap` | `insert` | `it` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 566 | [`f_mmap_insert_it_guarda`](casos/mmap/insert.md#f_mmap_insert_it_guarda) | `mmap` | `insert` | `it` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 567 | [`f_mmap_insert_it_bucle`](casos/mmap/insert.md#f_mmap_insert_it_bucle) | `mmap` | `insert` | `it` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 568 | [`f_mmap_insert_it_llamada`](casos/mmap/insert.md#f_mmap_insert_it_llamada) | `mmap` | `insert` | `it` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 569 | [`f_mmap_insert_ref_recto`](casos/mmap/insert.md#f_mmap_insert_ref_recto) | `mmap` | `insert` | `ref` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 570 | [`f_mmap_insert_ref_guarda`](casos/mmap/insert.md#f_mmap_insert_ref_guarda) | `mmap` | `insert` | `ref` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 571 | [`f_mmap_insert_ref_bucle`](casos/mmap/insert.md#f_mmap_insert_ref_bucle) | `mmap` | `insert` | `ref` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 572 | [`f_mmap_insert_ref_llamada`](casos/mmap/insert.md#f_mmap_insert_ref_llamada) | `mmap` | `insert` | `ref` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 573 | [`f_mmap_insert_ptr_recto`](casos/mmap/insert.md#f_mmap_insert_ptr_recto) | `mmap` | `insert` | `ptr` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 574 | [`f_mmap_insert_ptr_guarda`](casos/mmap/insert.md#f_mmap_insert_ptr_guarda) | `mmap` | `insert` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 575 | [`f_mmap_insert_ptr_bucle`](casos/mmap/insert.md#f_mmap_insert_ptr_bucle) | `mmap` | `insert` | `ptr` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 576 | [`f_mmap_insert_ptr_llamada`](casos/mmap/insert.md#f_mmap_insert_ptr_llamada) | `mmap` | `insert` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 577 | [`f_mmap_erase_begin_it_recto`](casos/mmap/erase_begin.md#f_mmap_erase_begin_it_recto) | `mmap` | `erase_begin` | `it` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 578 | [`f_mmap_erase_begin_it_guarda`](casos/mmap/erase_begin.md#f_mmap_erase_begin_it_guarda) | `mmap` | `erase_begin` | `it` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 579 | [`f_mmap_erase_begin_it_bucle`](casos/mmap/erase_begin.md#f_mmap_erase_begin_it_bucle) | `mmap` | `erase_begin` | `it` | `bucle` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 580 | [`f_mmap_erase_begin_it_llamada`](casos/mmap/erase_begin.md#f_mmap_erase_begin_it_llamada) | `mmap` | `erase_begin` | `it` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 581 | [`f_mmap_erase_begin_ref_recto`](casos/mmap/erase_begin.md#f_mmap_erase_begin_ref_recto) | `mmap` | `erase_begin` | `ref` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 582 | [`f_mmap_erase_begin_ref_guarda`](casos/mmap/erase_begin.md#f_mmap_erase_begin_ref_guarda) | `mmap` | `erase_begin` | `ref` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 583 | [`f_mmap_erase_begin_ref_bucle`](casos/mmap/erase_begin.md#f_mmap_erase_begin_ref_bucle) | `mmap` | `erase_begin` | `ref` | `bucle` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 584 | [`f_mmap_erase_begin_ref_llamada`](casos/mmap/erase_begin.md#f_mmap_erase_begin_ref_llamada) | `mmap` | `erase_begin` | `ref` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 585 | [`f_mmap_erase_begin_ptr_recto`](casos/mmap/erase_begin.md#f_mmap_erase_begin_ptr_recto) | `mmap` | `erase_begin` | `ptr` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 586 | [`f_mmap_erase_begin_ptr_guarda`](casos/mmap/erase_begin.md#f_mmap_erase_begin_ptr_guarda) | `mmap` | `erase_begin` | `ptr` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 587 | [`f_mmap_erase_begin_ptr_bucle`](casos/mmap/erase_begin.md#f_mmap_erase_begin_ptr_bucle) | `mmap` | `erase_begin` | `ptr` | `bucle` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 588 | [`f_mmap_erase_begin_ptr_llamada`](casos/mmap/erase_begin.md#f_mmap_erase_begin_ptr_llamada) | `mmap` | `erase_begin` | `ptr` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 589 | [`f_mmap_clear_it_recto`](casos/mmap/clear.md#f_mmap_clear_it_recto) | `mmap` | `clear` | `it` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 590 | [`f_mmap_clear_it_guarda`](casos/mmap/clear.md#f_mmap_clear_it_guarda) | `mmap` | `clear` | `it` | `guarda` | 🔴 `UB` | ✅ detectado | 🛑 |
| 591 | [`f_mmap_clear_it_bucle`](casos/mmap/clear.md#f_mmap_clear_it_bucle) | `mmap` | `clear` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 592 | [`f_mmap_clear_it_llamada`](casos/mmap/clear.md#f_mmap_clear_it_llamada) | `mmap` | `clear` | `it` | `llamada` | 🔴 `UB` | ✅ detectado | 🛑 |
| 593 | [`f_mmap_clear_ref_recto`](casos/mmap/clear.md#f_mmap_clear_ref_recto) | `mmap` | `clear` | `ref` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 594 | [`f_mmap_clear_ref_guarda`](casos/mmap/clear.md#f_mmap_clear_ref_guarda) | `mmap` | `clear` | `ref` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 595 | [`f_mmap_clear_ref_bucle`](casos/mmap/clear.md#f_mmap_clear_ref_bucle) | `mmap` | `clear` | `ref` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 596 | [`f_mmap_clear_ref_llamada`](casos/mmap/clear.md#f_mmap_clear_ref_llamada) | `mmap` | `clear` | `ref` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 597 | [`f_mmap_clear_ptr_recto`](casos/mmap/clear.md#f_mmap_clear_ptr_recto) | `mmap` | `clear` | `ptr` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 598 | [`f_mmap_clear_ptr_guarda`](casos/mmap/clear.md#f_mmap_clear_ptr_guarda) | `mmap` | `clear` | `ptr` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 599 | [`f_mmap_clear_ptr_bucle`](casos/mmap/clear.md#f_mmap_clear_ptr_bucle) | `mmap` | `clear` | `ptr` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 600 | [`f_mmap_clear_ptr_llamada`](casos/mmap/clear.md#f_mmap_clear_ptr_llamada) | `mmap` | `clear` | `ptr` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 601 | [`f_uset_insert_it_recto`](casos/uset/insert.md#f_uset_insert_it_recto) | `uset` | `insert` | `it` | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 602 | [`f_uset_insert_it_recto_reserva`](casos/garantias.md#f_uset_insert_it_recto_reserva) | `uset` | `insert` | `it` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 603 | [`f_uset_insert_it_guarda`](casos/uset/insert.md#f_uset_insert_it_guarda) | `uset` | `insert` | `it` | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 604 | [`f_uset_insert_it_guarda_reserva`](casos/garantias.md#f_uset_insert_it_guarda_reserva) | `uset` | `insert` | `it` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 605 | [`f_uset_insert_it_bucle`](casos/uset/insert.md#f_uset_insert_it_bucle) | `uset` | `insert` | `it` | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 606 | [`f_uset_insert_it_bucle_reserva`](casos/garantias.md#f_uset_insert_it_bucle_reserva) | `uset` | `insert` | `it` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 607 | [`f_uset_insert_it_llamada`](casos/uset/insert.md#f_uset_insert_it_llamada) | `uset` | `insert` | `it` | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 608 | [`f_uset_insert_it_llamada_reserva`](casos/garantias.md#f_uset_insert_it_llamada_reserva) | `uset` | `insert` | `it` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 609 | [`f_uset_insert_ref_recto`](casos/uset/insert.md#f_uset_insert_ref_recto) | `uset` | `insert` | `ref` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 610 | [`f_uset_insert_ref_guarda`](casos/uset/insert.md#f_uset_insert_ref_guarda) | `uset` | `insert` | `ref` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 611 | [`f_uset_insert_ref_bucle`](casos/uset/insert.md#f_uset_insert_ref_bucle) | `uset` | `insert` | `ref` | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 612 | [`f_uset_insert_ref_bucle_reserva`](casos/garantias.md#f_uset_insert_ref_bucle_reserva) | `uset` | `insert` | `ref` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 613 | [`f_uset_insert_ref_llamada`](casos/uset/insert.md#f_uset_insert_ref_llamada) | `uset` | `insert` | `ref` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 614 | [`f_uset_insert_ptr_recto`](casos/uset/insert.md#f_uset_insert_ptr_recto) | `uset` | `insert` | `ptr` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 615 | [`f_uset_insert_ptr_guarda`](casos/uset/insert.md#f_uset_insert_ptr_guarda) | `uset` | `insert` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 616 | [`f_uset_insert_ptr_bucle`](casos/uset/insert.md#f_uset_insert_ptr_bucle) | `uset` | `insert` | `ptr` | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 617 | [`f_uset_insert_ptr_bucle_reserva`](casos/garantias.md#f_uset_insert_ptr_bucle_reserva) | `uset` | `insert` | `ptr` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 618 | [`f_uset_insert_ptr_llamada`](casos/uset/insert.md#f_uset_insert_ptr_llamada) | `uset` | `insert` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 619 | [`f_uset_erase_begin_it_recto`](casos/uset/erase_begin.md#f_uset_erase_begin_it_recto) | `uset` | `erase_begin` | `it` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 620 | [`f_uset_erase_begin_it_guarda`](casos/uset/erase_begin.md#f_uset_erase_begin_it_guarda) | `uset` | `erase_begin` | `it` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 621 | [`f_uset_erase_begin_it_bucle`](casos/uset/erase_begin.md#f_uset_erase_begin_it_bucle) | `uset` | `erase_begin` | `it` | `bucle` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 622 | [`f_uset_erase_begin_it_llamada`](casos/uset/erase_begin.md#f_uset_erase_begin_it_llamada) | `uset` | `erase_begin` | `it` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 623 | [`f_uset_erase_begin_ref_recto`](casos/uset/erase_begin.md#f_uset_erase_begin_ref_recto) | `uset` | `erase_begin` | `ref` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 624 | [`f_uset_erase_begin_ref_guarda`](casos/uset/erase_begin.md#f_uset_erase_begin_ref_guarda) | `uset` | `erase_begin` | `ref` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 625 | [`f_uset_erase_begin_ref_bucle`](casos/uset/erase_begin.md#f_uset_erase_begin_ref_bucle) | `uset` | `erase_begin` | `ref` | `bucle` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 626 | [`f_uset_erase_begin_ref_llamada`](casos/uset/erase_begin.md#f_uset_erase_begin_ref_llamada) | `uset` | `erase_begin` | `ref` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 627 | [`f_uset_erase_begin_ptr_recto`](casos/uset/erase_begin.md#f_uset_erase_begin_ptr_recto) | `uset` | `erase_begin` | `ptr` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 628 | [`f_uset_erase_begin_ptr_guarda`](casos/uset/erase_begin.md#f_uset_erase_begin_ptr_guarda) | `uset` | `erase_begin` | `ptr` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 629 | [`f_uset_erase_begin_ptr_bucle`](casos/uset/erase_begin.md#f_uset_erase_begin_ptr_bucle) | `uset` | `erase_begin` | `ptr` | `bucle` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 630 | [`f_uset_erase_begin_ptr_llamada`](casos/uset/erase_begin.md#f_uset_erase_begin_ptr_llamada) | `uset` | `erase_begin` | `ptr` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 631 | [`f_uset_clear_it_recto`](casos/uset/clear.md#f_uset_clear_it_recto) | `uset` | `clear` | `it` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 632 | [`f_uset_clear_it_guarda`](casos/uset/clear.md#f_uset_clear_it_guarda) | `uset` | `clear` | `it` | `guarda` | 🔴 `UB` | ✅ detectado | 🛑 |
| 633 | [`f_uset_clear_it_bucle`](casos/uset/clear.md#f_uset_clear_it_bucle) | `uset` | `clear` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 634 | [`f_uset_clear_it_llamada`](casos/uset/clear.md#f_uset_clear_it_llamada) | `uset` | `clear` | `it` | `llamada` | 🔴 `UB` | ✅ detectado | 🛑 |
| 635 | [`f_uset_clear_ref_recto`](casos/uset/clear.md#f_uset_clear_ref_recto) | `uset` | `clear` | `ref` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 636 | [`f_uset_clear_ref_guarda`](casos/uset/clear.md#f_uset_clear_ref_guarda) | `uset` | `clear` | `ref` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 637 | [`f_uset_clear_ref_bucle`](casos/uset/clear.md#f_uset_clear_ref_bucle) | `uset` | `clear` | `ref` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 638 | [`f_uset_clear_ref_llamada`](casos/uset/clear.md#f_uset_clear_ref_llamada) | `uset` | `clear` | `ref` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 639 | [`f_uset_clear_ptr_recto`](casos/uset/clear.md#f_uset_clear_ptr_recto) | `uset` | `clear` | `ptr` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 640 | [`f_uset_clear_ptr_guarda`](casos/uset/clear.md#f_uset_clear_ptr_guarda) | `uset` | `clear` | `ptr` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 641 | [`f_uset_clear_ptr_bucle`](casos/uset/clear.md#f_uset_clear_ptr_bucle) | `uset` | `clear` | `ptr` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 642 | [`f_uset_clear_ptr_llamada`](casos/uset/clear.md#f_uset_clear_ptr_llamada) | `uset` | `clear` | `ptr` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 643 | [`f_uset_rehash_it_recto`](casos/uset/rehash.md#f_uset_rehash_it_recto) | `uset` | `rehash` | `it` | `recto` | 🔴 `UB` | ❌ no detectado | — |
| 644 | [`f_uset_rehash_it_guarda`](casos/uset/rehash.md#f_uset_rehash_it_guarda) | `uset` | `rehash` | `it` | `guarda` | 🔴 `UB` | ❌ no detectado | — |
| 645 | [`f_uset_rehash_it_bucle`](casos/uset/rehash.md#f_uset_rehash_it_bucle) | `uset` | `rehash` | `it` | `bucle` | 🔴 `UB` | ❌ no detectado | — |
| 646 | [`f_uset_rehash_it_llamada`](casos/uset/rehash.md#f_uset_rehash_it_llamada) | `uset` | `rehash` | `it` | `llamada` | 🔴 `UB` | ❌ no detectado | — |
| 647 | [`f_uset_rehash_ref_recto`](casos/uset/rehash.md#f_uset_rehash_ref_recto) | `uset` | `rehash` | `ref` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 648 | [`f_uset_rehash_ref_guarda`](casos/uset/rehash.md#f_uset_rehash_ref_guarda) | `uset` | `rehash` | `ref` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 649 | [`f_uset_rehash_ref_bucle`](casos/uset/rehash.md#f_uset_rehash_ref_bucle) | `uset` | `rehash` | `ref` | `bucle` | 🔴 `UB` | ❌ no detectado | — |
| 650 | [`f_uset_rehash_ref_llamada`](casos/uset/rehash.md#f_uset_rehash_ref_llamada) | `uset` | `rehash` | `ref` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 651 | [`f_uset_rehash_ptr_recto`](casos/uset/rehash.md#f_uset_rehash_ptr_recto) | `uset` | `rehash` | `ptr` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 652 | [`f_uset_rehash_ptr_guarda`](casos/uset/rehash.md#f_uset_rehash_ptr_guarda) | `uset` | `rehash` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 653 | [`f_uset_rehash_ptr_bucle`](casos/uset/rehash.md#f_uset_rehash_ptr_bucle) | `uset` | `rehash` | `ptr` | `bucle` | 🔴 `UB` | ❌ no detectado | — |
| 654 | [`f_uset_rehash_ptr_llamada`](casos/uset/rehash.md#f_uset_rehash_ptr_llamada) | `uset` | `rehash` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 655 | [`f_uset_reserve_it_recto`](casos/uset/reserve.md#f_uset_reserve_it_recto) | `uset` | `reserve` | `it` | `recto` | 🔴 `UB` | ❌ no detectado | — |
| 656 | [`f_uset_reserve_it_guarda`](casos/uset/reserve.md#f_uset_reserve_it_guarda) | `uset` | `reserve` | `it` | `guarda` | 🔴 `UB` | ❌ no detectado | — |
| 657 | [`f_uset_reserve_it_bucle`](casos/uset/reserve.md#f_uset_reserve_it_bucle) | `uset` | `reserve` | `it` | `bucle` | 🔴 `UB` | ❌ no detectado | — |
| 658 | [`f_uset_reserve_it_llamada`](casos/uset/reserve.md#f_uset_reserve_it_llamada) | `uset` | `reserve` | `it` | `llamada` | 🔴 `UB` | ❌ no detectado | — |
| 659 | [`f_uset_reserve_ref_recto`](casos/uset/reserve.md#f_uset_reserve_ref_recto) | `uset` | `reserve` | `ref` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 660 | [`f_uset_reserve_ref_guarda`](casos/uset/reserve.md#f_uset_reserve_ref_guarda) | `uset` | `reserve` | `ref` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 661 | [`f_uset_reserve_ref_bucle`](casos/uset/reserve.md#f_uset_reserve_ref_bucle) | `uset` | `reserve` | `ref` | `bucle` | 🔴 `UB` | ❌ no detectado | — |
| 662 | [`f_uset_reserve_ref_llamada`](casos/uset/reserve.md#f_uset_reserve_ref_llamada) | `uset` | `reserve` | `ref` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 663 | [`f_uset_reserve_ptr_recto`](casos/uset/reserve.md#f_uset_reserve_ptr_recto) | `uset` | `reserve` | `ptr` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 664 | [`f_uset_reserve_ptr_guarda`](casos/uset/reserve.md#f_uset_reserve_ptr_guarda) | `uset` | `reserve` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 665 | [`f_uset_reserve_ptr_bucle`](casos/uset/reserve.md#f_uset_reserve_ptr_bucle) | `uset` | `reserve` | `ptr` | `bucle` | 🔴 `UB` | ❌ no detectado | — |
| 666 | [`f_uset_reserve_ptr_llamada`](casos/uset/reserve.md#f_uset_reserve_ptr_llamada) | `uset` | `reserve` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 667 | [`f_umap_insert_it_recto`](casos/umap/insert.md#f_umap_insert_it_recto) | `umap` | `insert` | `it` | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 668 | [`f_umap_insert_it_recto_reserva`](casos/garantias.md#f_umap_insert_it_recto_reserva) | `umap` | `insert` | `it` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 669 | [`f_umap_insert_it_guarda`](casos/umap/insert.md#f_umap_insert_it_guarda) | `umap` | `insert` | `it` | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 670 | [`f_umap_insert_it_guarda_reserva`](casos/garantias.md#f_umap_insert_it_guarda_reserva) | `umap` | `insert` | `it` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 671 | [`f_umap_insert_it_bucle`](casos/umap/insert.md#f_umap_insert_it_bucle) | `umap` | `insert` | `it` | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 672 | [`f_umap_insert_it_bucle_reserva`](casos/garantias.md#f_umap_insert_it_bucle_reserva) | `umap` | `insert` | `it` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 673 | [`f_umap_insert_it_llamada`](casos/umap/insert.md#f_umap_insert_it_llamada) | `umap` | `insert` | `it` | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 674 | [`f_umap_insert_it_llamada_reserva`](casos/garantias.md#f_umap_insert_it_llamada_reserva) | `umap` | `insert` | `it` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 675 | [`f_umap_insert_ref_recto`](casos/umap/insert.md#f_umap_insert_ref_recto) | `umap` | `insert` | `ref` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 676 | [`f_umap_insert_ref_guarda`](casos/umap/insert.md#f_umap_insert_ref_guarda) | `umap` | `insert` | `ref` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 677 | [`f_umap_insert_ref_bucle`](casos/umap/insert.md#f_umap_insert_ref_bucle) | `umap` | `insert` | `ref` | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 678 | [`f_umap_insert_ref_bucle_reserva`](casos/garantias.md#f_umap_insert_ref_bucle_reserva) | `umap` | `insert` | `ref` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 679 | [`f_umap_insert_ref_llamada`](casos/umap/insert.md#f_umap_insert_ref_llamada) | `umap` | `insert` | `ref` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 680 | [`f_umap_insert_ptr_recto`](casos/umap/insert.md#f_umap_insert_ptr_recto) | `umap` | `insert` | `ptr` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 681 | [`f_umap_insert_ptr_guarda`](casos/umap/insert.md#f_umap_insert_ptr_guarda) | `umap` | `insert` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 682 | [`f_umap_insert_ptr_bucle`](casos/umap/insert.md#f_umap_insert_ptr_bucle) | `umap` | `insert` | `ptr` | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | 🛑 |
| 683 | [`f_umap_insert_ptr_bucle_reserva`](casos/garantias.md#f_umap_insert_ptr_bucle_reserva) | `umap` | `insert` | `ptr` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 684 | [`f_umap_insert_ptr_llamada`](casos/umap/insert.md#f_umap_insert_ptr_llamada) | `umap` | `insert` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 685 | [`f_umap_subscript_it_recto`](casos/umap/subscript.md#f_umap_subscript_it_recto) | `umap` | `subscript` | `it` | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | — |
| 686 | [`f_umap_subscript_it_recto_reserva`](casos/garantias.md#f_umap_subscript_it_recto_reserva) | `umap` | `subscript` | `it` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 687 | [`f_umap_subscript_it_guarda`](casos/umap/subscript.md#f_umap_subscript_it_guarda) | `umap` | `subscript` | `it` | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | — |
| 688 | [`f_umap_subscript_it_guarda_reserva`](casos/garantias.md#f_umap_subscript_it_guarda_reserva) | `umap` | `subscript` | `it` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 689 | [`f_umap_subscript_it_bucle`](casos/umap/subscript.md#f_umap_subscript_it_bucle) | `umap` | `subscript` | `it` | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | — |
| 690 | [`f_umap_subscript_it_bucle_reserva`](casos/garantias.md#f_umap_subscript_it_bucle_reserva) | `umap` | `subscript` | `it` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 691 | [`f_umap_subscript_it_llamada`](casos/umap/subscript.md#f_umap_subscript_it_llamada) | `umap` | `subscript` | `it` | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | — |
| 692 | [`f_umap_subscript_it_llamada_reserva`](casos/garantias.md#f_umap_subscript_it_llamada_reserva) | `umap` | `subscript` | `it` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 693 | [`f_umap_subscript_ref_recto`](casos/umap/subscript.md#f_umap_subscript_ref_recto) | `umap` | `subscript` | `ref` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 694 | [`f_umap_subscript_ref_guarda`](casos/umap/subscript.md#f_umap_subscript_ref_guarda) | `umap` | `subscript` | `ref` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 695 | [`f_umap_subscript_ref_bucle`](casos/umap/subscript.md#f_umap_subscript_ref_bucle) | `umap` | `subscript` | `ref` | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | — |
| 696 | [`f_umap_subscript_ref_bucle_reserva`](casos/garantias.md#f_umap_subscript_ref_bucle_reserva) | `umap` | `subscript` | `ref` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 697 | [`f_umap_subscript_ref_llamada`](casos/umap/subscript.md#f_umap_subscript_ref_llamada) | `umap` | `subscript` | `ref` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 698 | [`f_umap_subscript_ptr_recto`](casos/umap/subscript.md#f_umap_subscript_ptr_recto) | `umap` | `subscript` | `ptr` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 699 | [`f_umap_subscript_ptr_guarda`](casos/umap/subscript.md#f_umap_subscript_ptr_guarda) | `umap` | `subscript` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 700 | [`f_umap_subscript_ptr_bucle`](casos/umap/subscript.md#f_umap_subscript_ptr_bucle) | `umap` | `subscript` | `ptr` | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | — |
| 701 | [`f_umap_subscript_ptr_bucle_reserva`](casos/garantias.md#f_umap_subscript_ptr_bucle_reserva) | `umap` | `subscript` | `ptr` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 702 | [`f_umap_subscript_ptr_llamada`](casos/umap/subscript.md#f_umap_subscript_ptr_llamada) | `umap` | `subscript` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 703 | [`f_umap_erase_begin_it_recto`](casos/umap/erase_begin.md#f_umap_erase_begin_it_recto) | `umap` | `erase_begin` | `it` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 704 | [`f_umap_erase_begin_it_guarda`](casos/umap/erase_begin.md#f_umap_erase_begin_it_guarda) | `umap` | `erase_begin` | `it` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 705 | [`f_umap_erase_begin_it_bucle`](casos/umap/erase_begin.md#f_umap_erase_begin_it_bucle) | `umap` | `erase_begin` | `it` | `bucle` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 706 | [`f_umap_erase_begin_it_llamada`](casos/umap/erase_begin.md#f_umap_erase_begin_it_llamada) | `umap` | `erase_begin` | `it` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 707 | [`f_umap_erase_begin_ref_recto`](casos/umap/erase_begin.md#f_umap_erase_begin_ref_recto) | `umap` | `erase_begin` | `ref` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 708 | [`f_umap_erase_begin_ref_guarda`](casos/umap/erase_begin.md#f_umap_erase_begin_ref_guarda) | `umap` | `erase_begin` | `ref` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 709 | [`f_umap_erase_begin_ref_bucle`](casos/umap/erase_begin.md#f_umap_erase_begin_ref_bucle) | `umap` | `erase_begin` | `ref` | `bucle` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 710 | [`f_umap_erase_begin_ref_llamada`](casos/umap/erase_begin.md#f_umap_erase_begin_ref_llamada) | `umap` | `erase_begin` | `ref` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 711 | [`f_umap_erase_begin_ptr_recto`](casos/umap/erase_begin.md#f_umap_erase_begin_ptr_recto) | `umap` | `erase_begin` | `ptr` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 712 | [`f_umap_erase_begin_ptr_guarda`](casos/umap/erase_begin.md#f_umap_erase_begin_ptr_guarda) | `umap` | `erase_begin` | `ptr` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 713 | [`f_umap_erase_begin_ptr_bucle`](casos/umap/erase_begin.md#f_umap_erase_begin_ptr_bucle) | `umap` | `erase_begin` | `ptr` | `bucle` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 714 | [`f_umap_erase_begin_ptr_llamada`](casos/umap/erase_begin.md#f_umap_erase_begin_ptr_llamada) | `umap` | `erase_begin` | `ptr` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 715 | [`f_umap_clear_it_recto`](casos/umap/clear.md#f_umap_clear_it_recto) | `umap` | `clear` | `it` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 716 | [`f_umap_clear_it_guarda`](casos/umap/clear.md#f_umap_clear_it_guarda) | `umap` | `clear` | `it` | `guarda` | 🔴 `UB` | ✅ detectado | 🛑 |
| 717 | [`f_umap_clear_it_bucle`](casos/umap/clear.md#f_umap_clear_it_bucle) | `umap` | `clear` | `it` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 718 | [`f_umap_clear_it_llamada`](casos/umap/clear.md#f_umap_clear_it_llamada) | `umap` | `clear` | `it` | `llamada` | 🔴 `UB` | ✅ detectado | 🛑 |
| 719 | [`f_umap_clear_ref_recto`](casos/umap/clear.md#f_umap_clear_ref_recto) | `umap` | `clear` | `ref` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 720 | [`f_umap_clear_ref_guarda`](casos/umap/clear.md#f_umap_clear_ref_guarda) | `umap` | `clear` | `ref` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 721 | [`f_umap_clear_ref_bucle`](casos/umap/clear.md#f_umap_clear_ref_bucle) | `umap` | `clear` | `ref` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 722 | [`f_umap_clear_ref_llamada`](casos/umap/clear.md#f_umap_clear_ref_llamada) | `umap` | `clear` | `ref` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 723 | [`f_umap_clear_ptr_recto`](casos/umap/clear.md#f_umap_clear_ptr_recto) | `umap` | `clear` | `ptr` | `recto` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 724 | [`f_umap_clear_ptr_guarda`](casos/umap/clear.md#f_umap_clear_ptr_guarda) | `umap` | `clear` | `ptr` | `guarda` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 725 | [`f_umap_clear_ptr_bucle`](casos/umap/clear.md#f_umap_clear_ptr_bucle) | `umap` | `clear` | `ptr` | `bucle` | 🔴 `UB` | ✅ detectado | 🛑 |
| 726 | [`f_umap_clear_ptr_llamada`](casos/umap/clear.md#f_umap_clear_ptr_llamada) | `umap` | `clear` | `ptr` | `llamada` | 🔴 `UB` | ❌ no detectado | 🛑 |
| 727 | [`f_umap_rehash_it_recto`](casos/umap/rehash.md#f_umap_rehash_it_recto) | `umap` | `rehash` | `it` | `recto` | 🔴 `UB` | ❌ no detectado | — |
| 728 | [`f_umap_rehash_it_guarda`](casos/umap/rehash.md#f_umap_rehash_it_guarda) | `umap` | `rehash` | `it` | `guarda` | 🔴 `UB` | ❌ no detectado | — |
| 729 | [`f_umap_rehash_it_bucle`](casos/umap/rehash.md#f_umap_rehash_it_bucle) | `umap` | `rehash` | `it` | `bucle` | 🔴 `UB` | ❌ no detectado | — |
| 730 | [`f_umap_rehash_it_llamada`](casos/umap/rehash.md#f_umap_rehash_it_llamada) | `umap` | `rehash` | `it` | `llamada` | 🔴 `UB` | ❌ no detectado | — |
| 731 | [`f_umap_rehash_ref_recto`](casos/umap/rehash.md#f_umap_rehash_ref_recto) | `umap` | `rehash` | `ref` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 732 | [`f_umap_rehash_ref_guarda`](casos/umap/rehash.md#f_umap_rehash_ref_guarda) | `umap` | `rehash` | `ref` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 733 | [`f_umap_rehash_ref_bucle`](casos/umap/rehash.md#f_umap_rehash_ref_bucle) | `umap` | `rehash` | `ref` | `bucle` | 🔴 `UB` | ❌ no detectado | — |
| 734 | [`f_umap_rehash_ref_llamada`](casos/umap/rehash.md#f_umap_rehash_ref_llamada) | `umap` | `rehash` | `ref` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 735 | [`f_umap_rehash_ptr_recto`](casos/umap/rehash.md#f_umap_rehash_ptr_recto) | `umap` | `rehash` | `ptr` | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 736 | [`f_umap_rehash_ptr_guarda`](casos/umap/rehash.md#f_umap_rehash_ptr_guarda) | `umap` | `rehash` | `ptr` | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 737 | [`f_umap_rehash_ptr_bucle`](casos/umap/rehash.md#f_umap_rehash_ptr_bucle) | `umap` | `rehash` | `ptr` | `bucle` | 🔴 `UB` | ❌ no detectado | — |
| 738 | [`f_umap_rehash_ptr_llamada`](casos/umap/rehash.md#f_umap_rehash_ptr_llamada) | `umap` | `rehash` | `ptr` | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 739 | [`f_vector_erase_ret_it_bucle`](casos/garantias.md#f_vector_erase_ret_it_bucle) | `vector` | `erase_ret` | `it` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 740 | [`f_deque_erase_ret_it_bucle`](casos/garantias.md#f_deque_erase_ret_it_bucle) | `deque` | `erase_ret` | `it` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 741 | [`f_list_erase_ret_it_bucle`](casos/garantias.md#f_list_erase_ret_it_bucle) | `list` | `erase_ret` | `it` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 742 | [`f_set_erase_ret_it_bucle`](casos/garantias.md#f_set_erase_ret_it_bucle) | `set` | `erase_ret` | `it` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 743 | [`f_mset_erase_ret_it_bucle`](casos/garantias.md#f_mset_erase_ret_it_bucle) | `mset` | `erase_ret` | `it` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 744 | [`f_map_erase_ret_it_bucle`](casos/garantias.md#f_map_erase_ret_it_bucle) | `map` | `erase_ret` | `it` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 745 | [`f_mmap_erase_ret_it_bucle`](casos/garantias.md#f_mmap_erase_ret_it_bucle) | `mmap` | `erase_ret` | `it` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 746 | [`f_uset_erase_ret_it_bucle`](casos/garantias.md#f_uset_erase_ret_it_bucle) | `uset` | `erase_ret` | `it` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 747 | [`f_umap_erase_ret_it_bucle`](casos/garantias.md#f_umap_erase_ret_it_bucle) | `umap` | `erase_ret` | `it` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 748 | [`f_vector_insert_ret_it_bucle`](casos/garantias.md#f_vector_insert_ret_it_bucle) | `vector` | `insert_ret` | `it` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 749 | [`f_deque_insert_ret_it_bucle`](casos/garantias.md#f_deque_insert_ret_it_bucle) | `deque` | `insert_ret` | `it` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
| 750 | [`f_list_insert_ret_it_bucle`](casos/garantias.md#f_list_insert_ret_it_bucle) | `list` | `insert_ret` | `it` | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | — |
