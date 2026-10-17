
# `std::list`

108 casos (9 operaciones × 3 handles × 4 formas).
`UB`: 36 · detectados estáticamente: 12 (33.3%).

Las columnas *Iterador* y *Ref/Ptr* indican la etiqueta en forma `recto`; en
forma `bucle` puede pasar a `UB` por el iterador de control.

| Operación | Mutación | Iterador | Ref/Ptr | UB | Detectados (estático) | Detectados (dinámico) |
|---|---|---|---|---:|---:|---:|
| [`push_back`](push_back.md) | `c.push_back(1);` | 🟢 `SAFE` | 🟢 `SAFE` | 0 | 0 | 0 |
| [`push_front`](push_front.md) | `c.push_front(1);` | 🟢 `SAFE` | 🟢 `SAFE` | 0 | 0 | 0 |
| [`insert`](insert.md) | `c.insert(c.begin(),1);` | 🟢 `SAFE` | 🟢 `SAFE` | 0 | 0 | 0 |
| [`erase_begin`](erase_begin.md) | `c.erase(c.begin());` | 🔴 `UB` | 🔴 `UB` | 12 | 4 | 12 |
| [`clear`](clear.md) | `c.clear();` | 🔴 `UB` | 🔴 `UB` | 12 | 4 | 12 |
| [`resize_grow`](resize_grow.md) | `c.resize(c.size()+100);` | 🟢 `SAFE` | 🟢 `SAFE` | 0 | 0 | 0 |
| [`pop_front`](pop_front.md) | `c.pop_front();` | 🔴 `UB` | 🔴 `UB` | 12 | 4 | 12 |
| [`reverse`](reverse.md) | `c.reverse();` | 🟢 `SAFE` | 🟢 `SAFE` | 0 | 0 | 0 |
| [`sort`](sort.md) | `c.sort();` | 🟢 `SAFE` | 🟢 `SAFE` | 0 | 0 | 0 |
