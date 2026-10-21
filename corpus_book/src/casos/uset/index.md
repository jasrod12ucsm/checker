
# `std::unordered_set`

67 casos (5 operaciones × 3 handles × 4 formas, más 7 de buen uso con garantía).
`UB`: 36 · detectados estáticamente: 5 (13.9%).

Las columnas *Iterador* y *Ref/Ptr* indican la etiqueta en forma `recto`; en
forma `bucle` puede pasar a `UB` por el iterador de control.

| Operación | Mutación | Iterador | Ref/Ptr | UB | Detectados (estático) | Detectados (dinámico) |
|---|---|---|---|---:|---:|---:|
| [`insert`](insert.md) | `c.insert(99);` | 🟡 `POLICY` | 🟢 `SAFE` | 0 | 0 | 0 |
| [`erase_begin`](erase_begin.md) | `c.erase(c.begin());` | 🔴 `UB` | 🔴 `UB` | 12 | 0 | 12 |
| [`clear`](clear.md) | `c.clear();` | 🔴 `UB` | 🔴 `UB` | 12 | 5 | 12 |
| [`rehash`](rehash.md) | `c.rehash(1024);` | 🔴 `UB` | 🟢 `SAFE` | 6 | 0 | 0 |
| [`reserve`](reserve.md) | `c.reserve(1024);` | 🔴 `UB` | 🟢 `SAFE` | 6 | 0 | 0 |
