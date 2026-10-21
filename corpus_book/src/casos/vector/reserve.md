# `std::vector::reserve`

Mutación: `c.reserve(c.size()+100);`

- Iterador retenido: 🟡 `POLICY`
- Referencia/puntero retenido: 🟡 `POLICY`
- Casos `UB` detectados estáticamente: 0/0

**En palabras:** después de `c.reserve(c.size()+100);` sobre un `std::vector`, un iterador guardado **puede** quedar inválido según el estado del contenedor (capacidad o factor de carga); una referencia o puntero guardado **puede** quedar inválido según el estado del contenedor (capacidad o factor de carga).

Mapa de los 12 casos. Cada celda muestra la respuesta correcta (etiqueta) y, debajo, lo que hizo el analizador estático de Clang. Clic para ir al caso. Ver [Cómo leer este libro](../../guia.md).

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_reserve_it_recto) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_reserve_it_guarda) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_reserve_it_bucle) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_reserve_it_llamada) |
| **referencia** | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_reserve_ref_recto) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_reserve_ref_guarda) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_reserve_ref_bucle) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_reserve_ref_llamada) |
| **puntero** | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_reserve_ptr_recto) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_reserve_ptr_guarda) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_reserve_ptr_bucle) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_reserve_ptr_llamada) |

## Handle: iterador

### f_vector_reserve_it_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_reserve_it_recto(std::vector<int>& c) {
  auto it = c.begin();
  c.reserve(c.size()+100);
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
    iterator "this" @ 0x7fffbd55a950 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7fffbd55a9e0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
bits/alloc_traits.h:517:13
    #3 0x5bf7996c875b in std::_Vector_base<int, std::allocator<int>>::_M_deallocate(int*, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:390:4
    #4 0x5bf7996b6b58 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:93:4
    #5 0x5bf7995e462c in f_vector_reserve_it_recto(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:911:5
    #6 0x5bf799674478 in main /work/test/runtime_runner.cpp:683:5
    #7 0x727a5e8121c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x727a5e81228a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x5bf7994df4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5bf7995c8d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5bf7996c8c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5bf7996c850f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5bf7996c850f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x5bf7996b6720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x5bf799656187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x5bf79967446b in main /work/test/runtime_runner.cpp:682:26
    #7 0x727a5e8121c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x727a5e81228a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x5bf7994df4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:912:8 in f_vector_reserve_it_recto(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6eaa5dbdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6eaa5dbdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6eaa5dbdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6eaa5dbdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6eaa5dbdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6eaa5dbe0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x6eaa5dbe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6eaa5dbe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6eaa5dbe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6eaa5dbe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6eaa5dbe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==406==ABORTING
````

</details>

### f_vector_reserve_it_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_reserve_it_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.reserve(c.size()+100);
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
    iterator "this" @ 0x7ffdc193f0e0 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffdc193f1a0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
ts/alloc_traits.h:517:13
    #3 0x5a24583c975b in std::_Vector_base<int, std::allocator<int>>::_M_deallocate(int*, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:390:4
    #4 0x5a24583b7b58 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:93:4
    #5 0x5a24582e58d7 in f_vector_reserve_it_guarda(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:917:5
    #6 0x5a24583755ee in main /work/test/runtime_runner.cpp:688:5
    #7 0x7d36dc2671c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x7d36dc26728a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x5a24581e04b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5a24582c9d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5a24583c9c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5a24583c950f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5a24583c950f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x5a24583b7720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x5a2458357187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x5a24583755e1 in main /work/test/runtime_runner.cpp:687:26
    #7 0x7d36dc2671c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x7d36dc26728a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x5a24581e04b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:918:8 in f_vector_reserve_it_guarda(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7966db5dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7966db5dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7966db5dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7966db5dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7966db5dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7966db5e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7966db5e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7966db5e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7966db5e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7966db5e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7966db5e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==411==ABORTING
````

</details>

### f_vector_reserve_it_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_reserve_it_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.reserve(c.size()+100);
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
    iterator "this" @ 0x7fff924d7d40 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7fff924d7e00
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
its/alloc_traits.h:517:13
    #3 0x5eff0c74775b in std::_Vector_base<int, std::allocator<int>>::_M_deallocate(int*, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:390:4
    #4 0x5eff0c735b58 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:93:4
    #5 0x5eff0c663c02 in f_vector_reserve_it_bucle(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:923:7
    #6 0x5eff0c6f3764 in main /work/test/runtime_runner.cpp:693:5
    #7 0x7f221a2051c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x7f221a20528a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x5eff0c55e4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5eff0c647d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5eff0c747c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5eff0c74750f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5eff0c74750f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x5eff0c735720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x5eff0c6d5187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x5eff0c6f3757 in main /work/test/runtime_runner.cpp:692:26
    #7 0x7f221a2051c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x7f221a20528a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x5eff0c55e4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:924:10 in f_vector_reserve_it_bucle(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7b52195dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b52195dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b52195dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b52195dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b52195dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b52195e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7b52195e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b52195e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b52195e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b52195e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b52195e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==416==ABORTING
````

</details>

### f_vector_reserve_it_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_reserve_it_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_vector_reserve(c);
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
    iterator "this" @ 0x7fff0dbc9110 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7fff0dbc91d0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
signed long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:390:4
    #4 0x59a4d6ee1b58 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:93:4
    #5 0x59a4d6df5bbe in mutar_vector_reserve(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:22:52
    #6 0x59a4d6e0fe8c in f_vector_reserve_it_llamada(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:930:3
    #7 0x59a4d6e9f8da in main /work/test/runtime_runner.cpp:698:5
    #8 0x7cc17411b1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x7cc17411b28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x59a4d6d0a4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x59a4d6df3d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x59a4d6ef3c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x59a4d6ef350f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x59a4d6ef350f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x59a4d6ee1720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x59a4d6e81187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x59a4d6e9f8cd in main /work/test/runtime_runner.cpp:697:26
    #7 0x7cc17411b1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x7cc17411b28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x59a4d6d0a4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:931:8 in f_vector_reserve_it_llamada(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x78f1733dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x78f1733dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x78f1733dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x78f1733dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x78f1733dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x78f1733e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x78f1733e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x78f1733e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x78f1733e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x78f1733e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x78f1733e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==421==ABORTING
````

</details>

## Handle: referencia

### f_vector_reserve_ref_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_reserve_ref_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.reserve(c.size()+100);
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
ts/alloc_traits.h:517:13
    #3 0x61ba0062f75b in std::_Vector_base<int, std::allocator<int>>::_M_deallocate(int*, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:390:4
    #4 0x61ba0061db58 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:93:4
    #5 0x61ba0054c115 in f_vector_reserve_ref_recto(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:936:5
    #6 0x61ba005dba50 in main /work/test/runtime_runner.cpp:703:5
    #7 0x7fe9f0fae1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x7fe9f0fae28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x61ba004464b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x61ba0052fd31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x61ba0062fc77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x61ba0062f50f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x61ba0062f50f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x61ba0061d720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x61ba005bd187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x61ba005dba43 in main /work/test/runtime_runner.cpp:702:26
    #7 0x7fe9f0fae1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x7fe9f0fae28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x61ba004464b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:937:8 in f_vector_reserve_ref_recto(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7c19f01dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c19f01dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c19f01dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c19f01dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c19f01dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c19f01e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7c19f01e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c19f01e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c19f01e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c19f01e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c19f01e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==426==ABORTING
````

</details>

### f_vector_reserve_ref_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_reserve_ref_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.reserve(c.size()+100);
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
/alloc_traits.h:517:13
    #3 0x5fdb4e5e575b in std::_Vector_base<int, std::allocator<int>>::_M_deallocate(int*, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:390:4
    #4 0x5fdb4e5d3b58 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:93:4
    #5 0x5fdb4e5023ca in f_vector_reserve_ref_guarda(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:943:5
    #6 0x5fdb4e591bc6 in main /work/test/runtime_runner.cpp:708:5
    #7 0x79ead96181c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x79ead961828a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x5fdb4e3fc4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5fdb4e4e5d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5fdb4e5e5c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5fdb4e5e550f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5fdb4e5e550f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x5fdb4e5d3720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x5fdb4e573187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x5fdb4e591bb9 in main /work/test/runtime_runner.cpp:707:26
    #7 0x79ead96181c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x79ead961828a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x5fdb4e3fc4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:944:8 in f_vector_reserve_ref_guarda(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x761ad89dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x761ad89dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x761ad89dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x761ad89dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x761ad89dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x761ad89e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x761ad89e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x761ad89e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x761ad89e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x761ad89e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x761ad89e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==431==ABORTING
````

</details>

### f_vector_reserve_ref_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_reserve_ref_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.reserve(c.size()+100);
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
    iterator "this" @ 0x7ffedef83ff0 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffedef840b0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
s/alloc_traits.h:517:13
    #3 0x5f2ce40fb75b in std::_Vector_base<int, std::allocator<int>>::_M_deallocate(int*, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:390:4
    #4 0x5f2ce40e9b58 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:93:4
    #5 0x5f2ce4018705 in f_vector_reserve_ref_bucle(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:950:7
    #6 0x5f2ce40a7d3c in main /work/test/runtime_runner.cpp:713:5
    #7 0x7dd1713d31c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x7dd1713d328a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x5f2ce3f124b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5f2ce3ffbd31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5f2ce40fbc77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5f2ce40fb50f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5f2ce40fb50f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x5f2ce40e9720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x5f2ce4089187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x5f2ce40a7d2f in main /work/test/runtime_runner.cpp:712:26
    #7 0x7dd1713d31c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x7dd1713d328a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x5f2ce3f124b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:951:10 in f_vector_reserve_ref_bucle(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7a01707dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a01707dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a01707dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a01707dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a01707dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7a01707e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7a01707e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a01707e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a01707e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a01707e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a01707e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==436==ABORTING
````

</details>

### f_vector_reserve_ref_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_reserve_ref_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_vector_reserve(c);
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
gned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:390:4
    #4 0x5a0392d02b58 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:93:4
    #5 0x5a0392c16bbe in mutar_vector_reserve(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:22:52
    #6 0x5a0392c319a5 in f_vector_reserve_ref_llamada(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:958:3
    #7 0x5a0392cc0eb2 in main /work/test/runtime_runner.cpp:718:5
    #8 0x7e86d32bf1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x7e86d32bf28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x5a0392b2b4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5a0392c14d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5a0392d14c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5a0392d1450f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5a0392d1450f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x5a0392d02720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x5a0392ca2187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x5a0392cc0ea5 in main /work/test/runtime_runner.cpp:717:26
    #7 0x7e86d32bf1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x7e86d32bf28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x5a0392b2b4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:959:8 in f_vector_reserve_ref_llamada(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7ab6d25dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ab6d25dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ab6d25dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ab6d25dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ab6d25dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7ab6d25e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7ab6d25e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ab6d25e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ab6d25e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ab6d25e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ab6d25e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==441==ABORTING
````

</details>

## Handle: puntero

### f_vector_reserve_ptr_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_reserve_ptr_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.reserve(c.size()+100);
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
ts/alloc_traits.h:517:13
    #3 0x5a9375d5375b in std::_Vector_base<int, std::allocator<int>>::_M_deallocate(int*, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:390:4
    #4 0x5a9375d41b58 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:93:4
    #5 0x5a9375c70bd2 in f_vector_reserve_ptr_recto(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:964:5
    #6 0x5a9375d00028 in main /work/test/runtime_runner.cpp:723:5
    #7 0x70ebc7ed21c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x70ebc7ed228a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x5a9375b6a4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5a9375c53d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5a9375d53c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5a9375d5350f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5a9375d5350f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x5a9375d41720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x5a9375ce1187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x5a9375d0001b in main /work/test/runtime_runner.cpp:722:26
    #7 0x70ebc7ed21c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x70ebc7ed228a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x5a9375b6a4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:965:8 in f_vector_reserve_ptr_recto(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6d1bc71dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d1bc71dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d1bc71dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d1bc71dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d1bc71dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6d1bc71e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x6d1bc71e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d1bc71e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d1bc71e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d1bc71e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d1bc71e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==446==ABORTING
````

</details>

### f_vector_reserve_ptr_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_reserve_ptr_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.reserve(c.size()+100);
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
/alloc_traits.h:517:13
    #3 0x62084f51375b in std::_Vector_base<int, std::allocator<int>>::_M_deallocate(int*, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:390:4
    #4 0x62084f501b58 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:93:4
    #5 0x62084f430e87 in f_vector_reserve_ptr_guarda(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:971:5
    #6 0x62084f4c019e in main /work/test/runtime_runner.cpp:728:5
    #7 0x74dcc73e41c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x74dcc73e428a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x62084f32a4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x62084f413d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x62084f513c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x62084f51350f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x62084f51350f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x62084f501720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x62084f4a1187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x62084f4c0191 in main /work/test/runtime_runner.cpp:727:26
    #7 0x74dcc73e41c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x74dcc73e428a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x62084f32a4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:972:8 in f_vector_reserve_ptr_guarda(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x710cc67dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x710cc67dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x710cc67dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x710cc67dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x710cc67dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x710cc67e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x710cc67e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x710cc67e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x710cc67e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x710cc67e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x710cc67e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==451==ABORTING
````

</details>

### f_vector_reserve_ptr_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_reserve_ptr_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.reserve(c.size()+100);
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
    iterator "this" @ 0x7fff298f4af0 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7fff298f4bb0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
s/alloc_traits.h:517:13
    #3 0x5b94d610875b in std::_Vector_base<int, std::allocator<int>>::_M_deallocate(int*, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:390:4
    #4 0x5b94d60f6b58 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:93:4
    #5 0x5b94d60261c2 in f_vector_reserve_ptr_bucle(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:978:7
    #6 0x5b94d60b5314 in main /work/test/runtime_runner.cpp:733:5
    #7 0x795fb5c1f1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x795fb5c1f28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x5b94d5f1f4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5b94d6008d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5b94d6108c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5b94d610850f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5b94d610850f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x5b94d60f6720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x5b94d6096187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x5b94d60b5307 in main /work/test/runtime_runner.cpp:732:26
    #7 0x795fb5c1f1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x795fb5c1f28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x5b94d5f1f4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:979:10 in f_vector_reserve_ptr_bucle(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x758fb4fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x758fb4fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x758fb4fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x758fb4fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x758fb4fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x758fb4fe0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x758fb4fe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x758fb4fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x758fb4fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x758fb4fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x758fb4fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==456==ABORTING
````

</details>

### f_vector_reserve_ptr_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_reserve_ptr_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_vector_reserve(c);
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
gned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:390:4
    #4 0x5c125fedeb58 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:93:4
    #5 0x5c125fdf2bbe in mutar_vector_reserve(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:22:52
    #6 0x5c125fe0e459 in f_vector_reserve_ptr_llamada(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:986:3
    #7 0x5c125fe9d48a in main /work/test/runtime_runner.cpp:738:5
    #8 0x79c546c621c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x79c546c6228a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x5c125fd074b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5c125fdf0d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5c125fef0c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5c125fef050f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5c125fef050f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x5c125fede720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x5c125fe7e187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x5c125fe9d47d in main /work/test/runtime_runner.cpp:737:26
    #7 0x79c546c621c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x79c546c6228a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x5c125fd074b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:987:8 in f_vector_reserve_ptr_llamada(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x75f545fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75f545fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75f545fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75f545fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75f545fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x75f545fe0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x75f545fe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x75f545fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x75f545fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x75f545fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x75f545fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==461==ABORTING
````

</details>
