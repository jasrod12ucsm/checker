# `std::vector::emplace_back`

Mutación: `c.emplace_back(1);`

- Iterador retenido: 🟡 `POLICY`
- Referencia/puntero retenido: 🟡 `POLICY`
- Casos `UB` detectados estáticamente: 0/0

**En palabras:** después de `c.emplace_back(1);` sobre un `std::vector`, un iterador guardado **puede** quedar inválido según el estado del contenedor (capacidad o factor de carga); una referencia o puntero guardado **puede** quedar inválido según el estado del contenedor (capacidad o factor de carga).

Mapa de los 12 casos. Cada celda muestra la respuesta correcta (etiqueta) y, debajo, lo que hizo el analizador estático de Clang. Clic para ir al caso. Ver [Cómo leer este libro](../../guia.md).

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_emplace_back_it_recto) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_emplace_back_it_guarda) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_emplace_back_it_bucle) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_emplace_back_it_llamada) |
| **referencia** | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_emplace_back_ref_recto) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_emplace_back_ref_guarda) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_emplace_back_ref_bucle) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_emplace_back_ref_llamada) |
| **puntero** | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_emplace_back_ptr_recto) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_emplace_back_ptr_guarda) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_emplace_back_ptr_bucle) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_emplace_back_ptr_llamada) |

## Handle: iterador

### f_vector_emplace_back_it_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_emplace_back_it_recto(std::vector<int>& c) {
  auto it = c.begin();
  c.emplace_back(1);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | 🛑 attempt to dereference a singular iterator | 🛑 heap-use-after-free |
| `preserve` | capacidad 512, con espacio para la mutación | sin detección | sin detección |

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
    iterator "this" @ 0x7ffd42f26ba0 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffd42f26c30
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
or<int>>::_M_realloc_insert<int>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int>>>, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:519:7
    #5 0x59db11dd39f0 in int& std::vector<int, std::allocator<int>>::emplace_back<int>(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:123:4
    #6 0x59db11cf01c0 in f_vector_emplace_back_it_recto(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:247:5
    #7 0x59db11d89b38 in main /work/test/runtime_runner.cpp:203:5
    #8 0x7a609fbba1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x7a609fbba28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x59db11bfd4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x59db11ce6d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x59db11de6c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x59db11de650f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x59db11de650f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x59db11dd4720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x59db11d74187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x59db11d89b2b in main /work/test/runtime_runner.cpp:202:26
    #7 0x7a609fbba1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x7a609fbba28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x59db11bfd4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:248:8 in f_vector_emplace_back_it_recto(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x76909eddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x76909eddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x76909eddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x76909eddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x76909eddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x76909ede0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x76909ede0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x76909ede0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x76909ede0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x76909ede0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x76909ede0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==103==ABORTING
````

</details>

### f_vector_emplace_back_it_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_emplace_back_it_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.emplace_back(1);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | 🛑 attempt to dereference a singular iterator | 🛑 heap-use-after-free |
| `preserve` | capacidad 512, con espacio para la mutación | sin detección | sin detección |

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
    iterator "this" @ 0x7ffe4ce710e0 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffe4ce711a0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
<int>>::_M_realloc_insert<int>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int>>>, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:519:7
    #5 0x5c1c2ed869f0 in int& std::vector<int, std::allocator<int>>::emplace_back<int>(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:123:4
    #6 0x5c1c2eca3718 in f_vector_emplace_back_it_guarda(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:259:5
    #7 0x5c1c2ed3ce24 in main /work/test/runtime_runner.cpp:213:5
    #8 0x7ed451b8a1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x7ed451b8a28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x5c1c2ebb04b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5c1c2ec99d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5c1c2ed99c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5c1c2ed9950f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5c1c2ed9950f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x5c1c2ed87720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x5c1c2ed27187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x5c1c2ed3ce17 in main /work/test/runtime_runner.cpp:212:26
    #7 0x7ed451b8a1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x7ed451b8a28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x5c1c2ebb04b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:260:8 in f_vector_emplace_back_it_guarda(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7b0450ddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b0450ddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b0450ddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b0450ddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b0450ddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b0450de0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7b0450de0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b0450de0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b0450de0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b0450de0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b0450de0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==110==ABORTING
````

</details>

### f_vector_emplace_back_it_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_emplace_back_it_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.emplace_back(1);
    sink(*it);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | 🛑 attempt to dereference a singular iterator | 🛑 heap-use-after-free |
| `preserve` | capacidad 512, con espacio para la mutación | sin detección | sin detección |

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
    iterator "this" @ 0x7ffdbb148430 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffdbb1484f0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
r<int>>::_M_realloc_insert<int>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int>>>, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:519:7
    #5 0x5a8a50abb9f0 in int& std::vector<int, std::allocator<int>>::emplace_back<int>(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:123:4
    #6 0x5a8a509d8d63 in f_vector_emplace_back_it_bucle(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:272:7
    #7 0x5a8a50a72110 in main /work/test/runtime_runner.cpp:223:5
    #8 0x7fa535e661c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x7fa535e6628a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x5a8a508e54b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5a8a509ced31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5a8a50acec77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5a8a50ace50f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5a8a50ace50f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x5a8a50abc720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x5a8a50a5c187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x5a8a50a72103 in main /work/test/runtime_runner.cpp:222:26
    #7 0x7fa535e661c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x7fa535e6628a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x5a8a508e54b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:273:10 in f_vector_emplace_back_it_bucle(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7bd5351dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd5351dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd5351dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd5351dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd5351dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bd5351e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7bd5351e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd5351e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd5351e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd5351e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd5351e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==117==ABORTING
````

</details>

### f_vector_emplace_back_it_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_emplace_back_it_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_vector_emplace_back(c);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | 🛑 attempt to dereference a singular iterator | 🛑 heap-use-after-free |
| `preserve` | capacidad 512, con espacio para la mutación | sin detección | sin detección |

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
    iterator "this" @ 0x7ffff8c43c10 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffff8c43cd0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:519:7
    #5 0x621b69d569f0 in int& std::vector<int, std::allocator<int>>::emplace_back<int>(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:123:4
    #6 0x621b69c6b486 in mutar_vector_emplace_back(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:16:57
    #7 0x621b69c7439c in f_vector_emplace_back_it_llamada(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:287:3
    #8 0x621b69d0d3fc in main /work/test/runtime_runner.cpp:233:5
    #9 0x7e275d8671c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x7e275d86728a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x621b69b804b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x621b69c69d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x621b69d69c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x621b69d6950f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x621b69d6950f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x621b69d57720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x621b69cf7187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x621b69d0d3ef in main /work/test/runtime_runner.cpp:232:26
    #7 0x7e275d8671c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x7e275d86728a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x621b69b804b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:288:8 in f_vector_emplace_back_it_llamada(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7a575cbdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a575cbdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a575cbdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a575cbdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a575cbdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7a575cbe0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7a575cbe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a575cbe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a575cbe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a575cbe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a575cbe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==124==ABORTING
````

</details>

## Handle: referencia

### f_vector_emplace_back_ref_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_emplace_back_ref_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.emplace_back(1);
  sink(h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | sin detección | 🛑 heap-use-after-free |
| `preserve` | capacidad 512, con espacio para la mutación | sin detección | sin detección |

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
<int>>::_M_realloc_insert<int>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int>>>, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:519:7
    #5 0x58f26b2509f0 in int& std::vector<int, std::allocator<int>>::emplace_back<int>(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:123:4
    #6 0x58f26b16e919 in f_vector_emplace_back_ref_recto(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:300:5
    #7 0x58f26b2076e8 in main /work/test/runtime_runner.cpp:243:5
    #8 0x7241b46141c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x7241b461428a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x58f26b07a4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x58f26b163d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x58f26b263c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x58f26b26350f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x58f26b26350f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x58f26b251720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x58f26b1f1187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x58f26b2076db in main /work/test/runtime_runner.cpp:242:26
    #7 0x7241b46141c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x7241b461428a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x58f26b07a4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:301:8 in f_vector_emplace_back_ref_recto(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6e71b39dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e71b39dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e71b39dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e71b39dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e71b39dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6e71b39e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x6e71b39e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e71b39e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e71b39e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e71b39e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e71b39e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==131==ABORTING
````

</details>

### f_vector_emplace_back_ref_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_emplace_back_ref_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.emplace_back(1);
  sink(h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | sin detección | 🛑 heap-use-after-free |
| `preserve` | capacidad 512, con espacio para la mutación | sin detección | sin detección |

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
nt>>::_M_realloc_insert<int>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int>>>, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:519:7
    #5 0x56d90fa639f0 in int& std::vector<int, std::allocator<int>>::emplace_back<int>(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:123:4
    #6 0x56d90f981e7b in f_vector_emplace_back_ref_guarda(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:314:5
    #7 0x56d90fa1a9d4 in main /work/test/runtime_runner.cpp:253:5
    #8 0x7cc2cc2c81c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x7cc2cc2c828a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x56d90f88d4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x56d90f976d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x56d90fa76c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x56d90fa7650f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x56d90fa7650f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x56d90fa64720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x56d90fa04187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x56d90fa1a9c7 in main /work/test/runtime_runner.cpp:252:26
    #7 0x7cc2cc2c81c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x7cc2cc2c828a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x56d90f88d4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:315:8 in f_vector_emplace_back_ref_guarda(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x78f2cb5dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x78f2cb5dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x78f2cb5dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x78f2cb5dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x78f2cb5dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x78f2cb5e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x78f2cb5e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x78f2cb5e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x78f2cb5e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x78f2cb5e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x78f2cb5e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==138==ABORTING
````

</details>

### f_vector_emplace_back_ref_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_emplace_back_ref_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.emplace_back(1);
    sink(h);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | 🛑 attempt to increment a singular iterator | 🛑 heap-use-after-free |
| `preserve` | capacidad 512, con espacio para la mutación | sin detección | sin detección |

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
    iterator "this" @ 0x7ffffeb03fe0 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffffeb040a0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
int>>::_M_realloc_insert<int>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int>>>, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:519:7
    #5 0x61abe675e9f0 in int& std::vector<int, std::allocator<int>>::emplace_back<int>(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:123:4
    #6 0x61abe667d4e6 in f_vector_emplace_back_ref_bucle(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:329:7
    #7 0x61abe6715cc0 in main /work/test/runtime_runner.cpp:263:5
    #8 0x7aa5a6d771c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x7aa5a6d7728a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x61abe65884b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x61abe6671d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x61abe6771c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x61abe677150f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x61abe677150f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x61abe675f720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x61abe66ff187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x61abe6715cb3 in main /work/test/runtime_runner.cpp:262:26
    #7 0x7aa5a6d771c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x7aa5a6d7728a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x61abe65884b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:330:10 in f_vector_emplace_back_ref_bucle(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x76d5a5fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x76d5a5fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x76d5a5fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x76d5a5fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x76d5a5fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x76d5a5fe0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x76d5a5fe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x76d5a5fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x76d5a5fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x76d5a5fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x76d5a5fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==145==ABORTING
````

</details>

### f_vector_emplace_back_ref_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_emplace_back_ref_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_vector_emplace_back(c);
  sink(h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | sin detección | 🛑 heap-use-after-free |
| `preserve` | capacidad 512, con espacio para la mutación | sin detección | sin detección |

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
c/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:519:7
    #5 0x64471c9e59f0 in int& std::vector<int, std::allocator<int>>::emplace_back<int>(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:123:4
    #6 0x64471c8fa486 in mutar_vector_emplace_back(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:16:57
    #7 0x64471c904b55 in f_vector_emplace_back_ref_llamada(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:346:3
    #8 0x64471c99cfac in main /work/test/runtime_runner.cpp:273:5
    #9 0x7610b009b1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x7610b009b28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x64471c80f4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x64471c8f8d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x64471c9f8c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x64471c9f850f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x64471c9f850f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x64471c9e6720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x64471c986187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x64471c99cf9f in main /work/test/runtime_runner.cpp:272:26
    #7 0x7610b009b1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x7610b009b28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x64471c80f4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:347:8 in f_vector_emplace_back_ref_llamada(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7240af3dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7240af3dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7240af3dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7240af3dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7240af3dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7240af3e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7240af3e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7240af3e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7240af3e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7240af3e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7240af3e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==152==ABORTING
````

</details>

## Handle: puntero

### f_vector_emplace_back_ptr_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_emplace_back_ptr_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.emplace_back(1);
  sink(*h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | sin detección | 🛑 heap-use-after-free |
| `preserve` | capacidad 512, con espacio para la mutación | sin detección | sin detección |

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
<int>>::_M_realloc_insert<int>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int>>>, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:519:7
    #5 0x648a25b7f9f0 in int& std::vector<int, std::allocator<int>>::emplace_back<int>(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:123:4
    #6 0x648a25a9f086 in f_vector_emplace_back_ptr_recto(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:360:5
    #7 0x648a25b37298 in main /work/test/runtime_runner.cpp:283:5
    #8 0x7f32d5f9a1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x7f32d5f9a28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x648a259a94b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x648a25a92d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x648a25b92c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x648a25b9250f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x648a25b9250f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x648a25b80720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x648a25b20187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x648a25b3728b in main /work/test/runtime_runner.cpp:282:26
    #7 0x7f32d5f9a1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x7f32d5f9a28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x648a259a94b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:361:8 in f_vector_emplace_back_ptr_recto(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7b62d51dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b62d51dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b62d51dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b62d51dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b62d51dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b62d51e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7b62d51e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b62d51e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b62d51e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b62d51e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b62d51e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==159==ABORTING
````

</details>

### f_vector_emplace_back_ptr_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_emplace_back_ptr_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.emplace_back(1);
  sink(*h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | sin detección | 🛑 heap-use-after-free |
| `preserve` | capacidad 512, con espacio para la mutación | sin detección | sin detección |

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
nt>>::_M_realloc_insert<int>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int>>>, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:519:7
    #5 0x606d4730e9f0 in int& std::vector<int, std::allocator<int>>::emplace_back<int>(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:123:4
    #6 0x606d4722e5e8 in f_vector_emplace_back_ptr_guarda(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:374:5
    #7 0x606d472c6584 in main /work/test/runtime_runner.cpp:293:5
    #8 0x7cdf6b4f41c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x7cdf6b4f428a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x606d471384b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x606d47221d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x606d47321c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x606d4732150f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x606d4732150f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x606d4730f720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x606d472af187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x606d472c6577 in main /work/test/runtime_runner.cpp:292:26
    #7 0x7cdf6b4f41c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x7cdf6b4f428a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x606d471384b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:375:8 in f_vector_emplace_back_ptr_guarda(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x790f6a7dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x790f6a7dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x790f6a7dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x790f6a7dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x790f6a7dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x790f6a7e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x790f6a7e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x790f6a7e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x790f6a7e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x790f6a7e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x790f6a7e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==166==ABORTING
````

</details>

### f_vector_emplace_back_ptr_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_emplace_back_ptr_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.emplace_back(1);
    sink(*h);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | 🛑 attempt to increment a singular iterator | 🛑 heap-use-after-free |
| `preserve` | capacidad 512, con espacio para la mutación | sin detección | sin detección |

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
    iterator "this" @ 0x7ffd393b8d00 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffd393b8dc0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
int>>::_M_realloc_insert<int>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int>>>, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:519:7
    #5 0x5c5c72a249f0 in int& std::vector<int, std::allocator<int>>::emplace_back<int>(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:123:4
    #6 0x5c5c72944c33 in f_vector_emplace_back_ptr_bucle(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:389:7
    #7 0x5c5c729dc870 in main /work/test/runtime_runner.cpp:303:5
    #8 0x7bd1a90021c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x7bd1a900228a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x5c5c7284e4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5c5c72937d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5c5c72a37c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5c5c72a3750f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5c5c72a3750f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x5c5c72a25720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x5c5c729c5187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x5c5c729dc863 in main /work/test/runtime_runner.cpp:302:26
    #7 0x7bd1a90021c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x7bd1a900228a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x5c5c7284e4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:390:10 in f_vector_emplace_back_ptr_bucle(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7801a83dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7801a83dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7801a83dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7801a83dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7801a83dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7801a83e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7801a83e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7801a83e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7801a83e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7801a83e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7801a83e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==173==ABORTING
````

</details>

### f_vector_emplace_back_ptr_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_emplace_back_ptr_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_vector_emplace_back(c);
  sink(*h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | sin detección | 🛑 heap-use-after-free |
| `preserve` | capacidad 512, con espacio para la mutación | sin detección | sin detección |

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
c/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:519:7
    #5 0x63ecddf289f0 in int& std::vector<int, std::allocator<int>>::emplace_back<int>(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:123:4
    #6 0x63ecdde3d486 in mutar_vector_emplace_back(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:16:57
    #7 0x63ecdde49289 in f_vector_emplace_back_ptr_llamada(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:406:3
    #8 0x63ecddee0b5c in main /work/test/runtime_runner.cpp:313:5
    #9 0x72c9e81be1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x72c9e81be28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x63ecddd524b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x63ecdde3bd31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x63ecddf3bc77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x63ecddf3b50f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x63ecddf3b50f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x63ecddf29720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x63ecddec9187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x63ecddee0b4f in main /work/test/runtime_runner.cpp:312:26
    #7 0x72c9e81be1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x72c9e81be28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x63ecddd524b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:407:8 in f_vector_emplace_back_ptr_llamada(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6ef9e73dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6ef9e73dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6ef9e73dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6ef9e73dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6ef9e73dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6ef9e73e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x6ef9e73e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6ef9e73e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6ef9e73e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6ef9e73e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6ef9e73e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==180==ABORTING
````

</details>
