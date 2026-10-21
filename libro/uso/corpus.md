# Usar el corpus

El corpus (el **banco**) son 750 funciones C++ en `test/corpus.cpp`. Cada una
obtiene un handle a un elemento, muta el contenedor y usa el handle. Su
respuesta correcta está en `test/corpus_truth.json`.

## Un caso

{{codigo test/corpus.cpp f_vector_clear_ref_recto}}

```json
"f_vector_clear_ref_recto": {
  "contenedor": "vector", "op": "clear", "sostiene": "ref", "forma": "recto",
  "esperado": "UB", "garantia": "ninguna",
  "handles": {"sostenido": "UB", "control": null}
}
```

El nombre dice todo: `f_<contenedor>_<operación>_<handle>_<forma>`, con
`_reserva` al final en los casos de buen uso con `reserve`, y `erase_ret` en
los de `it = c.erase(it)`.

| Campo | Valores |
|---|---|
| `sostiene` | `it` (iterador), `ref` (referencia), `ptr` (puntero) |
| `forma` | `recto`; `guarda` (compara con `end()`); `llamada` (la mutación ocurre en otra función); `bucle` (también se usa el iterador de control) |
| `esperado` | `UB` (inválido), `SAFE` (válido), `POLICY` (depende de la capacidad o del *rehash*) |
| `garantia` | `ninguna`, `reserva` (`reserve(size() + k)` antes), `devuelto` (el iterador que devuelve la mutación) |

La misma situación con garantía no tiene UB:

{{codigo test/corpus.cpp f_vector_push_back_ref_recto_reserva}}

## De dónde sale la etiqueta

Nadie la escribe a mano. `bench/gen_corpus.py` arma cada caso y le pregunta
la etiqueta a `bench/etiquetar.py`, que lee `norma/matriz.json`. La etiqueta
es el peor efecto que la norma da a los handles que el caso usa (el retenido
y, en `bucle`, el iterador de control):

{{codigo bench/etiquetar.py por_handle}}

{{codigo bench/etiquetar.py etiqueta}}

El núcleo del checker, en C++, es la otra implementación de la misma norma.
El gtest `Banco.ElVeredictoDelNucleoEsLaEtiqueta` compara las dos celda por
celda (ver [RF-08](requerimientos.md#rf-08-aplicar-la-regla-de-c17)).

## Analizar un solo caso

`-analyze-function` limita el análisis a una función:

```bash
docker compose run --rm shell
clang++ -std=c++17 --analyze -o /dev/null \
  -Xclang -load -Xclang build/plugin/libContainerInvalidation.so \
  -Xclang -analyzer-checker=ucsm.ContainerInvalidation \
  -Xclang -analyzer-output=text \
  -Xclang -analyze-function="f_vector_clear_ref_recto(std::vector<int> &)" \
  test/corpus.cpp
```

Para el mismo caso en las cuatro condiciones del experimento:

```bash
python3 bench/experimento.py --solo f_vector_clear_ref_recto --salida build/x
```

Cada caso tiene además su página en este libro, con el código, la etiqueta,
lo que hizo CSA, lo que hizo el checker y lo que dijeron los oráculos
dinámicos: [Índice de casos](../indice.md).

## El banco está sellado

`test/banco-1.json` guarda el sha256 de `corpus.cpp` y de
`corpus_truth.json`. El experimento se niega a correr si el banco no
coincide con un sello (`BankNotFrozen`), y `verificar` regenera el banco
desde la norma y comprueba que da el mismo sha256.

Para ampliar el banco (otra operación, otra forma): cambia
`bench/gen_corpus.py` o `norma/matriz.json`, regenera con
`python3 bench/gen_corpus.py`, valida con
`python3 bench/run_runtime_validation.py --timeout 1` hasta tener 0
contradicciones, y crea un sello nuevo `test/banco-2.json`. No se edita
`banco-1`: los resultados publicados se refieren a él.

## Otros archivos de `test/`

| Archivo | Qué es |
|---|---|
| `corpus_results.json` | por caso: qué hizo CSA y qué hizo el checker (lo escribe el experimento) |
| `corpus_fallos.json` | los falsos negativos de CSA con su causa |
| `runtime_runner.cpp` | el ejecutable de la validación dinámica (generado) |
| `runtime_validation_results.json` | lo que vio cada oráculo en cada ejecución |
| `matrix.cpp`, `matrix_truth.json`, `matrix_results.json` | la matriz normativa anterior al banco (`bench/gen_matrix.py`, `bench/run_matrix.py`) |
