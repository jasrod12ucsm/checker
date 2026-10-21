# `std::forward_list::clear`

Mutación: `c.clear();`

- Iterador retenido: 🔴 `UB`
- Referencia/puntero retenido: 🔴 `UB`
- Casos `UB` detectados estáticamente: 5/12

**En palabras:** después de `c.clear();` sobre un `std::forward_list`, un iterador guardado queda **inválido**: usarlo después es un bug (UB); una referencia o puntero guardado queda **inválido**: usarlo después es un bug (UB).

Mapa de los 12 casos. Cada celda muestra la respuesta correcta (etiqueta) y, debajo, lo que hizo el analizador estático de Clang. Clic para ir al caso. Ver [Cómo leer este libro](../../guia.md).

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🔴 `UB`<br>❌ no detectado](#f_flist_clear_it_recto) | [🔴 `UB`<br>✅ detectado](#f_flist_clear_it_guarda) | [🔴 `UB`<br>✅ detectado](#f_flist_clear_it_bucle) | [🔴 `UB`<br>✅ detectado](#f_flist_clear_it_llamada) |
| **referencia** | [🔴 `UB`<br>❌ no detectado](#f_flist_clear_ref_recto) | [🔴 `UB`<br>❌ no detectado](#f_flist_clear_ref_guarda) | [🔴 `UB`<br>✅ detectado](#f_flist_clear_ref_bucle) | [🔴 `UB`<br>❌ no detectado](#f_flist_clear_ref_llamada) |
| **puntero** | [🔴 `UB`<br>❌ no detectado](#f_flist_clear_ptr_recto) | [🔴 `UB`<br>❌ no detectado](#f_flist_clear_ptr_guarda) | [🔴 `UB`<br>✅ detectado](#f_flist_clear_ptr_bucle) | [🔴 `UB`<br>❌ no detectado](#f_flist_clear_ptr_llamada) |

## Handle: iterador

### f_flist_clear_it_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_flist_clear_it_recto(std::forward_list<int>& c) {
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
    const [with _Iterator = std::_Fwd_list_iterator<int>; _Sequence = std::
    debug::forward_list<int>; _Category = std::forward_iterator_tag; 
    reference = int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fff3020e0c0 {
      type = std::_Fwd_list_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::forward_list<int, std::allocator<int> >' @ 0x7fff3020e140
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
123:5
    #8 0x75ff835b91c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x75ff835b928a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x5cca054304b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5cca05519d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5cca05635a67 in std::__new_allocator<std::_Fwd_list_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5cca056357df in std::allocator_traits<std::allocator<std::_Fwd_list_node<int>>>::allocate(std::allocator<std::_Fwd_list_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5cca056357df in std::_Fwd_list_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:360:15
    #4 0x5cca05655feb in std::_Fwd_list_node<int>* std::_Fwd_list_base<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:368:26
    #5 0x5cca05655be2 in void std::forward_list<int, std::allocator<int>>::_M_range_initialize<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.tcc:105:28
    #6 0x5cca056124f1 in std::forward_list<int, std::allocator<int>>::forward_list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:597:9
    #7 0x5cca055a7f60 in make_flist(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:53:68
    #8 0x5cca055de866 in main /work/test/runtime_runner.cpp:2122:32
    #9 0x75ff835b91c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x75ff835b928a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x5cca054304b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2832:8 in f_flist_clear_it_recto(std::forward_list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x721f827dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x721f827dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x721f827dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x721f827dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x721f827dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x721f827e0000: fa fa fd[fd]fa fa fd fd fa fa fd fd fa fa fa fa
  0x721f827e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x721f827e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x721f827e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x721f827e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x721f827e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1129==ABORTING
````

</details>

### f_flist_clear_it_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `guarda` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_flist_clear_it_guarda(std::forward_list<int>& c) {
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
    const [with _Iterator = std::_Fwd_list_iterator<int>; _Sequence = std::
    debug::forward_list<int>; _Category = std::forward_iterator_tag; 
    reference = int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffd4e31c9b0 {
      type = std::_Fwd_list_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::forward_list<int, std::allocator<int> >' @ 0x7ffd4e31ca70
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
28:5
    #8 0x7f7829c741c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x7f7829c7428a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x5d72966fe4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5d72967e7d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5d7296903a67 in std::__new_allocator<std::_Fwd_list_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5d72969037df in std::allocator_traits<std::allocator<std::_Fwd_list_node<int>>>::allocate(std::allocator<std::_Fwd_list_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5d72969037df in std::_Fwd_list_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:360:15
    #4 0x5d7296923feb in std::_Fwd_list_node<int>* std::_Fwd_list_base<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:368:26
    #5 0x5d7296923be2 in void std::forward_list<int, std::allocator<int>>::_M_range_initialize<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.tcc:105:28
    #6 0x5d72968e04f1 in std::forward_list<int, std::allocator<int>>::forward_list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:597:9
    #7 0x5d7296875f60 in make_flist(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:53:68
    #8 0x5d72968ac98a in main /work/test/runtime_runner.cpp:2127:32
    #9 0x7f7829c741c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x7f7829c7428a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x5d72966fe4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2838:8 in f_flist_clear_it_guarda(std::forward_list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7b9828fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9828fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9828fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9828fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9828fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b9828fe0000: fa fa fd[fd]fa fa fd fd fa fa fd fd fa fa fa fa
  0x7b9828fe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b9828fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b9828fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b9828fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b9828fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1132==ABORTING
````

</details>

### f_flist_clear_it_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_flist_clear_it_bucle(std::forward_list<int>& c) {
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
    const [with _Iterator = std::_Fwd_list_iterator<int>; _Sequence = std::
    debug::forward_list<int>; _Category = std::forward_iterator_tag; 
    reference = int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffebf7f8520 {
      type = std::_Fwd_list_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::forward_list<int, std::allocator<int> >' @ 0x7ffebf7f85e0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
33:5
    #8 0x7975c01f11c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x7975c01f128a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x648f404e44b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x648f405cdd31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x648f406e9a67 in std::__new_allocator<std::_Fwd_list_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x648f406e97df in std::allocator_traits<std::allocator<std::_Fwd_list_node<int>>>::allocate(std::allocator<std::_Fwd_list_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x648f406e97df in std::_Fwd_list_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:360:15
    #4 0x648f40709feb in std::_Fwd_list_node<int>* std::_Fwd_list_base<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:368:26
    #5 0x648f40709be2 in void std::forward_list<int, std::allocator<int>>::_M_range_initialize<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.tcc:105:28
    #6 0x648f406c64f1 in std::forward_list<int, std::allocator<int>>::forward_list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:597:9
    #7 0x648f4065bf60 in make_flist(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:53:68
    #8 0x648f40692aae in main /work/test/runtime_runner.cpp:2132:32
    #9 0x7975c01f11c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x7975c01f128a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x648f404e44b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2844:10 in f_flist_clear_it_bucle(std::forward_list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7595bf5dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7595bf5dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7595bf5dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7595bf5dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7595bf5dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7595bf5e0000: fa fa fd[fd]fa fa fd fd fa fa fd fd fa fa fa fa
  0x7595bf5e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7595bf5e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7595bf5e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7595bf5e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7595bf5e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1135==ABORTING
````

</details>

### f_flist_clear_it_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `llamada` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_flist_clear_it_llamada(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_flist_clear(c);
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
    const [with _Iterator = std::_Fwd_list_iterator<int>; _Sequence = std::
    debug::forward_list<int>; _Category = std::forward_iterator_tag; 
    reference = int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffc4c3d4290 {
      type = std::_Fwd_list_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::forward_list<int, std::allocator<int> >' @ 0x7ffc4c3d4350
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
:5
    #9 0x7c4f5cdc71c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x7c4f5cdc728a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x62482d4744b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x62482d55dd31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x62482d679a67 in std::__new_allocator<std::_Fwd_list_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x62482d6797df in std::allocator_traits<std::allocator<std::_Fwd_list_node<int>>>::allocate(std::allocator<std::_Fwd_list_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x62482d6797df in std::_Fwd_list_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:360:15
    #4 0x62482d699feb in std::_Fwd_list_node<int>* std::_Fwd_list_base<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:368:26
    #5 0x62482d699be2 in void std::forward_list<int, std::allocator<int>>::_M_range_initialize<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.tcc:105:28
    #6 0x62482d6564f1 in std::forward_list<int, std::allocator<int>>::forward_list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:597:9
    #7 0x62482d5ebf60 in make_flist(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:53:68
    #8 0x62482d622bd2 in main /work/test/runtime_runner.cpp:2137:32
    #9 0x7c4f5cdc71c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x7c4f5cdc728a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x62482d4744b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2851:8 in f_flist_clear_it_llamada(std::forward_list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x786f5bfdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x786f5bfdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x786f5bfdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x786f5bfdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x786f5bfdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x786f5bfe0000: fa fa fd[fd]fa fa fd fd fa fa fd fd fa fa fa fa
  0x786f5bfe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x786f5bfe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x786f5bfe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x786f5bfe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x786f5bfe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1138==ABORTING
````

</details>

## Handle: referencia

### f_flist_clear_ref_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_flist_clear_ref_recto(std::forward_list<int>& c) {
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
43:5
    #8 0x7708b07d51c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x7708b07d528a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x5a464fdc44b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5a464feadd31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5a464ffc9a67 in std::__new_allocator<std::_Fwd_list_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5a464ffc97df in std::allocator_traits<std::allocator<std::_Fwd_list_node<int>>>::allocate(std::allocator<std::_Fwd_list_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5a464ffc97df in std::_Fwd_list_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:360:15
    #4 0x5a464ffe9feb in std::_Fwd_list_node<int>* std::_Fwd_list_base<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:368:26
    #5 0x5a464ffe9be2 in void std::forward_list<int, std::allocator<int>>::_M_range_initialize<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.tcc:105:28
    #6 0x5a464ffa64f1 in std::forward_list<int, std::allocator<int>>::forward_list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:597:9
    #7 0x5a464ff3bf60 in make_flist(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:53:68
    #8 0x5a464ff72cf6 in main /work/test/runtime_runner.cpp:2142:32
    #9 0x7708b07d51c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x7708b07d528a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x5a464fdc44b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2857:8 in f_flist_clear_ref_recto(std::forward_list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7328afbdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7328afbdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7328afbdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7328afbdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7328afbdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7328afbe0000: fa fa fd[fd]fa fa fd fd fa fa fd fd fa fa fa fa
  0x7328afbe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7328afbe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7328afbe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7328afbe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7328afbe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1141==ABORTING
````

</details>

### f_flist_clear_ref_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_flist_clear_ref_guarda(std::forward_list<int>& c) {
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
8:5
    #8 0x7ef3264e41c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x7ef3264e428a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x57f97a6804b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x57f97a769d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x57f97a885a67 in std::__new_allocator<std::_Fwd_list_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x57f97a8857df in std::allocator_traits<std::allocator<std::_Fwd_list_node<int>>>::allocate(std::allocator<std::_Fwd_list_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x57f97a8857df in std::_Fwd_list_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:360:15
    #4 0x57f97a8a5feb in std::_Fwd_list_node<int>* std::_Fwd_list_base<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:368:26
    #5 0x57f97a8a5be2 in void std::forward_list<int, std::allocator<int>>::_M_range_initialize<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.tcc:105:28
    #6 0x57f97a8624f1 in std::forward_list<int, std::allocator<int>>::forward_list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:597:9
    #7 0x57f97a7f7f60 in make_flist(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:53:68
    #8 0x57f97a82ee1a in main /work/test/runtime_runner.cpp:2147:32
    #9 0x7ef3264e41c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x7ef3264e428a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x57f97a6804b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2864:8 in f_flist_clear_ref_guarda(std::forward_list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7b13257dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b13257dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b13257dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b13257dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b13257dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b13257e0000: fa fa fd[fd]fa fa fd fd fa fa fd fd fa fa fa fa
  0x7b13257e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b13257e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b13257e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b13257e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b13257e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1144==ABORTING
````

</details>

### f_flist_clear_ref_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `bucle` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_flist_clear_ref_bucle(std::forward_list<int>& c) {
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
    [with _Iterator = std::_Fwd_list_iterator<int>; _Sequence = std::
    debug::forward_list<int>; _Category = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fffe791a630 {
      type = std::_Fwd_list_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::forward_list<int, std::allocator<int> >' @ 0x7fffe791a6f0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
3:5
    #8 0x7bbeabd4a1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x7bbeabd4a28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x5bc63c1b54b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5bc63c29ed31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5bc63c3baa67 in std::__new_allocator<std::_Fwd_list_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5bc63c3ba7df in std::allocator_traits<std::allocator<std::_Fwd_list_node<int>>>::allocate(std::allocator<std::_Fwd_list_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5bc63c3ba7df in std::_Fwd_list_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:360:15
    #4 0x5bc63c3dafeb in std::_Fwd_list_node<int>* std::_Fwd_list_base<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:368:26
    #5 0x5bc63c3dabe2 in void std::forward_list<int, std::allocator<int>>::_M_range_initialize<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.tcc:105:28
    #6 0x5bc63c3974f1 in std::forward_list<int, std::allocator<int>>::forward_list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:597:9
    #7 0x5bc63c32cf60 in make_flist(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:53:68
    #8 0x5bc63c363f3e in main /work/test/runtime_runner.cpp:2152:32
    #9 0x7bbeabd4a1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x7bbeabd4a28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x5bc63c1b54b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2871:10 in f_flist_clear_ref_bucle(std::forward_list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x77deaafdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x77deaafdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x77deaafdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x77deaafdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x77deaafdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x77deaafe0000: fa fa fd[fd]fa fa fd fd fa fa fd fd fa fa fa fa
  0x77deaafe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x77deaafe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x77deaafe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x77deaafe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x77deaafe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1147==ABORTING
````

</details>

### f_flist_clear_ref_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_flist_clear_ref_llamada(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_flist_clear(c);
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
5
    #9 0x7532a80281c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x7532a802828a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x5c1f1e2084b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5c1f1e2f1d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5c1f1e40da67 in std::__new_allocator<std::_Fwd_list_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5c1f1e40d7df in std::allocator_traits<std::allocator<std::_Fwd_list_node<int>>>::allocate(std::allocator<std::_Fwd_list_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5c1f1e40d7df in std::_Fwd_list_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:360:15
    #4 0x5c1f1e42dfeb in std::_Fwd_list_node<int>* std::_Fwd_list_base<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:368:26
    #5 0x5c1f1e42dbe2 in void std::forward_list<int, std::allocator<int>>::_M_range_initialize<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.tcc:105:28
    #6 0x5c1f1e3ea4f1 in std::forward_list<int, std::allocator<int>>::forward_list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:597:9
    #7 0x5c1f1e37ff60 in make_flist(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:53:68
    #8 0x5c1f1e3b7062 in main /work/test/runtime_runner.cpp:2157:32
    #9 0x7532a80281c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x7532a802828a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x5c1f1e2084b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2879:8 in f_flist_clear_ref_llamada(std::forward_list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7152a73dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7152a73dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7152a73dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7152a73dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7152a73dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7152a73e0000: fa fa fd[fd]fa fa fd fd fa fa fd fd fa fa fa fa
  0x7152a73e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7152a73e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7152a73e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7152a73e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7152a73e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1150==ABORTING
````

</details>

## Handle: puntero

### f_flist_clear_ptr_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_flist_clear_ptr_recto(std::forward_list<int>& c) {
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
63:5
    #8 0x7b2017c091c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x7b2017c0928a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x5f006f9cb4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5f006fab4d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5f006fbd0a67 in std::__new_allocator<std::_Fwd_list_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5f006fbd07df in std::allocator_traits<std::allocator<std::_Fwd_list_node<int>>>::allocate(std::allocator<std::_Fwd_list_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5f006fbd07df in std::_Fwd_list_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:360:15
    #4 0x5f006fbf0feb in std::_Fwd_list_node<int>* std::_Fwd_list_base<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:368:26
    #5 0x5f006fbf0be2 in void std::forward_list<int, std::allocator<int>>::_M_range_initialize<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.tcc:105:28
    #6 0x5f006fbad4f1 in std::forward_list<int, std::allocator<int>>::forward_list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:597:9
    #7 0x5f006fb42f60 in make_flist(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:53:68
    #8 0x5f006fb7a186 in main /work/test/runtime_runner.cpp:2162:32
    #9 0x7b2017c091c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x7b2017c0928a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x5f006f9cb4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2885:8 in f_flist_clear_ptr_recto(std::forward_list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x774016fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x774016fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x774016fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x774016fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x774016fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x774016fe0000: fa fa fd[fd]fa fa fd fd fa fa fd fd fa fa fa fa
  0x774016fe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x774016fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x774016fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x774016fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x774016fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1153==ABORTING
````

</details>

### f_flist_clear_ptr_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_flist_clear_ptr_guarda(std::forward_list<int>& c) {
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
8:5
    #8 0x78fc86b291c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x78fc86b2928a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x5fd9a739d4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5fd9a7486d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5fd9a75a2a67 in std::__new_allocator<std::_Fwd_list_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5fd9a75a27df in std::allocator_traits<std::allocator<std::_Fwd_list_node<int>>>::allocate(std::allocator<std::_Fwd_list_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5fd9a75a27df in std::_Fwd_list_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:360:15
    #4 0x5fd9a75c2feb in std::_Fwd_list_node<int>* std::_Fwd_list_base<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:368:26
    #5 0x5fd9a75c2be2 in void std::forward_list<int, std::allocator<int>>::_M_range_initialize<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.tcc:105:28
    #6 0x5fd9a757f4f1 in std::forward_list<int, std::allocator<int>>::forward_list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:597:9
    #7 0x5fd9a7514f60 in make_flist(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:53:68
    #8 0x5fd9a754c2aa in main /work/test/runtime_runner.cpp:2167:32
    #9 0x78fc86b291c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x78fc86b2928a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x5fd9a739d4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2892:8 in f_flist_clear_ptr_guarda(std::forward_list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x751c85ddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x751c85ddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x751c85ddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x751c85ddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x751c85ddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x751c85de0000: fa fa fd[fd]fa fa fd fd fa fa fd fd fa fa fa fa
  0x751c85de0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x751c85de0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x751c85de0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x751c85de0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x751c85de0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1156==ABORTING
````

</details>

### f_flist_clear_ptr_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `bucle` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_flist_clear_ptr_bucle(std::forward_list<int>& c) {
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
    [with _Iterator = std::_Fwd_list_iterator<int>; _Sequence = std::
    debug::forward_list<int>; _Category = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffce93f3410 {
      type = std::_Fwd_list_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::forward_list<int, std::allocator<int> >' @ 0x7ffce93f34d0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
3:5
    #8 0x7102793651c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x71027936528a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x63be1f64c4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x63be1f735d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x63be1f851a67 in std::__new_allocator<std::_Fwd_list_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x63be1f8517df in std::allocator_traits<std::allocator<std::_Fwd_list_node<int>>>::allocate(std::allocator<std::_Fwd_list_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x63be1f8517df in std::_Fwd_list_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:360:15
    #4 0x63be1f871feb in std::_Fwd_list_node<int>* std::_Fwd_list_base<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:368:26
    #5 0x63be1f871be2 in void std::forward_list<int, std::allocator<int>>::_M_range_initialize<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.tcc:105:28
    #6 0x63be1f82e4f1 in std::forward_list<int, std::allocator<int>>::forward_list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:597:9
    #7 0x63be1f7c3f60 in make_flist(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:53:68
    #8 0x63be1f7fb3ce in main /work/test/runtime_runner.cpp:2172:32
    #9 0x7102793651c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x71027936528a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x63be1f64c4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2899:10 in f_flist_clear_ptr_bucle(std::forward_list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6d22785dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d22785dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d22785dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d22785dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d22785dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6d22785e0000: fa fa fd[fd]fa fa fd fd fa fa fd fd fa fa fa fa
  0x6d22785e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d22785e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d22785e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d22785e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d22785e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1159==ABORTING
````

</details>

### f_flist_clear_ptr_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_flist_clear_ptr_llamada(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_flist_clear(c);
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
5
    #9 0x77792ce5d1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x77792ce5d28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x60f4686454b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x60f46872ed31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x60f46884aa67 in std::__new_allocator<std::_Fwd_list_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x60f46884a7df in std::allocator_traits<std::allocator<std::_Fwd_list_node<int>>>::allocate(std::allocator<std::_Fwd_list_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x60f46884a7df in std::_Fwd_list_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:360:15
    #4 0x60f46886afeb in std::_Fwd_list_node<int>* std::_Fwd_list_base<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:368:26
    #5 0x60f46886abe2 in void std::forward_list<int, std::allocator<int>>::_M_range_initialize<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.tcc:105:28
    #6 0x60f4688274f1 in std::forward_list<int, std::allocator<int>>::forward_list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:597:9
    #7 0x60f4687bcf60 in make_flist(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:53:68
    #8 0x60f4687f44f2 in main /work/test/runtime_runner.cpp:2177:32
    #9 0x77792ce5d1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x77792ce5d28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x60f4686454b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2907:8 in f_flist_clear_ptr_llamada(std::forward_list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x73992c1dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73992c1dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73992c1dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73992c1dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73992c1dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x73992c1e0000: fa fa fd[fd]fa fa fd fd fa fa fd fd fa fa fa fa
  0x73992c1e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x73992c1e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x73992c1e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x73992c1e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x73992c1e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1162==ABORTING
````

</details>
