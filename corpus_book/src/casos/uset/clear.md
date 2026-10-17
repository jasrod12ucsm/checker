# `std::unordered_set::clear`

Mutación: `c.clear();`

- Iterador retenido: 🔴 `UB`
- Referencia/puntero retenido: 🔴 `UB`
- Casos `UB` detectados estáticamente: 4/12

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🔴 avisa](#f_uset_clear_it_recto) | [🔴 avisa](#f_uset_clear_it_guarda) | [🔴 avisa](#f_uset_clear_it_bucle) | [🔴 avisa](#f_uset_clear_it_llamada) |
| **referencia** | [🔴 calla](#f_uset_clear_ref_recto) | [🔴 calla](#f_uset_clear_ref_guarda) | [🔴 calla](#f_uset_clear_ref_bucle) | [🔴 calla](#f_uset_clear_ref_llamada) |
| **puntero** | [🔴 calla](#f_uset_clear_ptr_recto) | [🔴 calla](#f_uset_clear_ptr_guarda) | [🔴 calla](#f_uset_clear_ptr_bucle) | [🔴 calla](#f_uset_clear_ptr_llamada) |

## Handle: iterador

### f_uset_clear_it_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `recto` | 🔴 `UB` | ✅ detectado |

```cpp
void f_uset_clear_it_recto(std::unordered_set<int>& c) {
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
    const [with _Iterator = std::detail::_Node_iterator<int, true, false>; 
    _Sequence = std::debug::unordered_set<int>; _Category = 
    std::forward_iterator_tag; reference = const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffc0a523030 {
      type = std::detail::_Node_iterator<int, true, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int> >' @ 0x7ffc0a5230b0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
a678  (/tmp/mi-linter-runtime-validation/runtime_asan+0x307678) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55e008547aa5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x344aa5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55e0085041f0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3011f0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55e008490e9d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x28de9d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55e0084eb12f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e812f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f15fc427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f15fc4278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55e0082a32c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55e008408fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55e0085428d7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33f8d7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55e00854189c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e89c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55e0085413c2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e3c2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55e008540af9  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33daf9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55e008503fd5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x300fd5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55e0084a5437  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2437) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55e0084eb122  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e8122) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f15fc427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f15fc4278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55e0082a32c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x28df06) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b35fb5dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b35fb5dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b35fb5dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b35fb5dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b35fb5dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b35fb5e0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x7b35fb5e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b35fb5e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b35fb5e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b35fb5e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b35fb5e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==395==ABORTING
````

</details>

### f_uset_clear_it_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `guarda` | 🔴 `UB` | ✅ detectado |

```cpp
void f_uset_clear_it_guarda(std::unordered_set<int>& c) {
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
    const [with _Iterator = std::detail::_Node_iterator<int, true, false>; 
    _Sequence = std::debug::unordered_set<int>; _Category = 
    std::forward_iterator_tag; reference = const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffcc2ff6a10 {
      type = std::detail::_Node_iterator<int, true, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int> >' @ 0x7ffcc2ff6ad0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
b678  (/tmp/mi-linter-runtime-validation/runtime_asan+0x307678) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55c8e85d8aa5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x344aa5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55c8e85951f0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3011f0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55c8e8522122  (/tmp/mi-linter-runtime-validation/runtime_asan+0x28e122) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55c8e857c279  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e8279) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f567dc27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f567dc278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55c8e83342c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55c8e8499fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55c8e85d38d7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33f8d7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55c8e85d289c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e89c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55c8e85d23c2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e3c2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55c8e85d1af9  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33daf9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55c8e8594fd5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x300fd5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55c8e8536437  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2437) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55c8e857c26c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e826c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f567dc27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f567dc278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55c8e83342c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x28e18b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b767cddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b767cddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b767cddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b767cddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b767cddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b767cde0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x7b767cde0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b767cde0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b767cde0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b767cde0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b767cde0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==397==ABORTING
````

</details>

### f_uset_clear_it_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ✅ detectado |

```cpp
void f_uset_clear_it_bucle(std::unordered_set<int>& c) {
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
    const [with _Iterator = std::detail::_Node_iterator<int, true, false>; 
    _Sequence = std::debug::unordered_set<int>; _Category = 
    std::forward_iterator_tag; reference = const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffd804431e0 {
      type = std::detail::_Node_iterator<int, true, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int> >' @ 0x7ffd804432a0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
5678  (/tmp/mi-linter-runtime-validation/runtime_asan+0x307678) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55d3fe9d2aa5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x344aa5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55d3fe98f1f0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3011f0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55d3fe91c438  (/tmp/mi-linter-runtime-validation/runtime_asan+0x28e438) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55d3fe9763c3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e83c3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f2f5ea27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f2f5ea278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55d3fe72e2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55d3fe893fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55d3fe9cd8d7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33f8d7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55d3fe9cc89c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e89c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55d3fe9cc3c2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e3c2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55d3fe9cbaf9  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33daf9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55d3fe98efd5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x300fd5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55d3fe930437  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2437) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55d3fe9763b6  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e83b6) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f2f5ea27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f2f5ea278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55d3fe72e2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x28e4a1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b4f5dbdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b4f5dbdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b4f5dbdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b4f5dbdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b4f5dbdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b4f5dbe0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x7b4f5dbe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b4f5dbe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b4f5dbe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b4f5dbe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b4f5dbe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==399==ABORTING
````

</details>

### f_uset_clear_it_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `llamada` | 🔴 `UB` | ✅ detectado |

```cpp
void f_uset_clear_it_llamada(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_uset_clear(c);
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
    const [with _Iterator = std::detail::_Node_iterator<int, true, false>; 
    _Sequence = std::debug::unordered_set<int>; _Category = 
    std::forward_iterator_tag; reference = const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fff42fa8bb0 {
      type = std::detail::_Node_iterator<int, true, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int> >' @ 0x7fff42fa8c70
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
aa5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x344aa5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5644be93f1f0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3011f0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5644be8492ee  (/tmp/mi-linter-runtime-validation/runtime_asan+0x20b2ee) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5644be8cc6e0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x28e6e0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x5644be92650d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e850d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7f8150627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7f81506278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x5644be6de2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5644be843fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5644be97d8d7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33f8d7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5644be97c89c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e89c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5644be97c3c2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e3c2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5644be97baf9  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33daf9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5644be93efd5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x300fd5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5644be8e0437  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2437) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5644be926500  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e8500) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f8150627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f81506278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x5644be6de2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x28e749) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7ba14f7dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ba14f7dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ba14f7dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ba14f7dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ba14f7dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7ba14f7e0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x7ba14f7e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ba14f7e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ba14f7e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ba14f7e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ba14f7e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==401==ABORTING
````

</details>

## Handle: referencia

### f_uset_clear_ref_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `recto` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_uset_clear_ref_recto(std::unordered_set<int>& c) {
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
a678  (/tmp/mi-linter-runtime-validation/runtime_asan+0x307678) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x561fa7e27aa5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x344aa5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x561fa7de41f0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3011f0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x561fa7d71949  (/tmp/mi-linter-runtime-validation/runtime_asan+0x28e949) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x561fa7dcb657  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e8657) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fa6ab627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fa6ab6278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x561fa7b832c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x561fa7ce8fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x561fa7e228d7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33f8d7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x561fa7e2189c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e89c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x561fa7e213c2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e3c2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x561fa7e20af9  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33daf9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x561fa7de3fd5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x300fd5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x561fa7d85437  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2437) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x561fa7dcb64a  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e864a) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7fa6ab627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7fa6ab6278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x561fa7b832c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x28e97e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bc6aa7dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bc6aa7dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bc6aa7dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bc6aa7dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bc6aa7dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bc6aa7e0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x7bc6aa7e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bc6aa7e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bc6aa7e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bc6aa7e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bc6aa7e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==403==ABORTING
````

</details>

### f_uset_clear_ref_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `guarda` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_uset_clear_ref_guarda(std::unordered_set<int>& c) {
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
2678  (/tmp/mi-linter-runtime-validation/runtime_asan+0x307678) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55dbc35cfaa5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x344aa5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55dbc358c1f0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3011f0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55dbc3519bf7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x28ebf7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55dbc35737a1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e87a1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f673a827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f673a8278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55dbc332b2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55dbc3490fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55dbc35ca8d7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33f8d7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55dbc35c989c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e89c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55dbc35c93c2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e3c2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55dbc35c8af9  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33daf9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55dbc358bfd5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x300fd5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55dbc352d437  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2437) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55dbc3573794  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e8794) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f673a827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f673a8278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55dbc332b2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x28ec2f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b87399dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b87399dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b87399dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b87399dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b87399dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b87399e0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x7b87399e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b87399e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b87399e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b87399e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b87399e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==405==ABORTING
````

</details>

### f_uset_clear_ref_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_uset_clear_ref_bucle(std::unordered_set<int>& c) {
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
    [with _Iterator = std::detail::_Node_iterator<int, true, false>; 
    _Sequence = std::debug::unordered_set<int>; _Category = 
    std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffc6aa686e0 {
      type = std::detail::_Node_iterator<int, true, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int> >' @ 0x7ffc6aa687a0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
3678  (/tmp/mi-linter-runtime-validation/runtime_asan+0x307678) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x563728ba0aa5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x344aa5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x563728b5d1f0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3011f0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x563728aeaf22  (/tmp/mi-linter-runtime-validation/runtime_asan+0x28ef22) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x563728b448eb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e88eb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f12de827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f12de8278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x5637288fc2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x563728a61fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x563728b9b8d7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33f8d7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x563728b9a89c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e89c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x563728b9a3c2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e3c2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x563728b99af9  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33daf9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x563728b5cfd5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x300fd5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x563728afe437  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2437) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x563728b448de  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e88de) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f12de827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f12de8278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x5637288fc2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x28ef5a) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b32dd9dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b32dd9dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b32dd9dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b32dd9dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b32dd9dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b32dd9e0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x7b32dd9e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b32dd9e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b32dd9e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b32dd9e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b32dd9e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==407==ABORTING
````

</details>

### f_uset_clear_ref_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `llamada` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_uset_clear_ref_llamada(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_uset_clear(c);
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
aa5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x344aa5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5640e04391f0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3011f0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5640e03432ee  (/tmp/mi-linter-runtime-validation/runtime_asan+0x20b2ee) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5640e03c71f5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x28f1f5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x5640e0420a35  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e8a35) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7f8b1c227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7f8b1c2278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x5640e01d82c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5640e033dfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5640e04778d7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33f8d7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5640e047689c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e89c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5640e04763c2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e3c2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5640e0475af9  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33daf9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5640e0438fd5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x300fd5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5640e03da437  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2437) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5640e0420a28  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e8a28) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f8b1c227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f8b1c2278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x5640e01d82c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x28f22d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bab1b3dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bab1b3dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bab1b3dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bab1b3dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bab1b3dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bab1b3e0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x7bab1b3e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bab1b3e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bab1b3e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bab1b3e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bab1b3e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==409==ABORTING
````

</details>

## Handle: puntero

### f_uset_clear_ptr_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `recto` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_uset_clear_ptr_recto(std::unordered_set<int>& c) {
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
b678  (/tmp/mi-linter-runtime-validation/runtime_asan+0x307678) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x559471628aa5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x344aa5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5594715e51f0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3011f0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5594715733f6  (/tmp/mi-linter-runtime-validation/runtime_asan+0x28f3f6) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5594715ccb7f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e8b7f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f2d97e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f2d97e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x5594713842c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5594714e9fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5594716238d7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33f8d7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55947162289c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e89c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5594716223c2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e3c2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x559471621af9  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33daf9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5594715e4fd5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x300fd5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x559471586437  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2437) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5594715ccb72  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e8b72) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f2d97e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f2d97e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x5594713842c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x28f457) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b4d96fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b4d96fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b4d96fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b4d96fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b4d96fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b4d96fe0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x7b4d96fe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b4d96fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b4d96fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b4d96fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b4d96fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==411==ABORTING
````

</details>

### f_uset_clear_ptr_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `guarda` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_uset_clear_ptr_guarda(std::unordered_set<int>& c) {
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
5678  (/tmp/mi-linter-runtime-validation/runtime_asan+0x307678) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x559b01fa2aa5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x344aa5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x559b01f5f1f0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3011f0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x559b01eed67f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x28f67f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x559b01f46cc9  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e8cc9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f0287c27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f0287c278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x559b01cfe2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x559b01e63fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x559b01f9d8d7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33f8d7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x559b01f9c89c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e89c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x559b01f9c3c2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e3c2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x559b01f9baf9  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33daf9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x559b01f5efd5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x300fd5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x559b01f00437  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2437) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x559b01f46cbc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e8cbc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f0287c27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f0287c278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x559b01cfe2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x28f6e0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b2286ddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b2286ddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b2286ddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b2286ddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b2286ddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b2286de0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x7b2286de0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b2286de0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b2286de0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b2286de0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b2286de0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==413==ABORTING
````

</details>

### f_uset_clear_ptr_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_uset_clear_ptr_bucle(std::unordered_set<int>& c) {
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
    [with _Iterator = std::detail::_Node_iterator<int, true, false>; 
    _Sequence = std::debug::unordered_set<int>; _Category = 
    std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffd01143140 {
      type = std::detail::_Node_iterator<int, true, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int> >' @ 0x7ffd01143200
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
e678  (/tmp/mi-linter-runtime-validation/runtime_asan+0x307678) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55f30dedbaa5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x344aa5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55f30de981f0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3011f0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55f30de2698f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x28f98f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55f30de7fe13  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e8e13) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f72d4a27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f72d4a278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55f30dc372c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55f30dd9cfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55f30ded68d7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33f8d7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55f30ded589c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e89c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55f30ded53c2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e3c2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55f30ded4af9  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33daf9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55f30de97fd5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x300fd5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55f30de39437  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2437) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55f30de7fe06  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e8e06) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f72d4a27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f72d4a278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55f30dc372c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x28f9f3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b92d3bdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b92d3bdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b92d3bdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b92d3bdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b92d3bdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b92d3be0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x7b92d3be0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b92d3be0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b92d3be0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b92d3be0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b92d3be0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==415==ABORTING
````

</details>

### f_uset_clear_ptr_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `llamada` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_uset_clear_ptr_llamada(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_uset_clear(c);
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
aa5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x344aa5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55ddc4d791f0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3011f0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55ddc4c832ee  (/tmp/mi-linter-runtime-validation/runtime_asan+0x20b2ee) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55ddc4d07c4d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x28fc4d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55ddc4d60f5d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e8f5d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7fd63a427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7fd63a4278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x55ddc4b182c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55ddc4c7dfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55ddc4db78d7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33f8d7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55ddc4db689c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e89c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55ddc4db63c2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e3c2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55ddc4db5af9  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33daf9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55ddc4d78fd5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x300fd5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55ddc4d1a437  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2437) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55ddc4d60f50  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e8f50) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7fd63a427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7fd63a4278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55ddc4b182c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x28fcae) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bf6395dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf6395dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf6395dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf6395dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf6395dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bf6395e0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x7bf6395e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf6395e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf6395e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf6395e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf6395e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==417==ABORTING
````

</details>
