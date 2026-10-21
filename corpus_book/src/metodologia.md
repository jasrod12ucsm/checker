
# Metodología

## Dimensiones

Cada caso es una tupla `(contenedor, operación, sostiene, forma, garantía)`:

| Dimensión | Valores |
|---|---|
| Contenedor | `std::vector`, `std::deque`, `std::list`, `std::forward_list`, `std::set`, `std::multiset`, `std::map`, `std::multimap`, `std::unordered_set`, `std::unordered_map` |
| Operación mutadora | 57 pares contenedor–operación |
| Sostiene (handle retenido) | `it` iterador, `ref` referencia, `ptr` puntero |
| Forma sintáctica | `recto`, `guarda`, `bucle`, `llamada` |
| Garantía (D-20) | `ninguna`; `reserva`: `reserve(size() + k)` antes; `devuelto`: el handle que devuelve la mutación |

Total: 57 pares × 3 handles × 4 formas = **684 casos** sin garantía,
más **66** casos de buen uso con garantía = **750 casos**.

### Formas sintácticas

- **`recto`**: handle obtenido, mutación directa y uso, sin comparación contra `end()`.
- **`guarda`**: igual que `recto`, pero con `if (it == c.end()) return;` antes de mutar.
- **`bucle`**: mutación dentro de un `for` acotado a tres rondas; también participa el iterador de control.
- **`llamada`**: la mutación ocurre dentro de una función auxiliar `mutar_*` (cruza una llamada).

La etiqueta depende del contenedor, la operación y el handle; la forma solo
cambia si el analizador *ve* el defecto. Excepción: en `bucle` el iterador de
control también se usa tras la mutación, de modo que si la operación invalida
iteradores el caso es `UB` aunque la referencia retenida siga siendo válida.

## Etiquetas normativas

- 🔴 **`UB`**: según las reglas de invalidación de C++17, el uso posterior es
  comportamiento indefinido.
- 🟢 **`SAFE`**: el handle sigue siendo válido tras la mutación.
- 🟡 **`POLICY`**: depende del estado (capacidad de un `vector`, factor de carga
  de un contenedor `unordered`). Se ejecuta dinámicamente en dos escenarios:
  `force` (fuerza la invalidación) y `preserve` (la evita).

## Benchmark estático

```bash
python3 bench/gen_corpus.py
python3 bench/experimento.py      # dentro de la imagen checker:llvm21
python3 bench/pruebas_evaluacion.py
```

Una invocación de `clang++ --analyze -std=c++17` **por caso y por condición**
(`-analyze-function=<firma>`), con salida SARIF. La condición de referencia usa
los checkers

```text
core, cplusplus, alpha.cplusplus.IteratorModeling, alpha.cplusplus.ContainerModeling, alpha.cplusplus.InvalidatedIterator, alpha.cplusplus.IteratorRange, alpha.cplusplus.MismatchedIterator
```

y `aggressive-binary-operation-simplification=true`; las experimentales, los
mismos más el plugin. Ver [Experimento](resultados/experimento.md).

**Cotejo por sitio.** Un aviso se atribuye al caso cuya función lo contiene, y
al **handle** sobre el que cae: el sostenido (la línea de `sink(...)`) o el
iterador de control (la cabecera del `for`). En un caso `UB`, el aviso acierta
sólo si cae sobre un handle que la norma da por inválido.

## Validación dinámica

```bash
python3 bench/run_runtime_validation.py --timeout 2
```

Cada caso se ejecuta en un proceso aislado con dos instrumentos:

| Instrumento | Compilador | Flags |
|---|---|---|
| libstdc++ Debug Mode | `g++ (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0` | `-D_GLIBCXX_DEBUG` |
| ASan + UBSan | `Ubuntu clang version 21.1.8 (++20251221032922+2078da43e25a-1~exp1~20251221153059.70)` | `-fsanitize=address,undefined` |

Estándar: C++17. Una ejecución sin detección **no**
reclasifica un caso `UB` como seguro: C++ no exige que el defecto se manifieste.

## Matriz normativa

```bash
python3 bench/gen_matrix.py
python3 bench/run_matrix.py
```

Benchmark previo y más pequeño (114 casos): una celda por
contenedor × operación × dominio (iterador / referencia), siempre en forma
`guarda`.
