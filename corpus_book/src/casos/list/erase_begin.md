# `std::list::erase_begin`

Mutación: `c.erase(c.begin());`

- Iterador retenido: 🔴 `UB`
- Referencia/puntero retenido: 🔴 `UB`
- Casos `UB` detectados estáticamente: 0/12

**En palabras:** después de `c.erase(c.begin());` sobre un `std::list`, un iterador guardado queda **inválido**: usarlo después es un bug (UB); una referencia o puntero guardado queda **inválido**: usarlo después es un bug (UB).

Mapa de los 12 casos. Cada celda muestra la respuesta correcta (etiqueta) y, debajo, lo que hizo el analizador estático de Clang. Clic para ir al caso. Ver [Cómo leer este libro](../../guia.md).

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🔴 `UB`<br>❌ no detectado](#f_list_erase_begin_it_recto) | [🔴 `UB`<br>❌ no detectado](#f_list_erase_begin_it_guarda) | [🔴 `UB`<br>❌ no detectado](#f_list_erase_begin_it_bucle) | [🔴 `UB`<br>❌ no detectado](#f_list_erase_begin_it_llamada) |
| **referencia** | [🔴 `UB`<br>❌ no detectado](#f_list_erase_begin_ref_recto) | [🔴 `UB`<br>❌ no detectado](#f_list_erase_begin_ref_guarda) | [🔴 `UB`<br>❌ no detectado](#f_list_erase_begin_ref_bucle) | [🔴 `UB`<br>❌ no detectado](#f_list_erase_begin_ref_llamada) |
| **puntero** | [🔴 `UB`<br>❌ no detectado](#f_list_erase_begin_ptr_recto) | [🔴 `UB`<br>❌ no detectado](#f_list_erase_begin_ptr_guarda) | [🔴 `UB`<br>❌ no detectado](#f_list_erase_begin_ptr_bucle) | [🔴 `UB`<br>❌ no detectado](#f_list_erase_begin_ptr_llamada) |

## Handle: iterador

### f_list_erase_begin_it_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_list_erase_begin_it_recto(std::list<int>& c) {
  auto it = c.begin();
  c.erase(c.begin());
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
    iterator "this" @ 0x7ffc8cc2e060 {
      type = std::_List_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::list<int, std::allocator<int> >' @ 0x7ffc8cc2e170
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
T0 here:
    #0 0x62c85b676d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x62c85b78eee4 in std::__new_allocator<std::_List_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x62c85b78ebb4 in std::allocator_traits<std::allocator<std::_List_node<int>>>::allocate(std::allocator<std::_List_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x62c85b78ebb4 in std::__cxx11::_List_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:518:16
    #4 0x62c85b7b2755 in std::_List_node<int>* std::__cxx11::list<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:710:21
    #5 0x62c85b7b2570 in void std::__cxx11::list<int, std::allocator<int>>::_M_insert<int const&>(std::_List_iterator<int>, int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:2005:18
    #6 0x62c85b7b24ad in int& std::__cxx11::list<int, std::allocator<int>>::emplace_back<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1321:10
    #7 0x62c85b7b2260 in void std::__cxx11::list<int, std::allocator<int>>::_M_initialize_dispatch<int const*>(int const*, int const*, std::__false_type) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1934:6
    #8 0x62c85b76f121 in std::__cxx11::list<int, std::allocator<int>>::list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:837:9
    #9 0x62c85b704bb0 in make_list[abi:cxx11](Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:52:59
    #10 0x62c85b732a73 in main /work/test/runtime_runner.cpp:1582:24
    #11 0x7852a5eb51c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x7852a5eb528a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x62c85b58d4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2112:8 in f_list_erase_begin_it_recto(std::__cxx11::list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7482a51dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7482a51dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7482a51dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7482a51dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7482a51dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7482a51e0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x7482a51e0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7482a51e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7482a51e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7482a51e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7482a51e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==865==ABORTING
````

</details>

### f_list_erase_begin_it_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_list_erase_begin_it_guarda(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.erase(c.begin());
  sink(*it);
}
```

> **Causa del falso negativo:** 3. Se invalida por identidad del iterador, no por posicion

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
    iterator "this" @ 0x7fffa3d33060 {
      type = std::_List_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::list<int, std::allocator<int> >' @ 0x7fffa3d33180
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
0 here:
    #0 0x5e9f3a92ad31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5e9f3aa42ee4 in std::__new_allocator<std::_List_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5e9f3aa42bb4 in std::allocator_traits<std::allocator<std::_List_node<int>>>::allocate(std::allocator<std::_List_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5e9f3aa42bb4 in std::__cxx11::_List_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:518:16
    #4 0x5e9f3aa66755 in std::_List_node<int>* std::__cxx11::list<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:710:21
    #5 0x5e9f3aa66570 in void std::__cxx11::list<int, std::allocator<int>>::_M_insert<int const&>(std::_List_iterator<int>, int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:2005:18
    #6 0x5e9f3aa664ad in int& std::__cxx11::list<int, std::allocator<int>>::emplace_back<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1321:10
    #7 0x5e9f3aa66260 in void std::__cxx11::list<int, std::allocator<int>>::_M_initialize_dispatch<int const*>(int const*, int const*, std::__false_type) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1934:6
    #8 0x5e9f3aa23121 in std::__cxx11::list<int, std::allocator<int>>::list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:837:9
    #9 0x5e9f3a9b8bb0 in make_list[abi:cxx11](Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:52:59
    #10 0x5e9f3a9e6ba9 in main /work/test/runtime_runner.cpp:1587:24
    #11 0x7925388dc1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x7925388dc28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x5e9f3a8414b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2118:8 in f_list_erase_begin_it_guarda(std::__cxx11::list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x755537bdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x755537bdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x755537bdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x755537bdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x755537bdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x755537be0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x755537be0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x755537be0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x755537be0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x755537be0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x755537be0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==868==ABORTING
````

</details>

### f_list_erase_begin_it_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_list_erase_begin_it_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.erase(c.begin());
    sink(*it);
  }
}
```

> **Causa del falso negativo:** 3. Se invalida por identidad del iterador, no por posicion

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
    iterator "this" @ 0x7ffd7bd93700 {
      type = std::_List_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::list<int, std::allocator<int> >' @ 0x7ffd7bd93820
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
0 here:
    #0 0x5c00d6ce3d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5c00d6dfbee4 in std::__new_allocator<std::_List_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5c00d6dfbbb4 in std::allocator_traits<std::allocator<std::_List_node<int>>>::allocate(std::allocator<std::_List_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5c00d6dfbbb4 in std::__cxx11::_List_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:518:16
    #4 0x5c00d6e1f755 in std::_List_node<int>* std::__cxx11::list<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:710:21
    #5 0x5c00d6e1f570 in void std::__cxx11::list<int, std::allocator<int>>::_M_insert<int const&>(std::_List_iterator<int>, int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:2005:18
    #6 0x5c00d6e1f4ad in int& std::__cxx11::list<int, std::allocator<int>>::emplace_back<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1321:10
    #7 0x5c00d6e1f260 in void std::__cxx11::list<int, std::allocator<int>>::_M_initialize_dispatch<int const*>(int const*, int const*, std::__false_type) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1934:6
    #8 0x5c00d6ddc121 in std::__cxx11::list<int, std::allocator<int>>::list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:837:9
    #9 0x5c00d6d71bb0 in make_list[abi:cxx11](Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:52:59
    #10 0x5c00d6d9fcdf in main /work/test/runtime_runner.cpp:1592:24
    #11 0x7510e46c11c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x7510e46c128a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x5c00d6bfa4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2124:10 in f_list_erase_begin_it_bucle(std::__cxx11::list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7140e39dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7140e39dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7140e39dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7140e39dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7140e39dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7140e39e0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x7140e39e0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7140e39e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7140e39e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7140e39e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7140e39e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==871==ABORTING
````

</details>

### f_list_erase_begin_it_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_list_erase_begin_it_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_list_erase_begin(c);
  sink(*it);
}
```

> **Causa del falso negativo:** 3. Se invalida por identidad del iterador, no por posicion

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
    iterator "this" @ 0x7ffdc5742810 {
      type = std::_List_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::list<int, std::allocator<int> >' @ 0x7ffdc57428d0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
 here:
    #0 0x65003008bd31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x6500301a3ee4 in std::__new_allocator<std::_List_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x6500301a3bb4 in std::allocator_traits<std::allocator<std::_List_node<int>>>::allocate(std::allocator<std::_List_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x6500301a3bb4 in std::__cxx11::_List_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:518:16
    #4 0x6500301c7755 in std::_List_node<int>* std::__cxx11::list<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:710:21
    #5 0x6500301c7570 in void std::__cxx11::list<int, std::allocator<int>>::_M_insert<int const&>(std::_List_iterator<int>, int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:2005:18
    #6 0x6500301c74ad in int& std::__cxx11::list<int, std::allocator<int>>::emplace_back<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1321:10
    #7 0x6500301c7260 in void std::__cxx11::list<int, std::allocator<int>>::_M_initialize_dispatch<int const*>(int const*, int const*, std::__false_type) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1934:6
    #8 0x650030184121 in std::__cxx11::list<int, std::allocator<int>>::list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:837:9
    #9 0x650030119bb0 in make_list[abi:cxx11](Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:52:59
    #10 0x650030147e15 in main /work/test/runtime_runner.cpp:1597:24
    #11 0x7c08cb15f1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x7c08cb15f28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x65002ffa24b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2131:8 in f_list_erase_begin_it_llamada(std::__cxx11::list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7838ca3dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7838ca3dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7838ca3dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7838ca3dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7838ca3dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7838ca3e0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x7838ca3e0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7838ca3e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7838ca3e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7838ca3e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7838ca3e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==874==ABORTING
````

</details>

## Handle: referencia

### f_list_erase_begin_ref_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_list_erase_begin_ref_recto(std::list<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.erase(c.begin());
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
0 here:
    #0 0x5df1c8bb8d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5df1c8cd0ee4 in std::__new_allocator<std::_List_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5df1c8cd0bb4 in std::allocator_traits<std::allocator<std::_List_node<int>>>::allocate(std::allocator<std::_List_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5df1c8cd0bb4 in std::__cxx11::_List_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:518:16
    #4 0x5df1c8cf4755 in std::_List_node<int>* std::__cxx11::list<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:710:21
    #5 0x5df1c8cf4570 in void std::__cxx11::list<int, std::allocator<int>>::_M_insert<int const&>(std::_List_iterator<int>, int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:2005:18
    #6 0x5df1c8cf44ad in int& std::__cxx11::list<int, std::allocator<int>>::emplace_back<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1321:10
    #7 0x5df1c8cf4260 in void std::__cxx11::list<int, std::allocator<int>>::_M_initialize_dispatch<int const*>(int const*, int const*, std::__false_type) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1934:6
    #8 0x5df1c8cb1121 in std::__cxx11::list<int, std::allocator<int>>::list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:837:9
    #9 0x5df1c8c46bb0 in make_list[abi:cxx11](Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:52:59
    #10 0x5df1c8c74f4b in main /work/test/runtime_runner.cpp:1602:24
    #11 0x7b1782f321c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x7b1782f3228a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x5df1c8acf4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2137:8 in f_list_erase_begin_ref_recto(std::__cxx11::list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7747821dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7747821dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7747821dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7747821dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7747821dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7747821e0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x7747821e0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7747821e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7747821e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7747821e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7747821e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==877==ABORTING
````

</details>

### f_list_erase_begin_ref_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_list_erase_begin_ref_guarda(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.erase(c.begin());
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
 here:
    #0 0x6522111e5d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x6522112fdee4 in std::__new_allocator<std::_List_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x6522112fdbb4 in std::allocator_traits<std::allocator<std::_List_node<int>>>::allocate(std::allocator<std::_List_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x6522112fdbb4 in std::__cxx11::_List_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:518:16
    #4 0x652211321755 in std::_List_node<int>* std::__cxx11::list<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:710:21
    #5 0x652211321570 in void std::__cxx11::list<int, std::allocator<int>>::_M_insert<int const&>(std::_List_iterator<int>, int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:2005:18
    #6 0x6522113214ad in int& std::__cxx11::list<int, std::allocator<int>>::emplace_back<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1321:10
    #7 0x652211321260 in void std::__cxx11::list<int, std::allocator<int>>::_M_initialize_dispatch<int const*>(int const*, int const*, std::__false_type) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1934:6
    #8 0x6522112de121 in std::__cxx11::list<int, std::allocator<int>>::list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:837:9
    #9 0x652211273bb0 in make_list[abi:cxx11](Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:52:59
    #10 0x6522112a2081 in main /work/test/runtime_runner.cpp:1607:24
    #11 0x777d7581f1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x777d7581f28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x6522110fc4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2144:8 in f_list_erase_begin_ref_guarda(std::__cxx11::list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x73ad74bdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73ad74bdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73ad74bdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73ad74bdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73ad74bdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x73ad74be0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x73ad74be0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x73ad74be0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x73ad74be0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x73ad74be0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x73ad74be0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==880==ABORTING
````

</details>

### f_list_erase_begin_ref_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `bucle` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_list_erase_begin_ref_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.erase(c.begin());
    sink(h);
  }
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

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
    iterator "this" @ 0x7ffd195ec510 {
      type = std::_List_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::list<int, std::allocator<int> >' @ 0x7ffd195ec630
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
 here:
    #0 0x5d2716c78d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5d2716d90ee4 in std::__new_allocator<std::_List_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5d2716d90bb4 in std::allocator_traits<std::allocator<std::_List_node<int>>>::allocate(std::allocator<std::_List_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5d2716d90bb4 in std::__cxx11::_List_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:518:16
    #4 0x5d2716db4755 in std::_List_node<int>* std::__cxx11::list<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:710:21
    #5 0x5d2716db4570 in void std::__cxx11::list<int, std::allocator<int>>::_M_insert<int const&>(std::_List_iterator<int>, int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:2005:18
    #6 0x5d2716db44ad in int& std::__cxx11::list<int, std::allocator<int>>::emplace_back<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1321:10
    #7 0x5d2716db4260 in void std::__cxx11::list<int, std::allocator<int>>::_M_initialize_dispatch<int const*>(int const*, int const*, std::__false_type) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1934:6
    #8 0x5d2716d71121 in std::__cxx11::list<int, std::allocator<int>>::list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:837:9
    #9 0x5d2716d06bb0 in make_list[abi:cxx11](Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:52:59
    #10 0x5d2716d351b7 in main /work/test/runtime_runner.cpp:1612:24
    #11 0x7ecf35a721c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x7ecf35a7228a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x5d2716b8f4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2151:10 in f_list_erase_begin_ref_bucle(std::__cxx11::list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7aff34ddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7aff34ddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7aff34ddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7aff34ddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7aff34ddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7aff34de0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x7aff34de0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7aff34de0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7aff34de0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7aff34de0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7aff34de0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==883==ABORTING
````

</details>

### f_list_erase_begin_ref_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_list_erase_begin_ref_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_list_erase_begin(c);
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
here:
    #0 0x56a7338d2d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x56a7339eaee4 in std::__new_allocator<std::_List_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x56a7339eabb4 in std::allocator_traits<std::allocator<std::_List_node<int>>>::allocate(std::allocator<std::_List_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x56a7339eabb4 in std::__cxx11::_List_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:518:16
    #4 0x56a733a0e755 in std::_List_node<int>* std::__cxx11::list<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:710:21
    #5 0x56a733a0e570 in void std::__cxx11::list<int, std::allocator<int>>::_M_insert<int const&>(std::_List_iterator<int>, int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:2005:18
    #6 0x56a733a0e4ad in int& std::__cxx11::list<int, std::allocator<int>>::emplace_back<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1321:10
    #7 0x56a733a0e260 in void std::__cxx11::list<int, std::allocator<int>>::_M_initialize_dispatch<int const*>(int const*, int const*, std::__false_type) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1934:6
    #8 0x56a7339cb121 in std::__cxx11::list<int, std::allocator<int>>::list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:837:9
    #9 0x56a733960bb0 in make_list[abi:cxx11](Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:52:59
    #10 0x56a73398f2ed in main /work/test/runtime_runner.cpp:1617:24
    #11 0x73c2fcb0a1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x73c2fcb0a28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x56a7337e94b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2159:8 in f_list_erase_begin_ref_llamada(std::__cxx11::list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6ff2fbddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6ff2fbddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6ff2fbddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6ff2fbddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6ff2fbddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6ff2fbde0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x6ff2fbde0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x6ff2fbde0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6ff2fbde0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6ff2fbde0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6ff2fbde0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==886==ABORTING
````

</details>

## Handle: puntero

### f_list_erase_begin_ptr_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_list_erase_begin_ptr_recto(std::list<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.erase(c.begin());
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
0 here:
    #0 0x5958a70a1d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5958a71b9ee4 in std::__new_allocator<std::_List_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5958a71b9bb4 in std::allocator_traits<std::allocator<std::_List_node<int>>>::allocate(std::allocator<std::_List_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5958a71b9bb4 in std::__cxx11::_List_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:518:16
    #4 0x5958a71dd755 in std::_List_node<int>* std::__cxx11::list<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:710:21
    #5 0x5958a71dd570 in void std::__cxx11::list<int, std::allocator<int>>::_M_insert<int const&>(std::_List_iterator<int>, int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:2005:18
    #6 0x5958a71dd4ad in int& std::__cxx11::list<int, std::allocator<int>>::emplace_back<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1321:10
    #7 0x5958a71dd260 in void std::__cxx11::list<int, std::allocator<int>>::_M_initialize_dispatch<int const*>(int const*, int const*, std::__false_type) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1934:6
    #8 0x5958a719a121 in std::__cxx11::list<int, std::allocator<int>>::list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:837:9
    #9 0x5958a712fbb0 in make_list[abi:cxx11](Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:52:59
    #10 0x5958a715e423 in main /work/test/runtime_runner.cpp:1622:24
    #11 0x72a4d807a1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x72a4d807a28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x5958a6fb84b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2165:8 in f_list_erase_begin_ptr_recto(std::__cxx11::list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6ed4d73dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6ed4d73dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6ed4d73dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6ed4d73dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6ed4d73dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6ed4d73e0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x6ed4d73e0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x6ed4d73e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6ed4d73e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6ed4d73e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6ed4d73e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==889==ABORTING
````

</details>

### f_list_erase_begin_ptr_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_list_erase_begin_ptr_guarda(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.erase(c.begin());
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
 here:
    #0 0x58248ea3dd31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x58248eb55ee4 in std::__new_allocator<std::_List_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x58248eb55bb4 in std::allocator_traits<std::allocator<std::_List_node<int>>>::allocate(std::allocator<std::_List_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x58248eb55bb4 in std::__cxx11::_List_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:518:16
    #4 0x58248eb79755 in std::_List_node<int>* std::__cxx11::list<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:710:21
    #5 0x58248eb79570 in void std::__cxx11::list<int, std::allocator<int>>::_M_insert<int const&>(std::_List_iterator<int>, int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:2005:18
    #6 0x58248eb794ad in int& std::__cxx11::list<int, std::allocator<int>>::emplace_back<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1321:10
    #7 0x58248eb79260 in void std::__cxx11::list<int, std::allocator<int>>::_M_initialize_dispatch<int const*>(int const*, int const*, std::__false_type) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1934:6
    #8 0x58248eb36121 in std::__cxx11::list<int, std::allocator<int>>::list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:837:9
    #9 0x58248eacbbb0 in make_list[abi:cxx11](Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:52:59
    #10 0x58248eafa559 in main /work/test/runtime_runner.cpp:1627:24
    #11 0x7156ab54a1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x7156ab54a28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x58248e9544b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2172:8 in f_list_erase_begin_ptr_guarda(std::__cxx11::list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6d86aa7dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d86aa7dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d86aa7dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d86aa7dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d86aa7dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6d86aa7e0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x6d86aa7e0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x6d86aa7e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d86aa7e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d86aa7e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d86aa7e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==892==ABORTING
````

</details>

### f_list_erase_begin_ptr_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `bucle` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_list_erase_begin_ptr_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.erase(c.begin());
    sink(*h);
  }
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

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
    iterator "this" @ 0x7fff4b35b730 {
      type = std::_List_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::list<int, std::allocator<int> >' @ 0x7fff4b35b850
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
 here:
    #0 0x57d05b5d8d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x57d05b6f0ee4 in std::__new_allocator<std::_List_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x57d05b6f0bb4 in std::allocator_traits<std::allocator<std::_List_node<int>>>::allocate(std::allocator<std::_List_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x57d05b6f0bb4 in std::__cxx11::_List_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:518:16
    #4 0x57d05b714755 in std::_List_node<int>* std::__cxx11::list<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:710:21
    #5 0x57d05b714570 in void std::__cxx11::list<int, std::allocator<int>>::_M_insert<int const&>(std::_List_iterator<int>, int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:2005:18
    #6 0x57d05b7144ad in int& std::__cxx11::list<int, std::allocator<int>>::emplace_back<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1321:10
    #7 0x57d05b714260 in void std::__cxx11::list<int, std::allocator<int>>::_M_initialize_dispatch<int const*>(int const*, int const*, std::__false_type) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1934:6
    #8 0x57d05b6d1121 in std::__cxx11::list<int, std::allocator<int>>::list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:837:9
    #9 0x57d05b666bb0 in make_list[abi:cxx11](Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:52:59
    #10 0x57d05b69568f in main /work/test/runtime_runner.cpp:1632:24
    #11 0x7e9caec911c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x7e9caec9128a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x57d05b4ef4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2179:10 in f_list_erase_begin_ptr_bucle(std::__cxx11::list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7accadfdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7accadfdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7accadfdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7accadfdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7accadfdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7accadfe0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x7accadfe0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7accadfe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7accadfe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7accadfe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7accadfe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==895==ABORTING
````

</details>

### f_list_erase_begin_ptr_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_list_erase_begin_ptr_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_list_erase_begin(c);
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
here:
    #0 0x55b056318d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x55b056430ee4 in std::__new_allocator<std::_List_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x55b056430bb4 in std::allocator_traits<std::allocator<std::_List_node<int>>>::allocate(std::allocator<std::_List_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x55b056430bb4 in std::__cxx11::_List_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:518:16
    #4 0x55b056454755 in std::_List_node<int>* std::__cxx11::list<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:710:21
    #5 0x55b056454570 in void std::__cxx11::list<int, std::allocator<int>>::_M_insert<int const&>(std::_List_iterator<int>, int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:2005:18
    #6 0x55b0564544ad in int& std::__cxx11::list<int, std::allocator<int>>::emplace_back<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1321:10
    #7 0x55b056454260 in void std::__cxx11::list<int, std::allocator<int>>::_M_initialize_dispatch<int const*>(int const*, int const*, std::__false_type) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1934:6
    #8 0x55b056411121 in std::__cxx11::list<int, std::allocator<int>>::list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:837:9
    #9 0x55b0563a6bb0 in make_list[abi:cxx11](Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:52:59
    #10 0x55b0563d57c5 in main /work/test/runtime_runner.cpp:1637:24
    #11 0x7176229e91c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x7176229e928a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x55b05622f4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2187:8 in f_list_erase_begin_ptr_llamada(std::__cxx11::list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6da621ddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6da621ddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6da621ddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6da621ddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6da621ddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6da621de0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x6da621de0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x6da621de0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6da621de0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6da621de0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6da621de0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==898==ABORTING
````

</details>
