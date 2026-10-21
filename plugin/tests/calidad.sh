#!/usr/bin/env bash
# Controles de calidad del capítulo 7.4: formato, tipos del arnés y cobertura del núcleo.
# Sólo lee el código: el formato se comprueba (--dry-run), no se aplica.
set -euo pipefail
cd /work

echo "== formato (clang-format, estilo LLVM) =="
find plugin \( -name '*.cpp' -o -name '*.h' \) -not -path '*/tests/lit/*' -print0 |
  xargs -0 clang-format --dry-run -Werror
echo "sin diferencias"

echo "== tipos del arnés (mypy) =="
mypy --ignore-missing-imports --cache-dir build/mypy \
  bench/experimento.py bench/pruebas_evaluacion.py bench/etiquetar.py bench/gen_corpus.py \
  bench/codigo_real.py bench/inyeccion.py bench/run_runtime_validation.py bench/rendimiento.py bench/regresion.py norma/gen_tabla.py

echo "== leyes de la evaluación =="
python3 bench/pruebas_evaluacion.py

echo "== cobertura de líneas del núcleo (llvm-cov, umbral 90 %) =="
cmake -S plugin -B build/cov -G Ninja -DCMAKE_BUILD_TYPE=Debug -DUCSM_COVERAGE=ON >/dev/null
cmake --build build/cov --target dominio_tests >/dev/null
rm -f build/cov/leyes.profraw build/cov/leyes.profdata
LLVM_PROFILE_FILE=build/cov/leyes.profraw ./build/cov/dominio_tests --gtest_brief=1
llvm-profdata merge -o build/cov/leyes.profdata build/cov/leyes.profraw
llvm-cov report ./build/cov/dominio_tests -instr-profile=build/cov/leyes.profdata plugin/dominio/ | tee build/cov/informe.txt
lineas=$(awk '/^TOTAL/ {print $(NF-3)}' build/cov/informe.txt | tr -d '%')
python3 -c "import sys; v=float('$lineas'); print(f'líneas: {v} %'); sys.exit(0 if v >= 90 else 1)"
