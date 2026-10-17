# `std::forward_list::clear`

Mutación: `c.clear();`

- Iterador retenido: 🔴 `UB`
- Referencia/puntero retenido: 🔴 `UB`
- Casos `UB` detectados estáticamente: 4/12

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🔴 avisa](#f_flist_clear_it_recto) | [🔴 avisa](#f_flist_clear_it_guarda) | [🔴 avisa](#f_flist_clear_it_bucle) | [🔴 avisa](#f_flist_clear_it_llamada) |
| **referencia** | [🔴 calla](#f_flist_clear_ref_recto) | [🔴 calla](#f_flist_clear_ref_guarda) | [🔴 calla](#f_flist_clear_ref_bucle) | [🔴 calla](#f_flist_clear_ref_llamada) |
| **puntero** | [🔴 calla](#f_flist_clear_ptr_recto) | [🔴 calla](#f_flist_clear_ptr_guarda) | [🔴 calla](#f_flist_clear_ptr_bucle) | [🔴 calla](#f_flist_clear_ptr_llamada) |

## Handle: iterador

### f_flist_clear_it_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `recto` | 🔴 `UB` | ✅ detectado |

```cpp
void f_flist_clear_it_recto(std::forward_list<int>& c) {
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
    const [with _Iterator = std::_Fwd_list_iterator<int>; _Sequence = std::
    debug::forward_list<int>; _Category = std::forward_iterator_tag; 
    reference = int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffd09a4ace0 {
      type = std::_Fwd_list_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::forward_list<int, std::allocator<int> >' @ 0x7ffd09a4ad60
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
a23e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33123e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55701c6d7e6c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fee6c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55701c63e68d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x26568d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55701c6adcd0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d4cd0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7fad4a227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7fad4a2278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55701c4792c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55701c5defe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55701c709687  (/tmp/mi-linter-runtime-validation/runtime_asan+0x330687) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55701c70928f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33028f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55701c708d5c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32fd5c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55701c72b3d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3523d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55701c72ae13  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351e13) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55701c6dde40  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304e40) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55701c679dea  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a0dea) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55701c6adcc3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d4cc3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fad4a227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fad4a2278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55701c4792c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x2656f6) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bcd493dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bcd493dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bcd493dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bcd493dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bcd493dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bcd493e0000: fa fa fd[fd]fa fa fd fd fa fa fd fd fa fa fa fa
  0x7bcd493e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bcd493e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bcd493e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bcd493e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bcd493e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==357==ABORTING
````

</details>

### f_flist_clear_it_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `guarda` | 🔴 `UB` | ✅ detectado |

```cpp
void f_flist_clear_it_guarda(std::forward_list<int>& c) {
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
    const [with _Iterator = std::_Fwd_list_iterator<int>; _Sequence = std::
    debug::forward_list<int>; _Category = std::forward_iterator_tag; 
    reference = int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fffb4351320 {
      type = std::_Fwd_list_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::forward_list<int, std::allocator<int> >' @ 0x7fffb43513e0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
823e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33123e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55d953f65e6c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fee6c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55d953ecc912  (/tmp/mi-linter-runtime-validation/runtime_asan+0x265912) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55d953f3bdf4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d4df4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7fb67e827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7fb67e8278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55d953d072c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55d953e6cfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55d953f97687  (/tmp/mi-linter-runtime-validation/runtime_asan+0x330687) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55d953f9728f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33028f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55d953f96d5c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32fd5c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55d953fb93d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3523d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55d953fb8e13  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351e13) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55d953f6be40  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304e40) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55d953f07dea  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a0dea) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55d953f3bde7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d4de7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fb67e827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fb67e8278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55d953d072c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x26597b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bd67d9dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd67d9dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd67d9dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd67d9dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd67d9dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bd67d9e0000: fa fa fd[fd]fa fa fd fd fa fa fd fd fa fa fa fa
  0x7bd67d9e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd67d9e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd67d9e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd67d9e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd67d9e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==359==ABORTING
````

</details>

### f_flist_clear_it_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ✅ detectado |

```cpp
void f_flist_clear_it_bucle(std::forward_list<int>& c) {
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
    const [with _Iterator = std::_Fwd_list_iterator<int>; _Sequence = std::
    debug::forward_list<int>; _Category = std::forward_iterator_tag; 
    reference = int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffcf1d131f0 {
      type = std::_Fwd_list_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::forward_list<int, std::allocator<int> >' @ 0x7ffcf1d132b0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
f23e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33123e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5598eb41ce6c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fee6c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5598eb383c28  (/tmp/mi-linter-runtime-validation/runtime_asan+0x265c28) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5598eb3f2f18  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d4f18) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f77c5427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f77c54278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x5598eb1be2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5598eb323fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5598eb44e687  (/tmp/mi-linter-runtime-validation/runtime_asan+0x330687) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5598eb44e28f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33028f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5598eb44dd5c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32fd5c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5598eb4703d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3523d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5598eb46fe13  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351e13) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5598eb422e40  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304e40) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5598eb3bedea  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a0dea) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5598eb3f2f0b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d4f0b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f77c5427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f77c54278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x5598eb1be2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x265c91) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b97c45dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b97c45dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b97c45dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b97c45dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b97c45dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b97c45e0000: fa fa fd[fd]fa fa fd fd fa fa fd fd fa fa fa fa
  0x7b97c45e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b97c45e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b97c45e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b97c45e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b97c45e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==361==ABORTING
````

</details>

### f_flist_clear_it_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `llamada` | 🔴 `UB` | ✅ detectado |

```cpp
void f_flist_clear_it_llamada(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_flist_clear(c);
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
    const [with _Iterator = std::_Fwd_list_iterator<int>; _Sequence = std::
    debug::forward_list<int>; _Category = std::forward_iterator_tag; 
    reference = int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffc5e638420 {
      type = std::_Fwd_list_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::forward_list<int, std::allocator<int> >' @ 0x7ffc5e6384e0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
e6c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fee6c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x555e886cd19e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x20a19e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x555e88728ed0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x265ed0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x555e8879803c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d503c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f26e8e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f26e8e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x555e885632c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x555e886c8fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x555e887f3687  (/tmp/mi-linter-runtime-validation/runtime_asan+0x330687) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x555e887f328f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33028f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x555e887f2d5c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32fd5c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x555e888153d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3523d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x555e88814e13  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351e13) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x555e887c7e40  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304e40) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x555e88763dea  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a0dea) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x555e8879802f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d502f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f26e8e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f26e8e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x555e885632c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x265f39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b46e7fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b46e7fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b46e7fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b46e7fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b46e7fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b46e7fe0000: fa fa fd[fd]fa fa fd fd fa fa fd fd fa fa fa fa
  0x7b46e7fe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b46e7fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b46e7fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b46e7fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b46e7fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==363==ABORTING
````

</details>

## Handle: referencia

### f_flist_clear_ref_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `recto` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_flist_clear_ref_recto(std::forward_list<int>& c) {
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
523e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33123e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x56128d9a2e6c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fee6c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x56128d90a139  (/tmp/mi-linter-runtime-validation/runtime_asan+0x266139) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x56128d979160  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d5160) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f36fd627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f36fd6278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x56128d7442c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x56128d8a9fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x56128d9d4687  (/tmp/mi-linter-runtime-validation/runtime_asan+0x330687) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x56128d9d428f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33028f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x56128d9d3d5c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32fd5c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x56128d9f63d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3523d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x56128d9f5e13  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351e13) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x56128d9a8e40  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304e40) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x56128d944dea  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a0dea) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x56128d979153  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d5153) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f36fd627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f36fd6278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x56128d7442c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x26616e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b56fc7dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b56fc7dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b56fc7dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b56fc7dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b56fc7dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b56fc7e0000: fa fa fd[fd]fa fa fd fd fa fa fd fd fa fa fa fa
  0x7b56fc7e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b56fc7e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b56fc7e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b56fc7e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b56fc7e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==365==ABORTING
````

</details>

### f_flist_clear_ref_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `guarda` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_flist_clear_ref_guarda(std::forward_list<int>& c) {
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
123e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33123e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55f6b6a3ee6c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fee6c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55f6b69a63e7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2663e7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55f6b6a15284  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d5284) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f5378e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f5378e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55f6b67e02c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55f6b6945fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55f6b6a70687  (/tmp/mi-linter-runtime-validation/runtime_asan+0x330687) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55f6b6a7028f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33028f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55f6b6a6fd5c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32fd5c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55f6b6a923d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3523d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55f6b6a91e13  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351e13) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55f6b6a44e40  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304e40) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55f6b69e0dea  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a0dea) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55f6b6a15277  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d5277) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f5378e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f5378e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55f6b67e02c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x26641f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b7377fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b7377fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b7377fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b7377fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b7377fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b7377fe0000: fa fa fd[fd]fa fa fd fd fa fa fd fd fa fa fa fa
  0x7b7377fe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b7377fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b7377fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b7377fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b7377fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==367==ABORTING
````

</details>

### f_flist_clear_ref_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_flist_clear_ref_bucle(std::forward_list<int>& c) {
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
    [with _Iterator = std::_Fwd_list_iterator<int>; _Sequence = std::
    debug::forward_list<int>; _Category = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffd7fc4c980 {
      type = std::_Fwd_list_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::forward_list<int, std::allocator<int> >' @ 0x7ffd7fc4ca40
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
523e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33123e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55af68192e6c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fee6c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55af680fa712  (/tmp/mi-linter-runtime-validation/runtime_asan+0x266712) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55af681693a8  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d53a8) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f2d83227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f2d832278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55af67f342c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55af68099fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55af681c4687  (/tmp/mi-linter-runtime-validation/runtime_asan+0x330687) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55af681c428f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33028f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55af681c3d5c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32fd5c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55af681e63d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3523d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55af681e5e13  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351e13) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55af68198e40  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304e40) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55af68134dea  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a0dea) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55af6816939b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d539b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f2d83227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f2d832278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55af67f342c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x26674a) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b4d823dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b4d823dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b4d823dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b4d823dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b4d823dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b4d823e0000: fa fa fd[fd]fa fa fd fd fa fa fd fd fa fa fa fa
  0x7b4d823e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b4d823e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b4d823e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b4d823e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b4d823e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==369==ABORTING
````

</details>

### f_flist_clear_ref_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `llamada` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_flist_clear_ref_llamada(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_flist_clear(c);
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
e6c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fee6c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x562161aa619e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x20a19e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x562161b029e5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2669e5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x562161b714cc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d54cc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fd6e9c27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fd6e9c278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x56216193c2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x562161aa1fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x562161bcc687  (/tmp/mi-linter-runtime-validation/runtime_asan+0x330687) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x562161bcc28f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33028f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x562161bcbd5c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32fd5c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x562161bee3d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3523d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x562161bede13  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351e13) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x562161ba0e40  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304e40) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x562161b3cdea  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a0dea) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x562161b714bf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d54bf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fd6e9c27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fd6e9c278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x56216193c2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x266a1d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bf6e8ddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf6e8ddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf6e8ddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf6e8ddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf6e8ddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bf6e8de0000: fa fa fd[fd]fa fa fd fd fa fa fd fd fa fa fa fa
  0x7bf6e8de0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf6e8de0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf6e8de0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf6e8de0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf6e8de0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==371==ABORTING
````

</details>

## Handle: puntero

### f_flist_clear_ptr_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `recto` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_flist_clear_ptr_recto(std::forward_list<int>& c) {
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
823e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33123e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55ea01af5e6c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fee6c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55ea01a5dbe6  (/tmp/mi-linter-runtime-validation/runtime_asan+0x266be6) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55ea01acc5f0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d55f0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7fef9ae27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7fef9ae278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55ea018972c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55ea019fcfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55ea01b27687  (/tmp/mi-linter-runtime-validation/runtime_asan+0x330687) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55ea01b2728f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33028f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55ea01b26d5c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32fd5c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55ea01b493d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3523d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55ea01b48e13  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351e13) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55ea01afbe40  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304e40) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55ea01a97dea  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a0dea) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55ea01acc5e3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d55e3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fef9ae27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fef9ae278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55ea018972c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x266c47) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c0f99fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c0f99fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c0f99fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c0f99fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c0f99fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c0f99fe0000: fa fa fd[fd]fa fa fd fd fa fa fd fd fa fa fa fa
  0x7c0f99fe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c0f99fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c0f99fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c0f99fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c0f99fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==373==ABORTING
````

</details>

### f_flist_clear_ptr_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `guarda` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_flist_clear_ptr_guarda(std::forward_list<int>& c) {
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
023e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33123e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x56221150de6c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fee6c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x562211475e6f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x266e6f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5622114e4714  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d5714) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f3d71e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f3d71e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x5622112af2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x562211414fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x56221153f687  (/tmp/mi-linter-runtime-validation/runtime_asan+0x330687) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x56221153f28f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33028f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x56221153ed5c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32fd5c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5622115613d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3523d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x562211560e13  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351e13) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x562211513e40  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304e40) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5622114afdea  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a0dea) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5622114e4707  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d5707) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f3d71e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f3d71e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x5622112af2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x266ed0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b5d70fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b5d70fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b5d70fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b5d70fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b5d70fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b5d70fe0000: fa fa fd[fd]fa fa fd fd fa fa fd fd fa fa fa fa
  0x7b5d70fe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b5d70fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b5d70fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b5d70fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b5d70fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==375==ABORTING
````

</details>

### f_flist_clear_ptr_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_flist_clear_ptr_bucle(std::forward_list<int>& c) {
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
    [with _Iterator = std::_Fwd_list_iterator<int>; _Sequence = std::
    debug::forward_list<int>; _Category = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffec3de33e0 {
      type = std::_Fwd_list_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::forward_list<int, std::allocator<int> >' @ 0x7ffec3de34a0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
723e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33123e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55e039234e6c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fee6c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55e03919d17f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x26717f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55e03920b838  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d5838) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7fb6fd027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7fb6fd0278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55e038fd62c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55e03913bfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55e039266687  (/tmp/mi-linter-runtime-validation/runtime_asan+0x330687) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55e03926628f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33028f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55e039265d5c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32fd5c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55e0392883d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3523d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55e039287e13  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351e13) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55e03923ae40  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304e40) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55e0391d6dea  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a0dea) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55e03920b82b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d582b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fb6fd027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fb6fd0278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55e038fd62c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x2671e3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bd6fc1dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd6fc1dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd6fc1dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd6fc1dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd6fc1dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bd6fc1e0000: fa fa fd[fd]fa fa fd fd fa fa fd fd fa fa fa fa
  0x7bd6fc1e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd6fc1e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd6fc1e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd6fc1e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd6fc1e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==377==ABORTING
````

</details>

### f_flist_clear_ptr_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `llamada` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_flist_clear_ptr_llamada(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_flist_clear(c);
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
e6c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fee6c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x561e546b719e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x20a19e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x561e5471443d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x26743d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x561e5478295c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d595c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f7c74627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f7c746278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x561e5454d2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x561e546b2fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x561e547dd687  (/tmp/mi-linter-runtime-validation/runtime_asan+0x330687) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x561e547dd28f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33028f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x561e547dcd5c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32fd5c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x561e547ff3d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3523d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x561e547fee13  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351e13) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x561e547b1e40  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304e40) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x561e5474ddea  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a0dea) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x561e5478294f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d594f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f7c74627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f7c746278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x561e5454d2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x26749e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b9c737dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9c737dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9c737dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9c737dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9c737dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b9c737e0000: fa fa fd[fd]fa fa fd fd fa fa fd fd fa fa fa fa
  0x7b9c737e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b9c737e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b9c737e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b9c737e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b9c737e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==379==ABORTING
````

</details>
