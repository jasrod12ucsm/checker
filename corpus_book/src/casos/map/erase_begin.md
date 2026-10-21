# `std::map::erase_begin`

Mutación: `c.erase(c.begin());`

- Iterador retenido: 🔴 `UB`
- Referencia/puntero retenido: 🔴 `UB`
- Casos `UB` detectados estáticamente: 0/12

**En palabras:** después de `c.erase(c.begin());` sobre un `std::map`, un iterador guardado queda **inválido**: usarlo después es un bug (UB); una referencia o puntero guardado queda **inválido**: usarlo después es un bug (UB).

Mapa de los 12 casos. Cada celda muestra la respuesta correcta (etiqueta) y, debajo, lo que hizo el analizador estático de Clang. Clic para ir al caso. Ver [Cómo leer este libro](../../guia.md).

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🔴 `UB`<br>❌ no detectado](#f_map_erase_begin_it_recto) | [🔴 `UB`<br>❌ no detectado](#f_map_erase_begin_it_guarda) | [🔴 `UB`<br>❌ no detectado](#f_map_erase_begin_it_bucle) | [🔴 `UB`<br>❌ no detectado](#f_map_erase_begin_it_llamada) |
| **referencia** | [🔴 `UB`<br>❌ no detectado](#f_map_erase_begin_ref_recto) | [🔴 `UB`<br>❌ no detectado](#f_map_erase_begin_ref_guarda) | [🔴 `UB`<br>❌ no detectado](#f_map_erase_begin_ref_bucle) | [🔴 `UB`<br>❌ no detectado](#f_map_erase_begin_ref_llamada) |
| **puntero** | [🔴 `UB`<br>❌ no detectado](#f_map_erase_begin_ptr_recto) | [🔴 `UB`<br>❌ no detectado](#f_map_erase_begin_ptr_guarda) | [🔴 `UB`<br>❌ no detectado](#f_map_erase_begin_ptr_bucle) | [🔴 `UB`<br>❌ no detectado](#f_map_erase_begin_ptr_llamada) |

## Handle: iterador

### f_map_erase_begin_it_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_map_erase_begin_it_recto(std::map<int,int>& c) {
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
    >; _Sequence = std::debug::map<int, int>; _Category = 
    std::forward_iterator_tag; pointer = std::pair<const int, int>*]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fff878444c0 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::map<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7fff878445b0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x62dbafaa1899 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_unique_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x62dbafaa11c9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_unique<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x62dbafa59183 in std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::map(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_map.h:244:14
    #10 0x62dbaf9eeaaa in make_map(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:57:62
    #11 0x62dbafa30362 in main /work/test/runtime_runner.cpp:2782:28
    #12 0x7ed88a3571c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x7ed88a35728a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x62dbaf8764b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3712:12 in f_map_erase_begin_it_recto(std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x7b18895dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b18895dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b18895dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b18895dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b18895dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b18895e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7b18895e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7b18895e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b18895e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b18895e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b18895e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1453==ABORTING
````

</details>

### f_map_erase_begin_it_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_map_erase_begin_it_guarda(std::map<int,int>& c) {
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
    >; _Sequence = std::debug::map<int, int>; _Category = 
    std::forward_iterator_tag; pointer = std::pair<const int, int>*]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fffa893c3e0 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::map<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7fffa893c4d0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
nt> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x5d9142ea7899 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_unique_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x5d9142ea71c9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_unique<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x5d9142e5f183 in std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::map(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_map.h:244:14
    #10 0x5d9142df4aaa in make_map(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:57:62
    #11 0x5d9142e364e1 in main /work/test/runtime_runner.cpp:2787:28
    #12 0x7d7955c1a1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x7d7955c1a28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x5d9142c7c4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3718:12 in f_map_erase_begin_it_guarda(std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x79b954fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x79b954fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x79b954fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x79b954fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x79b954fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x79b954fe0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x79b954fe0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x79b954fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x79b954fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x79b954fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x79b954fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1456==ABORTING
````

</details>

### f_map_erase_begin_it_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_map_erase_begin_it_bucle(std::map<int,int>& c) {
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
    >; _Sequence = std::debug::map<int, int>; _Category = 
    std::forward_iterator_tag; pointer = std::pair<const int, int>*]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffeb6408b50 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::map<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffeb6408c40
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x564cbe541899 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_unique_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x564cbe5411c9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_unique<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x564cbe4f9183 in std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::map(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_map.h:244:14
    #10 0x564cbe48eaaa in make_map(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:57:62
    #11 0x564cbe4d0660 in main /work/test/runtime_runner.cpp:2792:28
    #12 0x77585ab5f1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x77585ab5f28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x564cbe3164b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3724:14 in f_map_erase_begin_it_bucle(std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x739859ddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x739859ddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x739859ddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x739859ddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x739859ddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x739859de0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x739859de0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x739859de0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x739859de0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x739859de0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x739859de0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1459==ABORTING
````

</details>

### f_map_erase_begin_it_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_map_erase_begin_it_llamada(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_map_erase_begin(c);
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
    >; _Sequence = std::debug::map<int, int>; _Category = 
    std::forward_iterator_tag; pointer = std::pair<const int, int>*]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffc50b2c9f0 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::map<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffc50b2cab0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
t> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x628f0bc31899 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_unique_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x628f0bc311c9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_unique<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x628f0bbe9183 in std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::map(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_map.h:244:14
    #10 0x628f0bb7eaaa in make_map(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:57:62
    #11 0x628f0bbc07df in main /work/test/runtime_runner.cpp:2797:28
    #12 0x72750132f1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x72750132f28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x628f0ba064b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3731:12 in f_map_erase_begin_it_llamada(std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x6eb5005dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6eb5005dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6eb5005dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6eb5005dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6eb5005dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6eb5005e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x6eb5005e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x6eb5005e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6eb5005e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6eb5005e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6eb5005e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1462==ABORTING
````

</details>

## Handle: referencia

### f_map_erase_begin_ref_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_map_erase_begin_ref_recto(std::map<int,int>& c) {
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
nt> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x5b3ab5f9a899 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_unique_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x5b3ab5f9a1c9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_unique<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x5b3ab5f52183 in std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::map(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_map.h:244:14
    #10 0x5b3ab5ee7aaa in make_map(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:57:62
    #11 0x5b3ab5f2995e in main /work/test/runtime_runner.cpp:2802:28
    #12 0x7a941f8e61c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x7a941f8e628a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x5b3ab5d6f4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3737:10 in f_map_erase_begin_ref_recto(std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x76d41ebdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x76d41ebdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x76d41ebdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x76d41ebdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x76d41ebdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x76d41ebe0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x76d41ebe0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x76d41ebe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x76d41ebe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x76d41ebe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x76d41ebe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1465==ABORTING
````

</details>

### f_map_erase_begin_ref_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_map_erase_begin_ref_guarda(std::map<int,int>& c) {
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
t> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x5d223f364899 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_unique_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x5d223f3641c9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_unique<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x5d223f31c183 in std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::map(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_map.h:244:14
    #10 0x5d223f2b1aaa in make_map(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:57:62
    #11 0x5d223f2f3add in main /work/test/runtime_runner.cpp:2807:28
    #12 0x76f399ad61c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x76f399ad628a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x5d223f1394b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3744:10 in f_map_erase_begin_ref_guarda(std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x733398ddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x733398ddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x733398ddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x733398ddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x733398ddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x733398de0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x733398de0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x733398de0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x733398de0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x733398de0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x733398de0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1468==ABORTING
````

</details>

### f_map_erase_begin_ref_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `bucle` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_map_erase_begin_ref_bucle(std::map<int,int>& c) {
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
    _Sequence = std::debug::map<int, int>; _Category = 
    std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffeb1002160 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::map<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffeb1002250
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
nt> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x587a90c31899 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_unique_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x587a90c311c9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_unique<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x587a90be9183 in std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::map(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_map.h:244:14
    #10 0x587a90b7eaaa in make_map(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:57:62
    #11 0x587a90bc0c5c in main /work/test/runtime_runner.cpp:2812:28
    #12 0x774be40781c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x774be407828a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x587a90a064b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3751:12 in f_map_erase_begin_ref_bucle(std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x738be33dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x738be33dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x738be33dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x738be33dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x738be33dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x738be33e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x738be33e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x738be33e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x738be33e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x738be33e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x738be33e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1471==ABORTING
````

</details>

### f_map_erase_begin_ref_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_map_erase_begin_ref_llamada(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_map_erase_begin(c);
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
> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x5857140b8899 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_unique_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x5857140b81c9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_unique<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x585714070183 in std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::map(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_map.h:244:14
    #10 0x585714005aaa in make_map(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:57:62
    #11 0x585714047ddb in main /work/test/runtime_runner.cpp:2817:28
    #12 0x7e7b362721c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x7e7b3627228a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x585713e8d4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3759:10 in f_map_erase_begin_ref_llamada(std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x7abb355dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7abb355dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7abb355dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7abb355dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7abb355dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7abb355e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7abb355e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7abb355e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7abb355e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7abb355e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7abb355e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1474==ABORTING
````

</details>

## Handle: puntero

### f_map_erase_begin_ptr_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_map_erase_begin_ptr_recto(std::map<int,int>& c) {
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
nt> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x5c8e7a05f899 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_unique_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x5c8e7a05f1c9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_unique<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x5c8e7a017183 in std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::map(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_map.h:244:14
    #10 0x5c8e79facaaa in make_map(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:57:62
    #11 0x5c8e79feef5a in main /work/test/runtime_runner.cpp:2822:28
    #12 0x71f404f131c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x71f404f1328a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x5c8e79e344b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3765:11 in f_map_erase_begin_ptr_recto(std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x6e34041dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e34041dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e34041dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e34041dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e34041dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6e34041e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x6e34041e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x6e34041e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e34041e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e34041e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e34041e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1477==ABORTING
````

</details>

### f_map_erase_begin_ptr_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_map_erase_begin_ptr_guarda(std::map<int,int>& c) {
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
t> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x637c46c45899 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_unique_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x637c46c451c9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_unique<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x637c46bfd183 in std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::map(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_map.h:244:14
    #10 0x637c46b92aaa in make_map(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:57:62
    #11 0x637c46bd50d9 in main /work/test/runtime_runner.cpp:2827:28
    #12 0x73ca2d7011c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x73ca2d70128a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x637c46a1a4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3772:11 in f_map_erase_begin_ptr_guarda(std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x700a2c9dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x700a2c9dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x700a2c9dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x700a2c9dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x700a2c9dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x700a2c9e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x700a2c9e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x700a2c9e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x700a2c9e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x700a2c9e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x700a2c9e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1480==ABORTING
````

</details>

### f_map_erase_begin_ptr_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `bucle` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_map_erase_begin_ptr_bucle(std::map<int,int>& c) {
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
    _Sequence = std::debug::map<int, int>; _Category = 
    std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fff20b3ec40 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::map<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7fff20b3ed30
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
nt> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x594505fd4899 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_unique_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x594505fd41c9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_unique<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x594505f8c183 in std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::map(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_map.h:244:14
    #10 0x594505f21aaa in make_map(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:57:62
    #11 0x594505f64258 in main /work/test/runtime_runner.cpp:2832:28
    #12 0x7e681f99c1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x7e681f99c28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x594505da94b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3779:13 in f_map_erase_begin_ptr_bucle(std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x7aa81ebdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7aa81ebdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7aa81ebdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7aa81ebdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7aa81ebdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7aa81ebe0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7aa81ebe0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7aa81ebe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7aa81ebe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7aa81ebe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7aa81ebe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1483==ABORTING
````

</details>

### f_map_erase_begin_ptr_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_map_erase_begin_ptr_llamada(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_map_erase_begin(c);
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
> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1831:19
    #7 0x62030bdf6899 in std::_Rb_tree_iterator<std::pair<int const, int>> std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_unique_<std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node>(std::_Rb_tree_const_iterator<std::pair<int const, int>>, std::pair<int const, int> const&, std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_Alloc_node&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:2284:9
    #8 0x62030bdf61c9 in std::enable_if<__same_value_type<std::pair<int const, int> const*>::value, void>::type std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int>>, std::less<int>, std::allocator<std::pair<int const, int>>>::_M_insert_range_unique<std::pair<int const, int> const*>(std::pair<int const, int> const*, std::pair<int const, int> const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_tree.h:1104:6
    #9 0x62030bdae183 in std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>::map(std::initializer_list<std::pair<int const, int>>, std::less<int> const&, std::allocator<std::pair<int const, int>> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_map.h:244:14
    #10 0x62030bd43aaa in make_map(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:57:62
    #11 0x62030bd863d7 in main /work/test/runtime_runner.cpp:2837:28
    #12 0x706f316061c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #13 0x706f3160628a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #14 0x62030bbcb4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:3787:11 in f_map_erase_begin_ptr_llamada(std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int>>>&)
Shadow bytes around the buggy address:
  0x6caf309dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6caf309dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6caf309dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6caf309dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6caf309dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6caf309e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x6caf309e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x6caf309e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6caf309e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6caf309e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6caf309e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1486==ABORTING
````

</details>
