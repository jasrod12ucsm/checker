# `std::vector::resize_grow`

Mutación: `c.resize(c.size()+100);`

- Iterador retenido: 🟡 `POLICY`
- Referencia/puntero retenido: 🟡 `POLICY`
- Casos `UB` detectados estáticamente: 0/0

**En palabras:** después de `c.resize(c.size()+100);` sobre un `std::vector`, un iterador guardado **puede** quedar inválido según el estado del contenedor (capacidad o factor de carga); una referencia o puntero guardado **puede** quedar inválido según el estado del contenedor (capacidad o factor de carga).

Mapa de los 12 casos. Cada celda muestra la respuesta correcta (etiqueta) y, debajo, lo que hizo el analizador estático de Clang. Clic para ir al caso. Ver [Cómo leer este libro](../../guia.md).

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_resize_grow_it_recto) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_resize_grow_it_guarda) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_resize_grow_it_bucle) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_resize_grow_it_llamada) |
| **referencia** | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_resize_grow_ref_recto) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_resize_grow_ref_guarda) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_resize_grow_ref_bucle) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_resize_grow_ref_llamada) |
| **puntero** | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_resize_grow_ptr_recto) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_resize_grow_ptr_guarda) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_resize_grow_ptr_bucle) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_resize_grow_ptr_llamada) |

## Handle: iterador

### f_vector_resize_grow_it_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_resize_grow_it_recto(std::vector<int>& c) {
  auto it = c.begin();
  c.resize(c.size()+100);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | 🛑 attempt to dereference a singular iterator | 🛑 heap-use-after-free |
| `preserve` | capacidad 512, suficiente para size()+100 tres veces | sin detección | sin detección |

<details>
<summary>stderr libstdc++ Debug · <code>force</code></summary>

````text
/usr/include/c++/13/debug/safe_iterator.h:298:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::reference 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator*() 
    const [with _Iterator = gnu_cxx::normal_iterator<int*, std::vector<int, 
    std::allocator<int> > >; _Sequence = std::debug::vector<int>; _Category 
    = std::forward_iterator_tag; reference = int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffe29b9f680 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffe29b9f710
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
/bits/stl_vector.h:390:4
    #4 0x647b7da0ce38 in std::vector<int, std::allocator<int>>::_M_default_append(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:703:8
    #5 0x647b7d9f632d in std::vector<int, std::allocator<int>>::resize(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1016:4
    #6 0x647b7d9225bc in f_vector_resize_grow_it_recto(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:831:5
    #7 0x647b7d9b32f0 in main /work/test/runtime_runner.cpp:623:5
    #8 0x7dd11dd961c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x7dd11dd9628a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x647b7d81f4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x647b7d908d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x647b7da08c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x647b7da0850f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x647b7da0850f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x647b7d9f6720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x647b7d996187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x647b7d9b32e3 in main /work/test/runtime_runner.cpp:622:26
    #7 0x7dd11dd961c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x7dd11dd9628a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x647b7d81f4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:832:8 in f_vector_resize_grow_it_recto(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7a011cfdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a011cfdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a011cfdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a011cfdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a011cfdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7a011cfe0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7a011cfe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a011cfe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a011cfe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a011cfe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a011cfe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==346==ABORTING
````

</details>

### f_vector_resize_grow_it_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_resize_grow_it_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.resize(c.size()+100);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | 🛑 attempt to dereference a singular iterator | 🛑 heap-use-after-free |
| `preserve` | capacidad 512, suficiente para size()+100 tres veces | sin detección | sin detección |

<details>
<summary>stderr libstdc++ Debug · <code>force</code></summary>

````text
/usr/include/c++/13/debug/safe_iterator.h:298:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::reference 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator*() 
    const [with _Iterator = gnu_cxx::normal_iterator<int*, std::vector<int, 
    std::allocator<int> > >; _Sequence = std::debug::vector<int>; _Category 
    = std::forward_iterator_tag; reference = int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fff1c7a6080 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7fff1c7a6140
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
its/stl_vector.h:390:4
    #4 0x6482d965be38 in std::vector<int, std::allocator<int>>::_M_default_append(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:703:8
    #5 0x6482d964532d in std::vector<int, std::allocator<int>>::resize(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1016:4
    #6 0x6482d9571867 in f_vector_resize_grow_it_guarda(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:837:5
    #7 0x6482d9602466 in main /work/test/runtime_runner.cpp:628:5
    #8 0x7b23e16f91c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x7b23e16f928a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x6482d946e4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x6482d9557d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x6482d9657c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x6482d965750f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x6482d965750f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x6482d9645720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x6482d95e5187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x6482d9602459 in main /work/test/runtime_runner.cpp:627:26
    #7 0x7b23e16f91c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x7b23e16f928a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x6482d946e4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:838:8 in f_vector_resize_grow_it_guarda(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7753e09dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7753e09dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7753e09dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7753e09dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7753e09dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7753e09e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7753e09e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7753e09e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7753e09e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7753e09e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7753e09e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==351==ABORTING
````

</details>

### f_vector_resize_grow_it_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_resize_grow_it_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.resize(c.size()+100);
    sink(*it);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | 🛑 attempt to dereference a singular iterator | 🛑 heap-use-after-free |
| `preserve` | capacidad 512, suficiente para size()+100 tres veces | sin detección | sin detección |

<details>
<summary>stderr libstdc++ Debug · <code>force</code></summary>

````text
/usr/include/c++/13/debug/safe_iterator.h:298:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::reference 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator*() 
    const [with _Iterator = gnu_cxx::normal_iterator<int*, std::vector<int, 
    std::allocator<int> > >; _Sequence = std::debug::vector<int>; _Category 
    = std::forward_iterator_tag; reference = int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fff51445770 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7fff51445830
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
bits/stl_vector.h:390:4
    #4 0x5d16294f9e38 in std::vector<int, std::allocator<int>>::_M_default_append(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:703:8
    #5 0x5d16294e332d in std::vector<int, std::allocator<int>>::resize(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1016:4
    #6 0x5d162940fb92 in f_vector_resize_grow_it_bucle(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:843:7
    #7 0x5d16294a05dc in main /work/test/runtime_runner.cpp:633:5
    #8 0x796b04e731c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x796b04e7328a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x5d162930c4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5d16293f5d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5d16294f5c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5d16294f550f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5d16294f550f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x5d16294e3720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x5d1629483187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x5d16294a05cf in main /work/test/runtime_runner.cpp:632:26
    #7 0x796b04e731c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x796b04e7328a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x5d162930c4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:844:10 in f_vector_resize_grow_it_bucle(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x759b041dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x759b041dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x759b041dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x759b041dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x759b041dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x759b041e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x759b041e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x759b041e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x759b041e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x759b041e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x759b041e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==356==ABORTING
````

</details>

### f_vector_resize_grow_it_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_resize_grow_it_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_vector_resize_grow(c);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | 🛑 attempt to dereference a singular iterator | 🛑 heap-use-after-free |
| `preserve` | capacidad 512, suficiente para size()+100 tres veces | sin detección | sin detección |

<details>
<summary>stderr libstdc++ Debug · <code>force</code></summary>

````text
/usr/include/c++/13/debug/safe_iterator.h:298:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::reference 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator*() 
    const [with _Iterator = gnu_cxx::normal_iterator<int*, std::vector<int, 
    std::allocator<int> > >; _Sequence = std::debug::vector<int>; _Category 
    = std::forward_iterator_tag; reference = int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffd6baaed20 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffd6baaede0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:703:8
    #5 0x5ed16ed2932d in std::vector<int, std::allocator<int>>::resize(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1016:4
    #6 0x5ed16ec3db2e in mutar_vector_resize_grow(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:21:56
    #7 0x5ed16ec55e1c in f_vector_resize_grow_it_llamada(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:850:3
    #8 0x5ed16ece6752 in main /work/test/runtime_runner.cpp:638:5
    #9 0x78d7d2a4f1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x78d7d2a4f28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x5ed16eb524b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5ed16ec3bd31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5ed16ed3bc77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5ed16ed3b50f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5ed16ed3b50f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x5ed16ed29720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x5ed16ecc9187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x5ed16ece6745 in main /work/test/runtime_runner.cpp:637:26
    #7 0x78d7d2a4f1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x78d7d2a4f28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x5ed16eb524b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:851:8 in f_vector_resize_grow_it_llamada(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7507d1ddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7507d1ddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7507d1ddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7507d1ddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7507d1ddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7507d1de0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7507d1de0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7507d1de0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7507d1de0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7507d1de0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7507d1de0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==361==ABORTING
````

</details>

## Handle: referencia

### f_vector_resize_grow_ref_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_resize_grow_ref_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.resize(c.size()+100);
  sink(h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | sin detección | 🛑 heap-use-after-free |
| `preserve` | capacidad 512, suficiente para size()+100 tres veces | sin detección | sin detección |

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
its/stl_vector.h:390:4
    #4 0x62bd60e5fe38 in std::vector<int, std::allocator<int>>::_M_default_append(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:703:8
    #5 0x62bd60e4932d in std::vector<int, std::allocator<int>>::resize(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1016:4
    #6 0x62bd60d760a5 in f_vector_resize_grow_ref_recto(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:856:5
    #7 0x62bd60e068c8 in main /work/test/runtime_runner.cpp:643:5
    #8 0x78aafcd9a1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x78aafcd9a28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x62bd60c724b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x62bd60d5bd31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x62bd60e5bc77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x62bd60e5b50f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x62bd60e5b50f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x62bd60e49720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x62bd60de9187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x62bd60e068bb in main /work/test/runtime_runner.cpp:642:26
    #7 0x78aafcd9a1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x78aafcd9a28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x62bd60c724b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:857:8 in f_vector_resize_grow_ref_recto(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x74dafbfdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x74dafbfdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x74dafbfdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x74dafbfdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x74dafbfdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x74dafbfe0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x74dafbfe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x74dafbfe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x74dafbfe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x74dafbfe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x74dafbfe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==366==ABORTING
````

</details>

### f_vector_resize_grow_ref_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_resize_grow_ref_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.resize(c.size()+100);
  sink(h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | sin detección | 🛑 heap-use-after-free |
| `preserve` | capacidad 512, suficiente para size()+100 tres veces | sin detección | sin detección |

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
s/stl_vector.h:390:4
    #4 0x61b674950e38 in std::vector<int, std::allocator<int>>::_M_default_append(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:703:8
    #5 0x61b67493a32d in std::vector<int, std::allocator<int>>::resize(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1016:4
    #6 0x61b67486735a in f_vector_resize_grow_ref_guarda(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:863:5
    #7 0x61b6748f7a3e in main /work/test/runtime_runner.cpp:648:5
    #8 0x7fb6a92031c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x7fb6a920328a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x61b6747634b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x61b67484cd31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x61b67494cc77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x61b67494c50f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x61b67494c50f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x61b67493a720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x61b6748da187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x61b6748f7a31 in main /work/test/runtime_runner.cpp:647:26
    #7 0x7fb6a92031c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x7fb6a920328a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x61b6747634b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:864:8 in f_vector_resize_grow_ref_guarda(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7be6a85dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7be6a85dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7be6a85dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7be6a85dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7be6a85dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7be6a85e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7be6a85e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7be6a85e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7be6a85e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7be6a85e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7be6a85e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==371==ABORTING
````

</details>

### f_vector_resize_grow_ref_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_resize_grow_ref_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.resize(c.size()+100);
    sink(h);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | 🛑 attempt to increment a singular iterator | 🛑 heap-use-after-free |
| `preserve` | capacidad 512, suficiente para size()+100 tres veces | sin detección | sin detección |

<details>
<summary>stderr libstdc++ Debug · <code>force</code></summary>

````text
/usr/include/c++/13/debug/safe_iterator.h:326:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>& 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator++() 
    [with _Iterator = gnu_cxx::normal_iterator<int*, std::vector<int, 
    std::allocator<int> > >; _Sequence = std::debug::vector<int>; _Category 
    = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fff84946570 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7fff84946630
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
ts/stl_vector.h:390:4
    #4 0x5fb2b81ede38 in std::vector<int, std::allocator<int>>::_M_default_append(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:703:8
    #5 0x5fb2b81d732d in std::vector<int, std::allocator<int>>::resize(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1016:4
    #6 0x5fb2b8104695 in f_vector_resize_grow_ref_bucle(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:870:7
    #7 0x5fb2b8194bb4 in main /work/test/runtime_runner.cpp:653:5
    #8 0x73db9cd901c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x73db9cd9028a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x5fb2b80004b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5fb2b80e9d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5fb2b81e9c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5fb2b81e950f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5fb2b81e950f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x5fb2b81d7720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x5fb2b8177187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x5fb2b8194ba7 in main /work/test/runtime_runner.cpp:652:26
    #7 0x73db9cd901c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x73db9cd9028a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x5fb2b80004b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:871:10 in f_vector_resize_grow_ref_bucle(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x700b9bfdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x700b9bfdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x700b9bfdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x700b9bfdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x700b9bfdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x700b9bfe0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x700b9bfe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x700b9bfe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x700b9bfe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x700b9bfe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x700b9bfe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==376==ABORTING
````

</details>

### f_vector_resize_grow_ref_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_resize_grow_ref_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_vector_resize_grow(c);
  sink(h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | sin detección | 🛑 heap-use-after-free |
| `preserve` | capacidad 512, suficiente para size()+100 tres veces | sin detección | sin detección |

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
r/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:703:8
    #5 0x650cb14d732d in std::vector<int, std::allocator<int>>::resize(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1016:4
    #6 0x650cb13ebb2e in mutar_vector_resize_grow(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:21:56
    #7 0x650cb1404935 in f_vector_resize_grow_ref_llamada(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:878:3
    #8 0x650cb1494d2a in main /work/test/runtime_runner.cpp:658:5
    #9 0x78a2cb3d01c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x78a2cb3d028a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x650cb13004b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x650cb13e9d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x650cb14e9c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x650cb14e950f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x650cb14e950f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x650cb14d7720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x650cb1477187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x650cb1494d1d in main /work/test/runtime_runner.cpp:657:26
    #7 0x78a2cb3d01c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x78a2cb3d028a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x650cb13004b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:879:8 in f_vector_resize_grow_ref_llamada(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x74d2ca7dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x74d2ca7dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x74d2ca7dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x74d2ca7dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x74d2ca7dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x74d2ca7e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x74d2ca7e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x74d2ca7e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x74d2ca7e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x74d2ca7e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x74d2ca7e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==381==ABORTING
````

</details>

## Handle: puntero

### f_vector_resize_grow_ptr_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_resize_grow_ptr_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.resize(c.size()+100);
  sink(*h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | sin detección | 🛑 heap-use-after-free |
| `preserve` | capacidad 512, suficiente para size()+100 tres veces | sin detección | sin detección |

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
its/stl_vector.h:390:4
    #4 0x5bfb2b30ee38 in std::vector<int, std::allocator<int>>::_M_default_append(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:703:8
    #5 0x5bfb2b2f832d in std::vector<int, std::allocator<int>>::resize(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1016:4
    #6 0x5bfb2b225b62 in f_vector_resize_grow_ptr_recto(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:884:5
    #7 0x5bfb2b2b5ea0 in main /work/test/runtime_runner.cpp:663:5
    #8 0x7b6b532891c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x7b6b5328928a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x5bfb2b1214b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5bfb2b20ad31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5bfb2b30ac77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5bfb2b30a50f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5bfb2b30a50f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x5bfb2b2f8720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x5bfb2b298187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x5bfb2b2b5e93 in main /work/test/runtime_runner.cpp:662:26
    #7 0x7b6b532891c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x7b6b5328928a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x5bfb2b1214b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:885:8 in f_vector_resize_grow_ptr_recto(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x779b525dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x779b525dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x779b525dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x779b525dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x779b525dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x779b525e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x779b525e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x779b525e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x779b525e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x779b525e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x779b525e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==386==ABORTING
````

</details>

### f_vector_resize_grow_ptr_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_resize_grow_ptr_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.resize(c.size()+100);
  sink(*h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | sin detección | 🛑 heap-use-after-free |
| `preserve` | capacidad 512, suficiente para size()+100 tres veces | sin detección | sin detección |

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
s/stl_vector.h:390:4
    #4 0x5587c5314e38 in std::vector<int, std::allocator<int>>::_M_default_append(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:703:8
    #5 0x5587c52fe32d in std::vector<int, std::allocator<int>>::resize(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1016:4
    #6 0x5587c522be17 in f_vector_resize_grow_ptr_guarda(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:891:5
    #7 0x5587c52bc016 in main /work/test/runtime_runner.cpp:668:5
    #8 0x71101d88f1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x71101d88f28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x5587c51274b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5587c5210d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5587c5310c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5587c531050f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5587c531050f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x5587c52fe720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x5587c529e187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x5587c52bc009 in main /work/test/runtime_runner.cpp:667:26
    #7 0x71101d88f1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x71101d88f28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x5587c51274b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:892:8 in f_vector_resize_grow_ptr_guarda(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6d401cbdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d401cbdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d401cbdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d401cbdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d401cbdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6d401cbe0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x6d401cbe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d401cbe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d401cbe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d401cbe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d401cbe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==391==ABORTING
````

</details>

### f_vector_resize_grow_ptr_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_resize_grow_ptr_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.resize(c.size()+100);
    sink(*h);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | 🛑 attempt to increment a singular iterator | 🛑 heap-use-after-free |
| `preserve` | capacidad 512, suficiente para size()+100 tres veces | sin detección | sin detección |

<details>
<summary>stderr libstdc++ Debug · <code>force</code></summary>

````text
/usr/include/c++/13/debug/safe_iterator.h:326:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>& 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator++() 
    [with _Iterator = gnu_cxx::normal_iterator<int*, std::vector<int, 
    std::allocator<int> > >; _Sequence = std::debug::vector<int>; _Category 
    = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fff970b6720 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7fff970b67e0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
ts/stl_vector.h:390:4
    #4 0x5706250c4e38 in std::vector<int, std::allocator<int>>::_M_default_append(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:703:8
    #5 0x5706250ae32d in std::vector<int, std::allocator<int>>::resize(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1016:4
    #6 0x570624fdc152 in f_vector_resize_grow_ptr_bucle(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:898:7
    #7 0x57062506c18c in main /work/test/runtime_runner.cpp:673:5
    #8 0x79cafab001c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x79cafab0028a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x570624ed74b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x570624fc0d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5706250c0c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5706250c050f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5706250c050f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x5706250ae720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x57062504e187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x57062506c17f in main /work/test/runtime_runner.cpp:672:26
    #7 0x79cafab001c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x79cafab0028a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x570624ed74b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:899:10 in f_vector_resize_grow_ptr_bucle(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x75faf9ddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75faf9ddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75faf9ddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75faf9ddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75faf9ddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x75faf9de0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x75faf9de0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x75faf9de0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x75faf9de0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x75faf9de0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x75faf9de0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==396==ABORTING
````

</details>

### f_vector_resize_grow_ptr_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_resize_grow_ptr_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_vector_resize_grow(c);
  sink(*h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | sin detección | 🛑 heap-use-after-free |
| `preserve` | capacidad 512, suficiente para size()+100 tres veces | sin detección | sin detección |

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
r/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:703:8
    #5 0x5f918e14632d in std::vector<int, std::allocator<int>>::resize(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1016:4
    #6 0x5f918e05ab2e in mutar_vector_resize_grow(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:21:56
    #7 0x5f918e0743e9 in f_vector_resize_grow_ptr_llamada(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:906:3
    #8 0x5f918e104302 in main /work/test/runtime_runner.cpp:678:5
    #9 0x7d426b6c71c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x7d426b6c728a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x5f918df6f4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5f918e058d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5f918e158c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5f918e15850f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5f918e15850f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x5f918e146720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x5f918e0e6187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x5f918e1042f5 in main /work/test/runtime_runner.cpp:677:26
    #7 0x7d426b6c71c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x7d426b6c728a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x5f918df6f4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:907:8 in f_vector_resize_grow_ptr_llamada(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x79726a9dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x79726a9dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x79726a9dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x79726a9dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x79726a9dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x79726a9e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x79726a9e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x79726a9e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x79726a9e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x79726a9e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x79726a9e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==401==ABORTING
````

</details>
