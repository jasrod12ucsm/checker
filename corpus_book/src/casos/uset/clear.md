# `std::unordered_set::clear`

Mutación: `c.clear();`

- Iterador retenido: 🔴 `UB`
- Referencia/puntero retenido: 🔴 `UB`
- Casos `UB` detectados estáticamente: 5/12

**En palabras:** después de `c.clear();` sobre un `std::unordered_set`, un iterador guardado queda **inválido**: usarlo después es un bug (UB); una referencia o puntero guardado queda **inválido**: usarlo después es un bug (UB).

Mapa de los 12 casos. Cada celda muestra la respuesta correcta (etiqueta) y, debajo, lo que hizo el analizador estático de Clang. Clic para ir al caso. Ver [Cómo leer este libro](../../guia.md).

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🔴 `UB`<br>❌ no detectado](#f_uset_clear_it_recto) | [🔴 `UB`<br>✅ detectado](#f_uset_clear_it_guarda) | [🔴 `UB`<br>✅ detectado](#f_uset_clear_it_bucle) | [🔴 `UB`<br>✅ detectado](#f_uset_clear_it_llamada) |
| **referencia** | [🔴 `UB`<br>❌ no detectado](#f_uset_clear_ref_recto) | [🔴 `UB`<br>❌ no detectado](#f_uset_clear_ref_guarda) | [🔴 `UB`<br>✅ detectado](#f_uset_clear_ref_bucle) | [🔴 `UB`<br>❌ no detectado](#f_uset_clear_ref_llamada) |
| **puntero** | [🔴 `UB`<br>❌ no detectado](#f_uset_clear_ptr_recto) | [🔴 `UB`<br>❌ no detectado](#f_uset_clear_ptr_guarda) | [🔴 `UB`<br>✅ detectado](#f_uset_clear_ptr_bucle) | [🔴 `UB`<br>❌ no detectado](#f_uset_clear_ptr_llamada) |

## Handle: iterador

### f_uset_clear_it_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_uset_clear_it_recto(std::unordered_set<int>& c) {
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
    const [with _Iterator = std::detail::_Node_iterator<int, true, false>; 
    _Sequence = std::debug::unordered_set<int>; _Category = 
    std::forward_iterator_tag; reference = const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffe0f9fc720 {
      type = std::detail::_Node_iterator<int, true, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int> >' @ 0x7ffe0f9fc7a0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
tor<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert_unique_aux<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:904:11
    #8 0x62e7e1a3d64a in std::pair<std::__detail::_Node_iterator<int, true, false>, bool> std::_Hashtable<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&, std::integral_constant<bool, true>) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:916:11
    #9 0x62e7e1a3d2ef in std::__detail::_Insert<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>, true>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable_policy.h:1075:13
    #10 0x62e7e1a08d74 in std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_set.h:433:21
    #11 0x62e7e19a4467 in make_uset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:65:56
    #12 0x62e7e19ed63d in main /work/test/runtime_runner.cpp:3232:33
    #13 0x762c12b481c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x762c12b4828a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #15 0x62e7e182b4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4318:8 in f_uset_clear_it_recto(std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x724c11ddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x724c11ddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x724c11ddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x724c11ddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x724c11ddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x724c11de0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x724c11de0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x724c11de0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x724c11de0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x724c11de0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x724c11de0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1705==ABORTING
````

</details>

### f_uset_clear_it_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `guarda` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_uset_clear_it_guarda(std::unordered_set<int>& c) {
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
    const [with _Iterator = std::detail::_Node_iterator<int, true, false>; 
    _Sequence = std::debug::unordered_set<int>; _Category = 
    std::forward_iterator_tag; reference = const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffcfd6a79d0 {
      type = std::detail::_Node_iterator<int, true, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int> >' @ 0x7ffcfd6a7a90
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
or<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert_unique_aux<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:904:11
    #8 0x5816e8a9364a in std::pair<std::__detail::_Node_iterator<int, true, false>, bool> std::_Hashtable<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&, std::integral_constant<bool, true>) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:916:11
    #9 0x5816e8a932ef in std::__detail::_Insert<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>, true>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable_policy.h:1075:13
    #10 0x5816e8a5ed74 in std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_set.h:433:21
    #11 0x5816e89fa467 in make_uset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:65:56
    #12 0x5816e8a43787 in main /work/test/runtime_runner.cpp:3237:33
    #13 0x771a361ef1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x771a361ef28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #15 0x5816e88814b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4324:8 in f_uset_clear_it_guarda(std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x733a355dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x733a355dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x733a355dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x733a355dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x733a355dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x733a355e0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x733a355e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x733a355e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x733a355e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x733a355e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x733a355e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1708==ABORTING
````

</details>

### f_uset_clear_it_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_uset_clear_it_bucle(std::unordered_set<int>& c) {
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
    const [with _Iterator = std::detail::_Node_iterator<int, true, false>; 
    _Sequence = std::debug::unordered_set<int>; _Category = 
    std::forward_iterator_tag; reference = const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffe58179350 {
      type = std::detail::_Node_iterator<int, true, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int> >' @ 0x7ffe58179410
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
or<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert_unique_aux<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:904:11
    #8 0x58fa15ab564a in std::pair<std::__detail::_Node_iterator<int, true, false>, bool> std::_Hashtable<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&, std::integral_constant<bool, true>) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:916:11
    #9 0x58fa15ab52ef in std::__detail::_Insert<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>, true>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable_policy.h:1075:13
    #10 0x58fa15a80d74 in std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_set.h:433:21
    #11 0x58fa15a1c467 in make_uset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:65:56
    #12 0x58fa15a658d1 in main /work/test/runtime_runner.cpp:3242:33
    #13 0x7d1251eeb1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x7d1251eeb28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #15 0x58fa158a34b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4330:10 in f_uset_clear_it_bucle(std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7932511dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7932511dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7932511dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7932511dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7932511dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7932511e0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x7932511e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7932511e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7932511e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7932511e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7932511e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1711==ABORTING
````

</details>

### f_uset_clear_it_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `llamada` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_uset_clear_it_llamada(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_uset_clear(c);
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
    const [with _Iterator = std::detail::_Node_iterator<int, true, false>; 
    _Sequence = std::debug::unordered_set<int>; _Category = 
    std::forward_iterator_tag; reference = const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffd98c30680 {
      type = std::detail::_Node_iterator<int, true, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int> >' @ 0x7ffd98c30740
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
r<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert_unique_aux<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:904:11
    #8 0x5b19b3bb064a in std::pair<std::__detail::_Node_iterator<int, true, false>, bool> std::_Hashtable<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&, std::integral_constant<bool, true>) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:916:11
    #9 0x5b19b3bb02ef in std::__detail::_Insert<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>, true>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable_policy.h:1075:13
    #10 0x5b19b3b7bd74 in std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_set.h:433:21
    #11 0x5b19b3b17467 in make_uset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:65:56
    #12 0x5b19b3b60a1b in main /work/test/runtime_runner.cpp:3247:33
    #13 0x70676f5601c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x70676f56028a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #15 0x5b19b399e4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4337:8 in f_uset_clear_it_llamada(std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6c876e7dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6c876e7dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6c876e7dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6c876e7dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6c876e7dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6c876e7e0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x6c876e7e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6c876e7e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6c876e7e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6c876e7e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6c876e7e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1714==ABORTING
````

</details>

## Handle: referencia

### f_uset_clear_ref_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_uset_clear_ref_recto(std::unordered_set<int>& c) {
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
or<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert_unique_aux<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:904:11
    #8 0x575531b3764a in std::pair<std::__detail::_Node_iterator<int, true, false>, bool> std::_Hashtable<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&, std::integral_constant<bool, true>) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:916:11
    #9 0x575531b372ef in std::__detail::_Insert<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>, true>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable_policy.h:1075:13
    #10 0x575531b02d74 in std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_set.h:433:21
    #11 0x575531a9e467 in make_uset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:65:56
    #12 0x575531ae7b65 in main /work/test/runtime_runner.cpp:3252:33
    #13 0x7f179b2b01c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x7f179b2b028a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #15 0x5755319254b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4343:8 in f_uset_clear_ref_recto(std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7b379a5dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b379a5dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b379a5dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b379a5dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b379a5dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b379a5e0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x7b379a5e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b379a5e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b379a5e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b379a5e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b379a5e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1717==ABORTING
````

</details>

### f_uset_clear_ref_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_uset_clear_ref_guarda(std::unordered_set<int>& c) {
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
r<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert_unique_aux<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:904:11
    #8 0x5a8e3bf0364a in std::pair<std::__detail::_Node_iterator<int, true, false>, bool> std::_Hashtable<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&, std::integral_constant<bool, true>) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:916:11
    #9 0x5a8e3bf032ef in std::__detail::_Insert<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>, true>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable_policy.h:1075:13
    #10 0x5a8e3beced74 in std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_set.h:433:21
    #11 0x5a8e3be6a467 in make_uset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:65:56
    #12 0x5a8e3beb3caf in main /work/test/runtime_runner.cpp:3257:33
    #13 0x71ad0a6141c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x71ad0a61428a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #15 0x5a8e3bcf14b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4350:8 in f_uset_clear_ref_guarda(std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6dcd099dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6dcd099dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6dcd099dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6dcd099dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6dcd099dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6dcd099e0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x6dcd099e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6dcd099e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6dcd099e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6dcd099e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6dcd099e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1720==ABORTING
````

</details>

### f_uset_clear_ref_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `bucle` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_uset_clear_ref_bucle(std::unordered_set<int>& c) {
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
    [with _Iterator = std::detail::_Node_iterator<int, true, false>; 
    _Sequence = std::debug::unordered_set<int>; _Category = 
    std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffd17febb90 {
      type = std::detail::_Node_iterator<int, true, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int> >' @ 0x7ffd17febc50
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
r<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert_unique_aux<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:904:11
    #8 0x6090cc57364a in std::pair<std::__detail::_Node_iterator<int, true, false>, bool> std::_Hashtable<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&, std::integral_constant<bool, true>) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:916:11
    #9 0x6090cc5732ef in std::__detail::_Insert<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>, true>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable_policy.h:1075:13
    #10 0x6090cc53ed74 in std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_set.h:433:21
    #11 0x6090cc4da467 in make_uset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:65:56
    #12 0x6090cc523df9 in main /work/test/runtime_runner.cpp:3262:33
    #13 0x71abe4ea81c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x71abe4ea828a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #15 0x6090cc3614b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4357:10 in f_uset_clear_ref_bucle(std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6dcbe41dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6dcbe41dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6dcbe41dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6dcbe41dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6dcbe41dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6dcbe41e0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x6dcbe41e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6dcbe41e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6dcbe41e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6dcbe41e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6dcbe41e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1723==ABORTING
````

</details>

### f_uset_clear_ref_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_uset_clear_ref_llamada(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_uset_clear(c);
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
<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert_unique_aux<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:904:11
    #8 0x6388d7a7b64a in std::pair<std::__detail::_Node_iterator<int, true, false>, bool> std::_Hashtable<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&, std::integral_constant<bool, true>) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:916:11
    #9 0x6388d7a7b2ef in std::__detail::_Insert<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>, true>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable_policy.h:1075:13
    #10 0x6388d7a46d74 in std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_set.h:433:21
    #11 0x6388d79e2467 in make_uset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:65:56
    #12 0x6388d7a2bf43 in main /work/test/runtime_runner.cpp:3267:33
    #13 0x7d054a72f1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x7d054a72f28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #15 0x6388d78694b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4365:8 in f_uset_clear_ref_llamada(std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7925499dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7925499dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7925499dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7925499dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7925499dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7925499e0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x7925499e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7925499e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7925499e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7925499e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7925499e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1726==ABORTING
````

</details>

## Handle: puntero

### f_uset_clear_ptr_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_uset_clear_ptr_recto(std::unordered_set<int>& c) {
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
or<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert_unique_aux<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:904:11
    #8 0x582b9f84f64a in std::pair<std::__detail::_Node_iterator<int, true, false>, bool> std::_Hashtable<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&, std::integral_constant<bool, true>) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:916:11
    #9 0x582b9f84f2ef in std::__detail::_Insert<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>, true>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable_policy.h:1075:13
    #10 0x582b9f81ad74 in std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_set.h:433:21
    #11 0x582b9f7b6467 in make_uset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:65:56
    #12 0x582b9f80008d in main /work/test/runtime_runner.cpp:3272:33
    #13 0x715ddf85a1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x715ddf85a28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #15 0x582b9f63d4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4371:8 in f_uset_clear_ptr_recto(std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6d7ddebdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d7ddebdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d7ddebdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d7ddebdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d7ddebdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6d7ddebe0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x6d7ddebe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d7ddebe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d7ddebe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d7ddebe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d7ddebe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1729==ABORTING
````

</details>

### f_uset_clear_ptr_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_uset_clear_ptr_guarda(std::unordered_set<int>& c) {
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
r<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert_unique_aux<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:904:11
    #8 0x61e3da3f664a in std::pair<std::__detail::_Node_iterator<int, true, false>, bool> std::_Hashtable<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&, std::integral_constant<bool, true>) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:916:11
    #9 0x61e3da3f62ef in std::__detail::_Insert<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>, true>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable_policy.h:1075:13
    #10 0x61e3da3c1d74 in std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_set.h:433:21
    #11 0x61e3da35d467 in make_uset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:65:56
    #12 0x61e3da3a71d7 in main /work/test/runtime_runner.cpp:3277:33
    #13 0x73dfc688d1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x73dfc688d28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #15 0x61e3da1e44b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4378:8 in f_uset_clear_ptr_guarda(std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6fffc5bdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6fffc5bdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6fffc5bdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6fffc5bdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6fffc5bdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6fffc5be0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x6fffc5be0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6fffc5be0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6fffc5be0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6fffc5be0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6fffc5be0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1732==ABORTING
````

</details>

### f_uset_clear_ptr_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `bucle` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_uset_clear_ptr_bucle(std::unordered_set<int>& c) {
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
    [with _Iterator = std::detail::_Node_iterator<int, true, false>; 
    _Sequence = std::debug::unordered_set<int>; _Category = 
    std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffd9e4463b0 {
      type = std::detail::_Node_iterator<int, true, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int> >' @ 0x7ffd9e446470
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
r<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert_unique_aux<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:904:11
    #8 0x59e554b7c64a in std::pair<std::__detail::_Node_iterator<int, true, false>, bool> std::_Hashtable<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&, std::integral_constant<bool, true>) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:916:11
    #9 0x59e554b7c2ef in std::__detail::_Insert<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>, true>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable_policy.h:1075:13
    #10 0x59e554b47d74 in std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_set.h:433:21
    #11 0x59e554ae3467 in make_uset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:65:56
    #12 0x59e554b2d321 in main /work/test/runtime_runner.cpp:3282:33
    #13 0x7731d9cde1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x7731d9cde28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #15 0x59e55496a4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4385:10 in f_uset_clear_ptr_bucle(std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7351d8fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7351d8fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7351d8fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7351d8fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7351d8fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7351d8fe0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x7351d8fe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7351d8fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7351d8fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7351d8fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7351d8fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1735==ABORTING
````

</details>

### f_uset_clear_ptr_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_uset_clear_ptr_llamada(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_uset_clear(c);
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
<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert_unique_aux<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:904:11
    #8 0x645eda16a64a in std::pair<std::__detail::_Node_iterator<int, true, false>, bool> std::_Hashtable<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&, std::integral_constant<bool, true>) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:916:11
    #9 0x645eda16a2ef in std::__detail::_Insert<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>, true>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable_policy.h:1075:13
    #10 0x645eda135d74 in std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_set.h:433:21
    #11 0x645eda0d1467 in make_uset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:65:56
    #12 0x645eda11b46b in main /work/test/runtime_runner.cpp:3287:33
    #13 0x7e216448e1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x7e216448e28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #15 0x645ed9f584b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4393:8 in f_uset_clear_ptr_llamada(std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7a41637dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a41637dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a41637dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a41637dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a41637dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7a41637e0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x7a41637e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a41637e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a41637e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a41637e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a41637e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1738==ABORTING
````

</details>
