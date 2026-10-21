# `std::vector::push_back`

Mutación: `c.push_back(1);`

- Iterador retenido: 🟡 `POLICY`
- Referencia/puntero retenido: 🟡 `POLICY`
- Casos `UB` detectados estáticamente: 0/0

**En palabras:** después de `c.push_back(1);` sobre un `std::vector`, un iterador guardado **puede** quedar inválido según el estado del contenedor (capacidad o factor de carga); una referencia o puntero guardado **puede** quedar inválido según el estado del contenedor (capacidad o factor de carga).

Mapa de los 12 casos. Cada celda muestra la respuesta correcta (etiqueta) y, debajo, lo que hizo el analizador estático de Clang. Clic para ir al caso. Ver [Cómo leer este libro](../../guia.md).

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_push_back_it_recto) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_push_back_it_guarda) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_push_back_it_bucle) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_push_back_it_llamada) |
| **referencia** | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_push_back_ref_recto) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_push_back_ref_guarda) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_push_back_ref_bucle) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_push_back_ref_llamada) |
| **puntero** | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_push_back_ptr_recto) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_push_back_ptr_guarda) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_push_back_ptr_bucle) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_push_back_ptr_llamada) |

## Handle: iterador

### f_vector_push_back_it_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_push_back_it_recto(std::vector<int>& c) {
  auto it = c.begin();
  c.push_back(1);
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
    iterator "this" @ 0x7ffc5d7dd400 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffc5d7dd490
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
/../include/c++/13/bits/vector.tcc:519:7
    #5 0x643502c839f0 in int& std::vector<int, std::allocator<int>>::emplace_back<int>(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:123:4
    #6 0x643502c833bc in std::vector<int, std::allocator<int>>::push_back(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1299:9
    #7 0x643502b9bbc0 in f_vector_push_back_it_recto(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:75:5
    #8 0x643502c378b2 in main /work/test/runtime_runner.cpp:83:5
    #9 0x79b8f9dbf1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x79b8f9dbf28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x643502aad4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x643502b96d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x643502c96c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x643502c9650f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x643502c9650f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x643502c84720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x643502c24187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x643502c378a5 in main /work/test/runtime_runner.cpp:82:26
    #7 0x79b8f9dbf1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x79b8f9dbf28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x643502aad4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:76:8 in f_vector_push_back_it_recto(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x75e8f8fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75e8f8fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75e8f8fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75e8f8fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75e8f8fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x75e8f8fe0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x75e8f8fe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x75e8f8fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x75e8f8fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x75e8f8fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x75e8f8fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==19==ABORTING
````

</details>

### f_vector_push_back_it_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_push_back_it_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.push_back(1);
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
    iterator "this" @ 0x7fff0ad7b2f0 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7fff0ad7b3b0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
./include/c++/13/bits/vector.tcc:519:7
    #5 0x55c1fe7199f0 in int& std::vector<int, std::allocator<int>>::emplace_back<int>(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:123:4
    #6 0x55c1fe7193bc in std::vector<int, std::allocator<int>>::push_back(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1299:9
    #7 0x55c1fe632118 in f_vector_push_back_it_guarda(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:87:5
    #8 0x55c1fe6cdb7a in main /work/test/runtime_runner.cpp:93:5
    #9 0x7ebe7fe931c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x7ebe7fe9328a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x55c1fe5434b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x55c1fe62cd31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x55c1fe72cc77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x55c1fe72c50f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x55c1fe72c50f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x55c1fe71a720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x55c1fe6ba187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x55c1fe6cdb6d in main /work/test/runtime_runner.cpp:92:26
    #7 0x7ebe7fe931c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x7ebe7fe9328a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x55c1fe5434b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:88:8 in f_vector_push_back_it_guarda(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7aee7f1dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7aee7f1dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7aee7f1dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7aee7f1dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7aee7f1dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7aee7f1e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7aee7f1e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7aee7f1e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7aee7f1e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7aee7f1e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7aee7f1e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==26==ABORTING
````

</details>

### f_vector_push_back_it_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_push_back_it_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.push_back(1);
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
    iterator "this" @ 0x7ffceb764470 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffceb764530
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
nclude/c++/13/bits/vector.tcc:519:7
    #5 0x5b4cbc8749f0 in int& std::vector<int, std::allocator<int>>::emplace_back<int>(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:123:4
    #6 0x5b4cbc8743bc in std::vector<int, std::allocator<int>>::push_back(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1299:9
    #7 0x5b4cbc78d763 in f_vector_push_back_it_bucle(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:100:7
    #8 0x5b4cbc828e42 in main /work/test/runtime_runner.cpp:103:5
    #9 0x7bcafa2de1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x7bcafa2de28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x5b4cbc69e4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5b4cbc787d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5b4cbc887c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5b4cbc88750f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5b4cbc88750f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x5b4cbc875720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x5b4cbc815187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x5b4cbc828e35 in main /work/test/runtime_runner.cpp:102:26
    #7 0x7bcafa2de1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x7bcafa2de28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x5b4cbc69e4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:101:10 in f_vector_push_back_it_bucle(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x77faf95dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x77faf95dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x77faf95dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x77faf95dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x77faf95dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x77faf95e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x77faf95e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x77faf95e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x77faf95e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x77faf95e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x77faf95e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==33==ABORTING
````

</details>

### f_vector_push_back_it_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_push_back_it_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_vector_push_back(c);
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
    iterator "this" @ 0x7ffd4748e940 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffd4748ea00
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
t>(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:123:4
    #6 0x5a68b8ea43bc in std::vector<int, std::allocator<int>>::push_back(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1299:9
    #7 0x5a68b8db9336 in mutar_vector_push_back(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:15:54
    #8 0x5a68b8dbdd9c in f_vector_push_back_it_llamada(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:115:3
    #9 0x5a68b8e5910a in main /work/test/runtime_runner.cpp:113:5
    #10 0x78cff0f491c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x78cff0f4928a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x5a68b8cce4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5a68b8db7d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5a68b8eb7c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5a68b8eb750f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5a68b8eb750f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x5a68b8ea5720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x5a68b8e45187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x5a68b8e590fd in main /work/test/runtime_runner.cpp:112:26
    #7 0x78cff0f491c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x78cff0f4928a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x5a68b8cce4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:116:8 in f_vector_push_back_it_llamada(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x74fff01dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x74fff01dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x74fff01dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x74fff01dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x74fff01dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x74fff01e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x74fff01e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x74fff01e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x74fff01e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x74fff01e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x74fff01e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==40==ABORTING
````

</details>

## Handle: referencia

### f_vector_push_back_ref_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_push_back_ref_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.push_back(1);
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
clude/c++/13/bits/vector.tcc:519:7
    #5 0x5cef916789f0 in int& std::vector<int, std::allocator<int>>::emplace_back<int>(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:123:4
    #6 0x5cef916783bc in std::vector<int, std::allocator<int>>::push_back(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1299:9
    #7 0x5cef91592319 in f_vector_push_back_ref_recto(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:128:5
    #8 0x5cef9162d3d8 in main /work/test/runtime_runner.cpp:123:5
    #9 0x718f572df1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x718f572df28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x5cef914a24b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5cef9158bd31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5cef9168bc77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5cef9168b50f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5cef9168b50f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x5cef91679720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x5cef91619187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x5cef9162d3cb in main /work/test/runtime_runner.cpp:122:26
    #7 0x718f572df1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x718f572df28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x5cef914a24b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:129:8 in f_vector_push_back_ref_recto(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6dbf565dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6dbf565dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6dbf565dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6dbf565dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6dbf565dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6dbf565e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x6dbf565e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6dbf565e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6dbf565e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6dbf565e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6dbf565e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==47==ABORTING
````

</details>

### f_vector_push_back_ref_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_push_back_ref_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.push_back(1);
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
ude/c++/13/bits/vector.tcc:519:7
    #5 0x5e94bccb29f0 in int& std::vector<int, std::allocator<int>>::emplace_back<int>(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:123:4
    #6 0x5e94bccb23bc in std::vector<int, std::allocator<int>>::push_back(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1299:9
    #7 0x5e94bcbcc87b in f_vector_push_back_ref_guarda(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:142:5
    #8 0x5e94bcc676c4 in main /work/test/runtime_runner.cpp:133:5
    #9 0x731399ecf1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x731399ecf28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x5e94bcadc4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5e94bcbc5d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5e94bccc5c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5e94bccc550f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5e94bccc550f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x5e94bccb3720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x5e94bcc53187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x5e94bcc676b7 in main /work/test/runtime_runner.cpp:132:26
    #7 0x731399ecf1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x731399ecf28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x5e94bcadc4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:143:8 in f_vector_push_back_ref_guarda(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6f43991dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f43991dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f43991dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f43991dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f43991dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6f43991e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x6f43991e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f43991e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f43991e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f43991e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f43991e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==54==ABORTING
````

</details>

### f_vector_push_back_ref_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_push_back_ref_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.push_back(1);
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
    iterator "this" @ 0x7ffe58ebd7f0 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffe58ebd8b0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
lude/c++/13/bits/vector.tcc:519:7
    #5 0x5f7162f2d9f0 in int& std::vector<int, std::allocator<int>>::emplace_back<int>(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:123:4
    #6 0x5f7162f2d3bc in std::vector<int, std::allocator<int>>::push_back(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1299:9
    #7 0x5f7162e47ee6 in f_vector_push_back_ref_bucle(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:157:7
    #8 0x5f7162ee29b0 in main /work/test/runtime_runner.cpp:143:5
    #9 0x77231c48f1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x77231c48f28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x5f7162d574b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5f7162e40d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5f7162f40c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5f7162f4050f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5f7162f4050f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x5f7162f2e720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x5f7162ece187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x5f7162ee29a3 in main /work/test/runtime_runner.cpp:142:26
    #7 0x77231c48f1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x77231c48f28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x5f7162d574b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:158:10 in f_vector_push_back_ref_bucle(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x73531b7dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73531b7dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73531b7dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73531b7dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73531b7dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x73531b7e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x73531b7e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x73531b7e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x73531b7e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x73531b7e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x73531b7e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==61==ABORTING
````

</details>

### f_vector_push_back_ref_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_push_back_ref_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_vector_push_back(c);
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
(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:123:4
    #6 0x60a4e1b333bc in std::vector<int, std::allocator<int>>::push_back(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1299:9
    #7 0x60a4e1a48336 in mutar_vector_push_back(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:15:54
    #8 0x60a4e1a4e555 in f_vector_push_back_ref_llamada(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:174:3
    #9 0x60a4e1ae8c9c in main /work/test/runtime_runner.cpp:153:5
    #10 0x7388ae8601c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x7388ae86028a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x60a4e195d4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x60a4e1a46d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x60a4e1b46c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x60a4e1b4650f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x60a4e1b4650f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x60a4e1b34720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x60a4e1ad4187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x60a4e1ae8c8f in main /work/test/runtime_runner.cpp:152:26
    #7 0x7388ae8601c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x7388ae86028a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x60a4e195d4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:175:8 in f_vector_push_back_ref_llamada(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6fb8adbdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6fb8adbdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6fb8adbdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6fb8adbdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6fb8adbdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6fb8adbe0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x6fb8adbe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6fb8adbe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6fb8adbe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6fb8adbe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6fb8adbe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==68==ABORTING
````

</details>

## Handle: puntero

### f_vector_push_back_ptr_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_push_back_ptr_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.push_back(1);
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
clude/c++/13/bits/vector.tcc:519:7
    #5 0x61b815bc39f0 in int& std::vector<int, std::allocator<int>>::emplace_back<int>(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:123:4
    #6 0x61b815bc33bc in std::vector<int, std::allocator<int>>::push_back(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1299:9
    #7 0x61b815adea86 in f_vector_push_back_ptr_recto(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:188:5
    #8 0x61b815b78f88 in main /work/test/runtime_runner.cpp:163:5
    #9 0x72ea040721c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x72ea0407228a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x61b8159ed4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x61b815ad6d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x61b815bd6c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x61b815bd650f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x61b815bd650f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x61b815bc4720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x61b815b64187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x61b815b78f7b in main /work/test/runtime_runner.cpp:162:26
    #7 0x72ea040721c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x72ea0407228a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x61b8159ed4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:189:8 in f_vector_push_back_ptr_recto(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6f1a033dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f1a033dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f1a033dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f1a033dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f1a033dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6f1a033e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x6f1a033e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f1a033e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f1a033e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f1a033e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f1a033e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==75==ABORTING
````

</details>

### f_vector_push_back_ptr_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_push_back_ptr_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.push_back(1);
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
ude/c++/13/bits/vector.tcc:519:7
    #5 0x64338f7e99f0 in int& std::vector<int, std::allocator<int>>::emplace_back<int>(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:123:4
    #6 0x64338f7e93bc in std::vector<int, std::allocator<int>>::push_back(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1299:9
    #7 0x64338f704fe8 in f_vector_push_back_ptr_guarda(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:202:5
    #8 0x64338f79f274 in main /work/test/runtime_runner.cpp:173:5
    #9 0x7445933d71c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x7445933d728a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x64338f6134b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x64338f6fcd31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x64338f7fcc77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x64338f7fc50f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x64338f7fc50f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x64338f7ea720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x64338f78a187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x64338f79f267 in main /work/test/runtime_runner.cpp:172:26
    #7 0x7445933d71c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x7445933d728a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x64338f6134b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:203:8 in f_vector_push_back_ptr_guarda(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7075927dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7075927dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7075927dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7075927dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7075927dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7075927e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7075927e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7075927e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7075927e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7075927e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7075927e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==82==ABORTING
````

</details>

### f_vector_push_back_ptr_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_push_back_ptr_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.push_back(1);
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
    iterator "this" @ 0x7ffd2c8cc1e0 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffd2c8cc2a0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
lude/c++/13/bits/vector.tcc:519:7
    #5 0x603ca5f389f0 in int& std::vector<int, std::allocator<int>>::emplace_back<int>(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:123:4
    #6 0x603ca5f383bc in std::vector<int, std::allocator<int>>::push_back(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1299:9
    #7 0x603ca5e54633 in f_vector_push_back_ptr_bucle(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:217:7
    #8 0x603ca5eee560 in main /work/test/runtime_runner.cpp:183:5
    #9 0x75b91ca681c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x75b91ca6828a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x603ca5d624b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x603ca5e4bd31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x603ca5f4bc77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x603ca5f4b50f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x603ca5f4b50f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x603ca5f39720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x603ca5ed9187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x603ca5eee553 in main /work/test/runtime_runner.cpp:182:26
    #7 0x75b91ca681c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x75b91ca6828a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x603ca5d624b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:218:10 in f_vector_push_back_ptr_bucle(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x71e91bddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x71e91bddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x71e91bddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x71e91bddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x71e91bddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x71e91bde0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x71e91bde0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x71e91bde0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x71e91bde0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x71e91bde0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x71e91bde0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==89==ABORTING
````

</details>

### f_vector_push_back_ptr_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_push_back_ptr_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_vector_push_back(c);
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
(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:123:4
    #6 0x6530902ac3bc in std::vector<int, std::allocator<int>>::push_back(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1299:9
    #7 0x6530901c1336 in mutar_vector_push_back(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:15:54
    #8 0x6530901c8c89 in f_vector_push_back_ptr_llamada(std::vector<int, std::allocator<int>>&) /work/test/corpus.cpp:234:3
    #9 0x65309026284c in main /work/test/runtime_runner.cpp:193:5
    #10 0x76233b8781c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x76233b87828a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x6530900d64b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x6530901bfd31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x6530902bfc77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x6530902bf50f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x6530902bf50f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x6530902ad720 in std::vector<int, std::allocator<int>>::reserve(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:79:22
    #5 0x65309024d187 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:40:7
    #6 0x65309026283f in main /work/test/runtime_runner.cpp:192:26
    #7 0x76233b8781c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #8 0x76233b87828a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x6530900d64b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:235:8 in f_vector_push_back_ptr_llamada(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x72533abdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x72533abdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x72533abdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x72533abdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x72533abdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x72533abe0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x72533abe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x72533abe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x72533abe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x72533abe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x72533abe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==96==ABORTING
````

</details>
