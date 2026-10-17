# `std::multimap::erase_begin`

Mutación: `c.erase(c.begin());`

- Iterador retenido: 🔴 `UB`
- Referencia/puntero retenido: 🔴 `UB`
- Casos `UB` detectados estáticamente: 4/12

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🔴 avisa](#f_mmap_erase_begin_it_recto) | [🔴 avisa](#f_mmap_erase_begin_it_guarda) | [🔴 avisa](#f_mmap_erase_begin_it_bucle) | [🔴 avisa](#f_mmap_erase_begin_it_llamada) |
| **referencia** | [🔴 calla](#f_mmap_erase_begin_ref_recto) | [🔴 calla](#f_mmap_erase_begin_ref_guarda) | [🔴 calla](#f_mmap_erase_begin_ref_bucle) | [🔴 calla](#f_mmap_erase_begin_ref_llamada) |
| **puntero** | [🔴 calla](#f_mmap_erase_begin_ptr_recto) | [🔴 calla](#f_mmap_erase_begin_ptr_guarda) | [🔴 calla](#f_mmap_erase_begin_ptr_bucle) | [🔴 calla](#f_mmap_erase_begin_ptr_llamada) |

## Handle: iterador

### f_mmap_erase_begin_it_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `recto` | 🔴 `UB` | ✅ detectado |

```cpp
void f_mmap_erase_begin_it_recto(std::multimap<int,int>& c) {
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
    >; _Sequence = std::debug::multimap<int, int>; _Category = 
    std::forward_iterator_tag; pointer = std::pair<const int, int>*]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffd3418a000 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffd3418a0f0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x285313) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x56453e8aea84  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e3a84) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fbbc1c27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fbbc1c278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x56453e66b2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x56453e7d0fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x56453e9036c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x56453e9033cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x56453e923068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x56453e923019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x56453e922caf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x56453e923967  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358967) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x56453e923546  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358546) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x56453e8d1033  (/tmp/mi-linter-runtime-validation/runtime_asan+0x306033) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x56453e86ce04  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a1e04) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x56453e8aea77  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e3a77) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7fbbc1c27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7fbbc1c278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x56453e66b2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x2853b4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bfbc0ddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bfbc0ddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bfbc0ddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bfbc0ddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bfbc0ddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bfbc0de0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7bfbc0de0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7bfbc0de0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bfbc0de0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bfbc0de0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bfbc0de0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==293==ABORTING
````

</details>

### f_mmap_erase_begin_it_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `guarda` | 🔴 `UB` | ✅ detectado |

```cpp
void f_mmap_erase_begin_it_guarda(std::multimap<int,int>& c) {
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
    >; _Sequence = std::debug::multimap<int, int>; _Category = 
    std::forward_iterator_tag; pointer = std::pair<const int, int>*]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffd3ad02390 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffd3ad02480
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x28561d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55b698c83c03  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e3c03) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f8572427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f85724278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55b698a402c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55b698ba5fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55b698cd86c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55b698cd83cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55b698cf8068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55b698cf8019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55b698cf7caf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55b698cf8967  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358967) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55b698cf8546  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358546) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55b698ca6033  (/tmp/mi-linter-runtime-validation/runtime_asan+0x306033) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55b698c41e04  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a1e04) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55b698c83bf6  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e3bf6) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f8572427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f85724278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55b698a402c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x2856c1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bc5715dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bc5715dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bc5715dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bc5715dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bc5715dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bc5715e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7bc5715e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7bc5715e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bc5715e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bc5715e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bc5715e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==295==ABORTING
````

</details>

### f_mmap_erase_begin_it_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ✅ detectado |

```cpp
void f_mmap_erase_begin_it_bucle(std::multimap<int,int>& c) {
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
    >; _Sequence = std::debug::multimap<int, int>; _Category = 
    std::forward_iterator_tag; pointer = std::pair<const int, int>*]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffe72e85b70 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffe72e85c60
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2859c0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x560d80872d82  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e3d82) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f8dfa227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f8dfa2278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x560d8062f2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x560d80794fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x560d808c76c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x560d808c73cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x560d808e7068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x560d808e7019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x560d808e6caf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x560d808e7967  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358967) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x560d808e7546  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358546) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x560d80895033  (/tmp/mi-linter-runtime-validation/runtime_asan+0x306033) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x560d80830e04  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a1e04) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x560d80872d75  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e3d75) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f8dfa227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f8dfa2278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x560d8062f2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x285a64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bcdf93dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bcdf93dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bcdf93dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bcdf93dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bcdf93dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bcdf93e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7bcdf93e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7bcdf93e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bcdf93e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bcdf93e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bcdf93e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==297==ABORTING
````

</details>

### f_mmap_erase_begin_it_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `llamada` | 🔴 `UB` | ✅ detectado |

```cpp
void f_mmap_erase_begin_it_llamada(std::multimap<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_mmap_erase_begin(c);
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
    >; _Sequence = std::debug::multimap<int, int>; _Category = 
    std::forward_iterator_tag; pointer = std::pair<const int, int>*]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffe9131f3b0 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffe9131f470
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
  (/tmp/mi-linter-runtime-validation/runtime_asan+0x285cb0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55ad21ee0f01  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e3f01) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7f267b227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7f267b2278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x55ad21c9d2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55ad21e02fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55ad21f356c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55ad21f353cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55ad21f55068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55ad21f55019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55ad21f54caf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55ad21f55967  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358967) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55ad21f55546  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358546) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55ad21f03033  (/tmp/mi-linter-runtime-validation/runtime_asan+0x306033) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55ad21e9ee04  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a1e04) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55ad21ee0ef4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e3ef4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f267b227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f267b2278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55ad21c9d2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x285d4d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b667a3dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b667a3dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b667a3dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b667a3dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b667a3dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b667a3e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7b667a3e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7b667a3e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b667a3e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b667a3e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b667a3e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==299==ABORTING
````

</details>

## Handle: referencia

### f_mmap_erase_begin_ref_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `recto` | 🔴 `UB` | ❌ falso negativo |

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
| `natural` | estado inicial ordinario | — (código 0) | 🛑 heap-use-after-free |

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x285f91) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55d2131a0080  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e4080) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f38cec27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f38cec278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55d212f5c2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55d2130c1fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55d2131f46c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55d2131f43cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55d213214068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55d213214019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55d213213caf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55d213214967  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358967) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55d213214546  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358546) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55d2131c2033  (/tmp/mi-linter-runtime-validation/runtime_asan+0x306033) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55d21315de04  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a1e04) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55d2131a0073  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e4073) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f38cec27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f38cec278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55d212f5c2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x285ff2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b78cdddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b78cdddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b78cdddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b78cdddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b78cdddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b78cdde0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7b78cdde0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7b78cdde0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b78cdde0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b78cdde0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b78cdde0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==301==ABORTING
````

</details>

### f_mmap_erase_begin_ref_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `guarda` | 🔴 `UB` | ❌ falso negativo |

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
| `natural` | estado inicial ordinario | — (código 0) | 🛑 heap-use-after-free |

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2862a0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55d4452381ff  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e41ff) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f26c3627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f26c36278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55d444ff42c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55d445159fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55d44528c6c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55d44528c3cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55d4452ac068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55d4452ac019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55d4452abcaf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55d4452ac967  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358967) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55d4452ac546  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358546) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55d44525a033  (/tmp/mi-linter-runtime-validation/runtime_asan+0x306033) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55d4451f5e04  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a1e04) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55d4452381f2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e41f2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f26c3627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f26c36278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55d444ff42c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x2862fe) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b66c27dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b66c27dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b66c27dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b66c27dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b66c27dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b66c27e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7b66c27e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7b66c27e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b66c27e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b66c27e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b66c27e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==303==ABORTING
````

</details>

### f_mmap_erase_begin_ref_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `bucle` | 🔴 `UB` | ❌ falso negativo |

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
/usr/include/c++/16/debug/safe_iterator.h:392:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>& 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator++() 
    [with _Iterator = std::_Rb_tree_iterator<std::pair<const int, int> >; 
    _Sequence = std::debug::multimap<int, int>; _Category = 
    std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffe9d425400 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffe9d4254f0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x286630) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55c6f417337e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e437e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f3deca27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f3deca278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55c6f3f2f2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55c6f4094fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55c6f41c76c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55c6f41c73cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55c6f41e7068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55c6f41e7019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55c6f41e6caf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55c6f41e7967  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358967) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55c6f41e7546  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358546) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55c6f4195033  (/tmp/mi-linter-runtime-validation/runtime_asan+0x306033) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55c6f4130e04  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a1e04) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55c6f4173371  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e4371) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f3deca27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f3deca278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55c6f3f2f2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x286691) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b7debbdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b7debbdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b7debbdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b7debbdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b7debbdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b7debbe0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7b7debbe0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7b7debbe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b7debbe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b7debbe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b7debbe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==305==ABORTING
````

</details>

### f_mmap_erase_begin_ref_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `llamada` | 🔴 `UB` | ❌ falso negativo |

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
| `natural` | estado inicial ordinario | — (código 0) | 🛑 heap-use-after-free |

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
  (/tmp/mi-linter-runtime-validation/runtime_asan+0x286925) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x563281b814fd  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e44fd) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7fa335027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7fa3350278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x56328193d2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x563281aa2fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x563281bd56c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x563281bd53cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x563281bf5068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x563281bf5019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x563281bf4caf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x563281bf5967  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358967) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x563281bf5546  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358546) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x563281ba3033  (/tmp/mi-linter-runtime-validation/runtime_asan+0x306033) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x563281b3ee04  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a1e04) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x563281b814f0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e44f0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7fa335027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7fa3350278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x56328193d2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x28697f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7be3341dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7be3341dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7be3341dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7be3341dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7be3341dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7be3341e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7be3341e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7be3341e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7be3341e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7be3341e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7be3341e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==307==ABORTING
````

</details>

## Handle: puntero

### f_mmap_erase_begin_ptr_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `recto` | 🔴 `UB` | ❌ falso negativo |

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
| `natural` | estado inicial ordinario | — (código 0) | 🛑 heap-use-after-free |

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x286b9e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5575d4ce867c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e467c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fbc8d427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fbc8d4278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x5575d4aa42c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5575d4c09fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5575d4d3c6c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5575d4d3c3cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5575d4d5c068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5575d4d5c019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5575d4d5bcaf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5575d4d5c967  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358967) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5575d4d5c546  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358546) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5575d4d0a033  (/tmp/mi-linter-runtime-validation/runtime_asan+0x306033) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x5575d4ca5e04  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a1e04) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x5575d4ce866f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e466f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7fbc8d427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7fbc8d4278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x5575d4aa42c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x286c3d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bfc8c5dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bfc8c5dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bfc8c5dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bfc8c5dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bfc8c5dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bfc8c5e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7bfc8c5e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7bfc8c5e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bfc8c5e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bfc8c5e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bfc8c5e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==309==ABORTING
````

</details>

### f_mmap_erase_begin_ptr_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `guarda` | 🔴 `UB` | ❌ falso negativo |

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
| `natural` | estado inicial ordinario | — (código 0) | 🛑 heap-use-after-free |

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x286ead) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5602b2f0d7fb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e47fb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fe736827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fe7368278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x5602b2cc92c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5602b2e2efe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5602b2f616c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5602b2f613cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5602b2f81068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5602b2f81019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5602b2f80caf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5602b2f81967  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358967) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5602b2f81546  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358546) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5602b2f2f033  (/tmp/mi-linter-runtime-validation/runtime_asan+0x306033) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x5602b2ecae04  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a1e04) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x5602b2f0d7ee  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e47ee) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7fe736827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7fe7368278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x5602b2cc92c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x286f49) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c27359dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c27359dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c27359dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c27359dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c27359dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c27359e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7c27359e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7c27359e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c27359e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c27359e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c27359e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==311==ABORTING
````

</details>

### f_mmap_erase_begin_ptr_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `bucle` | 🔴 `UB` | ❌ falso negativo |

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
/usr/include/c++/16/debug/safe_iterator.h:392:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>& 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator++() 
    [with _Iterator = std::_Rb_tree_iterator<std::pair<const int, int> >; 
    _Sequence = std::debug::multimap<int, int>; _Category = 
    std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fff9124ab80 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7fff9124ac70
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x28724d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5559c820197a  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e497a) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f6ee1a27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f6ee1a278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x5559c7fbd2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5559c8122fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5559c82556c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5559c82553cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5559c8275068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5559c8275019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5559c8274caf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5559c8275967  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358967) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5559c8275546  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358546) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5559c8223033  (/tmp/mi-linter-runtime-validation/runtime_asan+0x306033) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x5559c81bee04  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a1e04) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x5559c820196d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e496d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f6ee1a27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f6ee1a278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x5559c7fbd2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x2872ec) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7baee0bdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7baee0bdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7baee0bdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7baee0bdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7baee0bdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7baee0be0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7baee0be0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7baee0be0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7baee0be0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7baee0be0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7baee0be0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==313==ABORTING
````

</details>

### f_mmap_erase_begin_ptr_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `llamada` | 🔴 `UB` | ❌ falso negativo |

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
| `natural` | estado inicial ordinario | — (código 0) | 🛑 heap-use-after-free |

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
  (/tmp/mi-linter-runtime-validation/runtime_asan+0x287552) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x56366d51eaf9  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e4af9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7f3b8a827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7f3b8a8278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x56366d2da2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x56366d43ffe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x56366d5726c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x56366d5723cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x56366d592068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x56366d592019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x56366d591caf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x56366d592967  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358967) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x56366d592546  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358546) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x56366d540033  (/tmp/mi-linter-runtime-validation/runtime_asan+0x306033) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x56366d4dbe04  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a1e04) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x56366d51eaec  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e4aec) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f3b8a827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f3b8a8278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x56366d2da2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x2875ea) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b7b899dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b7b899dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b7b899dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b7b899dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b7b899dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b7b899e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7b7b899e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7b7b899e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b7b899e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b7b899e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b7b899e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==315==ABORTING
````

</details>
