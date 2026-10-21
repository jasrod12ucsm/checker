# `std::multimap::clear`

Mutación: `c.clear();`

- Iterador retenido: 🔴 `UB`
- Referencia/puntero retenido: 🔴 `UB`
- Casos `UB` detectados estáticamente: 5/12

**En palabras:** después de `c.clear();` sobre un `std::multimap`, un iterador guardado queda **inválido**: usarlo después es un bug (UB); una referencia o puntero guardado queda **inválido**: usarlo después es un bug (UB).

Mapa de los 12 casos. Cada celda muestra la respuesta correcta (etiqueta) y, debajo, lo que hizo el analizador estático de Clang. Clic para ir al caso. Ver [Cómo leer este libro](../../guia.md).

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🔴 `UB`<br>❌ no detectado](#f_mmap_clear_it_recto) | [🔴 `UB`<br>✅ detectado](#f_mmap_clear_it_guarda) | [🔴 `UB`<br>✅ detectado](#f_mmap_clear_it_bucle) | [🔴 `UB`<br>✅ detectado](#f_mmap_clear_it_llamada) |
| **referencia** | [🔴 `UB`<br>❌ no detectado](#f_mmap_clear_ref_recto) | [🔴 `UB`<br>❌ no detectado](#f_mmap_clear_ref_guarda) | [🔴 `UB`<br>✅ detectado](#f_mmap_clear_ref_bucle) | [🔴 `UB`<br>❌ no detectado](#f_mmap_clear_ref_llamada) |
| **puntero** | [🔴 `UB`<br>❌ no detectado](#f_mmap_clear_ptr_recto) | [🔴 `UB`<br>❌ no detectado](#f_mmap_clear_ptr_guarda) | [🔴 `UB`<br>✅ detectado](#f_mmap_clear_ptr_bucle) | [🔴 `UB`<br>❌ no detectado](#f_mmap_clear_ptr_llamada) |

## Handle: iterador

### f_mmap_clear_it_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_mmap_clear_it_recto(std::multimap<int,int>& c) {
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
    >; _Sequence = std::debug::multimap<int, int>; _Category = 
    std::forward_iterator_tag; pointer = std::pair<const int, int>*]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fff61851a80 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7fff61851b00
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
d::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x5abb8081c8f7 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_equal_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x5abb8081c4f9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_equal<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x5abb807d35b3 in std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::multimap(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multimap.h:234:14
    #10 0x5abb80768e7a in make_mmap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:58:68
    #11 0x5abb807ae80e in main /work/test/runtime_runner.cpp:3022:33
    #12 0x7702b5c4f1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x7702b5c4f28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x5abb805f04b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4032:12 in f_mmap_clear_it_recto(std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x7342b4fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7342b4fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7342b4fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7342b4fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7342b4fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7342b4fe0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7342b4fe0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7342b4fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7342b4fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7342b4fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7342b4fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1585==ABORTING
````

</details>

### f_mmap_clear_it_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `guarda` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_mmap_clear_it_guarda(std::multimap<int,int>& c) {
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
    >; _Sequence = std::debug::multimap<int, int>; _Category = 
    std::forward_iterator_tag; pointer = std::pair<const int, int>*]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffdd9262c40 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffdd9262d00
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x55eb0ac8e8f7 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_equal_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x55eb0ac8e4f9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_equal<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x55eb0ac455b3 in std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::multimap(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multimap.h:234:14
    #10 0x55eb0abdae7a in make_mmap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:58:68
    #11 0x55eb0ac2094a in main /work/test/runtime_runner.cpp:3027:33
    #12 0x711302d2d1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x711302d2d28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x55eb0aa624b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4038:12 in f_mmap_clear_it_guarda(std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x6d5301fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d5301fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d5301fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d5301fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d5301fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6d5301fe0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x6d5301fe0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x6d5301fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d5301fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d5301fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d5301fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1588==ABORTING
````

</details>

### f_mmap_clear_it_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_mmap_clear_it_bucle(std::multimap<int,int>& c) {
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
    >; _Sequence = std::debug::multimap<int, int>; _Category = 
    std::forward_iterator_tag; pointer = std::pair<const int, int>*]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffce3341f90 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffce3342050
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
d::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x644dd1af38f7 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_equal_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x644dd1af34f9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_equal<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x644dd1aaa5b3 in std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::multimap(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multimap.h:234:14
    #10 0x644dd1a3fe7a in make_mmap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:58:68
    #11 0x644dd1a85a86 in main /work/test/runtime_runner.cpp:3032:33
    #12 0x7fe7aa8851c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x7fe7aa88528a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x644dd18c74b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4044:14 in f_mmap_clear_it_bucle(std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x7c27a9bdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c27a9bdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c27a9bdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c27a9bdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c27a9bdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c27a9be0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7c27a9be0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7c27a9be0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c27a9be0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c27a9be0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c27a9be0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1591==ABORTING
````

</details>

### f_mmap_clear_it_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `llamada` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_mmap_clear_it_llamada(std::multimap<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_mmap_clear(c);
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
    >; _Sequence = std::debug::multimap<int, int>; _Category = 
    std::forward_iterator_tag; pointer = std::pair<const int, int>*]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffcbb7eb520 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffcbb7eb5e0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
:_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x64413800a8f7 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_equal_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x64413800a4f9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_equal<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x644137fc15b3 in std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::multimap(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multimap.h:234:14
    #10 0x644137f56e7a in make_mmap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:58:68
    #11 0x644137f9cbc2 in main /work/test/runtime_runner.cpp:3037:33
    #12 0x76d02dd721c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x76d02dd7228a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x644137dde4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4051:12 in f_mmap_clear_it_llamada(std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x73102cfdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73102cfdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73102cfdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73102cfdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73102cfdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x73102cfe0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x73102cfe0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x73102cfe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x73102cfe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x73102cfe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x73102cfe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1594==ABORTING
````

</details>

## Handle: referencia

### f_mmap_clear_ref_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_mmap_clear_ref_recto(std::multimap<int,int>& c) {
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
::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x6493e63138f7 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_equal_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x6493e63134f9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_equal<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x6493e62ca5b3 in std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::multimap(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multimap.h:234:14
    #10 0x6493e625fe7a in make_mmap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:58:68
    #11 0x6493e62a5cfe in main /work/test/runtime_runner.cpp:3042:33
    #12 0x726311c491c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x726311c4928a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x6493e60e74b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4057:10 in f_mmap_clear_ref_recto(std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x6ea310fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6ea310fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6ea310fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6ea310fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6ea310fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6ea310fe0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x6ea310fe0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x6ea310fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6ea310fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6ea310fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6ea310fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1597==ABORTING
````

</details>

### f_mmap_clear_ref_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_mmap_clear_ref_guarda(std::multimap<int,int>& c) {
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
:_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x5b37eab0f8f7 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_equal_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x5b37eab0f4f9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_equal<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x5b37eaac65b3 in std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::multimap(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multimap.h:234:14
    #10 0x5b37eaa5be7a in make_mmap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:58:68
    #11 0x5b37eaaa1e3a in main /work/test/runtime_runner.cpp:3047:33
    #12 0x7064a461a1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x7064a461a28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x5b37ea8e34b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4064:10 in f_mmap_clear_ref_guarda(std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x6ca4a39dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6ca4a39dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6ca4a39dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6ca4a39dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6ca4a39dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6ca4a39e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x6ca4a39e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x6ca4a39e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6ca4a39e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6ca4a39e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6ca4a39e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1600==ABORTING
````

</details>

### f_mmap_clear_ref_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `bucle` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_mmap_clear_ref_bucle(std::multimap<int,int>& c) {
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
    _Sequence = std::debug::multimap<int, int>; _Category = 
    std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fffc42b2ff0 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7fffc42b30b0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x5bc05eec58f7 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_equal_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x5bc05eec54f9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_equal<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x5bc05ee7c5b3 in std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::multimap(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multimap.h:234:14
    #10 0x5bc05ee11e7a in make_mmap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:58:68
    #11 0x5bc05ee57f76 in main /work/test/runtime_runner.cpp:3052:33
    #12 0x7616ff90f1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x7616ff90f28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x5bc05ec994b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4071:12 in f_mmap_clear_ref_bucle(std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x7256febdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7256febdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7256febdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7256febdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7256febdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7256febe0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7256febe0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7256febe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7256febe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7256febe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7256febe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1603==ABORTING
````

</details>

### f_mmap_clear_ref_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_mmap_clear_ref_llamada(std::multimap<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_mmap_clear(c);
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
_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x5a4917e528f7 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_equal_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x5a4917e524f9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_equal<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x5a4917e095b3 in std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::multimap(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multimap.h:234:14
    #10 0x5a4917d9ee7a in make_mmap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:58:68
    #11 0x5a4917de50b2 in main /work/test/runtime_runner.cpp:3057:33
    #12 0x7e6d457981c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x7e6d4579828a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x5a4917c264b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4079:10 in f_mmap_clear_ref_llamada(std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x7aad449dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7aad449dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7aad449dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7aad449dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7aad449dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7aad449e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7aad449e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7aad449e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7aad449e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7aad449e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7aad449e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1606==ABORTING
````

</details>

## Handle: puntero

### f_mmap_clear_ptr_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_mmap_clear_ptr_recto(std::multimap<int,int>& c) {
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
::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x64bc9d7ca8f7 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_equal_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x64bc9d7ca4f9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_equal<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x64bc9d7815b3 in std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::multimap(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multimap.h:234:14
    #10 0x64bc9d716e7a in make_mmap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:58:68
    #11 0x64bc9d75d1ee in main /work/test/runtime_runner.cpp:3062:33
    #12 0x7eedf70941c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x7eedf709428a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x64bc9d59e4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4085:11 in f_mmap_clear_ptr_recto(std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x7b2df63dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b2df63dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b2df63dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b2df63dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b2df63dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b2df63e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7b2df63e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7b2df63e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b2df63e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b2df63e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b2df63e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1609==ABORTING
````

</details>

### f_mmap_clear_ptr_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_mmap_clear_ptr_guarda(std::multimap<int,int>& c) {
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
:_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x57d34650b8f7 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_equal_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x57d34650b4f9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_equal<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x57d3464c25b3 in std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::multimap(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multimap.h:234:14
    #10 0x57d346457e7a in make_mmap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:58:68
    #11 0x57d34649e32a in main /work/test/runtime_runner.cpp:3067:33
    #12 0x71d241d211c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x71d241d2128a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x57d3462df4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4092:11 in f_mmap_clear_ptr_guarda(std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x6e1240fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e1240fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e1240fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e1240fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e1240fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6e1240fe0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x6e1240fe0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x6e1240fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e1240fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e1240fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e1240fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1612==ABORTING
````

</details>

### f_mmap_clear_ptr_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `bucle` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_mmap_clear_ptr_bucle(std::multimap<int,int>& c) {
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
    _Sequence = std::debug::multimap<int, int>; _Category = 
    std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffcfd2425b0 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffcfd242670
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x59ad71f668f7 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_equal_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x59ad71f664f9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_equal<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x59ad71f1d5b3 in std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::multimap(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multimap.h:234:14
    #10 0x59ad71eb2e7a in make_mmap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:58:68
    #11 0x59ad71ef9466 in main /work/test/runtime_runner.cpp:3072:33
    #12 0x744d130f41c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x744d130f428a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x59ad71d3a4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4099:13 in f_mmap_clear_ptr_bucle(std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x708d123dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x708d123dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x708d123dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x708d123dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x708d123dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x708d123e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x708d123e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x708d123e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x708d123e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x708d123e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x708d123e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1615==ABORTING
````

</details>

### f_mmap_clear_ptr_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_mmap_clear_ptr_llamada(std::multimap<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_mmap_clear(c);
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
_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x623afd7968f7 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_equal_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x623afd7964f9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_equal<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x623afd74d5b3 in std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::multimap(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multimap.h:234:14
    #10 0x623afd6e2e7a in make_mmap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:58:68
    #11 0x623afd7295a2 in main /work/test/runtime_runner.cpp:3077:33
    #12 0x7891712351c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x78917123528a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x623afd56a4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4107:11 in f_mmap_clear_ptr_llamada(std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x74d1705dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x74d1705dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x74d1705dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x74d1705dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x74d1705dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x74d1705e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x74d1705e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x74d1705e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x74d1705e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x74d1705e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x74d1705e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1618==ABORTING
````

</details>
