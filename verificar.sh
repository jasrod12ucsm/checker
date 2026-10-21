#!/usr/bin/env bash
# Verifica los requerimientos del checker. Se corre dentro de la imagen:
#   docker compose run --rm verificar              rápida, menos de un minuto
#   docker compose run --rm verificar --completo   además el banco entero y la validación dinámica (unos 4 min con 16 núcleos)
# Cada paso dice qué requerimientos demuestra (libro: Guía de uso → Dónde se valida cada requerimiento).
set -euo pipefail
cd "$(dirname "$0")"
inicio=$(date +%s)
paso() { printf '\n== %s\n' "$1"; }

paso "RF-16, RF-17: construir el plugin; gen_tabla.py comprueba las leyes de la norma"
cmake -S plugin -B build/plugin -G Ninja -DCMAKE_BUILD_TYPE=Debug >/dev/null
cmake --build build/plugin >/dev/null
echo "build/plugin/libContainerInvalidation.so"

paso "RF-08, RF-09, RF-10, RF-17, RNF-07: leyes del núcleo (gtest)"
./build/plugin/dominio_tests --gtest_brief=1 | tail -1

paso "RF-01, RF-04 a RF-12, RNF-06: el checker dentro de clang (lit)"
lit -sv build/plugin/tests/lit | grep -E "^(PASS|FAIL)|Passed|Failed"

paso "RF-14, RN-001, RN-004, RN-005, RN-006: leyes de la evaluación"
python3 bench/pruebas_evaluacion.py | tail -3

paso "RF-15, RN-001, RN-007: regenerar el banco desde la norma y comprobar su sello (test/banco-1.json)"
python3 bench/gen_corpus.py >/dev/null
python3 - <<'PY'
import hashlib, json, sys
sello = json.load(open("test/banco-1.json"))
for f in ("corpus.cpp", "corpus_truth.json"):
    h = hashlib.sha256(open(f"test/{f}", "rb").read()).hexdigest()
    print(f"test/{f}: {'igual al sello' if h == sello[f] else 'DISTINTO del sello'} {sello['banco']}")
    if h != sello[f]:
        sys.exit(1)
PY

paso "RF-03, RF-07: analizar un proyecto desde su base de compilación (ejemplos/)"
mkdir -p build/verificacion
python3 bench/codigo_real.py . build/verificacion/ejemplos.json Possibly noredundancy ejemplos
python3 - <<'PY'
import json, sys
r = json.load(open("build/verificacion/ejemplos.json"))["proyectos"]["ejemplos"]["resultados"]
avisos = {res["file"].rsplit("/", 1)[-1]: [a["clase"] for a in res["avisos"]] for res in r}
print(avisos)
esperado = {"prueba.cpp": ["confirmado", "posible"], "buen_uso.cpp": []}
sys.exit(0 if {k: sorted(v) for k, v in avisos.items()} == esperado else "los avisos de ejemplos/ no son los esperados")
PY

if [ "${1:-}" = "--completo" ]; then
  paso "RF-02, RF-13, RN-002, RN-003, RN-007, RNF-01 a RNF-03: experimento, banco completo"
  python3 bench/experimento.py
  python3 bench/regresion.py
  paso "RF-15: validación dinámica del banco (libstdc++ Debug Mode y ASan/UBSan, 852 ejecuciones)"
  python3 bench/run_runtime_validation.py --timeout 1 --output build/verificacion/runtime.json --build-dir build/runtime >/dev/null
  python3 - <<'PY'
import json, sys
d = json.load(open("build/verificacion/runtime.json"))
safe = [r["fn"] for r in d["resultados"] if r["etiqueta_normativa"] == "SAFE"
        and "DETECTADO" in (r["libstdcxx_debug"]["estado"], r["asan_ubsan"]["estado"])]
print(f"{d['ejecuciones']} ejecuciones; {d['resumen']}; contradicciones (SAFE con detección): {len(safe)}")
sys.exit(1 if safe else 0)
PY
else
  paso "RF-02, RF-13, RN-002, RN-003, RN-007, RNF-01 a RNF-03: experimento, muestra del banco"
  python3 bench/experimento.py --muestra --salida build/verificacion
  python3 bench/regresion.py --muestra build/verificacion/metricas.json
fi

paso "RNF-04, RNF-05: costo del checker (test/experimento/ejecucion.json)"
python3 bench/rendimiento.py

printf '\nTodo en verde en %s s.\n' "$(( $(date +%s) - inicio ))"
