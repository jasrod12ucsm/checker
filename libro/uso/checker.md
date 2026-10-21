# Levantar el checker

El checker es una biblioteca dinámica, `libContainerInvalidation.so`, que
`clang` carga con `-load`. No hay que recompilar LLVM. Se construye y se
usa **dentro de la imagen**, porque enlaza contra las cabeceras de Clang
21.1.8 de esa imagen.

## Construir y probar

```bash
docker compose build              # una vez
docker compose run --rm plugin    # CMake + 40 gtests + 5 pruebas lit
```

Lo que hace `plugin`, paso a paso:

```bash
cmake -S plugin -B build/plugin -G Ninja -DCMAKE_BUILD_TYPE=Debug
cmake --build build/plugin            # genera NormTable.inc desde norma/matriz.json y compila
./build/plugin/dominio_tests          # leyes del núcleo (gtest)
lit build/plugin/tests/lit            # el checker dentro de clang
```

El resultado queda en `build/plugin/libContainerInvalidation.so`. `build/` es
un volumen de Docker: el binario no sirve fuera del contenedor.

Al construir, CMake llama a `norma/gen_tabla.py`. Si `matriz.json` rompe una
ley de la norma (una regla sin cláusula, un iterador que se preserva donde su
referencia se invalida…), la tabla no se genera y el build falla.

{{codigo plugin/CMakeLists.txt 21-33}}

## Usarlo sobre un archivo

Abre una shell dentro de la imagen:

```bash
docker compose run --rm shell
```

y analiza un archivo. `ejemplos/prueba.cpp` trae tres funciones: una con un
uso inválido seguro, una que depende de la capacidad y una con garantía.

{{codigo ejemplos/prueba.cpp posible}}

```bash
P=build/plugin/libContainerInvalidation.so
clang++ -std=c++17 --analyze -o /dev/null \
  -Xclang -load -Xclang $P \
  -Xclang -analyzer-checker=ucsm.ContainerInvalidation \
  ejemplos/prueba.cpp
```

```text
ejemplos/prueba.cpp:7:10: warning: Uso de una referencia invalidada: 'std::vector::clear' (línea 6) lo invalidó [ucsm.ContainerInvalidation]
1 warning generated.
```

### Las opciones

| Opción | Qué hace |
|---|---|
| `-Xclang -analyzer-config -Xclang ucsm.ContainerInvalidation:PolicyMode=Possibly` | además de los avisos confirmados, da avisos **posibles** cuando la invalidación depende de la capacidad o del *rehash* y el código no dio ninguna garantía. Por omisión es `Silent`: solo confirmados |
| `-Xclang -analyzer-output=text` | muestra la ruta del aviso: dónde se obtuvo el handle, qué lo invalidó y dónde se usó |
| `-Xclang -analyzer-checker-option-help` (con `-cc1 -load`) | lista las opciones del checker |

Con las dos primeras:

```text
ejemplos/prueba.cpp:13:10: warning: Uso de una referencia posiblemente invalidada: 'std::vector::push_back' (línea 12) si la capacidad está agotada reubica los elementos; nada garantiza espacio: use reserve(size() + n) antes, o vuelva a obtenerlo [ucsm.ContainerInvalidation]
ejemplos/prueba.cpp:11:12: note: El handle al elemento se obtiene de 'std::vector::operator[]'
ejemplos/prueba.cpp:12:3: note: El handle al elemento puede quedar invalidado por 'std::vector::push_back'
```

La función `con_garantia` no da aviso en ningún modo, porque
`reserve(size() + 1)` garantiza la inserción.

## Usarlo sobre un proyecto

Un proyecto CMake se analiza desde su base de compilación
(`compile_commands.json`), una invocación de `clang` por unidad de
traducción. `bench/codigo_real.py` hace eso. `ejemplos/` es un proyecto
mínimo para probarlo:

```bash
python3 bench/codigo_real.py . build/verificacion/ejemplos.json Possibly noredundancy ejemplos
# ejemplos: 2 TU, 2 avisos, 0 TU con error, 0.5 s
```

Para un proyecto tuyo, clónalo en una carpeta, agrégalo a `PROYECTOS` en
`bench/codigo_real.py` con sus opciones de CMake y corre
`python3 bench/codigo_real.py <carpeta> salida.json`. Los avisos quedan en
el JSON con su ruta completa para revisarlos a mano.
