# `std::multiset::clear`

Mutación: `c.clear();`

- Iterador retenido: 🔴 `UB`
- Referencia/puntero retenido: 🔴 `UB`
- Casos `UB` detectados estáticamente: 4/12

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🔴 avisa](#f_mset_clear_it_recto) | [🔴 avisa](#f_mset_clear_it_guarda) | [🔴 avisa](#f_mset_clear_it_bucle) | [🔴 avisa](#f_mset_clear_it_llamada) |
| **referencia** | [🔴 calla](#f_mset_clear_ref_recto) | [🔴 calla](#f_mset_clear_ref_guarda) | [🔴 calla](#f_mset_clear_ref_bucle) | [🔴 calla](#f_mset_clear_ref_llamada) |
| **puntero** | [🔴 calla](#f_mset_clear_ptr_recto) | [🔴 calla](#f_mset_clear_ptr_guarda) | [🔴 calla](#f_mset_clear_ptr_bucle) | [🔴 calla](#f_mset_clear_ptr_llamada) |

## Handle: iterador

### f_mset_clear_it_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `recto` | 🔴 `UB` | ✅ detectado |

```cpp
void f_mset_clear_it_recto(std::multiset<int>& c) {
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
    std::debug::multiset<int>; _Category = std::forward_iterator_tag; 
    reference = const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffc71d87890 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::multiset<int, std::less<int>, std::allocator<int> >' @ 0x7ffc71d87910
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2749fb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55a33113e320  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2dc320) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f054bc27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f054bc278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55a330f022c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55a331067fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55a331195d64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55a3311959ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55a3311b6c88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55a3311b6c39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55a3311b651f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55a3311b7597  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355597) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55a3311b7176  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355176) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55a331167733  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305733) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55a3311035ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a15ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55a33113e313  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2dc313) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f054bc27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f054bc278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55a330f022c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x274a64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b454addfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b454addfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b454addfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b454addff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b454addff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b454ade0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7b454ade0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7b454ade0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b454ade0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b454ade0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b454ade0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==125==ABORTING
````

</details>

### f_mset_clear_it_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `guarda` | 🔴 `UB` | ✅ detectado |

```cpp
void f_mset_clear_it_guarda(std::multiset<int>& c) {
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
    std::debug::multiset<int>; _Category = std::forward_iterator_tag; 
    reference = const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fffcf9231d0 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::multiset<int, std::less<int>, std::allocator<int> >' @ 0x7fffcf923290
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x274c9e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55af812bc45c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2dc45c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f887fa27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f887fa278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55af810802c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55af811e5fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55af81313d64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55af813139ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55af81334c88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55af81334c39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55af8133451f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55af81335597  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355597) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55af81335176  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355176) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55af812e5733  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305733) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55af812815ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a15ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55af812bc44f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2dc44f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f887fa27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f887fa278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55af810802c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x274d07) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bc87ebdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bc87ebdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bc87ebdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bc87ebdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bc87ebdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bc87ebe0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7bc87ebe0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7bc87ebe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bc87ebe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bc87ebe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bc87ebe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==127==ABORTING
````

</details>

### f_mset_clear_it_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ✅ detectado |

```cpp
void f_mset_clear_it_bucle(std::multiset<int>& c) {
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
    std::debug::multiset<int>; _Category = std::forward_iterator_tag; 
    reference = const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffca45100a0 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::multiset<int, std::less<int>, std::allocator<int> >' @ 0x7ffca4510160
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x274fd4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5598a98fb598  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2dc598) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f62bd427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f62bd4278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x5598a96bf2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5598a9824fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5598a9952d64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5598a99529ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5598a9973c88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5598a9973c39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5598a997351f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5598a9974597  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355597) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5598a9974176  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355176) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5598a9924733  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305733) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x5598a98c05ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a15ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x5598a98fb58b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2dc58b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f62bd427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f62bd4278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x5598a96bf2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x27503d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7ba2bc5dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ba2bc5dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ba2bc5dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ba2bc5dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ba2bc5dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7ba2bc5e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7ba2bc5e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7ba2bc5e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ba2bc5e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ba2bc5e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ba2bc5e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==129==ABORTING
````

</details>

### f_mset_clear_it_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `llamada` | 🔴 `UB` | ✅ detectado |

```cpp
void f_mset_clear_it_llamada(std::multiset<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_mset_clear(c);
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
    iterator "this" @ 0x7fff67e3dcd0 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::multiset<int, std::less<int>, std::allocator<int> >' @ 0x7fff67e3dd90
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
  (/tmp/mi-linter-runtime-validation/runtime_asan+0x27529c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55a751b846d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2dc6d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7ff0e6627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7ff0e66278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x55a7519482c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55a751aadfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55a751bdbd64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55a751bdb9ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55a751bfcc88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55a751bfcc39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55a751bfc51f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55a751bfd597  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355597) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55a751bfd176  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355176) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55a751bad733  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305733) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55a751b495ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a15ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55a751b846c7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2dc6c7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7ff0e6627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7ff0e66278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55a7519482c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x275305) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c30e57dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c30e57dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c30e57dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c30e57dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c30e57dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c30e57e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7c30e57e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7c30e57e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c30e57e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c30e57e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c30e57e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==131==ABORTING
````

</details>

## Handle: referencia

### f_mset_clear_ref_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `recto` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_mset_clear_ref_recto(std::multiset<int>& c) {
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
7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x275517) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x564c7405a810  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2dc810) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f77f4427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f77f44278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x564c73e1e2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x564c73f83fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x564c740b1d64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x564c740b19ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x564c740d2c88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x564c740d2c39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x564c740d251f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x564c740d3597  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355597) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x564c740d3176  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355176) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x564c74083733  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305733) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x564c7401f5ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a15ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x564c7405a803  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2dc803) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f77f4427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f77f44278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x564c73e1e2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x27554c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bb7f35dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bb7f35dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bb7f35dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bb7f35dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bb7f35dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bb7f35e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7bb7f35e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7bb7f35e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bb7f35e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bb7f35e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bb7f35e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==133==ABORTING
````

</details>

### f_mset_clear_ref_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `guarda` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_mset_clear_ref_guarda(std::multiset<int>& c) {
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
3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2757d3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55fa56ebf94c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2dc94c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fb92f027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fb92f0278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55fa56c832c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55fa56de8fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55fa56f16d64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55fa56f169ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55fa56f37c88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55fa56f37c39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55fa56f3751f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55fa56f38597  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355597) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55fa56f38176  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355176) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55fa56ee8733  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305733) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55fa56e845ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a15ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55fa56ebf93f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2dc93f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7fb92f027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7fb92f0278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55fa56c832c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x27580b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bf92e1dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf92e1dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf92e1dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf92e1dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf92e1dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bf92e1e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7bf92e1e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7bf92e1e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf92e1e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf92e1e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf92e1e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==135==ABORTING
````

</details>

### f_mset_clear_ref_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_mset_clear_ref_bucle(std::multiset<int>& c) {
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
    debug::multiset<int>; _Category = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffc10c47420 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::multiset<int, std::less<int>, std::allocator<int> >' @ 0x7ffc10c474e0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x275b0e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x559913c22a88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2dca88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fc99a827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fc99a8278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x5599139e62c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x559913b4bfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x559913c79d64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x559913c799ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x559913c9ac88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x559913c9ac39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x559913c9a51f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x559913c9b597  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355597) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x559913c9b176  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355176) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x559913c4b733  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305733) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x559913be75ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a15ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x559913c22a7b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2dca7b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7fc99a827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7fc99a8278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x5599139e62c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x275b46) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c09999dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c09999dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c09999dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c09999dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c09999dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c09999e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7c09999e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7c09999e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c09999e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c09999e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c09999e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==137==ABORTING
````

</details>

### f_mset_clear_ref_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `llamada` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_mset_clear_ref_llamada(std::multiset<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_mset_clear(c);
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
  (/tmp/mi-linter-runtime-validation/runtime_asan+0x275e01) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x5615665a6bc4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2dcbc4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7f20bbc27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7f20bbc278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x56156636a2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5615664cffe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5615665fdd64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5615665fd9ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x56156661ec88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x56156661ec39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x56156661e51f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x56156661f597  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355597) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x56156661f176  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355176) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5615665cf733  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305733) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x56156656b5ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a15ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x5615665a6bb7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2dcbb7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f20bbc27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f20bbc278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x56156636a2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x275e39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b60baddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b60baddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b60baddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b60baddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b60baddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b60bade0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7b60bade0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7b60bade0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b60bade0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b60bade0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b60bade0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==139==ABORTING
````

</details>

## Handle: puntero

### f_mset_clear_ptr_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `recto` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_mset_clear_ptr_recto(std::multiset<int>& c) {
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
4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x276014) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55bea83f2d00  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2dcd00) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fadbe627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fadbe6278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55bea81b62c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55bea831bfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55bea8449d64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55bea84499ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55bea846ac88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55bea846ac39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55bea846a51f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55bea846b597  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355597) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55bea846b176  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355176) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55bea841b733  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305733) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55bea83b75ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a15ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55bea83f2cf3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2dccf3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7fadbe627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7fadbe6278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55bea81b62c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x276075) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bedbd7dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bedbd7dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bedbd7dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bedbd7dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bedbd7dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bedbd7e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7bedbd7e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7bedbd7e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bedbd7e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bedbd7e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bedbd7e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==141==ABORTING
````

</details>

### f_mset_clear_ptr_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `guarda` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_mset_clear_ptr_guarda(std::multiset<int>& c) {
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
b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2762bb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55f77d870e3c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2dce3c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f15aea27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f15aea278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55f77d6342c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55f77d799fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55f77d8c7d64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55f77d8c79ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55f77d8e8c88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55f77d8e8c39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55f77d8e851f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55f77d8e9597  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355597) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55f77d8e9176  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355176) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55f77d899733  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305733) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55f77d8355ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a15ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55f77d870e2f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2dce2f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f15aea27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f15aea278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55f77d6342c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x27631c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b55adbdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b55adbdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b55adbdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b55adbdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b55adbdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b55adbe0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7b55adbe0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7b55adbe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b55adbe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b55adbe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b55adbe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==143==ABORTING
````

</details>

### f_mset_clear_ptr_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_mset_clear_ptr_bucle(std::multiset<int>& c) {
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
    debug::multiset<int>; _Category = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffdaba52000 {
      type = std::_Rb_tree_const_iterator<int> (constant iterator);
      state = singular;
      references sequence with type 'std::debug::multiset<int, std::less<int>, std::allocator<int> >' @ 0x7ffdaba520c0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2765eb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55ee0f896f78  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2dcf78) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7feb26a27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7feb26a278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55ee0f65a2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55ee0f7bffe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55ee0f8edd64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55ee0f8ed9ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55ee0f90ec88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55ee0f90ec39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55ee0f90e51f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55ee0f90f597  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355597) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55ee0f90f176  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355176) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55ee0f8bf733  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305733) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55ee0f85b5ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a15ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55ee0f896f6b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2dcf6b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7feb26a27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7feb26a278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55ee0f65a2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x27664f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c2b25bdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c2b25bdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c2b25bdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c2b25bdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c2b25bdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c2b25be0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7c2b25be0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7c2b25be0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c2b25be0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c2b25be0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c2b25be0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==145==ABORTING
````

</details>

### f_mset_clear_ptr_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `llamada` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_mset_clear_ptr_llamada(std::multiset<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_mset_clear(c);
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
  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2768b9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x555e0d5e10b4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2dd0b4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7f336d027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7f336d0278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x555e0d3a42c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x555e0d509fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x555e0d637d64  (/tmp/mi-linter-runtime-validation/runtime_asan+0x333d64) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x555e0d6379ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3339ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x555e0d658c88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x555e0d658c39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x354c39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x555e0d65851f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35451f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x555e0d659597  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355597) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x555e0d659176  (/tmp/mi-linter-runtime-validation/runtime_asan+0x355176) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x555e0d609733  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305733) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x555e0d5a55ed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a15ed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x555e0d5e10a7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2dd0a7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f336d027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f336d0278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x555e0d3a42c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x27691a) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b736c1dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b736c1dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b736c1dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b736c1dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b736c1dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b736c1e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7b736c1e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7b736c1e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b736c1e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b736c1e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b736c1e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==147==ABORTING
````

</details>
