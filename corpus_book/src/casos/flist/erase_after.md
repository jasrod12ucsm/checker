# `std::forward_list::erase_after`

Mutación: `c.erase_after(c.before_begin());`

- Iterador retenido: 🔴 `UB`
- Referencia/puntero retenido: 🔴 `UB`
- Casos `UB` detectados estáticamente: 1/12

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🔴 calla](#f_flist_erase_after_it_recto) | [🔴 calla](#f_flist_erase_after_it_guarda) | [🔴 avisa](#f_flist_erase_after_it_bucle) | [🔴 calla](#f_flist_erase_after_it_llamada) |
| **referencia** | [🔴 calla](#f_flist_erase_after_ref_recto) | [🔴 calla](#f_flist_erase_after_ref_guarda) | [🔴 calla](#f_flist_erase_after_ref_bucle) | [🔴 calla](#f_flist_erase_after_ref_llamada) |
| **puntero** | [🔴 calla](#f_flist_erase_after_ptr_recto) | [🔴 calla](#f_flist_erase_after_ptr_guarda) | [🔴 calla](#f_flist_erase_after_ptr_bucle) | [🔴 calla](#f_flist_erase_after_ptr_llamada) |

## Handle: iterador

### f_flist_erase_after_it_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `recto` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_flist_erase_after_it_recto(std::forward_list<int>& c) {
  auto it = c.begin();
  c.erase_after(c.before_begin());
  sink(*it);
}
```

> **Causa del falso negativo:** 2. Sin comparacion previa contra end(), el modelado no se activa

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
    iterator "this" @ 0x7ffebbe26130 {
      type = std::_Fwd_list_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::forward_list<int, std::allocator<int> >' @ 0x7ffebbe26250
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
5dc3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x330dc3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x560b725e3d1b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fed1b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x560b7254804a  (/tmp/mi-linter-runtime-validation/runtime_asan+0x26304a) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x560b725b8c8c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d3c8c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f4c2a227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f4c2a2278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x560b723852c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x560b724eafe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x560b72615687  (/tmp/mi-linter-runtime-validation/runtime_asan+0x330687) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x560b7261528f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33028f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x560b72614d5c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32fd5c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x560b726373d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3523d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x560b72636e13  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351e13) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x560b725e9e40  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304e40) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x560b72585dea  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a0dea) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x560b725b8c7f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d3c7f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f4c2a227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f4c2a2278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x560b723852c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x2630c2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b6c293dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b6c293dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b6c293dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b6c293dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b6c293dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b6c293e0000: fa fa fd[fd]fa fa 00 00 fa fa 00 00 fa fa fa fa
  0x7b6c293e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b6c293e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b6c293e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b6c293e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b6c293e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==333==ABORTING
````

</details>

### f_flist_erase_after_it_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `guarda` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_flist_erase_after_it_guarda(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.erase_after(c.before_begin());
  sink(*it);
}
```

> **Causa del falso negativo:** 3. Se invalida por identidad del iterador, no por posicion

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
    iterator "this" @ 0x7ffd84b0a560 {
      type = std::_Fwd_list_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::forward_list<int, std::allocator<int> >' @ 0x7ffd84b0a680
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
edc3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x330dc3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5641fd00cd1b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fed1b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5641fcf7138d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x26338d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5641fcfe1de7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d3de7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f4cc1027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f4cc10278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x5641fcdae2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5641fcf13fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5641fd03e687  (/tmp/mi-linter-runtime-validation/runtime_asan+0x330687) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5641fd03e28f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33028f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5641fd03dd5c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32fd5c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5641fd0603d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3523d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5641fd05fe13  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351e13) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5641fd012e40  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304e40) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5641fcfaedea  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a0dea) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5641fcfe1dda  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d3dda) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f4cc1027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f4cc10278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x5641fcdae2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x263408) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b6cc01dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b6cc01dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b6cc01dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b6cc01dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b6cc01dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b6cc01e0000: fa fa fd[fd]fa fa 00 00 fa fa 00 00 fa fa fa fa
  0x7b6cc01e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b6cc01e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b6cc01e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b6cc01e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b6cc01e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==335==ABORTING
````

</details>

### f_flist_erase_after_it_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ✅ detectado |

```cpp
void f_flist_erase_after_it_bucle(std::forward_list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.erase_after(c.before_begin());
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
    iterator "this" @ 0x7ffc740bc7f0 {
      type = std::_Fwd_list_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::forward_list<int, std::allocator<int> >' @ 0x7ffc740bc910
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
fdc3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x330dc3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55ac0902dd1b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fed1b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55ac08f92776  (/tmp/mi-linter-runtime-validation/runtime_asan+0x263776) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55ac09002f42  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d3f42) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7fb8f4c27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7fb8f4c278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55ac08dcf2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55ac08f34fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55ac0905f687  (/tmp/mi-linter-runtime-validation/runtime_asan+0x330687) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55ac0905f28f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33028f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55ac0905ed5c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32fd5c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55ac090813d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3523d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55ac09080e13  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351e13) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55ac09033e40  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304e40) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55ac08fcfdea  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a0dea) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55ac09002f35  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d3f35) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fb8f4c27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fb8f4c278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55ac08dcf2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x2637f1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bd8f3ddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd8f3ddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd8f3ddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd8f3ddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd8f3ddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bd8f3de0000: fa fa fd[fd]fa fa 00 00 fa fa 00 00 fa fa fa fa
  0x7bd8f3de0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd8f3de0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd8f3de0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd8f3de0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd8f3de0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==337==ABORTING
````

</details>

### f_flist_erase_after_it_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `llamada` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_flist_erase_after_it_llamada(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_flist_erase_after(c);
  sink(*it);
}
```

> **Causa del falso negativo:** 3. Se invalida por identidad del iterador, no por posicion

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
    iterator "this" @ 0x7ffc51fbc590 {
      type = std::_Fwd_list_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::forward_list<int, std::allocator<int> >' @ 0x7ffc51fbc650
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
d1b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fed1b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x56231b3860dd  (/tmp/mi-linter-runtime-validation/runtime_asan+0x20a0dd) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x56231b3dfa60  (/tmp/mi-linter-runtime-validation/runtime_asan+0x263a60) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x56231b45009d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d409d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fa317827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fa3178278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x56231b21c2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x56231b381fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x56231b4ac687  (/tmp/mi-linter-runtime-validation/runtime_asan+0x330687) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x56231b4ac28f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33028f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x56231b4abd5c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32fd5c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x56231b4ce3d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3523d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x56231b4cde13  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351e13) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x56231b480e40  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304e40) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x56231b41cdea  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a0dea) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x56231b450090  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d4090) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fa317827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fa3178278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x56231b21c2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x263ac9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bc3169dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bc3169dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bc3169dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bc3169dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bc3169dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bc3169e0000: fa fa fd[fd]fa fa 00 00 fa fa 00 00 fa fa fa fa
  0x7bc3169e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bc3169e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bc3169e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bc3169e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bc3169e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==339==ABORTING
````

</details>

## Handle: referencia

### f_flist_erase_after_ref_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `recto` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_flist_erase_after_ref_recto(std::forward_list<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.erase_after(c.before_begin());
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
bdc3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x330dc3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55ebbed99d1b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fed1b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55ebbecfed55  (/tmp/mi-linter-runtime-validation/runtime_asan+0x263d55) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55ebbed6f1f8  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d41f8) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7fb6bcc27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7fb6bcc278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55ebbeb3b2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55ebbeca0fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55ebbedcb687  (/tmp/mi-linter-runtime-validation/runtime_asan+0x330687) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55ebbedcb28f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33028f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55ebbedcad5c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32fd5c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55ebbeded3d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3523d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55ebbedece13  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351e13) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55ebbed9fe40  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304e40) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55ebbed3bdea  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a0dea) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55ebbed6f1eb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d41eb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fb6bcc27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fb6bcc278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55ebbeb3b2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x263d9f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bd6bbddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd6bbddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd6bbddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd6bbddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd6bbddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bd6bbde0000: fa fa fd[fd]fa fa 00 00 fa fa 00 00 fa fa fa fa
  0x7bd6bbde0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd6bbde0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd6bbde0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd6bbde0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd6bbde0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==341==ABORTING
````

</details>

### f_flist_erase_after_ref_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `guarda` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_flist_erase_after_ref_guarda(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.erase_after(c.before_begin());
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
4dc3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x330dc3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x563e67a92d1b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fed1b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x563e679f80c5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2640c5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x563e67a68353  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d4353) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f8fb7627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f8fb76278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x563e678342c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x563e67999fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x563e67ac4687  (/tmp/mi-linter-runtime-validation/runtime_asan+0x330687) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x563e67ac428f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33028f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x563e67ac3d5c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32fd5c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x563e67ae63d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3523d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x563e67ae5e13  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351e13) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x563e67a98e40  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304e40) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x563e67a34dea  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a0dea) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x563e67a68346  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d4346) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f8fb7627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f8fb76278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x563e678342c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x26410f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bafb67dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bafb67dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bafb67dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bafb67dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bafb67dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bafb67e0000: fa fa fd[fd]fa fa 00 00 fa fa 00 00 fa fa fa fa
  0x7bafb67e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bafb67e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bafb67e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bafb67e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bafb67e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==343==ABORTING
````

</details>

### f_flist_erase_after_ref_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_flist_erase_after_ref_bucle(std::forward_list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.erase_after(c.before_begin());
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
    iterator "this" @ 0x7ffd1a9bd940 {
      type = std::_Fwd_list_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::forward_list<int, std::allocator<int> >' @ 0x7ffd1a9bda60
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
9dc3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x330dc3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x56232dfb7d1b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fed1b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x56232df1d4b0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2644b0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x56232df8d4ae  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d44ae) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f783f427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f783f4278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x56232dd592c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x56232debefe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x56232dfe9687  (/tmp/mi-linter-runtime-validation/runtime_asan+0x330687) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x56232dfe928f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33028f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x56232dfe8d5c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32fd5c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x56232e00b3d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3523d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x56232e00ae13  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351e13) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x56232dfbde40  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304e40) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x56232df59dea  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a0dea) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x56232df8d4a1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d44a1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f783f427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f783f4278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x56232dd592c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x2644fa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b983e5dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b983e5dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b983e5dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b983e5dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b983e5dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b983e5e0000: fa fa fd[fd]fa fa 00 00 fa fa 00 00 fa fa fa fa
  0x7b983e5e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b983e5e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b983e5e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b983e5e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b983e5e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==345==ABORTING
````

</details>

### f_flist_erase_after_ref_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `llamada` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_flist_erase_after_ref_llamada(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_flist_erase_after(c);
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
d1b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fed1b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x557d5e6480dd  (/tmp/mi-linter-runtime-validation/runtime_asan+0x20a0dd) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x557d5e6a27c5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2647c5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x557d5e712609  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d4609) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f3461827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f34618278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x557d5e4de2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x557d5e643fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x557d5e76e687  (/tmp/mi-linter-runtime-validation/runtime_asan+0x330687) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x557d5e76e28f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33028f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x557d5e76dd5c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32fd5c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x557d5e7903d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3523d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x557d5e78fe13  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351e13) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x557d5e742e40  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304e40) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x557d5e6dedea  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a0dea) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x557d5e7125fc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d45fc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f3461827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f34618278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x557d5e4de2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x2647fd) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b54609dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b54609dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b54609dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b54609dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b54609dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b54609e0000: fa fa fd[fd]fa fa 00 00 fa fa 00 00 fa fa fa fa
  0x7b54609e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b54609e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b54609e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b54609e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b54609e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==347==ABORTING
````

</details>

## Handle: puntero

### f_flist_erase_after_ptr_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `recto` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_flist_erase_after_ptr_recto(std::forward_list<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.erase_after(c.before_begin());
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
3dc3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x330dc3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x559d661c1d1b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fed1b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x559d66127a52  (/tmp/mi-linter-runtime-validation/runtime_asan+0x264a52) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x559d66197764  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d4764) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7fda26a27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7fda26a278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x559d65f632c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x559d660c8fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x559d661f3687  (/tmp/mi-linter-runtime-validation/runtime_asan+0x330687) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x559d661f328f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33028f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x559d661f2d5c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32fd5c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x559d662153d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3523d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x559d66214e13  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351e13) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x559d661c7e40  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304e40) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x559d66163dea  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a0dea) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x559d66197757  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d4757) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fda26a27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fda26a278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x559d65f632c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x264ac8) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bfa25bdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bfa25bdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bfa25bdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bfa25bdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bfa25bdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bfa25be0000: fa fa fd[fd]fa fa 00 00 fa fa 00 00 fa fa fa fa
  0x7bfa25be0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bfa25be0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bfa25be0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bfa25be0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bfa25be0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==349==ABORTING
````

</details>

### f_flist_erase_after_ptr_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `guarda` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_flist_erase_after_ptr_guarda(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.erase_after(c.before_begin());
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
adc3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x330dc3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x561715238d1b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fed1b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x56171519ed9a  (/tmp/mi-linter-runtime-validation/runtime_asan+0x264d9a) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x56171520e8bf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d48bf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f0493a27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f0493a278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x561714fda2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x56171513ffe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x56171526a687  (/tmp/mi-linter-runtime-validation/runtime_asan+0x330687) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x56171526a28f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33028f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x561715269d5c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32fd5c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x56171528c3d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3523d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x56171528be13  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351e13) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x56171523ee40  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304e40) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5617151dadea  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a0dea) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x56171520e8b2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d48b2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f0493a27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f0493a278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x561714fda2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x264e10) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b2492bdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b2492bdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b2492bdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b2492bdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b2492bdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b2492be0000: fa fa fd[fd]fa fa 00 00 fa fa 00 00 fa fa fa fa
  0x7b2492be0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b2492be0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b2492be0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b2492be0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b2492be0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==351==ABORTING
````

</details>

### f_flist_erase_after_ptr_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_flist_erase_after_ptr_bucle(std::forward_list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.erase_after(c.before_begin());
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
    iterator "this" @ 0x7ffccc48ae50 {
      type = std::_Fwd_list_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::forward_list<int, std::allocator<int> >' @ 0x7ffccc48af70
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
0dc3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x330dc3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x56490137ed1b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fed1b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5649012e517d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x26517d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x564901354a1a  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d4a1a) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7ff3fd427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7ff3fd4278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x5649011202c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x564901285fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5649013b0687  (/tmp/mi-linter-runtime-validation/runtime_asan+0x330687) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5649013b028f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33028f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5649013afd5c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32fd5c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5649013d23d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3523d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5649013d1e13  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351e13) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x564901384e40  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304e40) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x564901320dea  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a0dea) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x564901354a0d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d4a0d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7ff3fd427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7ff3fd4278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x5649011202c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x2651f3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c13fc5dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c13fc5dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c13fc5dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c13fc5dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c13fc5dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c13fc5e0000: fa fa fd[fd]fa fa 00 00 fa fa 00 00 fa fa fa fa
  0x7c13fc5e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c13fc5e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c13fc5e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c13fc5e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c13fc5e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==353==ABORTING
````

</details>

### f_flist_erase_after_ptr_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `llamada` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_flist_erase_after_ptr_llamada(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_flist_erase_after(c);
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
d1b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fed1b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55dc0df5a0dd  (/tmp/mi-linter-runtime-validation/runtime_asan+0x20a0dd) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55dc0dfb546d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x26546d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55dc0e024b75  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d4b75) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f5b87427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f5b874278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55dc0ddf02c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55dc0df55fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55dc0e080687  (/tmp/mi-linter-runtime-validation/runtime_asan+0x330687) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55dc0e08028f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33028f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55dc0e07fd5c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32fd5c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55dc0e0a23d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3523d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55dc0e0a1e13  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351e13) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55dc0e054e40  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304e40) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55dc0dff0dea  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a0dea) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55dc0e024b68  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2d4b68) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f5b87427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f5b874278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55dc0ddf02c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x2654ce) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b7b865dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b7b865dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b7b865dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b7b865dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b7b865dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b7b865e0000: fa fa fd[fd]fa fa 00 00 fa fa 00 00 fa fa fa fa
  0x7b7b865e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b7b865e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b7b865e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b7b865e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b7b865e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==355==ABORTING
````

</details>
