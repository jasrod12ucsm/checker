# `std::multiset::erase_begin`

Mutación: `c.erase(c.begin());`

- Iterador retenido: 🔴 `UB`
- Referencia/puntero retenido: 🔴 `UB`
- Casos `UB` detectados estáticamente: 0/12

**En palabras:** después de `c.erase(c.begin());` sobre un `std::multiset`, un iterador guardado queda **inválido**: usarlo después es un bug (UB); una referencia o puntero guardado queda **inválido**: usarlo después es un bug (UB).

Mapa de los 12 casos. Cada celda muestra la respuesta correcta (etiqueta) y, debajo, lo que hizo el analizador estático de Clang. Clic para ir al caso. Ver [Cómo leer este libro](../../guia.md).

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🔴 `UB`<br>❌ no detectado](#f_mset_erase_begin_it_recto) | [🔴 `UB`<br>❌ no detectado](#f_mset_erase_begin_it_guarda) | [🔴 `UB`<br>❌ no detectado](#f_mset_erase_begin_it_bucle) | [🔴 `UB`<br>❌ no detectado](#f_mset_erase_begin_it_llamada) |
| **referencia** | [🔴 `UB`<br>❌ no detectado](#f_mset_erase_begin_ref_recto) | [🔴 `UB`<br>❌ no detectado](#f_mset_erase_begin_ref_guarda) | [🔴 `UB`<br>❌ no detectado](#f_mset_erase_begin_ref_bucle) | [🔴 `UB`<br>❌ no detectado](#f_mset_erase_begin_ref_llamada) |
| **puntero** | [🔴 `UB`<br>❌ no detectado](#f_mset_erase_begin_ptr_recto) | [🔴 `UB`<br>❌ no detectado](#f_mset_erase_begin_ptr_guarda) | [🔴 `UB`<br>❌ no detectado](#f_mset_erase_begin_ptr_bucle) | [🔴 `UB`<br>❌ no detectado](#f_mset_erase_begin_ptr_llamada) |

## Handle: iterador

### f_mset_erase_begin_it_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_mset_erase_begin_it_recto(std::multiset<int>& c) {
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
    const [with _Iterator = std::_Rb_tree_const_iterator<int>; _Sequence = 
    std::debug::multiset<int>; _Category = std::forward_iterator_tag; 
    reference = const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffc7dc23a50 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::multiset<int, std::less<int>, std::allocator<int> >' @ 0x7ffc7dc23b40
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
ree.h:613:23
    #5 0x5678607e5ad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x5678607e53e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x5678607e6407 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_equal_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x5678607e6009 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_equal<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x56786079fd53 in std::multiset<int, std::less<int>, std::allocator<int>>::multiset(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multiset.h:244:14
    #10 0x5678607356e3 in make_mset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:56:63
    #11 0x567860771cc2 in main /work/test/runtime_runner.cpp:2482:28
    #12 0x72d96aed01c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x72d96aed028a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x5678605bd4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3312:8 in f_mset_erase_begin_it_recto(std::multiset<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6f196a1dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f196a1dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f196a1dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f196a1dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f196a1dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6f196a1e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x6f196a1e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x6f196a1e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f196a1e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f196a1e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f196a1e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1309==ABORTING
````

</details>

### f_mset_erase_begin_it_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_mset_erase_begin_it_guarda(std::multiset<int>& c) {
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
    const [with _Iterator = std::_Rb_tree_const_iterator<int>; _Sequence = 
    std::debug::multiset<int>; _Category = std::forward_iterator_tag; 
    reference = const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffe0965d080 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::multiset<int, std::less<int>, std::allocator<int> >' @ 0x7ffe0965d170
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
ee.h:613:23
    #5 0x59aad43bfad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x59aad43bf3e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x59aad43c0407 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_equal_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x59aad43c0009 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_equal<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x59aad4379d53 in std::multiset<int, std::less<int>, std::allocator<int>>::multiset(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multiset.h:244:14
    #10 0x59aad430f6e3 in make_mset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:56:63
    #11 0x59aad434be41 in main /work/test/runtime_runner.cpp:2487:28
    #12 0x745af65f41c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x745af65f428a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x59aad41974b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3318:8 in f_mset_erase_begin_it_guarda(std::multiset<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x709af59dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x709af59dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x709af59dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x709af59dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x709af59dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x709af59e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x709af59e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x709af59e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x709af59e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x709af59e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x709af59e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1312==ABORTING
````

</details>

### f_mset_erase_begin_it_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_mset_erase_begin_it_bucle(std::multiset<int>& c) {
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
    const [with _Iterator = std::_Rb_tree_const_iterator<int>; _Sequence = 
    std::debug::multiset<int>; _Category = std::forward_iterator_tag; 
    reference = const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffe782bc160 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::multiset<int, std::less<int>, std::allocator<int> >' @ 0x7ffe782bc250
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
ee.h:613:23
    #5 0x63746d816ad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x63746d8163e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x63746d817407 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_equal_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x63746d817009 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_equal<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x63746d7d0d53 in std::multiset<int, std::less<int>, std::allocator<int>>::multiset(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multiset.h:244:14
    #10 0x63746d7666e3 in make_mset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:56:63
    #11 0x63746d7a2fc0 in main /work/test/runtime_runner.cpp:2492:28
    #12 0x74c96743d1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x74c96743d28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x63746d5ee4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3324:10 in f_mset_erase_begin_it_bucle(std::multiset<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7109667dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7109667dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7109667dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7109667dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7109667dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7109667e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7109667e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7109667e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7109667e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7109667e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7109667e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1315==ABORTING
````

</details>

### f_mset_erase_begin_it_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_mset_erase_begin_it_llamada(std::multiset<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_mset_erase_begin(c);
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
    const [with _Iterator = std::_Rb_tree_const_iterator<int>; _Sequence = 
    std::debug::multiset<int>; _Category = std::forward_iterator_tag; 
    reference = const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffcd52cf030 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::multiset<int, std::less<int>, std::allocator<int> >' @ 0x7ffcd52cf0f0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
e.h:613:23
    #5 0x5d170d573ad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x5d170d5733e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x5d170d574407 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_equal_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x5d170d574009 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_equal<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x5d170d52dd53 in std::multiset<int, std::less<int>, std::allocator<int>>::multiset(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multiset.h:244:14
    #10 0x5d170d4c36e3 in make_mset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:56:63
    #11 0x5d170d50013f in main /work/test/runtime_runner.cpp:2497:28
    #12 0x7ce1bca461c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x7ce1bca4628a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x5d170d34b4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3331:8 in f_mset_erase_begin_it_llamada(std::multiset<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7921bbddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7921bbddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7921bbddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7921bbddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7921bbddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7921bbde0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7921bbde0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7921bbde0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7921bbde0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7921bbde0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7921bbde0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1318==ABORTING
````

</details>

## Handle: referencia

### f_mset_erase_begin_ref_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_mset_erase_begin_ref_recto(std::multiset<int>& c) {
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
ee.h:613:23
    #5 0x5e54dd4bdad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x5e54dd4bd3e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x5e54dd4be407 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_equal_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x5e54dd4be009 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_equal<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x5e54dd477d53 in std::multiset<int, std::less<int>, std::allocator<int>>::multiset(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multiset.h:244:14
    #10 0x5e54dd40d6e3 in make_mset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:56:63
    #11 0x5e54dd44a2be in main /work/test/runtime_runner.cpp:2502:28
    #12 0x72080a5581c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x72080a55828a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x5e54dd2954b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3337:8 in f_mset_erase_begin_ref_recto(std::multiset<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6e48097dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e48097dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e48097dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e48097dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e48097dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6e48097e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x6e48097e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x6e48097e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e48097e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e48097e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e48097e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1321==ABORTING
````

</details>

### f_mset_erase_begin_ref_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_mset_erase_begin_ref_guarda(std::multiset<int>& c) {
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
e.h:613:23
    #5 0x58a19ffebad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x58a19ffeb3e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x58a19ffec407 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_equal_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x58a19ffec009 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_equal<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x58a19ffa5d53 in std::multiset<int, std::less<int>, std::allocator<int>>::multiset(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multiset.h:244:14
    #10 0x58a19ff3b6e3 in make_mset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:56:63
    #11 0x58a19ff7843d in main /work/test/runtime_runner.cpp:2507:28
    #12 0x7354cbf9a1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x7354cbf9a28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x58a19fdc34b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3344:8 in f_mset_erase_begin_ref_guarda(std::multiset<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6f94cb1dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f94cb1dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f94cb1dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f94cb1dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f94cb1dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6f94cb1e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x6f94cb1e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x6f94cb1e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f94cb1e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f94cb1e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f94cb1e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1324==ABORTING
````

</details>

### f_mset_erase_begin_ref_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `bucle` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_mset_erase_begin_ref_bucle(std::multiset<int>& c) {
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
    [with _Iterator = std::_Rb_tree_const_iterator<int>; _Sequence = std::
    debug::multiset<int>; _Category = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffc149dd730 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::multiset<int, std::less<int>, std::allocator<int> >' @ 0x7ffc149dd820
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
e.h:613:23
    #5 0x5720c6630ad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x5720c66303e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x5720c6631407 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_equal_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x5720c6631009 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_equal<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x5720c65ead53 in std::multiset<int, std::less<int>, std::allocator<int>>::multiset(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multiset.h:244:14
    #10 0x5720c65806e3 in make_mset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:56:63
    #11 0x5720c65bd5bc in main /work/test/runtime_runner.cpp:2512:28
    #12 0x7cb8da55c1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x7cb8da55c28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x5720c64084b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3351:10 in f_mset_erase_begin_ref_bucle(std::multiset<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x78f8d97dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x78f8d97dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x78f8d97dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x78f8d97dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x78f8d97dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x78f8d97e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x78f8d97e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x78f8d97e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x78f8d97e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x78f8d97e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x78f8d97e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1327==ABORTING
````

</details>

### f_mset_erase_begin_ref_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_mset_erase_begin_ref_llamada(std::multiset<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_mset_erase_begin(c);
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
.h:613:23
    #5 0x61615a3fbad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x61615a3fb3e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x61615a3fc407 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_equal_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x61615a3fc009 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_equal<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x61615a3b5d53 in std::multiset<int, std::less<int>, std::allocator<int>>::multiset(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multiset.h:244:14
    #10 0x61615a34b6e3 in make_mset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:56:63
    #11 0x61615a38873b in main /work/test/runtime_runner.cpp:2517:28
    #12 0x7b1ca4db11c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x7b1ca4db128a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x61615a1d34b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3359:8 in f_mset_erase_begin_ref_llamada(std::multiset<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x775ca3fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x775ca3fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x775ca3fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x775ca3fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x775ca3fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x775ca3fe0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x775ca3fe0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x775ca3fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x775ca3fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x775ca3fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x775ca3fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1330==ABORTING
````

</details>

## Handle: puntero

### f_mset_erase_begin_ptr_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_mset_erase_begin_ptr_recto(std::multiset<int>& c) {
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
ee.h:613:23
    #5 0x5d3d440f1ad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x5d3d440f13e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x5d3d440f2407 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_equal_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x5d3d440f2009 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_equal<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x5d3d440abd53 in std::multiset<int, std::less<int>, std::allocator<int>>::multiset(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multiset.h:244:14
    #10 0x5d3d440416e3 in make_mset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:56:63
    #11 0x5d3d4407e8ba in main /work/test/runtime_runner.cpp:2522:28
    #12 0x71ce2f78c1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x71ce2f78c28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x5d3d43ec94b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3365:8 in f_mset_erase_begin_ptr_recto(std::multiset<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6e0e2e9dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e0e2e9dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e0e2e9dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e0e2e9dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e0e2e9dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6e0e2e9e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x6e0e2e9e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x6e0e2e9e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e0e2e9e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e0e2e9e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e0e2e9e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1333==ABORTING
````

</details>

### f_mset_erase_begin_ptr_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_mset_erase_begin_ptr_guarda(std::multiset<int>& c) {
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
e.h:613:23
    #5 0x622dd5126ad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x622dd51263e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x622dd5127407 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_equal_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x622dd5127009 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_equal<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x622dd50e0d53 in std::multiset<int, std::less<int>, std::allocator<int>>::multiset(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multiset.h:244:14
    #10 0x622dd50766e3 in make_mset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:56:63
    #11 0x622dd50b3a39 in main /work/test/runtime_runner.cpp:2527:28
    #12 0x73d7395371c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x73d73953728a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x622dd4efe4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3372:8 in f_mset_erase_begin_ptr_guarda(std::multiset<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7017387dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7017387dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7017387dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7017387dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7017387dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7017387e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7017387e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7017387e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7017387e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7017387e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7017387e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1336==ABORTING
````

</details>

### f_mset_erase_begin_ptr_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `bucle` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_mset_erase_begin_ptr_bucle(std::multiset<int>& c) {
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
    [with _Iterator = std::_Rb_tree_const_iterator<int>; _Sequence = std::
    debug::multiset<int>; _Category = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fff20a0ad30 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::multiset<int, std::less<int>, std::allocator<int> >' @ 0x7fff20a0ae20
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
e.h:613:23
    #5 0x609e44cadad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x609e44cad3e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x609e44cae407 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_equal_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x609e44cae009 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_equal<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x609e44c67d53 in std::multiset<int, std::less<int>, std::allocator<int>>::multiset(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multiset.h:244:14
    #10 0x609e44bfd6e3 in make_mset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:56:63
    #11 0x609e44c3abb8 in main /work/test/runtime_runner.cpp:2532:28
    #12 0x76d22234a1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x76d22234a28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x609e44a854b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3379:10 in f_mset_erase_begin_ptr_bucle(std::multiset<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7312215dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7312215dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7312215dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7312215dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7312215dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7312215e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7312215e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7312215e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7312215e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7312215e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7312215e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1339==ABORTING
````

</details>

### f_mset_erase_begin_ptr_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_mset_erase_begin_ptr_llamada(std::multiset<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_mset_erase_begin(c);
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
.h:613:23
    #5 0x582c8c858ad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x582c8c8583e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x582c8c859407 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_equal_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x582c8c859009 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_equal<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x582c8c812d53 in std::multiset<int, std::less<int>, std::allocator<int>>::multiset(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multiset.h:244:14
    #10 0x582c8c7a86e3 in make_mset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:56:63
    #11 0x582c8c7e5d37 in main /work/test/runtime_runner.cpp:2537:28
    #12 0x7e0a037cf1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x7e0a037cf28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x582c8c6304b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3387:8 in f_mset_erase_begin_ptr_llamada(std::multiset<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7a4a02bdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a4a02bdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a4a02bdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a4a02bdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a4a02bdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7a4a02be0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7a4a02be0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7a4a02be0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a4a02be0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a4a02be0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a4a02be0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1342==ABORTING
````

</details>
