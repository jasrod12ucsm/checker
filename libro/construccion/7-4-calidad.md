# 7.4 Calidad del código

| Característica | Práctica | Medida / control | Umbral | Hoy |
|---|---|---|---|---|
| **Servicio: corrección** | una prueba por regla del dominio y por requisito; API completa con `inject` | Vitest (`npm test`) | todas en verde; cobertura ≥ 90 % de líneas y funciones, ≥ 80 % de ramas | 140 pruebas en la imagen Docker; 97,6 % de líneas, 96,2 % de funciones, 87,7 % de ramas |
| **Servicio: mantenibilidad** | capas por paquete; el dominio sin Fastify, SQLite ni Node | `pruebas/arquitectura.test.ts` | 0 importaciones fuera de capa | cumplido (RNF-S05) |
| **Servicio: tipos** | `strict` y garantías que no deben compilar | `tsc` y `@ts-expect-error` | 0 errores; cada garantía sigue sin compilar | cumplido |
| **Servicio: seguridad de acceso** | claves scrypt, sesión guardada como hash, cookie `httpOnly`/`SameSite=Strict`, bloqueo tras 10 fallos, firma HMAC del *webhook* | `cripto.test.ts`, `api.test.ts` | todas en verde | cumplido (RNF-S01, RNF-S02) |
| **Servicio: inyección** | SQL siempre con consultas preparadas y parámetros (`db.prepare`); `clang` con `execFile` y argumentos separados, sin consola | revisión y prueba de arquitectura | 0 SQL armado con texto del usuario; 0 llamadas a una consola | cumplido |
| **Servicio: XSS** | la API solo responde JSON, nunca HTML con datos del usuario; el panel mostrará los datos como texto (React escapa por defecto) | revisión | 0 HTML armado con datos | cumplido en la API |
| **Servicio: eficiencia** | medir el tiempo de una revisión | demostración de punta a punta con `clang` real | — | 0,28 s por revisión de dos archivos |
| **Motor: legibilidad** | estilo LLVM, nombres del lenguaje ubicuo, documentación en español | `clang-format --dry-run -Werror`; `-Wall -Wextra` | 0 diferencias de formato, 0 avisos del compilador | 0 y 0 |
| **Motor: mantenibilidad** | capas con frontera de *target*; la norma en un solo archivo; núcleo puro | el núcleo (`ucsm_dominio`) **no compila** si incluye Clang | la norma sólo en `matriz.json` | cumplido (RNF-07) |
| **Motor: corrección** | una prueba por ley; `lit` por regla; el banco como regresión | gtests, `lit`, `bench/experimento.py` | 0 casos `SAFE` con aviso confirmado; ningún UB detectado se pierde | 40 gtests, 5 `lit`; 0/306 FP; 342/342 UB |
| **Motor: eficiencia** | medir antes de optimizar | tiempo y RSS máximo por caso, referencia frente a experimental | < 10 % de tiempo, < 5 % de memoria (RNF-04/05) | +0,3 % y +0,7 % |
| **Motor: robustez** | el checker nunca aborta `clang`; las constantes que no caben se tratan como desconocidas | incidentes del experimento; proyectos reales | 0 caídas | 0 en 3 000 ejecuciones y 781 unidades |
| **Arnés: seguridad** | el arnés no interpola nombres en una orden de consola | `subprocess.run([...])` sin `shell=True` | 0 usos de `shell=True` | cumplido |
| **Arnés: tipos** | anotaciones en todo el arnés | `mypy` | 0 errores | 0 en 10 archivos |
| **Motor: pruebas** | pirámide: leyes → `lit` → banco → código real | los cuatro niveles en verde; cobertura de líneas del núcleo con `llvm-cov` | ≥ 90 % en `dominio/` | 92,5 % de líneas, 86,9 % de ramas |

## Las reglas que vuelven imposibles errores concretos

| Regla | Error que hace imposible |
|---|---|
| `Revision<E>` lleva su estado en el tipo | publicar una revisión que no está en análisis |
| `Autorizado<P>` como primer argumento | ejecutar una operación sin haber comprobado el permiso |
| unión de estados + `inalcanzable(never)` | olvidar un estado nuevo de la revisión o un error nuevo en el mapa HTTP |
| zod en cada frontera (HTTP y filas) | que un dato mal formado llegue al dominio |
| `dominio/` sin include dirs de Clang | que la lógica de la norma dependa del motor y no se pueda probar sola |
| `switch` sin `default:` + `-Werror=switch` | olvidar una variante nueva de `Effect` o `Validity` |
| `Validity` de tres valores | presentar «no sé» como «seguro» |
| tabla normativa generada | que el checker y las etiquetas digan cosas distintas |
| `Outcome` de cinco valores en el arnés | que un *timeout* cuente como «sin avisos» |
| métricas `Ratio │ Undefined` | un 0/0 publicado como 0 % |

## TDD donde rinde

En el servicio, cada regla del dominio tiene su prueba en el mismo paquete,
y cada requisito una prueba de caso de uso con dobles de los puertos, que no
necesita ningún adaptador para correr. El núcleo
del motor se escribió **ley primero**: la prueba de la ley, después la
decisión. En la cáscara no rinde igual (depende del motor). Ahí se escribe el
caso `lit` mínimo que reproduce el FN o el FP, y después el reconocimiento que
lo cierra. Así se cerraron el borrado por rango de RocksDB y la constante
enorme que abortaba `clang`.
