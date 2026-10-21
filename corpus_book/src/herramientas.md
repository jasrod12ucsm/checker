
# Las herramientas de ejecución

Las dos son **herramientas que vigilan un programa mientras se ejecuta** y lo
detienen apenas hace algo prohibido.

## El problema que resuelven

Cuando un programa C++ usa un iterador roto, normalmente **no pasa nada
visible**: lee un número viejo que seguía en esa memoria y continúa. El bug está,
pero escondido. Es como cruzar un semáforo en rojo sin que pase un auto: hiciste
algo prohibido, pero no te enteras.

Estas herramientas **ponen un policía en el semáforo**: cada vez que el programa
hace algo prohibido, lo paran y dicen exactamente qué hizo.

## libstdc++ Debug Mode — vigila los iteradores

**libstdc++** es la biblioteca estándar de C++ que trae `g++`: el código que
implementa `std::vector`, `std::map`, etc. **Debug Mode** es una versión
"vigilada" de esa misma biblioteca. Se activa al compilar:

```bash
g++ -D_GLIBCXX_DEBUG programa.cpp
```

En esa versión **cada contenedor lleva una lista de sus iteradores**. Cuando
modificas el contenedor, marca como rotos los iteradores que el estándar dice que
se rompen. Cuando usas un iterador, primero revisa si está marcado y, si lo está,
detiene el programa:

```cpp
std::vector<int> v = {1, 2, 3};
auto it = v.begin();
v.clear();          // Debug Mode: "it ahora está roto"
int x = *it;        // Debug Mode: ¡alto!
```

```text
Error: attempt to dereference a singular iterator.
```

*Singular iterator* es la forma técnica de decir "iterador roto". También aparece
`attempt to increment a singular iterator`, cuando se hace `++it` sobre uno roto.

**Límite:** solo vigila **iteradores**. Una referencia (`const int& r = v[0]`) o
un puntero (`int* p = &v[0]`) son tipos básicos del lenguaje, no de la
biblioteca, así que Debug Mode no puede seguirlos.

## AddressSanitizer (ASan) — vigila la memoria

Es una herramienta del compilador (`clang++` o `g++`):

```bash
clang++ -fsanitize=address programa.cpp
```

No sabe nada de iteradores: **vigila la memoria**. Cuando el programa libera
memoria (por ejemplo, un vector que se muda a otro lugar y suelta el espacio
viejo), ASan marca ese espacio como prohibido. Si después el programa lo lee o lo
escribe, lo detiene:

```cpp
std::vector<int> v = {1, 2, 3};
int* p = &v[0];      // puntero al primer elemento
v.push_back(4);      // sin espacio: el vector se muda y libera la memoria vieja
int x = *p;          // p apunta a memoria liberada: ASan dice ¡alto!
```

```text
ERROR: AddressSanitizer: heap-use-after-free
```

*Heap-use-after-free* = usaste memoria después de liberarla.

**Límite:** solo ve el bug si la memoria **realmente se liberó**. Si el
contenedor invalida algo pero conserva la memoria (por ejemplo, `vector::clear`
destruye los elementos pero no suelta el espacio), para ASan el acceso es legal.

## UBSan (Undefined Behavior Sanitizer)

Se activa junto con ASan (`-fsanitize=address,undefined`) y vigila **otros**
tipos de comportamiento indefinido: división por cero, desbordamiento de enteros,
etc. En este corpus no aportó detecciones propias (todas las de esta compilación
fueron `heap-use-after-free` de ASan); se activa porque no cuesta nada.

## Por qué se usan las dos

Ven cosas distintas, y a veces solo una nota el bug:

| Situación | Debug Mode | ASan |
|---|---|---|
| Iterador roto **y** memoria liberada | ✅ lo ve | ✅ lo ve |
| Iterador roto, memoria **no** liberada | ✅ lo ve | ❌ la memoria sigue siendo "legal" |
| Referencia o puntero a memoria liberada | ❌ no sigue referencias | ✅ lo ve |
| Referencia o puntero roto, memoria **no** liberada | ❌ | ❌ **nadie lo ve** |

La última fila explica la mayoría de los casos UB que ninguna herramienta
detectó: ver [¿Coincide con el estándar?](resultados/dinamica.md#coincide-con-el-estándar).

## Pruébalo tú

```cpp
// prueba.cpp
#include <vector>
#include <cstdio>
int main() {
    std::vector<int> v = {1, 2, 3};
    auto it = v.begin();
    v.clear();
    std::printf("%d\n", *it);
}
```

```bash
g++ prueba.cpp -o normal && ./normal                      # imprime algo y "funciona"
g++ -D_GLIBCXX_DEBUG prueba.cpp -o debug && ./debug       # Debug Mode lo detiene
clang++ -fsanitize=address prueba.cpp -o asan && ./asan   # ASan probablemente NO lo ve
```

El tercero probablemente no diga nada, porque `clear()` no libera la memoria del
vector: es justo la diferencia entre las dos herramientas.
