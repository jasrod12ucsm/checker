
# `std::unordered_map`

60 casos (5 operaciones × 3 handles × 4 formas).
`UB`: 32 · detectados estáticamente: 8 (25.0%).

Las columnas *Iterador* y *Ref/Ptr* indican la etiqueta en forma `recto`; en
forma `bucle` puede pasar a `UB` por el iterador de control.

| Operación | Mutación | Iterador | Ref/Ptr | UB | Detectados (estático) | Detectados (dinámico) |
|---|---|---|---|---:|---:|---:|
| [`insert`](insert.md) | `c.insert({99,1});` | 🟡 `POLICY` | 🟢 `SAFE` | 1 | 0 | 0 |
| [`subscript`](subscript.md) | `c[97]=1;` | 🟡 `POLICY` | 🟢 `SAFE` | 1 | 0 | 0 |
| [`erase_begin`](erase_begin.md) | `c.erase(c.begin());` | 🔴 `UB` | 🔴 `UB` | 12 | 4 | 12 |
| [`clear`](clear.md) | `c.clear();` | 🔴 `UB` | 🔴 `UB` | 12 | 4 | 12 |
| [`rehash`](rehash.md) | `c.rehash(1024);` | 🔴 `UB` | 🟢 `SAFE` | 6 | 0 | 0 |
