# `std::map::erase_begin`

Mutación: `c.erase(c.begin());`

- Iterador retenido: 🔴 `UB`
- Referencia/puntero retenido: 🔴 `UB`
- Casos `UB` detectados estáticamente: 4/12

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🔴 avisa](#f_map_erase_begin_it_recto) | [🔴 avisa](#f_map_erase_begin_it_guarda) | [🔴 avisa](#f_map_erase_begin_it_bucle) | [🔴 avisa](#f_map_erase_begin_it_llamada) |
| **referencia** | [🔴 calla](#f_map_erase_begin_ref_recto) | [🔴 calla](#f_map_erase_begin_ref_guarda) | [🔴 calla](#f_map_erase_begin_ref_bucle) | [🔴 calla](#f_map_erase_begin_ref_llamada) |
| **puntero** | [🔴 calla](#f_map_erase_begin_ptr_recto) | [🔴 calla](#f_map_erase_begin_ptr_guarda) | [🔴 calla](#f_map_erase_begin_ptr_bucle) | [🔴 calla](#f_map_erase_begin_ptr_llamada) |

## Handle: iterador

### f_map_erase_begin_it_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `recto` | 🔴 `UB` | ✅ detectado |

```cpp
void f_map_erase_begin_it_recto(std::map<int,int>& c) {
  auto it = c.begin();
  c.erase(c.begin());
  sink(it->second);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | 🛑 attempt to dereference a singular iterator | 🛑 heap-use-after-free |

<details>
<summary>stderr libstdc++ Debug · <code>natural</code></summary>

````text
/usr/include/c++/16/debug/safe_iterator.h:370:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::pointer 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator->() 
    const [with _Iterator = std::_Rb_tree_iterator<std::pair<const int, int> 
    >; _Sequence = std::debug::map<int, int>; _Category = 
    std::forward_iterator_tag; pointer = std::pair<const int, int>*]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffec980d2a0 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::map<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffec980d390
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x27e343) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55bda74297cc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e07cc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fd5eec27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fd5eec278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55bda71e92c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55bda734efe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55bda74816c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55bda74813cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55bda74a1068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55bda74a1019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55bda74a0caf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55bda74a08a5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3578a5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55bda74a01a6  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3571a6) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55bda744ebb3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305bb3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55bda73ea9f4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a19f4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55bda74297bf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e07bf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7fd5eec27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7fd5eec278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55bda71e92c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x27e3e4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c15edddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c15edddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c15edddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c15edddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c15edddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c15edde0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7c15edde0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7c15edde0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c15edde0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c15edde0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c15edde0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==221==ABORTING
````

</details>

### f_map_erase_begin_it_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `guarda` | 🔴 `UB` | ✅ detectado |

```cpp
void f_map_erase_begin_it_guarda(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.erase(c.begin());
  sink(it->second);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | 🛑 attempt to dereference a singular iterator | 🛑 heap-use-after-free |

<details>
<summary>stderr libstdc++ Debug · <code>natural</code></summary>

````text
/usr/include/c++/16/debug/safe_iterator.h:370:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::pointer 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator->() 
    const [with _Iterator = std::_Rb_tree_iterator<std::pair<const int, int> 
    >; _Sequence = std::debug::map<int, int>; _Category = 
    std::forward_iterator_tag; pointer = std::pair<const int, int>*]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fff9bd6db60 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::map<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7fff9bd6dc50
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x27e64d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x56407857794b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e094b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7ff619627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7ff6196278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x5640783372c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x56407849cfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5640785cf6c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5640785cf3cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5640785ef068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5640785ef019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5640785eecaf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5640785ee8a5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3578a5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5640785ee1a6  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3571a6) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x56407859cbb3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305bb3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x5640785389f4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a19f4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x56407857793e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e093e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7ff619627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7ff6196278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x5640783372c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x27e6f1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c36187dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c36187dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c36187dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c36187dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c36187dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c36187e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7c36187e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7c36187e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c36187e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c36187e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c36187e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==223==ABORTING
````

</details>

### f_map_erase_begin_it_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ✅ detectado |

```cpp
void f_map_erase_begin_it_bucle(std::map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.erase(c.begin());
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
/usr/include/c++/16/debug/safe_iterator.h:370:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::pointer 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator->() 
    const [with _Iterator = std::_Rb_tree_iterator<std::pair<const int, int> 
    >; _Sequence = std::debug::map<int, int>; _Category = 
    std::forward_iterator_tag; pointer = std::pair<const int, int>*]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffcc5230950 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::map<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffcc5230a40
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x27e9f0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55cd1fae7aca  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e0aca) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f1064227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f10642278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55cd1f8a72c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55cd1fa0cfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55cd1fb3f6c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55cd1fb3f3cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55cd1fb5f068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55cd1fb5f019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55cd1fb5ecaf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55cd1fb5e8a5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3578a5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55cd1fb5e1a6  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3571a6) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55cd1fb0cbb3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305bb3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55cd1faa89f4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a19f4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55cd1fae7abd  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e0abd) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f1064227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f10642278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55cd1f8a72c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x27ea94) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b50633dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b50633dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b50633dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b50633dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b50633dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b50633e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7b50633e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7b50633e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b50633e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b50633e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b50633e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==225==ABORTING
````

</details>

### f_map_erase_begin_it_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `llamada` | 🔴 `UB` | ✅ detectado |

```cpp
void f_map_erase_begin_it_llamada(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_map_erase_begin(c);
  sink(it->second);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | 🛑 attempt to dereference a singular iterator | 🛑 heap-use-after-free |

<details>
<summary>stderr libstdc++ Debug · <code>natural</code></summary>

````text
/usr/include/c++/16/debug/safe_iterator.h:370:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::pointer 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator->() 
    const [with _Iterator = std::_Rb_tree_iterator<std::pair<const int, int> 
    >; _Sequence = std::debug::map<int, int>; _Category = 
    std::forward_iterator_tag; pointer = std::pair<const int, int>*]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffd752215c0 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::map<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffd75221680
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
  (/tmp/mi-linter-runtime-validation/runtime_asan+0x27ece0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x562cb6feec49  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e0c49) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7f3f00227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7f3f002278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x562cb6dae2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x562cb6f13fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x562cb70466c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x562cb70463cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x562cb7066068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x562cb7066019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x562cb7065caf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x562cb70658a5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3578a5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x562cb70651a6  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3571a6) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x562cb7013bb3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305bb3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x562cb6faf9f4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a19f4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x562cb6feec3c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e0c3c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f3f00227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f3f002278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x562cb6dae2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x27ed7d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b7eff3dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b7eff3dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b7eff3dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b7eff3dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b7eff3dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b7eff3e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7b7eff3e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7b7eff3e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b7eff3e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b7eff3e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b7eff3e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==227==ABORTING
````

</details>

## Handle: referencia

### f_map_erase_begin_ref_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `recto` | 🔴 `UB` | ❌ falso negativo |

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
| `natural` | estado inicial ordinario | — (código 0) | 🛑 heap-use-after-free |

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x27efc1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x555b19394dc8  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e0dc8) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f9147e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f9147e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x555b191542c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x555b192b9fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x555b193ec6c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x555b193ec3cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x555b1940c068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x555b1940c019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x555b1940bcaf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x555b1940b8a5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3578a5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x555b1940b1a6  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3571a6) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x555b193b9bb3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305bb3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x555b193559f4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a19f4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x555b19394dbb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e0dbb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f9147e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f9147e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x555b191542c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x27f022) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bd146fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd146fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd146fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd146fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd146fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bd146fe0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7bd146fe0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7bd146fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd146fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd146fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd146fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==229==ABORTING
````

</details>

### f_map_erase_begin_ref_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `guarda` | 🔴 `UB` | ❌ falso negativo |

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
| `natural` | estado inicial ordinario | — (código 0) | 🛑 heap-use-after-free |

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x27f2d0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55d1b7e73f47  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e0f47) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f50f6c27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f50f6c278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55d1b7c332c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55d1b7d98fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55d1b7ecb6c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55d1b7ecb3cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55d1b7eeb068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55d1b7eeb019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55d1b7eeacaf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55d1b7eea8a5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3578a5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55d1b7eea1a6  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3571a6) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55d1b7e98bb3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305bb3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55d1b7e349f4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a19f4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55d1b7e73f3a  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e0f3a) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f50f6c27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f50f6c278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55d1b7c332c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x27f32e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b90f5ddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b90f5ddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b90f5ddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b90f5ddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b90f5ddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b90f5de0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7b90f5de0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7b90f5de0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b90f5de0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b90f5de0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b90f5de0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==231==ABORTING
````

</details>

### f_map_erase_begin_ref_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `bucle` | 🔴 `UB` | ❌ falso negativo |

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
/usr/include/c++/16/debug/safe_iterator.h:392:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>& 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator++() 
    [with _Iterator = std::_Rb_tree_iterator<std::pair<const int, int> >; 
    _Sequence = std::debug::map<int, int>; _Category = 
    std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fffcd0e85a0 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::map<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7fffcd0e8690
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x27f660) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55d563e490c6  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e10c6) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fc3e1427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fc3e14278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55d563c082c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55d563d6dfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55d563ea06c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55d563ea03cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55d563ec0068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55d563ec0019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55d563ebfcaf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55d563ebf8a5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3578a5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55d563ebf1a6  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3571a6) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55d563e6dbb3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305bb3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55d563e099f4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a19f4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55d563e490b9  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e10b9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7fc3e1427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7fc3e14278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55d563c082c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x27f6c1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c03e05dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c03e05dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c03e05dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c03e05dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c03e05dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c03e05e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7c03e05e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7c03e05e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c03e05e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c03e05e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c03e05e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==233==ABORTING
````

</details>

### f_map_erase_begin_ref_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `llamada` | 🔴 `UB` | ❌ falso negativo |

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
| `natural` | estado inicial ordinario | — (código 0) | 🛑 heap-use-after-free |

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
  (/tmp/mi-linter-runtime-validation/runtime_asan+0x27f955) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55b60e688245  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e1245) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7f15b6027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7f15b60278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x55b60e4472c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55b60e5acfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55b60e6df6c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55b60e6df3cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55b60e6ff068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55b60e6ff019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55b60e6fecaf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55b60e6fe8a5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3578a5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55b60e6fe1a6  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3571a6) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55b60e6acbb3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305bb3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55b60e6489f4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a19f4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55b60e688238  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e1238) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f15b6027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f15b60278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55b60e4472c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x27f9af) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b55b51dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b55b51dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b55b51dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b55b51dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b55b51dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b55b51e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7b55b51e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7b55b51e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b55b51e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b55b51e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b55b51e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==235==ABORTING
````

</details>

## Handle: puntero

### f_map_erase_begin_ptr_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `recto` | 🔴 `UB` | ❌ falso negativo |

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
| `natural` | estado inicial ordinario | — (código 0) | 🛑 heap-use-after-free |

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x27fbce) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55ea238ae3c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e13c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f26dee27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f26dee278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55ea2366d2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55ea237d2fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55ea239056c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55ea239053cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55ea23925068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55ea23925019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55ea23924caf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55ea239248a5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3578a5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55ea239241a6  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3571a6) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55ea238d2bb3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305bb3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55ea2386e9f4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a19f4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55ea238ae3b7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e13b7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f26dee27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f26dee278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55ea2366d2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x27fc6d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b66ddfdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b66ddfdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b66ddfdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b66ddfdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b66ddfdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b66ddfe0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7b66ddfe0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7b66ddfe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b66ddfe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b66ddfe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b66ddfe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==237==ABORTING
````

</details>

### f_map_erase_begin_ptr_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `guarda` | 🔴 `UB` | ❌ falso negativo |

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
| `natural` | estado inicial ordinario | — (código 0) | 🛑 heap-use-after-free |

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x27fedd) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x56133a9de543  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e1543) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f7ce4227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f7ce42278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x56133a79d2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x56133a902fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x56133aa356c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x56133aa353cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x56133aa55068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x56133aa55019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x56133aa54caf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x56133aa548a5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3578a5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x56133aa541a6  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3571a6) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x56133aa02bb3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305bb3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x56133a99e9f4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a19f4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x56133a9de536  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e1536) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f7ce4227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f7ce42278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x56133a79d2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x27ff79) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bbce33dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bbce33dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bbce33dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bbce33dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bbce33dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bbce33e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7bbce33e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7bbce33e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bbce33e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bbce33e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bbce33e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==239==ABORTING
````

</details>

### f_map_erase_begin_ptr_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `bucle` | 🔴 `UB` | ❌ falso negativo |

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
/usr/include/c++/16/debug/safe_iterator.h:392:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>& 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator++() 
    [with _Iterator = std::_Rb_tree_iterator<std::pair<const int, int> >; 
    _Sequence = std::debug::map<int, int>; _Category = 
    std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffdb27d34d0 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::map<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffdb27d35c0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x28027d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5594c0f936c2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e16c2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f80dec27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f80dec278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x5594c0d522c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5594c0eb7fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5594c0fea6c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5594c0fea3cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5594c100a068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5594c100a019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5594c1009caf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5594c10098a5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3578a5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5594c10091a6  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3571a6) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5594c0fb7bb3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305bb3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x5594c0f539f4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a19f4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x5594c0f936b5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e16b5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f80dec27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f80dec278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x5594c0d522c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x28031c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bc0ddddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bc0ddddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bc0ddddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bc0ddddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bc0ddddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bc0ddde0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7bc0ddde0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7bc0ddde0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bc0ddde0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bc0ddde0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bc0ddde0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==241==ABORTING
````

</details>

### f_map_erase_begin_ptr_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `llamada` | 🔴 `UB` | ❌ falso negativo |

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
| `natural` | estado inicial ordinario | — (código 0) | 🛑 heap-use-after-free |

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
  (/tmp/mi-linter-runtime-validation/runtime_asan+0x280582) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x563ca581f841  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e1841) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7f113d227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7f113d2278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x563ca55de2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x563ca5743fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x563ca58766c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x563ca58763cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x563ca5896068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x563ca5896019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x563ca5895caf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x563ca58958a5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3578a5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x563ca58951a6  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3571a6) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x563ca5843bb3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305bb3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x563ca57df9f4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a19f4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x563ca581f834  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e1834) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f113d227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f113d2278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x563ca55de2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x28061a) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b513c3dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b513c3dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b513c3dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b513c3dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b513c3dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b513c3e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7b513c3e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7b513c3e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b513c3e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b513c3e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b513c3e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==243==ABORTING
````

</details>
