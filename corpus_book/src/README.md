
# Corpus de invalidación de iteradores


Este libro documenta **todos los casos** del corpus de invalidación de
iteradores, referencias y punteros de contenedores STL (C++17), junto con los
resultados de cada benchmark ejecutado sobre él.

> Generado automáticamente por `bench/gen_book.py` a partir de los artefactos de
> `test/`. No editar a mano: regenerar con `python3 bench/gen_book.py`.

## Cifras

| | |
|---|---:|
| Casos analíticos (funciones en `test/corpus.cpp`) | **750** |
| Contenedores | 10 |
| Pares contenedor–operación | 57 |
| Casos `UB` normativo | 342 |
| Casos `SAFE` normativo | 306 |
| Casos `POLICY` (depende del estado) | 102 |
| Ejecuciones dinámicas | 852 |
| Cobertura del protocolo dinámico | `COMPLETA` |
| Casos de la matriz normativa (`test/matrix.cpp`) | 114 |

## Resultado principal del análisis estático

El Clang Static Analyzer (checkers `alpha.cplusplus.*`) detecta
**80 de 342** casos `UB` (23.4%),
con **0** falsos positivos sobre 306 casos `SAFE`.
Ver [Análisis estático](resultados/estatico.md) y
[Catálogo de falsos negativos](resultados/fallos.md).

## Cómo leer el libro

- **Metodología**: dimensiones del corpus, etiquetas y protocolo.
- **Resultados**: benchmark estático, validación dinámica y matriz normativa.
- **Casos del corpus**: un capítulo por contenedor y una página por operación,
  con el código de cada uno de los 750 casos, su etiqueta normativa, lo que
  dijo el analizador estático y lo que observaron los instrumentos dinámicos.
- **Índice de casos**: tabla plana de los 750 casos con enlaces.

La búsqueda (tecla `s`) acepta nombres de función, p. ej. `f_deque_push_back_ref_bucle`.
