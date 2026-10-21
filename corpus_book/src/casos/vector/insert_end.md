# `std::vector::insert_end`

Mutación: `c.insert(c.end(),1);`

- Iterador retenido: 🟡 `POLICY`
- Referencia/puntero retenido: 🟡 `POLICY`
- Casos `UB` detectados estáticamente: 0/0

**En palabras:** después de `c.insert(c.end(),1);` sobre un `std::vector`, un iterador guardado **puede** quedar inválido según el estado del contenedor (capacidad o factor de carga); una referencia o puntero guardado **puede** quedar inválido según el estado del contenedor (capacidad o factor de carga).

Mapa de los 12 casos. Cada celda muestra la respuesta correcta (etiqueta) y, debajo, lo que hizo el analizador estático de Clang. Clic para ir al caso. Ver [Cómo leer este libro](../../guia.md).

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_insert_end_it_recto) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_insert_end_it_guarda) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_insert_end_it_bucle) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_insert_end_it_llamada) |
| **referencia** | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_insert_end_ref_recto) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_insert_end_ref_guarda) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_insert_end_ref_bucle) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_insert_end_ref_llamada) |
| **puntero** | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_insert_end_ptr_recto) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_insert_end_ptr_guarda) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_insert_end_ptr_bucle) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_insert_end_ptr_llamada) |

## Handle: iterador

### f_vector_insert_end_it_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_insert_end_it_recto(std::vector<int>& c) {
  auto it = c.begin();
  c.insert(c.end(),1);
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
    iterator "this" @ 0x7ffe703683c0 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffe703684e0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
, std::vector<int, std::allocator<int>>>, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:372:2
    #6 0x5d4df0aaead6 in std::vector<int, std::allocator<int>>::insert(__gnu_cxx::__normal_iterator<int const*, std::vector<int, std::allocator<int>>>, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1394:16
    #7 0x5d4df09d1f32 in f_vector_insert_end_it_recto(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:499:5
    #8 0x5d4df0a67fd0 in main /work/test/runtime_runner.cpp:383:5
    #9 0x78d508aa41c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x78d508aa428a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x5d4df08d84b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5d4df09c1d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5d4df0ac1c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5d4df0ac150f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5d4df0ac150f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x5d4df0aaf720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x5d4df0a4f187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x5d4df0a67fc3 in main /work/test/runtime_runner.cpp:382:26
    #7 0x78d508aa41c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x78d508aa428a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x5d4df08d84b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:500:8 in f_vector_insert_end_it_recto(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x750507ddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x750507ddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x750507ddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x750507ddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x750507ddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x750507de0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x750507de0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x750507de0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x750507de0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x750507de0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x750507de0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==214==ABORTING
````

</details>

### f_vector_insert_end_it_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_insert_end_it_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.insert(c.end(),1);
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
    iterator "this" @ 0x7fffe35be130 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7fffe35be250
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
std::vector<int, std::allocator<int>>>, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:372:2
    #6 0x623fec6e0ad6 in std::vector<int, std::allocator<int>>::insert(__gnu_cxx::__normal_iterator<int const*, std::vector<int, std::allocator<int>>>, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1394:16
    #7 0x623fec6045f4 in f_vector_insert_end_it_guarda(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:511:5
    #8 0x623fec69a2bc in main /work/test/runtime_runner.cpp:393:5
    #9 0x7b06b7d171c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x7b06b7d1728a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x623fec50a4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x623fec5f3d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x623fec6f3c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x623fec6f350f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x623fec6f350f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x623fec6e1720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x623fec681187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x623fec69a2af in main /work/test/runtime_runner.cpp:392:26
    #7 0x7b06b7d171c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x7b06b7d1728a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x623fec50a4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:512:8 in f_vector_insert_end_it_guarda(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7736b6fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7736b6fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7736b6fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7736b6fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7736b6fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7736b6fe0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7736b6fe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7736b6fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7736b6fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7736b6fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7736b6fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==221==ABORTING
````

</details>

### f_vector_insert_end_it_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_insert_end_it_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.insert(c.end(),1);
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
    iterator "this" @ 0x7ffe5496f2a0 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffe5496f3c0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
 std::vector<int, std::allocator<int>>>, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:372:2
    #6 0x57df16039ad6 in std::vector<int, std::allocator<int>>::insert(__gnu_cxx::__normal_iterator<int const*, std::vector<int, std::allocator<int>>>, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1394:16
    #7 0x57df15f5dddd in f_vector_insert_end_it_bucle(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:524:7
    #8 0x57df15ff35a8 in main /work/test/runtime_runner.cpp:403:5
    #9 0x79474e7e81c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x79474e7e828a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x57df15e634b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x57df15f4cd31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x57df1604cc77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x57df1604c50f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x57df1604c50f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x57df1603a720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x57df15fda187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x57df15ff359b in main /work/test/runtime_runner.cpp:402:26
    #7 0x79474e7e81c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x79474e7e828a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x57df15e634b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:525:10 in f_vector_insert_end_it_bucle(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x75774dbdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75774dbdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75774dbdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75774dbdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75774dbdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x75774dbe0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x75774dbe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x75774dbe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x75774dbe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x75774dbe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x75774dbe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==228==ABORTING
````

</details>

### f_vector_insert_end_it_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_insert_end_it_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_vector_insert_end(c);
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
    iterator "this" @ 0x7ffd34418d50 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffd34418e10
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
cc:372:2
    #6 0x5aee97d3fad6 in std::vector<int, std::allocator<int>>::insert(__gnu_cxx::__normal_iterator<int const*, std::vector<int, std::allocator<int>>>, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1394:16
    #7 0x5aee97c54830 in mutar_vector_insert_end(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:18:55
    #8 0x5aee97c644fc in f_vector_insert_end_it_llamada(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:539:3
    #9 0x5aee97cf9894 in main /work/test/runtime_runner.cpp:413:5
    #10 0x7097740921c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x70977409228a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x5aee97b694b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5aee97c52d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5aee97d52c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5aee97d5250f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5aee97d5250f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x5aee97d40720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x5aee97ce0187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x5aee97cf9887 in main /work/test/runtime_runner.cpp:412:26
    #7 0x7097740921c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x70977409228a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x5aee97b694b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:540:8 in f_vector_insert_end_it_llamada(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6cc7733dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6cc7733dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6cc7733dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6cc7733dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6cc7733dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6cc7733e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x6cc7733e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6cc7733e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6cc7733e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6cc7733e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6cc7733e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==235==ABORTING
````

</details>

## Handle: referencia

### f_vector_insert_end_ref_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_insert_end_ref_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.insert(c.end(),1);
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
std::vector<int, std::allocator<int>>>, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:372:2
    #6 0x651bbb2ffad6 in std::vector<int, std::allocator<int>>::insert(__gnu_cxx::__normal_iterator<int const*, std::vector<int, std::allocator<int>>>, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1394:16
    #7 0x651bbb224afe in f_vector_insert_end_ref_recto(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:552:5
    #8 0x651bbb2b9b80 in main /work/test/runtime_runner.cpp:423:5
    #9 0x7d3ef7c9c1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x7d3ef7c9c28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x651bbb1294b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x651bbb212d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x651bbb312c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x651bbb31250f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x651bbb31250f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x651bbb300720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x651bbb2a0187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x651bbb2b9b73 in main /work/test/runtime_runner.cpp:422:26
    #7 0x7d3ef7c9c1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x7d3ef7c9c28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x651bbb1294b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:553:8 in f_vector_insert_end_ref_recto(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x796ef6fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x796ef6fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x796ef6fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x796ef6fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x796ef6fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x796ef6fe0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x796ef6fe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x796ef6fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x796ef6fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x796ef6fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x796ef6fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==242==ABORTING
````

</details>

### f_vector_insert_end_ref_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_insert_end_ref_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.insert(c.end(),1);
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
d::vector<int, std::allocator<int>>>, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:372:2
    #6 0x5a302adffad6 in std::vector<int, std::allocator<int>>::insert(__gnu_cxx::__normal_iterator<int const*, std::vector<int, std::allocator<int>>>, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1394:16
    #7 0x5a302ad25225 in f_vector_insert_end_ref_guarda(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:566:5
    #8 0x5a302adb9e6c in main /work/test/runtime_runner.cpp:433:5
    #9 0x7b16c33f51c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x7b16c33f528a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x5a302ac294b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5a302ad12d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5a302ae12c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5a302ae1250f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5a302ae1250f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x5a302ae00720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x5a302ada0187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x5a302adb9e5f in main /work/test/runtime_runner.cpp:432:26
    #7 0x7b16c33f51c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x7b16c33f528a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x5a302ac294b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:567:8 in f_vector_insert_end_ref_guarda(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7746c27dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7746c27dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7746c27dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7746c27dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7746c27dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7746c27e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7746c27e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7746c27e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7746c27e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7746c27e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7746c27e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==249==ABORTING
````

</details>

### f_vector_insert_end_ref_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_insert_end_ref_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.insert(c.end(),1);
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
    iterator "this" @ 0x7ffda53c2a40 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffda53c2b60
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
td::vector<int, std::allocator<int>>>, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:372:2
    #6 0x5720208a0ad6 in std::vector<int, std::allocator<int>>::insert(__gnu_cxx::__normal_iterator<int const*, std::vector<int, std::allocator<int>>>, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1394:16
    #7 0x5720207c6a30 in f_vector_insert_end_ref_bucle(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:581:7
    #8 0x57202085b158 in main /work/test/runtime_runner.cpp:443:5
    #9 0x7dd61c7871c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x7dd61c78728a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x5720206ca4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5720207b3d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5720208b3c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5720208b350f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5720208b350f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x5720208a1720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x572020841187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x57202085b14b in main /work/test/runtime_runner.cpp:442:26
    #7 0x7dd61c7871c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x7dd61c78728a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x5720206ca4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:582:10 in f_vector_insert_end_ref_bucle(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7a061b9dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a061b9dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a061b9dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a061b9dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a061b9dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7a061b9e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7a061b9e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a061b9e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a061b9e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a061b9e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a061b9e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==256==ABORTING
````

</details>

### f_vector_insert_end_ref_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_insert_end_ref_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_vector_insert_end(c);
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
:372:2
    #6 0x637f24863ad6 in std::vector<int, std::allocator<int>>::insert(__gnu_cxx::__normal_iterator<int const*, std::vector<int, std::allocator<int>>>, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1394:16
    #7 0x637f24778830 in mutar_vector_insert_end(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:18:55
    #8 0x637f2478a1b5 in f_vector_insert_end_ref_llamada(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:598:3
    #9 0x637f2481e444 in main /work/test/runtime_runner.cpp:453:5
    #10 0x7c7a1e3f71c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x7c7a1e3f728a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x637f2468d4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x637f24776d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x637f24876c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x637f2487650f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x637f2487650f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x637f24864720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x637f24804187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x637f2481e437 in main /work/test/runtime_runner.cpp:452:26
    #7 0x7c7a1e3f71c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x7c7a1e3f728a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x637f2468d4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:599:8 in f_vector_insert_end_ref_llamada(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x78aa1d7dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x78aa1d7dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x78aa1d7dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x78aa1d7dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x78aa1d7dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x78aa1d7e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x78aa1d7e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x78aa1d7e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x78aa1d7e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x78aa1d7e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x78aa1d7e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==263==ABORTING
````

</details>

## Handle: puntero

### f_vector_insert_end_ptr_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_insert_end_ptr_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.insert(c.end(),1);
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
std::vector<int, std::allocator<int>>>, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:372:2
    #6 0x5be068bc1ad6 in std::vector<int, std::allocator<int>>::insert(__gnu_cxx::__normal_iterator<int const*, std::vector<int, std::allocator<int>>>, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1394:16
    #7 0x5be068ae876b in f_vector_insert_end_ptr_recto(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:612:5
    #8 0x5be068b7c730 in main /work/test/runtime_runner.cpp:463:5
    #9 0x7389f65801c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x7389f658028a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x5be0689eb4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5be068ad4d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5be068bd4c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5be068bd450f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5be068bd450f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x5be068bc2720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x5be068b62187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x5be068b7c723 in main /work/test/runtime_runner.cpp:462:26
    #7 0x7389f65801c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x7389f658028a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x5be0689eb4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:613:8 in f_vector_insert_end_ptr_recto(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6fb9f57dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6fb9f57dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6fb9f57dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6fb9f57dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6fb9f57dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6fb9f57e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x6fb9f57e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6fb9f57e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6fb9f57e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6fb9f57e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6fb9f57e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==270==ABORTING
````

</details>

### f_vector_insert_end_ptr_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_insert_end_ptr_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.insert(c.end(),1);
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
d::vector<int, std::allocator<int>>>, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:372:2
    #6 0x61ed3abffad6 in std::vector<int, std::allocator<int>>::insert(__gnu_cxx::__normal_iterator<int const*, std::vector<int, std::allocator<int>>>, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1394:16
    #7 0x61ed3ab26e34 in f_vector_insert_end_ptr_guarda(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:626:5
    #8 0x61ed3abbaa1c in main /work/test/runtime_runner.cpp:473:5
    #9 0x73b756fc61c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x73b756fc628a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x61ed3aa294b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x61ed3ab12d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x61ed3ac12c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x61ed3ac1250f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x61ed3ac1250f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x61ed3ac00720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x61ed3aba0187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x61ed3abbaa0f in main /work/test/runtime_runner.cpp:472:26
    #7 0x73b756fc61c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x73b756fc628a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x61ed3aa294b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:627:8 in f_vector_insert_end_ptr_guarda(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6fe7561dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6fe7561dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6fe7561dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6fe7561dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6fe7561dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6fe7561e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x6fe7561e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6fe7561e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6fe7561e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6fe7561e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6fe7561e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==277==ABORTING
````

</details>

### f_vector_insert_end_ptr_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_insert_end_ptr_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.insert(c.end(),1);
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
    iterator "this" @ 0x7ffd5bfe3080 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffd5bfe31a0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
td::vector<int, std::allocator<int>>>, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:372:2
    #6 0x642b9d258ad6 in std::vector<int, std::allocator<int>>::insert(__gnu_cxx::__normal_iterator<int const*, std::vector<int, std::allocator<int>>>, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1394:16
    #7 0x642b9d18062d in f_vector_insert_end_ptr_bucle(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:641:7
    #8 0x642b9d213d08 in main /work/test/runtime_runner.cpp:483:5
    #9 0x78da162a11c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x78da162a128a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x642b9d0824b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x642b9d16bd31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x642b9d26bc77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x642b9d26b50f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x642b9d26b50f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x642b9d259720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x642b9d1f9187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x642b9d213cfb in main /work/test/runtime_runner.cpp:482:26
    #7 0x78da162a11c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x78da162a128a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x642b9d0824b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:642:10 in f_vector_insert_end_ptr_bucle(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x750a155dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x750a155dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x750a155dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x750a155dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x750a155dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x750a155e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x750a155e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x750a155e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x750a155e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x750a155e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x750a155e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==284==ABORTING
````

</details>

### f_vector_insert_end_ptr_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_insert_end_ptr_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_vector_insert_end(c);
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
:372:2
    #6 0x5c3c0f3eead6 in std::vector<int, std::allocator<int>>::insert(__gnu_cxx::__normal_iterator<int const*, std::vector<int, std::allocator<int>>>, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1394:16
    #7 0x5c3c0f303830 in mutar_vector_insert_end(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:18:55
    #8 0x5c3c0f316d69 in f_vector_insert_end_ptr_llamada(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:658:3
    #9 0x5c3c0f3a9ff4 in main /work/test/runtime_runner.cpp:493:5
    #10 0x77a71c1ad1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x77a71c1ad28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x5c3c0f2184b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5c3c0f301d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5c3c0f401c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5c3c0f40150f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5c3c0f40150f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x5c3c0f3ef720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x5c3c0f38f187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x5c3c0f3a9fe7 in main /work/test/runtime_runner.cpp:492:26
    #7 0x77a71c1ad1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x77a71c1ad28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x5c3c0f2184b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:659:8 in f_vector_insert_end_ptr_llamada(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x73d71b3dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73d71b3dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73d71b3dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73d71b3dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73d71b3dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x73d71b3e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x73d71b3e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x73d71b3e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x73d71b3e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x73d71b3e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x73d71b3e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==291==ABORTING
````

</details>
