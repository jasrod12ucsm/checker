# `std::map::clear`

Mutación: `c.clear();`

- Iterador retenido: 🔴 `UB`
- Referencia/puntero retenido: 🔴 `UB`
- Casos `UB` detectados estáticamente: 4/12

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🔴 avisa](#f_map_clear_it_recto) | [🔴 avisa](#f_map_clear_it_guarda) | [🔴 avisa](#f_map_clear_it_bucle) | [🔴 avisa](#f_map_clear_it_llamada) |
| **referencia** | [🔴 calla](#f_map_clear_ref_recto) | [🔴 calla](#f_map_clear_ref_guarda) | [🔴 calla](#f_map_clear_ref_bucle) | [🔴 calla](#f_map_clear_ref_llamada) |
| **puntero** | [🔴 calla](#f_map_clear_ptr_recto) | [🔴 calla](#f_map_clear_ptr_guarda) | [🔴 calla](#f_map_clear_ptr_bucle) | [🔴 calla](#f_map_clear_ptr_llamada) |

## Handle: iterador

### f_map_clear_it_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `recto` | 🔴 `UB` | ✅ detectado |

```cpp
void f_map_clear_it_recto(std::map<int,int>& c) {
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
    >; _Sequence = std::debug::map<int, int>; _Category = 
    std::forward_iterator_tag; pointer = std::pair<const int, int>*]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fff5e3816c0 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::map<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7fff5e381740
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2807e0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5617a46b59c0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e19c0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f4edf627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f4edf6278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x5617a44742c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5617a45d9fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5617a470c6c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5617a470c3cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5617a472c068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5617a472c019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5617a472bcaf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5617a472b8a5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3578a5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5617a472b1a6  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3571a6) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5617a46d9bb3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305bb3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x5617a46759f4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a19f4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x5617a46b59b3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e19b3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f4edf627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f4edf6278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x5617a44742c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x28087d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b8ede7dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b8ede7dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b8ede7dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b8ede7dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b8ede7dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b8ede7e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7b8ede7e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7b8ede7e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b8ede7e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b8ede7e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b8ede7e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==245==ABORTING
````

</details>

### f_map_clear_it_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `guarda` | 🔴 `UB` | ✅ detectado |

```cpp
void f_map_clear_it_guarda(std::map<int,int>& c) {
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
    >; _Sequence = std::debug::map<int, int>; _Category = 
    std::forward_iterator_tag; pointer = std::pair<const int, int>*]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffd1711c860 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::map<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffd1711c920
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x280a92) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55a73014aafc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e1afc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f8b3c627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f8b3c6278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55a72ff092c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55a73006efe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55a7301a16c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55a7301a13cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55a7301c1068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55a7301c1019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55a7301c0caf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55a7301c08a5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3578a5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55a7301c01a6  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3571a6) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55a73016ebb3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305bb3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55a73010a9f4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a19f4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55a73014aaef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e1aef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f8b3c627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f8b3c6278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55a72ff092c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x280b2f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bcb3b7dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bcb3b7dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bcb3b7dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bcb3b7dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bcb3b7dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bcb3b7e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7bcb3b7e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7bcb3b7e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bcb3b7e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bcb3b7e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bcb3b7e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==247==ABORTING
````

</details>

### f_map_clear_it_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ✅ detectado |

```cpp
void f_map_clear_it_bucle(std::map<int,int>& c) {
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
    >; _Sequence = std::debug::map<int, int>; _Category = 
    std::forward_iterator_tag; pointer = std::pair<const int, int>*]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffd58f63870 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::map<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffd58f63930
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
8  (/tmp/mi-linter-runtime-validation/runtime_asan+0x280dd8) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x559996d24c38  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e1c38) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f998b827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f998b8278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x559996ae32c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x559996c48fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x559996d7b6c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x559996d7b3cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x559996d9b068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x559996d9b019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x559996d9acaf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x559996d9a8a5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3578a5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x559996d9a1a6  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3571a6) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x559996d48bb3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305bb3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x559996ce49f4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a19f4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x559996d24c2b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e1c2b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f998b827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f998b8278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x559996ae32c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x280e75) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bd98a9dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd98a9dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd98a9dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd98a9dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd98a9dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bd98a9e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7bd98a9e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7bd98a9e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd98a9e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd98a9e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd98a9e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==249==ABORTING
````

</details>

### f_map_clear_it_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `llamada` | 🔴 `UB` | ✅ detectado |

```cpp
void f_map_clear_it_llamada(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_map_clear(c);
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
    >; _Sequence = std::debug::map<int, int>; _Category = 
    std::forward_iterator_tag; pointer = std::pair<const int, int>*]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffeaf493c90 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::map<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffeaf493d50
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2810c0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55f4d0a70d74  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e1d74) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7fe00a427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7fe00a4278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x55f4d082f2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55f4d0994fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55f4d0ac76c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55f4d0ac73cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55f4d0ae7068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55f4d0ae7019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55f4d0ae6caf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55f4d0ae68a5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3578a5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55f4d0ae61a6  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3571a6) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55f4d0a94bb3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305bb3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55f4d0a309f4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a19f4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55f4d0a70d67  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e1d67) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7fe00a427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7fe00a4278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55f4d082f2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x28115d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c20095dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c20095dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c20095dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c20095dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c20095dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c20095e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7c20095e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7c20095e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c20095e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c20095e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c20095e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==251==ABORTING
````

</details>

## Handle: referencia

### f_map_clear_ref_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `recto` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_map_clear_ref_recto(std::map<int,int>& c) {
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
9  (/tmp/mi-linter-runtime-validation/runtime_asan+0x281359) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55c907676eb0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e1eb0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fb048a27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fb048a278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55c9074352c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55c90759afe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55c9076cd6c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55c9076cd3cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55c9076ed068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55c9076ed019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55c9076eccaf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55c9076ec8a5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3578a5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55c9076ec1a6  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3571a6) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55c90769abb3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305bb3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55c9076369f4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a19f4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55c907676ea3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e1ea3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7fb048a27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7fb048a278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55c9074352c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x2813b0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bf047bdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf047bdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf047bdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf047bdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf047bdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bf047be0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7bf047be0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7bf047be0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf047be0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf047be0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf047be0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==253==ABORTING
````

</details>

### f_map_clear_ref_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `guarda` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_map_clear_ref_guarda(std::map<int,int>& c) {
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
7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x281627) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x560896538fec  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e1fec) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fc213427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fc2134278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x5608962f72c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x56089645cfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x56089658f6c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x56089658f3cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5608965af068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5608965af019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5608965aecaf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5608965ae8a5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3578a5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5608965ae1a6  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3571a6) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x56089655cbb3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305bb3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x5608964f89f4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a19f4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x560896538fdf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e1fdf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7fc213427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7fc2134278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x5608962f72c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x281681) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c02125dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c02125dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c02125dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c02125dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c02125dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c02125e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7c02125e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7c02125e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c02125e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c02125e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c02125e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==255==ABORTING
````

</details>

### f_map_clear_ref_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_map_clear_ref_bucle(std::map<int,int>& c) {
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
    _Sequence = std::debug::map<int, int>; _Category = 
    std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffe24e0a150 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::map<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffe24e0a210
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x281972) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55cf84cc6128  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e2128) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f6916c27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f6916c278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55cf84a842c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55cf84be9fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55cf84d1c6c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55cf84d1c3cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55cf84d3c068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55cf84d3c019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55cf84d3bcaf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55cf84d3b8a5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3578a5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55cf84d3b1a6  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3571a6) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55cf84ce9bb3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305bb3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55cf84c859f4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a19f4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55cf84cc611b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e211b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f6916c27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f6916c278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55cf84a842c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x2819cc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7ba915ddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ba915ddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ba915ddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ba915ddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ba915ddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7ba915de0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7ba915de0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7ba915de0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ba915de0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ba915de0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ba915de0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==257==ABORTING
````

</details>

### f_map_clear_ref_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `llamada` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_map_clear_ref_llamada(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_map_clear(c);
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
  (/tmp/mi-linter-runtime-validation/runtime_asan+0x281c65) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55df36e2e264  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e2264) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7fb97be27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7fb97be278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x55df36bec2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55df36d51fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55df36e846c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55df36e843cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55df36ea4068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55df36ea4019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55df36ea3caf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55df36ea38a5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3578a5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55df36ea31a6  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3571a6) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55df36e51bb3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305bb3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55df36ded9f4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a19f4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55df36e2e257  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e2257) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7fb97be27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7fb97be278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55df36bec2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x281cbf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bf97afdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf97afdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf97afdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf97afdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf97afdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bf97afe0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7bf97afe0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7bf97afe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf97afe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf97afe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf97afe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==259==ABORTING
````

</details>

## Handle: puntero

### f_map_clear_ptr_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `recto` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_map_clear_ptr_recto(std::map<int,int>& c) {
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
6  (/tmp/mi-linter-runtime-validation/runtime_asan+0x281e96) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5565eca713a0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e23a0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fa6aaa27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fa6aaa278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x5565ec82f2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5565ec994fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5565ecac76c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5565ecac73cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5565ecae7068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5565ecae7019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5565ecae6caf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5565ecae68a5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3578a5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5565ecae61a6  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3571a6) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5565eca94bb3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305bb3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x5565eca309f4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a19f4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x5565eca71393  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e2393) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7fa6aaa27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7fa6aaa278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x5565ec82f2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x281f2b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7be6a9bdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7be6a9bdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7be6a9bdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7be6a9bdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7be6a9bdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7be6a9be0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7be6a9be0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7be6a9be0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7be6a9be0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7be6a9be0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7be6a9be0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==261==ABORTING
````

</details>

### f_map_clear_ptr_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `guarda` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_map_clear_ptr_guarda(std::map<int,int>& c) {
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
4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x282164) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x558dd28db4dc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e24dc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f47b9627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f47b96278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x558dd26992c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x558dd27fefe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x558dd29316c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x558dd29313cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x558dd2951068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x558dd2951019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x558dd2950caf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x558dd29508a5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3578a5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x558dd29501a6  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3571a6) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x558dd28febb3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305bb3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x558dd289a9f4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a19f4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x558dd28db4cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e24cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f47b9627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f47b96278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x558dd26992c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x2821fc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b87b87dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b87b87dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b87b87dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b87b87dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b87b87dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b87b87e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7b87b87e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7b87b87e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b87b87e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b87b87e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b87b87e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==263==ABORTING
````

</details>

### f_map_clear_ptr_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_map_clear_ptr_bucle(std::map<int,int>& c) {
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
    _Sequence = std::debug::map<int, int>; _Category = 
    std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffc6395bca0 {
      type = std::_Rb_tree_iterator<std::pair<int const, int> > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::map<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >' @ 0x7ffc6395bd60
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2824af) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55fdec780618  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e2618) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f3fa5027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f3fa50278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55fdec53e2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55fdec6a3fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55fdec7d66c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55fdec7d63cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55fdec7f6068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55fdec7f6019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55fdec7f5caf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55fdec7f58a5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3578a5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55fdec7f51a6  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3571a6) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55fdec7a3bb3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305bb3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55fdec73f9f4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a19f4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55fdec78060b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e260b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f3fa5027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f3fa50278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55fdec53e2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x282547) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b7fa41dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b7fa41dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b7fa41dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b7fa41dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b7fa41dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b7fa41e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7b7fa41e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7b7fa41e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b7fa41e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b7fa41e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b7fa41e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==265==ABORTING
````

</details>

### f_map_clear_ptr_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `llamada` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_map_clear_ptr_llamada(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_map_clear(c);
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
  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2827b2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55dc865f4754  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e2754) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7f3105027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7f31050278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x55dc863b22c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55dc86517fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55dc8664a6c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3386c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55dc8664a3cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3383cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55dc8666a068  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358068) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55dc8666a019  (/tmp/mi-linter-runtime-validation/runtime_asan+0x358019) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55dc86669caf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x357caf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55dc866698a5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3578a5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55dc866691a6  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3571a6) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55dc86617bb3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x305bb3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55dc865b39f4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a19f4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55dc865f4747  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e2747) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f3105027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f31050278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55dc863b22c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x28284a) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b71041dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b71041dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b71041dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b71041dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b71041dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b71041e0000: fa fa fd fd fd fd[fd]fa fa fa fd fd fd fd fd fa
  0x7b71041e0080: fa fa fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x7b71041e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b71041e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b71041e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b71041e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==267==ABORTING
````

</details>
