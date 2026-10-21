# `std::unordered_map::erase_begin`

Mutación: `c.erase(c.begin());`

- Iterador retenido: 🔴 `UB`
- Referencia/puntero retenido: 🔴 `UB`
- Casos `UB` detectados estáticamente: 0/12

**En palabras:** después de `c.erase(c.begin());` sobre un `std::unordered_map`, un iterador guardado queda **inválido**: usarlo después es un bug (UB); una referencia o puntero guardado queda **inválido**: usarlo después es un bug (UB).

Mapa de los 12 casos. Cada celda muestra la respuesta correcta (etiqueta) y, debajo, lo que hizo el analizador estático de Clang. Clic para ir al caso. Ver [Cómo leer este libro](../../guia.md).

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🔴 `UB`<br>❌ no detectado](#f_umap_erase_begin_it_recto) | [🔴 `UB`<br>❌ no detectado](#f_umap_erase_begin_it_guarda) | [🔴 `UB`<br>❌ no detectado](#f_umap_erase_begin_it_bucle) | [🔴 `UB`<br>❌ no detectado](#f_umap_erase_begin_it_llamada) |
| **referencia** | [🔴 `UB`<br>❌ no detectado](#f_umap_erase_begin_ref_recto) | [🔴 `UB`<br>❌ no detectado](#f_umap_erase_begin_ref_guarda) | [🔴 `UB`<br>❌ no detectado](#f_umap_erase_begin_ref_bucle) | [🔴 `UB`<br>❌ no detectado](#f_umap_erase_begin_ref_llamada) |
| **puntero** | [🔴 `UB`<br>❌ no detectado](#f_umap_erase_begin_ptr_recto) | [🔴 `UB`<br>❌ no detectado](#f_umap_erase_begin_ptr_guarda) | [🔴 `UB`<br>❌ no detectado](#f_umap_erase_begin_ptr_bucle) | [🔴 `UB`<br>❌ no detectado](#f_umap_erase_begin_ptr_llamada) |

## Handle: iterador

### f_umap_erase_begin_it_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_umap_erase_begin_it_recto(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  c.erase(c.begin());
  sink(it->second);
}
```

> **Causa del falso negativo:** 2. Sin comparacion previa contra end(), el modelado no se activa

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | 🛑 attempt to dereference a singular iterator | 🛑 heap-use-after-free |

<details>
<summary>stderr libstdc++ Debug · <code>natural</code></summary>

````text
/usr/include/c++/13/debug/safe_iterator.h:312:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::pointer 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator->() 
    const [with _Iterator = std::detail::_Node_iterator<std::pair<const int, 
    int>, false, false>; _Sequence = std::debug::unordered_map<int, int>; 
    _Category = std::forward_iterator_tag; pointer = std::pair<const int, 
    int>*]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffd1da5c550 {
      type = std::detail::_Node_iterator<std::pair<int const, int>, false, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffd1da5c640
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_Scoped_node::_Scoped_node<int, int>(std::__detail::_Hashtable_alloc<std::allocator<std::__detail::_Hash_node<std::pair<int const, int>, false>>>*, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:307:19
    #5 0x5952d9900a2f in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_M_emplace<int, int>(std::integral_constant<bool, true>, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:2087:15
    #6 0x5952d9900754 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:961:11
    #7 0x5952d98b5ae0 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_map.h:396:16
    #8 0x5952d984bb21 in make_umap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:73:62
    #9 0x5952d989b465 in main /work/test/runtime_runner.cpp:3592:38
    #10 0x7301c5ce91c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x7301c5ce928a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x5952d96d24b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4810:12 in f_umap_erase_begin_it_recto(std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x6f21c4fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f21c4fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f21c4fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f21c4fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f21c4fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6f21c4fe0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x6f21c4fe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f21c4fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f21c4fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f21c4fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f21c4fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1885==ABORTING
````

</details>

### f_umap_erase_begin_it_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_umap_erase_begin_it_guarda(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.erase(c.begin());
  sink(it->second);
}
```

> **Causa del falso negativo:** 3. Se invalida por identidad del iterador, no por posicion

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | 🛑 attempt to dereference a singular iterator | 🛑 heap-use-after-free |

<details>
<summary>stderr libstdc++ Debug · <code>natural</code></summary>

````text
/usr/include/c++/13/debug/safe_iterator.h:312:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::pointer 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator->() 
    const [with _Iterator = std::detail::_Node_iterator<std::pair<const int, 
    int>, false, false>; _Sequence = std::debug::unordered_map<int, int>; 
    _Category = std::forward_iterator_tag; pointer = std::pair<const int, 
    int>*]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffef970d5a0 {
      type = std::detail::_Node_iterator<std::pair<int const, int>, false, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffef970d690
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
ehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_Scoped_node::_Scoped_node<int, int>(std::__detail::_Hashtable_alloc<std::allocator<std::__detail::_Hash_node<std::pair<int const, int>, false>>>*, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:307:19
    #5 0x582e016faa2f in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_M_emplace<int, int>(std::integral_constant<bool, true>, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:2087:15
    #6 0x582e016fa754 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:961:11
    #7 0x582e016afae0 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_map.h:396:16
    #8 0x582e01645b21 in make_umap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:73:62
    #9 0x582e016955f9 in main /work/test/runtime_runner.cpp:3597:38
    #10 0x7aba56d911c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x7aba56d9128a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x582e014cc4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4816:12 in f_umap_erase_begin_it_guarda(std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x76da55fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x76da55fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x76da55fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x76da55fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x76da55fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x76da55fe0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x76da55fe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x76da55fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x76da55fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x76da55fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x76da55fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1888==ABORTING
````

</details>

### f_umap_erase_begin_it_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_umap_erase_begin_it_bucle(std::unordered_map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.erase(c.begin());
    sink(it->second);
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
/usr/include/c++/13/debug/safe_iterator.h:312:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::pointer 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator->() 
    const [with _Iterator = std::detail::_Node_iterator<std::pair<const int, 
    int>, false, false>; _Sequence = std::debug::unordered_map<int, int>; 
    _Category = std::forward_iterator_tag; pointer = std::pair<const int, 
    int>*]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffd024166c0 {
      type = std::detail::_Node_iterator<std::pair<int const, int>, false, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffd024167b0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_Scoped_node::_Scoped_node<int, int>(std::__detail::_Hashtable_alloc<std::allocator<std::__detail::_Hash_node<std::pair<int const, int>, false>>>*, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:307:19
    #5 0x5b2f02adea2f in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_M_emplace<int, int>(std::integral_constant<bool, true>, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:2087:15
    #6 0x5b2f02ade754 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:961:11
    #7 0x5b2f02a93ae0 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_map.h:396:16
    #8 0x5b2f02a29b21 in make_umap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:73:62
    #9 0x5b2f02a7978d in main /work/test/runtime_runner.cpp:3602:38
    #10 0x7e42cad3f1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x7e42cad3f28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x5b2f028b04b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4822:14 in f_umap_erase_begin_it_bucle(std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x7a62c9fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a62c9fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a62c9fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a62c9fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a62c9fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7a62c9fe0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x7a62c9fe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a62c9fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a62c9fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a62c9fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a62c9fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1891==ABORTING
````

</details>

### f_umap_erase_begin_it_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_umap_erase_begin_it_llamada(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_umap_erase_begin(c);
  sink(it->second);
}
```

> **Causa del falso negativo:** 3. Se invalida por identidad del iterador, no por posicion

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | 🛑 attempt to dereference a singular iterator | 🛑 heap-use-after-free |

<details>
<summary>stderr libstdc++ Debug · <code>natural</code></summary>

````text
/usr/include/c++/13/debug/safe_iterator.h:312:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::pointer 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator->() 
    const [with _Iterator = std::detail::_Node_iterator<std::pair<const int, 
    int>, false, false>; _Sequence = std::debug::unordered_map<int, int>; 
    _Category = std::forward_iterator_tag; pointer = std::pair<const int, 
    int>*]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffed52d4480 {
      type = std::detail::_Node_iterator<std::pair<int const, int>, false, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffed52d4540
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
hash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_Scoped_node::_Scoped_node<int, int>(std::__detail::_Hashtable_alloc<std::allocator<std::__detail::_Hash_node<std::pair<int const, int>, false>>>*, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:307:19
    #5 0x5f202a8f0a2f in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_M_emplace<int, int>(std::integral_constant<bool, true>, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:2087:15
    #6 0x5f202a8f0754 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:961:11
    #7 0x5f202a8a5ae0 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_map.h:396:16
    #8 0x5f202a83bb21 in make_umap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:73:62
    #9 0x5f202a88b921 in main /work/test/runtime_runner.cpp:3607:38
    #10 0x72b3b5f251c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x72b3b5f2528a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x5f202a6c24b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4829:12 in f_umap_erase_begin_it_llamada(std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x6ed3b51dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6ed3b51dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6ed3b51dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6ed3b51dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6ed3b51dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6ed3b51e0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x6ed3b51e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6ed3b51e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6ed3b51e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6ed3b51e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6ed3b51e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1894==ABORTING
````

</details>

## Handle: referencia

### f_umap_erase_begin_ref_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_umap_erase_begin_ref_recto(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.erase(c.begin());
  sink(h.second);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | 🛑 heap-use-after-free |

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
ehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_Scoped_node::_Scoped_node<int, int>(std::__detail::_Hashtable_alloc<std::allocator<std::__detail::_Hash_node<std::pair<int const, int>, false>>>*, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:307:19
    #5 0x57837bc4ba2f in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_M_emplace<int, int>(std::integral_constant<bool, true>, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:2087:15
    #6 0x57837bc4b754 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:961:11
    #7 0x57837bc00ae0 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_map.h:396:16
    #8 0x57837bb96b21 in make_umap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:73:62
    #9 0x57837bbe6ab5 in main /work/test/runtime_runner.cpp:3612:38
    #10 0x7615230a91c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x7615230a928a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x57837ba1d4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4835:10 in f_umap_erase_begin_ref_recto(std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x7235223dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7235223dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7235223dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7235223dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7235223dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7235223e0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x7235223e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7235223e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7235223e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7235223e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7235223e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1897==ABORTING
````

</details>

### f_umap_erase_begin_ref_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_umap_erase_begin_ref_guarda(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.erase(c.begin());
  sink(h.second);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | 🛑 heap-use-after-free |

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
hash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_Scoped_node::_Scoped_node<int, int>(std::__detail::_Hashtable_alloc<std::allocator<std::__detail::_Hash_node<std::pair<int const, int>, false>>>*, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:307:19
    #5 0x58ce47ccea2f in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_M_emplace<int, int>(std::integral_constant<bool, true>, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:2087:15
    #6 0x58ce47cce754 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:961:11
    #7 0x58ce47c83ae0 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_map.h:396:16
    #8 0x58ce47c19b21 in make_umap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:73:62
    #9 0x58ce47c69c49 in main /work/test/runtime_runner.cpp:3617:38
    #10 0x77d0a8b9b1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x77d0a8b9b28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x58ce47aa04b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4842:10 in f_umap_erase_begin_ref_guarda(std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x73f0a7ddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73f0a7ddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73f0a7ddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73f0a7ddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73f0a7ddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x73f0a7de0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x73f0a7de0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x73f0a7de0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x73f0a7de0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x73f0a7de0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x73f0a7de0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1900==ABORTING
````

</details>

### f_umap_erase_begin_ref_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `bucle` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_umap_erase_begin_ref_bucle(std::unordered_map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.erase(c.begin());
    sink(h.second);
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
    [with _Iterator = std::detail::_Node_iterator<std::pair<const int, int>, 
    false, false>; _Sequence = std::debug::unordered_map<int, int>; 
    _Category = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffe8d1ce840 {
      type = std::detail::_Node_iterator<std::pair<int const, int>, false, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffe8d1ce930
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
ehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_Scoped_node::_Scoped_node<int, int>(std::__detail::_Hashtable_alloc<std::allocator<std::__detail::_Hash_node<std::pair<int const, int>, false>>>*, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:307:19
    #5 0x6399beadea2f in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_M_emplace<int, int>(std::integral_constant<bool, true>, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:2087:15
    #6 0x6399beade754 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:961:11
    #7 0x6399bea93ae0 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_map.h:396:16
    #8 0x6399bea29b21 in make_umap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:73:62
    #9 0x6399bea79ddd in main /work/test/runtime_runner.cpp:3622:38
    #10 0x7cf1fb0451c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x7cf1fb04528a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x6399be8b04b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4849:12 in f_umap_erase_begin_ref_bucle(std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x7911fa3dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7911fa3dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7911fa3dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7911fa3dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7911fa3dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7911fa3e0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x7911fa3e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7911fa3e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7911fa3e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7911fa3e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7911fa3e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1903==ABORTING
````

</details>

### f_umap_erase_begin_ref_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_umap_erase_begin_ref_llamada(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_umap_erase_begin(c);
  sink(h.second);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | 🛑 heap-use-after-free |

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
ash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_Scoped_node::_Scoped_node<int, int>(std::__detail::_Hashtable_alloc<std::allocator<std::__detail::_Hash_node<std::pair<int const, int>, false>>>*, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:307:19
    #5 0x64f81f8c4a2f in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_M_emplace<int, int>(std::integral_constant<bool, true>, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:2087:15
    #6 0x64f81f8c4754 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:961:11
    #7 0x64f81f879ae0 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_map.h:396:16
    #8 0x64f81f80fb21 in make_umap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:73:62
    #9 0x64f81f85ff71 in main /work/test/runtime_runner.cpp:3627:38
    #10 0x72f093ff51c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x72f093ff528a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x64f81f6964b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4857:10 in f_umap_erase_begin_ref_llamada(std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x6f10933dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f10933dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f10933dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f10933dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f10933dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6f10933e0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x6f10933e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f10933e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f10933e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f10933e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f10933e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1906==ABORTING
````

</details>

## Handle: puntero

### f_umap_erase_begin_ptr_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_umap_erase_begin_ptr_recto(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.erase(c.begin());
  sink(h->second);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | 🛑 heap-use-after-free |

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
ehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_Scoped_node::_Scoped_node<int, int>(std::__detail::_Hashtable_alloc<std::allocator<std::__detail::_Hash_node<std::pair<int const, int>, false>>>*, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:307:19
    #5 0x57df16563a2f in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_M_emplace<int, int>(std::integral_constant<bool, true>, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:2087:15
    #6 0x57df16563754 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:961:11
    #7 0x57df16518ae0 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_map.h:396:16
    #8 0x57df164aeb21 in make_umap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:73:62
    #9 0x57df164ff105 in main /work/test/runtime_runner.cpp:3632:38
    #10 0x7ded8b0681c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x7ded8b06828a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x57df163354b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4863:11 in f_umap_erase_begin_ptr_recto(std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x7a0d8a3dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a0d8a3dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a0d8a3dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a0d8a3dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a0d8a3dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7a0d8a3e0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x7a0d8a3e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a0d8a3e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a0d8a3e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a0d8a3e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a0d8a3e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1909==ABORTING
````

</details>

### f_umap_erase_begin_ptr_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_umap_erase_begin_ptr_guarda(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.erase(c.begin());
  sink(h->second);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | 🛑 heap-use-after-free |

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
hash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_Scoped_node::_Scoped_node<int, int>(std::__detail::_Hashtable_alloc<std::allocator<std::__detail::_Hash_node<std::pair<int const, int>, false>>>*, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:307:19
    #5 0x629b31581a2f in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_M_emplace<int, int>(std::integral_constant<bool, true>, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:2087:15
    #6 0x629b31581754 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:961:11
    #7 0x629b31536ae0 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_map.h:396:16
    #8 0x629b314ccb21 in make_umap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:73:62
    #9 0x629b3151d299 in main /work/test/runtime_runner.cpp:3637:38
    #10 0x774f8801d1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x774f8801d28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x629b313534b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4870:11 in f_umap_erase_begin_ptr_guarda(std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x736f873dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x736f873dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x736f873dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x736f873dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x736f873dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x736f873e0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x736f873e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x736f873e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x736f873e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x736f873e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x736f873e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1912==ABORTING
````

</details>

### f_umap_erase_begin_ptr_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `bucle` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_umap_erase_begin_ptr_bucle(std::unordered_map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.erase(c.begin());
    sink(h->second);
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
    [with _Iterator = std::detail::_Node_iterator<std::pair<const int, int>, 
    false, false>; _Sequence = std::debug::unordered_map<int, int>; 
    _Category = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffd7d7ad220 {
      type = std::detail::_Node_iterator<std::pair<int const, int>, false, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffd7d7ad310
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
ehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_Scoped_node::_Scoped_node<int, int>(std::__detail::_Hashtable_alloc<std::allocator<std::__detail::_Hash_node<std::pair<int const, int>, false>>>*, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:307:19
    #5 0x62b5aea0ea2f in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_M_emplace<int, int>(std::integral_constant<bool, true>, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:2087:15
    #6 0x62b5aea0e754 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:961:11
    #7 0x62b5ae9c3ae0 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_map.h:396:16
    #8 0x62b5ae959b21 in make_umap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:73:62
    #9 0x62b5ae9aa42d in main /work/test/runtime_runner.cpp:3642:38
    #10 0x7f9b068e31c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x7f9b068e328a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x62b5ae7e04b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4877:13 in f_umap_erase_begin_ptr_bucle(std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x7bbb05bdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bbb05bdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bbb05bdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bbb05bdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bbb05bdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bbb05be0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x7bbb05be0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bbb05be0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bbb05be0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bbb05be0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bbb05be0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1915==ABORTING
````

</details>

### f_umap_erase_begin_ptr_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_umap_erase_begin_ptr_llamada(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_umap_erase_begin(c);
  sink(h->second);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | 🛑 heap-use-after-free |

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
ash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_Scoped_node::_Scoped_node<int, int>(std::__detail::_Hashtable_alloc<std::allocator<std::__detail::_Hash_node<std::pair<int const, int>, false>>>*, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:307:19
    #5 0x5c355a57fa2f in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_M_emplace<int, int>(std::integral_constant<bool, true>, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:2087:15
    #6 0x5c355a57f754 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:961:11
    #7 0x5c355a534ae0 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_map.h:396:16
    #8 0x5c355a4cab21 in make_umap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:73:62
    #9 0x5c355a51b5c1 in main /work/test/runtime_runner.cpp:3647:38
    #10 0x72b401fce1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x72b401fce28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x5c355a3514b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4885:11 in f_umap_erase_begin_ptr_llamada(std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x6ed4013dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6ed4013dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6ed4013dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6ed4013dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6ed4013dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6ed4013e0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x6ed4013e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6ed4013e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6ed4013e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6ed4013e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6ed4013e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1918==ABORTING
````

</details>
