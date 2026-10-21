
# `std::set`

49 casos (4 operaciones × 3 handles × 4 formas, más 1 de buen uso con garantía).
`UB`: 24 · detectados estáticamente: 5 (20.8%).

Las columnas *Iterador* y *Ref/Ptr* indican la etiqueta en forma `recto`; en
forma `bucle` puede pasar a `UB` por el iterador de control.

| Operación | Mutación | Iterador | Ref/Ptr | UB | Detectados (estático) | Detectados (dinámico) |
|---|---|---|---|---:|---:|---:|
| [`insert`](insert.md) | `c.insert(99);` | 🟢 `SAFE` | 🟢 `SAFE` | 0 | 0 | 0 |
| [`emplace`](emplace.md) | `c.emplace(98);` | 🟢 `SAFE` | 🟢 `SAFE` | 0 | 0 | 0 |
| [`erase_begin`](erase_begin.md) | `c.erase(c.begin());` | 🔴 `UB` | 🔴 `UB` | 12 | 0 | 12 |
| [`clear`](clear.md) | `c.clear();` | 🔴 `UB` | 🔴 `UB` | 12 | 5 | 12 |
