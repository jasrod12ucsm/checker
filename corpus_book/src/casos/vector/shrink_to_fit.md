# `std::vector::shrink_to_fit`

Mutación: `c.shrink_to_fit();`

- Iterador retenido: 🟡 `POLICY`
- Referencia/puntero retenido: 🟡 `POLICY`
- Casos `UB` detectados estáticamente: 0/0

**En palabras:** después de `c.shrink_to_fit();` sobre un `std::vector`, un iterador guardado **puede** quedar inválido según el estado del contenedor (capacidad o factor de carga); una referencia o puntero guardado **puede** quedar inválido según el estado del contenedor (capacidad o factor de carga).

Mapa de los 12 casos. Cada celda muestra la respuesta correcta (etiqueta) y, debajo, lo que hizo el analizador estático de Clang. Clic para ir al caso. Ver [Cómo leer este libro](../../guia.md).

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_shrink_to_fit_it_recto) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_shrink_to_fit_it_guarda) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_shrink_to_fit_it_bucle) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_shrink_to_fit_it_llamada) |
| **referencia** | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_shrink_to_fit_ref_recto) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_shrink_to_fit_ref_guarda) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_shrink_to_fit_ref_bucle) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_shrink_to_fit_ref_llamada) |
| **puntero** | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_shrink_to_fit_ptr_recto) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_shrink_to_fit_ptr_guarda) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_shrink_to_fit_ptr_bucle) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_shrink_to_fit_ptr_llamada) |

## Handle: iterador

### f_vector_shrink_to_fit_it_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_shrink_to_fit_it_recto(std::vector<int>& c) {
  auto it = c.begin();
  c.shrink_to_fit();
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | holgura de capacidad | 🛑 attempt to dereference a singular iterator | 🛑 heap-use-after-free |
| `preserve` | capacidad previamente ajustada al tamaño | sin detección | sin detección |

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
    iterator "this" @ 0x7ffff0aad070 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffff0aad100
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
de/c++/13/bits/alloc_traits.h:906:6
    #7 0x579754b4f928 in std::vector<int, std::allocator<int>>::_M_shrink_to_fit() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:721:14
    #8 0x579754b38f94 in std::vector<int, std::allocator<int>>::shrink_to_fit() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1069:9
    #9 0x579754a68659 in f_vector_shrink_to_fit_it_recto(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:991:5
    #10 0x579754af7600 in main /work/test/runtime_runner.cpp:743:5
    #11 0x70afb1ed91c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x70afb1ed928a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x5797549614b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x579754a4ad31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x579754b4ac77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x579754b4a50f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x579754b4a50f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x579754b38720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x579754ad7f8b in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:34:44
    #6 0x579754af75f3 in main /work/test/runtime_runner.cpp:742:26
    #7 0x70afb1ed91c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x70afb1ed928a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x5797549614b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:992:8 in f_vector_shrink_to_fit_it_recto(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6e3fb11dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e3fb11dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e3fb11dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e3fb11dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e3fb11e0000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x6e3fb11e0080:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x6e3fb11e0100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x6e3fb11e0180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x6e3fb11e0200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x6e3fb11e0280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x6e3fb11e0300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==466==ABORTING
````

</details>

### f_vector_shrink_to_fit_it_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_shrink_to_fit_it_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.shrink_to_fit();
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | holgura de capacidad | 🛑 attempt to dereference a singular iterator | 🛑 heap-use-after-free |
| `preserve` | capacidad previamente ajustada al tamaño | sin detección | sin detección |

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
    iterator "this" @ 0x7ffc6e5da590 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffc6e5da650
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
/c++/13/bits/alloc_traits.h:906:6
    #7 0x5bb1cafdc928 in std::vector<int, std::allocator<int>>::_M_shrink_to_fit() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:721:14
    #8 0x5bb1cafc5f94 in std::vector<int, std::allocator<int>>::shrink_to_fit() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1069:9
    #9 0x5bb1caef58be in f_vector_shrink_to_fit_it_guarda(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:997:5
    #10 0x5bb1caf84776 in main /work/test/runtime_runner.cpp:748:5
    #11 0x70b3174781c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x70b31747828a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x5bb1cadee4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5bb1caed7d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5bb1cafd7c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5bb1cafd750f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5bb1cafd750f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x5bb1cafc5720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x5bb1caf64f8b in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:34:44
    #6 0x5bb1caf84769 in main /work/test/runtime_runner.cpp:747:26
    #7 0x70b3174781c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x70b31747828a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x5bb1cadee4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:998:8 in f_vector_shrink_to_fit_it_guarda(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6e43167dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e43167dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e43167dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e43167dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e43167e0000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x6e43167e0080:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x6e43167e0100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x6e43167e0180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x6e43167e0200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x6e43167e0280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x6e43167e0300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==471==ABORTING
````

</details>

### f_vector_shrink_to_fit_it_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_shrink_to_fit_it_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.shrink_to_fit();
    sink(*it);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | holgura de capacidad | 🛑 attempt to dereference a singular iterator | 🛑 heap-use-after-free |
| `preserve` | capacidad previamente ajustada al tamaño | sin detección | sin detección |

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
    iterator "this" @ 0x7fff8885d4c0 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7fff8885d580
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
c++/13/bits/alloc_traits.h:906:6
    #7 0x5fbf3b3d5928 in std::vector<int, std::allocator<int>>::_M_shrink_to_fit() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:721:14
    #8 0x5fbf3b3bef94 in std::vector<int, std::allocator<int>>::shrink_to_fit() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1069:9
    #9 0x5fbf3b2eeb9f in f_vector_shrink_to_fit_it_bucle(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:1003:7
    #10 0x5fbf3b37d8ec in main /work/test/runtime_runner.cpp:753:5
    #11 0x78c5d5cbd1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x78c5d5cbd28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x5fbf3b1e74b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5fbf3b2d0d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5fbf3b3d0c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5fbf3b3d050f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5fbf3b3d050f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x5fbf3b3be720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x5fbf3b35df8b in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:34:44
    #6 0x5fbf3b37d8df in main /work/test/runtime_runner.cpp:752:26
    #7 0x78c5d5cbd1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x78c5d5cbd28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x5fbf3b1e74b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:1004:10 in f_vector_shrink_to_fit_it_bucle(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7655d4fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7655d4fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7655d4fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7655d4fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7655d4fe0000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x7655d4fe0080:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7655d4fe0100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7655d4fe0180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7655d4fe0200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7655d4fe0280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7655d4fe0300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==476==ABORTING
````

</details>

### f_vector_shrink_to_fit_it_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_shrink_to_fit_it_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_vector_shrink_to_fit(c);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | holgura de capacidad | 🛑 attempt to dereference a singular iterator | 🛑 heap-use-after-free |
| `preserve` | capacidad previamente ajustada al tamaño | sin detección | sin detección |

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
    iterator "this" @ 0x7ffdb7ecfa20 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffdb7ecfae0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:721:14
    #8 0x5a2adc069f94 in std::vector<int, std::allocator<int>>::shrink_to_fit() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1069:9
    #9 0x5a2adbf7dc0e in mutar_vector_shrink_to_fit(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:23:58
    #10 0x5a2adbf99e2c in f_vector_shrink_to_fit_it_llamada(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:1010:3
    #11 0x5a2adc028a62 in main /work/test/runtime_runner.cpp:758:5
    #12 0x72790783a1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x72790783a28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x5a2adbe924b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5a2adbf7bd31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5a2adc07bc77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5a2adc07b50f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5a2adc07b50f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x5a2adc069720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x5a2adc008f8b in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:34:44
    #6 0x5a2adc028a55 in main /work/test/runtime_runner.cpp:757:26
    #7 0x72790783a1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x72790783a28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x5a2adbe924b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:1011:8 in f_vector_shrink_to_fit_it_llamada(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x700906bdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x700906bdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x700906bdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x700906bdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x700906be0000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x700906be0080:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x700906be0100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x700906be0180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x700906be0200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x700906be0280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x700906be0300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==481==ABORTING
````

</details>

## Handle: referencia

### f_vector_shrink_to_fit_ref_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_shrink_to_fit_ref_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.shrink_to_fit();
  sink(h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | holgura de capacidad | sin detección | 🛑 heap-use-after-free |
| `preserve` | capacidad previamente ajustada al tamaño | sin detección | sin detección |

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
++/13/bits/alloc_traits.h:906:6
    #7 0x60cfe7ec9928 in std::vector<int, std::allocator<int>>::_M_shrink_to_fit() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:721:14
    #8 0x60cfe7eb2f94 in std::vector<int, std::allocator<int>>::shrink_to_fit() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1069:9
    #9 0x60cfe7de3072 in f_vector_shrink_to_fit_ref_recto(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:1016:5
    #10 0x60cfe7e71bd8 in main /work/test/runtime_runner.cpp:763:5
    #11 0x73353a9a41c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x73353a9a428a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x60cfe7cdb4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x60cfe7dc4d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x60cfe7ec4c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x60cfe7ec450f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x60cfe7ec450f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x60cfe7eb2720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x60cfe7e51f8b in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:34:44
    #6 0x60cfe7e71bcb in main /work/test/runtime_runner.cpp:762:26
    #7 0x73353a9a41c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x73353a9a428a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x60cfe7cdb4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:1017:8 in f_vector_shrink_to_fit_ref_recto(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x70c539bdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x70c539bdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x70c539bdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x70c539bdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x70c539be0000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x70c539be0080:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x70c539be0100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x70c539be0180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x70c539be0200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x70c539be0280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x70c539be0300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==486==ABORTING
````

</details>

### f_vector_shrink_to_fit_ref_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_shrink_to_fit_ref_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.shrink_to_fit();
  sink(h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | holgura de capacidad | sin detección | 🛑 heap-use-after-free |
| `preserve` | capacidad previamente ajustada al tamaño | sin detección | sin detección |

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
/13/bits/alloc_traits.h:906:6
    #7 0x57ca49f94928 in std::vector<int, std::allocator<int>>::_M_shrink_to_fit() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:721:14
    #8 0x57ca49f7df94 in std::vector<int, std::allocator<int>>::shrink_to_fit() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1069:9
    #9 0x57ca49eae2e7 in f_vector_shrink_to_fit_ref_guarda(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:1023:5
    #10 0x57ca49f3cd4e in main /work/test/runtime_runner.cpp:768:5
    #11 0x7b644c3c41c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x7b644c3c428a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x57ca49da64b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x57ca49e8fd31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x57ca49f8fc77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x57ca49f8f50f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x57ca49f8f50f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x57ca49f7d720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x57ca49f1cf8b in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:34:44
    #6 0x57ca49f3cd41 in main /work/test/runtime_runner.cpp:767:26
    #7 0x7b644c3c41c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x7b644c3c428a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x57ca49da64b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:1024:8 in f_vector_shrink_to_fit_ref_guarda(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x78f44b5dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x78f44b5dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x78f44b5dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x78f44b5dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x78f44b5e0000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x78f44b5e0080:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x78f44b5e0100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x78f44b5e0180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x78f44b5e0200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x78f44b5e0280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x78f44b5e0300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==491==ABORTING
````

</details>

### f_vector_shrink_to_fit_ref_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_shrink_to_fit_ref_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.shrink_to_fit();
    sink(h);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | holgura de capacidad | 🛑 attempt to increment a singular iterator | 🛑 heap-use-after-free |
| `preserve` | capacidad previamente ajustada al tamaño | sin detección | sin detección |

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
    iterator "this" @ 0x7ffdd5ad6c30 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffdd5ad6cf0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
+/13/bits/alloc_traits.h:906:6
    #7 0x6191380c2928 in std::vector<int, std::allocator<int>>::_M_shrink_to_fit() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:721:14
    #8 0x6191380abf94 in std::vector<int, std::allocator<int>>::shrink_to_fit() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1069:9
    #9 0x619137fdc5e2 in f_vector_shrink_to_fit_ref_bucle(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:1030:7
    #10 0x61913806aec4 in main /work/test/runtime_runner.cpp:773:5
    #11 0x7c6e9590a1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x7c6e9590a28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x619137ed44b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x619137fbdd31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x6191380bdc77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x6191380bd50f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x6191380bd50f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x6191380ab720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x61913804af8b in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:34:44
    #6 0x61913806aeb7 in main /work/test/runtime_runner.cpp:772:26
    #7 0x7c6e9590a1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x7c6e9590a28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x619137ed44b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:1031:10 in f_vector_shrink_to_fit_ref_bucle(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x79fe94bdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x79fe94bdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x79fe94bdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x79fe94bdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x79fe94be0000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x79fe94be0080:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x79fe94be0100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x79fe94be0180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x79fe94be0200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x79fe94be0280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x79fe94be0300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==496==ABORTING
````

</details>

### f_vector_shrink_to_fit_ref_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_shrink_to_fit_ref_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_vector_shrink_to_fit(c);
  sink(h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | holgura de capacidad | sin detección | 🛑 heap-use-after-free |
| `preserve` | capacidad previamente ajustada al tamaño | sin detección | sin detección |

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
cc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:721:14
    #8 0x5d3f80ef5f94 in std::vector<int, std::allocator<int>>::shrink_to_fit() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1069:9
    #9 0x5d3f80e09c0e in mutar_vector_shrink_to_fit(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:23:58
    #10 0x5d3f80e26885 in f_vector_shrink_to_fit_ref_llamada(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:1038:3
    #11 0x5d3f80eb503a in main /work/test/runtime_runner.cpp:778:5
    #12 0x7100c22d61c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x7100c22d628a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x5d3f80d1e4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5d3f80e07d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5d3f80f07c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5d3f80f0750f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5d3f80f0750f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x5d3f80ef5720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x5d3f80e94f8b in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:34:44
    #6 0x5d3f80eb502d in main /work/test/runtime_runner.cpp:777:26
    #7 0x7100c22d61c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x7100c22d628a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x5d3f80d1e4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:1039:8 in f_vector_shrink_to_fit_ref_llamada(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6e90c15dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e90c15dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e90c15dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e90c15dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e90c15e0000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x6e90c15e0080:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x6e90c15e0100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x6e90c15e0180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x6e90c15e0200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x6e90c15e0280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x6e90c15e0300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==501==ABORTING
````

</details>

## Handle: puntero

### f_vector_shrink_to_fit_ptr_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_shrink_to_fit_ptr_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.shrink_to_fit();
  sink(*h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | holgura de capacidad | sin detección | 🛑 heap-use-after-free |
| `preserve` | capacidad previamente ajustada al tamaño | sin detección | sin detección |

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
++/13/bits/alloc_traits.h:906:6
    #7 0x5679e41f6928 in std::vector<int, std::allocator<int>>::_M_shrink_to_fit() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:721:14
    #8 0x5679e41dff94 in std::vector<int, std::allocator<int>>::shrink_to_fit() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1069:9
    #9 0x5679e4110a6f in f_vector_shrink_to_fit_ptr_recto(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:1044:5
    #10 0x5679e419f1b0 in main /work/test/runtime_runner.cpp:783:5
    #11 0x7a533eef61c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x7a533eef628a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x5679e40084b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5679e40f1d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5679e41f1c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5679e41f150f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5679e41f150f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x5679e41df720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x5679e417ef8b in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:34:44
    #6 0x5679e419f1a3 in main /work/test/runtime_runner.cpp:782:26
    #7 0x7a533eef61c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x7a533eef628a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x5679e40084b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:1045:8 in f_vector_shrink_to_fit_ptr_recto(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x77e33e1dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x77e33e1dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x77e33e1dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x77e33e1dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x77e33e1e0000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x77e33e1e0080:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x77e33e1e0100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x77e33e1e0180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x77e33e1e0200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x77e33e1e0280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x77e33e1e0300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==506==ABORTING
````

</details>

### f_vector_shrink_to_fit_ptr_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_shrink_to_fit_ptr_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.shrink_to_fit();
  sink(*h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | holgura de capacidad | sin detección | 🛑 heap-use-after-free |
| `preserve` | capacidad previamente ajustada al tamaño | sin detección | sin detección |

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
/13/bits/alloc_traits.h:906:6
    #7 0x63c5d5b1c928 in std::vector<int, std::allocator<int>>::_M_shrink_to_fit() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:721:14
    #8 0x63c5d5b05f94 in std::vector<int, std::allocator<int>>::shrink_to_fit() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1069:9
    #9 0x63c5d5a36cdb in f_vector_shrink_to_fit_ptr_guarda(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:1051:5
    #10 0x63c5d5ac5326 in main /work/test/runtime_runner.cpp:788:5
    #11 0x7bc4f0f451c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x7bc4f0f4528a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x63c5d592e4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x63c5d5a17d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x63c5d5b17c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x63c5d5b1750f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x63c5d5b1750f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x63c5d5b05720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x63c5d5aa4f8b in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:34:44
    #6 0x63c5d5ac5319 in main /work/test/runtime_runner.cpp:787:26
    #7 0x7bc4f0f451c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x7bc4f0f4528a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x63c5d592e4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:1052:8 in f_vector_shrink_to_fit_ptr_guarda(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7954f01dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7954f01dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7954f01dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7954f01dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7954f01e0000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x7954f01e0080:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7954f01e0100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7954f01e0180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7954f01e0200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7954f01e0280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7954f01e0300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==511==ABORTING
````

</details>

### f_vector_shrink_to_fit_ptr_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_shrink_to_fit_ptr_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.shrink_to_fit();
    sink(*h);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | holgura de capacidad | 🛑 attempt to increment a singular iterator | 🛑 heap-use-after-free |
| `preserve` | capacidad previamente ajustada al tamaño | sin detección | sin detección |

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
    iterator "this" @ 0x7fff577ed9f0 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7fff577edab0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
+/13/bits/alloc_traits.h:906:6
    #7 0x568c6ebde928 in std::vector<int, std::allocator<int>>::_M_shrink_to_fit() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:721:14
    #8 0x568c6ebc7f94 in std::vector<int, std::allocator<int>>::shrink_to_fit() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1069:9
    #9 0x568c6eaf8fcf in f_vector_shrink_to_fit_ptr_bucle(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:1058:7
    #10 0x568c6eb8749c in main /work/test/runtime_runner.cpp:793:5
    #11 0x7c99474491c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x7c994744928a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x568c6e9f04b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x568c6ead9d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x568c6ebd9c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x568c6ebd950f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x568c6ebd950f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x568c6ebc7720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x568c6eb66f8b in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:34:44
    #6 0x568c6eb8748f in main /work/test/runtime_runner.cpp:792:26
    #7 0x7c99474491c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x7c994744928a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x568c6e9f04b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:1059:10 in f_vector_shrink_to_fit_ptr_bucle(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7a29467dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a29467dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a29467dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a29467dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a29467e0000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x7a29467e0080:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7a29467e0100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7a29467e0180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7a29467e0200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7a29467e0280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7a29467e0300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==516==ABORTING
````

</details>

### f_vector_shrink_to_fit_ptr_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_shrink_to_fit_ptr_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_vector_shrink_to_fit(c);
  sink(*h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | holgura de capacidad | sin detección | 🛑 heap-use-after-free |
| `preserve` | capacidad previamente ajustada al tamaño | sin detección | sin detección |

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
cc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:721:14
    #8 0x5dd59b12bf94 in std::vector<int, std::allocator<int>>::shrink_to_fit() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1069:9
    #9 0x5dd59b03fc0e in mutar_vector_shrink_to_fit(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:23:58
    #10 0x5dd59b05d269 in f_vector_shrink_to_fit_ptr_llamada(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:1066:3
    #11 0x5dd59b0eb612 in main /work/test/runtime_runner.cpp:798:5
    #12 0x7ceef0d3a1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x7ceef0d3a28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x5dd59af544b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5dd59b03dd31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5dd59b13dc77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5dd59b13d50f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5dd59b13d50f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x5dd59b12b720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x5dd59b0caf8b in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:34:44
    #6 0x5dd59b0eb605 in main /work/test/runtime_runner.cpp:797:26
    #7 0x7ceef0d3a1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x7ceef0d3a28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x5dd59af544b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:1067:8 in f_vector_shrink_to_fit_ptr_llamada(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7a7eeffdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a7eeffdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a7eeffdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a7eeffdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a7eeffe0000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x7a7eeffe0080:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7a7eeffe0100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7a7eeffe0180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7a7eeffe0200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7a7eeffe0280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7a7eeffe0300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==521==ABORTING
````

</details>
