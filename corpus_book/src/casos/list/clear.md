# `std::list::clear`

Mutación: `c.clear();`

- Iterador retenido: 🔴 `UB`
- Referencia/puntero retenido: 🔴 `UB`
- Casos `UB` detectados estáticamente: 4/12

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🔴 avisa](#f_list_clear_it_recto) | [🔴 avisa](#f_list_clear_it_guarda) | [🔴 avisa](#f_list_clear_it_bucle) | [🔴 avisa](#f_list_clear_it_llamada) |
| **referencia** | [🔴 calla](#f_list_clear_ref_recto) | [🔴 calla](#f_list_clear_ref_guarda) | [🔴 calla](#f_list_clear_ref_bucle) | [🔴 calla](#f_list_clear_ref_llamada) |
| **puntero** | [🔴 calla](#f_list_clear_ptr_recto) | [🔴 calla](#f_list_clear_ptr_guarda) | [🔴 calla](#f_list_clear_ptr_bucle) | [🔴 calla](#f_list_clear_ptr_llamada) |

## Handle: iterador

### f_list_clear_it_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `recto` | 🔴 `UB` | ✅ detectado |

```cpp
void f_list_clear_it_recto(std::list<int>& c) {
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
    const [with _Iterator = std::_List_iterator<int>; _Sequence = std::
    debug::list<int>; _Category = std::forward_iterator_tag; reference = 
    int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffe56da4d60 {
      type = std::_List_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::list<int, std::allocator<int> >' @ 0x7ffe56da4de0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
cd  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2543cd) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55ecd1b8dd65  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2ccd65) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f462b027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f462b0278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55ecd19612c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55ecd1ac6fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55ecd1bec544  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b544) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55ecd1bec14f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b14f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55ecd1bebc9c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32ac9c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55ecd1c12941  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351941) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55ecd1c126e0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3516e0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55ecd1c1261d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35161d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55ecd1c122d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3512d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55ecd1bc5a20  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304a20) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55ecd1b619fa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a09fa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55ecd1b8dd58  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2ccd58) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f462b027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f462b0278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55ecd19612c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x254436) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b762a1dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b762a1dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b762a1dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b762a1dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b762a1dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b762a1e0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa fd fd
  0x7b762a1e0080: fd fa fa fa fd fd fd fa fa fa fa fa fa fa fa fa
  0x7b762a1e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b762a1e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b762a1e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b762a1e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==165==ABORTING
````

</details>

### f_list_clear_it_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `guarda` | 🔴 `UB` | ✅ detectado |

```cpp
void f_list_clear_it_guarda(std::list<int>& c) {
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
    const [with _Iterator = std::_List_iterator<int>; _Sequence = std::
    debug::list<int>; _Category = std::forward_iterator_tag; reference = 
    int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffeb89aaab0 {
      type = std::_List_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::list<int, std::allocator<int> >' @ 0x7ffeb89aab70
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
52  (/tmp/mi-linter-runtime-validation/runtime_asan+0x254652) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55f26551ce9b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cce9b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f6bbec27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f6bbec278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55f2652f02c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55f265455fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55f26557b544  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b544) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55f26557b14f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b14f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55f26557ac9c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32ac9c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55f2655a1941  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351941) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55f2655a16e0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3516e0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55f2655a161d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35161d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55f2655a12d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3512d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55f265554a20  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304a20) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55f2654f09fa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a09fa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55f26551ce8e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cce8e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f6bbec27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f6bbec278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55f2652f02c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x2546bb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b9bbdddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9bbdddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9bbdddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9bbdddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9bbdddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b9bbdde0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa fd fd
  0x7b9bbdde0080: fd fa fa fa fd fd fd fa fa fa fa fa fa fa fa fa
  0x7b9bbdde0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b9bbdde0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b9bbdde0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b9bbdde0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==167==ABORTING
````

</details>

### f_list_clear_it_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ✅ detectado |

```cpp
void f_list_clear_it_bucle(std::list<int>& c) {
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
    const [with _Iterator = std::_List_iterator<int>; _Sequence = std::
    debug::list<int>; _Category = std::forward_iterator_tag; reference = 
    int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffe3e232430 {
      type = std::_List_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::list<int, std::allocator<int> >' @ 0x7ffe3e2324f0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
68  (/tmp/mi-linter-runtime-validation/runtime_asan+0x254968) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55ba4d071fd1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2ccfd1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f67d8027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f67d80278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55ba4ce452c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55ba4cfaafe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55ba4d0d0544  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b544) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55ba4d0d014f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b14f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55ba4d0cfc9c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32ac9c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55ba4d0f6941  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351941) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55ba4d0f66e0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3516e0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55ba4d0f661d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35161d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55ba4d0f62d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3512d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55ba4d0a9a20  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304a20) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55ba4d0459fa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a09fa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55ba4d071fc4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2ccfc4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f67d8027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f67d80278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55ba4ce452c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x2549d1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b97d71dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b97d71dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b97d71dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b97d71dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b97d71dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b97d71e0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa fd fd
  0x7b97d71e0080: fd fa fa fa fd fd fd fa fa fa fa fa fa fa fa fa
  0x7b97d71e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b97d71e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b97d71e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b97d71e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==169==ABORTING
````

</details>

### f_list_clear_it_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `llamada` | 🔴 `UB` | ✅ detectado |

```cpp
void f_list_clear_it_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_list_clear(c);
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
    const [with _Iterator = std::_List_iterator<int>; _Sequence = std::
    debug::list<int>; _Category = std::forward_iterator_tag; reference = 
    int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffe18b698c0 {
      type = std::_List_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::list<int, std::allocator<int> >' @ 0x7ffe18b69980
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x254c10) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55b46c764107  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cd107) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f1ab6827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f1ab68278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55b46c5372c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55b46c69cfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55b46c7c2544  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b544) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55b46c7c214f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b14f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55b46c7c1c9c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32ac9c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55b46c7e8941  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351941) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55b46c7e86e0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3516e0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55b46c7e861d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35161d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55b46c7e82d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3512d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55b46c79ba20  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304a20) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55b46c7379fa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a09fa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55b46c7640fa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cd0fa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f1ab6827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f1ab68278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55b46c5372c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x254c79) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b4ab59dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b4ab59dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b4ab59dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b4ab59dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b4ab59dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b4ab59e0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa fd fd
  0x7b4ab59e0080: fd fa fa fa fd fd fd fa fa fa fa fa fa fa fa fa
  0x7b4ab59e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b4ab59e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b4ab59e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b4ab59e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==171==ABORTING
````

</details>

## Handle: referencia

### f_list_clear_ref_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `recto` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_list_clear_ref_recto(std::list<int>& c) {
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
79  (/tmp/mi-linter-runtime-validation/runtime_asan+0x254e79) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x563697dd423d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cd23d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f0560427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f05604278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x563697ba72c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x563697d0cfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x563697e32544  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b544) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x563697e3214f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b14f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x563697e31c9c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32ac9c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x563697e58941  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351941) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x563697e586e0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3516e0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x563697e5861d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35161d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x563697e582d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3512d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x563697e0ba20  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304a20) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x563697da79fa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a09fa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x563697dd4230  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cd230) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f0560427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f05604278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x563697ba72c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x254eae) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b355f5dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b355f5dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b355f5dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b355f5dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b355f5dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b355f5e0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa fd fd
  0x7b355f5e0080: fd fa fa fa fd fd fd fa fa fa fa fa fa fa fa fa
  0x7b355f5e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b355f5e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b355f5e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b355f5e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==173==ABORTING
````

</details>

### f_list_clear_ref_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `guarda` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_list_clear_ref_guarda(std::list<int>& c) {
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
27  (/tmp/mi-linter-runtime-validation/runtime_asan+0x255127) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55e6e9602373  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cd373) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7fc028227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7fc0282278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55e6e93d52c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55e6e953afe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55e6e9660544  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b544) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55e6e966014f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b14f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55e6e965fc9c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32ac9c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55e6e9686941  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351941) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55e6e96866e0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3516e0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55e6e968661d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35161d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55e6e96862d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3512d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55e6e9639a20  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304a20) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55e6e95d59fa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a09fa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55e6e9602366  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cd366) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7fc028227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7fc0282278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55e6e93d52c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x25515f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bf0273dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf0273dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf0273dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf0273dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf0273dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bf0273e0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa fd fd
  0x7bf0273e0080: fd fa fa fa fd fd fd fa fa fa fa fa fa fa fa fa
  0x7bf0273e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf0273e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf0273e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf0273e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==175==ABORTING
````

</details>

### f_list_clear_ref_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_list_clear_ref_bucle(std::list<int>& c) {
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
    [with _Iterator = std::_List_iterator<int>; _Sequence = std::
    debug::list<int>; _Category = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffecbb4a350 {
      type = std::_List_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::list<int, std::allocator<int> >' @ 0x7ffecbb4a410
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
52  (/tmp/mi-linter-runtime-validation/runtime_asan+0x255452) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55af08a7e4a9  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cd4a9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f5aeae27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f5aeae278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55af088512c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55af089b6fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55af08adc544  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b544) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55af08adc14f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b14f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55af08adbc9c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32ac9c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55af08b02941  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351941) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55af08b026e0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3516e0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55af08b0261d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35161d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55af08b022d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3512d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55af08ab5a20  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304a20) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55af08a519fa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a09fa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55af08a7e49c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cd49c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f5aeae27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f5aeae278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55af088512c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x25548a) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b8ae9fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b8ae9fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b8ae9fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b8ae9fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b8ae9fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b8ae9fe0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa fd fd
  0x7b8ae9fe0080: fd fa fa fa fd fd fd fa fa fa fa fa fa fa fa fa
  0x7b8ae9fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b8ae9fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b8ae9fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b8ae9fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==177==ABORTING
````

</details>

### f_list_clear_ref_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `llamada` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_list_clear_ref_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_list_clear(c);
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
5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x255725) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x56533ce505df  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cd5df) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fb67b227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fb67b2278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x56533cc232c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x56533cd88fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x56533ceae544  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b544) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x56533ceae14f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b14f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x56533ceadc9c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32ac9c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x56533ced4941  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351941) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x56533ced46e0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3516e0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x56533ced461d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35161d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x56533ced42d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3512d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x56533ce87a20  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304a20) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x56533ce239fa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a09fa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x56533ce505d2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cd5d2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7fb67b227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7fb67b2278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x56533cc232c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x25575d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7be67a3dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7be67a3dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7be67a3dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7be67a3dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7be67a3dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7be67a3e0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa fd fd
  0x7be67a3e0080: fd fa fa fa fd fd fd fa fa fa fa fa fa fa fa fa
  0x7be67a3e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7be67a3e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7be67a3e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7be67a3e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==179==ABORTING
````

</details>

## Handle: puntero

### f_list_clear_ptr_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `recto` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_list_clear_ptr_recto(std::list<int>& c) {
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
26  (/tmp/mi-linter-runtime-validation/runtime_asan+0x255926) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x563b4bb15715  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cd715) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f5babc27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f5babc278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x563b4b8e82c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x563b4ba4dfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x563b4bb73544  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b544) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x563b4bb7314f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b14f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x563b4bb72c9c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32ac9c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x563b4bb99941  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351941) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x563b4bb996e0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3516e0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x563b4bb9961d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35161d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x563b4bb992d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3512d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x563b4bb4ca20  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304a20) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x563b4bae89fa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a09fa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x563b4bb15708  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cd708) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f5babc27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f5babc278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x563b4b8e82c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x255987) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b8baaddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b8baaddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b8baaddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b8baaddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b8baaddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b8baade0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa fd fd
  0x7b8baade0080: fd fa fa fa fd fd fd fa fa fa fa fa fa fa fa fa
  0x7b8baade0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b8baade0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b8baade0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b8baade0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==181==ABORTING
````

</details>

### f_list_clear_ptr_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `guarda` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_list_clear_ptr_guarda(std::list<int>& c) {
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
af  (/tmp/mi-linter-runtime-validation/runtime_asan+0x255baf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x559de158584b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cd84b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f439da27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f439da278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x559de13582c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x559de14bdfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x559de15e3544  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b544) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x559de15e314f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b14f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x559de15e2c9c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32ac9c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x559de1609941  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351941) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x559de16096e0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3516e0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x559de160961d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35161d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x559de16092d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3512d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x559de15bca20  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304a20) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x559de15589fa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a09fa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x559de158583e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cd83e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f439da27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f439da278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x559de13582c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x255c10) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b739cbdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b739cbdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b739cbdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b739cbdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b739cbdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b739cbe0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa fd fd
  0x7b739cbe0080: fd fa fa fa fd fd fd fa fa fa fa fa fa fa fa fa
  0x7b739cbe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b739cbe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b739cbe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b739cbe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==183==ABORTING
````

</details>

### f_list_clear_ptr_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_list_clear_ptr_bucle(std::list<int>& c) {
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
    [with _Iterator = std::_List_iterator<int>; _Sequence = std::
    debug::list<int>; _Category = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fff3e67a890 {
      type = std::_List_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::list<int, std::allocator<int> >' @ 0x7fff3e67a950
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
bf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x255ebf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x561c851ac981  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cd981) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f871d027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f871d0278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x561c84f7f2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x561c850e4fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x561c8520a544  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b544) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x561c8520a14f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b14f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x561c85209c9c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32ac9c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x561c85230941  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351941) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x561c852306e0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3516e0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x561c8523061d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35161d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x561c852302d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3512d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x561c851e3a20  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304a20) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x561c8517f9fa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a09fa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x561c851ac974  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cd974) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f871d027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f871d0278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x561c84f7f2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x255f23) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bb71c1dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bb71c1dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bb71c1dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bb71c1dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bb71c1dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bb71c1e0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa fd fd
  0x7bb71c1e0080: fd fa fa fa fd fd fd fa fa fa fa fa fa fa fa fa
  0x7bb71c1e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bb71c1e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bb71c1e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bb71c1e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==185==ABORTING
````

</details>

### f_list_clear_ptr_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `llamada` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_list_clear_ptr_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_list_clear(c);
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
d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x25617d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x557468e1dab7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cdab7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f65c5c27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f65c5c278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x557468bf02c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x557468d55fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x557468e7b544  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b544) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x557468e7b14f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b14f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x557468e7ac9c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32ac9c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x557468ea1941  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351941) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x557468ea16e0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3516e0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x557468ea161d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35161d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x557468ea12d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3512d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x557468e54a20  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304a20) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x557468df09fa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a09fa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x557468e1daaa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cdaaa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f65c5c27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f65c5c278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x557468bf02c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x2561de) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b95c4ddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b95c4ddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b95c4ddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b95c4ddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b95c4ddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b95c4de0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa fd fd
  0x7b95c4de0080: fd fa fa fa fd fd fd fa fa fa fa fa fa fa fa fa
  0x7b95c4de0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b95c4de0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b95c4de0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b95c4de0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==187==ABORTING
````

</details>
