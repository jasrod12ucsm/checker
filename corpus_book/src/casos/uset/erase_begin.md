# `std::unordered_set::erase_begin`

Mutación: `c.erase(c.begin());`

- Iterador retenido: 🔴 `UB`
- Referencia/puntero retenido: 🔴 `UB`
- Casos `UB` detectados estáticamente: 0/12

**En palabras:** después de `c.erase(c.begin());` sobre un `std::unordered_set`, un iterador guardado queda **inválido**: usarlo después es un bug (UB); una referencia o puntero guardado queda **inválido**: usarlo después es un bug (UB).

Mapa de los 12 casos. Cada celda muestra la respuesta correcta (etiqueta) y, debajo, lo que hizo el analizador estático de Clang. Clic para ir al caso. Ver [Cómo leer este libro](../../guia.md).

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🔴 `UB`<br>❌ no detectado](#f_uset_erase_begin_it_recto) | [🔴 `UB`<br>❌ no detectado](#f_uset_erase_begin_it_guarda) | [🔴 `UB`<br>❌ no detectado](#f_uset_erase_begin_it_bucle) | [🔴 `UB`<br>❌ no detectado](#f_uset_erase_begin_it_llamada) |
| **referencia** | [🔴 `UB`<br>❌ no detectado](#f_uset_erase_begin_ref_recto) | [🔴 `UB`<br>❌ no detectado](#f_uset_erase_begin_ref_guarda) | [🔴 `UB`<br>❌ no detectado](#f_uset_erase_begin_ref_bucle) | [🔴 `UB`<br>❌ no detectado](#f_uset_erase_begin_ref_llamada) |
| **puntero** | [🔴 `UB`<br>❌ no detectado](#f_uset_erase_begin_ptr_recto) | [🔴 `UB`<br>❌ no detectado](#f_uset_erase_begin_ptr_guarda) | [🔴 `UB`<br>❌ no detectado](#f_uset_erase_begin_ptr_bucle) | [🔴 `UB`<br>❌ no detectado](#f_uset_erase_begin_ptr_llamada) |

## Handle: iterador

### f_uset_erase_begin_it_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_uset_erase_begin_it_recto(std::unordered_set<int>& c) {
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
    const [with _Iterator = std::detail::_Node_iterator<int, true, false>; 
    _Sequence = std::debug::unordered_set<int>; _Category = 
    std::forward_iterator_tag; reference = const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffcef872e00 {
      type = std::detail::_Node_iterator<int, true, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int> >' @ 0x7ffcef872ef0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
t>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert_unique_aux<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:904:11
    #8 0x56352178f64a in std::pair<std::__detail::_Node_iterator<int, true, false>, bool> std::_Hashtable<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&, std::integral_constant<bool, true>) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:916:11
    #9 0x56352178f2ef in std::__detail::_Insert<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>, true>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable_policy.h:1075:13
    #10 0x56352175ad74 in std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_set.h:433:21
    #11 0x5635216f6467 in make_uset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:65:56
    #12 0x56352173e34d in main /work/test/runtime_runner.cpp:3172:33
    #13 0x7ef27a9d71c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x7ef27a9d728a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #15 0x56352157d4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4238:8 in f_uset_erase_begin_it_recto(std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7b1279ddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b1279ddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b1279ddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b1279ddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b1279ddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b1279de0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x7b1279de0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b1279de0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b1279de0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b1279de0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b1279de0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1669==ABORTING
````

</details>

### f_uset_erase_begin_it_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_uset_erase_begin_it_guarda(std::unordered_set<int>& c) {
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
    const [with _Iterator = std::detail::_Node_iterator<int, true, false>; 
    _Sequence = std::debug::unordered_set<int>; _Category = 
    std::forward_iterator_tag; reference = const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fff30313210 {
      type = std::detail::_Node_iterator<int, true, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int> >' @ 0x7fff30313300
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert_unique_aux<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:904:11
    #8 0x563c6a3fa64a in std::pair<std::__detail::_Node_iterator<int, true, false>, bool> std::_Hashtable<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&, std::integral_constant<bool, true>) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:916:11
    #9 0x563c6a3fa2ef in std::__detail::_Insert<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>, true>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable_policy.h:1075:13
    #10 0x563c6a3c5d74 in std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_set.h:433:21
    #11 0x563c6a361467 in make_uset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:65:56
    #12 0x563c6a3a94e1 in main /work/test/runtime_runner.cpp:3177:33
    #13 0x762d439201c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x762d4392028a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #15 0x563c6a1e84b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4244:8 in f_uset_erase_begin_it_guarda(std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x724d42bdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x724d42bdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x724d42bdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x724d42bdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x724d42bdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x724d42be0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x724d42be0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x724d42be0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x724d42be0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x724d42be0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x724d42be0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1672==ABORTING
````

</details>

### f_uset_erase_begin_it_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_uset_erase_begin_it_bucle(std::unordered_set<int>& c) {
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
    const [with _Iterator = std::detail::_Node_iterator<int, true, false>; 
    _Sequence = std::debug::unordered_set<int>; _Category = 
    std::forward_iterator_tag; reference = const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fffe24dfa50 {
      type = std::detail::_Node_iterator<int, true, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int> >' @ 0x7fffe24dfb40
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert_unique_aux<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:904:11
    #8 0x64cc2841564a in std::pair<std::__detail::_Node_iterator<int, true, false>, bool> std::_Hashtable<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&, std::integral_constant<bool, true>) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:916:11
    #9 0x64cc284152ef in std::__detail::_Insert<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>, true>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable_policy.h:1075:13
    #10 0x64cc283e0d74 in std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_set.h:433:21
    #11 0x64cc2837c467 in make_uset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:65:56
    #12 0x64cc283c4675 in main /work/test/runtime_runner.cpp:3182:33
    #13 0x7619497181c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x76194971828a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #15 0x64cc282034b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4250:10 in f_uset_erase_begin_it_bucle(std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7239489dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7239489dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7239489dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7239489dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7239489dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7239489e0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x7239489e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7239489e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7239489e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7239489e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7239489e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1675==ABORTING
````

</details>

### f_uset_erase_begin_it_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_uset_erase_begin_it_llamada(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_uset_erase_begin(c);
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
    const [with _Iterator = std::detail::_Node_iterator<int, true, false>; 
    _Sequence = std::debug::unordered_set<int>; _Category = 
    std::forward_iterator_tag; reference = const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fffc15ae5f0 {
      type = std::detail::_Node_iterator<int, true, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int> >' @ 0x7fffc15ae6b0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert_unique_aux<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:904:11
    #8 0x643fb72f964a in std::pair<std::__detail::_Node_iterator<int, true, false>, bool> std::_Hashtable<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&, std::integral_constant<bool, true>) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:916:11
    #9 0x643fb72f92ef in std::__detail::_Insert<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>, true>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable_policy.h:1075:13
    #10 0x643fb72c4d74 in std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_set.h:433:21
    #11 0x643fb7260467 in make_uset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:65:56
    #12 0x643fb72a8809 in main /work/test/runtime_runner.cpp:3187:33
    #13 0x7c3c82af91c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x7c3c82af928a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #15 0x643fb70e74b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4257:8 in f_uset_erase_begin_it_llamada(std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x785c81ddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x785c81ddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x785c81ddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x785c81ddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x785c81ddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x785c81de0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x785c81de0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x785c81de0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x785c81de0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x785c81de0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x785c81de0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1678==ABORTING
````

</details>

## Handle: referencia

### f_uset_erase_begin_ref_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_uset_erase_begin_ref_recto(std::unordered_set<int>& c) {
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
>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert_unique_aux<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:904:11
    #8 0x5aff0fbda64a in std::pair<std::__detail::_Node_iterator<int, true, false>, bool> std::_Hashtable<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&, std::integral_constant<bool, true>) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:916:11
    #9 0x5aff0fbda2ef in std::__detail::_Insert<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>, true>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable_policy.h:1075:13
    #10 0x5aff0fba5d74 in std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_set.h:433:21
    #11 0x5aff0fb41467 in make_uset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:65:56
    #12 0x5aff0fb8999d in main /work/test/runtime_runner.cpp:3192:33
    #13 0x7d2692c131c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x7d2692c1328a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #15 0x5aff0f9c84b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4263:8 in f_uset_erase_begin_ref_recto(std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x794691fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x794691fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x794691fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x794691fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x794691fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x794691fe0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x794691fe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x794691fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x794691fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x794691fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x794691fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1681==ABORTING
````

</details>

### f_uset_erase_begin_ref_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_uset_erase_begin_ref_guarda(std::unordered_set<int>& c) {
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
, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert_unique_aux<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:904:11
    #8 0x58c2e381764a in std::pair<std::__detail::_Node_iterator<int, true, false>, bool> std::_Hashtable<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&, std::integral_constant<bool, true>) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:916:11
    #9 0x58c2e38172ef in std::__detail::_Insert<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>, true>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable_policy.h:1075:13
    #10 0x58c2e37e2d74 in std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_set.h:433:21
    #11 0x58c2e377e467 in make_uset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:65:56
    #12 0x58c2e37c6b31 in main /work/test/runtime_runner.cpp:3197:33
    #13 0x7601901b71c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x7601901b728a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #15 0x58c2e36054b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4270:8 in f_uset_erase_begin_ref_guarda(std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x72218f3dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x72218f3dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x72218f3dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x72218f3dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x72218f3dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x72218f3e0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x72218f3e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x72218f3e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x72218f3e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x72218f3e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x72218f3e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1684==ABORTING
````

</details>

### f_uset_erase_begin_ref_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `bucle` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_uset_erase_begin_ref_bucle(std::unordered_set<int>& c) {
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
    [with _Iterator = std::detail::_Node_iterator<int, true, false>; 
    _Sequence = std::debug::unordered_set<int>; _Category = 
    std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffd44863100 {
      type = std::detail::_Node_iterator<int, true, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int> >' @ 0x7ffd448631f0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert_unique_aux<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:904:11
    #8 0x5a7168b9564a in std::pair<std::__detail::_Node_iterator<int, true, false>, bool> std::_Hashtable<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&, std::integral_constant<bool, true>) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:916:11
    #9 0x5a7168b952ef in std::__detail::_Insert<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>, true>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable_policy.h:1075:13
    #10 0x5a7168b60d74 in std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_set.h:433:21
    #11 0x5a7168afc467 in make_uset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:65:56
    #12 0x5a7168b44cc5 in main /work/test/runtime_runner.cpp:3202:33
    #13 0x7de626d861c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x7de626d8628a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #15 0x5a71689834b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4277:10 in f_uset_erase_begin_ref_bucle(std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7a0625fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a0625fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a0625fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a0625fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a0625fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7a0625fe0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x7a0625fe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a0625fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a0625fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a0625fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a0625fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1687==ABORTING
````

</details>

### f_uset_erase_begin_ref_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_uset_erase_begin_ref_llamada(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_uset_erase_begin(c);
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
 std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert_unique_aux<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:904:11
    #8 0x63206101e64a in std::pair<std::__detail::_Node_iterator<int, true, false>, bool> std::_Hashtable<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&, std::integral_constant<bool, true>) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:916:11
    #9 0x63206101e2ef in std::__detail::_Insert<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>, true>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable_policy.h:1075:13
    #10 0x632060fe9d74 in std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_set.h:433:21
    #11 0x632060f85467 in make_uset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:65:56
    #12 0x632060fcde59 in main /work/test/runtime_runner.cpp:3207:33
    #13 0x7f08a703b1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x7f08a703b28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #15 0x632060e0c4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4285:8 in f_uset_erase_begin_ref_llamada(std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7b28a63dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b28a63dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b28a63dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b28a63dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b28a63dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b28a63e0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x7b28a63e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b28a63e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b28a63e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b28a63e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b28a63e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1690==ABORTING
````

</details>

## Handle: puntero

### f_uset_erase_begin_ptr_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_uset_erase_begin_ptr_recto(std::unordered_set<int>& c) {
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
>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert_unique_aux<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:904:11
    #8 0x62cb22fd664a in std::pair<std::__detail::_Node_iterator<int, true, false>, bool> std::_Hashtable<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&, std::integral_constant<bool, true>) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:916:11
    #9 0x62cb22fd62ef in std::__detail::_Insert<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>, true>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable_policy.h:1075:13
    #10 0x62cb22fa1d74 in std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_set.h:433:21
    #11 0x62cb22f3d467 in make_uset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:65:56
    #12 0x62cb22f85fed in main /work/test/runtime_runner.cpp:3212:33
    #13 0x716ee246f1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x716ee246f28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #15 0x62cb22dc44b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4291:8 in f_uset_erase_begin_ptr_recto(std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6d8ee17dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d8ee17dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d8ee17dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d8ee17dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d8ee17dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6d8ee17e0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x6d8ee17e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d8ee17e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d8ee17e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d8ee17e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d8ee17e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1693==ABORTING
````

</details>

### f_uset_erase_begin_ptr_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_uset_erase_begin_ptr_guarda(std::unordered_set<int>& c) {
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
, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert_unique_aux<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:904:11
    #8 0x5c5ba992264a in std::pair<std::__detail::_Node_iterator<int, true, false>, bool> std::_Hashtable<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&, std::integral_constant<bool, true>) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:916:11
    #9 0x5c5ba99222ef in std::__detail::_Insert<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>, true>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable_policy.h:1075:13
    #10 0x5c5ba98edd74 in std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_set.h:433:21
    #11 0x5c5ba9889467 in make_uset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:65:56
    #12 0x5c5ba98d2181 in main /work/test/runtime_runner.cpp:3217:33
    #13 0x792659a221c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x792659a2228a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #15 0x5c5ba97104b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4298:8 in f_uset_erase_begin_ptr_guarda(std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x754658ddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x754658ddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x754658ddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x754658ddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x754658ddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x754658de0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x754658de0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x754658de0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x754658de0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x754658de0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x754658de0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1696==ABORTING
````

</details>

### f_uset_erase_begin_ptr_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `bucle` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_uset_erase_begin_ptr_bucle(std::unordered_set<int>& c) {
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
    [with _Iterator = std::detail::_Node_iterator<int, true, false>; 
    _Sequence = std::debug::unordered_set<int>; _Category = 
    std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffe8287a070 {
      type = std::detail::_Node_iterator<int, true, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int> >' @ 0x7ffe8287a160
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert_unique_aux<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:904:11
    #8 0x5e4cd18ba64a in std::pair<std::__detail::_Node_iterator<int, true, false>, bool> std::_Hashtable<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&, std::integral_constant<bool, true>) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:916:11
    #9 0x5e4cd18ba2ef in std::__detail::_Insert<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>, true>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable_policy.h:1075:13
    #10 0x5e4cd1885d74 in std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_set.h:433:21
    #11 0x5e4cd1821467 in make_uset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:65:56
    #12 0x5e4cd186a315 in main /work/test/runtime_runner.cpp:3222:33
    #13 0x740afc18d1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x740afc18d28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #15 0x5e4cd16a84b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4305:10 in f_uset_erase_begin_ptr_bucle(std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x702afb3dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x702afb3dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x702afb3dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x702afb3dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x702afb3dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x702afb3e0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x702afb3e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x702afb3e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x702afb3e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x702afb3e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x702afb3e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1699==ABORTING
````

</details>

### f_uset_erase_begin_ptr_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_uset_erase_begin_ptr_llamada(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_uset_erase_begin(c);
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
 std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert_unique_aux<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:904:11
    #8 0x63e1acba164a in std::pair<std::__detail::_Node_iterator<int, true, false>, bool> std::_Hashtable<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>>::_M_insert<int, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>>>(int&&, std::__detail::_AllocNode<std::allocator<std::__detail::_Hash_node<int, false>>> const&, std::integral_constant<bool, true>) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable.h:916:11
    #9 0x63e1acba12ef in std::__detail::_Insert<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true>, true>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/hashtable_policy.h:1075:13
    #10 0x63e1acb6cd74 in std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>::insert(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/unordered_set.h:433:21
    #11 0x63e1acb08467 in make_uset(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:65:56
    #12 0x63e1acb514a9 in main /work/test/runtime_runner.cpp:3227:33
    #13 0x7f737d44f1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x7f737d44f28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #15 0x63e1ac98f4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4313:8 in f_uset_erase_begin_ptr_llamada(std::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7b937c7dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b937c7dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b937c7dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b937c7dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b937c7dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b937c7e0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x7b937c7e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b937c7e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b937c7e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b937c7e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b937c7e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1702==ABORTING
````

</details>
