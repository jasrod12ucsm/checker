# 7.4 Calidad del código

| Característica | Práctica | Medida / control | Umbral | Hoy |
|---|---|---|---|---|
| **Legibilidad** | estilo LLVM, nombres del lenguaje ubicuo, documentación en español | `clang-format --dry-run -Werror`; `-Wall -Wextra` | 0 diferencias de formato, 0 avisos del compilador | 0 y 0 |
| **Mantenibilidad** | capas con frontera de *target*; la norma en un solo archivo; núcleo puro | el núcleo (`ucsm_dominio`) **no compila** si incluye Clang | la norma sólo en `matriz.json` | cumplido (RNF-07) |
| **Corrección** | una prueba por ley; `lit` por regla; el banco como regresión | gtests, `lit`, `bench/experimento.py` | 0 casos `SAFE` con aviso confirmado; ningún UB detectado se pierde | 40 gtests, 5 `lit`; 0/306 FP; 342/342 UB |
| **Eficiencia** | medir antes de optimizar | tiempo y RSS máximo por caso, referencia frente a experimental | < 10 % de tiempo, < 5 % de memoria (RNF-04/05) | +0.3 % y +0.7 % |
| **Robustez** | el checker nunca aborta `clang`; las constantes que no caben se tratan como desconocidas | incidentes del experimento; proyectos reales | 0 caídas | 0 en 3 000 ejecuciones y 781 unidades |
| **Seguridad** | el arnés no interpola nombres en una orden de consola | `subprocess.run([...])` sin `shell=True` | 0 usos de `shell=True` | cumplido |
| **Tipos del arnés** | anotaciones en todo el arnés | `mypy` | 0 errores | 0 en 8 módulos |
| **Pruebas** | pirámide: leyes → `lit` → banco → código real | los cuatro niveles en verde; cobertura de líneas del núcleo con `llvm-cov` | ≥ 90 % en `dominio/` | 92.5 % de líneas, 86.9 % de ramas |

## Las reglas que vuelven imposibles errores concretos

| Regla | Error que hace imposible |
|---|---|
| `dominio/` sin include dirs de Clang | que la lógica de la norma dependa del motor y no se pueda probar sola |
| `switch` sin `default:` + `-Werror=switch` | olvidar una variante nueva de `Effect` o `Validity` |
| `Validity` de tres valores | presentar «no sé» como «seguro» |
| tabla normativa generada | que el checker y las etiquetas digan cosas distintas |
| `Outcome` de cinco valores en el arnés | que un *timeout* cuente como «sin avisos» |
| métricas `Ratio │ Undefined` | un 0/0 publicado como 0 % |

## TDD donde rinde

El núcleo se escribió **ley primero**: la prueba de la ley, después la
decisión. En la cáscara no rinde igual (depende del motor). Ahí se escribe el
caso `lit` mínimo que reproduce el FN o el FP, y después el reconocimiento que
lo cierra. Así se cerraron el borrado por rango de RocksDB y la constante
enorme que abortaba `clang`.
