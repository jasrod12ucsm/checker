# `std::unordered_map::clear`

Mutación: `c.clear();`

- Iterador retenido: 🔴 `UB`
- Referencia/puntero retenido: 🔴 `UB`
- Casos `UB` detectados estáticamente: 5/12

**En palabras:** después de `c.clear();` sobre un `std::unordered_map`, un iterador guardado queda **inválido**: usarlo después es un bug (UB); una referencia o puntero guardado queda **inválido**: usarlo después es un bug (UB).

Mapa de los 12 casos. Cada celda muestra la respuesta correcta (etiqueta) y, debajo, lo que hizo el analizador estático de Clang. Clic para ir al caso. Ver [Cómo leer este libro](../../guia.md).

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🔴 `UB`<br>❌ no detectado](#f_umap_clear_it_recto) | [🔴 `UB`<br>✅ detectado](#f_umap_clear_it_guarda) | [🔴 `UB`<br>✅ detectado](#f_umap_clear_it_bucle) | [🔴 `UB`<br>✅ detectado](#f_umap_clear_it_llamada) |
| **referencia** | [🔴 `UB`<br>❌ no detectado](#f_umap_clear_ref_recto) | [🔴 `UB`<br>❌ no detectado](#f_umap_clear_ref_guarda) | [🔴 `UB`<br>✅ detectado](#f_umap_clear_ref_bucle) | [🔴 `UB`<br>❌ no detectado](#f_umap_clear_ref_llamada) |
| **puntero** | [🔴 `UB`<br>❌ no detectado](#f_umap_clear_ptr_recto) | [🔴 `UB`<br>❌ no detectado](#f_umap_clear_ptr_guarda) | [🔴 `UB`<br>✅ detectado](#f_umap_clear_ptr_bucle) | [🔴 `UB`<br>❌ no detectado](#f_umap_clear_ptr_llamada) |

## Handle: iterador

### f_umap_clear_it_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_umap_clear_it_recto(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  c.clear();
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
    iterator "this" @ 0x7ffddc5c0690 {
      type = std::detail::_Node_iterator<std::pair<int const, int>, false, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffddc5c0710
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_Scoped_node::_Scoped_node<int, int>(std::__detail::_Hashtable_alloc<std::allocator<std::__detail::_Hash_node<std::pair<int const, int>, false>>>*, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:307:19
    #5 0x5a254a2aea2f in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_M_emplace<int, int>(std::integral_constant<bool, true>, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:2087:15
    #6 0x5a254a2ae754 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:961:11
    #7 0x5a254a263ae0 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_map.h:396:16
    #8 0x5a254a1f9b21 in make_umap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:73:62
    #9 0x5a254a24a755 in main /work/test/runtime_runner.cpp:3652:38
    #10 0x74dbd54c61c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x74dbd54c628a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x5a254a0804b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4890:12 in f_umap_clear_it_recto(std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x70fbd47dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x70fbd47dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x70fbd47dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x70fbd47dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x70fbd47dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x70fbd47e0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x70fbd47e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x70fbd47e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x70fbd47e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x70fbd47e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x70fbd47e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1921==ABORTING
````

</details>

### f_umap_clear_it_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `guarda` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_umap_clear_it_guarda(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.clear();
  sink(it->second);
}
```

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
    iterator "this" @ 0x7ffc1e4aed30 {
      type = std::detail::_Node_iterator<std::pair<int const, int>, false, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffc1e4aedf0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
rime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_Scoped_node::_Scoped_node<int, int>(std::__detail::_Hashtable_alloc<std::allocator<std::__detail::_Hash_node<std::pair<int const, int>, false>>>*, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:307:19
    #5 0x59142a206a2f in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_M_emplace<int, int>(std::integral_constant<bool, true>, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:2087:15
    #6 0x59142a206754 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:961:11
    #7 0x59142a1bbae0 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_map.h:396:16
    #8 0x59142a151b21 in make_umap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:73:62
    #9 0x59142a1a289f in main /work/test/runtime_runner.cpp:3657:38
    #10 0x7e00fff411c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x7e00fff4128a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x591429fd84b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4896:12 in f_umap_clear_it_guarda(std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x7a20ff1dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a20ff1dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a20ff1dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a20ff1dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a20ff1dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7a20ff1e0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x7a20ff1e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a20ff1e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a20ff1e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a20ff1e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a20ff1e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1924==ABORTING
````

</details>

### f_umap_clear_it_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_umap_clear_it_bucle(std::unordered_map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.clear();
    sink(it->second);
  }
}
```

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
    iterator "this" @ 0x7ffdfd1260d0 {
      type = std::detail::_Node_iterator<std::pair<int const, int>, false, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffdfd126190
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_Scoped_node::_Scoped_node<int, int>(std::__detail::_Hashtable_alloc<std::allocator<std::__detail::_Hash_node<std::pair<int const, int>, false>>>*, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:307:19
    #5 0x56271d501a2f in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_M_emplace<int, int>(std::integral_constant<bool, true>, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:2087:15
    #6 0x56271d501754 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:961:11
    #7 0x56271d4b6ae0 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_map.h:396:16
    #8 0x56271d44cb21 in make_umap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:73:62
    #9 0x56271d49d9e9 in main /work/test/runtime_runner.cpp:3662:38
    #10 0x7fe6a352e1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x7fe6a352e28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x56271d2d34b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4902:14 in f_umap_clear_it_bucle(std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x7c06a27dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c06a27dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c06a27dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c06a27dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c06a27dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c06a27e0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x7c06a27e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c06a27e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c06a27e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c06a27e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c06a27e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1927==ABORTING
````

</details>

### f_umap_clear_it_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `llamada` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_umap_clear_it_llamada(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_umap_clear(c);
  sink(it->second);
}
```

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
    iterator "this" @ 0x7ffecf60cb00 {
      type = std::detail::_Node_iterator<std::pair<int const, int>, false, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffecf60cbc0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
ime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_Scoped_node::_Scoped_node<int, int>(std::__detail::_Hashtable_alloc<std::allocator<std::__detail::_Hash_node<std::pair<int const, int>, false>>>*, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:307:19
    #5 0x5ecc96551a2f in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_M_emplace<int, int>(std::integral_constant<bool, true>, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:2087:15
    #6 0x5ecc96551754 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:961:11
    #7 0x5ecc96506ae0 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_map.h:396:16
    #8 0x5ecc9649cb21 in make_umap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:73:62
    #9 0x5ecc964edb33 in main /work/test/runtime_runner.cpp:3667:38
    #10 0x7bf6f374e1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x7bf6f374e28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x5ecc963234b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4909:12 in f_umap_clear_it_llamada(std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x7816f29dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7816f29dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7816f29dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7816f29dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7816f29dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7816f29e0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x7816f29e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7816f29e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7816f29e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7816f29e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7816f29e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1930==ABORTING
````

</details>

## Handle: referencia

### f_umap_clear_ref_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_umap_clear_ref_recto(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.clear();
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
rime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_Scoped_node::_Scoped_node<int, int>(std::__detail::_Hashtable_alloc<std::allocator<std::__detail::_Hash_node<std::pair<int const, int>, false>>>*, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:307:19
    #5 0x6073ba436a2f in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_M_emplace<int, int>(std::integral_constant<bool, true>, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:2087:15
    #6 0x6073ba436754 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:961:11
    #7 0x6073ba3ebae0 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_map.h:396:16
    #8 0x6073ba381b21 in make_umap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:73:62
    #9 0x6073ba3d2c77 in main /work/test/runtime_runner.cpp:3672:38
    #10 0x77172fd831c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x77172fd8328a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x6073ba2084b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4915:10 in f_umap_clear_ref_recto(std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x73372efdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73372efdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73372efdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73372efdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73372efdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x73372efe0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x73372efe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x73372efe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x73372efe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x73372efe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x73372efe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1933==ABORTING
````

</details>

### f_umap_clear_ref_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_umap_clear_ref_guarda(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.clear();
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
ime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_Scoped_node::_Scoped_node<int, int>(std::__detail::_Hashtable_alloc<std::allocator<std::__detail::_Hash_node<std::pair<int const, int>, false>>>*, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:307:19
    #5 0x58721f47ea2f in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_M_emplace<int, int>(std::integral_constant<bool, true>, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:2087:15
    #6 0x58721f47e754 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:961:11
    #7 0x58721f433ae0 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_map.h:396:16
    #8 0x58721f3c9b21 in make_umap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:73:62
    #9 0x58721f41adbb in main /work/test/runtime_runner.cpp:3677:38
    #10 0x712d4af2b1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x712d4af2b28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x58721f2504b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4922:10 in f_umap_clear_ref_guarda(std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x6d4d4a1dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d4d4a1dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d4d4a1dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d4d4a1dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d4d4a1dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6d4d4a1e0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x6d4d4a1e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d4d4a1e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d4d4a1e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d4d4a1e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d4d4a1e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1936==ABORTING
````

</details>

### f_umap_clear_ref_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `bucle` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_umap_clear_ref_bucle(std::unordered_map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.clear();
    sink(h.second);
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
    [with _Iterator = std::detail::_Node_iterator<std::pair<const int, int>, 
    false, false>; _Sequence = std::debug::unordered_map<int, int>; 
    _Category = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffea3583e30 {
      type = std::detail::_Node_iterator<std::pair<int const, int>, false, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffea3583ef0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
rime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_Scoped_node::_Scoped_node<int, int>(std::__detail::_Hashtable_alloc<std::allocator<std::__detail::_Hash_node<std::pair<int const, int>, false>>>*, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:307:19
    #5 0x580335468a2f in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_M_emplace<int, int>(std::integral_constant<bool, true>, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:2087:15
    #6 0x580335468754 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:961:11
    #7 0x58033541dae0 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_map.h:396:16
    #8 0x5803353b3b21 in make_umap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:73:62
    #9 0x580335404eff in main /work/test/runtime_runner.cpp:3682:38
    #10 0x7efe893141c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x7efe8931428a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x58033523a4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4929:12 in f_umap_clear_ref_bucle(std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x7b1e885dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b1e885dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b1e885dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b1e885dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b1e885dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b1e885e0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x7b1e885e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b1e885e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b1e885e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b1e885e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b1e885e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1939==ABORTING
````

</details>

### f_umap_clear_ref_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_umap_clear_ref_llamada(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_umap_clear(c);
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
me_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_Scoped_node::_Scoped_node<int, int>(std::__detail::_Hashtable_alloc<std::allocator<std::__detail::_Hash_node<std::pair<int const, int>, false>>>*, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:307:19
    #5 0x5f53ae628a2f in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_M_emplace<int, int>(std::integral_constant<bool, true>, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:2087:15
    #6 0x5f53ae628754 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:961:11
    #7 0x5f53ae5ddae0 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_map.h:396:16
    #8 0x5f53ae573b21 in make_umap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:73:62
    #9 0x5f53ae5c5043 in main /work/test/runtime_runner.cpp:3687:38
    #10 0x79cf62d261c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x79cf62d2628a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x5f53ae3fa4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4937:10 in f_umap_clear_ref_llamada(std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x75ef61fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75ef61fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75ef61fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75ef61fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75ef61fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x75ef61fe0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x75ef61fe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x75ef61fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x75ef61fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x75ef61fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x75ef61fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1942==ABORTING
````

</details>

## Handle: puntero

### f_umap_clear_ptr_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_umap_clear_ptr_recto(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.clear();
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
rime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_Scoped_node::_Scoped_node<int, int>(std::__detail::_Hashtable_alloc<std::allocator<std::__detail::_Hash_node<std::pair<int const, int>, false>>>*, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:307:19
    #5 0x5853e62dca2f in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_M_emplace<int, int>(std::integral_constant<bool, true>, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:2087:15
    #6 0x5853e62dc754 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:961:11
    #7 0x5853e6291ae0 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_map.h:396:16
    #8 0x5853e6227b21 in make_umap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:73:62
    #9 0x5853e6279187 in main /work/test/runtime_runner.cpp:3692:38
    #10 0x71e89535e1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x71e89535e28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x5853e60ae4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4943:11 in f_umap_clear_ptr_recto(std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x6e08945dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e08945dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e08945dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e08945dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e08945dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6e08945e0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x6e08945e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e08945e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e08945e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e08945e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e08945e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1945==ABORTING
````

</details>

### f_umap_clear_ptr_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_umap_clear_ptr_guarda(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.clear();
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
ime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_Scoped_node::_Scoped_node<int, int>(std::__detail::_Hashtable_alloc<std::allocator<std::__detail::_Hash_node<std::pair<int const, int>, false>>>*, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:307:19
    #5 0x5d864e68ea2f in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_M_emplace<int, int>(std::integral_constant<bool, true>, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:2087:15
    #6 0x5d864e68e754 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:961:11
    #7 0x5d864e643ae0 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_map.h:396:16
    #8 0x5d864e5d9b21 in make_umap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:73:62
    #9 0x5d864e62b2cb in main /work/test/runtime_runner.cpp:3697:38
    #10 0x721aaaaa11c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x721aaaaa128a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x5d864e4604b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4950:11 in f_umap_clear_ptr_guarda(std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x6e3aa9ddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e3aa9ddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e3aa9ddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e3aa9ddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e3aa9ddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6e3aa9de0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x6e3aa9de0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e3aa9de0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e3aa9de0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e3aa9de0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e3aa9de0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1948==ABORTING
````

</details>

### f_umap_clear_ptr_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `bucle` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_umap_clear_ptr_bucle(std::unordered_map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.clear();
    sink(h->second);
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
    [with _Iterator = std::detail::_Node_iterator<std::pair<const int, int>, 
    false, false>; _Sequence = std::debug::unordered_map<int, int>; 
    _Category = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffe8d365620 {
      type = std::detail::_Node_iterator<std::pair<int const, int>, false, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffe8d3656e0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
rime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_Scoped_node::_Scoped_node<int, int>(std::__detail::_Hashtable_alloc<std::allocator<std::__detail::_Hash_node<std::pair<int const, int>, false>>>*, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:307:19
    #5 0x6267832dba2f in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_M_emplace<int, int>(std::integral_constant<bool, true>, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:2087:15
    #6 0x6267832db754 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:961:11
    #7 0x626783290ae0 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_map.h:396:16
    #8 0x626783226b21 in make_umap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:73:62
    #9 0x62678327840f in main /work/test/runtime_runner.cpp:3702:38
    #10 0x703ecae301c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x703ecae3028a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x6267830ad4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4957:13 in f_umap_clear_ptr_bucle(std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x6c5eca1dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6c5eca1dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6c5eca1dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6c5eca1dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6c5eca1dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6c5eca1e0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x6c5eca1e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6c5eca1e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6c5eca1e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6c5eca1e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6c5eca1e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1951==ABORTING
````

</details>

### f_umap_clear_ptr_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_umap_clear_ptr_llamada(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_umap_clear(c);
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
me_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_Scoped_node::_Scoped_node<int, int>(std::__detail::_Hashtable_alloc<std::allocator<std::__detail::_Hash_node<std::pair<int const, int>, false>>>*, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:307:19
    #5 0x5ebcca733a2f in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::_M_emplace<int, int>(std::integral_constant<bool, true>, int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:2087:15
    #6 0x5ebcca733754 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int>>, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:961:11
    #7 0x5ebcca6e8ae0 in std::pair<std::__detail::_Node_iterator<std::pair<int const, int>, false, false>, bool> std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>::emplace<int, int>(int&&, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_map.h:396:16
    #8 0x5ebcca67eb21 in make_umap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:73:62
    #9 0x5ebcca6d0553 in main /work/test/runtime_runner.cpp:3707:38
    #10 0x79d1095c81c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x79d1095c828a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #12 0x5ebcca5054b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4965:11 in f_umap_clear_ptr_llamada(std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x75f1087dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75f1087dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75f1087dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75f1087dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75f1087dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x75f1087e0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x75f1087e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x75f1087e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x75f1087e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x75f1087e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x75f1087e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1954==ABORTING
````

</details>
