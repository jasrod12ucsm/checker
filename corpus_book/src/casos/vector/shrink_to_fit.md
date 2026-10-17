# `std::vector::shrink_to_fit`

Mutación: `c.shrink_to_fit();`

- Iterador retenido: 🟡 `POLICY`
- Referencia/puntero retenido: 🟡 `POLICY`
- Casos `UB` detectados estáticamente: 0/0

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🟡 calla](#f_vector_shrink_to_fit_it_recto) | [🟡 calla](#f_vector_shrink_to_fit_it_guarda) | [🟡 calla](#f_vector_shrink_to_fit_it_bucle) | [🟡 calla](#f_vector_shrink_to_fit_it_llamada) |
| **referencia** | [🟡 calla](#f_vector_shrink_to_fit_ref_recto) | [🟡 calla](#f_vector_shrink_to_fit_ref_guarda) | [🟡 calla](#f_vector_shrink_to_fit_ref_bucle) | [🟡 calla](#f_vector_shrink_to_fit_ref_llamada) |
| **puntero** | [🟡 calla](#f_vector_shrink_to_fit_ptr_recto) | [🟡 calla](#f_vector_shrink_to_fit_ptr_guarda) | [🟡 calla](#f_vector_shrink_to_fit_ptr_bucle) | [🟡 calla](#f_vector_shrink_to_fit_ptr_llamada) |

## Handle: iterador

### f_vector_shrink_to_fit_it_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `recto` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_shrink_to_fit_it_recto(std::vector<int>& c) {
  auto it = c.begin();
  c.shrink_to_fit();
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | holgura de capacidad | 🛑 attempt to dereference a singular iterator | 🛑 heap-use-after-free |
| `preserve` | capacidad previamente ajustada al tamaño | — (código 0) | — (código 0) |

<details>
<summary>stderr libstdc++ Debug · <code>force</code></summary>

````text
/usr/include/c++/16/debug/safe_iterator.h:352:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::reference 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator*() 
    const [with _Iterator = gnu_cxx::normal_iterator<int*, std::vector<int, 
    std::allocator<int> > >; _Sequence = std::debug::vector<int>; _Category 
    = std::forward_iterator_tag; reference = int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffd1e4da0f0 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffd1e4da180
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
7e1f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x315e1f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5611e78c64d0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3044d0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5611e78d6e34  (/tmp/mi-linter-runtime-validation/runtime_asan+0x314e34) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5611e78d6ba8  (/tmp/mi-linter-runtime-validation/runtime_asan+0x314ba8) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5611e78bcec4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2faec4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5611e77ef350  (/tmp/mi-linter-runtime-validation/runtime_asan+0x22d350) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x5611e787ea5d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bca5d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7f3da2827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7f3da28278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x5611e76622c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5611e77c7fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5611e78ceb37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5611e78ce27f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5611e78bc650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5611e7861d04  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29fd04) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5611e787ea50  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bca50) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7f3da2827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7f3da28278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x5611e76622c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x22d432) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7ccda19dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ccda19dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ccda19dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ccda19dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ccda19e0000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x7ccda19e0080:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7ccda19e0100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7ccda19e0180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7ccda19e0200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7ccda19e0280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7ccda19e0300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==295==ABORTING
````

</details>

### f_vector_shrink_to_fit_it_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `guarda` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_shrink_to_fit_it_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.shrink_to_fit();
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | holgura de capacidad | 🛑 attempt to dereference a singular iterator | 🛑 heap-use-after-free |
| `preserve` | capacidad previamente ajustada al tamaño | — (código 0) | — (código 0) |

<details>
<summary>stderr libstdc++ Debug · <code>force</code></summary>

````text
/usr/include/c++/16/debug/safe_iterator.h:352:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::reference 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator*() 
    const [with _Iterator = gnu_cxx::normal_iterator<int*, std::vector<int, 
    std::allocator<int> > >; _Sequence = std::debug::vector<int>; _Category 
    = std::forward_iterator_tag; reference = int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fffc5841da0 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7fffc5841e60
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
2e1f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x315e1f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55683dd114d0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3044d0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55683dd21e34  (/tmp/mi-linter-runtime-validation/runtime_asan+0x314e34) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55683dd21ba8  (/tmp/mi-linter-runtime-validation/runtime_asan+0x314ba8) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55683dd07ec4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2faec4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55683dc3a831  (/tmp/mi-linter-runtime-validation/runtime_asan+0x22d831) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55683dcc9bd3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bcbd3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7f9b9c627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7f9b9c6278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x55683daad2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55683dc12fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55683dd19b37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55683dd1927f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55683dd07650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55683dcacd04  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29fd04) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55683dcc9bc6  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bcbc6) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7f9b9c627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7f9b9c6278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x55683daad2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x22d919) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7d2b9b7dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7d2b9b7dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7d2b9b7dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7d2b9b7dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7d2b9b7e0000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x7d2b9b7e0080:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d2b9b7e0100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d2b9b7e0180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d2b9b7e0200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d2b9b7e0280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d2b9b7e0300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==299==ABORTING
````

</details>

### f_vector_shrink_to_fit_it_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `bucle` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_shrink_to_fit_it_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.shrink_to_fit();
    sink(*it);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | holgura de capacidad | 🛑 attempt to dereference a singular iterator | 🛑 heap-use-after-free |
| `preserve` | capacidad previamente ajustada al tamaño | — (código 0) | — (código 0) |

<details>
<summary>stderr libstdc++ Debug · <code>force</code></summary>

````text
/usr/include/c++/16/debug/safe_iterator.h:352:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::reference 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator*() 
    const [with _Iterator = gnu_cxx::normal_iterator<int*, std::vector<int, 
    std::allocator<int> > >; _Sequence = std::debug::vector<int>; _Category 
    = std::forward_iterator_tag; reference = int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fffdf1ad990 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7fffdf1ada50
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
9e1f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x315e1f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x558c54ec84d0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3044d0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x558c54ed8e34  (/tmp/mi-linter-runtime-validation/runtime_asan+0x314e34) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x558c54ed8ba8  (/tmp/mi-linter-runtime-validation/runtime_asan+0x314ba8) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x558c54ebeec4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2faec4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x558c54df1de1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x22dde1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x558c54e80d49  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bcd49) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7f375e827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7f375e8278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x558c54c642c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x558c54dc9fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x558c54ed0b37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x558c54ed027f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x558c54ebe650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x558c54e63d04  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29fd04) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x558c54e80d3c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bcd3c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7f375e827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7f375e8278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x558c54c642c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x22decc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7cc75d9dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7cc75d9dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7cc75d9dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7cc75d9dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7cc75d9e0000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x7cc75d9e0080:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7cc75d9e0100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7cc75d9e0180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7cc75d9e0200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7cc75d9e0280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7cc75d9e0300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==303==ABORTING
````

</details>

### f_vector_shrink_to_fit_it_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `llamada` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_shrink_to_fit_it_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_vector_shrink_to_fit(c);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | holgura de capacidad | 🛑 attempt to dereference a singular iterator | 🛑 heap-use-after-free |
| `preserve` | capacidad previamente ajustada al tamaño | — (código 0) | — (código 0) |

<details>
<summary>stderr libstdc++ Debug · <code>force</code></summary>

````text
/usr/include/c++/16/debug/safe_iterator.h:352:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::reference 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator*() 
    const [with _Iterator = gnu_cxx::normal_iterator<int*, std::vector<int, 
    std::allocator<int> > >; _Sequence = std::debug::vector<int>; _Category 
    = std::forward_iterator_tag; reference = int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffd45dc6770 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffd45dc6830
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
4d0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3044d0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5607100b8e34  (/tmp/mi-linter-runtime-validation/runtime_asan+0x314e34) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5607100b8ba8  (/tmp/mi-linter-runtime-validation/runtime_asan+0x314ba8) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x56071009eec4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2faec4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x56070ffac79e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x20879e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x56070ffd23ef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x22e3ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x560710060ebf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bcebf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7f7f57827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7f7f578278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x56070fe442c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x56070ffa9fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5607100b0b37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5607100b027f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x56071009e650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x560710043d04  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29fd04) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x560710060eb2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bceb2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7f7f57827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7f7f578278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x56070fe442c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x22e4d7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7d0f569dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7d0f569dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7d0f569dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7d0f569dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7d0f569e0000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x7d0f569e0080:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d0f569e0100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d0f569e0180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d0f569e0200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d0f569e0280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d0f569e0300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==307==ABORTING
````

</details>

## Handle: referencia

### f_vector_shrink_to_fit_ref_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `recto` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_shrink_to_fit_ref_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.shrink_to_fit();
  sink(h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | holgura de capacidad | — (código 0) | 🛑 heap-use-after-free |
| `preserve` | capacidad previamente ajustada al tamaño | — (código 0) | — (código 0) |

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
be1f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x315e1f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55c70bb6a4d0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3044d0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55c70bb7ae34  (/tmp/mi-linter-runtime-validation/runtime_asan+0x314e34) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55c70bb7aba8  (/tmp/mi-linter-runtime-validation/runtime_asan+0x314ba8) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55c70bb60ec4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2faec4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55c70ba94755  (/tmp/mi-linter-runtime-validation/runtime_asan+0x22e755) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55c70bb23035  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bd035) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7fce03227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7fce032278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x55c70b9062c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55c70ba6bfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55c70bb72b37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55c70bb7227f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55c70bb60650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55c70bb05d04  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29fd04) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55c70bb23028  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bd028) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7fce03227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7fce032278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x55c70b9062c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x22e787) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7d5e023dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7d5e023dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7d5e023dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7d5e023dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7d5e023e0000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x7d5e023e0080:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d5e023e0100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d5e023e0180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d5e023e0200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d5e023e0280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d5e023e0300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==311==ABORTING
````

</details>

### f_vector_shrink_to_fit_ref_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `guarda` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_shrink_to_fit_ref_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.shrink_to_fit();
  sink(h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | holgura de capacidad | — (código 0) | 🛑 heap-use-after-free |
| `preserve` | capacidad previamente ajustada al tamaño | — (código 0) | — (código 0) |

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
ae1f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x315e1f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x557e642294d0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3044d0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x557e64239e34  (/tmp/mi-linter-runtime-validation/runtime_asan+0x314e34) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x557e64239ba8  (/tmp/mi-linter-runtime-validation/runtime_asan+0x314ba8) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x557e6421fec4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2faec4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x557e64153c3a  (/tmp/mi-linter-runtime-validation/runtime_asan+0x22ec3a) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x557e641e21ab  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bd1ab) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7ff72c627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7ff72c6278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x557e63fc52c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x557e6412afe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x557e64231b37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x557e6423127f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x557e6421f650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x557e641c4d04  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29fd04) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x557e641e219e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bd19e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7ff72c627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7ff72c6278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x557e63fc52c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x22ec6f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7d872b7dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7d872b7dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7d872b7dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7d872b7dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7d872b7e0000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x7d872b7e0080:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d872b7e0100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d872b7e0180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d872b7e0200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d872b7e0280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d872b7e0300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==315==ABORTING
````

</details>

### f_vector_shrink_to_fit_ref_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `bucle` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_shrink_to_fit_ref_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.shrink_to_fit();
    sink(h);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | holgura de capacidad | 🛑 attempt to increment a singular iterator | 🛑 heap-use-after-free |
| `preserve` | capacidad previamente ajustada al tamaño | — (código 0) | — (código 0) |

<details>
<summary>stderr libstdc++ Debug · <code>force</code></summary>

````text
/usr/include/c++/16/debug/safe_iterator.h:392:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>& 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator++() 
    [with _Iterator = gnu_cxx::normal_iterator<int*, std::vector<int, 
    std::allocator<int> > >; _Sequence = std::debug::vector<int>; _Category 
    = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffd494f5210 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffd494f52d0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
1e1f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x315e1f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x560a113904d0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3044d0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x560a113a0e34  (/tmp/mi-linter-runtime-validation/runtime_asan+0x314e34) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x560a113a0ba8  (/tmp/mi-linter-runtime-validation/runtime_asan+0x314ba8) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x560a11386ec4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2faec4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x560a112bb1db  (/tmp/mi-linter-runtime-validation/runtime_asan+0x22f1db) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x560a11349321  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bd321) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7fc00c827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7fc00c8278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x560a1112c2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x560a11291fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x560a11398b37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x560a1139827f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x560a11386650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x560a1132bd04  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29fd04) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x560a11349314  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bd314) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7fc00c827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7fc00c8278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x560a1112c2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x22f213) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7d500b9dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7d500b9dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7d500b9dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7d500b9dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7d500b9e0000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x7d500b9e0080:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d500b9e0100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d500b9e0180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d500b9e0200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d500b9e0280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d500b9e0300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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

### f_vector_shrink_to_fit_ref_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `llamada` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_shrink_to_fit_ref_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_vector_shrink_to_fit(c);
  sink(h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | holgura de capacidad | — (código 0) | 🛑 heap-use-after-free |
| `preserve` | capacidad previamente ajustada al tamaño | — (código 0) | — (código 0) |

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
4d0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3044d0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5636ebccae34  (/tmp/mi-linter-runtime-validation/runtime_asan+0x314e34) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5636ebccaba8  (/tmp/mi-linter-runtime-validation/runtime_asan+0x314ba8) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5636ebcb0ec4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2faec4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5636ebbbe79e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x20879e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x5636ebbe57e8  (/tmp/mi-linter-runtime-validation/runtime_asan+0x22f7e8) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x5636ebc73497  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bd497) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7efcab027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7efcab0278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x5636eba562c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5636ebbbbfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5636ebcc2b37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5636ebcc227f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5636ebcb0650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5636ebc55d04  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29fd04) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5636ebc7348a  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bd48a) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7efcab027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7efcab0278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x5636eba562c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x22f81d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c8caa1dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c8caa1dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c8caa1dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c8caa1dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c8caa1e0000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x7c8caa1e0080:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7c8caa1e0100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7c8caa1e0180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7c8caa1e0200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7c8caa1e0280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7c8caa1e0300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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

## Handle: puntero

### f_vector_shrink_to_fit_ptr_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `recto` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_shrink_to_fit_ptr_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.shrink_to_fit();
  sink(*h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | holgura de capacidad | — (código 0) | 🛑 heap-use-after-free |
| `preserve` | capacidad previamente ajustada al tamaño | — (código 0) | — (código 0) |

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
3e1f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x315e1f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5572197124d0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3044d0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x557219722e34  (/tmp/mi-linter-runtime-validation/runtime_asan+0x314e34) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x557219722ba8  (/tmp/mi-linter-runtime-validation/runtime_asan+0x314ba8) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x557219708ec4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2faec4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55721963da79  (/tmp/mi-linter-runtime-validation/runtime_asan+0x22fa79) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x5572196cb60d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bd60d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7ffa3ac27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7ffa3ac278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x5572194ae2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x557219613fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55721971ab37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55721971a27f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x557219708650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5572196add04  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29fd04) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5572196cb600  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bd600) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7ffa3ac27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7ffa3ac278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x5572194ae2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x22fada) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7d8a39ddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7d8a39ddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7d8a39ddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7d8a39ddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7d8a39de0000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x7d8a39de0080:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d8a39de0100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d8a39de0180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d8a39de0200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d8a39de0280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d8a39de0300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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

### f_vector_shrink_to_fit_ptr_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `guarda` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_shrink_to_fit_ptr_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.shrink_to_fit();
  sink(*h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | holgura de capacidad | — (código 0) | 🛑 heap-use-after-free |
| `preserve` | capacidad previamente ajustada al tamaño | — (código 0) | — (código 0) |

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
3e1f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x315e1f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x558216e724d0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3044d0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x558216e82e34  (/tmp/mi-linter-runtime-validation/runtime_asan+0x314e34) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x558216e82ba8  (/tmp/mi-linter-runtime-validation/runtime_asan+0x314ba8) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x558216e68ec4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2faec4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x558216d9df5e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x22ff5e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x558216e2b783  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bd783) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7f0deae27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7f0deae278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x558216c0e2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x558216d73fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x558216e7ab37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x558216e7a27f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x558216e68650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x558216e0dd04  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29fd04) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x558216e2b776  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bd776) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7f0deae27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7f0deae278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x558216c0e2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x22ffc2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c9de9fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c9de9fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c9de9fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c9de9fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c9de9fe0000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x7c9de9fe0080:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7c9de9fe0100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7c9de9fe0180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7c9de9fe0200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7c9de9fe0280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7c9de9fe0300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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

### f_vector_shrink_to_fit_ptr_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `bucle` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_shrink_to_fit_ptr_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.shrink_to_fit();
    sink(*h);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | holgura de capacidad | 🛑 attempt to increment a singular iterator | 🛑 heap-use-after-free |
| `preserve` | capacidad previamente ajustada al tamaño | — (código 0) | — (código 0) |

<details>
<summary>stderr libstdc++ Debug · <code>force</code></summary>

````text
/usr/include/c++/16/debug/safe_iterator.h:392:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>& 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator++() 
    [with _Iterator = gnu_cxx::normal_iterator<int*, std::vector<int, 
    std::allocator<int> > >; _Sequence = std::debug::vector<int>; _Category 
    = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffe1067b4e0 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffe1067b5a0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
de1f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x315e1f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5558d788c4d0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3044d0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5558d789ce34  (/tmp/mi-linter-runtime-validation/runtime_asan+0x314e34) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5558d789cba8  (/tmp/mi-linter-runtime-validation/runtime_asan+0x314ba8) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5558d7882ec4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2faec4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5558d77b84ff  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2304ff) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x5558d78458f9  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bd8f9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7f0012a27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7f0012a278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x5558d76282c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5558d778dfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5558d7894b37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5558d789427f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5558d7882650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5558d7827d04  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29fd04) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5558d78458ec  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bd8ec) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7f0012a27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7f0012a278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x5558d76282c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x230563) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c9011bdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c9011bdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c9011bdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c9011bdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c9011be0000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x7c9011be0080:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7c9011be0100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7c9011be0180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7c9011be0200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7c9011be0280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7c9011be0300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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

### f_vector_shrink_to_fit_ptr_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `llamada` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_shrink_to_fit_ptr_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_vector_shrink_to_fit(c);
  sink(*h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | holgura de capacidad | — (código 0) | 🛑 heap-use-after-free |
| `preserve` | capacidad previamente ajustada al tamaño | — (código 0) | — (código 0) |

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
4d0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x3044d0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x555c094c5e34  (/tmp/mi-linter-runtime-validation/runtime_asan+0x314e34) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x555c094c5ba8  (/tmp/mi-linter-runtime-validation/runtime_asan+0x314ba8) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x555c094abec4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2faec4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x555c093b979e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x20879e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x555c093e1b0c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x230b0c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x555c0946ea6f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bda6f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #11 0x7efc8b027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x7efc8b0278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #13 0x555c092512c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x555c093b6fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x555c094bdb37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x555c094bd27f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x555c094ab650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x555c09450d04  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29fd04) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x555c0946ea62  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bda62) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7efc8b027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7efc8b0278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x555c092512c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x230b70) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c8c8a1dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c8c8a1dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c8c8a1dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c8c8a1dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c8c8a1e0000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x7c8c8a1e0080:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7c8c8a1e0100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7c8c8a1e0180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7c8c8a1e0200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7c8c8a1e0280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7c8c8a1e0300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
