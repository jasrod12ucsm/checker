# `std::unordered_map::erase_begin`

Mutación: `c.erase(c.begin());`

- Iterador retenido: 🔴 `UB`
- Referencia/puntero retenido: 🔴 `UB`
- Casos `UB` detectados estáticamente: 4/12

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🔴 avisa](#f_umap_erase_begin_it_recto) | [🔴 avisa](#f_umap_erase_begin_it_guarda) | [🔴 avisa](#f_umap_erase_begin_it_bucle) | [🔴 avisa](#f_umap_erase_begin_it_llamada) |
| **referencia** | [🔴 calla](#f_umap_erase_begin_ref_recto) | [🔴 calla](#f_umap_erase_begin_ref_guarda) | [🔴 calla](#f_umap_erase_begin_ref_bucle) | [🔴 calla](#f_umap_erase_begin_ref_llamada) |
| **puntero** | [🔴 calla](#f_umap_erase_begin_ptr_recto) | [🔴 calla](#f_umap_erase_begin_ptr_guarda) | [🔴 calla](#f_umap_erase_begin_ptr_bucle) | [🔴 calla](#f_umap_erase_begin_ptr_llamada) |

## Handle: iterador

### f_umap_erase_begin_it_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `recto` | 🔴 `UB` | ✅ detectado |

```cpp
void f_umap_erase_begin_it_recto(std::unordered_map<int,int>& c) {
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
    const [with _Iterator = std::detail::_Node_iterator<std::pair<const int, 
    int>, false, false>; _Sequence = std::debug::unordered_map<int, int>; 
    _Category = std::forward_iterator_tag; pointer = std::pair<const int, 
    int>*]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffdd9783020 {
      type = std::detail::_Node_iterator<std::pair<int const, int>, false, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffdd9783110
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
318  (/tmp/mi-linter-runtime-validation/runtime_asan+0x34c318) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55b26e27f1b0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x34c1b0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55b26e2345a7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3015a7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55b26e1cc083  (/tmp/mi-linter-runtime-validation/runtime_asan+0x299083) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55b26e220c67  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2edc67) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7efdbae27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7efdbae278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x55b26dfd32c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55b26e138fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55b26e27a497  (/tmp/mi-linter-runtime-validation/runtime_asan+0x347497) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55b26e28e405  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35b405) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55b26e28de6e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35ae6e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55b26e28d4b1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35a4b1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55b26e2395ad  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3065ad) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55b26e1d5b31  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2b31) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55b26e220c5a  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2edc5a) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7efdbae27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7efdbae278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55b26dfd32c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x299124) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b1db9fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b1db9fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b1db9fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b1db9fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b1db9fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b1db9fe0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x7b1db9fe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b1db9fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b1db9fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b1db9fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b1db9fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==122==ABORTING
````

</details>

### f_umap_erase_begin_it_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `guarda` | 🔴 `UB` | ✅ detectado |

```cpp
void f_umap_erase_begin_it_guarda(std::unordered_map<int,int>& c) {
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
    const [with _Iterator = std::detail::_Node_iterator<std::pair<const int, 
    int>, false, false>; _Sequence = std::debug::unordered_map<int, int>; 
    _Category = std::forward_iterator_tag; pointer = std::pair<const int, 
    int>*]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffdca235a30 {
      type = std::detail::_Node_iterator<std::pair<int const, int>, false, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffdca235b20
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
318  (/tmp/mi-linter-runtime-validation/runtime_asan+0x34c318) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55a927bbe1b0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x34c1b0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55a927b735a7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3015a7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55a927b0b38d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29938d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55a927b5fdfb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2eddfb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7f1c87827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7f1c878278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x55a9279122c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55a927a77fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55a927bb9497  (/tmp/mi-linter-runtime-validation/runtime_asan+0x347497) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55a927bcd405  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35b405) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55a927bcce6e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35ae6e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55a927bcc4b1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35a4b1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55a927b785ad  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3065ad) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55a927b14b31  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2b31) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55a927b5fdee  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2eddee) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f1c87827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f1c878278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55a9279122c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x299431) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b3c869dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b3c869dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b3c869dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b3c869dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b3c869dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b3c869e0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x7b3c869e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b3c869e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b3c869e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b3c869e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b3c869e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==124==ABORTING
````

</details>

### f_umap_erase_begin_it_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ✅ detectado |

```cpp
void f_umap_erase_begin_it_bucle(std::unordered_map<int,int>& c) {
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
    const [with _Iterator = std::detail::_Node_iterator<std::pair<const int, 
    int>, false, false>; _Sequence = std::debug::unordered_map<int, int>; 
    _Category = std::forward_iterator_tag; pointer = std::pair<const int, 
    int>*]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffe7430d6e0 {
      type = std::detail::_Node_iterator<std::pair<int const, int>, false, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffe7430d7d0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
318  (/tmp/mi-linter-runtime-validation/runtime_asan+0x34c318) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x560f15dce1b0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x34c1b0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x560f15d835a7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3015a7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x560f15d1b730  (/tmp/mi-linter-runtime-validation/runtime_asan+0x299730) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x560f15d6ff8f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2edf8f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7f1f98027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7f1f980278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x560f15b222c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x560f15c87fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x560f15dc9497  (/tmp/mi-linter-runtime-validation/runtime_asan+0x347497) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x560f15ddd405  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35b405) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x560f15ddce6e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35ae6e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x560f15ddc4b1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35a4b1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x560f15d885ad  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3065ad) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x560f15d24b31  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2b31) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x560f15d6ff82  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2edf82) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f1f98027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f1f980278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x560f15b222c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x2997d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b3f971dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b3f971dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b3f971dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b3f971dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b3f971dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b3f971e0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x7b3f971e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b3f971e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b3f971e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b3f971e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b3f971e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==126==ABORTING
````

</details>

### f_umap_erase_begin_it_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `llamada` | 🔴 `UB` | ✅ detectado |

```cpp
void f_umap_erase_begin_it_llamada(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_umap_erase_begin(c);
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
    const [with _Iterator = std::detail::_Node_iterator<std::pair<const int, 
    int>, false, false>; _Sequence = std::debug::unordered_map<int, int>; 
    _Category = std::forward_iterator_tag; pointer = std::pair<const int, 
    int>*]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fff16951af0 {
      type = std::detail::_Node_iterator<std::pair<int const, int>, false, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int> > >' @ 0x7fff16951bb0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
b0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x34c1b0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5583487fa5a7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3015a7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5583487047d1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x20b7d1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x558348792a20  (/tmp/mi-linter-runtime-validation/runtime_asan+0x299a20) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x5583487e7123  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2ee123) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7fcd32827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7fcd328278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x5583485992c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5583486fefe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x558348840497  (/tmp/mi-linter-runtime-validation/runtime_asan+0x347497) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x558348854405  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35b405) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x558348853e6e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35ae6e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5583488534b1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35a4b1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5583487ff5ad  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3065ad) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55834879bb31  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2b31) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5583487e7116  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2ee116) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7fcd32827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7fcd328278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x5583485992c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x299abd) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bed319dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bed319dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bed319dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bed319dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bed319dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bed319e0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x7bed319e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bed319e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bed319e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bed319e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bed319e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==128==ABORTING
````

</details>

## Handle: referencia

### f_umap_erase_begin_ref_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `recto` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_umap_erase_begin_ref_recto(std::unordered_map<int,int>& c) {
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
318  (/tmp/mi-linter-runtime-validation/runtime_asan+0x34c318) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5620ac1e41b0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x34c1b0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5620ac1995a7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3015a7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5620ac131d01  (/tmp/mi-linter-runtime-validation/runtime_asan+0x299d01) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x5620ac1862b7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2ee2b7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7f9d07027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7f9d070278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x5620abf382c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5620ac09dfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5620ac1df497  (/tmp/mi-linter-runtime-validation/runtime_asan+0x347497) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5620ac1f3405  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35b405) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5620ac1f2e6e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35ae6e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5620ac1f24b1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35a4b1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5620ac19e5ad  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3065ad) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5620ac13ab31  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2b31) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5620ac1862aa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2ee2aa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f9d07027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f9d070278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x5620abf382c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x299d62) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bbd061dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bbd061dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bbd061dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bbd061dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bbd061dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bbd061e0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x7bbd061e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bbd061e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bbd061e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bbd061e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bbd061e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==130==ABORTING
````

</details>

### f_umap_erase_begin_ref_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `guarda` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_umap_erase_begin_ref_guarda(std::unordered_map<int,int>& c) {
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
318  (/tmp/mi-linter-runtime-validation/runtime_asan+0x34c318) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x561f751591b0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x34c1b0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x561f7510e5a7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3015a7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x561f750a7010  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29a010) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x561f750fb44b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2ee44b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7f548b427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7f548b4278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x561f74ead2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x561f75012fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x561f75154497  (/tmp/mi-linter-runtime-validation/runtime_asan+0x347497) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x561f75168405  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35b405) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x561f75167e6e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35ae6e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x561f751674b1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35a4b1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x561f751135ad  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3065ad) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x561f750afb31  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2b31) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x561f750fb43e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2ee43e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f548b427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f548b4278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x561f74ead2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x29a06e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b748a5dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b748a5dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b748a5dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b748a5dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b748a5dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b748a5e0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x7b748a5e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b748a5e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b748a5e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b748a5e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b748a5e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==132==ABORTING
````

</details>

### f_umap_erase_begin_ref_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_umap_erase_begin_ref_bucle(std::unordered_map<int,int>& c) {
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
    [with _Iterator = std::detail::_Node_iterator<std::pair<const int, int>, 
    false, false>; _Sequence = std::debug::unordered_map<int, int>; 
    _Category = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffddcc7c1f0 {
      type = std::detail::_Node_iterator<std::pair<int const, int>, false, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffddcc7c2e0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
318  (/tmp/mi-linter-runtime-validation/runtime_asan+0x34c318) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x56058b7c71b0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x34c1b0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x56058b77c5a7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3015a7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x56058b7153a0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29a3a0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x56058b7695df  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2ee5df) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7f7371e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7f7371e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x56058b51b2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x56058b680fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x56058b7c2497  (/tmp/mi-linter-runtime-validation/runtime_asan+0x347497) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x56058b7d6405  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35b405) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x56058b7d5e6e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35ae6e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x56058b7d54b1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35a4b1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x56058b7815ad  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3065ad) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x56058b71db31  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2b31) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x56058b7695d2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2ee5d2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f7371e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f7371e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x56058b51b2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x29a401) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b9370fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9370fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9370fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9370fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9370fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b9370fe0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x7b9370fe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b9370fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b9370fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b9370fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b9370fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==134==ABORTING
````

</details>

### f_umap_erase_begin_ref_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `llamada` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_umap_erase_begin_ref_llamada(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_umap_erase_begin(c);
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
b0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x34c1b0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55c0b6cdb5a7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3015a7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55c0b6be57d1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x20b7d1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55c0b6c74695  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29a695) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55c0b6cc8773  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2ee773) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f6f92227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f6f922278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55c0b6a7a2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55c0b6bdffe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55c0b6d21497  (/tmp/mi-linter-runtime-validation/runtime_asan+0x347497) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55c0b6d35405  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35b405) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55c0b6d34e6e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35ae6e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55c0b6d344b1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35a4b1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55c0b6ce05ad  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3065ad) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55c0b6c7cb31  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2b31) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55c0b6cc8766  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2ee766) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f6f92227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f6f922278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55c0b6a7a2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x29a6ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b8f913dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b8f913dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b8f913dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b8f913dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b8f913dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b8f913e0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x7b8f913e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b8f913e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b8f913e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b8f913e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b8f913e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==136==ABORTING
````

</details>

## Handle: puntero

### f_umap_erase_begin_ptr_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `recto` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_umap_erase_begin_ptr_recto(std::unordered_map<int,int>& c) {
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
318  (/tmp/mi-linter-runtime-validation/runtime_asan+0x34c318) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5650718f11b0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x34c1b0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5650718a65a7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3015a7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x56507183f90e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29a90e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x565071893907  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2ee907) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7f7b16227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7f7b162278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x5650716452c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5650717aafe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5650718ec497  (/tmp/mi-linter-runtime-validation/runtime_asan+0x347497) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x565071900405  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35b405) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5650718ffe6e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35ae6e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5650718ff4b1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35a4b1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5650718ab5ad  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3065ad) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x565071847b31  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2b31) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5650718938fa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2ee8fa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f7b16227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f7b162278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x5650716452c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x29a9ad) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b9b153dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9b153dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9b153dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9b153dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9b153dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b9b153e0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x7b9b153e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b9b153e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b9b153e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b9b153e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b9b153e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==138==ABORTING
````

</details>

### f_umap_erase_begin_ptr_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `guarda` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_umap_erase_begin_ptr_guarda(std::unordered_map<int,int>& c) {
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
318  (/tmp/mi-linter-runtime-validation/runtime_asan+0x34c318) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5618706401b0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x34c1b0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5618705f55a7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3015a7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x56187058ec1d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ac1d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x5618705e2a9b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2eea9b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7f11d2627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7f11d26278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x5618703942c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5618704f9fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x56187063b497  (/tmp/mi-linter-runtime-validation/runtime_asan+0x347497) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x56187064f405  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35b405) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x56187064ee6e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35ae6e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x56187064e4b1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35a4b1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5618705fa5ad  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3065ad) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x561870596b31  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2b31) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5618705e2a8e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2eea8e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f11d2627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f11d26278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x5618703942c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x29acb9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b31d17dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b31d17dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b31d17dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b31d17dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b31d17dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b31d17e0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x7b31d17e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b31d17e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b31d17e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b31d17e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b31d17e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==140==ABORTING
````

</details>

### f_umap_erase_begin_ptr_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_umap_erase_begin_ptr_bucle(std::unordered_map<int,int>& c) {
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
    [with _Iterator = std::detail::_Node_iterator<std::pair<const int, int>, 
    false, false>; _Sequence = std::debug::unordered_map<int, int>; 
    _Category = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffdaba1b2c0 {
      type = std::detail::_Node_iterator<std::pair<int const, int>, false, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffdaba1b3b0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
318  (/tmp/mi-linter-runtime-validation/runtime_asan+0x34c318) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55bac3e751b0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x34c1b0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55bac3e2a5a7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3015a7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55bac3dc3fbd  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29afbd) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55bac3e17c29  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2eec29) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7f2999e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7f2999e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x55bac3bc92c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55bac3d2efe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55bac3e70497  (/tmp/mi-linter-runtime-validation/runtime_asan+0x347497) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55bac3e84405  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35b405) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55bac3e83e6e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35ae6e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55bac3e834b1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35a4b1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55bac3e2f5ad  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3065ad) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55bac3dcbb31  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2b31) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55bac3e17c1c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2eec1c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f2999e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f2999e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55bac3bc92c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x29b05c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b4998fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b4998fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b4998fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b4998fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b4998fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b4998fe0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x7b4998fe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b4998fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b4998fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b4998fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b4998fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==142==ABORTING
````

</details>

### f_umap_erase_begin_ptr_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `llamada` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_umap_erase_begin_ptr_llamada(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_umap_erase_begin(c);
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
b0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x34c1b0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5621b9a455a7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3015a7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5621b994f7d1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x20b7d1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x5621b99df2c2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29b2c2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x5621b9a32db7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2eedb7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7fd43c027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7fd43c0278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x5621b97e42c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5621b9949fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5621b9a8b497  (/tmp/mi-linter-runtime-validation/runtime_asan+0x347497) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5621b9a9f405  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35b405) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5621b9a9ee6e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35ae6e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5621b9a9e4b1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35a4b1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5621b9a4a5ad  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3065ad) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5621b99e6b31  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2b31) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5621b9a32daa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2eedaa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7fd43c027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7fd43c0278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x5621b97e42c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x29b35a) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bf43b1dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf43b1dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf43b1dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf43b1dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf43b1dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bf43b1e0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x7bf43b1e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf43b1e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf43b1e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf43b1e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf43b1e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==144==ABORTING
````

</details>
