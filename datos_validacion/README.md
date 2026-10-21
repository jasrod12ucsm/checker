# Datos de validación dinámica del corpus

Este paquete contiene el corpus de 684 programas C++17 y su evidencia de
validación dinámica reproducible.

## Contenido

- `bench/gen_corpus.py`: genera el corpus fuente y el oráculo normativo.
- `bench/gen_runtime_harness.py`: genera el despachador que aísla cada caso en
  un proceso.
- `bench/run_runtime_validation.py`: compila y ejecuta el protocolo dinámico.
- `test/corpus.cpp`: los 684 programas del corpus.
- `test/corpus_truth.json`: clasificación normativa por caso.
- `test/runtime_runner.cpp`: despachador generado para la corrida publicada.
- `test/runtime_validation_results.json`: resultados por caso, escenario,
  instrumento y entorno de compilación.
- `test/corpus_results.json` y `test/corpus_fallos.json`: resultados del
  analizador estático evaluado.

## Reproducción

Desde la raíz del proyecto:

```bash
python3 bench/gen_corpus.py
python3 bench/experimento.py   # dentro de la imagen checker:llvm21
python3 bench/run_runtime_validation.py --timeout 1
```

Se requieren Python 3, `g++` con libstdc++ Debug Mode y `clang++` con
AddressSanitizer y UBSan. La corrida incluida cubre los 684 casos base y las
759 ejecuciones previstas por el protocolo: una para cada caso `UB` o `SAFE` y
dos configuraciones controladas para cada caso `POLICY`.

## Interpretación

`cobertura_protocolo: "COMPLETA"` en el archivo de resultados confirma que se
ejecutaron todos los casos y escenarios declarados. Las etiquetas semánticas
proceden del oráculo normativo; una ejecución sin detección no convierte un caso
de comportamiento indefinido en seguro, porque C++ no exige que el defecto se
manifieste.
