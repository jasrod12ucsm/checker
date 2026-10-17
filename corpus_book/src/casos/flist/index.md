
# `std::forward_list`

48 casos (4 operaciones × 3 handles × 4 formas).
`UB`: 24 · detectados estáticamente: 5 (20.8%).

Las columnas *Iterador* y *Ref/Ptr* indican la etiqueta en forma `recto`; en
forma `bucle` puede pasar a `UB` por el iterador de control.

| Operación | Mutación | Iterador | Ref/Ptr | UB | Detectados (estático) | Detectados (dinámico) |
|---|---|---|---|---:|---:|---:|
| [`push_front`](push_front.md) | `c.push_front(1);` | 🟢 `SAFE` | 🟢 `SAFE` | 0 | 0 | 0 |
| [`insert_after`](insert_after.md) | `c.insert_after(c.before_begin(),1);` | 🟢 `SAFE` | 🟢 `SAFE` | 0 | 0 | 0 |
| [`erase_after`](erase_after.md) | `c.erase_after(c.before_begin());` | 🔴 `UB` | 🔴 `UB` | 12 | 1 | 12 |
| [`clear`](clear.md) | `c.clear();` | 🔴 `UB` | 🔴 `UB` | 12 | 4 | 12 |
