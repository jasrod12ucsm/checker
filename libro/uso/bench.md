# Correr los bench

Todos se corren **dentro de la imagen**: `docker compose run --rm <servicio>`,
o desde `docker compose run --rm shell`. Los tiempos son de una máquina de
16 núcleos.

| Qué | Orden | Tiempo | Escribe en |
|---|---|---|---|
| Verificación rápida de los requerimientos | `docker compose run --rm verificar` | 30 s | `build/verificacion/` |
| Experimento completo + regresión + costo | `docker compose run --rm experimento` | 2–3 min | `test/experimento/`, `test/corpus_results.json`, `test/corpus_fallos.json` |
| Validación dinámica del banco | `python3 bench/run_runtime_validation.py --timeout 1` | 1 min | `test/runtime_validation_results.json` |
| Calidad: formato, `mypy`, leyes del arnés, cobertura | `docker compose run --rm calidad` | 1 min | `build/cov/` |
| Código real (4 proyectos) | `python3 bench/codigo_real.py build/real salida.json` | unos 20 min, casi todo RocksDB | el JSON que le pases |
| Defectos sembrados en código real | `python3 bench/inyeccion.py build/real salida.json` | minutos | el JSON que le pases |

## El experimento

Corre el banco (750 casos) en cuatro condiciones, con una invocación de
`clang` por caso y condición:

| Condición | Checkers |
|---|---|
| `Reference` | `core`, `cplusplus` y los cinco `alpha.cplusplus` de iteradores y contenedores de CSA |
| `Experimental-Silent` | lo mismo + el checker con `PolicyMode=Silent` |
| `Experimental-Possibly` | lo mismo + el checker con `PolicyMode=Possibly` |
| `Plugin-Possibly` | `core`, `cplusplus` y el checker, sin los `alpha` |

```bash
docker compose run --rm experimento
# 750 casos × 4 condiciones en 130.8 s
#   Reference              TP  80 FN 262 FP  0 TN 306 POLICY   0/102 ...
#   Experimental-Possibly  TP 342 FN   0 FP  0 TN 306 POLICY 102/102 ...
```

Cada aviso se lee del SARIF de `clang`, se atribuye a la función del caso y
al handle sobre el que cae (cotejo por sitio), y se cuenta como VP, FP, FN, VN,
aviso posible o incidente. Salidas:

| Archivo | Contenido |
|---|---|
| `test/experimento/ejecucion.json` | cada ejecución: condición, resultado, segundos, memoria, avisos |
| `test/experimento/cotejo.json` | el veredicto de cada caso en cada condición |
| `test/experimento/metricas.json` | conteos, precisión, exhaustividad y F1, por contenedor, operación, handle, forma y garantía; versiones y sha256 del plugin y del banco |

Después corre `bench/regresion.py`, que falla si un caso `SAFE` gana un aviso
o si un UB que se detectaba deja de detectarse, y `bench/rendimiento.py`, que
comprueba el costo del checker (tiempo +10 % y memoria +5 % como máximo).

Para depurar:

```bash
python3 bench/experimento.py --muestra --salida build/verificacion   # 81 casos, un poco de todo
python3 bench/experimento.py --solo f_vector_clear_ref_recto --salida build/x
```

Con `--muestra` o `--solo`, los resultados oficiales de `test/` no se tocan.

## La validación dinámica

Comprueba las etiquetas del banco ejecutando cada caso de verdad con dos
oráculos: libstdc++ en modo de depuración (`-D_GLIBCXX_DEBUG`) y
AddressSanitizer con UndefinedBehaviorSanitizer. Cada caso corre en un
proceso aparte; los `POLICY`, dos veces (forzando y evitando la condición).

```bash
python3 bench/gen_corpus.py                           # el banco, desde la norma
python3 bench/run_runtime_validation.py --timeout 1   # 852 ejecuciones
```

Una detección en un caso `SAFE` sería una contradicción con la norma.
Hay 0. Ver [Protocolo de validación dinámica](../banco/protocolo-dinamico.md).

## Código real

Los cuatro proyectos se clonan **dentro de la imagen**, porque `build/` es un
volumen de Docker. Estos son los *commits* que se analizaron:

```bash
docker compose run --rm shell
mkdir -p build/real && cd build/real
git clone https://github.com/ninja-build/ninja   && git -C ninja    checkout 2daa09ba270b0a43e1929d29b073348aa985dfaa
git clone https://github.com/google/leveldb      && git -C leveldb  checkout 99b3c03b3284f5886f9ef9a4ef703d57373e61be
git clone https://github.com/jbeder/yaml-cpp     && git -C yaml-cpp checkout f7320141120f720aecc4c32be25586e7da9eb978
git clone https://github.com/facebook/rocksdb    && git -C rocksdb  checkout 3c27a3dde0993210c5cc30d99717093f7537916f
cd /work
python3 bench/codigo_real.py build/real build/real/avisos.json                      # los cuatro
python3 bench/codigo_real.py build/real build/real/ninja.json Possibly noredundancy ninja   # uno
python3 bench/inyeccion.py build/real build/real/inyeccion.json                     # S1–S8, B1, B2
```

RocksDB tiene 682 unidades: suma 9 451 s de análisis, unos 14 minutos con los 12 procesos en paralelo que usa el script. Los resultados
registrados están en `test/codigo_real/` y en
[Código real](../resultados/codigo-real.md).

## Calidad

```bash
docker compose run --rm calidad
```

Comprueba el formato del plugin con `clang-format` (estilo LLVM, sin
aplicarlo), los tipos del arnés con `mypy`, las 11 leyes de la evaluación y
la cobertura de líneas del núcleo con `llvm-cov`, que debe ser de 90 % o más.
Hoy es 92.5 %.

## El CI

`.github/workflows/ci.yml` corre `plugin`, `calidad` y `experimento` en
GitHub Actions con la misma imagen, y publica `test/experimento/` como
artefacto.
