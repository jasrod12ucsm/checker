# `std::set::clear`

Mutación: `c.clear();`

- Iterador retenido: 🔴 `UB`
- Referencia/puntero retenido: 🔴 `UB`
- Casos `UB` detectados estáticamente: 5/12

**En palabras:** después de `c.clear();` sobre un `std::set`, un iterador guardado queda **inválido**: usarlo después es un bug (UB); una referencia o puntero guardado queda **inválido**: usarlo después es un bug (UB).

Mapa de los 12 casos. Cada celda muestra la respuesta correcta (etiqueta) y, debajo, lo que hizo el analizador estático de Clang. Clic para ir al caso. Ver [Cómo leer este libro](../../guia.md).

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🔴 `UB`<br>❌ no detectado](#f_set_clear_it_recto) | [🔴 `UB`<br>✅ detectado](#f_set_clear_it_guarda) | [🔴 `UB`<br>✅ detectado](#f_set_clear_it_bucle) | [🔴 `UB`<br>✅ detectado](#f_set_clear_it_llamada) |
| **referencia** | [🔴 `UB`<br>❌ no detectado](#f_set_clear_ref_recto) | [🔴 `UB`<br>❌ no detectado](#f_set_clear_ref_guarda) | [🔴 `UB`<br>✅ detectado](#f_set_clear_ref_bucle) | [🔴 `UB`<br>❌ no detectado](#f_set_clear_ref_llamada) |
| **puntero** | [🔴 `UB`<br>❌ no detectado](#f_set_clear_ptr_recto) | [🔴 `UB`<br>❌ no detectado](#f_set_clear_ptr_guarda) | [🔴 `UB`<br>✅ detectado](#f_set_clear_ptr_bucle) | [🔴 `UB`<br>❌ no detectado](#f_set_clear_ptr_llamada) |

## Handle: iterador

### f_set_clear_it_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_set_clear_it_recto(std::set<int>& c) {
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
    const [with _Iterator = std::_Rb_tree_const_iterator<int>; _Sequence = 
    std::debug::set<int>; _Category = std::forward_iterator_tag; reference = 
    const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffeb12dc300 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::set<int, std::less<int>, std::allocator<int> >' @ 0x7ffeb12dc380
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
./include/c++/13/bits/stl_tree.h:613:23
    #5 0x616d5d452ad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x616d5d4523e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x616d5d450eb9 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_unique_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x616d5d4507c9 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_unique<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x616d5d40c923 in std::set<int, std::less<int>, std::allocator<int>>::set(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_set.h:249:14
    #10 0x616d5d3a2323 in make_set(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:55:57
    #11 0x616d5d3dcbfe in main /work/test/runtime_runner.cpp:2362:23
    #12 0x7b477d24d1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x7b477d24d28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x616d5d22a4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3152:8 in f_set_clear_it_recto(std::set<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x77877c5dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x77877c5dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x77877c5dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x77877c5dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x77877c5dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x77877c5e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x77877c5e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x77877c5e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x77877c5e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x77877c5e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x77877c5e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1249==ABORTING
````

</details>

### f_set_clear_it_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `guarda` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_set_clear_it_guarda(std::set<int>& c) {
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
    const [with _Iterator = std::_Rb_tree_const_iterator<int>; _Sequence = 
    std::debug::set<int>; _Category = std::forward_iterator_tag; reference = 
    const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fff902eaf40 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::set<int, std::less<int>, std::allocator<int> >' @ 0x7fff902eb000
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
/include/c++/13/bits/stl_tree.h:613:23
    #5 0x57eacf0f7ad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x57eacf0f73e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x57eacf0f5eb9 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_unique_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x57eacf0f57c9 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_unique<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x57eacf0b1923 in std::set<int, std::less<int>, std::allocator<int>>::set(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_set.h:249:14
    #10 0x57eacf047323 in make_set(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:55:57
    #11 0x57eacf081d3a in main /work/test/runtime_runner.cpp:2367:23
    #12 0x7dffc02b11c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x7dffc02b128a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x57eaceecf4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3158:8 in f_set_clear_it_guarda(std::set<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7a3fbf5dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a3fbf5dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a3fbf5dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a3fbf5dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a3fbf5dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7a3fbf5e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7a3fbf5e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7a3fbf5e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a3fbf5e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a3fbf5e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a3fbf5e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1252==ABORTING
````

</details>

### f_set_clear_it_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_set_clear_it_bucle(std::set<int>& c) {
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
    const [with _Iterator = std::_Rb_tree_const_iterator<int>; _Sequence = 
    std::debug::set<int>; _Category = std::forward_iterator_tag; reference = 
    const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fff66ad71e0 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::set<int, std::less<int>, std::allocator<int> >' @ 0x7fff66ad72a0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
/include/c++/13/bits/stl_tree.h:613:23
    #5 0x5e6518040ad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x5e65180403e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x5e651803eeb9 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_unique_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x5e651803e7c9 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_unique<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x5e6517ffa923 in std::set<int, std::less<int>, std::allocator<int>>::set(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_set.h:249:14
    #10 0x5e6517f90323 in make_set(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:55:57
    #11 0x5e6517fcae76 in main /work/test/runtime_runner.cpp:2372:23
    #12 0x76b0339891c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x76b03398928a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x5e6517e184b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3164:10 in f_set_clear_it_bucle(std::set<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x72f032bdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x72f032bdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x72f032bdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x72f032bdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x72f032bdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x72f032be0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x72f032be0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x72f032be0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x72f032be0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x72f032be0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x72f032be0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1255==ABORTING
````

</details>

### f_set_clear_it_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `llamada` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_set_clear_it_llamada(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_set_clear(c);
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
    const [with _Iterator = std::_Rb_tree_const_iterator<int>; _Sequence = 
    std::debug::set<int>; _Category = std::forward_iterator_tag; reference = 
    const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffe5fc8afe0 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::set<int, std::less<int>, std::allocator<int> >' @ 0x7ffe5fc8b0a0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
include/c++/13/bits/stl_tree.h:613:23
    #5 0x6489a0f6ead9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x6489a0f6e3e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x6489a0f6ceb9 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_unique_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x6489a0f6c7c9 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_unique<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x6489a0f28923 in std::set<int, std::less<int>, std::allocator<int>>::set(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_set.h:249:14
    #10 0x6489a0ebe323 in make_set(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:55:57
    #11 0x6489a0ef8fb2 in main /work/test/runtime_runner.cpp:2377:23
    #12 0x7519536af1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x7519536af28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x6489a0d464b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3171:8 in f_set_clear_it_llamada(std::set<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7159529dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7159529dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7159529dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7159529dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7159529dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7159529e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7159529e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7159529e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7159529e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7159529e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7159529e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1258==ABORTING
````

</details>

## Handle: referencia

### f_set_clear_ref_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_set_clear_ref_recto(std::set<int>& c) {
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
/include/c++/13/bits/stl_tree.h:613:23
    #5 0x5dfdd8165ad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x5dfdd81653e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x5dfdd8163eb9 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_unique_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x5dfdd81637c9 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_unique<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x5dfdd811f923 in std::set<int, std::less<int>, std::allocator<int>>::set(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_set.h:249:14
    #10 0x5dfdd80b5323 in make_set(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:55:57
    #11 0x5dfdd80f00ee in main /work/test/runtime_runner.cpp:2382:23
    #12 0x7fec131b81c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x7fec131b828a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x5dfdd7f3d4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3177:8 in f_set_clear_ref_recto(std::set<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7c2c123dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c2c123dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c2c123dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c2c123dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c2c123dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c2c123e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7c2c123e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7c2c123e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c2c123e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c2c123e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c2c123e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1261==ABORTING
````

</details>

### f_set_clear_ref_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_set_clear_ref_guarda(std::set<int>& c) {
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
include/c++/13/bits/stl_tree.h:613:23
    #5 0x61a5bbae2ad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x61a5bbae23e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x61a5bbae0eb9 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_unique_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x61a5bbae07c9 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_unique<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x61a5bba9c923 in std::set<int, std::less<int>, std::allocator<int>>::set(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_set.h:249:14
    #10 0x61a5bba32323 in make_set(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:55:57
    #11 0x61a5bba6d22a in main /work/test/runtime_runner.cpp:2387:23
    #12 0x75f54c2091c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x75f54c20928a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x61a5bb8ba4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3184:8 in f_set_clear_ref_guarda(std::set<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x72354b5dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x72354b5dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x72354b5dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x72354b5dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x72354b5dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x72354b5e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x72354b5e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x72354b5e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x72354b5e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x72354b5e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x72354b5e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1264==ABORTING
````

</details>

### f_set_clear_ref_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `bucle` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_set_clear_ref_bucle(std::set<int>& c) {
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
    [with _Iterator = std::_Rb_tree_const_iterator<int>; _Sequence = std::
    debug::set<int>; _Category = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fff74d83e70 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::set<int, std::less<int>, std::allocator<int> >' @ 0x7fff74d83f30
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
include/c++/13/bits/stl_tree.h:613:23
    #5 0x583f1db8bad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x583f1db8b3e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x583f1db89eb9 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_unique_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x583f1db897c9 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_unique<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x583f1db45923 in std::set<int, std::less<int>, std::allocator<int>>::set(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_set.h:249:14
    #10 0x583f1dadb323 in make_set(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:55:57
    #11 0x583f1db16366 in main /work/test/runtime_runner.cpp:2392:23
    #12 0x700516a421c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x700516a4228a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x583f1d9634b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3191:10 in f_set_clear_ref_bucle(std::set<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6c4515ddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6c4515ddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6c4515ddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6c4515ddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6c4515ddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6c4515de0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x6c4515de0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x6c4515de0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6c4515de0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6c4515de0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6c4515de0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1267==ABORTING
````

</details>

### f_set_clear_ref_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_set_clear_ref_llamada(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_set_clear(c);
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
nclude/c++/13/bits/stl_tree.h:613:23
    #5 0x5ac4d495cad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x5ac4d495c3e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x5ac4d495aeb9 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_unique_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x5ac4d495a7c9 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_unique<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x5ac4d4916923 in std::set<int, std::less<int>, std::allocator<int>>::set(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_set.h:249:14
    #10 0x5ac4d48ac323 in make_set(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:55:57
    #11 0x5ac4d48e74a2 in main /work/test/runtime_runner.cpp:2397:23
    #12 0x7d430e5c11c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x7d430e5c128a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x5ac4d47344b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3199:8 in f_set_clear_ref_llamada(std::set<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x79830d7dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x79830d7dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x79830d7dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x79830d7dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x79830d7dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x79830d7e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x79830d7e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x79830d7e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x79830d7e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x79830d7e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x79830d7e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1270==ABORTING
````

</details>

## Handle: puntero

### f_set_clear_ptr_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_set_clear_ptr_recto(std::set<int>& c) {
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
/include/c++/13/bits/stl_tree.h:613:23
    #5 0x5f83281acad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x5f83281ac3e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x5f83281aaeb9 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_unique_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x5f83281aa7c9 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_unique<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x5f8328166923 in std::set<int, std::less<int>, std::allocator<int>>::set(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_set.h:249:14
    #10 0x5f83280fc323 in make_set(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:55:57
    #11 0x5f83281375de in main /work/test/runtime_runner.cpp:2402:23
    #12 0x777e011671c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x777e0116728a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x5f8327f844b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3205:8 in f_set_clear_ptr_recto(std::set<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x73be003dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73be003dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73be003dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73be003dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73be003dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x73be003e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x73be003e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x73be003e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x73be003e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x73be003e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x73be003e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1273==ABORTING
````

</details>

### f_set_clear_ptr_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_set_clear_ptr_guarda(std::set<int>& c) {
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
include/c++/13/bits/stl_tree.h:613:23
    #5 0x62960745ead9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x62960745e3e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x62960745ceb9 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_unique_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x62960745c7c9 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_unique<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x629607418923 in std::set<int, std::less<int>, std::allocator<int>>::set(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_set.h:249:14
    #10 0x6296073ae323 in make_set(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:55:57
    #11 0x6296073e971a in main /work/test/runtime_runner.cpp:2407:23
    #12 0x7ad4acf611c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x7ad4acf6128a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x6296072364b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3212:8 in f_set_clear_ptr_guarda(std::set<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7714ac1dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7714ac1dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7714ac1dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7714ac1dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7714ac1dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7714ac1e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7714ac1e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7714ac1e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7714ac1e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7714ac1e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7714ac1e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1276==ABORTING
````

</details>

### f_set_clear_ptr_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `bucle` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_set_clear_ptr_bucle(std::set<int>& c) {
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
    [with _Iterator = std::_Rb_tree_const_iterator<int>; _Sequence = std::
    debug::set<int>; _Category = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffcf4f54420 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::set<int, std::less<int>, std::allocator<int> >' @ 0x7ffcf4f544e0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
include/c++/13/bits/stl_tree.h:613:23
    #5 0x58200af1cad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x58200af1c3e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x58200af1aeb9 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_unique_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x58200af1a7c9 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_unique<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x58200aed6923 in std::set<int, std::less<int>, std::allocator<int>>::set(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_set.h:249:14
    #10 0x58200ae6c323 in make_set(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:55:57
    #11 0x58200aea7856 in main /work/test/runtime_runner.cpp:2412:23
    #12 0x7919214791c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x79192147928a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x58200acf44b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3219:10 in f_set_clear_ptr_bucle(std::set<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7559207dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7559207dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7559207dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7559207dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7559207dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7559207e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7559207e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7559207e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7559207e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7559207e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7559207e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1279==ABORTING
````

</details>

### f_set_clear_ptr_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_set_clear_ptr_llamada(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_set_clear(c);
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
nclude/c++/13/bits/stl_tree.h:613:23
    #5 0x63f86871cad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x63f86871c3e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x63f86871aeb9 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_unique_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x63f86871a7c9 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_unique<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x63f8686d6923 in std::set<int, std::less<int>, std::allocator<int>>::set(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_set.h:249:14
    #10 0x63f86866c323 in make_set(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:55:57
    #11 0x63f8686a7992 in main /work/test/runtime_runner.cpp:2417:23
    #12 0x7aaaf49061c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x7aaaf490628a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x63f8684f44b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3227:8 in f_set_clear_ptr_llamada(std::set<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x76eaf3bdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x76eaf3bdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x76eaf3bdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x76eaf3bdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x76eaf3bdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x76eaf3be0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x76eaf3be0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x76eaf3be0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x76eaf3be0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x76eaf3be0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x76eaf3be0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1282==ABORTING
````

</details>
