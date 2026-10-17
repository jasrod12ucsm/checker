# Validación dinámica del corpus

## Propósito y alcance

El corpus no evalúa fugas de memoria. Evalúa el uso posterior de un iterador,
referencia o puntero que puede haber sido invalidado por una mutación de un
contenedor STL. El efecto de ese uso es comportamiento indefinido (UB): puede
manifestarse como acceso a memoria liberada, aborto de la biblioteca, resultado
aparentemente correcto o ausencia total de síntoma observable.

Por esta razón, la ausencia de un *crash* no reclasifica un caso UB como seguro.
La regla normativa de C++17 conserva el papel de oráculo semántico. La ejecución
instrumentada aporta una segunda fuente de evidencia independiente: demuestra
cuándo una implementación concreta logra observar el defecto.

## Estrategia de doble oráculo

Cada función de `test/corpus.cpp` se invoca en un proceso independiente mediante
un *harness* generado. Un proceso separado es necesario porque una detección
puede abortar la ejecución. Se emplean dos instrumentos complementarios:

| Instrumento | Compilación | Evidencia que aporta |
|-------------|-------------|----------------------|
| libstdc++ Debug Mode | `g++ -D_GLIBCXX_DEBUG` | Detecta usos inválidos de iteradores mediante los iteradores seguros de la biblioteca. |
| AddressSanitizer y UBSan | `clang++ -fsanitize=address,undefined` | Detecta manifestaciones físicas observables, como `heap-use-after-free`. |

Los instrumentos no sustituyen al estándar: ASan no tiene por qué detectar una
invalidez que no reutilice memoria liberada, y el modo de depuración de una
biblioteca puede no implementar todas las comprobaciones semánticas posibles.

Los casos `POLICY` se ejecutan dos veces:

- `force`: fuerza la condición invalidante: capacidad agotada antes de mutar un
  `vector`, o factor de carga alcanzado antes de insertar en un contenedor
  `unordered`.
- `preserve`: establece una capacidad de 256 elementos, suficiente para las
  solicitudes `size()+100`, o ejecuta `reserve(256)` antes de una inserción en
  un contenedor `unordered`.

La precondición concreta de cada ejecución se conserva en el campo `escenario`
de `runtime_validation_results.json`. `shrink_to_fit` constituye una excepción
documentada: es una solicitud no vinculante; el protocolo registra su resultado
observado con y sin holgura de capacidad, sin atribuirle una garantía que C++ no
ofrece.

## Protocolo reproducible

La ejecución se reproduce con:

```bash
python3 bench/gen_corpus.py
python3 bench/run_runtime_validation.py --timeout 1
```

El segundo comando genera `test/runtime_runner.cpp`, compila ambos binarios
instrumentados y guarda la evidencia por caso en
`test/runtime_validation_results.json`. Los bucles del corpus están acotados a
tres rondas para conservar la mutación durante la iteración sin introducir
recorridos infinitos en contenedores cuyos iteradores permanecen válidos.

Los archivos que forman el paquete de validación son:

- `bench/gen_corpus.py`: generador del corpus y del oráculo normativo.
- `bench/gen_runtime_harness.py`: generador del ejecutable de despacho.
- `bench/run_runtime_validation.py`: protocolo experimental y recolector.
- `test/corpus_truth.json`: clasificación normativa de los 684 casos.
- `test/runtime_validation_results.json`: evidencia dinámica reproducible.

## Control estructural descubierto durante la validación

La primera ejecución instrumentada encontró ocho casos inicialmente etiquetados
como `SAFE`: referencias o punteros de `deque` dentro de un bucle. Aunque el
handle declarado conserva validez, el iterador de control del `for` queda
invalidado por la operación y su incremento posterior produce UB. La regla del
generador fue corregida para clasificar el programa completo, no solo el handle
que se observa explícitamente.

La segunda revisión detectó que `vector::pop_back` dentro de un bucle acotado
termina eliminando el elemento inicialmente retenido. Sus tres variantes se
reclasificaron de `POLICY` a `UB`. Tras reducir el alcance a diez contenedores,
el corpus final contiene 363 casos `UB`, 246 casos `SAFE` y 75 casos `POLICY`.
Ninguno de los casos `SAFE` produjo una
detección dinámica.

## Validación dinámica completa del protocolo

La corrida final cubrió los 684 casos base y produjo 759 ejecuciones: una por
caso `UB` o `SAFE` y dos por cada caso `POLICY`. El informe declara
`cobertura_protocolo: "COMPLETA"` únicamente si están presentes todas esas
ejecuciones y todos los identificadores del oráculo normativo. La siguiente
tabla resume la evidencia observada:

| Etiqueta normativa | Ejecuciones | Debug Mode: detectado | ASan/UBSan: detectado |
|--------------------|------------:|----------------------:|----------------------:|
| `UB` | 363 | 192 | 222 |
| `SAFE` | 246 | 0 | 0 |
| `POLICY` | 150 | 30 | 57 |

Los casos UB no observados dinámicamente permanecen como UB: C++ no obliga a
que una implementación manifieste el error en tiempo de ejecución. El resultado
correcto es una validación dinámica completa de la cobertura experimental y una
combinación de trazabilidad normativa con observación dinámica. No significa
erróneamente que todo UB deba producir un fallo visible: los casos sin síntoma
siguen siendo UB por su regla normativa.

## Redacción para la tesis

> El corpus fue sometido a validación dinámica completa de su protocolo
> experimental. Cada uno de los 684 casos se ejecutó de forma aislada bajo
> libstdc++ Debug Mode y bajo
> AddressSanitizer/UBSan. El primer instrumento verifica usos inválidos de
> iteradores a nivel de biblioteca; el segundo identifica manifestaciones de
> seguridad de memoria, como accesos a memoria liberada. Las etiquetas se
> conservaron fundamentadas en las reglas de invalidación de C++17, debido a que
> el comportamiento indefinido no exige una manifestación observable. La
> evidencia permitió además detectar y corregir dos inconsistencias del
> generador: en los bucles se debe considerar el iterador de control y, para
> `pop_back`, las rondas sucesivas pueden eliminar el elemento retenido.
