# `std::list::clear`

Mutación: `c.clear();`

- Iterador retenido: 🔴 `UB`
- Referencia/puntero retenido: 🔴 `UB`
- Casos `UB` detectados estáticamente: 5/12

**En palabras:** después de `c.clear();` sobre un `std::list`, un iterador guardado queda **inválido**: usarlo después es un bug (UB); una referencia o puntero guardado queda **inválido**: usarlo después es un bug (UB).

Mapa de los 12 casos. Cada celda muestra la respuesta correcta (etiqueta) y, debajo, lo que hizo el analizador estático de Clang. Clic para ir al caso. Ver [Cómo leer este libro](../../guia.md).

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🔴 `UB`<br>❌ no detectado](#f_list_clear_it_recto) | [🔴 `UB`<br>✅ detectado](#f_list_clear_it_guarda) | [🔴 `UB`<br>✅ detectado](#f_list_clear_it_bucle) | [🔴 `UB`<br>✅ detectado](#f_list_clear_it_llamada) |
| **referencia** | [🔴 `UB`<br>❌ no detectado](#f_list_clear_ref_recto) | [🔴 `UB`<br>❌ no detectado](#f_list_clear_ref_guarda) | [🔴 `UB`<br>✅ detectado](#f_list_clear_ref_bucle) | [🔴 `UB`<br>❌ no detectado](#f_list_clear_ref_llamada) |
| **puntero** | [🔴 `UB`<br>❌ no detectado](#f_list_clear_ptr_recto) | [🔴 `UB`<br>❌ no detectado](#f_list_clear_ptr_guarda) | [🔴 `UB`<br>✅ detectado](#f_list_clear_ptr_bucle) | [🔴 `UB`<br>❌ no detectado](#f_list_clear_ptr_llamada) |

## Handle: iterador

### f_list_clear_it_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_list_clear_it_recto(std::list<int>& c) {
  auto it = c.begin();
  c.clear();
  sink(*it);
}
```

> **Causa del falso negativo:** 2. Sin comparacion previa contra end(), el modelado no se activa

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | 🛑 attempt to dereference a singular iterator | 🛑 heap-use-after-free |

<details>
<summary>stderr libstdc++ Debug · <code>natural</code></summary>

````text
/usr/include/c++/13/debug/safe_iterator.h:298:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::reference 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator*() 
    const [with _Iterator = std::_List_iterator<int>; _Sequence = std::
    debug::list<int>; _Category = std::forward_iterator_tag; reference = 
    int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fff9ac20830 {
      type = std::_List_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::list<int, std::allocator<int> >' @ 0x7fff9ac208b0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
hread T0 here:
    #0 0x62e929fc9d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x62e92a0e1ee4 in std::__new_allocator<std::_List_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x62e92a0e1bb4 in std::allocator_traits<std::allocator<std::_List_node<int>>>::allocate(std::allocator<std::_List_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x62e92a0e1bb4 in std::__cxx11::_List_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:518:16
    #4 0x62e92a105755 in std::_List_node<int>* std::__cxx11::list<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:710:21
    #5 0x62e92a105570 in void std::__cxx11::list<int, std::allocator<int>>::_M_insert<int const&>(std::_List_iterator<int>, int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:2005:18
    #6 0x62e92a1054ad in int& std::__cxx11::list<int, std::allocator<int>>::emplace_back<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1321:10
    #7 0x62e92a105260 in void std::__cxx11::list<int, std::allocator<int>>::_M_initialize_dispatch<int const*>(int const*, int const*, std::__false_type) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1934:6
    #8 0x62e92a0c2121 in std::__cxx11::list<int, std::allocator<int>>::list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:837:9
    #9 0x62e92a057bb0 in make_list[abi:cxx11](Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:52:59
    #10 0x62e92a0868fb in main /work/test/runtime_runner.cpp:1642:24
    #11 0x71031adc11c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x71031adc128a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x62e929ee04b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2192:8 in f_list_clear_it_recto(std::__cxx11::list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6d3319fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d3319fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d3319fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d3319fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d3319fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6d3319fe0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa fd fd
  0x6d3319fe0080: fd fa fa fa fd fd fd fa fa fa fa fa fa fa fa fa
  0x6d3319fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d3319fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d3319fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d3319fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==901==ABORTING
````

</details>

### f_list_clear_it_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `guarda` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_list_clear_it_guarda(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.clear();
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | 🛑 attempt to dereference a singular iterator | 🛑 heap-use-after-free |

<details>
<summary>stderr libstdc++ Debug · <code>natural</code></summary>

````text
/usr/include/c++/13/debug/safe_iterator.h:298:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::reference 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator*() 
    const [with _Iterator = std::_List_iterator<int>; _Sequence = std::
    debug::list<int>; _Category = std::forward_iterator_tag; reference = 
    int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffdcf07a110 {
      type = std::_List_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::list<int, std::allocator<int> >' @ 0x7ffdcf07a1d0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
read T0 here:
    #0 0x6079b6f26d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x6079b703eee4 in std::__new_allocator<std::_List_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x6079b703ebb4 in std::allocator_traits<std::allocator<std::_List_node<int>>>::allocate(std::allocator<std::_List_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x6079b703ebb4 in std::__cxx11::_List_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:518:16
    #4 0x6079b7062755 in std::_List_node<int>* std::__cxx11::list<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:710:21
    #5 0x6079b7062570 in void std::__cxx11::list<int, std::allocator<int>>::_M_insert<int const&>(std::_List_iterator<int>, int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:2005:18
    #6 0x6079b70624ad in int& std::__cxx11::list<int, std::allocator<int>>::emplace_back<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1321:10
    #7 0x6079b7062260 in void std::__cxx11::list<int, std::allocator<int>>::_M_initialize_dispatch<int const*>(int const*, int const*, std::__false_type) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1934:6
    #8 0x6079b701f121 in std::__cxx11::list<int, std::allocator<int>>::list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:837:9
    #9 0x6079b6fb4bb0 in make_list[abi:cxx11](Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:52:59
    #10 0x6079b6fe3a31 in main /work/test/runtime_runner.cpp:1647:24
    #11 0x7b76929881c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x7b769298828a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x6079b6e3d4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2198:8 in f_list_clear_it_guarda(std::__cxx11::list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x77a691bdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x77a691bdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x77a691bdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x77a691bdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x77a691bdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x77a691be0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa fd fd
  0x77a691be0080: fd fa fa fa fd fd fd fa fa fa fa fa fa fa fa fa
  0x77a691be0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x77a691be0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x77a691be0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x77a691be0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==904==ABORTING
````

</details>

### f_list_clear_it_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_list_clear_it_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.clear();
    sink(*it);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | 🛑 attempt to dereference a singular iterator | 🛑 heap-use-after-free |

<details>
<summary>stderr libstdc++ Debug · <code>natural</code></summary>

````text
/usr/include/c++/13/debug/safe_iterator.h:298:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::reference 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator*() 
    const [with _Iterator = std::_List_iterator<int>; _Sequence = std::
    debug::list<int>; _Category = std::forward_iterator_tag; reference = 
    int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffc53159690 {
      type = std::_List_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::list<int, std::allocator<int> >' @ 0x7ffc53159750
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
read T0 here:
    #0 0x60bcdb0fcd31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x60bcdb214ee4 in std::__new_allocator<std::_List_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x60bcdb214bb4 in std::allocator_traits<std::allocator<std::_List_node<int>>>::allocate(std::allocator<std::_List_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x60bcdb214bb4 in std::__cxx11::_List_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:518:16
    #4 0x60bcdb238755 in std::_List_node<int>* std::__cxx11::list<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:710:21
    #5 0x60bcdb238570 in void std::__cxx11::list<int, std::allocator<int>>::_M_insert<int const&>(std::_List_iterator<int>, int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:2005:18
    #6 0x60bcdb2384ad in int& std::__cxx11::list<int, std::allocator<int>>::emplace_back<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1321:10
    #7 0x60bcdb238260 in void std::__cxx11::list<int, std::allocator<int>>::_M_initialize_dispatch<int const*>(int const*, int const*, std::__false_type) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1934:6
    #8 0x60bcdb1f5121 in std::__cxx11::list<int, std::allocator<int>>::list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:837:9
    #9 0x60bcdb18abb0 in make_list[abi:cxx11](Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:52:59
    #10 0x60bcdb1b9b67 in main /work/test/runtime_runner.cpp:1652:24
    #11 0x73f7a50ee1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x73f7a50ee28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x60bcdb0134b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2204:10 in f_list_clear_it_bucle(std::__cxx11::list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7027a43dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7027a43dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7027a43dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7027a43dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7027a43dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7027a43e0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa fd fd
  0x7027a43e0080: fd fa fa fa fd fd fd fa fa fa fa fa fa fa fa fa
  0x7027a43e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7027a43e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7027a43e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7027a43e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==907==ABORTING
````

</details>

### f_list_clear_it_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `llamada` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_list_clear_it_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_list_clear(c);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | 🛑 attempt to dereference a singular iterator | 🛑 heap-use-after-free |

<details>
<summary>stderr libstdc++ Debug · <code>natural</code></summary>

````text
/usr/include/c++/13/debug/safe_iterator.h:298:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::reference 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator*() 
    const [with _Iterator = std::_List_iterator<int>; _Sequence = std::
    debug::list<int>; _Category = std::forward_iterator_tag; reference = 
    int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffea9681e70 {
      type = std::_List_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::list<int, std::allocator<int> >' @ 0x7ffea9681f30
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
ead T0 here:
    #0 0x62cae0595d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x62cae06adee4 in std::__new_allocator<std::_List_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x62cae06adbb4 in std::allocator_traits<std::allocator<std::_List_node<int>>>::allocate(std::allocator<std::_List_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x62cae06adbb4 in std::__cxx11::_List_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:518:16
    #4 0x62cae06d1755 in std::_List_node<int>* std::__cxx11::list<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:710:21
    #5 0x62cae06d1570 in void std::__cxx11::list<int, std::allocator<int>>::_M_insert<int const&>(std::_List_iterator<int>, int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:2005:18
    #6 0x62cae06d14ad in int& std::__cxx11::list<int, std::allocator<int>>::emplace_back<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1321:10
    #7 0x62cae06d1260 in void std::__cxx11::list<int, std::allocator<int>>::_M_initialize_dispatch<int const*>(int const*, int const*, std::__false_type) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1934:6
    #8 0x62cae068e121 in std::__cxx11::list<int, std::allocator<int>>::list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:837:9
    #9 0x62cae0623bb0 in make_list[abi:cxx11](Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:52:59
    #10 0x62cae0652c9d in main /work/test/runtime_runner.cpp:1657:24
    #11 0x7f126e7e21c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x7f126e7e228a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x62cae04ac4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2211:8 in f_list_clear_it_llamada(std::__cxx11::list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7b426dbdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b426dbdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b426dbdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b426dbdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b426dbdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b426dbe0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa fd fd
  0x7b426dbe0080: fd fa fa fa fd fd fd fa fa fa fa fa fa fa fa fa
  0x7b426dbe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b426dbe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b426dbe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b426dbe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==910==ABORTING
````

</details>

## Handle: referencia

### f_list_clear_ref_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_list_clear_ref_recto(std::list<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.clear();
  sink(h);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | 🛑 heap-use-after-free |

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
read T0 here:
    #0 0x6000d64aad31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x6000d65c2ee4 in std::__new_allocator<std::_List_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x6000d65c2bb4 in std::allocator_traits<std::allocator<std::_List_node<int>>>::allocate(std::allocator<std::_List_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x6000d65c2bb4 in std::__cxx11::_List_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:518:16
    #4 0x6000d65e6755 in std::_List_node<int>* std::__cxx11::list<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:710:21
    #5 0x6000d65e6570 in void std::__cxx11::list<int, std::allocator<int>>::_M_insert<int const&>(std::_List_iterator<int>, int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:2005:18
    #6 0x6000d65e64ad in int& std::__cxx11::list<int, std::allocator<int>>::emplace_back<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1321:10
    #7 0x6000d65e6260 in void std::__cxx11::list<int, std::allocator<int>>::_M_initialize_dispatch<int const*>(int const*, int const*, std::__false_type) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1934:6
    #8 0x6000d65a3121 in std::__cxx11::list<int, std::allocator<int>>::list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:837:9
    #9 0x6000d6538bb0 in make_list[abi:cxx11](Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:52:59
    #10 0x6000d6567dd3 in main /work/test/runtime_runner.cpp:1662:24
    #11 0x796df46841c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x796df468428a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x6000d63c14b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2217:8 in f_list_clear_ref_recto(std::__cxx11::list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x759df39dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x759df39dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x759df39dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x759df39dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x759df39dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x759df39e0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa fd fd
  0x759df39e0080: fd fa fa fa fd fd fd fa fa fa fa fa fa fa fa fa
  0x759df39e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x759df39e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x759df39e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x759df39e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==913==ABORTING
````

</details>

### f_list_clear_ref_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_list_clear_ref_guarda(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.clear();
  sink(h);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | 🛑 heap-use-after-free |

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
ead T0 here:
    #0 0x5941f7923d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5941f7a3bee4 in std::__new_allocator<std::_List_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5941f7a3bbb4 in std::allocator_traits<std::allocator<std::_List_node<int>>>::allocate(std::allocator<std::_List_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5941f7a3bbb4 in std::__cxx11::_List_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:518:16
    #4 0x5941f7a5f755 in std::_List_node<int>* std::__cxx11::list<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:710:21
    #5 0x5941f7a5f570 in void std::__cxx11::list<int, std::allocator<int>>::_M_insert<int const&>(std::_List_iterator<int>, int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:2005:18
    #6 0x5941f7a5f4ad in int& std::__cxx11::list<int, std::allocator<int>>::emplace_back<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1321:10
    #7 0x5941f7a5f260 in void std::__cxx11::list<int, std::allocator<int>>::_M_initialize_dispatch<int const*>(int const*, int const*, std::__false_type) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1934:6
    #8 0x5941f7a1c121 in std::__cxx11::list<int, std::allocator<int>>::list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:837:9
    #9 0x5941f79b1bb0 in make_list[abi:cxx11](Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:52:59
    #10 0x5941f79e0f09 in main /work/test/runtime_runner.cpp:1667:24
    #11 0x7329de9a21c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x7329de9a228a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x5941f783a4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2224:8 in f_list_clear_ref_guarda(std::__cxx11::list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6f59ddbdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f59ddbdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f59ddbdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f59ddbdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f59ddbdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6f59ddbe0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa fd fd
  0x6f59ddbe0080: fd fa fa fa fd fd fd fa fa fa fa fa fa fa fa fa
  0x6f59ddbe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f59ddbe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f59ddbe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f59ddbe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==916==ABORTING
````

</details>

### f_list_clear_ref_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `bucle` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_list_clear_ref_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.clear();
    sink(h);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | 🛑 attempt to increment a singular iterator | 🛑 heap-use-after-free |

<details>
<summary>stderr libstdc++ Debug · <code>natural</code></summary>

````text
/usr/include/c++/13/debug/safe_iterator.h:326:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>& 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator++() 
    [with _Iterator = std::_List_iterator<int>; _Sequence = std::
    debug::list<int>; _Category = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffe6f6cc1e0 {
      type = std::_List_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::list<int, std::allocator<int> >' @ 0x7ffe6f6cc2a0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
ead T0 here:
    #0 0x5677e54d4d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5677e55ecee4 in std::__new_allocator<std::_List_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5677e55ecbb4 in std::allocator_traits<std::allocator<std::_List_node<int>>>::allocate(std::allocator<std::_List_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5677e55ecbb4 in std::__cxx11::_List_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:518:16
    #4 0x5677e5610755 in std::_List_node<int>* std::__cxx11::list<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:710:21
    #5 0x5677e5610570 in void std::__cxx11::list<int, std::allocator<int>>::_M_insert<int const&>(std::_List_iterator<int>, int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:2005:18
    #6 0x5677e56104ad in int& std::__cxx11::list<int, std::allocator<int>>::emplace_back<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1321:10
    #7 0x5677e5610260 in void std::__cxx11::list<int, std::allocator<int>>::_M_initialize_dispatch<int const*>(int const*, int const*, std::__false_type) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1934:6
    #8 0x5677e55cd121 in std::__cxx11::list<int, std::allocator<int>>::list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:837:9
    #9 0x5677e5562bb0 in make_list[abi:cxx11](Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:52:59
    #10 0x5677e559203f in main /work/test/runtime_runner.cpp:1672:24
    #11 0x7b4de41ca1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x7b4de41ca28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x5677e53eb4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2231:10 in f_list_clear_ref_bucle(std::__cxx11::list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x777de33dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x777de33dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x777de33dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x777de33dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x777de33dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x777de33e0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa fd fd
  0x777de33e0080: fd fa fa fa fd fd fd fa fa fa fa fa fa fa fa fa
  0x777de33e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x777de33e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x777de33e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x777de33e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==919==ABORTING
````

</details>

### f_list_clear_ref_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_list_clear_ref_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_list_clear(c);
  sink(h);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | 🛑 heap-use-after-free |

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
ad T0 here:
    #0 0x609511b6bd31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x609511c83ee4 in std::__new_allocator<std::_List_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x609511c83bb4 in std::allocator_traits<std::allocator<std::_List_node<int>>>::allocate(std::allocator<std::_List_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x609511c83bb4 in std::__cxx11::_List_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:518:16
    #4 0x609511ca7755 in std::_List_node<int>* std::__cxx11::list<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:710:21
    #5 0x609511ca7570 in void std::__cxx11::list<int, std::allocator<int>>::_M_insert<int const&>(std::_List_iterator<int>, int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:2005:18
    #6 0x609511ca74ad in int& std::__cxx11::list<int, std::allocator<int>>::emplace_back<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1321:10
    #7 0x609511ca7260 in void std::__cxx11::list<int, std::allocator<int>>::_M_initialize_dispatch<int const*>(int const*, int const*, std::__false_type) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1934:6
    #8 0x609511c64121 in std::__cxx11::list<int, std::allocator<int>>::list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:837:9
    #9 0x609511bf9bb0 in make_list[abi:cxx11](Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:52:59
    #10 0x609511c29175 in main /work/test/runtime_runner.cpp:1677:24
    #11 0x72bc5d7631c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x72bc5d76328a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x609511a824b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2239:8 in f_list_clear_ref_llamada(std::__cxx11::list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6eec5c9dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6eec5c9dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6eec5c9dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6eec5c9dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6eec5c9dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6eec5c9e0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa fd fd
  0x6eec5c9e0080: fd fa fa fa fd fd fd fa fa fa fa fa fa fa fa fa
  0x6eec5c9e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6eec5c9e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6eec5c9e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6eec5c9e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==922==ABORTING
````

</details>

## Handle: puntero

### f_list_clear_ptr_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_list_clear_ptr_recto(std::list<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.clear();
  sink(*h);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | 🛑 heap-use-after-free |

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
read T0 here:
    #0 0x57d2ad11fd31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x57d2ad237ee4 in std::__new_allocator<std::_List_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x57d2ad237bb4 in std::allocator_traits<std::allocator<std::_List_node<int>>>::allocate(std::allocator<std::_List_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x57d2ad237bb4 in std::__cxx11::_List_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:518:16
    #4 0x57d2ad25b755 in std::_List_node<int>* std::__cxx11::list<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:710:21
    #5 0x57d2ad25b570 in void std::__cxx11::list<int, std::allocator<int>>::_M_insert<int const&>(std::_List_iterator<int>, int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:2005:18
    #6 0x57d2ad25b4ad in int& std::__cxx11::list<int, std::allocator<int>>::emplace_back<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1321:10
    #7 0x57d2ad25b260 in void std::__cxx11::list<int, std::allocator<int>>::_M_initialize_dispatch<int const*>(int const*, int const*, std::__false_type) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1934:6
    #8 0x57d2ad218121 in std::__cxx11::list<int, std::allocator<int>>::list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:837:9
    #9 0x57d2ad1adbb0 in make_list[abi:cxx11](Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:52:59
    #10 0x57d2ad1dd2ab in main /work/test/runtime_runner.cpp:1682:24
    #11 0x796eaccaf1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x796eaccaf28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x57d2ad0364b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2245:8 in f_list_clear_ptr_recto(std::__cxx11::list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x759eabfdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x759eabfdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x759eabfdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x759eabfdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x759eabfdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x759eabfe0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa fd fd
  0x759eabfe0080: fd fa fa fa fd fd fd fa fa fa fa fa fa fa fa fa
  0x759eabfe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x759eabfe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x759eabfe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x759eabfe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==925==ABORTING
````

</details>

### f_list_clear_ptr_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_list_clear_ptr_guarda(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.clear();
  sink(*h);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | 🛑 heap-use-after-free |

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
ead T0 here:
    #0 0x646dd37b7d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x646dd38cfee4 in std::__new_allocator<std::_List_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x646dd38cfbb4 in std::allocator_traits<std::allocator<std::_List_node<int>>>::allocate(std::allocator<std::_List_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x646dd38cfbb4 in std::__cxx11::_List_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:518:16
    #4 0x646dd38f3755 in std::_List_node<int>* std::__cxx11::list<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:710:21
    #5 0x646dd38f3570 in void std::__cxx11::list<int, std::allocator<int>>::_M_insert<int const&>(std::_List_iterator<int>, int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:2005:18
    #6 0x646dd38f34ad in int& std::__cxx11::list<int, std::allocator<int>>::emplace_back<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1321:10
    #7 0x646dd38f3260 in void std::__cxx11::list<int, std::allocator<int>>::_M_initialize_dispatch<int const*>(int const*, int const*, std::__false_type) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1934:6
    #8 0x646dd38b0121 in std::__cxx11::list<int, std::allocator<int>>::list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:837:9
    #9 0x646dd3845bb0 in make_list[abi:cxx11](Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:52:59
    #10 0x646dd38753e1 in main /work/test/runtime_runner.cpp:1687:24
    #11 0x71c41410a1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x71c41410a28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x646dd36ce4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2252:8 in f_list_clear_ptr_guarda(std::__cxx11::list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6df4133dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6df4133dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6df4133dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6df4133dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6df4133dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6df4133e0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa fd fd
  0x6df4133e0080: fd fa fa fa fd fd fd fa fa fa fa fa fa fa fa fa
  0x6df4133e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6df4133e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6df4133e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6df4133e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==928==ABORTING
````

</details>

### f_list_clear_ptr_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `bucle` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_list_clear_ptr_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.clear();
    sink(*h);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | 🛑 attempt to increment a singular iterator | 🛑 heap-use-after-free |

<details>
<summary>stderr libstdc++ Debug · <code>natural</code></summary>

````text
/usr/include/c++/13/debug/safe_iterator.h:326:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>& 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator++() 
    [with _Iterator = std::_List_iterator<int>; _Sequence = std::
    debug::list<int>; _Category = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffcfacce470 {
      type = std::_List_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::list<int, std::allocator<int> >' @ 0x7ffcfacce530
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
ead T0 here:
    #0 0x5f9217afbd31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5f9217c13ee4 in std::__new_allocator<std::_List_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5f9217c13bb4 in std::allocator_traits<std::allocator<std::_List_node<int>>>::allocate(std::allocator<std::_List_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5f9217c13bb4 in std::__cxx11::_List_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:518:16
    #4 0x5f9217c37755 in std::_List_node<int>* std::__cxx11::list<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:710:21
    #5 0x5f9217c37570 in void std::__cxx11::list<int, std::allocator<int>>::_M_insert<int const&>(std::_List_iterator<int>, int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:2005:18
    #6 0x5f9217c374ad in int& std::__cxx11::list<int, std::allocator<int>>::emplace_back<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1321:10
    #7 0x5f9217c37260 in void std::__cxx11::list<int, std::allocator<int>>::_M_initialize_dispatch<int const*>(int const*, int const*, std::__false_type) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1934:6
    #8 0x5f9217bf4121 in std::__cxx11::list<int, std::allocator<int>>::list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:837:9
    #9 0x5f9217b89bb0 in make_list[abi:cxx11](Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:52:59
    #10 0x5f9217bb9517 in main /work/test/runtime_runner.cpp:1692:24
    #11 0x7f2e2f1a41c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x7f2e2f1a428a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x5f9217a124b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2259:10 in f_list_clear_ptr_bucle(std::__cxx11::list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7b5e2e3dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b5e2e3dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b5e2e3dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b5e2e3dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b5e2e3dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b5e2e3e0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa fd fd
  0x7b5e2e3e0080: fd fa fa fa fd fd fd fa fa fa fa fa fa fa fa fa
  0x7b5e2e3e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b5e2e3e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b5e2e3e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b5e2e3e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==931==ABORTING
````

</details>

### f_list_clear_ptr_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_list_clear_ptr_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_list_clear(c);
  sink(*h);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | 🛑 heap-use-after-free |

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
ad T0 here:
    #0 0x5de9434d3d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5de9435ebee4 in std::__new_allocator<std::_List_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5de9435ebbb4 in std::allocator_traits<std::allocator<std::_List_node<int>>>::allocate(std::allocator<std::_List_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5de9435ebbb4 in std::__cxx11::_List_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:518:16
    #4 0x5de94360f755 in std::_List_node<int>* std::__cxx11::list<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:710:21
    #5 0x5de94360f570 in void std::__cxx11::list<int, std::allocator<int>>::_M_insert<int const&>(std::_List_iterator<int>, int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:2005:18
    #6 0x5de94360f4ad in int& std::__cxx11::list<int, std::allocator<int>>::emplace_back<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1321:10
    #7 0x5de94360f260 in void std::__cxx11::list<int, std::allocator<int>>::_M_initialize_dispatch<int const*>(int const*, int const*, std::__false_type) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1934:6
    #8 0x5de9435cc121 in std::__cxx11::list<int, std::allocator<int>>::list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:837:9
    #9 0x5de943561bb0 in make_list[abi:cxx11](Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:52:59
    #10 0x5de94359164d in main /work/test/runtime_runner.cpp:1697:24
    #11 0x70d18745d1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x70d18745d28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x5de9433ea4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2267:8 in f_list_clear_ptr_llamada(std::__cxx11::list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6d01867dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d01867dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d01867dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d01867dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d01867dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6d01867e0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa fd fd
  0x6d01867e0080: fd fa fa fa fd fd fd fa fa fa fa fa fa fa fa fa
  0x6d01867e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d01867e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d01867e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d01867e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==934==ABORTING
````

</details>
