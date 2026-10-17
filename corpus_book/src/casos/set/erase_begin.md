# `std::set::erase_begin`

Mutación: `c.erase(c.begin());`

- Iterador retenido: 🔴 `UB`
- Referencia/puntero retenido: 🔴 `UB`
- Casos `UB` detectados estáticamente: 4/12

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🔴 avisa](#f_set_erase_begin_it_recto) | [🔴 avisa](#f_set_erase_begin_it_guarda) | [🔴 avisa](#f_set_erase_begin_it_bucle) | [🔴 avisa](#f_set_erase_begin_it_llamada) |
| **referencia** | [🔴 calla](#f_set_erase_begin_ref_recto) | [🔴 calla](#f_set_erase_begin_ref_guarda) | [🔴 calla](#f_set_erase_begin_ref_bucle) | [🔴 calla](#f_set_erase_begin_ref_llamada) |
| **puntero** | [🔴 calla](#f_set_erase_begin_ptr_recto) | [🔴 calla](#f_set_erase_begin_ptr_guarda) | [🔴 calla](#f_set_erase_begin_ptr_bucle) | [🔴 calla](#f_set_erase_begin_ptr_llamada) |

## Handle: iterador

### f_set_erase_begin_it_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `recto` | 🔴 `UB` | ✅ detectado |

```cpp
void f_set_erase_begin_it_recto(std::set<int>& c) {
  auto it = c.begin();
  c.erase(c.begin());
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
    iterator "this" @ 0x7ffeae2f2390 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::set<int, std::less<int>, std::allocator<int> >' @ 0x7ffeae2f2480
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x26bdef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x557425b6be74  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d7e74) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f078b027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f078b0278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x5574259342c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x557425a99fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x557425bc7d64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x557425bc79ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x557425be8c88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x557425be8c39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x557425be851f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x557425be7425  (/tmp/mi-linter-runtime-validation/runtime_asan+0x353425) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x557425be6d06  (/tmp/mi-linter-runtime-validation/runtime_asan+0x352d06) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x557425b992b3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3052b3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x557425b351ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a11ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x557425b6be67  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d7e67) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f078b027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f078b0278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x5574259342c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x26be5c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b478a1dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b478a1dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b478a1dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b478a1dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b478a1dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b478a1e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7b478a1e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7b478a1e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b478a1e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b478a1e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b478a1e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==29==ABORTING
````

</details>

### f_set_erase_begin_it_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `guarda` | 🔴 `UB` | ✅ detectado |

```cpp
void f_set_erase_begin_it_guarda(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.erase(c.begin());
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
    iterator "this" @ 0x7ffdbf5e5770 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::set<int, std::less<int>, std::allocator<int> >' @ 0x7ffdbf5e5860
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
e7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x26c0e7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55ca6490fff3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d7ff3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f5e6c827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f5e6c8278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55ca646d82c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55ca6483dfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55ca6496bd64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55ca6496b9ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55ca6498cc88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55ca6498cc39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55ca6498c51f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55ca6498b425  (/tmp/mi-linter-runtime-validation/runtime_asan+0x353425) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55ca6498ad06  (/tmp/mi-linter-runtime-validation/runtime_asan+0x352d06) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55ca6493d2b3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3052b3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55ca648d91ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a11ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55ca6490ffe6  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d7fe6) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f5e6c827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f5e6c8278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55ca646d82c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x26c157) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b9e6b9dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9e6b9dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9e6b9dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9e6b9dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9e6b9dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b9e6b9e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7b9e6b9e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7b9e6b9e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b9e6b9e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b9e6b9e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b9e6b9e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==31==ABORTING
````

</details>

### f_set_erase_begin_it_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ✅ detectado |

```cpp
void f_set_erase_begin_it_bucle(std::set<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.erase(c.begin());
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
    iterator "this" @ 0x7fff838fb780 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::set<int, std::less<int>, std::allocator<int> >' @ 0x7fff838fb870
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
62  (/tmp/mi-linter-runtime-validation/runtime_asan+0x26c462) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55cb38baa172  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d8172) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fb75f427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fb75f4278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55cb389722c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55cb38ad7fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55cb38c05d64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55cb38c059ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55cb38c26c88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55cb38c26c39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55cb38c2651f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55cb38c25425  (/tmp/mi-linter-runtime-validation/runtime_asan+0x353425) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55cb38c24d06  (/tmp/mi-linter-runtime-validation/runtime_asan+0x352d06) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55cb38bd72b3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3052b3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55cb38b731ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a11ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55cb38baa165  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d8165) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7fb75f427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7fb75f4278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55cb389722c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x26c4d2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bf75e5dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf75e5dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf75e5dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf75e5dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf75e5dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bf75e5e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7bf75e5e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7bf75e5e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf75e5e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf75e5e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf75e5e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==33==ABORTING
````

</details>

### f_set_erase_begin_it_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `llamada` | 🔴 `UB` | ✅ detectado |

```cpp
void f_set_erase_begin_it_llamada(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_set_erase_begin(c);
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
    iterator "this" @ 0x7ffcedee3050 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::set<int, std::less<int>, std::allocator<int> >' @ 0x7ffcedee3110
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x26c72c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x56538039d2f1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d82f1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7f7260027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7f72600278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x5653801652c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5653802cafe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5653803f8d64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5653803f89ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x565380419c88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x565380419c39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x56538041951f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x565380418425  (/tmp/mi-linter-runtime-validation/runtime_asan+0x353425) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x565380417d06  (/tmp/mi-linter-runtime-validation/runtime_asan+0x352d06) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5653803ca2b3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3052b3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x5653803661ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a11ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x56538039d2e4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d82e4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f7260027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f72600278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x5653801652c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x26c795) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bb25f1dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bb25f1dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bb25f1dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bb25f1dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bb25f1dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bb25f1e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7bb25f1e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7bb25f1e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bb25f1e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bb25f1e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bb25f1e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==35==ABORTING
````

</details>

## Handle: referencia

### f_set_erase_begin_ref_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `recto` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_set_erase_begin_ref_recto(std::set<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.erase(c.begin());
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
fd  (/tmp/mi-linter-runtime-validation/runtime_asan+0x26c9fd) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5640b3462470  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d8470) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fdaa7e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fdaa7e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x5640b322a2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5640b338ffe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5640b34bdd64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5640b34bd9ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5640b34dec88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5640b34dec39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5640b34de51f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5640b34dd425  (/tmp/mi-linter-runtime-validation/runtime_asan+0x353425) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5640b34dcd06  (/tmp/mi-linter-runtime-validation/runtime_asan+0x352d06) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5640b348f2b3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3052b3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x5640b342b1ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a11ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x5640b3462463  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d8463) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7fdaa7e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7fdaa7e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x5640b322a2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x26ca3c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c1aa6fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c1aa6fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c1aa6fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c1aa6fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c1aa6fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c1aa6fe0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7c1aa6fe0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7c1aa6fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c1aa6fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c1aa6fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c1aa6fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==37==ABORTING
````

</details>

### f_set_erase_begin_ref_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `guarda` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_set_erase_begin_ref_guarda(std::set<int>& c) {
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
| `natural` | estado inicial ordinario | — (código 0) | 🛑 heap-use-after-free |

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
0a  (/tmp/mi-linter-runtime-validation/runtime_asan+0x26cd0a) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x560c99dd95ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d85ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f796ea27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f796ea278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x560c99ba12c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x560c99d06fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x560c99e34d64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x560c99e349ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x560c99e55c88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x560c99e55c39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x560c99e5551f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x560c99e54425  (/tmp/mi-linter-runtime-validation/runtime_asan+0x353425) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x560c99e53d06  (/tmp/mi-linter-runtime-validation/runtime_asan+0x352d06) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x560c99e062b3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3052b3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x560c99da21ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a11ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x560c99dd95e2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d85e2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f796ea27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f796ea278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x560c99ba12c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x26cd43) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bb96dbdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bb96dbdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bb96dbdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bb96dbdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bb96dbdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bb96dbe0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7bb96dbe0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7bb96dbe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bb96dbe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bb96dbe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bb96dbe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==39==ABORTING
````

</details>

### f_set_erase_begin_ref_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_set_erase_begin_ref_bucle(std::set<int>& c) {
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
/usr/include/c++/16/debug/safe_iterator.h:392:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>& 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator++() 
    [with _Iterator = std::_Rb_tree_const_iterator<int>; _Sequence = std::
    debug::set<int>; _Category = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffe192d4540 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::set<int, std::less<int>, std::allocator<int> >' @ 0x7ffe192d4630
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
aa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x26d0aa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55b8e97ac76e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d876e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7feb5e227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7feb5e2278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55b8e95742c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55b8e96d9fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55b8e9807d64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55b8e98079ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55b8e9828c88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55b8e9828c39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55b8e982851f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55b8e9827425  (/tmp/mi-linter-runtime-validation/runtime_asan+0x353425) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55b8e9826d06  (/tmp/mi-linter-runtime-validation/runtime_asan+0x352d06) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55b8e97d92b3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3052b3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55b8e97751ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a11ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55b8e97ac761  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d8761) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7feb5e227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7feb5e2278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55b8e95742c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x26d0e9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c2b5d3dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c2b5d3dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c2b5d3dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c2b5d3dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c2b5d3dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c2b5d3e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7c2b5d3e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7c2b5d3e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c2b5d3e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c2b5d3e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c2b5d3e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==41==ABORTING
````

</details>

### f_set_erase_begin_ref_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `llamada` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_set_erase_begin_ref_llamada(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_set_erase_begin(c);
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
1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x26d3a1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55abcc5188ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d88ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7f8a35827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7f8a358278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x55abcc2e02c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55abcc445fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55abcc573d64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55abcc5739ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55abcc594c88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55abcc594c39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55abcc59451f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55abcc593425  (/tmp/mi-linter-runtime-validation/runtime_asan+0x353425) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55abcc592d06  (/tmp/mi-linter-runtime-validation/runtime_asan+0x352d06) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55abcc5452b3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3052b3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55abcc4e11ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a11ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55abcc5188e0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d88e0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f8a35827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f8a358278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55abcc2e02c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x26d3d9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bca349dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bca349dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bca349dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bca349dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bca349dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bca349e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7bca349e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7bca349e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bca349e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bca349e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bca349e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==43==ABORTING
````

</details>

## Handle: puntero

### f_set_erase_begin_ptr_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `recto` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_set_erase_begin_ptr_recto(std::set<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.erase(c.begin());
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
f5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x26d5f5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5628b14c2a6c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d8a6c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f6bbfc27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f6bbfc278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x5628b128a2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5628b13effe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5628b151dd64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5628b151d9ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5628b153ec88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5628b153ec39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5628b153e51f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5628b153d425  (/tmp/mi-linter-runtime-validation/runtime_asan+0x353425) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5628b153cd06  (/tmp/mi-linter-runtime-validation/runtime_asan+0x352d06) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5628b14ef2b3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3052b3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x5628b148b1ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a11ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x5628b14c2a5f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d8a5f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f6bbfc27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f6bbfc278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x5628b128a2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x26d65a) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7babbeddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7babbeddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7babbeddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7babbeddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7babbeddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7babbede0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7babbede0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7babbede0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7babbede0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7babbede0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7babbede0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==45==ABORTING
````

</details>

### f_set_erase_begin_ptr_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `guarda` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_set_erase_begin_ptr_guarda(std::set<int>& c) {
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
| `natural` | estado inicial ordinario | — (código 0) | 🛑 heap-use-after-free |

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
f7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x26d8f7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55b800bf7beb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d8beb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fb1cbc27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fb1cbc278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55b8009bf2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55b800b24fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55b800c52d64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55b800c529ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55b800c73c88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55b800c73c39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55b800c7351f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55b800c72425  (/tmp/mi-linter-runtime-validation/runtime_asan+0x353425) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55b800c71d06  (/tmp/mi-linter-runtime-validation/runtime_asan+0x352d06) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55b800c242b3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3052b3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55b800bc01ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a11ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55b800bf7bde  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d8bde) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7fb1cbc27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7fb1cbc278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55b8009bf2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x26d95f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bf1caddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf1caddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf1caddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf1caddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf1caddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bf1cade0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7bf1cade0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7bf1cade0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf1cade0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf1cade0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf1cade0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==47==ABORTING
````

</details>

### f_set_erase_begin_ptr_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_set_erase_begin_ptr_bucle(std::set<int>& c) {
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
/usr/include/c++/16/debug/safe_iterator.h:392:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>& 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator++() 
    [with _Iterator = std::_Rb_tree_const_iterator<int>; _Sequence = std::
    debug::set<int>; _Category = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffeb9280bc0 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::set<int, std::less<int>, std::allocator<int> >' @ 0x7ffeb9280cb0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
97  (/tmp/mi-linter-runtime-validation/runtime_asan+0x26dc97) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55b47cbf1d6a  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d8d6a) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f0555e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f0555e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55b47c9b92c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55b47cb1efe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55b47cc4cd64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55b47cc4c9ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55b47cc6dc88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55b47cc6dc39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55b47cc6d51f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55b47cc6c425  (/tmp/mi-linter-runtime-validation/runtime_asan+0x353425) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55b47cc6bd06  (/tmp/mi-linter-runtime-validation/runtime_asan+0x352d06) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55b47cc1e2b3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3052b3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55b47cbba1ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a11ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55b47cbf1d5d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d8d5d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f0555e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f0555e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55b47c9b92c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x26dd02) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b4554fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b4554fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b4554fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b4554fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b4554fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b4554fe0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7b4554fe0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7b4554fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b4554fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b4554fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b4554fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==49==ABORTING
````

</details>

### f_set_erase_begin_ptr_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `llamada` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_set_erase_begin_ptr_llamada(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_set_erase_begin(c);
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
9  (/tmp/mi-linter-runtime-validation/runtime_asan+0x26df69) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55ec1a98fee9  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d8ee9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7f4a99027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7f4a990278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x55ec1a7572c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55ec1a8bcfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55ec1a9ead64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55ec1a9ea9ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55ec1aa0bc88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55ec1aa0bc39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55ec1aa0b51f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55ec1aa0a425  (/tmp/mi-linter-runtime-validation/runtime_asan+0x353425) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55ec1aa09d06  (/tmp/mi-linter-runtime-validation/runtime_asan+0x352d06) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55ec1a9bc2b3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3052b3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55ec1a9581ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a11ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55ec1a98fedc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d8edc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f4a99027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f4a990278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55ec1a7572c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x26dfca) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b8a981dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b8a981dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b8a981dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b8a981dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b8a981dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b8a981e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7b8a981e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7b8a981e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b8a981e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b8a981e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b8a981e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==51==ABORTING
````

</details>
