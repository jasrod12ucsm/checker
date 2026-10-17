# `std::unordered_set::erase_begin`

Mutación: `c.erase(c.begin());`

- Iterador retenido: 🔴 `UB`
- Referencia/puntero retenido: 🔴 `UB`
- Casos `UB` detectados estáticamente: 4/12

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🔴 avisa](#f_uset_erase_begin_it_recto) | [🔴 avisa](#f_uset_erase_begin_it_guarda) | [🔴 avisa](#f_uset_erase_begin_it_bucle) | [🔴 avisa](#f_uset_erase_begin_it_llamada) |
| **referencia** | [🔴 calla](#f_uset_erase_begin_ref_recto) | [🔴 calla](#f_uset_erase_begin_ref_guarda) | [🔴 calla](#f_uset_erase_begin_ref_bucle) | [🔴 calla](#f_uset_erase_begin_ref_llamada) |
| **puntero** | [🔴 calla](#f_uset_erase_begin_ptr_recto) | [🔴 calla](#f_uset_erase_begin_ptr_guarda) | [🔴 calla](#f_uset_erase_begin_ptr_bucle) | [🔴 calla](#f_uset_erase_begin_ptr_llamada) |

## Handle: iterador

### f_uset_erase_begin_it_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `recto` | 🔴 `UB` | ✅ detectado |

```cpp
void f_uset_erase_begin_it_recto(std::unordered_set<int>& c) {
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
    const [with _Iterator = std::detail::_Node_iterator<int, true, false>; 
    _Sequence = std::debug::unordered_set<int>; _Category = 
    std::forward_iterator_tag; reference = const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fff04934200 {
      type = std::detail::_Node_iterator<int, true, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int> >' @ 0x7fff049342f0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
908  (/tmp/mi-linter-runtime-validation/runtime_asan+0x343908) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x560c3be7f7a0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3437a0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x560c3be3d0c7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3010c7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x560c3bdc7c73  (/tmp/mi-linter-runtime-validation/runtime_asan+0x28bc73) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x560c3be22e3f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e6e3f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7fcb64027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7fcb640278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x560c3bbdc2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x560c3bd41fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x560c3be7b8d7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33f8d7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x560c3be7a89c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e89c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x560c3be7a3c2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e3c2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x560c3be79af9  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33daf9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x560c3be3cfd5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x300fd5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x560c3bdde437  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2437) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x560c3be22e32  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e6e32) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7fcb64027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7fcb640278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x560c3bbdc2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x28bce0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7beb631dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7beb631dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7beb631dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7beb631dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7beb631dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7beb631e0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x7beb631e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7beb631e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7beb631e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7beb631e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7beb631e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

### f_uset_erase_begin_it_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `guarda` | 🔴 `UB` | ✅ detectado |

```cpp
void f_uset_erase_begin_it_guarda(std::unordered_set<int>& c) {
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
    const [with _Iterator = std::detail::_Node_iterator<int, true, false>; 
    _Sequence = std::debug::unordered_set<int>; _Category = 
    std::forward_iterator_tag; reference = const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fff78f3a9d0 {
      type = std::detail::_Node_iterator<int, true, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int> >' @ 0x7fff78f3aac0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
908  (/tmp/mi-linter-runtime-validation/runtime_asan+0x343908) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55e81a49c7a0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3437a0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55e81a45a0c7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3010c7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55e81a3e4f4d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x28bf4d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55e81a43ffd3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e6fd3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7ffbed827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7ffbed8278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x55e81a1f92c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55e81a35efe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55e81a4988d7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33f8d7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55e81a49789c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e89c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55e81a4973c2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e3c2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55e81a496af9  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33daf9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55e81a459fd5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x300fd5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55e81a3fb437  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2437) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55e81a43ffc6  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e6fc6) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7ffbed827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7ffbed8278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55e81a1f92c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x28bfbd) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c1bec9dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c1bec9dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c1bec9dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c1bec9dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c1bec9dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c1bec9e0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x7c1bec9e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c1bec9e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c1bec9e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c1bec9e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c1bec9e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

### f_uset_erase_begin_it_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ✅ detectado |

```cpp
void f_uset_erase_begin_it_bucle(std::unordered_set<int>& c) {
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
    const [with _Iterator = std::detail::_Node_iterator<int, true, false>; 
    _Sequence = std::debug::unordered_set<int>; _Category = 
    std::forward_iterator_tag; reference = const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffd479d54b0 {
      type = std::detail::_Node_iterator<int, true, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int> >' @ 0x7ffd479d55a0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
908  (/tmp/mi-linter-runtime-validation/runtime_asan+0x343908) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55cf0de0e7a0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3437a0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55cf0ddcc0c7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3010c7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55cf0dd57298  (/tmp/mi-linter-runtime-validation/runtime_asan+0x28c298) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55cf0ddb2167  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e7167) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7eff75027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7eff750278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x55cf0db6b2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55cf0dcd0fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55cf0de0a8d7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33f8d7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55cf0de0989c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e89c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55cf0de093c2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e3c2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55cf0de08af9  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33daf9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55cf0ddcbfd5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x300fd5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55cf0dd6d437  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2437) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55cf0ddb215a  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e715a) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7eff75027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7eff750278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55cf0db6b2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x28c308) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b1f741dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b1f741dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b1f741dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b1f741dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b1f741dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b1f741e0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x7b1f741e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b1f741e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b1f741e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b1f741e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b1f741e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

### f_uset_erase_begin_it_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `llamada` | 🔴 `UB` | ✅ detectado |

```cpp
void f_uset_erase_begin_it_llamada(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_uset_erase_begin(c);
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
    iterator "this" @ 0x7ffc62ad7a80 {
      type = std::detail::_Node_iterator<int, true, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int> >' @ 0x7ffc62ad7b40
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
a0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3437a0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55fbfd5c40c7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3010c7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55fbfd4ce2a1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x20b2a1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55fbfd54f550  (/tmp/mi-linter-runtime-validation/runtime_asan+0x28c550) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55fbfd5aa2fb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e72fb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7fdfd1627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7fdfd16278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55fbfd3632c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55fbfd4c8fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55fbfd6028d7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33f8d7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55fbfd60189c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e89c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55fbfd6013c2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e3c2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55fbfd600af9  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33daf9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55fbfd5c3fd5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x300fd5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55fbfd565437  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2437) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55fbfd5aa2ee  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e72ee) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7fdfd1627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7fdfd16278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55fbfd3632c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x28c5b9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bffd07dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bffd07dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bffd07dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bffd07dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bffd07dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bffd07e0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x7bffd07e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bffd07e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bffd07e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bffd07e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bffd07e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

## Handle: referencia

### f_uset_erase_begin_ref_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `recto` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_uset_erase_begin_ref_recto(std::unordered_set<int>& c) {
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
908  (/tmp/mi-linter-runtime-validation/runtime_asan+0x343908) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x559ae3c297a0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3437a0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x559ae3be70c7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3010c7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x559ae3b72801  (/tmp/mi-linter-runtime-validation/runtime_asan+0x28c801) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x559ae3bcd48f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e748f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7f85baa27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7f85baa278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x559ae39862c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x559ae3aebfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x559ae3c258d7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33f8d7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x559ae3c2489c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e89c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x559ae3c243c2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e3c2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x559ae3c23af9  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33daf9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x559ae3be6fd5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x300fd5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x559ae3b88437  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2437) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x559ae3bcd482  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e7482) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f85baa27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f85baa278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x559ae39862c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x28c840) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7ba5b9bdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ba5b9bdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ba5b9bdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ba5b9bdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ba5b9bdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7ba5b9be0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x7ba5b9be0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ba5b9be0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ba5b9be0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ba5b9be0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ba5b9be0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

### f_uset_erase_begin_ref_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `guarda` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_uset_erase_begin_ref_guarda(std::unordered_set<int>& c) {
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
908  (/tmp/mi-linter-runtime-validation/runtime_asan+0x343908) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x555b142987a0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3437a0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x555b142560c7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3010c7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x555b141e1af0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x28caf0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x555b1423c623  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e7623) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7f1008627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7f10086278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x555b13ff52c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x555b1415afe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x555b142948d7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33f8d7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x555b1429389c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e89c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x555b142933c2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e3c2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x555b14292af9  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33daf9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x555b14255fd5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x300fd5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x555b141f7437  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2437) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x555b1423c616  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e7616) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f1008627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f10086278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x555b13ff52c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x28cb29) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b30077dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b30077dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b30077dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b30077dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b30077dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b30077e0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x7b30077e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b30077e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b30077e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b30077e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b30077e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==381==ABORTING
````

</details>

### f_uset_erase_begin_ref_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_uset_erase_begin_ref_bucle(std::unordered_set<int>& c) {
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
    [with _Iterator = std::detail::_Node_iterator<int, true, false>; 
    _Sequence = std::debug::unordered_set<int>; _Category = 
    std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fff2df55150 {
      type = std::detail::_Node_iterator<int, true, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int> >' @ 0x7fff2df55240
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
908  (/tmp/mi-linter-runtime-validation/runtime_asan+0x343908) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x561ecbb867a0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3437a0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x561ecbb440c7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3010c7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x561ecbacfe60  (/tmp/mi-linter-runtime-validation/runtime_asan+0x28ce60) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x561ecbb2a7b7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e77b7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7f5f8ee27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7f5f8ee278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x561ecb8e32c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x561ecba48fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x561ecbb828d7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33f8d7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x561ecbb8189c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e89c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x561ecbb813c2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e3c2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x561ecbb80af9  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33daf9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x561ecbb43fd5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x300fd5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x561ecbae5437  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2437) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x561ecbb2a7aa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e77aa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f5f8ee27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f5f8ee278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x561ecb8e32c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x28ce9f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b7f8dfdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b7f8dfdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b7f8dfdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b7f8dfdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b7f8dfdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b7f8dfe0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x7b7f8dfe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b7f8dfe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b7f8dfe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b7f8dfe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b7f8dfe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==383==ABORTING
````

</details>

### f_uset_erase_begin_ref_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `llamada` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_uset_erase_begin_ref_llamada(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_uset_erase_begin(c);
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
a0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3437a0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55944b3020c7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3010c7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55944b20c2a1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x20b2a1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55944b28e135  (/tmp/mi-linter-runtime-validation/runtime_asan+0x28d135) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55944b2e894b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e794b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f1f0e627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f1f0e6278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55944b0a12c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55944b206fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55944b3408d7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33f8d7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55944b33f89c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e89c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55944b33f3c2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e3c2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55944b33eaf9  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33daf9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55944b301fd5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x300fd5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55944b2a3437  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2437) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55944b2e893e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e793e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f1f0e627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f1f0e6278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55944b0a12c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x28d16d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b3f0d7dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b3f0d7dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b3f0d7dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b3f0d7dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b3f0d7dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b3f0d7e0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x7b3f0d7e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b3f0d7e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b3f0d7e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b3f0d7e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b3f0d7e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==385==ABORTING
````

</details>

## Handle: puntero

### f_uset_erase_begin_ptr_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `recto` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_uset_erase_begin_ptr_recto(std::unordered_set<int>& c) {
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
908  (/tmp/mi-linter-runtime-validation/runtime_asan+0x343908) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55612fc557a0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3437a0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55612fc130c7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3010c7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55612fb9f369  (/tmp/mi-linter-runtime-validation/runtime_asan+0x28d369) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55612fbf9adf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e7adf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7fe910e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7fe910e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x55612f9b22c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55612fb17fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55612fc518d7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33f8d7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55612fc5089c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e89c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55612fc503c2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e3c2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55612fc4faf9  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33daf9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55612fc12fd5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x300fd5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55612fbb4437  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2437) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55612fbf9ad2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e7ad2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7fe910e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7fe910e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55612f9b22c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x28d3ce) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c090ffdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c090ffdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c090ffdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c090ffdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c090ffdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c090ffe0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x7c090ffe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c090ffe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c090ffe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c090ffe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c090ffe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==387==ABORTING
````

</details>

### f_uset_erase_begin_ptr_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `guarda` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_uset_erase_begin_ptr_guarda(std::unordered_set<int>& c) {
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
908  (/tmp/mi-linter-runtime-validation/runtime_asan+0x343908) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5599de42d7a0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3437a0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5599de3eb0c7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3010c7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5599de37764d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x28d64d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x5599de3d1c73  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e7c73) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7fe5c0c27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7fe5c0c278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x5599de18a2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5599de2effe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5599de4298d7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33f8d7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5599de42889c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e89c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5599de4283c2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e3c2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5599de427af9  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33daf9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5599de3eafd5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x300fd5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5599de38c437  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2437) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5599de3d1c66  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e7c66) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7fe5c0c27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7fe5c0c278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x5599de18a2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x28d6b5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c05bfddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c05bfddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c05bfddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c05bfddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c05bfddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c05bfde0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x7c05bfde0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c05bfde0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c05bfde0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c05bfde0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c05bfde0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==389==ABORTING
````

</details>

### f_uset_erase_begin_ptr_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_uset_erase_begin_ptr_bucle(std::unordered_set<int>& c) {
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
    [with _Iterator = std::detail::_Node_iterator<int, true, false>; 
    _Sequence = std::debug::unordered_set<int>; _Category = 
    std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffee1d6ce40 {
      type = std::detail::_Node_iterator<int, true, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int> >' @ 0x7ffee1d6cf30
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
908  (/tmp/mi-linter-runtime-validation/runtime_asan+0x343908) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55636f3e77a0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3437a0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55636f3a50c7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3010c7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55636f3319bd  (/tmp/mi-linter-runtime-validation/runtime_asan+0x28d9bd) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55636f38be07  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e7e07) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7f269f027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7f269f0278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x55636f1442c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55636f2a9fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55636f3e38d7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33f8d7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55636f3e289c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e89c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55636f3e23c2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e3c2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55636f3e1af9  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33daf9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55636f3a4fd5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x300fd5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55636f346437  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2437) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55636f38bdfa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e7dfa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f269f027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f269f0278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55636f1442c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x28da28) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b469e1dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b469e1dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b469e1dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b469e1dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b469e1dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b469e1e0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x7b469e1e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b469e1e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b469e1e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b469e1e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b469e1e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==391==ABORTING
````

</details>

### f_uset_erase_begin_ptr_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `llamada` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_uset_erase_begin_ptr_llamada(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_uset_erase_begin(c);
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
a0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3437a0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55b2867e90c7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3010c7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55b2866f32a1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x20b2a1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55b286775c7d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x28dc7d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55b2867cff9b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e7f9b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7feabf827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7feabf8278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55b2865882c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55b2866edfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55b2868278d7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33f8d7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55b28682689c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e89c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55b2868263c2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33e3c2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55b286825af9  (/tmp/mi-linter-runtime-validation/runtime_asan+0x33daf9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55b2867e8fd5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x300fd5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55b28678a437  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a2437) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55b2867cff8e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2e7f8e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7feabf827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7feabf8278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55b2865882c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x28dcde) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c0abe9dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c0abe9dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c0abe9dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c0abe9dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c0abe9dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c0abe9e0000: fa fa 00 00 fa fa 00 00 fa fa fd[fd]fa fa fa fa
  0x7c0abe9e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c0abe9e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c0abe9e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c0abe9e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c0abe9e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==393==ABORTING
````

</details>
