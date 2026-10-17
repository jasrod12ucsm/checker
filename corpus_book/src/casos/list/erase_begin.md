# `std::list::erase_begin`

Mutación: `c.erase(c.begin());`

- Iterador retenido: 🔴 `UB`
- Referencia/puntero retenido: 🔴 `UB`
- Casos `UB` detectados estáticamente: 4/12

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🔴 avisa](#f_list_erase_begin_it_recto) | [🔴 avisa](#f_list_erase_begin_it_guarda) | [🔴 avisa](#f_list_erase_begin_it_bucle) | [🔴 avisa](#f_list_erase_begin_it_llamada) |
| **referencia** | [🔴 calla](#f_list_erase_begin_ref_recto) | [🔴 calla](#f_list_erase_begin_ref_guarda) | [🔴 calla](#f_list_erase_begin_ref_bucle) | [🔴 calla](#f_list_erase_begin_ref_llamada) |
| **puntero** | [🔴 calla](#f_list_erase_begin_ptr_recto) | [🔴 calla](#f_list_erase_begin_ptr_guarda) | [🔴 calla](#f_list_erase_begin_ptr_bucle) | [🔴 calla](#f_list_erase_begin_ptr_llamada) |

## Handle: iterador

### f_list_erase_begin_it_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `recto` | 🔴 `UB` | ✅ detectado |

```cpp
void f_list_erase_begin_it_recto(std::list<int>& c) {
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
    const [with _Iterator = std::_List_iterator<int>; _Sequence = std::
    debug::list<int>; _Category = std::forward_iterator_tag; reference = 
    int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffcacbf6650 {
      type = std::_List_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::list<int, std::allocator<int> >' @ 0x7ffcacbf6760
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
8a  (/tmp/mi-linter-runtime-validation/runtime_asan+0x251d8a) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x561cfeda8edd  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cbedd) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7fc70ac27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7fc70ac278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x561cfeb7d2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x561cfece2fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x561cfee08544  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b544) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x561cfee0814f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b14f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x561cfee07c9c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32ac9c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x561cfee2e941  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351941) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x561cfee2e6e0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3516e0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x561cfee2e61d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35161d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x561cfee2e2d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3512d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x561cfede1a20  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304a20) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x561cfed7d9fa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a09fa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x561cfeda8ed0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cbed0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7fc70ac27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7fc70ac278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x561cfeb7d2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x251e02) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bf709ddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf709ddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf709ddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf709ddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf709ddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bf709de0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x7bf709de0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7bf709de0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf709de0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf709de0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf709de0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

### f_list_erase_begin_it_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `guarda` | 🔴 `UB` | ✅ detectado |

```cpp
void f_list_erase_begin_it_guarda(std::list<int>& c) {
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
    const [with _Iterator = std::_List_iterator<int>; _Sequence = std::
    debug::list<int>; _Category = std::forward_iterator_tag; reference = 
    int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffef5011760 {
      type = std::_List_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::list<int, std::allocator<int> >' @ 0x7ffef5011880
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
cd  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2520cd) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55ccc2d4c013  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cc013) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f1ba2e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f1ba2e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55ccc2b202c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55ccc2c85fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55ccc2dab544  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b544) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55ccc2dab14f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b14f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55ccc2daac9c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32ac9c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55ccc2dd1941  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351941) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55ccc2dd16e0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3516e0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55ccc2dd161d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35161d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55ccc2dd12d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3512d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55ccc2d84a20  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304a20) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55ccc2d209fa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a09fa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55ccc2d4c006  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cc006) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f1ba2e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f1ba2e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55ccc2b202c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x252148) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b4ba1fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b4ba1fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b4ba1fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b4ba1fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b4ba1fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b4ba1fe0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x7b4ba1fe0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7b4ba1fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b4ba1fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b4ba1fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b4ba1fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

### f_list_erase_begin_it_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ✅ detectado |

```cpp
void f_list_erase_begin_it_bucle(std::list<int>& c) {
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
    const [with _Iterator = std::_List_iterator<int>; _Sequence = std::
    debug::list<int>; _Category = std::forward_iterator_tag; reference = 
    int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffd2a5f1c30 {
      type = std::_List_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::list<int, std::allocator<int> >' @ 0x7ffd2a5f1d50
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
b6  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2524b6) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55a98731d149  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cc149) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7fdadf427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7fdadf4278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55a9870f12c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55a987256fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55a98737c544  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b544) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55a98737c14f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b14f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55a98737bc9c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32ac9c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55a9873a2941  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351941) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55a9873a26e0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3516e0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55a9873a261d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35161d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55a9873a22d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3512d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55a987355a20  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304a20) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55a9872f19fa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a09fa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55a98731d13c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cc13c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7fdadf427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7fdadf4278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55a9870f12c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x252531) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c0ade5dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c0ade5dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c0ade5dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c0ade5dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c0ade5dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c0ade5e0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x7c0ade5e0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7c0ade5e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c0ade5e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c0ade5e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c0ade5e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

### f_list_erase_begin_it_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `llamada` | 🔴 `UB` | ✅ detectado |

```cpp
void f_list_erase_begin_it_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_list_erase_begin(c);
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
    iterator "this" @ 0x7fffee39dd30 {
      type = std::_List_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::list<int, std::allocator<int> >' @ 0x7fffee39ddf0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2527a0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x555d3a3b927f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cc27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fea9a827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fea9a8278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x555d3a18d2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x555d3a2f2fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x555d3a418544  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b544) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x555d3a41814f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b14f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x555d3a417c9c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32ac9c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x555d3a43e941  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351941) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x555d3a43e6e0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3516e0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x555d3a43e61d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35161d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x555d3a43e2d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3512d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x555d3a3f1a20  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304a20) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x555d3a38d9fa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a09fa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x555d3a3b9272  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cc272) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7fea9a827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7fea9a8278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x555d3a18d2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x252809) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c1a999dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c1a999dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c1a999dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c1a999dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c1a999dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c1a999e0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x7c1a999e0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7c1a999e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c1a999e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c1a999e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c1a999e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

## Handle: referencia

### f_list_erase_begin_ref_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `recto` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_list_erase_begin_ref_recto(std::list<int>& c) {
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
95  (/tmp/mi-linter-runtime-validation/runtime_asan+0x252a95) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x56498c7083b5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cc3b5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7fbb98227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7fbb982278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x56498c4dc2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x56498c641fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x56498c767544  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b544) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x56498c76714f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b14f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x56498c766c9c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32ac9c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x56498c78d941  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351941) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x56498c78d6e0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3516e0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x56498c78d61d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35161d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x56498c78d2d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3512d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x56498c740a20  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304a20) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x56498c6dc9fa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a09fa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x56498c7083a8  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cc3a8) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7fbb98227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7fbb982278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x56498c4dc2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x252adf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7beb973dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7beb973dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7beb973dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7beb973dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7beb973dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7beb973e0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x7beb973e0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7beb973e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7beb973e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7beb973e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7beb973e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==149==ABORTING
````

</details>

### f_list_erase_begin_ref_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `guarda` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_list_erase_begin_ref_guarda(std::list<int>& c) {
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
05  (/tmp/mi-linter-runtime-validation/runtime_asan+0x252e05) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55d5561d64eb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cc4eb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f56f6427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f56f64278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55d555faa2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55d55610ffe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55d556235544  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b544) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55d55623514f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b14f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55d556234c9c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32ac9c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55d55625b941  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351941) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55d55625b6e0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3516e0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55d55625b61d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35161d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55d55625b2d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3512d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55d55620ea20  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304a20) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55d5561aa9fa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a09fa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55d5561d64de  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cc4de) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f56f6427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f56f64278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55d555faa2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x252e4f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b86f55dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b86f55dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b86f55dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b86f55dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b86f55dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b86f55e0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x7b86f55e0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7b86f55e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b86f55e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b86f55e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b86f55e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==151==ABORTING
````

</details>

### f_list_erase_begin_ref_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_list_erase_begin_ref_bucle(std::list<int>& c) {
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
    [with _Iterator = std::_List_iterator<int>; _Sequence = std::
    debug::list<int>; _Category = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fffc7b8f6e0 {
      type = std::_List_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::list<int, std::allocator<int> >' @ 0x7fffc7b8f800
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
f0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2531f0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55ebf0fc7621  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cc621) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f74c7e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f74c7e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55ebf0d9b2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55ebf0f00fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55ebf1026544  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b544) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55ebf102614f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b14f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55ebf1025c9c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32ac9c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55ebf104c941  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351941) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55ebf104c6e0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3516e0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55ebf104c61d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35161d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55ebf104c2d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3512d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55ebf0fffa20  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304a20) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55ebf0f9b9fa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a09fa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55ebf0fc7614  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cc614) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f74c7e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f74c7e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55ebf0d9b2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x25323a) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7ba4c6fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ba4c6fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ba4c6fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ba4c6fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ba4c6fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7ba4c6fe0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x7ba4c6fe0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7ba4c6fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ba4c6fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ba4c6fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ba4c6fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==153==ABORTING
````

</details>

### f_list_erase_begin_ref_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `llamada` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_list_erase_begin_ref_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_list_erase_begin(c);
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
5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x253505) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x560f74a4e757  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cc757) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f85b6227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f85b62278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x560f748222c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x560f74987fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x560f74aad544  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b544) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x560f74aad14f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b14f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x560f74aacc9c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32ac9c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x560f74ad3941  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351941) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x560f74ad36e0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3516e0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x560f74ad361d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35161d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x560f74ad32d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3512d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x560f74a86a20  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304a20) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x560f74a229fa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a09fa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x560f74a4e74a  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cc74a) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f85b6227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f85b62278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x560f748222c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x25353d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bb5b53dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bb5b53dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bb5b53dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bb5b53dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bb5b53dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bb5b53e0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x7bb5b53e0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7bb5b53e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bb5b53e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bb5b53e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bb5b53e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==155==ABORTING
````

</details>

## Handle: puntero

### f_list_erase_begin_ptr_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `recto` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_list_erase_begin_ptr_recto(std::list<int>& c) {
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
92  (/tmp/mi-linter-runtime-validation/runtime_asan+0x253792) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5598c8d5e88d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cc88d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7fa22cc27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7fa22cc278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x5598c8b322c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5598c8c97fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5598c8dbd544  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b544) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5598c8dbd14f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b14f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5598c8dbcc9c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32ac9c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5598c8de3941  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351941) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5598c8de36e0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3516e0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5598c8de361d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35161d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5598c8de32d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3512d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5598c8d96a20  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304a20) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x5598c8d329fa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a09fa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x5598c8d5e880  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cc880) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7fa22cc27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7fa22cc278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x5598c8b322c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x253808) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bd22bddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd22bddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd22bddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd22bddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd22bddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bd22bde0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x7bd22bde0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7bd22bde0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd22bde0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd22bde0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd22bde0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==157==ABORTING
````

</details>

### f_list_erase_begin_ptr_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `guarda` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_list_erase_begin_ptr_guarda(std::list<int>& c) {
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
da  (/tmp/mi-linter-runtime-validation/runtime_asan+0x253ada) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5638d6d5e9c3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cc9c3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f68dae27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f68dae278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x5638d6b322c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5638d6c97fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5638d6dbd544  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b544) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5638d6dbd14f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b14f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5638d6dbcc9c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32ac9c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5638d6de3941  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351941) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5638d6de36e0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3516e0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5638d6de361d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35161d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5638d6de32d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3512d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5638d6d96a20  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304a20) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x5638d6d329fa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a09fa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x5638d6d5e9b6  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cc9b6) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f68dae27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f68dae278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x5638d6b322c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x253b50) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b98d9fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b98d9fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b98d9fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b98d9fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b98d9fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b98d9fe0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x7b98d9fe0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7b98d9fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b98d9fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b98d9fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b98d9fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==159==ABORTING
````

</details>

### f_list_erase_begin_ptr_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_list_erase_begin_ptr_bucle(std::list<int>& c) {
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
    [with _Iterator = std::_List_iterator<int>; _Sequence = std::
    debug::list<int>; _Category = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffc7b03e4a0 {
      type = std::_List_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::list<int, std::allocator<int> >' @ 0x7ffc7b03e5c0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
bd  (/tmp/mi-linter-runtime-validation/runtime_asan+0x253ebd) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55f9f7368af9  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2ccaf9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7fd7f1627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7fd7f16278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55f9f713c2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55f9f72a1fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55f9f73c7544  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b544) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55f9f73c714f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b14f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55f9f73c6c9c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32ac9c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55f9f73ed941  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351941) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55f9f73ed6e0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3516e0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55f9f73ed61d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35161d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55f9f73ed2d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3512d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55f9f73a0a20  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304a20) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55f9f733c9fa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a09fa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55f9f7368aec  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2ccaec) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7fd7f1627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7fd7f16278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55f9f713c2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x253f33) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c07f07dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c07f07dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c07f07dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c07f07dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c07f07dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c07f07e0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x7c07f07e0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7c07f07e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c07f07e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c07f07e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c07f07e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==161==ABORTING
````

</details>

### f_list_erase_begin_ptr_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `llamada` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_list_erase_begin_ptr_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_list_erase_begin(c);
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
d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2541ad) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55ba99352c2f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2ccc2f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f7138c27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f7138c278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55ba991262c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55ba9928bfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55ba993b1544  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b544) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55ba993b114f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b14f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55ba993b0c9c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32ac9c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55ba993d7941  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351941) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55ba993d76e0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3516e0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55ba993d761d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35161d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55ba993d72d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3512d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55ba9938aa20  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304a20) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55ba993269fa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a09fa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55ba99352c22  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2ccc22) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f7138c27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f7138c278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55ba991262c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x25420e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7ba137ddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ba137ddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ba137ddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ba137ddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ba137ddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7ba137de0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x7ba137de0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7ba137de0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ba137de0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ba137de0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ba137de0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==163==ABORTING
````

</details>
