# `std::map::clear`

Mutación: `c.clear();`

- Iterador retenido: 🔴 `UB`
- Referencia/puntero retenido: 🔴 `UB`
- Casos `UB` detectados estáticamente: 5/12

**En palabras:** después de `c.clear();` sobre un `std::map`, un iterador guardado queda **inválido**: usarlo después es un bug (UB); una referencia o puntero guardado queda **inválido**: usarlo después es un bug (UB).

Mapa de los 12 casos. Cada celda muestra la respuesta correcta (etiqueta) y, debajo, lo que hizo el analizador estático de Clang. Clic para ir al caso. Ver [Cómo leer este libro](../../guia.md).

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🔴 `UB`<br>❌ no detectado](#f_map_clear_it_recto) | [🔴 `UB`<br>✅ detectado](#f_map_clear_it_guarda) | [🔴 `UB`<br>✅ detectado](#f_map_clear_it_bucle) | [🔴 `UB`<br>✅ detectado](#f_map_clear_it_llamada) |
| **referencia** | [🔴 `UB`<br>❌ no detectado](#f_map_clear_ref_recto) | [🔴 `UB`<br>❌ no detectado](#f_map_clear_ref_guarda) | [🔴 `UB`<br>✅ detectado](#f_map_clear_ref_bucle) | [🔴 `UB`<br>❌ no detectado](#f_map_clear_ref_llamada) |
| **puntero** | [🔴 `UB`<br>❌ no detectado](#f_map_clear_ptr_recto) | [🔴 `UB`<br>❌ no detectado](#f_map_clear_ptr_guarda) | [🔴 `UB`<br>✅ detectado](#f_map_clear_ptr_bucle) | [🔴 `UB`<br>❌ no detectado](#f_map_clear_ptr_llamada) |

## Handle: iterador

### f_map_clear_it_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_map_clear_it_recto(std::map<int,int>& c) {
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
    const [with _Iterator = std::_Rb_tree_iterator<std::pair<const int, int> 
    >; _Sequence = std::debug::map<int, int>; _Category = 
    std::forward_iterator_tag; pointer = std::pair<const int, int>*]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffd0b04f0a0 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::map<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffd0b04f120
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
onst, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x5a056a3f5899 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_unique_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x5a056a3f51c9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_unique<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x5a056a3ad183 in std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::map(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_map.h:244:14
    #10 0x5a056a342aaa in make_map(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:57:62
    #11 0x5a056a385556 in main /work/test/runtime_runner.cpp:2842:28
    #12 0x72c2f50481c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x72c2f504828a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x5a056a1ca4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3792:12 in f_map_clear_it_recto(std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x6f02f43dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f02f43dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f02f43dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f02f43dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f02f43dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6f02f43e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x6f02f43e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x6f02f43e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f02f43e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f02f43e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f02f43e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1489==ABORTING
````

</details>

### f_map_clear_it_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `guarda` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_map_clear_it_guarda(std::map<int,int>& c) {
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
    const [with _Iterator = std::_Rb_tree_iterator<std::pair<const int, int> 
    >; _Sequence = std::debug::map<int, int>; _Category = 
    std::forward_iterator_tag; pointer = std::pair<const int, int>*]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffecce120a0 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::map<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffecce12160
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
nst, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x625fe7321899 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_unique_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x625fe73211c9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_unique<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x625fe72d9183 in std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::map(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_map.h:244:14
    #10 0x625fe726eaaa in make_map(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:57:62
    #11 0x625fe72b1692 in main /work/test/runtime_runner.cpp:2847:28
    #12 0x76b9281d01c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x76b9281d028a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x625fe70f64b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3798:12 in f_map_clear_it_guarda(std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x72f9275dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x72f9275dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x72f9275dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x72f9275dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x72f9275dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x72f9275e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x72f9275e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x72f9275e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x72f9275e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x72f9275e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x72f9275e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1492==ABORTING
````

</details>

### f_map_clear_it_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_map_clear_it_bucle(std::map<int,int>& c) {
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
    const [with _Iterator = std::_Rb_tree_iterator<std::pair<const int, int> 
    >; _Sequence = std::debug::map<int, int>; _Category = 
    std::forward_iterator_tag; pointer = std::pair<const int, int>*]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffe5f264730 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::map<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffe5f2647f0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
onst, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x5d2766e18899 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_unique_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x5d2766e181c9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_unique<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x5d2766dd0183 in std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::map(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_map.h:244:14
    #10 0x5d2766d65aaa in make_map(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:57:62
    #11 0x5d2766da87ce in main /work/test/runtime_runner.cpp:2852:28
    #12 0x7b46247ab1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x7b46247ab28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x5d2766bed4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3804:14 in f_map_clear_it_bucle(std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x7786239dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7786239dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7786239dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7786239dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7786239dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7786239e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7786239e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7786239e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7786239e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7786239e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7786239e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1495==ABORTING
````

</details>

### f_map_clear_it_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `llamada` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_map_clear_it_llamada(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_map_clear(c);
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
    const [with _Iterator = std::_Rb_tree_iterator<std::pair<const int, int> 
    >; _Sequence = std::debug::map<int, int>; _Category = 
    std::forward_iterator_tag; pointer = std::pair<const int, int>*]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffc846fe500 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::map<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffc846fe5c0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
st, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x5fe6a3b4b899 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_unique_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x5fe6a3b4b1c9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_unique<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x5fe6a3b03183 in std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::map(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_map.h:244:14
    #10 0x5fe6a3a98aaa in make_map(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:57:62
    #11 0x5fe6a3adb90a in main /work/test/runtime_runner.cpp:2857:28
    #12 0x7a7e885341c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x7a7e8853428a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x5fe6a39204b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3811:12 in f_map_clear_it_llamada(std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x76be877dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x76be877dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x76be877dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x76be877dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x76be877dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x76be877e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x76be877e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x76be877e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x76be877e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x76be877e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x76be877e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1498==ABORTING
````

</details>

## Handle: referencia

### f_map_clear_ref_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_map_clear_ref_recto(std::map<int,int>& c) {
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
nst, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x58d051e82899 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_unique_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x58d051e821c9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_unique<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x58d051e3a183 in std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::map(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_map.h:244:14
    #10 0x58d051dcfaaa in make_map(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:57:62
    #11 0x58d051e12a46 in main /work/test/runtime_runner.cpp:2862:28
    #12 0x71c3091271c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x71c30912728a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x58d051c574b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3817:10 in f_map_clear_ref_recto(std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x6e03083dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e03083dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e03083dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e03083dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e03083dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6e03083e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x6e03083e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x6e03083e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e03083e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e03083e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e03083e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1501==ABORTING
````

</details>

### f_map_clear_ref_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_map_clear_ref_guarda(std::map<int,int>& c) {
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
st, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x5573436b8899 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_unique_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x5573436b81c9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_unique<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x557343670183 in std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::map(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_map.h:244:14
    #10 0x557343605aaa in make_map(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:57:62
    #11 0x557343648b82 in main /work/test/runtime_runner.cpp:2867:28
    #12 0x7bb9853f31c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x7bb9853f328a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x55734348d4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3824:10 in f_map_clear_ref_guarda(std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x77f9847dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x77f9847dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x77f9847dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x77f9847dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x77f9847dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x77f9847e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x77f9847e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x77f9847e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x77f9847e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x77f9847e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x77f9847e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1504==ABORTING
````

</details>

### f_map_clear_ref_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `bucle` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_map_clear_ref_bucle(std::map<int,int>& c) {
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
    [with _Iterator = std::_Rb_tree_iterator<std::pair<const int, int> >; 
    _Sequence = std::debug::map<int, int>; _Category = 
    std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffc39ea2410 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::map<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffc39ea24d0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
nst, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x583917223899 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_unique_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x5839172231c9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_unique<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x5839171db183 in std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::map(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_map.h:244:14
    #10 0x583917170aaa in make_map(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:57:62
    #11 0x5839171b3cbe in main /work/test/runtime_runner.cpp:2872:28
    #12 0x76d11084d1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x76d11084d28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x583916ff84b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3831:12 in f_map_clear_ref_bucle(std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x73110fbdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73110fbdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73110fbdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73110fbdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73110fbdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x73110fbe0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x73110fbe0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x73110fbe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x73110fbe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x73110fbe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x73110fbe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1507==ABORTING
````

</details>

### f_map_clear_ref_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_map_clear_ref_llamada(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_map_clear(c);
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
t, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x59ed83a36899 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_unique_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x59ed83a361c9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_unique<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x59ed839ee183 in std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::map(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_map.h:244:14
    #10 0x59ed83983aaa in make_map(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:57:62
    #11 0x59ed839c6dfa in main /work/test/runtime_runner.cpp:2877:28
    #12 0x79203cd791c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x79203cd7928a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x59ed8380b4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3839:10 in f_map_clear_ref_llamada(std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x75603bfdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75603bfdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75603bfdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75603bfdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75603bfdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x75603bfe0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x75603bfe0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x75603bfe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x75603bfe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x75603bfe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x75603bfe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1510==ABORTING
````

</details>

## Handle: puntero

### f_map_clear_ptr_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_map_clear_ptr_recto(std::map<int,int>& c) {
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
nst, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x55f402b3b899 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_unique_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x55f402b3b1c9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_unique<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x55f402af3183 in std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::map(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_map.h:244:14
    #10 0x55f402a88aaa in make_map(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:57:62
    #11 0x55f402acbf36 in main /work/test/runtime_runner.cpp:2882:28
    #12 0x744c71f591c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x744c71f5928a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x55f4029104b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3845:11 in f_map_clear_ptr_recto(std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x708c711dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x708c711dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x708c711dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x708c711dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x708c711dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x708c711e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x708c711e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x708c711e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x708c711e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x708c711e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x708c711e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1513==ABORTING
````

</details>

### f_map_clear_ptr_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_map_clear_ptr_guarda(std::map<int,int>& c) {
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
st, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x5c1de9ac0899 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_unique_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x5c1de9ac01c9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_unique<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x5c1de9a78183 in std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::map(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_map.h:244:14
    #10 0x5c1de9a0daaa in make_map(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:57:62
    #11 0x5c1de9a51072 in main /work/test/runtime_runner.cpp:2887:28
    #12 0x7e93c28161c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x7e93c281628a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x5c1de98954b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3852:11 in f_map_clear_ptr_guarda(std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x7ad3c1bdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ad3c1bdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ad3c1bdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ad3c1bdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ad3c1bdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7ad3c1be0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7ad3c1be0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7ad3c1be0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ad3c1be0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ad3c1be0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ad3c1be0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1516==ABORTING
````

</details>

### f_map_clear_ptr_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `bucle` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_map_clear_ptr_bucle(std::map<int,int>& c) {
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
    [with _Iterator = std::_Rb_tree_iterator<std::pair<const int, int> >; 
    _Sequence = std::debug::map<int, int>; _Category = 
    std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffeb5bb6e00 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::map<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffeb5bb6ec0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
nst, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x608b44826899 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_unique_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x608b448261c9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_unique<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x608b447de183 in std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::map(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_map.h:244:14
    #10 0x608b44773aaa in make_map(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:57:62
    #11 0x608b447b71ae in main /work/test/runtime_runner.cpp:2892:28
    #12 0x72b25944b1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x72b25944b28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x608b445fb4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3859:13 in f_map_clear_ptr_bucle(std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x6ef2587dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6ef2587dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6ef2587dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6ef2587dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6ef2587dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6ef2587e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x6ef2587e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x6ef2587e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6ef2587e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6ef2587e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6ef2587e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1519==ABORTING
````

</details>

### f_map_clear_ptr_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_map_clear_ptr_llamada(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_map_clear(c);
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
t, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x61585324c899 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_unique_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x61585324c1c9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_unique<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x615853204183 in std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::map(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_map.h:244:14
    #10 0x615853199aaa in make_map(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:57:62
    #11 0x6158531dd2ea in main /work/test/runtime_runner.cpp:2897:28
    #12 0x76a08d0cf1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x76a08d0cf28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x6158530214b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3867:11 in f_map_clear_ptr_llamada(std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x72e08c3dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x72e08c3dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x72e08c3dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x72e08c3dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x72e08c3dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x72e08c3e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x72e08c3e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x72e08c3e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x72e08c3e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x72e08c3e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x72e08c3e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1522==ABORTING
````

</details>
