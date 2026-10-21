# `std::multimap::erase_begin`

Mutación: `c.erase(c.begin());`

- Iterador retenido: 🔴 `UB`
- Referencia/puntero retenido: 🔴 `UB`
- Casos `UB` detectados estáticamente: 0/12

**En palabras:** después de `c.erase(c.begin());` sobre un `std::multimap`, un iterador guardado queda **inválido**: usarlo después es un bug (UB); una referencia o puntero guardado queda **inválido**: usarlo después es un bug (UB).

Mapa de los 12 casos. Cada celda muestra la respuesta correcta (etiqueta) y, debajo, lo que hizo el analizador estático de Clang. Clic para ir al caso. Ver [Cómo leer este libro](../../guia.md).

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🔴 `UB`<br>❌ no detectado](#f_mmap_erase_begin_it_recto) | [🔴 `UB`<br>❌ no detectado](#f_mmap_erase_begin_it_guarda) | [🔴 `UB`<br>❌ no detectado](#f_mmap_erase_begin_it_bucle) | [🔴 `UB`<br>❌ no detectado](#f_mmap_erase_begin_it_llamada) |
| **referencia** | [🔴 `UB`<br>❌ no detectado](#f_mmap_erase_begin_ref_recto) | [🔴 `UB`<br>❌ no detectado](#f_mmap_erase_begin_ref_guarda) | [🔴 `UB`<br>❌ no detectado](#f_mmap_erase_begin_ref_bucle) | [🔴 `UB`<br>❌ no detectado](#f_mmap_erase_begin_ref_llamada) |
| **puntero** | [🔴 `UB`<br>❌ no detectado](#f_mmap_erase_begin_ptr_recto) | [🔴 `UB`<br>❌ no detectado](#f_mmap_erase_begin_ptr_guarda) | [🔴 `UB`<br>❌ no detectado](#f_mmap_erase_begin_ptr_bucle) | [🔴 `UB`<br>❌ no detectado](#f_mmap_erase_begin_ptr_llamada) |

## Handle: iterador

### f_mmap_erase_begin_it_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_mmap_erase_begin_it_recto(std::multimap<int,int>& c) {
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
    const [with _Iterator = std::_Rb_tree_iterator<std::pair<const int, int> 
    >; _Sequence = std::debug::multimap<int, int>; _Category = 
    std::forward_iterator_tag; pointer = std::pair<const int, int>*]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffefd926dc0 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffefd926eb0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x5b3ddb3a08f7 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_equal_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x5b3ddb3a04f9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_equal<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x5b3ddb3575b3 in std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::multimap(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multimap.h:234:14
    #10 0x5b3ddb2ece7a in make_mmap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:58:68
    #11 0x5b3ddb33161a in main /work/test/runtime_runner.cpp:2962:33
    #12 0x72c6238a71c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x72c6238a728a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x5b3ddb1744b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3952:12 in f_mmap_erase_begin_it_recto(std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x6f0622bdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f0622bdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f0622bdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f0622bdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f0622bdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6f0622be0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x6f0622be0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x6f0622be0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f0622be0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f0622be0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f0622be0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1549==ABORTING
````

</details>

### f_mmap_erase_begin_it_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_mmap_erase_begin_it_guarda(std::multimap<int,int>& c) {
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
    const [with _Iterator = std::_Rb_tree_iterator<std::pair<const int, int> 
    >; _Sequence = std::debug::multimap<int, int>; _Category = 
    std::forward_iterator_tag; pointer = std::pair<const int, int>*]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fff325652d0 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7fff325653c0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x60b13aa028f7 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_equal_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x60b13aa024f9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_equal<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x60b13a9b95b3 in std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::multimap(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multimap.h:234:14
    #10 0x60b13a94ee7a in make_mmap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:58:68
    #11 0x60b13a993799 in main /work/test/runtime_runner.cpp:2967:33
    #12 0x78b3ce7011c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x78b3ce70128a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x60b13a7d64b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3958:12 in f_mmap_erase_begin_it_guarda(std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x74f3cd9dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x74f3cd9dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x74f3cd9dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x74f3cd9dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x74f3cd9dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x74f3cd9e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x74f3cd9e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x74f3cd9e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x74f3cd9e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x74f3cd9e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x74f3cd9e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1552==ABORTING
````

</details>

### f_mmap_erase_begin_it_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_mmap_erase_begin_it_bucle(std::multimap<int,int>& c) {
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
    const [with _Iterator = std::_Rb_tree_iterator<std::pair<const int, int> 
    >; _Sequence = std::debug::multimap<int, int>; _Category = 
    std::forward_iterator_tag; pointer = std::pair<const int, int>*]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffcc7a6ba60 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffcc7a6bb50
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x55a2456948f7 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_equal_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x55a2456944f9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_equal<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x55a24564b5b3 in std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::multimap(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multimap.h:234:14
    #10 0x55a2455e0e7a in make_mmap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:58:68
    #11 0x55a245625918 in main /work/test/runtime_runner.cpp:2972:33
    #12 0x7798bf80a1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x7798bf80a28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x55a2454684b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3964:14 in f_mmap_erase_begin_it_bucle(std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x73d8bebdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73d8bebdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73d8bebdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73d8bebdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x73d8bebdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x73d8bebe0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x73d8bebe0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x73d8bebe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x73d8bebe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x73d8bebe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x73d8bebe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1555==ABORTING
````

</details>

### f_mmap_erase_begin_it_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_mmap_erase_begin_it_llamada(std::multimap<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_mmap_erase_begin(c);
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
    const [with _Iterator = std::_Rb_tree_iterator<std::pair<const int, int> 
    >; _Sequence = std::debug::multimap<int, int>; _Category = 
    std::forward_iterator_tag; pointer = std::pair<const int, int>*]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffdcba7a6b0 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffdcba7a770
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
ree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x5ac527e6a8f7 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_equal_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x5ac527e6a4f9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_equal<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x5ac527e215b3 in std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::multimap(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multimap.h:234:14
    #10 0x5ac527db6e7a in make_mmap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:58:68
    #11 0x5ac527dfba97 in main /work/test/runtime_runner.cpp:2977:33
    #12 0x7ba2593951c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x7ba25939528a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x5ac527c3e4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3971:12 in f_mmap_erase_begin_it_llamada(std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x77e2585dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x77e2585dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x77e2585dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x77e2585dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x77e2585dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x77e2585e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x77e2585e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x77e2585e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x77e2585e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x77e2585e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x77e2585e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1558==ABORTING
````

</details>

## Handle: referencia

### f_mmap_erase_begin_ref_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_mmap_erase_begin_ref_recto(std::multimap<int,int>& c) {
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
tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x6464f82cc8f7 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_equal_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x6464f82cc4f9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_equal<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x6464f82835b3 in std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::multimap(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multimap.h:234:14
    #10 0x6464f8218e7a in make_mmap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:58:68
    #11 0x6464f825dc16 in main /work/test/runtime_runner.cpp:2982:33
    #12 0x76daa74431c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x76daa744328a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x6464f80a04b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3977:10 in f_mmap_erase_begin_ref_recto(std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x731aa67dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x731aa67dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x731aa67dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x731aa67dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x731aa67dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x731aa67e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x731aa67e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x731aa67e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x731aa67e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x731aa67e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x731aa67e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1561==ABORTING
````

</details>

### f_mmap_erase_begin_ref_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_mmap_erase_begin_ref_guarda(std::multimap<int,int>& c) {
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
ree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x61c540fac8f7 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_equal_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x61c540fac4f9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_equal<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x61c540f635b3 in std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::multimap(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multimap.h:234:14
    #10 0x61c540ef8e7a in make_mmap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:58:68
    #11 0x61c540f3dd95 in main /work/test/runtime_runner.cpp:2987:33
    #12 0x75f0783d21c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x75f0783d228a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x61c540d804b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3984:10 in f_mmap_erase_begin_ref_guarda(std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x7230777dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7230777dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7230777dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7230777dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7230777dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7230777e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7230777e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7230777e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7230777e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7230777e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7230777e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1564==ABORTING
````

</details>

### f_mmap_erase_begin_ref_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `bucle` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_mmap_erase_begin_ref_bucle(std::multimap<int,int>& c) {
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
    [with _Iterator = std::_Rb_tree_iterator<std::pair<const int, int> >; 
    _Sequence = std::debug::multimap<int, int>; _Category = 
    std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffe01895070 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffe01895160
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x6260ef2768f7 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_equal_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x6260ef2764f9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_equal<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x6260ef22d5b3 in std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::multimap(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multimap.h:234:14
    #10 0x6260ef1c2e7a in make_mmap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:58:68
    #11 0x6260ef207f14 in main /work/test/runtime_runner.cpp:2992:33
    #12 0x70eb34d3c1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x70eb34d3c28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x6260ef04a4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3991:12 in f_mmap_erase_begin_ref_bucle(std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x6d2b33fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d2b33fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d2b33fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d2b33fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d2b33fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6d2b33fe0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x6d2b33fe0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x6d2b33fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d2b33fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d2b33fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d2b33fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1567==ABORTING
````

</details>

### f_mmap_erase_begin_ref_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_mmap_erase_begin_ref_llamada(std::multimap<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_mmap_erase_begin(c);
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
ee<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x5cbf2663a8f7 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_equal_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x5cbf2663a4f9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_equal<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x5cbf265f15b3 in std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::multimap(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multimap.h:234:14
    #10 0x5cbf26586e7a in make_mmap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:58:68
    #11 0x5cbf265cc093 in main /work/test/runtime_runner.cpp:2997:33
    #12 0x7bd7a0f511c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x7bd7a0f5128a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x5cbf2640e4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3999:10 in f_mmap_erase_begin_ref_llamada(std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x7817a01dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7817a01dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7817a01dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7817a01dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7817a01dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7817a01e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7817a01e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7817a01e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7817a01e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7817a01e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7817a01e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1570==ABORTING
````

</details>

## Handle: puntero

### f_mmap_erase_begin_ptr_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_mmap_erase_begin_ptr_recto(std::multimap<int,int>& c) {
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
tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x56b6a69038f7 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_equal_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x56b6a69034f9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_equal<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x56b6a68ba5b3 in std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::multimap(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multimap.h:234:14
    #10 0x56b6a684fe7a in make_mmap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:58:68
    #11 0x56b6a6895212 in main /work/test/runtime_runner.cpp:3002:33
    #12 0x7af86980c1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x7af86980c28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x56b6a66d74b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4005:11 in f_mmap_erase_begin_ptr_recto(std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x773868bdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x773868bdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x773868bdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x773868bdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x773868bdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x773868be0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x773868be0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x773868be0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x773868be0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x773868be0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x773868be0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1573==ABORTING
````

</details>

### f_mmap_erase_begin_ptr_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_mmap_erase_begin_ptr_guarda(std::multimap<int,int>& c) {
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
ree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x5ede6251c8f7 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_equal_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x5ede6251c4f9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_equal<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x5ede624d35b3 in std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::multimap(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multimap.h:234:14
    #10 0x5ede62468e7a in make_mmap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:58:68
    #11 0x5ede624ae391 in main /work/test/runtime_runner.cpp:3007:33
    #12 0x71587c24a1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x71587c24a28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x5ede622f04b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4012:11 in f_mmap_erase_begin_ptr_guarda(std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x6d987b5dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d987b5dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d987b5dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d987b5dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d987b5dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6d987b5e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x6d987b5e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x6d987b5e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d987b5e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d987b5e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d987b5e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1576==ABORTING
````

</details>

### f_mmap_erase_begin_ptr_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `bucle` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_mmap_erase_begin_ptr_bucle(std::multimap<int,int>& c) {
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
    [with _Iterator = std::_Rb_tree_iterator<std::pair<const int, int> >; 
    _Sequence = std::debug::multimap<int, int>; _Category = 
    std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffd51a3b8f0 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffd51a3b9e0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x64850c8f58f7 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_equal_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x64850c8f54f9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_equal<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x64850c8ac5b3 in std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::multimap(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multimap.h:234:14
    #10 0x64850c841e7a in make_mmap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:58:68
    #11 0x64850c887510 in main /work/test/runtime_runner.cpp:3012:33
    #12 0x7cc5052061c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x7cc50520628a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x64850c6c94b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4019:13 in f_mmap_erase_begin_ptr_bucle(std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x7905045dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7905045dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7905045dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7905045dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7905045dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7905045e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7905045e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7905045e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7905045e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7905045e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7905045e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1579==ABORTING
````

</details>

### f_mmap_erase_begin_ptr_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_mmap_erase_begin_ptr_llamada(std::multimap<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_mmap_erase_begin(c);
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
ee<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x61a5fbf5e8f7 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_equal_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2366:11
    #8 0x61a5fbf5e4f9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_equal<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1121:6
    #9 0x61a5fbf155b3 in std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::multimap(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_multimap.h:234:14
    #10 0x61a5fbeaae7a in make_mmap(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:58:68
    #11 0x61a5fbef068f in main /work/test/runtime_runner.cpp:3017:33
    #12 0x79af257661c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x79af2576628a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x61a5fbd324b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:4027:11 in f_mmap_erase_begin_ptr_llamada(std::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x75ef249dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75ef249dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75ef249dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75ef249dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75ef249dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x75ef249e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x75ef249e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x75ef249e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x75ef249e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x75ef249e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x75ef249e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1582==ABORTING
````

</details>
