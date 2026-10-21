
# `std::list`

110 casos (9 operaciones × 3 handles × 4 formas, más 2 de buen uso con garantía).
`UB`: 36 · detectados estáticamente: 5 (13.9%).

Las columnas *Iterador* y *Ref/Ptr* indican la etiqueta en forma `recto`; en
forma `bucle` puede pasar a `UB` por el iterador de control.

| Operación | Mutación | Iterador | Ref/Ptr | UB | Detectados (estático) | Detectados (dinámico) |
|---|---|---|---|---:|---:|---:|
| [`push_back`](push_back.md) | `c.push_back(1);` | 🟢 `SAFE` | 🟢 `SAFE` | 0 | 0 | 0 |
| [`push_front`](push_front.md) | `c.push_front(1);` | 🟢 `SAFE` | 🟢 `SAFE` | 0 | 0 | 0 |
| [`insert`](insert.md) | `c.insert(c.begin(),1);` | 🟢 `SAFE` | 🟢 `SAFE` | 0 | 0 | 0 |
| [`erase_begin`](erase_begin.md) | `c.erase(c.begin());` | 🔴 `UB` | 🔴 `UB` | 12 | 0 | 12 |
| [`clear`](clear.md) | `c.clear();` | 🔴 `UB` | 🔴 `UB` | 12 | 5 | 12 |
| [`resize_grow`](resize_grow.md) | `c.resize(c.size()+100);` | 🟢 `SAFE` | 🟢 `SAFE` | 0 | 0 | 0 |
| [`pop_front`](pop_front.md) | `c.pop_front();` | 🔴 `UB` | 🔴 `UB` | 12 | 0 | 12 |
| [`reverse`](reverse.md) | `c.reverse();` | 🟢 `SAFE` | 🟢 `SAFE` | 0 | 0 | 0 |
| [`sort`](sort.md) | `c.sort();` | 🟢 `SAFE` | 🟢 `SAFE` | 0 | 0 | 0 |
