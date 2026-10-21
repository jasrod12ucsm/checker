# `std::set::erase_begin`

Mutación: `c.erase(c.begin());`

- Iterador retenido: 🔴 `UB`
- Referencia/puntero retenido: 🔴 `UB`
- Casos `UB` detectados estáticamente: 0/12

**En palabras:** después de `c.erase(c.begin());` sobre un `std::set`, un iterador guardado queda **inválido**: usarlo después es un bug (UB); una referencia o puntero guardado queda **inválido**: usarlo después es un bug (UB).

Mapa de los 12 casos. Cada celda muestra la respuesta correcta (etiqueta) y, debajo, lo que hizo el analizador estático de Clang. Clic para ir al caso. Ver [Cómo leer este libro](../../guia.md).

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🔴 `UB`<br>❌ no detectado](#f_set_erase_begin_it_recto) | [🔴 `UB`<br>❌ no detectado](#f_set_erase_begin_it_guarda) | [🔴 `UB`<br>❌ no detectado](#f_set_erase_begin_it_bucle) | [🔴 `UB`<br>❌ no detectado](#f_set_erase_begin_it_llamada) |
| **referencia** | [🔴 `UB`<br>❌ no detectado](#f_set_erase_begin_ref_recto) | [🔴 `UB`<br>❌ no detectado](#f_set_erase_begin_ref_guarda) | [🔴 `UB`<br>❌ no detectado](#f_set_erase_begin_ref_bucle) | [🔴 `UB`<br>❌ no detectado](#f_set_erase_begin_ref_llamada) |
| **puntero** | [🔴 `UB`<br>❌ no detectado](#f_set_erase_begin_ptr_recto) | [🔴 `UB`<br>❌ no detectado](#f_set_erase_begin_ptr_guarda) | [🔴 `UB`<br>❌ no detectado](#f_set_erase_begin_ptr_bucle) | [🔴 `UB`<br>❌ no detectado](#f_set_erase_begin_ptr_llamada) |

## Handle: iterador

### f_set_erase_begin_it_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_set_erase_begin_it_recto(std::set<int>& c) {
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
    std::debug::set<int>; _Category = std::forward_iterator_tag; reference = 
    const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffcd9771560 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::set<int, std::less<int>, std::allocator<int> >' @ 0x7ffcd9771650
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
ude/c++/13/bits/stl_tree.h:613:23
    #5 0x5b8d8edf7ad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x5b8d8edf73e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x5b8d8edf5eb9 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_unique_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x5b8d8edf57c9 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_unique<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x5b8d8edb1923 in std::set<int, std::less<int>, std::allocator<int>>::set(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_set.h:249:14
    #10 0x5b8d8ed47323 in make_set(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:55:57
    #11 0x5b8d8ed80a0a in main /work/test/runtime_runner.cpp:2302:23
    #12 0x7cedb1c121c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x7cedb1c1228a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x5b8d8ebcf4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3072:8 in f_set_erase_begin_it_recto(std::set<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x792db0fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x792db0fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x792db0fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x792db0fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x792db0fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x792db0fe0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x792db0fe0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x792db0fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x792db0fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x792db0fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x792db0fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1213==ABORTING
````

</details>

### f_set_erase_begin_it_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_set_erase_begin_it_guarda(std::set<int>& c) {
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
    std::debug::set<int>; _Category = std::forward_iterator_tag; reference = 
    const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffdaec15000 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::set<int, std::less<int>, std::allocator<int> >' @ 0x7ffdaec150f0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
de/c++/13/bits/stl_tree.h:613:23
    #5 0x57d2f079fad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x57d2f079f3e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x57d2f079deb9 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_unique_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x57d2f079d7c9 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_unique<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x57d2f0759923 in std::set<int, std::less<int>, std::allocator<int>>::set(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_set.h:249:14
    #10 0x57d2f06ef323 in make_set(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:55:57
    #11 0x57d2f0728b89 in main /work/test/runtime_runner.cpp:2307:23
    #12 0x787f2fe521c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x787f2fe5228a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x57d2f05774b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3078:8 in f_set_erase_begin_it_guarda(std::set<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x74bf2f1dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x74bf2f1dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x74bf2f1dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x74bf2f1dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x74bf2f1dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x74bf2f1e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x74bf2f1e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x74bf2f1e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x74bf2f1e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x74bf2f1e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x74bf2f1e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1216==ABORTING
````

</details>

### f_set_erase_begin_it_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_set_erase_begin_it_bucle(std::set<int>& c) {
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
    std::debug::set<int>; _Category = std::forward_iterator_tag; reference = 
    const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffd44112a40 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::set<int, std::less<int>, std::allocator<int> >' @ 0x7ffd44112b30
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
de/c++/13/bits/stl_tree.h:613:23
    #5 0x59d707e0fad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x59d707e0f3e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x59d707e0deb9 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_unique_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x59d707e0d7c9 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_unique<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x59d707dc9923 in std::set<int, std::less<int>, std::allocator<int>>::set(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_set.h:249:14
    #10 0x59d707d5f323 in make_set(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:55:57
    #11 0x59d707d98d08 in main /work/test/runtime_runner.cpp:2312:23
    #12 0x76cb6ecbf1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x76cb6ecbf28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x59d707be74b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3084:10 in f_set_erase_begin_it_bucle(std::set<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x730b6dfdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x730b6dfdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x730b6dfdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x730b6dfdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x730b6dfdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x730b6dfe0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x730b6dfe0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x730b6dfe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x730b6dfe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x730b6dfe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x730b6dfe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1219==ABORTING
````

</details>

### f_set_erase_begin_it_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_set_erase_begin_it_llamada(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_set_erase_begin(c);
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
    std::debug::set<int>; _Category = std::forward_iterator_tag; reference = 
    const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffe39e1d6f0 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::set<int, std::less<int>, std::allocator<int> >' @ 0x7ffe39e1d7b0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
e/c++/13/bits/stl_tree.h:613:23
    #5 0x5e0cbb8f9ad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x5e0cbb8f93e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x5e0cbb8f7eb9 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_unique_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x5e0cbb8f77c9 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_unique<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x5e0cbb8b3923 in std::set<int, std::less<int>, std::allocator<int>>::set(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_set.h:249:14
    #10 0x5e0cbb849323 in make_set(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:55:57
    #11 0x5e0cbb882e87 in main /work/test/runtime_runner.cpp:2317:23
    #12 0x73276c0991c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x73276c09928a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x5e0cbb6d14b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3091:8 in f_set_erase_begin_it_llamada(std::set<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6f676b3dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f676b3dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f676b3dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f676b3dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f676b3dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6f676b3e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x6f676b3e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x6f676b3e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f676b3e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f676b3e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f676b3e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1222==ABORTING
````

</details>

## Handle: referencia

### f_set_erase_begin_ref_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_set_erase_begin_ref_recto(std::set<int>& c) {
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
de/c++/13/bits/stl_tree.h:613:23
    #5 0x5d3ed4899ad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x5d3ed48993e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x5d3ed4897eb9 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_unique_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x5d3ed48977c9 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_unique<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x5d3ed4853923 in std::set<int, std::less<int>, std::allocator<int>>::set(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_set.h:249:14
    #10 0x5d3ed47e9323 in make_set(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:55:57
    #11 0x5d3ed4823006 in main /work/test/runtime_runner.cpp:2322:23
    #12 0x7574c04c41c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x7574c04c428a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x5d3ed46714b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3097:8 in f_set_erase_begin_ref_recto(std::set<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x71b4bf7dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x71b4bf7dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x71b4bf7dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x71b4bf7dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x71b4bf7dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x71b4bf7e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x71b4bf7e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x71b4bf7e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x71b4bf7e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x71b4bf7e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x71b4bf7e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1225==ABORTING
````

</details>

### f_set_erase_begin_ref_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_set_erase_begin_ref_guarda(std::set<int>& c) {
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
e/c++/13/bits/stl_tree.h:613:23
    #5 0x623f20de7ad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x623f20de73e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x623f20de5eb9 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_unique_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x623f20de57c9 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_unique<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x623f20da1923 in std::set<int, std::less<int>, std::allocator<int>>::set(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_set.h:249:14
    #10 0x623f20d37323 in make_set(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:55:57
    #11 0x623f20d71185 in main /work/test/runtime_runner.cpp:2327:23
    #12 0x73df0a0411c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x73df0a04128a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x623f20bbf4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3104:8 in f_set_erase_begin_ref_guarda(std::set<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x701f093dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x701f093dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x701f093dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x701f093dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x701f093dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x701f093e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x701f093e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x701f093e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x701f093e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x701f093e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x701f093e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1228==ABORTING
````

</details>

### f_set_erase_begin_ref_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `bucle` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_set_erase_begin_ref_bucle(std::set<int>& c) {
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
    debug::set<int>; _Category = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffe1f9d7fb0 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::set<int, std::less<int>, std::allocator<int> >' @ 0x7ffe1f9d80a0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
e/c++/13/bits/stl_tree.h:613:23
    #5 0x62ab08c88ad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x62ab08c883e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x62ab08c86eb9 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_unique_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x62ab08c867c9 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_unique<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x62ab08c42923 in std::set<int, std::less<int>, std::allocator<int>>::set(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_set.h:249:14
    #10 0x62ab08bd8323 in make_set(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:55:57
    #11 0x62ab08c12304 in main /work/test/runtime_runner.cpp:2332:23
    #12 0x7e95043ed1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x7e95043ed28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x62ab08a604b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3111:10 in f_set_erase_begin_ref_bucle(std::set<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7ad5037dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ad5037dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ad5037dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ad5037dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ad5037dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7ad5037e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7ad5037e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7ad5037e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ad5037e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ad5037e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ad5037e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1231==ABORTING
````

</details>

### f_set_erase_begin_ref_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_set_erase_begin_ref_llamada(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_set_erase_begin(c);
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
/c++/13/bits/stl_tree.h:613:23
    #5 0x5b7fb687fad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x5b7fb687f3e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x5b7fb687deb9 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_unique_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x5b7fb687d7c9 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_unique<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x5b7fb6839923 in std::set<int, std::less<int>, std::allocator<int>>::set(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_set.h:249:14
    #10 0x5b7fb67cf323 in make_set(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:55:57
    #11 0x5b7fb6809483 in main /work/test/runtime_runner.cpp:2337:23
    #12 0x7ea206a071c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x7ea206a0728a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x5b7fb66574b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3119:8 in f_set_erase_begin_ref_llamada(std::set<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7ae205ddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ae205ddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ae205ddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ae205ddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ae205ddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7ae205de0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7ae205de0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7ae205de0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ae205de0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ae205de0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ae205de0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1234==ABORTING
````

</details>

## Handle: puntero

### f_set_erase_begin_ptr_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_set_erase_begin_ptr_recto(std::set<int>& c) {
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
de/c++/13/bits/stl_tree.h:613:23
    #5 0x5ddcb26ccad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x5ddcb26cc3e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x5ddcb26caeb9 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_unique_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x5ddcb26ca7c9 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_unique<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x5ddcb2686923 in std::set<int, std::less<int>, std::allocator<int>>::set(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_set.h:249:14
    #10 0x5ddcb261c323 in make_set(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:55:57
    #11 0x5ddcb2656602 in main /work/test/runtime_runner.cpp:2342:23
    #12 0x78f3441ed1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x78f3441ed28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x5ddcb24a44b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3125:8 in f_set_erase_begin_ptr_recto(std::set<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7533435dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7533435dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7533435dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7533435dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7533435dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7533435e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7533435e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7533435e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7533435e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7533435e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7533435e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1237==ABORTING
````

</details>

### f_set_erase_begin_ptr_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_set_erase_begin_ptr_guarda(std::set<int>& c) {
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
e/c++/13/bits/stl_tree.h:613:23
    #5 0x61b1ae1cdad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x61b1ae1cd3e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x61b1ae1cbeb9 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_unique_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x61b1ae1cb7c9 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_unique<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x61b1ae187923 in std::set<int, std::less<int>, std::allocator<int>>::set(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_set.h:249:14
    #10 0x61b1ae11d323 in make_set(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:55:57
    #11 0x61b1ae157781 in main /work/test/runtime_runner.cpp:2347:23
    #12 0x72ba9dd301c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x72ba9dd3028a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x61b1adfa54b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3132:8 in f_set_erase_begin_ptr_guarda(std::set<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6efa9cfdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6efa9cfdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6efa9cfdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6efa9cfdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6efa9cfdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6efa9cfe0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x6efa9cfe0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x6efa9cfe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6efa9cfe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6efa9cfe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6efa9cfe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1240==ABORTING
````

</details>

### f_set_erase_begin_ptr_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `bucle` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_set_erase_begin_ptr_bucle(std::set<int>& c) {
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
    debug::set<int>; _Category = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffee3a42f30 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::set<int, std::less<int>, std::allocator<int> >' @ 0x7ffee3a43020
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
e/c++/13/bits/stl_tree.h:613:23
    #5 0x559e8ae26ad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x559e8ae263e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x559e8ae24eb9 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_unique_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x559e8ae247c9 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_unique<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x559e8ade0923 in std::set<int, std::less<int>, std::allocator<int>>::set(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_set.h:249:14
    #10 0x559e8ad76323 in make_set(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:55:57
    #11 0x559e8adb0900 in main /work/test/runtime_runner.cpp:2352:23
    #12 0x73cc0193d1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x73cc0193d28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x559e8abfe4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3139:10 in f_set_erase_begin_ptr_bucle(std::set<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x700c00bdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x700c00bdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x700c00bdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x700c00bdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x700c00bdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x700c00be0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x700c00be0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x700c00be0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x700c00be0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x700c00be0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x700c00be0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1243==ABORTING
````

</details>

### f_set_erase_begin_ptr_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_set_erase_begin_ptr_llamada(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_set_erase_begin(c);
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
/c++/13/bits/stl_tree.h:613:23
    #5 0x5691af0d9ad9 in std::_Rb_tree_node<int>* std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node::operator()<int const&>(int const&) const /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:531:18
    #6 0x5691af0d93e1 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x5691af0d7eb9 in std::_Rb_tree_iterator<int> std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_unique_<int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node>(std::_Rb_tree_const_iterator<int>, int const&, std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x5691af0d77c9 in std::enable_if<__same_value_type<int const*>::value, void>::type std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int>>::_M_insert_range_unique<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x5691af093923 in std::set<int, std::less<int>, std::allocator<int>>::set(std::initializer_list<int>, std::less<int> const&, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_set.h:249:14
    #10 0x5691af029323 in make_set(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:55:57
    #11 0x5691af063a7f in main /work/test/runtime_runner.cpp:2357:23
    #12 0x7f03a7e321c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x7f03a7e3228a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x5691aeeb14b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3147:8 in f_set_erase_begin_ptr_llamada(std::set<int, std::less<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7b43a71dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b43a71dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b43a71dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b43a71dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b43a71dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b43a71e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7b43a71e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7b43a71e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b43a71e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b43a71e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b43a71e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1246==ABORTING
````

</details>
