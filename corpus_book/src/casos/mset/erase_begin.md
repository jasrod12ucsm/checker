# `std::multiset::erase_begin`

Mutación: `c.erase(c.begin());`

- Iterador retenido: 🔴 `UB`
- Referencia/puntero retenido: 🔴 `UB`
- Casos `UB` detectados estáticamente: 4/12

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🔴 avisa](#f_mset_erase_begin_it_recto) | [🔴 avisa](#f_mset_erase_begin_it_guarda) | [🔴 avisa](#f_mset_erase_begin_it_bucle) | [🔴 avisa](#f_mset_erase_begin_it_llamada) |
| **referencia** | [🔴 calla](#f_mset_erase_begin_ref_recto) | [🔴 calla](#f_mset_erase_begin_ref_guarda) | [🔴 calla](#f_mset_erase_begin_ref_bucle) | [🔴 calla](#f_mset_erase_begin_ref_llamada) |
| **puntero** | [🔴 calla](#f_mset_erase_begin_ptr_recto) | [🔴 calla](#f_mset_erase_begin_ptr_guarda) | [🔴 calla](#f_mset_erase_begin_ptr_bucle) | [🔴 calla](#f_mset_erase_begin_ptr_llamada) |

## Handle: iterador

### f_mset_erase_begin_it_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `recto` | 🔴 `UB` | ✅ detectado |

```cpp
void f_mset_erase_begin_it_recto(std::multiset<int>& c) {
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
    std::debug::multiset<int>; _Category = std::forward_iterator_tag; 
    reference = const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffc9b937ab0 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::multiset<int, std::less<int>, std::allocator<int> >' @ 0x7ffc9b937ba0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x27264f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x561973b7a12c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2db12c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fa700a27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fa700a278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x56197393f2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x561973aa4fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x561973bd2d64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x561973bd29ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x561973bf3c88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x561973bf3c39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x561973bf351f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x561973bf4597  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355597) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x561973bf4176  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355176) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x561973ba4733  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305733) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x561973b405ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a15ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x561973b7a11f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2db11f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7fa700a27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7fa700a278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x56197393f2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x2726bc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7be6ffbdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7be6ffbdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7be6ffbdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7be6ffbdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7be6ffbdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7be6ffbe0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7be6ffbe0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7be6ffbe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7be6ffbe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7be6ffbe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7be6ffbe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==101==ABORTING
````

</details>

### f_mset_erase_begin_it_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `guarda` | 🔴 `UB` | ✅ detectado |

```cpp
void f_mset_erase_begin_it_guarda(std::multiset<int>& c) {
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
    std::debug::multiset<int>; _Category = std::forward_iterator_tag; 
    reference = const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffedbb3c2c0 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::multiset<int, std::less<int>, std::allocator<int> >' @ 0x7ffedbb3c3b0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x272947) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55f5c99672ab  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2db2ab) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f7573e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f7573e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55f5c972c2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55f5c9891fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55f5c99bfd64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55f5c99bf9ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55f5c99e0c88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55f5c99e0c39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55f5c99e051f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55f5c99e1597  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355597) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55f5c99e1176  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355176) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55f5c9991733  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305733) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55f5c992d5ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a15ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55f5c996729e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2db29e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f7573e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f7573e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55f5c972c2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x2729b7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bb572fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bb572fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bb572fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bb572fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bb572fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bb572fe0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7bb572fe0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7bb572fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bb572fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bb572fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bb572fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==103==ABORTING
````

</details>

### f_mset_erase_begin_it_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ✅ detectado |

```cpp
void f_mset_erase_begin_it_bucle(std::multiset<int>& c) {
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
    std::debug::multiset<int>; _Category = std::forward_iterator_tag; 
    reference = const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fff9c934470 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::multiset<int, std::less<int>, std::allocator<int> >' @ 0x7fff9c934560
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x272cc2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x559870faf42a  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2db42a) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f49fba27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f49fba278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x559870d742c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x559870ed9fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x559871007d64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5598710079ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x559871028c88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x559871028c39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55987102851f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x559871029597  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355597) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x559871029176  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355176) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x559870fd9733  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305733) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x559870f755ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a15ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x559870faf41d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2db41d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f49fba27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f49fba278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x559870d742c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x272d32) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b89fabdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b89fabdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b89fabdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b89fabdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b89fabdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b89fabe0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7b89fabe0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7b89fabe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b89fabe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b89fabe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b89fabe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==105==ABORTING
````

</details>

### f_mset_erase_begin_it_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `llamada` | 🔴 `UB` | ✅ detectado |

```cpp
void f_mset_erase_begin_it_llamada(std::multiset<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_mset_erase_begin(c);
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
    std::debug::multiset<int>; _Category = std::forward_iterator_tag; 
    reference = const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fff7640e600 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::multiset<int, std::less<int>, std::allocator<int> >' @ 0x7fff7640e6c0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
  (/tmp/mi-linter-runtime-validation/runtime_asan+0x272f8c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55c4701335a9  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2db5a9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7f053f427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7f053f4278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x55c46fef82c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55c47005dfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55c47018bd64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55c47018b9ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55c4701acc88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55c4701acc39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55c4701ac51f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55c4701ad597  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355597) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55c4701ad176  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355176) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55c47015d733  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305733) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55c4700f95ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a15ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55c47013359c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2db59c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f053f427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f053f4278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55c46fef82c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x272ff5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b453e5dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b453e5dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b453e5dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b453e5dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b453e5dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b453e5e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7b453e5e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7b453e5e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b453e5e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b453e5e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b453e5e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==107==ABORTING
````

</details>

## Handle: referencia

### f_mset_erase_begin_ref_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `recto` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_mset_erase_begin_ref_recto(std::multiset<int>& c) {
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
d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x27325d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55e7238dc728  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2db728) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f6b7e427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f6b7e4278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55e7236a12c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55e723806fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55e723934d64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55e7239349ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55e723955c88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55e723955c39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55e72395551f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55e723956597  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355597) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55e723956176  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355176) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55e723906733  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305733) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55e7238a25ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a15ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55e7238dc71b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2db71b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f6b7e427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f6b7e4278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55e7236a12c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x27329c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bab7d5dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bab7d5dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bab7d5dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bab7d5dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bab7d5dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bab7d5e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7bab7d5e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7bab7d5e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bab7d5e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bab7d5e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bab7d5e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==109==ABORTING
````

</details>

### f_mset_erase_begin_ref_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `guarda` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_mset_erase_begin_ref_guarda(std::multiset<int>& c) {
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
a  (/tmp/mi-linter-runtime-validation/runtime_asan+0x27356a) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x56431feeb8a7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2db8a7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f9bce227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f9bce2278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x56431fcb02c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x56431fe15fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x56431ff43d64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x56431ff439ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x56431ff64c88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x56431ff64c39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x56431ff6451f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x56431ff65597  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355597) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x56431ff65176  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355176) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x56431ff15733  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305733) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x56431feb15ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a15ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x56431feeb89a  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2db89a) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f9bce227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f9bce2278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x56431fcb02c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x2735a3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bdbcd3dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bdbcd3dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bdbcd3dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bdbcd3dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bdbcd3dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bdbcd3e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7bdbcd3e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7bdbcd3e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bdbcd3e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bdbcd3e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bdbcd3e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==111==ABORTING
````

</details>

### f_mset_erase_begin_ref_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_mset_erase_begin_ref_bucle(std::multiset<int>& c) {
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
    debug::multiset<int>; _Category = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffed2c85d20 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::multiset<int, std::less<int>, std::allocator<int> >' @ 0x7ffed2c85e10
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
a  (/tmp/mi-linter-runtime-validation/runtime_asan+0x27390a) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5651a3476a26  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2dba26) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f20c4427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f20c44278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x5651a323b2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5651a33a0fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5651a34ced64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5651a34ce9ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5651a34efc88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5651a34efc39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5651a34ef51f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5651a34f0597  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355597) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5651a34f0176  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355176) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5651a34a0733  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305733) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x5651a343c5ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a15ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x5651a3476a19  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2dba19) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f20c4427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f20c44278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x5651a323b2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x273949) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b60c35dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b60c35dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b60c35dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b60c35dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b60c35dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b60c35e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7b60c35e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7b60c35e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b60c35e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b60c35e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b60c35e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==113==ABORTING
````

</details>

### f_mset_erase_begin_ref_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `llamada` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_mset_erase_begin_ref_llamada(std::multiset<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_mset_erase_begin(c);
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
  (/tmp/mi-linter-runtime-validation/runtime_asan+0x273c01) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55b7bb9ddba5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2dbba5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7fe0cea27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7fe0cea278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x55b7bb7a22c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55b7bb907fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55b7bba35d64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55b7bba359ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55b7bba56c88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55b7bba56c39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55b7bba5651f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55b7bba57597  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355597) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55b7bba57176  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355176) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55b7bba07733  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305733) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55b7bb9a35ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a15ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55b7bb9ddb98  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2dbb98) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7fe0cea27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7fe0cea278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55b7bb7a22c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x273c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c20cdbdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c20cdbdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c20cdbdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c20cdbdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c20cdbdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c20cdbe0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7c20cdbe0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7c20cdbe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c20cdbe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c20cdbe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c20cdbe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==115==ABORTING
````

</details>

## Handle: puntero

### f_mset_erase_begin_ptr_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `recto` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_mset_erase_begin_ptr_recto(std::multiset<int>& c) {
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
5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x273e55) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x558dbe873d24  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2dbd24) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fbdb9e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fbdb9e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x558dbe6382c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x558dbe79dfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x558dbe8cbd64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x558dbe8cb9ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x558dbe8ecc88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x558dbe8ecc39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x558dbe8ec51f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x558dbe8ed597  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355597) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x558dbe8ed176  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355176) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x558dbe89d733  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305733) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x558dbe8395ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a15ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x558dbe873d17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2dbd17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7fbdb9e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7fbdb9e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x558dbe6382c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x273eba) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bfdb8fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bfdb8fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bfdb8fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bfdb8fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bfdb8fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bfdb8fe0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7bfdb8fe0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7bfdb8fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bfdb8fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bfdb8fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bfdb8fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==117==ABORTING
````

</details>

### f_mset_erase_begin_ptr_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `guarda` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_mset_erase_begin_ptr_guarda(std::multiset<int>& c) {
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
7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x274157) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5649bc848ea3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2dbea3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fd0a7a27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fd0a7a278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x5649bc60d2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5649bc772fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5649bc8a0d64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5649bc8a09ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5649bc8c1c88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5649bc8c1c39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5649bc8c151f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5649bc8c2597  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355597) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5649bc8c2176  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355176) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5649bc872733  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305733) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x5649bc80e5ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a15ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x5649bc848e96  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2dbe96) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7fd0a7a27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7fd0a7a278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x5649bc60d2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x2741bf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c10a6bdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c10a6bdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c10a6bdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c10a6bdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c10a6bdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c10a6be0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7c10a6be0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7c10a6be0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c10a6be0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c10a6be0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c10a6be0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==119==ABORTING
````

</details>

### f_mset_erase_begin_ptr_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_mset_erase_begin_ptr_bucle(std::multiset<int>& c) {
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
    debug::multiset<int>; _Category = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffe7db5dfa0 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::multiset<int, std::less<int>, std::allocator<int> >' @ 0x7ffe7db5e090
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2744f7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55ebb7569022  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2dc022) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f9b03e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f9b03e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55ebb732d2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55ebb7492fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55ebb75c0d64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55ebb75c09ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55ebb75e1c88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55ebb75e1c39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55ebb75e151f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55ebb75e2597  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355597) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55ebb75e2176  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355176) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55ebb7592733  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305733) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55ebb752e5ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a15ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55ebb7569015  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2dc015) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f9b03e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f9b03e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55ebb732d2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x274562) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bdb02fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bdb02fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bdb02fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bdb02fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bdb02fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bdb02fe0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7bdb02fe0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7bdb02fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bdb02fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bdb02fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bdb02fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==121==ABORTING
````

</details>

### f_mset_erase_begin_ptr_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `llamada` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_mset_erase_begin_ptr_llamada(std::multiset<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_mset_erase_begin(c);
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
  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2747c9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x5583ca4a51a1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2dc1a1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7f4756027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7f47560278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x5583ca2692c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5583ca3cefe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5583ca4fcd64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5583ca4fc9ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5583ca51dc88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5583ca51dc39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5583ca51d51f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5583ca51e597  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355597) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5583ca51e176  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355176) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5583ca4ce733  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305733) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x5583ca46a5ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a15ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x5583ca4a5194  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2dc194) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f4756027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f47560278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x5583ca2692c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x27482a) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b87551dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b87551dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b87551dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b87551dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b87551dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b87551e0000: fa fa fd fd fd fd[fd]fa fa fa 00 00 00 00 00 fa
  0x7b87551e0080: fa fa 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7b87551e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b87551e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b87551e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b87551e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==123==ABORTING
````

</details>
