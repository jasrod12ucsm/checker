
# `std::deque`

98 casos (8 operaciones × 3 handles × 4 formas, más 2 de buen uso con garantía).
`UB`: 72 · detectados estáticamente: 30 (41.7%).

Las columnas *Iterador* y *Ref/Ptr* indican la etiqueta en forma `recto`; en
forma `bucle` puede pasar a `UB` por el iterador de control.

| Operación | Mutación | Iterador | Ref/Ptr | UB | Detectados (estático) | Detectados (dinámico) |
|---|---|---|---|---:|---:|---:|
| [`push_back`](push_back.md) | `c.push_back(1);` | 🔴 `UB` | 🟢 `SAFE` | 6 | 5 | 6 |
| [`push_front`](push_front.md) | `c.push_front(1);` | 🔴 `UB` | 🟢 `SAFE` | 6 | 5 | 6 |
| [`emplace_back`](emplace_back.md) | `c.emplace_back(1);` | 🔴 `UB` | 🟢 `SAFE` | 6 | 5 | 6 |
| [`insert_middle`](insert_middle.md) | `c.insert(c.begin()+1,1);` | 🔴 `UB` | 🔴 `UB` | 12 | 5 | 6 |
| [`erase_begin`](erase_begin.md) | `c.erase(c.begin());` | 🔴 `UB` | 🔴 `UB` | 12 | 5 | 6 |
| [`clear`](clear.md) | `c.clear();` | 🔴 `UB` | 🔴 `UB` | 12 | 5 | 6 |
| [`resize_grow`](resize_grow.md) | `c.resize(c.size()+100);` | 🔴 `UB` | 🟢 `SAFE` | 6 | 0 | 6 |
| [`pop_front`](pop_front.md) | `c.pop_front();` | 🔴 `UB` | 🔴 `UB` | 12 | 0 | 6 |
