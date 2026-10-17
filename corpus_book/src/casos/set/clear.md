# `std::set::clear`

Mutación: `c.clear();`

- Iterador retenido: 🔴 `UB`
- Referencia/puntero retenido: 🔴 `UB`
- Casos `UB` detectados estáticamente: 4/12

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🔴 avisa](#f_set_clear_it_recto) | [🔴 avisa](#f_set_clear_it_guarda) | [🔴 avisa](#f_set_clear_it_bucle) | [🔴 avisa](#f_set_clear_it_llamada) |
| **referencia** | [🔴 calla](#f_set_clear_ref_recto) | [🔴 calla](#f_set_clear_ref_guarda) | [🔴 calla](#f_set_clear_ref_bucle) | [🔴 calla](#f_set_clear_ref_llamada) |
| **puntero** | [🔴 calla](#f_set_clear_ptr_recto) | [🔴 calla](#f_set_clear_ptr_guarda) | [🔴 calla](#f_set_clear_ptr_bucle) | [🔴 calla](#f_set_clear_ptr_llamada) |

## Handle: iterador

### f_set_clear_it_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `recto` | 🔴 `UB` | ✅ detectado |

```cpp
void f_set_clear_it_recto(std::set<int>& c) {
  auto it = c.begin();
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
/usr/include/c++/16/debug/safe_iterator.h:352:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::reference 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator*() 
    const [with _Iterator = std::_Rb_tree_const_iterator<int>; _Sequence = 
    std::debug::set<int>; _Category = std::forward_iterator_tag; reference = 
    const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffec9aa5bd0 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::set<int, std::less<int>, std::allocator<int> >' @ 0x7ffec9aa5c50
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
9b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x26e19b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55739526a068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d9068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f3169827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f31698278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x5573950312c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x557395196fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5573952c4d64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5573952c49ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5573952e5c88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5573952e5c39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5573952e551f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5573952e4425  (/tmp/mi-linter-runtime-validation/runtime_asan+0x353425) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5573952e3d06  (/tmp/mi-linter-runtime-validation/runtime_asan+0x352d06) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5573952962b3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3052b3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x5573952321ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a11ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55739526a05b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d905b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f3169827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f31698278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x5573950312c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x26e204) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b71689dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b71689dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b71689dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b71689dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b71689dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b71689e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7b71689e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7b71689e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b71689e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b71689e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b71689e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==53==ABORTING
````

</details>

### f_set_clear_it_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `guarda` | 🔴 `UB` | ✅ detectado |

```cpp
void f_set_clear_it_guarda(std::set<int>& c) {
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
/usr/include/c++/16/debug/safe_iterator.h:352:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::reference 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator*() 
    const [with _Iterator = std::_Rb_tree_const_iterator<int>; _Sequence = 
    std::debug::set<int>; _Category = std::forward_iterator_tag; reference = 
    const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffde418b4e0 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::set<int, std::less<int>, std::allocator<int> >' @ 0x7ffde418b5a0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
3e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x26e43e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55b9a647b1a4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d91a4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f8363827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f83638278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55b9a62422c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55b9a63a7fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55b9a64d5d64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55b9a64d59ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55b9a64f6c88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55b9a64f6c39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55b9a64f651f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55b9a64f5425  (/tmp/mi-linter-runtime-validation/runtime_asan+0x353425) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55b9a64f4d06  (/tmp/mi-linter-runtime-validation/runtime_asan+0x352d06) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55b9a64a72b3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3052b3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55b9a64431ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a11ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55b9a647b197  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d9197) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f8363827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f83638278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55b9a62422c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x26e4a7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bc3629dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bc3629dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bc3629dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bc3629dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bc3629dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bc3629e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7bc3629e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7bc3629e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bc3629e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bc3629e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bc3629e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==55==ABORTING
````

</details>

### f_set_clear_it_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ✅ detectado |

```cpp
void f_set_clear_it_bucle(std::set<int>& c) {
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
/usr/include/c++/16/debug/safe_iterator.h:352:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::reference 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator*() 
    const [with _Iterator = std::_Rb_tree_const_iterator<int>; _Sequence = 
    std::debug::set<int>; _Category = std::forward_iterator_tag; reference = 
    const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffd7da17f30 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::set<int, std::less<int>, std::allocator<int> >' @ 0x7ffd7da17ff0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
74  (/tmp/mi-linter-runtime-validation/runtime_asan+0x26e774) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x563ced6b82e0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d92e0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f9113a27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f9113a278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x563ced47f2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x563ced5e4fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x563ced712d64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x563ced7129ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x563ced733c88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x563ced733c39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x563ced73351f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x563ced732425  (/tmp/mi-linter-runtime-validation/runtime_asan+0x353425) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x563ced731d06  (/tmp/mi-linter-runtime-validation/runtime_asan+0x352d06) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x563ced6e42b3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3052b3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x563ced6801ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a11ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x563ced6b82d3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d92d3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f9113a27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f9113a278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x563ced47f2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x26e7dd) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bd112bdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd112bdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd112bdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd112bdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd112bdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bd112be0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7bd112be0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7bd112be0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd112be0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd112be0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd112be0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==57==ABORTING
````

</details>

### f_set_clear_it_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `llamada` | 🔴 `UB` | ✅ detectado |

```cpp
void f_set_clear_it_llamada(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_set_clear(c);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | 🛑 attempt to dereference a singular iterator | 🛑 heap-use-after-free |

<details>
<summary>stderr libstdc++ Debug · <code>natural</code></summary>

````text
/usr/include/c++/16/debug/safe_iterator.h:352:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::reference 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator*() 
    const [with _Iterator = std::_Rb_tree_const_iterator<int>; _Sequence = 
    std::debug::set<int>; _Category = std::forward_iterator_tag; reference = 
    const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fff5a663820 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::set<int, std::less<int>, std::allocator<int> >' @ 0x7fff5a6638e0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x26ea3c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x564c812d041c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d941c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7f67d1c27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7f67d1c278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x564c810972c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x564c811fcfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x564c8132ad64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x564c8132a9ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x564c8134bc88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x564c8134bc39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x564c8134b51f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x564c8134a425  (/tmp/mi-linter-runtime-validation/runtime_asan+0x353425) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x564c81349d06  (/tmp/mi-linter-runtime-validation/runtime_asan+0x352d06) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x564c812fc2b3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3052b3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x564c812981ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a11ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x564c812d040f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d940f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f67d1c27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f67d1c278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x564c810972c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x26eaa5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7ba7d0ddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ba7d0ddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ba7d0ddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ba7d0ddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ba7d0ddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7ba7d0de0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7ba7d0de0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7ba7d0de0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ba7d0de0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ba7d0de0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ba7d0de0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==59==ABORTING
````

</details>

## Handle: referencia

### f_set_clear_ref_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `recto` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_set_clear_ref_recto(std::set<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.clear();
  sink(h);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | 🛑 heap-use-after-free |

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
b7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x26ecb7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x560a5fc24558  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d9558) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f6e85427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f6e854278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x560a5f9eb2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x560a5fb50fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x560a5fc7ed64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x560a5fc7e9ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x560a5fc9fc88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x560a5fc9fc39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x560a5fc9f51f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x560a5fc9e425  (/tmp/mi-linter-runtime-validation/runtime_asan+0x353425) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x560a5fc9dd06  (/tmp/mi-linter-runtime-validation/runtime_asan+0x352d06) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x560a5fc502b3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3052b3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x560a5fbec1ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a11ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x560a5fc2454b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d954b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f6e85427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f6e854278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x560a5f9eb2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x26ecec) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bae845dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bae845dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bae845dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bae845dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bae845dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bae845e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7bae845e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7bae845e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bae845e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bae845e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bae845e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==61==ABORTING
````

</details>

### f_set_clear_ref_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `guarda` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_set_clear_ref_guarda(std::set<int>& c) {
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
| `natural` | estado inicial ordinario | — (código 0) | 🛑 heap-use-after-free |

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
73  (/tmp/mi-linter-runtime-validation/runtime_asan+0x26ef73) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x56360e2fc694  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d9694) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f5687027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f56870278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x56360e0c32c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x56360e228fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x56360e356d64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x56360e3569ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x56360e377c88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x56360e377c39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x56360e37751f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x56360e376425  (/tmp/mi-linter-runtime-validation/runtime_asan+0x353425) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x56360e375d06  (/tmp/mi-linter-runtime-validation/runtime_asan+0x352d06) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x56360e3282b3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3052b3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x56360e2c41ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a11ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x56360e2fc687  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d9687) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f5687027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f56870278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x56360e0c32c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x26efab) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b96861dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b96861dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b96861dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b96861dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b96861dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b96861e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7b96861e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7b96861e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b96861e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b96861e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b96861e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==63==ABORTING
````

</details>

### f_set_clear_ref_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_set_clear_ref_bucle(std::set<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.clear();
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
/usr/include/c++/16/debug/safe_iterator.h:392:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>& 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator++() 
    [with _Iterator = std::_Rb_tree_const_iterator<int>; _Sequence = std::
    debug::set<int>; _Category = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fff841a46f0 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::set<int, std::less<int>, std::allocator<int> >' @ 0x7fff841a47b0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
ae  (/tmp/mi-linter-runtime-validation/runtime_asan+0x26f2ae) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5600d7b6e7d0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d97d0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f21d7627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f21d76278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x5600d79352c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5600d7a9afe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5600d7bc8d64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5600d7bc89ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5600d7be9c88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5600d7be9c39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5600d7be951f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5600d7be8425  (/tmp/mi-linter-runtime-validation/runtime_asan+0x353425) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5600d7be7d06  (/tmp/mi-linter-runtime-validation/runtime_asan+0x352d06) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5600d7b9a2b3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3052b3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x5600d7b361ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a11ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x5600d7b6e7c3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d97c3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f21d7627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f21d76278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x5600d79352c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x26f2e6) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b61d67dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b61d67dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b61d67dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b61d67dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b61d67dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b61d67e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7b61d67e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7b61d67e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b61d67e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b61d67e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b61d67e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==65==ABORTING
````

</details>

### f_set_clear_ref_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `llamada` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_set_clear_ref_llamada(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_set_clear(c);
  sink(h);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | 🛑 heap-use-after-free |

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x26f5a1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55b75691d90c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d990c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7fdb7a227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7fdb7a2278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x55b7566e42c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55b756849fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55b756977d64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55b7569779ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55b756998c88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55b756998c39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55b75699851f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55b756997425  (/tmp/mi-linter-runtime-validation/runtime_asan+0x353425) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55b756996d06  (/tmp/mi-linter-runtime-validation/runtime_asan+0x352d06) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55b7569492b3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3052b3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55b7568e51ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a11ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55b75691d8ff  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d98ff) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7fdb7a227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7fdb7a2278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55b7566e42c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x26f5d9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c1b793dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c1b793dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c1b793dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c1b793dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c1b793dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c1b793e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7c1b793e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7c1b793e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c1b793e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c1b793e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c1b793e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==67==ABORTING
````

</details>

## Handle: puntero

### f_set_clear_ptr_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `recto` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_set_clear_ptr_recto(std::set<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.clear();
  sink(*h);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | 🛑 heap-use-after-free |

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
b4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x26f7b4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x560e95a6fa48  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d9a48) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fe59bc27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fe59bc278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x560e958362c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x560e9599bfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x560e95ac9d64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x560e95ac99ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x560e95aeac88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x560e95aeac39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x560e95aea51f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x560e95ae9425  (/tmp/mi-linter-runtime-validation/runtime_asan+0x353425) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x560e95ae8d06  (/tmp/mi-linter-runtime-validation/runtime_asan+0x352d06) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x560e95a9b2b3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3052b3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x560e95a371ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a11ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x560e95a6fa3b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d9a3b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7fe59bc27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7fe59bc278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x560e958362c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x26f815) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c259addfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c259addfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c259addfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c259addff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c259addff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c259ade0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7c259ade0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7c259ade0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c259ade0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c259ade0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c259ade0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==69==ABORTING
````

</details>

### f_set_clear_ptr_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `guarda` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_set_clear_ptr_guarda(std::set<int>& c) {
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
| `natural` | estado inicial ordinario | — (código 0) | 🛑 heap-use-after-free |

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
5b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x26fa5b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5634396d4b84  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d9b84) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f7dbfc27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f7dbfc278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x56343949b2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x563439600fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x56343972ed64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x56343972e9ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x56343974fc88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x56343974fc39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x56343974f51f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x56343974e425  (/tmp/mi-linter-runtime-validation/runtime_asan+0x353425) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x56343974dd06  (/tmp/mi-linter-runtime-validation/runtime_asan+0x352d06) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5634397002b3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3052b3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x56343969c1ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a11ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x5634396d4b77  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d9b77) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f7dbfc27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f7dbfc278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x56343949b2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x26fabc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bbdbeddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bbdbeddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bbdbeddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bbdbeddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bbdbeddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bbdbede0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7bbdbede0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7bbdbede0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bbdbede0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bbdbede0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bbdbede0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==71==ABORTING
````

</details>

### f_set_clear_ptr_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_set_clear_ptr_bucle(std::set<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.clear();
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
/usr/include/c++/16/debug/safe_iterator.h:392:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>& 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator++() 
    [with _Iterator = std::_Rb_tree_const_iterator<int>; _Sequence = std::
    debug::set<int>; _Category = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fff11aa4de0 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::set<int, std::less<int>, std::allocator<int> >' @ 0x7fff11aa4ea0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
8b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x26fd8b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x563322218cc0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d9cc0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f2d63c27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f2d63c278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x563321fdf2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x563322144fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x563322272d64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5633222729ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x563322293c88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x563322293c39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x56332229351f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x563322292425  (/tmp/mi-linter-runtime-validation/runtime_asan+0x353425) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x563322291d06  (/tmp/mi-linter-runtime-validation/runtime_asan+0x352d06) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5633222442b3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3052b3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x5633221e01ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a11ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x563322218cb3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d9cb3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f2d63c27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f2d63c278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x563321fdf2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x26fdef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b6d62ddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b6d62ddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b6d62ddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b6d62ddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b6d62ddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b6d62de0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7b6d62de0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7b6d62de0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b6d62de0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b6d62de0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b6d62de0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==73==ABORTING
````

</details>

### f_set_clear_ptr_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `llamada` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_set_clear_ptr_llamada(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_set_clear(c);
  sink(*h);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | 🛑 heap-use-after-free |

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
9  (/tmp/mi-linter-runtime-validation/runtime_asan+0x270059) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x5604e3412dfc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d9dfc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7f5437a27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7f5437a278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x5604e31d92c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5604e333efe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5604e346cd64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5604e346c9ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5604e348dc88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5604e348dc39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5604e348d51f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5604e348c425  (/tmp/mi-linter-runtime-validation/runtime_asan+0x353425) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5604e348bd06  (/tmp/mi-linter-runtime-validation/runtime_asan+0x352d06) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5604e343e2b3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3052b3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x5604e33da1ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a11ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x5604e3412def  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d9def) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f5437a27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f5437a278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x5604e31d92c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x2700ba) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b9436bdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9436bdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9436bdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9436bdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9436bdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b9436be0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7b9436be0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7b9436be0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b9436be0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b9436be0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b9436be0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==75==ABORTING
````

</details>
