# `std::list::pop_front`

Mutación: `c.pop_front();`

- Iterador retenido: 🔴 `UB`
- Referencia/puntero retenido: 🔴 `UB`
- Casos `UB` detectados estáticamente: 4/12

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🔴 avisa](#f_list_pop_front_it_recto) | [🔴 avisa](#f_list_pop_front_it_guarda) | [🔴 avisa](#f_list_pop_front_it_bucle) | [🔴 avisa](#f_list_pop_front_it_llamada) |
| **referencia** | [🔴 calla](#f_list_pop_front_ref_recto) | [🔴 calla](#f_list_pop_front_ref_guarda) | [🔴 calla](#f_list_pop_front_ref_bucle) | [🔴 calla](#f_list_pop_front_ref_llamada) |
| **puntero** | [🔴 calla](#f_list_pop_front_ptr_recto) | [🔴 calla](#f_list_pop_front_ptr_guarda) | [🔴 calla](#f_list_pop_front_ptr_bucle) | [🔴 calla](#f_list_pop_front_ptr_llamada) |

## Handle: iterador

### f_list_pop_front_it_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `recto` | 🔴 `UB` | ✅ detectado |

```cpp
void f_list_pop_front_it_recto(std::list<int>& c) {
  auto it = c.begin();
  c.pop_front();
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
    iterator "this" @ 0x7ffce3d3e290 {
      type = std::_List_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::list<int, std::allocator<int> >' @ 0x7ffce3d3e310
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
dd  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2585dd) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x564b3893bd75  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2ced75) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f000de27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f000de278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x564b3870d2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x564b38872fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x564b38998544  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b544) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x564b3899814f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b14f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x564b38997c9c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32ac9c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x564b389be941  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351941) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x564b389be6e0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3516e0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x564b389be61d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35161d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x564b389be2d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3512d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x564b38971a20  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304a20) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x564b3890d9fa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a09fa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x564b3893bd68  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2ced68) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f000de27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f000de278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x564b3870d2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x258646) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b300cfdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b300cfdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b300cfdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b300cfdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b300cfdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b300cfe0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x7b300cfe0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7b300cfe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b300cfe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b300cfe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b300cfe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==213==ABORTING
````

</details>

### f_list_pop_front_it_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `guarda` | 🔴 `UB` | ✅ detectado |

```cpp
void f_list_pop_front_it_guarda(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.pop_front();
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
    iterator "this" @ 0x7ffc44039fd0 {
      type = std::_List_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::list<int, std::allocator<int> >' @ 0x7ffc4403a090
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
62  (/tmp/mi-linter-runtime-validation/runtime_asan+0x258862) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x555a286d9eab  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2ceeab) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f56d3a27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f56d3a278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x555a284ab2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x555a28610fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x555a28736544  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b544) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x555a2873614f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b14f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x555a28735c9c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32ac9c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x555a2875c941  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351941) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x555a2875c6e0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3516e0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x555a2875c61d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35161d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x555a2875c2d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3512d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x555a2870fa20  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304a20) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x555a286ab9fa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a09fa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x555a286d9e9e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cee9e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f56d3a27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f56d3a278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x555a284ab2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x2588cb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b86d2bdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b86d2bdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b86d2bdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b86d2bdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b86d2bdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b86d2be0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x7b86d2be0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7b86d2be0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b86d2be0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b86d2be0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b86d2be0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==215==ABORTING
````

</details>

### f_list_pop_front_it_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ✅ detectado |

```cpp
void f_list_pop_front_it_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.pop_front();
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
    iterator "this" @ 0x7ffe7e97af70 {
      type = std::_List_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::list<int, std::allocator<int> >' @ 0x7ffe7e97b030
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
78  (/tmp/mi-linter-runtime-validation/runtime_asan+0x258b78) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x557b54feefe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cefe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7faac8227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7faac82278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x557b54dc02c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x557b54f25fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x557b5504b544  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b544) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x557b5504b14f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b14f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x557b5504ac9c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32ac9c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x557b55071941  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351941) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x557b550716e0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3516e0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x557b5507161d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35161d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x557b550712d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3512d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x557b55024a20  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304a20) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x557b54fc09fa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a09fa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x557b54feefd4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cefd4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7faac8227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7faac82278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x557b54dc02c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x258be1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bdac73dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bdac73dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bdac73dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bdac73dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bdac73dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bdac73e0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x7bdac73e0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7bdac73e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bdac73e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bdac73e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bdac73e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==217==ABORTING
````

</details>

### f_list_pop_front_it_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `llamada` | 🔴 `UB` | ✅ detectado |

```cpp
void f_list_pop_front_it_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_list_pop_front(c);
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
    iterator "this" @ 0x7ffdf8b65d90 {
      type = std::_List_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::list<int, std::allocator<int> >' @ 0x7ffdf8b65e50
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x258e20) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55a3376bb117  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cf117) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fe453c27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fe453c278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55a33748c2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55a3375f1fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55a337717544  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b544) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55a33771714f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b14f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55a337716c9c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32ac9c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55a33773d941  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351941) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55a33773d6e0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3516e0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55a33773d61d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35161d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55a33773d2d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3512d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55a3376f0a20  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304a20) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55a33768c9fa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a09fa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55a3376bb10a  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cf10a) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7fe453c27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7fe453c278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55a33748c2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x258e89) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c1452ddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c1452ddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c1452ddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c1452ddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c1452ddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c1452de0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x7c1452de0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7c1452de0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c1452de0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c1452de0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c1452de0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==219==ABORTING
````

</details>

## Handle: referencia

### f_list_pop_front_ref_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `recto` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_list_pop_front_ref_recto(std::list<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.pop_front();
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
89  (/tmp/mi-linter-runtime-validation/runtime_asan+0x259089) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x56317bc8724d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cf24d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f0259827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f02598278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x56317ba582c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x56317bbbdfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x56317bce3544  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b544) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x56317bce314f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b14f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x56317bce2c9c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32ac9c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x56317bd09941  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351941) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x56317bd096e0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3516e0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x56317bd0961d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35161d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x56317bd092d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3512d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x56317bcbca20  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304a20) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x56317bc589fa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a09fa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x56317bc87240  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cf240) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f0259827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f02598278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x56317ba582c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x2590be) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b32589dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b32589dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b32589dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b32589dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b32589dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b32589e0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x7b32589e0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7b32589e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b32589e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b32589e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b32589e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==221==ABORTING
````

</details>

### f_list_pop_front_ref_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `guarda` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_list_pop_front_ref_guarda(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.pop_front();
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
37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x259337) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5581720d1383  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cf383) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f4f95c27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f4f95c278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x558171ea22c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x558172007fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55817212d544  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b544) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55817212d14f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b14f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55817212cc9c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32ac9c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x558172153941  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351941) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5581721536e0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3516e0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55817215361d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35161d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5581721532d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3512d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x558172106a20  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304a20) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x5581720a29fa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a09fa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x5581720d1376  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cf376) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f4f95c27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f4f95c278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x558171ea22c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x25936f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b7f94ddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b7f94ddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b7f94ddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b7f94ddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b7f94ddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b7f94de0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x7b7f94de0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7b7f94de0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b7f94de0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b7f94de0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b7f94de0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==223==ABORTING
````

</details>

### f_list_pop_front_ref_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_list_pop_front_ref_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.pop_front();
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
    iterator "this" @ 0x7ffc07639570 {
      type = std::_List_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::list<int, std::allocator<int> >' @ 0x7ffc07639630
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
62  (/tmp/mi-linter-runtime-validation/runtime_asan+0x259662) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55617420d4b9  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cf4b9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f782b227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f782b2278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x556173fde2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x556174143fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x556174269544  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b544) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55617426914f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b14f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x556174268c9c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32ac9c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55617428f941  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351941) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55617428f6e0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3516e0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55617428f61d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35161d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55617428f2d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3512d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x556174242a20  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304a20) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x5561741de9fa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a09fa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55617420d4ac  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cf4ac) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f782b227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f782b2278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x556173fde2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x25969a) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7ba82a3dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ba82a3dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ba82a3dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ba82a3dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ba82a3dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7ba82a3e0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x7ba82a3e0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7ba82a3e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ba82a3e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ba82a3e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ba82a3e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==225==ABORTING
````

</details>

### f_list_pop_front_ref_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `llamada` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_list_pop_front_ref_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_list_pop_front(c);
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
5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x259935) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55d5aa8275ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cf5ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7faa05027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7faa050278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55d5aa5f82c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55d5aa75dfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55d5aa883544  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b544) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55d5aa88314f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b14f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55d5aa882c9c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32ac9c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55d5aa8a9941  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351941) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55d5aa8a96e0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3516e0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55d5aa8a961d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35161d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55d5aa8a92d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3512d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55d5aa85ca20  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304a20) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55d5aa7f89fa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a09fa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55d5aa8275e2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cf5e2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7faa05027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7faa050278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55d5aa5f82c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x25996d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bda041dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bda041dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bda041dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bda041dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bda041dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bda041e0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x7bda041e0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7bda041e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bda041e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bda041e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bda041e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==227==ABORTING
````

</details>

## Handle: puntero

### f_list_pop_front_ptr_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `recto` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_list_pop_front_ptr_recto(std::list<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.pop_front();
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
36  (/tmp/mi-linter-runtime-validation/runtime_asan+0x259b36) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x558a69d93725  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cf725) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7efe76627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7efe766278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x558a69b642c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x558a69cc9fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x558a69def544  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b544) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x558a69def14f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b14f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x558a69deec9c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32ac9c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x558a69e15941  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351941) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x558a69e156e0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3516e0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x558a69e1561d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35161d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x558a69e152d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3512d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x558a69dc8a20  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304a20) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x558a69d649fa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a09fa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x558a69d93718  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cf718) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7efe76627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7efe766278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x558a69b642c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x259b97) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b2e757dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b2e757dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b2e757dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b2e757dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b2e757dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b2e757e0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x7b2e757e0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7b2e757e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b2e757e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b2e757e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b2e757e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==229==ABORTING
````

</details>

### f_list_pop_front_ptr_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `guarda` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_list_pop_front_ptr_guarda(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.pop_front();
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
bf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x259dbf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x558e7a31885b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cf85b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7fe950e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7fe950e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x558e7a0e92c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x558e7a24efe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x558e7a374544  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b544) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x558e7a37414f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b14f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x558e7a373c9c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32ac9c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x558e7a39a941  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351941) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x558e7a39a6e0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3516e0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x558e7a39a61d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35161d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x558e7a39a2d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3512d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x558e7a34da20  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304a20) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x558e7a2e99fa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a09fa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x558e7a31884e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cf84e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7fe950e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7fe950e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x558e7a0e92c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x259e20) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c194ffdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c194ffdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c194ffdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c194ffdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c194ffdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c194ffe0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x7c194ffe0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7c194ffe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c194ffe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c194ffe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c194ffe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==231==ABORTING
````

</details>

### f_list_pop_front_ptr_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_list_pop_front_ptr_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.pop_front();
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
    iterator "this" @ 0x7ffff9288100 {
      type = std::_List_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::list<int, std::allocator<int> >' @ 0x7ffff92881c0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x25a0cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55784c330991  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cf991) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7efde5e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7efde5e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55784c1012c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55784c266fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55784c38c544  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b544) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55784c38c14f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b14f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55784c38bc9c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32ac9c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55784c3b2941  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351941) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55784c3b26e0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3516e0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55784c3b261d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35161d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55784c3b22d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3512d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55784c365a20  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304a20) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55784c3019fa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a09fa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55784c330984  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cf984) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7efde5e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7efde5e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55784c1012c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x25a133) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b2de4fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b2de4fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b2de4fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b2de4fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b2de4fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b2de4fe0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x7b2de4fe0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7b2de4fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b2de4fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b2de4fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b2de4fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==233==ABORTING
````

</details>

### f_list_pop_front_ptr_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `llamada` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_list_pop_front_ptr_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_list_pop_front(c);
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
d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x25a38d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55baceb2eac7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cfac7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f45e6e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f45e6e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55bace8ff2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55bacea64fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55baceb8a544  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b544) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55baceb8a14f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32b14f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55baceb89c9c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x32ac9c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55bacebb0941  (/tmp/mi-linter-runtime-validation/runtime_asan+0x351941) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55bacebb06e0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3516e0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55bacebb061d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x35161d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55bacebb02d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3512d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55baceb63a20  (/tmp/mi-linter-runtime-validation/runtime_asan+0x304a20) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55baceaff9fa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a09fa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x55baceb2eaba  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2cfaba) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f45e6e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f45e6e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x55bace8ff2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x25a3ee) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b75e5fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b75e5fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b75e5fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b75e5fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b75e5fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b75e5fe0000: fa fa 00 00 00 fa fa fa fd fd[fd]fa fa fa 00 00
  0x7b75e5fe0080: 00 fa fa fa 00 00 00 fa fa fa fa fa fa fa fa fa
  0x7b75e5fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b75e5fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b75e5fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b75e5fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==235==ABORTING
````

</details>
