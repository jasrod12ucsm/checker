
# Matriz normativa

Benchmark preliminar de 114 casos (`test/matrix.cpp`): una celda por
contenedor × operación × dominio, todas en forma `guarda`.

## Totales

| Clasificación | Casos |
|---|---:|
| FALSO NEGATIVO | 40 |
| correcto | 34 |
| detectado | 15 |
| silencio (optimista) | 25 |

Exhaustividad global sobre `UB`: **15/55 = 27.3%**.

## Por contenedor y dominio

| Contenedor | Dominio | UB | Detectados | Huecos | SAFE | FP | POLICY |
|---|---|---:|---:|---:|---:|---:|---:|
| [`std::vector`](../matriz/vector.md) | iterador | 4 | 2 | 2 | 0 | 0 | 7 |
| [`std::vector`](../matriz/vector.md) | referencia | 4 | 0 | 4 | 0 | 0 | 7 |
| [`std::deque`](../matriz/deque.md) | iterador | 8 | 6 | 2 | 0 | 0 | 0 |
| [`std::deque`](../matriz/deque.md) | referencia | 4 | 0 | 4 | 4 | 0 | 0 |
| [`std::list`](../matriz/list.md) | iterador | 3 | 1 | 2 | 5 | 0 | 0 |
| [`std::list`](../matriz/list.md) | referencia | 3 | 0 | 3 | 5 | 0 | 0 |
| [`std::forward_list`](../matriz/flist.md) | iterador | 2 | 1 | 1 | 2 | 0 | 0 |
| [`std::forward_list`](../matriz/flist.md) | referencia | 2 | 0 | 2 | 2 | 0 | 0 |
| [`std::set`](../matriz/set.md) | iterador | 2 | 1 | 1 | 2 | 0 | 0 |
| [`std::set`](../matriz/set.md) | referencia | 2 | 0 | 2 | 2 | 0 | 0 |
| [`std::map`](../matriz/map.md) | iterador | 2 | 1 | 1 | 3 | 0 | 0 |
| [`std::map`](../matriz/map.md) | referencia | 2 | 0 | 2 | 3 | 0 | 0 |
| [`std::unordered_set`](../matriz/uset.md) | iterador | 4 | 1 | 3 | 0 | 0 | 1 |
| [`std::unordered_set`](../matriz/uset.md) | referencia | 2 | 0 | 2 | 3 | 0 | 0 |
| [`std::unordered_map`](../matriz/umap.md) | iterador | 3 | 1 | 2 | 0 | 0 | 2 |
| [`std::unordered_map`](../matriz/umap.md) | referencia | 2 | 0 | 2 | 3 | 0 | 0 |
| [`std::string`](../matriz/string.md) | iterador | 3 | 1 | 2 | 0 | 0 | 4 |
| [`std::string`](../matriz/string.md) | referencia | 3 | 0 | 3 | 0 | 0 | 4 |
