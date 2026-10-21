# `std::multiset::clear`

Mutación: `c.clear();`

- Iterador retenido: 🔴 `UB`
- Referencia/puntero retenido: 🔴 `UB`
- Casos `UB` detectados estáticamente: 5/12

**En palabras:** después de `c.clear();` sobre un `std::multiset`, un iterador guardado queda **inválido**: usarlo después es un bug (UB); una referencia o puntero guardado queda **inválido**: usarlo después es un bug (UB).

Mapa de los 12 casos. Cada celda muestra la respuesta correcta (etiqueta) y, debajo, lo que hizo el analizador estático de Clang. Clic para ir al caso. Ver [Cómo leer este libro](../../guia.md).

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🔴 `UB`<br>❌ no detectado](#f_mset_clear_it_recto) | [🔴 `UB`<br>✅ detectado](#f_mset_clear_it_guarda) | [🔴 `UB`<br>✅ detectado](#f_mset_clear_it_bucle) | [🔴 `UB`<br>✅ detectado](#f_mset_clear_it_llamada) |
| **referencia** | [🔴 `UB`<br>❌ no detectado](#f_mset_clear_ref_recto) | [🔴 `UB`<br>❌ no detectado](#f_mset_clear_ref_guarda) | [🔴 `UB`<br>✅ detectado](#f_mset_clear_ref_bucle) | [🔴 `UB`<br>❌ no detectado](#f_mset_clear_ref_llamada) |
| **puntero** | [🔴 `UB`<br>❌ no detectado](#f_mset_clear_ptr_recto) | [🔴 `UB`<br>❌ no detectado](#f_mset_clear_ptr_guarda) | [🔴 `UB`<br>✅ detectado](#f_mset_clear_ptr_bucle) | [🔴 `UB`<br>❌ no detectado](#f_mset_clear_ptr_llamada) |

## Handle: iterador

### f_mset_clear_it_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_mset_clear_it_recto(std::multiset<int>& c) {
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
    std::debug::multiset<int>; _Category = std::forward_iterator_tag; 
    reference = const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fffdfe29ed0 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::multiset<int, std::less<int>, std::allocator<int> >' @ 0x7fffdfe29f50
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
/stl_tree.h:613:23
    #5 0x5708f86e7ad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x5708f86e73e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x5708f86e8407 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_equal_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x5708f86e8009 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_equal<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x5708f86a1d53 in std::multiset<int, std::less<int>, std::allocator<int>>::multiset(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multiset.h:244:14
    #10 0x5708f86376e3 in make_mset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:56:63
    #11 0x5708f8674eb6 in main /work/test/runtime_runner.cpp:2542:28
    #12 0x75256d4561c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x75256d45628a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x5708f84bf4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3392:8 in f_mset_clear_it_recto(std::multiset<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x71656c7dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x71656c7dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x71656c7dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x71656c7dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x71656c7dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x71656c7e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x71656c7e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x71656c7e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x71656c7e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x71656c7e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x71656c7e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1345==ABORTING
````

</details>

### f_mset_clear_it_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `guarda` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_mset_clear_it_guarda(std::multiset<int>& c) {
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
    std::debug::multiset<int>; _Category = std::forward_iterator_tag; 
    reference = const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffd8446a100 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::multiset<int, std::less<int>, std::allocator<int> >' @ 0x7ffd8446a1c0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
stl_tree.h:613:23
    #5 0x587c68969ad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x587c689693e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x587c6896a407 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_equal_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x587c6896a009 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_equal<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x587c68923d53 in std::multiset<int, std::less<int>, std::allocator<int>>::multiset(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multiset.h:244:14
    #10 0x587c688b96e3 in make_mset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:56:63
    #11 0x587c688f6ff2 in main /work/test/runtime_runner.cpp:2547:28
    #12 0x72adce7c11c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x72adce7c128a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x587c687414b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3398:8 in f_mset_clear_it_guarda(std::multiset<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6eedcd9dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6eedcd9dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6eedcd9dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6eedcd9dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6eedcd9dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6eedcd9e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x6eedcd9e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x6eedcd9e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6eedcd9e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6eedcd9e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6eedcd9e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1348==ABORTING
````

</details>

### f_mset_clear_it_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_mset_clear_it_bucle(std::multiset<int>& c) {
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
    std::debug::multiset<int>; _Category = std::forward_iterator_tag; 
    reference = const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffd78d94460 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::multiset<int, std::less<int>, std::allocator<int> >' @ 0x7ffd78d94520
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
stl_tree.h:613:23
    #5 0x5b76f13dbad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x5b76f13db3e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x5b76f13dc407 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_equal_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x5b76f13dc009 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_equal<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x5b76f1395d53 in std::multiset<int, std::less<int>, std::allocator<int>>::multiset(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multiset.h:244:14
    #10 0x5b76f132b6e3 in make_mset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:56:63
    #11 0x5b76f136912e in main /work/test/runtime_runner.cpp:2552:28
    #12 0x743ba6cfd1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x743ba6cfd28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x5b76f11b34b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3404:10 in f_mset_clear_it_bucle(std::multiset<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x707ba5fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x707ba5fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x707ba5fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x707ba5fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x707ba5fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x707ba5fe0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x707ba5fe0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x707ba5fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x707ba5fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x707ba5fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x707ba5fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1351==ABORTING
````

</details>

### f_mset_clear_it_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `llamada` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_mset_clear_it_llamada(std::multiset<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_mset_clear(c);
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
    std::debug::multiset<int>; _Category = std::forward_iterator_tag; 
    reference = const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffd10ab6e80 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::multiset<int, std::less<int>, std::allocator<int> >' @ 0x7ffd10ab6f40
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
tl_tree.h:613:23
    #5 0x5f1a61b0cad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x5f1a61b0c3e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x5f1a61b0d407 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_equal_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x5f1a61b0d009 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_equal<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x5f1a61ac6d53 in std::multiset<int, std::less<int>, std::allocator<int>>::multiset(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multiset.h:244:14
    #10 0x5f1a61a5c6e3 in make_mset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:56:63
    #11 0x5f1a61a9a26a in main /work/test/runtime_runner.cpp:2557:28
    #12 0x770ad10e01c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x770ad10e028a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x5f1a618e44b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3411:8 in f_mset_clear_it_llamada(std::multiset<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x734ad03dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x734ad03dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x734ad03dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x734ad03dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x734ad03dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x734ad03e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x734ad03e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x734ad03e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x734ad03e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x734ad03e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x734ad03e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1354==ABORTING
````

</details>

## Handle: referencia

### f_mset_clear_ref_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_mset_clear_ref_recto(std::multiset<int>& c) {
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
stl_tree.h:613:23
    #5 0x623b04f87ad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x623b04f873e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x623b04f88407 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_equal_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x623b04f88009 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_equal<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x623b04f41d53 in std::multiset<int, std::less<int>, std::allocator<int>>::multiset(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multiset.h:244:14
    #10 0x623b04ed76e3 in make_mset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:56:63
    #11 0x623b04f153a6 in main /work/test/runtime_runner.cpp:2562:28
    #12 0x72aeca9c81c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x72aeca9c828a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x623b04d5f4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3417:8 in f_mset_clear_ref_recto(std::multiset<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6eeec9bdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6eeec9bdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6eeec9bdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6eeec9bdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6eeec9bdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6eeec9be0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x6eeec9be0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x6eeec9be0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6eeec9be0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6eeec9be0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6eeec9be0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1357==ABORTING
````

</details>

### f_mset_clear_ref_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_mset_clear_ref_guarda(std::multiset<int>& c) {
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
tl_tree.h:613:23
    #5 0x5e3083848ad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x5e30838483e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x5e3083849407 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_equal_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x5e3083849009 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_equal<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x5e3083802d53 in std::multiset<int, std::less<int>, std::allocator<int>>::multiset(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multiset.h:244:14
    #10 0x5e30837986e3 in make_mset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:56:63
    #11 0x5e30837d64e2 in main /work/test/runtime_runner.cpp:2567:28
    #12 0x77739860b1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x77739860b28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x5e30836204b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3424:8 in f_mset_clear_ref_guarda(std::multiset<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x73b3979dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73b3979dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73b3979dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73b3979dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73b3979dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x73b3979e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x73b3979e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x73b3979e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x73b3979e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x73b3979e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x73b3979e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1360==ABORTING
````

</details>

### f_mset_clear_ref_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `bucle` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_mset_clear_ref_bucle(std::multiset<int>& c) {
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
    debug::multiset<int>; _Category = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffc535cae80 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::multiset<int, std::less<int>, std::allocator<int> >' @ 0x7ffc535caf40
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
tl_tree.h:613:23
    #5 0x612a761c6ad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x612a761c63e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x612a761c7407 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_equal_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x612a761c7009 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_equal<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x612a76180d53 in std::multiset<int, std::less<int>, std::allocator<int>>::multiset(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multiset.h:244:14
    #10 0x612a761166e3 in make_mset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:56:63
    #11 0x612a7615461e in main /work/test/runtime_runner.cpp:2572:28
    #12 0x79110ae231c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x79110ae2328a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x612a75f9e4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3431:10 in f_mset_clear_ref_bucle(std::multiset<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x75510a1dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75510a1dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75510a1dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75510a1dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75510a1dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x75510a1e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x75510a1e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x75510a1e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x75510a1e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x75510a1e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x75510a1e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1363==ABORTING
````

</details>

### f_mset_clear_ref_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_mset_clear_ref_llamada(std::multiset<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_mset_clear(c);
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
l_tree.h:613:23
    #5 0x5efa493b9ad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x5efa493b93e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x5efa493ba407 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_equal_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x5efa493ba009 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_equal<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x5efa49373d53 in std::multiset<int, std::less<int>, std::allocator<int>>::multiset(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multiset.h:244:14
    #10 0x5efa493096e3 in make_mset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:56:63
    #11 0x5efa4934775a in main /work/test/runtime_runner.cpp:2577:28
    #12 0x731700deb1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x731700deb28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x5efa491914b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3439:8 in f_mset_clear_ref_llamada(std::multiset<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6f57001dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f57001dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f57001dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f57001dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f57001dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6f57001e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x6f57001e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x6f57001e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f57001e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f57001e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f57001e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1366==ABORTING
````

</details>

## Handle: puntero

### f_mset_clear_ptr_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_mset_clear_ptr_recto(std::multiset<int>& c) {
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
stl_tree.h:613:23
    #5 0x56f4bd387ad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x56f4bd3873e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x56f4bd388407 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_equal_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x56f4bd388009 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_equal<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x56f4bd341d53 in std::multiset<int, std::less<int>, std::allocator<int>>::multiset(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multiset.h:244:14
    #10 0x56f4bd2d76e3 in make_mset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:56:63
    #11 0x56f4bd315896 in main /work/test/runtime_runner.cpp:2582:28
    #12 0x7fa9def6c1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x7fa9def6c28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x56f4bd15f4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3445:8 in f_mset_clear_ptr_recto(std::multiset<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7be9de1dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7be9de1dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7be9de1dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7be9de1dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7be9de1dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7be9de1e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7be9de1e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7be9de1e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7be9de1e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7be9de1e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7be9de1e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1369==ABORTING
````

</details>

### f_mset_clear_ptr_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_mset_clear_ptr_guarda(std::multiset<int>& c) {
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
tl_tree.h:613:23
    #5 0x63435ba58ad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x63435ba583e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x63435ba59407 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_equal_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x63435ba59009 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_equal<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x63435ba12d53 in std::multiset<int, std::less<int>, std::allocator<int>>::multiset(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multiset.h:244:14
    #10 0x63435b9a86e3 in make_mset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:56:63
    #11 0x63435b9e69d2 in main /work/test/runtime_runner.cpp:2587:28
    #12 0x794b8d6ea1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x794b8d6ea28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x63435b8304b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3452:8 in f_mset_clear_ptr_guarda(std::multiset<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x758b8c9dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x758b8c9dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x758b8c9dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x758b8c9dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x758b8c9dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x758b8c9e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x758b8c9e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x758b8c9e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x758b8c9e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x758b8c9e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x758b8c9e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1372==ABORTING
````

</details>

### f_mset_clear_ptr_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `bucle` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_mset_clear_ptr_bucle(std::multiset<int>& c) {
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
    debug::multiset<int>; _Category = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffd6649d3b0 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::multiset<int, std::less<int>, std::allocator<int> >' @ 0x7ffd6649d470
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
tl_tree.h:613:23
    #5 0x55a475c37ad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x55a475c373e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x55a475c38407 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_equal_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x55a475c38009 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_equal<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x55a475bf1d53 in std::multiset<int, std::less<int>, std::allocator<int>>::multiset(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multiset.h:244:14
    #10 0x55a475b876e3 in make_mset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:56:63
    #11 0x55a475bc5b0e in main /work/test/runtime_runner.cpp:2592:28
    #12 0x7825b621f1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x7825b621f28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x55a475a0f4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3459:10 in f_mset_clear_ptr_bucle(std::multiset<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7465b55dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7465b55dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7465b55dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7465b55dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7465b55dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7465b55e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7465b55e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7465b55e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7465b55e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7465b55e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7465b55e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1375==ABORTING
````

</details>

### f_mset_clear_ptr_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_mset_clear_ptr_llamada(std::multiset<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_mset_clear(c);
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
l_tree.h:613:23
    #5 0x5be4c1e06ad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x5be4c1e063e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x5be4c1e07407 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_equal_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x5be4c1e07009 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_equal<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x5be4c1dc0d53 in std::multiset<int, std::less<int>, std::allocator<int>>::multiset(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multiset.h:244:14
    #10 0x5be4c1d566e3 in make_mset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:56:63
    #11 0x5be4c1d94c4a in main /work/test/runtime_runner.cpp:2597:28
    #12 0x7ddd0b6961c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x7ddd0b69628a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x5be4c1bde4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3467:8 in f_mset_clear_ptr_llamada(std::multiset<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7a1d0a9dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a1d0a9dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a1d0a9dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a1d0a9dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a1d0a9dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7a1d0a9e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7a1d0a9e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7a1d0a9e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a1d0a9e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a1d0a9e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a1d0a9e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1378==ABORTING
````

</details>
