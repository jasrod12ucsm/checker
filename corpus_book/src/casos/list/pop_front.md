# `std::list::pop_front`

Mutación: `c.pop_front();`

- Iterador retenido: 🔴 `UB`
- Referencia/puntero retenido: 🔴 `UB`
- Casos `UB` detectados estáticamente: 0/12

**En palabras:** después de `c.pop_front();` sobre un `std::list`, un iterador guardado queda **inválido**: usarlo después es un bug (UB); una referencia o puntero guardado queda **inválido**: usarlo después es un bug (UB).

Mapa de los 12 casos. Cada celda muestra la respuesta correcta (etiqueta) y, debajo, lo que hizo el analizador estático de Clang. Clic para ir al caso. Ver [Cómo leer este libro](../../guia.md).

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🔴 `UB`<br>❌ no detectado](#f_list_pop_front_it_recto) | [🔴 `UB`<br>❌ no detectado](#f_list_pop_front_it_guarda) | [🔴 `UB`<br>❌ no detectado](#f_list_pop_front_it_bucle) | [🔴 `UB`<br>❌ no detectado](#f_list_pop_front_it_llamada) |
| **referencia** | [🔴 `UB`<br>❌ no detectado](#f_list_pop_front_ref_recto) | [🔴 `UB`<br>❌ no detectado](#f_list_pop_front_ref_guarda) | [🔴 `UB`<br>❌ no detectado](#f_list_pop_front_ref_bucle) | [🔴 `UB`<br>❌ no detectado](#f_list_pop_front_ref_llamada) |
| **puntero** | [🔴 `UB`<br>❌ no detectado](#f_list_pop_front_ptr_recto) | [🔴 `UB`<br>❌ no detectado](#f_list_pop_front_ptr_guarda) | [🔴 `UB`<br>❌ no detectado](#f_list_pop_front_ptr_bucle) | [🔴 `UB`<br>❌ no detectado](#f_list_pop_front_ptr_llamada) |

## Handle: iterador

### f_list_pop_front_it_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_list_pop_front_it_recto(std::list<int>& c) {
  auto it = c.begin();
  c.pop_front();
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
    iterator "this" @ 0x7fff119eaa50 {
      type = std::_List_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::list<int, std::allocator<int> >' @ 0x7fff119eaad0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
d T0 here:
    #0 0x591a4548dd31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x591a455a5ee4 in std::__new_allocator<std::_List_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x591a455a5bb4 in std::allocator_traits<std::allocator<std::_List_node<int>>>::allocate(std::allocator<std::_List_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x591a455a5bb4 in std::__cxx11::_List_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:518:16
    #4 0x591a455c9755 in std::_List_node<int>* std::__cxx11::list<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:710:21
    #5 0x591a455c9570 in void std::__cxx11::list<int, std::allocator<int>>::_M_insert<int const&>(std::_List_iterator<int>, int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:2005:18
    #6 0x591a455c94ad in int& std::__cxx11::list<int, std::allocator<int>>::emplace_back<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1321:10
    #7 0x591a455c9260 in void std::__cxx11::list<int, std::allocator<int>>::_M_initialize_dispatch<int const*>(int const*, int const*, std::__false_type) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1934:6
    #8 0x591a45586121 in std::__cxx11::list<int, std::allocator<int>>::list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:837:9
    #9 0x591a4551bbb0 in make_list[abi:cxx11](Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:52:59
    #10 0x591a4554c90b in main /work/test/runtime_runner.cpp:1762:24
    #11 0x7409fc4fc1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x7409fc4fc28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x591a453a44b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2352:8 in f_list_pop_front_it_recto(std::__cxx11::list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7039fb7dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7039fb7dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7039fb7dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7039fb7dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7039fb7dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7039fb7e0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x7039fb7e0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7039fb7e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7039fb7e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7039fb7e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7039fb7e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==961==ABORTING
````

</details>

### f_list_pop_front_it_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_list_pop_front_it_guarda(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.pop_front();
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
    iterator "this" @ 0x7ffee36b1740 {
      type = std::_List_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::list<int, std::allocator<int> >' @ 0x7ffee36b1800
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
 T0 here:
    #0 0x6315e4759d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x6315e4871ee4 in std::__new_allocator<std::_List_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x6315e4871bb4 in std::allocator_traits<std::allocator<std::_List_node<int>>>::allocate(std::allocator<std::_List_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x6315e4871bb4 in std::__cxx11::_List_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:518:16
    #4 0x6315e4895755 in std::_List_node<int>* std::__cxx11::list<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:710:21
    #5 0x6315e4895570 in void std::__cxx11::list<int, std::allocator<int>>::_M_insert<int const&>(std::_List_iterator<int>, int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:2005:18
    #6 0x6315e48954ad in int& std::__cxx11::list<int, std::allocator<int>>::emplace_back<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1321:10
    #7 0x6315e4895260 in void std::__cxx11::list<int, std::allocator<int>>::_M_initialize_dispatch<int const*>(int const*, int const*, std::__false_type) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1934:6
    #8 0x6315e4852121 in std::__cxx11::list<int, std::allocator<int>>::list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:837:9
    #9 0x6315e47e7bb0 in make_list[abi:cxx11](Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:52:59
    #10 0x6315e4818a41 in main /work/test/runtime_runner.cpp:1767:24
    #11 0x7cf3fafe01c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x7cf3fafe028a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x6315e46704b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2358:8 in f_list_pop_front_it_guarda(std::__cxx11::list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7923fa3dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7923fa3dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7923fa3dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7923fa3dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7923fa3dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7923fa3e0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x7923fa3e0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7923fa3e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7923fa3e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7923fa3e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7923fa3e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==964==ABORTING
````

</details>

### f_list_pop_front_it_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_list_pop_front_it_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.pop_front();
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
    iterator "this" @ 0x7fff8bd31e60 {
      type = std::_List_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::list<int, std::allocator<int> >' @ 0x7fff8bd31f20
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
 T0 here:
    #0 0x60bbdb0c4d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x60bbdb1dcee4 in std::__new_allocator<std::_List_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x60bbdb1dcbb4 in std::allocator_traits<std::allocator<std::_List_node<int>>>::allocate(std::allocator<std::_List_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x60bbdb1dcbb4 in std::__cxx11::_List_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:518:16
    #4 0x60bbdb200755 in std::_List_node<int>* std::__cxx11::list<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:710:21
    #5 0x60bbdb200570 in void std::__cxx11::list<int, std::allocator<int>>::_M_insert<int const&>(std::_List_iterator<int>, int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:2005:18
    #6 0x60bbdb2004ad in int& std::__cxx11::list<int, std::allocator<int>>::emplace_back<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1321:10
    #7 0x60bbdb200260 in void std::__cxx11::list<int, std::allocator<int>>::_M_initialize_dispatch<int const*>(int const*, int const*, std::__false_type) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1934:6
    #8 0x60bbdb1bd121 in std::__cxx11::list<int, std::allocator<int>>::list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:837:9
    #9 0x60bbdb152bb0 in make_list[abi:cxx11](Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:52:59
    #10 0x60bbdb183b77 in main /work/test/runtime_runner.cpp:1772:24
    #11 0x7f67ef2841c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x7f67ef28428a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x60bbdafdb4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2364:10 in f_list_pop_front_it_bucle(std::__cxx11::list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7b97ee5dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b97ee5dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b97ee5dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b97ee5dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b97ee5dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b97ee5e0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x7b97ee5e0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7b97ee5e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b97ee5e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b97ee5e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b97ee5e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==967==ABORTING
````

</details>

### f_list_pop_front_it_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_list_pop_front_it_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_list_pop_front(c);
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
    iterator "this" @ 0x7ffc13895690 {
      type = std::_List_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::list<int, std::allocator<int> >' @ 0x7ffc13895750
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
T0 here:
    #0 0x6351f0543d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x6351f065bee4 in std::__new_allocator<std::_List_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x6351f065bbb4 in std::allocator_traits<std::allocator<std::_List_node<int>>>::allocate(std::allocator<std::_List_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x6351f065bbb4 in std::__cxx11::_List_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:518:16
    #4 0x6351f067f755 in std::_List_node<int>* std::__cxx11::list<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:710:21
    #5 0x6351f067f570 in void std::__cxx11::list<int, std::allocator<int>>::_M_insert<int const&>(std::_List_iterator<int>, int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:2005:18
    #6 0x6351f067f4ad in int& std::__cxx11::list<int, std::allocator<int>>::emplace_back<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1321:10
    #7 0x6351f067f260 in void std::__cxx11::list<int, std::allocator<int>>::_M_initialize_dispatch<int const*>(int const*, int const*, std::__false_type) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1934:6
    #8 0x6351f063c121 in std::__cxx11::list<int, std::allocator<int>>::list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:837:9
    #9 0x6351f05d1bb0 in make_list[abi:cxx11](Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:52:59
    #10 0x6351f0602cad in main /work/test/runtime_runner.cpp:1777:24
    #11 0x7a322f3a81c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x7a322f3a828a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x6351f045a4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2371:8 in f_list_pop_front_it_llamada(std::__cxx11::list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x76622e5dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x76622e5dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x76622e5dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x76622e5dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x76622e5dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x76622e5e0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x76622e5e0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x76622e5e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x76622e5e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x76622e5e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x76622e5e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==970==ABORTING
````

</details>

## Handle: referencia

### f_list_pop_front_ref_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_list_pop_front_ref_recto(std::list<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.pop_front();
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
 T0 here:
    #0 0x5c3470932d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5c3470a4aee4 in std::__new_allocator<std::_List_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5c3470a4abb4 in std::allocator_traits<std::allocator<std::_List_node<int>>>::allocate(std::allocator<std::_List_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5c3470a4abb4 in std::__cxx11::_List_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:518:16
    #4 0x5c3470a6e755 in std::_List_node<int>* std::__cxx11::list<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:710:21
    #5 0x5c3470a6e570 in void std::__cxx11::list<int, std::allocator<int>>::_M_insert<int const&>(std::_List_iterator<int>, int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:2005:18
    #6 0x5c3470a6e4ad in int& std::__cxx11::list<int, std::allocator<int>>::emplace_back<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1321:10
    #7 0x5c3470a6e260 in void std::__cxx11::list<int, std::allocator<int>>::_M_initialize_dispatch<int const*>(int const*, int const*, std::__false_type) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1934:6
    #8 0x5c3470a2b121 in std::__cxx11::list<int, std::allocator<int>>::list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:837:9
    #9 0x5c34709c0bb0 in make_list[abi:cxx11](Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:52:59
    #10 0x5c34709f1de3 in main /work/test/runtime_runner.cpp:1782:24
    #11 0x7332457711c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x73324577128a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x5c34708494b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2377:8 in f_list_pop_front_ref_recto(std::__cxx11::list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6f62449dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f62449dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f62449dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f62449dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f62449dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6f62449e0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x6f62449e0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x6f62449e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f62449e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f62449e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f62449e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==973==ABORTING
````

</details>

### f_list_pop_front_ref_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_list_pop_front_ref_guarda(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.pop_front();
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
T0 here:
    #0 0x59a6bcd08d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x59a6bce20ee4 in std::__new_allocator<std::_List_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x59a6bce20bb4 in std::allocator_traits<std::allocator<std::_List_node<int>>>::allocate(std::allocator<std::_List_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x59a6bce20bb4 in std::__cxx11::_List_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:518:16
    #4 0x59a6bce44755 in std::_List_node<int>* std::__cxx11::list<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:710:21
    #5 0x59a6bce44570 in void std::__cxx11::list<int, std::allocator<int>>::_M_insert<int const&>(std::_List_iterator<int>, int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:2005:18
    #6 0x59a6bce444ad in int& std::__cxx11::list<int, std::allocator<int>>::emplace_back<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1321:10
    #7 0x59a6bce44260 in void std::__cxx11::list<int, std::allocator<int>>::_M_initialize_dispatch<int const*>(int const*, int const*, std::__false_type) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1934:6
    #8 0x59a6bce01121 in std::__cxx11::list<int, std::allocator<int>>::list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:837:9
    #9 0x59a6bcd96bb0 in make_list[abi:cxx11](Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:52:59
    #10 0x59a6bcdc7f19 in main /work/test/runtime_runner.cpp:1787:24
    #11 0x76fc421251c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x76fc4212528a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x59a6bcc1f4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2384:8 in f_list_pop_front_ref_guarda(std::__cxx11::list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x732c413dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x732c413dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x732c413dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x732c413dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x732c413dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x732c413e0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x732c413e0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x732c413e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x732c413e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x732c413e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x732c413e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==976==ABORTING
````

</details>

### f_list_pop_front_ref_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `bucle` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_list_pop_front_ref_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.pop_front();
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
    iterator "this" @ 0x7fff425f1b20 {
      type = std::_List_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::list<int, std::allocator<int> >' @ 0x7fff425f1be0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
T0 here:
    #0 0x5e6dc6998d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5e6dc6ab0ee4 in std::__new_allocator<std::_List_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5e6dc6ab0bb4 in std::allocator_traits<std::allocator<std::_List_node<int>>>::allocate(std::allocator<std::_List_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5e6dc6ab0bb4 in std::__cxx11::_List_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:518:16
    #4 0x5e6dc6ad4755 in std::_List_node<int>* std::__cxx11::list<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:710:21
    #5 0x5e6dc6ad4570 in void std::__cxx11::list<int, std::allocator<int>>::_M_insert<int const&>(std::_List_iterator<int>, int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:2005:18
    #6 0x5e6dc6ad44ad in int& std::__cxx11::list<int, std::allocator<int>>::emplace_back<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1321:10
    #7 0x5e6dc6ad4260 in void std::__cxx11::list<int, std::allocator<int>>::_M_initialize_dispatch<int const*>(int const*, int const*, std::__false_type) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1934:6
    #8 0x5e6dc6a91121 in std::__cxx11::list<int, std::allocator<int>>::list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:837:9
    #9 0x5e6dc6a26bb0 in make_list[abi:cxx11](Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:52:59
    #10 0x5e6dc6a5804f in main /work/test/runtime_runner.cpp:1792:24
    #11 0x7d92094801c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x7d920948028a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x5e6dc68af4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2391:10 in f_list_pop_front_ref_bucle(std::__cxx11::list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x79c2087dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x79c2087dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x79c2087dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x79c2087dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x79c2087dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x79c2087e0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x79c2087e0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x79c2087e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x79c2087e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x79c2087e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x79c2087e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==979==ABORTING
````

</details>

### f_list_pop_front_ref_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_list_pop_front_ref_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_list_pop_front(c);
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
    #0 0x58f24444dd31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x58f244565ee4 in std::__new_allocator<std::_List_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x58f244565bb4 in std::allocator_traits<std::allocator<std::_List_node<int>>>::allocate(std::allocator<std::_List_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x58f244565bb4 in std::__cxx11::_List_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:518:16
    #4 0x58f244589755 in std::_List_node<int>* std::__cxx11::list<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:710:21
    #5 0x58f244589570 in void std::__cxx11::list<int, std::allocator<int>>::_M_insert<int const&>(std::_List_iterator<int>, int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:2005:18
    #6 0x58f2445894ad in int& std::__cxx11::list<int, std::allocator<int>>::emplace_back<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1321:10
    #7 0x58f244589260 in void std::__cxx11::list<int, std::allocator<int>>::_M_initialize_dispatch<int const*>(int const*, int const*, std::__false_type) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1934:6
    #8 0x58f244546121 in std::__cxx11::list<int, std::allocator<int>>::list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:837:9
    #9 0x58f2444dbbb0 in make_list[abi:cxx11](Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:52:59
    #10 0x58f24450d185 in main /work/test/runtime_runner.cpp:1797:24
    #11 0x7e060de891c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x7e060de8928a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x58f2443644b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2399:8 in f_list_pop_front_ref_llamada(std::__cxx11::list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7a360d1dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a360d1dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a360d1dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a360d1dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a360d1dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7a360d1e0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x7a360d1e0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7a360d1e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a360d1e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a360d1e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a360d1e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==982==ABORTING
````

</details>

## Handle: puntero

### f_list_pop_front_ptr_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_list_pop_front_ptr_recto(std::list<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.pop_front();
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
 T0 here:
    #0 0x5ed56b8cad31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5ed56b9e2ee4 in std::__new_allocator<std::_List_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5ed56b9e2bb4 in std::allocator_traits<std::allocator<std::_List_node<int>>>::allocate(std::allocator<std::_List_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5ed56b9e2bb4 in std::__cxx11::_List_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:518:16
    #4 0x5ed56ba06755 in std::_List_node<int>* std::__cxx11::list<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:710:21
    #5 0x5ed56ba06570 in void std::__cxx11::list<int, std::allocator<int>>::_M_insert<int const&>(std::_List_iterator<int>, int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:2005:18
    #6 0x5ed56ba064ad in int& std::__cxx11::list<int, std::allocator<int>>::emplace_back<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1321:10
    #7 0x5ed56ba06260 in void std::__cxx11::list<int, std::allocator<int>>::_M_initialize_dispatch<int const*>(int const*, int const*, std::__false_type) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1934:6
    #8 0x5ed56b9c3121 in std::__cxx11::list<int, std::allocator<int>>::list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:837:9
    #9 0x5ed56b958bb0 in make_list[abi:cxx11](Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:52:59
    #10 0x5ed56b98a2bb in main /work/test/runtime_runner.cpp:1802:24
    #11 0x72036ab151c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x72036ab1528a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x5ed56b7e14b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2405:8 in f_list_pop_front_ptr_recto(std::__cxx11::list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6e3369ddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e3369ddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e3369ddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e3369ddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e3369ddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6e3369de0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x6e3369de0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x6e3369de0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e3369de0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e3369de0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e3369de0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==985==ABORTING
````

</details>

### f_list_pop_front_ptr_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_list_pop_front_ptr_guarda(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.pop_front();
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
T0 here:
    #0 0x60ca978c1d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x60ca979d9ee4 in std::__new_allocator<std::_List_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x60ca979d9bb4 in std::allocator_traits<std::allocator<std::_List_node<int>>>::allocate(std::allocator<std::_List_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x60ca979d9bb4 in std::__cxx11::_List_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:518:16
    #4 0x60ca979fd755 in std::_List_node<int>* std::__cxx11::list<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:710:21
    #5 0x60ca979fd570 in void std::__cxx11::list<int, std::allocator<int>>::_M_insert<int const&>(std::_List_iterator<int>, int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:2005:18
    #6 0x60ca979fd4ad in int& std::__cxx11::list<int, std::allocator<int>>::emplace_back<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1321:10
    #7 0x60ca979fd260 in void std::__cxx11::list<int, std::allocator<int>>::_M_initialize_dispatch<int const*>(int const*, int const*, std::__false_type) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1934:6
    #8 0x60ca979ba121 in std::__cxx11::list<int, std::allocator<int>>::list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:837:9
    #9 0x60ca9794fbb0 in make_list[abi:cxx11](Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:52:59
    #10 0x60ca979813f1 in main /work/test/runtime_runner.cpp:1807:24
    #11 0x78b2eea401c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x78b2eea4028a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x60ca977d84b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2412:8 in f_list_pop_front_ptr_guarda(std::__cxx11::list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x74e2edddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x74e2edddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x74e2edddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x74e2edddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x74e2edddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x74e2edde0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x74e2edde0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x74e2edde0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x74e2edde0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x74e2edde0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x74e2edde0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==988==ABORTING
````

</details>

### f_list_pop_front_ptr_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `bucle` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_list_pop_front_ptr_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.pop_front();
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
    iterator "this" @ 0x7fff328318d0 {
      type = std::_List_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::list<int, std::allocator<int> >' @ 0x7fff32831990
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
T0 here:
    #0 0x5ca568ce3d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5ca568dfbee4 in std::__new_allocator<std::_List_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5ca568dfbbb4 in std::allocator_traits<std::allocator<std::_List_node<int>>>::allocate(std::allocator<std::_List_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5ca568dfbbb4 in std::__cxx11::_List_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:518:16
    #4 0x5ca568e1f755 in std::_List_node<int>* std::__cxx11::list<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:710:21
    #5 0x5ca568e1f570 in void std::__cxx11::list<int, std::allocator<int>>::_M_insert<int const&>(std::_List_iterator<int>, int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:2005:18
    #6 0x5ca568e1f4ad in int& std::__cxx11::list<int, std::allocator<int>>::emplace_back<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1321:10
    #7 0x5ca568e1f260 in void std::__cxx11::list<int, std::allocator<int>>::_M_initialize_dispatch<int const*>(int const*, int const*, std::__false_type) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1934:6
    #8 0x5ca568ddc121 in std::__cxx11::list<int, std::allocator<int>>::list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:837:9
    #9 0x5ca568d71bb0 in make_list[abi:cxx11](Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:52:59
    #10 0x5ca568da3527 in main /work/test/runtime_runner.cpp:1812:24
    #11 0x7ee22ac921c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x7ee22ac9228a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x5ca568bfa4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2419:10 in f_list_pop_front_ptr_bucle(std::__cxx11::list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7b1229fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b1229fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b1229fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b1229fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b1229fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b1229fe0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x7b1229fe0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7b1229fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b1229fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b1229fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b1229fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==991==ABORTING
````

</details>

### f_list_pop_front_ptr_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_list_pop_front_ptr_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_list_pop_front(c);
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
    #0 0x60bd240f6d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x60bd2420eee4 in std::__new_allocator<std::_List_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x60bd2420ebb4 in std::allocator_traits<std::allocator<std::_List_node<int>>>::allocate(std::allocator<std::_List_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x60bd2420ebb4 in std::__cxx11::_List_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:518:16
    #4 0x60bd24232755 in std::_List_node<int>* std::__cxx11::list<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:710:21
    #5 0x60bd24232570 in void std::__cxx11::list<int, std::allocator<int>>::_M_insert<int const&>(std::_List_iterator<int>, int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:2005:18
    #6 0x60bd242324ad in int& std::__cxx11::list<int, std::allocator<int>>::emplace_back<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1321:10
    #7 0x60bd24232260 in void std::__cxx11::list<int, std::allocator<int>>::_M_initialize_dispatch<int const*>(int const*, int const*, std::__false_type) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:1934:6
    #8 0x60bd241ef121 in std::__cxx11::list<int, std::allocator<int>>::list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_list.h:837:9
    #9 0x60bd24184bb0 in make_list[abi:cxx11](Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:52:59
    #10 0x60bd241b665d in main /work/test/runtime_runner.cpp:1817:24
    #11 0x722651b721c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x722651b7228a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x60bd2400d4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2427:8 in f_list_pop_front_ptr_llamada(std::__cxx11::list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6e5650ddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e5650ddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e5650ddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e5650ddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e5650ddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6e5650de0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x6e5650de0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x6e5650de0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e5650de0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e5650de0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e5650de0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==994==ABORTING
````

</details>
