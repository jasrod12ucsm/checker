# `std::unordered_map::clear`

Mutación: `c.clear();`

- Iterador retenido: 🔴 `UB`
- Referencia/puntero retenido: 🔴 `UB`
- Casos `UB` detectados estáticamente: 4/12

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🔴 avisa](#f_umap_clear_it_recto) | [🔴 avisa](#f_umap_clear_it_guarda) | [🔴 avisa](#f_umap_clear_it_bucle) | [🔴 avisa](#f_umap_clear_it_llamada) |
| **referencia** | [🔴 calla](#f_umap_clear_ref_recto) | [🔴 calla](#f_umap_clear_ref_guarda) | [🔴 calla](#f_umap_clear_ref_bucle) | [🔴 calla](#f_umap_clear_ref_llamada) |
| **puntero** | [🔴 calla](#f_umap_clear_ptr_recto) | [🔴 calla](#f_umap_clear_ptr_guarda) | [🔴 calla](#f_umap_clear_ptr_bucle) | [🔴 calla](#f_umap_clear_ptr_llamada) |

## Handle: iterador

### f_umap_clear_it_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `recto` | 🔴 `UB` | ✅ detectado |

```cpp
void f_umap_clear_it_recto(std::unordered_map<int,int>& c) {
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
    const [with _Iterator = std::detail::_Node_iterator<std::pair<const int, 
    int>, false, false>; _Sequence = std::debug::unordered_map<int, int>; 
    _Category = std::forward_iterator_tag; pointer = std::pair<const int, 
    int>*]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffd84247700 {
      type = std::detail::_Node_iterator<std::pair<int const, int>, false, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffd84247780
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
0538  (/tmp/mi-linter-runtime-validation/runtime_asan+0x308538) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55a6486b54b5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x34d4b5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55a6486696d0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3016d0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55a648603520  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29b520) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55a648656f45  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2eef45) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f3cb6e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f3cb6e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55a6484082c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55a64856dfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55a6486af497  (/tmp/mi-linter-runtime-validation/runtime_asan+0x347497) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55a6486c3405  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35b405) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55a6486c2e6e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35ae6e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55a6486c24b1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35a4b1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55a64866e5ad  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3065ad) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55a64860ab31  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2b31) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55a648656f38  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2eef38) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f3cb6e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f3cb6e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55a6484082c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x29b5bd) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b5cb5fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b5cb5fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b5cb5fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b5cb5fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b5cb5fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b5cb5fe0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x7b5cb5fe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b5cb5fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b5cb5fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b5cb5fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b5cb5fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==146==ABORTING
````

</details>

### f_umap_clear_it_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `guarda` | 🔴 `UB` | ✅ detectado |

```cpp
void f_umap_clear_it_guarda(std::unordered_map<int,int>& c) {
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
    const [with _Iterator = std::detail::_Node_iterator<std::pair<const int, 
    int>, false, false>; _Sequence = std::debug::unordered_map<int, int>; 
    _Category = std::forward_iterator_tag; pointer = std::pair<const int, 
    int>*]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffff235cef0 {
      type = std::detail::_Node_iterator<std::pair<int const, int>, false, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffff235cfb0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
3538  (/tmp/mi-linter-runtime-validation/runtime_asan+0x308538) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55fa656084b5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x34d4b5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55fa655bc6d0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3016d0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55fa655567d2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29b7d2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55fa655aa089  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2ef089) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fd3a3e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fd3a3e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55fa6535b2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55fa654c0fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55fa65602497  (/tmp/mi-linter-runtime-validation/runtime_asan+0x347497) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55fa65616405  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35b405) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55fa65615e6e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35ae6e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55fa656154b1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35a4b1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55fa655c15ad  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3065ad) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55fa6555db31  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2b31) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55fa655aa07c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2ef07c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7fd3a3e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7fd3a3e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55fa6535b2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x29b86f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bf3a2fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf3a2fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf3a2fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf3a2fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf3a2fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bf3a2fe0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x7bf3a2fe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf3a2fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf3a2fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf3a2fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf3a2fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==148==ABORTING
````

</details>

### f_umap_clear_it_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ✅ detectado |

```cpp
void f_umap_clear_it_bucle(std::unordered_map<int,int>& c) {
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
    const [with _Iterator = std::detail::_Node_iterator<std::pair<const int, 
    int>, false, false>; _Sequence = std::debug::unordered_map<int, int>; 
    _Category = std::forward_iterator_tag; pointer = std::pair<const int, 
    int>*]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffc49875c60 {
      type = std::detail::_Node_iterator<std::pair<int const, int>, false, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffc49875d20
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
4538  (/tmp/mi-linter-runtime-validation/runtime_asan+0x308538) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x564109b294b5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x34d4b5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x564109add6d0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3016d0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x564109a77b18  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29bb18) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x564109acb1cd  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2ef1cd) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fcca5427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fcca54278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x56410987c2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5641099e1fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x564109b23497  (/tmp/mi-linter-runtime-validation/runtime_asan+0x347497) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x564109b37405  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35b405) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x564109b36e6e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35ae6e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x564109b364b1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35a4b1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x564109ae25ad  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3065ad) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x564109a7eb31  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2b31) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x564109acb1c0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2ef1c0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7fcca5427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7fcca54278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x56410987c2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x29bbb5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7beca45dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7beca45dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7beca45dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7beca45dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7beca45dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7beca45e0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x7beca45e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7beca45e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7beca45e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7beca45e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7beca45e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==150==ABORTING
````

</details>

### f_umap_clear_it_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `llamada` | 🔴 `UB` | ✅ detectado |

```cpp
void f_umap_clear_it_llamada(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_umap_clear(c);
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
    iterator "this" @ 0x7ffca05f7ac0 {
      type = std::detail::_Node_iterator<std::pair<int const, int>, false, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffca05f7b80
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
4b5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x34d4b5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55d817d266d0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3016d0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55d817c3081e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x20b81e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55d817cc0e00  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29be00) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55d817d14311  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2ef311) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7f398b227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7f398b2278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x55d817ac52c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55d817c2afe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55d817d6c497  (/tmp/mi-linter-runtime-validation/runtime_asan+0x347497) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55d817d80405  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35b405) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55d817d7fe6e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35ae6e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55d817d7f4b1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35a4b1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55d817d2b5ad  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3065ad) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55d817cc7b31  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2b31) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55d817d14304  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2ef304) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f398b227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f398b2278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55d817ac52c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x29be9d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b598a3dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b598a3dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b598a3dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b598a3dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b598a3dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b598a3e0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x7b598a3e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b598a3e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b598a3e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b598a3e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b598a3e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==152==ABORTING
````

</details>

## Handle: referencia

### f_umap_clear_ref_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `recto` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_umap_clear_ref_recto(std::unordered_map<int,int>& c) {
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
0538  (/tmp/mi-linter-runtime-validation/runtime_asan+0x308538) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x56488ca454b5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x34d4b5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x56488c9f96d0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3016d0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x56488c994099  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29c099) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x56488c9e7455  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2ef455) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fa00a027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fa00a0278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x56488c7982c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x56488c8fdfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x56488ca3f497  (/tmp/mi-linter-runtime-validation/runtime_asan+0x347497) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x56488ca53405  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35b405) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x56488ca52e6e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35ae6e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x56488ca524b1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35a4b1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x56488c9fe5ad  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3065ad) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x56488c99ab31  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2b31) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x56488c9e7448  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2ef448) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7fa00a027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7fa00a0278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x56488c7982c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x29c0f0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bc0091dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bc0091dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bc0091dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bc0091dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bc0091dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bc0091e0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x7bc0091e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bc0091e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bc0091e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bc0091e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bc0091e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==154==ABORTING
````

</details>

### f_umap_clear_ref_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `guarda` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_umap_clear_ref_guarda(std::unordered_map<int,int>& c) {
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
b538  (/tmp/mi-linter-runtime-validation/runtime_asan+0x308538) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55c1bc3104b5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x34d4b5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55c1bc2c46d0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3016d0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55c1bc25f367  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29c367) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55c1bc2b2599  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2ef599) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fcfdd227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fcfdd2278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55c1bc0632c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55c1bc1c8fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55c1bc30a497  (/tmp/mi-linter-runtime-validation/runtime_asan+0x347497) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55c1bc31e405  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35b405) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55c1bc31de6e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35ae6e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55c1bc31d4b1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35a4b1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55c1bc2c95ad  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3065ad) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55c1bc265b31  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2b31) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55c1bc2b258c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2ef58c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7fcfdd227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7fcfdd2278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55c1bc0632c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x29c3c1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7befdc3dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7befdc3dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7befdc3dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7befdc3dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7befdc3dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7befdc3e0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x7befdc3e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7befdc3e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7befdc3e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7befdc3e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7befdc3e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==156==ABORTING
````

</details>

### f_umap_clear_ref_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_umap_clear_ref_bucle(std::unordered_map<int,int>& c) {
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
    [with _Iterator = std::detail::_Node_iterator<std::pair<const int, int>, 
    false, false>; _Sequence = std::debug::unordered_map<int, int>; 
    _Category = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffd2c2833b0 {
      type = std::detail::_Node_iterator<std::pair<int const, int>, false, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffd2c283470
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
5538  (/tmp/mi-linter-runtime-validation/runtime_asan+0x308538) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55db3a51a4b5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x34d4b5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55db3a4ce6d0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3016d0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55db3a4696b2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29c6b2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55db3a4bc6dd  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2ef6dd) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fefde427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fefde4278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55db3a26d2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55db3a3d2fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55db3a514497  (/tmp/mi-linter-runtime-validation/runtime_asan+0x347497) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55db3a528405  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35b405) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55db3a527e6e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35ae6e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55db3a5274b1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35a4b1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55db3a4d35ad  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3065ad) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55db3a46fb31  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2b31) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55db3a4bc6d0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2ef6d0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7fefde427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7fefde4278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55db3a26d2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x29c70c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c0fdd5dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c0fdd5dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c0fdd5dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c0fdd5dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c0fdd5dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c0fdd5e0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x7c0fdd5e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c0fdd5e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c0fdd5e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c0fdd5e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c0fdd5e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==158==ABORTING
````

</details>

### f_umap_clear_ref_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `llamada` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_umap_clear_ref_llamada(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_umap_clear(c);
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
4b5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x34d4b5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55d7850ea6d0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3016d0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55d784ff481e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x20b81e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55d7850859a5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29c9a5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55d7850d8821  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2ef821) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7f4841a27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7f4841a278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x55d784e892c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55d784feefe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55d785130497  (/tmp/mi-linter-runtime-validation/runtime_asan+0x347497) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55d785144405  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35b405) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55d785143e6e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35ae6e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55d7851434b1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35a4b1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55d7850ef5ad  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3065ad) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55d78508bb31  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2b31) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55d7850d8814  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2ef814) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f4841a27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f4841a278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55d784e892c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x29c9ff) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b6840bdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b6840bdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b6840bdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b6840bdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b6840bdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b6840be0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x7b6840be0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b6840be0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b6840be0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b6840be0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b6840be0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==160==ABORTING
````

</details>

## Handle: puntero

### f_umap_clear_ptr_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `recto` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_umap_clear_ptr_recto(std::unordered_map<int,int>& c) {
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
9538  (/tmp/mi-linter-runtime-validation/runtime_asan+0x308538) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55c52871e4b5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x34d4b5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55c5286d26d0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3016d0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55c52866dbd6  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29cbd6) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55c5286c0965  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2ef965) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f48c5427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f48c54278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55c5284712c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55c5285d6fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55c528718497  (/tmp/mi-linter-runtime-validation/runtime_asan+0x347497) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55c52872c405  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35b405) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55c52872be6e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35ae6e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55c52872b4b1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35a4b1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55c5286d75ad  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3065ad) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55c528673b31  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2b31) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55c5286c0958  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2ef958) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f48c5427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f48c54278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55c5284712c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x29cc6b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b68c45dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b68c45dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b68c45dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b68c45dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b68c45dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b68c45e0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x7b68c45e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b68c45e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b68c45e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b68c45e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b68c45e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==162==ABORTING
````

</details>

### f_umap_clear_ptr_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `guarda` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_umap_clear_ptr_guarda(std::unordered_map<int,int>& c) {
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
9538  (/tmp/mi-linter-runtime-validation/runtime_asan+0x308538) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x56237745e4b5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x34d4b5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5623774126d0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3016d0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5623773adea4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29cea4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x562377400aa9  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2efaa9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7efd8d827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7efd8d8278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x5623771b12c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x562377316fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x562377458497  (/tmp/mi-linter-runtime-validation/runtime_asan+0x347497) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x56237746c405  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35b405) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x56237746be6e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35ae6e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x56237746b4b1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35a4b1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5623774175ad  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3065ad) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5623773b3b31  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2b31) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x562377400a9c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2efa9c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7efd8d827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7efd8d8278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x5623771b12c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x29cf3c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b1d8c9dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b1d8c9dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b1d8c9dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b1d8c9dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b1d8c9dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b1d8c9e0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x7b1d8c9e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b1d8c9e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b1d8c9e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b1d8c9e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b1d8c9e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==164==ABORTING
````

</details>

### f_umap_clear_ptr_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_umap_clear_ptr_bucle(std::unordered_map<int,int>& c) {
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
    [with _Iterator = std::detail::_Node_iterator<std::pair<const int, int>, 
    false, false>; _Sequence = std::debug::unordered_map<int, int>; 
    _Category = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffe19388f00 {
      type = std::detail::_Node_iterator<std::pair<int const, int>, false, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffe19388fc0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
0538  (/tmp/mi-linter-runtime-validation/runtime_asan+0x308538) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55940a1254b5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x34d4b5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55940a0d96d0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3016d0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55940a0751ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29d1ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55940a0c7bed  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2efbed) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f0cfd427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f0cfd4278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x559409e782c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x559409fddfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55940a11f497  (/tmp/mi-linter-runtime-validation/runtime_asan+0x347497) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55940a133405  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35b405) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55940a132e6e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35ae6e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55940a1324b1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35a4b1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55940a0de5ad  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3065ad) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55940a07ab31  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2b31) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55940a0c7be0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2efbe0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f0cfd427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f0cfd4278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x559409e782c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x29d287) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b2cfc5dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b2cfc5dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b2cfc5dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b2cfc5dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b2cfc5dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b2cfc5e0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x7b2cfc5e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b2cfc5e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b2cfc5e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b2cfc5e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b2cfc5e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==166==ABORTING
````

</details>

### f_umap_clear_ptr_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `llamada` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_umap_clear_ptr_llamada(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_umap_clear(c);
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
4b5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x34d4b5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55d96b0e16d0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3016d0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55d96afeb81e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x20b81e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55d96b07d4f2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29d4f2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55d96b0cfd31  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2efd31) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7fc35ce27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7fc35ce278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x55d96ae802c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55d96afe5fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55d96b127497  (/tmp/mi-linter-runtime-validation/runtime_asan+0x347497) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55d96b13b405  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35b405) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55d96b13ae6e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35ae6e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55d96b13a4b1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35a4b1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55d96b0e65ad  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3065ad) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55d96b082b31  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2b31) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55d96b0cfd24  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2efd24) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7fc35ce27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7fc35ce278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55d96ae802c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x29d58a) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7be35bfdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7be35bfdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7be35bfdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7be35bfdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7be35bfdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7be35bfe0000: fa fa fd fd fa fa fd fd fa fa fd[fd]fa fa fa fa
  0x7be35bfe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7be35bfe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7be35bfe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7be35bfe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7be35bfe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==168==ABORTING
````

</details>
