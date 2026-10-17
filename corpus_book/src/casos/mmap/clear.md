# `std::multimap::clear`

Mutación: `c.clear();`

- Iterador retenido: 🔴 `UB`
- Referencia/puntero retenido: 🔴 `UB`
- Casos `UB` detectados estáticamente: 4/12

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🔴 avisa](#f_mmap_clear_it_recto) | [🔴 avisa](#f_mmap_clear_it_guarda) | [🔴 avisa](#f_mmap_clear_it_bucle) | [🔴 avisa](#f_mmap_clear_it_llamada) |
| **referencia** | [🔴 calla](#f_mmap_clear_ref_recto) | [🔴 calla](#f_mmap_clear_ref_guarda) | [🔴 calla](#f_mmap_clear_ref_bucle) | [🔴 calla](#f_mmap_clear_ref_llamada) |
| **puntero** | [🔴 calla](#f_mmap_clear_ptr_recto) | [🔴 calla](#f_mmap_clear_ptr_guarda) | [🔴 calla](#f_mmap_clear_ptr_bucle) | [🔴 calla](#f_mmap_clear_ptr_llamada) |

## Handle: iterador

### f_mmap_clear_it_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `recto` | 🔴 `UB` | ✅ detectado |

```cpp
void f_mmap_clear_it_recto(std::multimap<int,int>& c) {
  auto it = c.begin();
  c.clear();
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
    iterator "this" @ 0x7ffd363b8be0 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffd363b8c60
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2877b0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55f733530c78  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e4c78) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f3240427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f32404278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55f7332ec2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55f733451fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55f7335846c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55f7335843cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55f7335a4068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55f7335a4019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55f7335a3caf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55f7335a4967  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358967) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55f7335a4546  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358546) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55f733552033  (/tmp/mi-linter-runtime-validation/runtime_asan+0x306033) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55f7334ede04  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a1e04) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55f733530c6b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e4c6b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f3240427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f32404278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55f7332ec2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x28784d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b723f5dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b723f5dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b723f5dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b723f5dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b723f5dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b723f5e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7b723f5e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7b723f5e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b723f5e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b723f5e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b723f5e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==317==ABORTING
````

</details>

### f_mmap_clear_it_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `guarda` | 🔴 `UB` | ✅ detectado |

```cpp
void f_mmap_clear_it_guarda(std::multimap<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.clear();
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
    iterator "this" @ 0x7ffe5d7b7fb0 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffe5d7b8070
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x287a62) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55b376db7db4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e4db4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f8666827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f86668278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55b376b732c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55b376cd8fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55b376e0b6c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55b376e0b3cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55b376e2b068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55b376e2b019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55b376e2acaf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55b376e2b967  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358967) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55b376e2b546  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358546) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55b376dd9033  (/tmp/mi-linter-runtime-validation/runtime_asan+0x306033) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55b376d74e04  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a1e04) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55b376db7da7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e4da7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f8666827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f86668278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55b376b732c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x287aff) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bc6659dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bc6659dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bc6659dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bc6659dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bc6659dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bc6659e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7bc6659e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7bc6659e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bc6659e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bc6659e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bc6659e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==319==ABORTING
````

</details>

### f_mmap_clear_it_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ✅ detectado |

```cpp
void f_mmap_clear_it_bucle(std::multimap<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.clear();
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
    iterator "this" @ 0x7fff765819d0 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7fff76581a90
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
8  (/tmp/mi-linter-runtime-validation/runtime_asan+0x287da8) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x56244b608ef0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e4ef0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f2db5627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f2db56278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x56244b3c42c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x56244b529fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x56244b65c6c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x56244b65c3cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x56244b67c068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x56244b67c019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x56244b67bcaf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x56244b67c967  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358967) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x56244b67c546  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358546) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x56244b62a033  (/tmp/mi-linter-runtime-validation/runtime_asan+0x306033) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x56244b5c5e04  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a1e04) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x56244b608ee3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e4ee3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f2db5627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f2db56278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x56244b3c42c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x287e45) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b6db47dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b6db47dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b6db47dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b6db47dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b6db47dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b6db47e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7b6db47e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7b6db47e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b6db47e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b6db47e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b6db47e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==321==ABORTING
````

</details>

### f_mmap_clear_it_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `llamada` | 🔴 `UB` | ✅ detectado |

```cpp
void f_mmap_clear_it_llamada(std::multimap<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_mmap_clear(c);
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
    iterator "this" @ 0x7ffcdf745700 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffcdf7457c0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
  (/tmp/mi-linter-runtime-validation/runtime_asan+0x288090) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x5650012ae02c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e502c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7f5a15827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7f5a158278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x5650010692c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5650011cefe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5650013016c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5650013013cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x565001321068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x565001321019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x565001320caf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x565001321967  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358967) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x565001321546  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358546) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5650012cf033  (/tmp/mi-linter-runtime-validation/runtime_asan+0x306033) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x56500126ae04  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a1e04) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x5650012ae01f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e501f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f5a15827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f5a158278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x5650010692c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x28812d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b9a149dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9a149dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9a149dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9a149dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9a149dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b9a149e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7b9a149e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7b9a149e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b9a149e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b9a149e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b9a149e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==323==ABORTING
````

</details>

## Handle: referencia

### f_mmap_clear_ref_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `recto` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_mmap_clear_ref_recto(std::multimap<int,int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.clear();
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
9  (/tmp/mi-linter-runtime-validation/runtime_asan+0x288329) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5643219b2168  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e5168) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fdac9027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fdac90278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x56432176d2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5643218d2fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x564321a056c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x564321a053cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x564321a25068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x564321a25019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x564321a24caf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x564321a25967  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358967) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x564321a25546  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358546) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5643219d3033  (/tmp/mi-linter-runtime-validation/runtime_asan+0x306033) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x56432196ee04  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a1e04) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x5643219b215b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e515b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7fdac9027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7fdac90278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x56432176d2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x288380) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c1ac81dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c1ac81dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c1ac81dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c1ac81dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c1ac81dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c1ac81e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7c1ac81e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7c1ac81e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c1ac81e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c1ac81e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c1ac81e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==325==ABORTING
````

</details>

### f_mmap_clear_ref_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `guarda` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_mmap_clear_ref_guarda(std::multimap<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.clear();
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
7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2885f7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x556179c482a4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e52a4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fcd74027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fcd740278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x556179a032c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x556179b68fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x556179c9b6c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x556179c9b3cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x556179cbb068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x556179cbb019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x556179cbacaf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x556179cbb967  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358967) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x556179cbb546  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358546) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x556179c69033  (/tmp/mi-linter-runtime-validation/runtime_asan+0x306033) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x556179c04e04  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a1e04) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x556179c48297  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e5297) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7fcd74027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7fcd740278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x556179a032c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x288651) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c0d731dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c0d731dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c0d731dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c0d731dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c0d731dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c0d731e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7c0d731e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7c0d731e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c0d731e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c0d731e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c0d731e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==327==ABORTING
````

</details>

### f_mmap_clear_ref_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_mmap_clear_ref_bucle(std::multimap<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.clear();
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
    iterator "this" @ 0x7ffff77d8ec0 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffff77d8f80
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x288942) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55e6e00993e0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e53e0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f0231027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f02310278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55e6dfe542c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55e6dffb9fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55e6e00ec6c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55e6e00ec3cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55e6e010c068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55e6e010c019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55e6e010bcaf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55e6e010c967  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358967) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55e6e010c546  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358546) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55e6e00ba033  (/tmp/mi-linter-runtime-validation/runtime_asan+0x306033) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55e6e0055e04  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a1e04) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55e6e00993d3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e53d3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f0231027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f02310278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55e6dfe542c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x28899c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b42301dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b42301dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b42301dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b42301dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b42301dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b42301e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7b42301e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7b42301e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b42301e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b42301e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b42301e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==329==ABORTING
````

</details>

### f_mmap_clear_ref_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `llamada` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_mmap_clear_ref_llamada(std::multimap<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_mmap_clear(c);
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
  (/tmp/mi-linter-runtime-validation/runtime_asan+0x288c35) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x5642c4a6851c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e551c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7fd8c0427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7fd8c04278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x5642c48232c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5642c4988fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5642c4abb6c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5642c4abb3cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5642c4adb068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5642c4adb019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5642c4adacaf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5642c4adb967  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358967) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5642c4adb546  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358546) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5642c4a89033  (/tmp/mi-linter-runtime-validation/runtime_asan+0x306033) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x5642c4a24e04  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a1e04) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x5642c4a6850f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e550f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7fd8c0427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7fd8c04278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x5642c48232c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x288c8f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c18bf5dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c18bf5dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c18bf5dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c18bf5dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c18bf5dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c18bf5e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7c18bf5e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7c18bf5e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c18bf5e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c18bf5e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c18bf5e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==331==ABORTING
````

</details>

## Handle: puntero

### f_mmap_clear_ptr_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `recto` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_mmap_clear_ptr_recto(std::multimap<int,int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.clear();
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
6  (/tmp/mi-linter-runtime-validation/runtime_asan+0x288e66) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5601da125658  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e5658) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fad6b227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fad6b2278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x5601d9ee02c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5601da045fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5601da1786c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5601da1783cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5601da198068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5601da198019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5601da197caf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5601da198967  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358967) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5601da198546  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358546) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5601da146033  (/tmp/mi-linter-runtime-validation/runtime_asan+0x306033) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x5601da0e1e04  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a1e04) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x5601da12564b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e564b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7fad6b227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7fad6b2278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x5601d9ee02c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x288efb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bed6a3dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bed6a3dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bed6a3dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bed6a3dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bed6a3dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bed6a3e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7bed6a3e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7bed6a3e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bed6a3e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bed6a3e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bed6a3e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

### f_mmap_clear_ptr_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `guarda` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_mmap_clear_ptr_guarda(std::multimap<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.clear();
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
4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x289134) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x555879f3f794  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e5794) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f31e9627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f31e96278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x555879cfa2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x555879e5ffe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x555879f926c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x555879f923cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x555879fb2068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x555879fb2019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x555879fb1caf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x555879fb2967  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358967) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x555879fb2546  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358546) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x555879f60033  (/tmp/mi-linter-runtime-validation/runtime_asan+0x306033) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x555879efbe04  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a1e04) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x555879f3f787  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e5787) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f31e9627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f31e96278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x555879cfa2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x2891cc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b71e87dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b71e87dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b71e87dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b71e87dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b71e87dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b71e87e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7b71e87e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7b71e87e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b71e87e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b71e87e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b71e87e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

### f_mmap_clear_ptr_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_mmap_clear_ptr_bucle(std::multimap<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.clear();
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
    iterator "this" @ 0x7ffe9f70eba0 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::multimap<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffe9f70ec60
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x28947f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55d867daf8d0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e58d0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7faed0e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7faed0e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55d867b6a2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55d867ccffe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55d867e026c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55d867e023cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55d867e22068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55d867e22019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55d867e21caf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55d867e22967  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358967) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55d867e22546  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358546) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55d867dd0033  (/tmp/mi-linter-runtime-validation/runtime_asan+0x306033) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55d867d6be04  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a1e04) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55d867daf8c3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e58c3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7faed0e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7faed0e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55d867b6a2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x289517) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7beecffdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7beecffdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7beecffdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7beecffdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7beecffdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7beecffe0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7beecffe0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7beecffe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7beecffe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7beecffe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7beecffe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

### f_mmap_clear_ptr_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `llamada` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_mmap_clear_ptr_llamada(std::multimap<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_mmap_clear(c);
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
  (/tmp/mi-linter-runtime-validation/runtime_asan+0x289782) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55d34d7f0a0c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e5a0c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7ff7f1c27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7ff7f1c278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x55d34d5ab2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55d34d710fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55d34d8436c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55d34d8433cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55d34d863068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55d34d863019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55d34d862caf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55d34d863967  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358967) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55d34d863546  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358546) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55d34d811033  (/tmp/mi-linter-runtime-validation/runtime_asan+0x306033) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55d34d7ace04  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a1e04) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55d34d7f09ff  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e59ff) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7ff7f1c27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7ff7f1c278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55d34d5ab2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x28981a) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c37f0ddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c37f0ddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c37f0ddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c37f0ddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c37f0ddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c37f0de0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7c37f0de0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7c37f0de0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c37f0de0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c37f0de0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c37f0de0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
