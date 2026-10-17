
# `std::vector`

132 casos (11 operaciones × 3 handles × 4 formas).
`UB`: 66 · detectados estáticamente: 16 (24.2%).

Las columnas *Iterador* y *Ref/Ptr* indican la etiqueta en forma `recto`; en
forma `bucle` puede pasar a `UB` por el iterador de control.

| Operación | Mutación | Iterador | Ref/Ptr | UB | Detectados (estático) | Detectados (dinámico) |
|---|---|---|---|---:|---:|---:|
| [`push_back`](push_back.md) | `c.push_back(1);` | 🟡 `POLICY` | 🟡 `POLICY` | 3 | 0 | 3 |
| [`emplace_back`](emplace_back.md) | `c.emplace_back(1);` | 🟡 `POLICY` | 🟡 `POLICY` | 3 | 0 | 3 |
| [`insert_begin`](insert_begin.md) | `c.insert(c.begin(),1);` | 🔴 `UB` | 🔴 `UB` | 12 | 4 | 6 |
| [`insert_end`](insert_end.md) | `c.insert(c.end(),1);` | 🟡 `POLICY` | 🟡 `POLICY` | 3 | 0 | 3 |
| [`erase_begin`](erase_begin.md) | `c.erase(c.begin());` | 🔴 `UB` | 🔴 `UB` | 12 | 4 | 6 |
| [`clear`](clear.md) | `c.clear();` | 🔴 `UB` | 🔴 `UB` | 12 | 4 | 6 |
| [`resize_grow`](resize_grow.md) | `c.resize(c.size()+100);` | 🟡 `POLICY` | 🟡 `POLICY` | 3 | 0 | 3 |
| [`reserve`](reserve.md) | `c.reserve(c.size()+100);` | 🟡 `POLICY` | 🟡 `POLICY` | 3 | 0 | 3 |
| [`shrink_to_fit`](shrink_to_fit.md) | `c.shrink_to_fit();` | 🟡 `POLICY` | 🟡 `POLICY` | 0 | 0 | 0 |
| [`assign`](assign.md) | `c.assign(3,7);` | 🔴 `UB` | 🔴 `UB` | 12 | 4 | 6 |
| [`pop_back`](pop_back.md) | `c.pop_back();` | 🟡 `POLICY` | 🟡 `POLICY` | 3 | 0 | 3 |
