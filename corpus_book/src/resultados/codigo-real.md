
# Código real

Generado desde `test/codigo_real/` (`bench/codigo_real.py` y `bench/inyeccion.py`).
`PolicyMode=Possibly`, `-analyzer-inlining-mode=all` (D-22).
Sólo se guardan los avisos de `ucsm.ContainerInvalidation`.

| Proyecto | *Commit* | Unidades | Sin terminar | Confirmados | Posibles | Segundos (suma) |
|---|---|---:|---:|---:|---:|---:|
| ninja | `2daa09b` | 29 | 1 | 0 | 1 | 129.6 |
| leveldb | `99b3c03` | 39 | 0 | 0 | 0 | 72.0 |
| yaml-cpp | `f732014` | 31 | 0 | 0 | 0 | 82.3 |
| rocksdb | `3c27a3d` | 682 | 0 | 0 | 0 | 9451.4 |

## Avisos y unidades que no terminaron

Cada aviso se revisó a mano; la revisión está en
[7.7 Estado actual](../construccion/7-7-estado.md).

- **ninja** `src/missing_deps.cc:190` (posible): Uso de un iterador posiblemente invalidado: 'std::unordered_map::insert' (línea 180) si supera el factor de carga rehace las cubetas; nada garantiza espacio: use reserve(size() + n) antes, o vuelva a obtenerlo
- **ninja** `src/browse.cc`: no terminó. `/work/build/real/ninja/src/browse.cc:23:10: fatal error: 'build/browse_py.h' file not found`

## Defectos sembrados

| Id | Proyecto | Archivo | Mecanismo | Espera | Obtiene | |
|---|---|---|---|---|---|---|
| S1 | ninja | `src/build.cc` | map::erase libera el nodo y luego se lee e->second (M5) | confirmado | confirmado | ✔ |
| S2 | ninja | `src/build.cc` | map::erase y lectura posterior por el iterador (M5) | confirmado | confirmado | ✔ |
| S3 | ninja | `src/missing_deps.cc` | unordered_map::clear y uso de un iterador obtenido con insert(...).first (M5) | confirmado | confirmado | ✔ |
| S4 | ninja | `src/graph.cc` | referencia al frente de un deque y pop_front (M5) | confirmado | confirmado | ✔ |
| S5 | ninja | `src/build_log.cc` | unordered_map::erase dentro del recorrido y ++i (M5) | confirmado | confirmado | ✔ |
| S6 | yaml-cpp | `src/node_data.cpp` | list::erase y ++it sobre el borrado (M5) | confirmado | confirmado | ✔ |
| S7 | leveldb | `db/db_impl.cc` | puntero a un elemento de vector y push_back sin reserve (M1) | posible | posible | ✔ |
| S8 | ninja | `src/graph.cc` | puntero a back() de un vector y pop_back (M3) | confirmado | confirmado | ✔ |
| B1 | leveldb | `db/db_impl.cc` | la misma S7 con reserve(size() + 1) antes: garantía | nada | nada | ✔ |
| B2 | ninja | `src/build_log.cc` | i = erase(i): el iterador devuelto es válido | nada | nada | ✔ |
