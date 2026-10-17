# `std::vector::push_back`

Mutación: `c.push_back(1);`

- Iterador retenido: 🟡 `POLICY`
- Referencia/puntero retenido: 🟡 `POLICY`
- Casos `UB` detectados estáticamente: 0/3

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🟡 calla](#f_vector_push_back_it_recto) | [🟡 calla](#f_vector_push_back_it_guarda) | [🔴 calla](#f_vector_push_back_it_bucle) | [🟡 calla](#f_vector_push_back_it_llamada) |
| **referencia** | [🟡 calla](#f_vector_push_back_ref_recto) | [🟡 calla](#f_vector_push_back_ref_guarda) | [🔴 calla](#f_vector_push_back_ref_bucle) | [🟡 calla](#f_vector_push_back_ref_llamada) |
| **puntero** | [🟡 calla](#f_vector_push_back_ptr_recto) | [🟡 calla](#f_vector_push_back_ptr_guarda) | [🔴 calla](#f_vector_push_back_ptr_bucle) | [🟡 calla](#f_vector_push_back_ptr_llamada) |

## Handle: iterador

### f_vector_push_back_it_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `recto` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_push_back_it_recto(std::vector<int>& c) {
  auto it = c.begin();
  c.push_back(1);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | 🛑 attempt to dereference a singular iterator | 🛑 heap-use-after-free |
| `preserve` | capacidad 256, con espacio para la mutación | — (código 0) | — (código 0) |

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
    iterator "this" @ 0x7ffd069bbc20 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffd069bbcb0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
ee6cfb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30ccfb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55de2fee65cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c5cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55de2fee5661  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30b661) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55de2fed3416  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9416) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55de2fed2dfc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f8dfc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55de2fde59d7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x20b9d7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55de2fe8e1a7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b41a7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f1dd9427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f1dd94278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55de2fc7a2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55de2fddffe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55de2fee6b37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55de2fee627f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55de2fed4650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55de2fe79f17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55de2fe8e19a  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b419a) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7f1dd9427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7f1dd94278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x55de2fc7a2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x20bac1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b4dd85dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b4dd85dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b4dd85dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b4dd85dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b4dd85dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b4dd85e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7b4dd85e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b4dd85e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b4dd85e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b4dd85e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b4dd85e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==13==ABORTING
````

</details>

### f_vector_push_back_it_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `guarda` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_push_back_it_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.push_back(1);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | 🛑 attempt to dereference a singular iterator | 🛑 heap-use-after-free |
| `preserve` | capacidad 256, con espacio para la mutación | — (código 0) | — (código 0) |

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
    iterator "this" @ 0x7ffde88da6a0 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffde88da760
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
8abcfb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30ccfb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5621ac8ab5cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c5cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5621ac8aa661  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30b661) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5621ac898416  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9416) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5621ac897dfc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f8dfc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5621ac7aaef5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x20bef5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5621ac85330b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b430b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f7f0c827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f7f0c8278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x5621ac63f2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5621ac7a4fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5621ac8abb37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5621ac8ab27f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5621ac899650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5621ac83ef17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5621ac8532fe  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b42fe) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7f7f0c827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7f7f0c8278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x5621ac63f2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x20bfe5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7baf0b9dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7baf0b9dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7baf0b9dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7baf0b9dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7baf0b9dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7baf0b9e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7baf0b9e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7baf0b9e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7baf0b9e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7baf0b9e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7baf0b9e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==17==ABORTING
````

</details>

### f_vector_push_back_it_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_vector_push_back_it_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.push_back(1);
    sink(*it);
  }
}
```

> **Causa del falso negativo:** 4. La invalidacion por insercion/realojamiento no esta modelada

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
    const [with _Iterator = gnu_cxx::normal_iterator<int*, std::vector<int, 
    std::allocator<int> > >; _Sequence = std::debug::vector<int>; _Category 
    = std::forward_iterator_tag; reference = int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffcc71a73e0 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffcc71a74a0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
89661  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30b661) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55b3c5577416  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9416) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55b3c5576dfc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f8dfc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55b3c548a4b3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x20c4b3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55b3c553246f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b446f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f7f52027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f7f520278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55b3c531e2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55b3c5483fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55b3c558ab37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55b3c558a27f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55b3c5589097  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30b097) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55b3c5577416  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9416) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55b3c5576dfc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f8dfc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55b3c551e1a2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a01a2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55b3c5532462  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b4462) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f7f52027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f7f520278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55b3c531e2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x20c5a9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b9f511dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9f511dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9f511dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9f511dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9f511dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b9f511e0000: fa fa fd fa fa fa fd fa fa fa[fd]fd fa fa fa fa
  0x7b9f511e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b9f511e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b9f511e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b9f511e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b9f511e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==21==ABORTING
````

</details>

### f_vector_push_back_it_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `llamada` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_push_back_it_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_vector_push_back(c);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | 🛑 attempt to dereference a singular iterator | 🛑 heap-use-after-free |
| `preserve` | capacidad 256, con espacio para la mutación | — (código 0) | — (código 0) |

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
    iterator "this" @ 0x7fffe8ae3b90 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7fffe8ae3c50
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
715cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c5cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55d952070661  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30b661) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55d95205e416  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9416) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55d95205ddfc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f8dfc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55d951f6ca73  (/tmp/mi-linter-runtime-validation/runtime_asan+0x207a73) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55d951f71abf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x20cabf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55d9520195d3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b45d3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7f5cc1827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7f5cc18278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x55d951e052c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55d951f6afe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55d952071b37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55d95207127f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55d95205f650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55d952004f17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55d9520195c6  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b45c6) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7f5cc1827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7f5cc18278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x55d951e052c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x20cba7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b8cc09dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b8cc09dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b8cc09dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b8cc09dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b8cc09dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b8cc09e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7b8cc09e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b8cc09e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b8cc09e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b8cc09e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b8cc09e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==23==ABORTING
````

</details>

## Handle: referencia

### f_vector_push_back_ref_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `recto` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_push_back_ref_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.push_back(1);
  sink(h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | — (código 0) | 🛑 heap-use-after-free |
| `preserve` | capacidad 256, con espacio para la mutación | — (código 0) | — (código 0) |

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
e8fcfb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30ccfb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55fb71e8f5cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c5cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55fb71e8e661  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30b661) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55fb71e7c416  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9416) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55fb71e7bdfc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f8dfc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55fb71d8fe61  (/tmp/mi-linter-runtime-validation/runtime_asan+0x20ce61) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55fb71e37737  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b4737) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fcd85627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fcd856278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55fb71c232c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55fb71d88fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55fb71e8fb37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55fb71e8f27f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55fb71e7d650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55fb71e22f17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55fb71e3772a  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b472a) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7fcd85627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7fcd856278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x55fb71c232c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x20cea1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bfd847dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bfd847dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bfd847dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bfd847dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bfd847dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bfd847e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7bfd847e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bfd847e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bfd847e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bfd847e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bfd847e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==27==ABORTING
````

</details>

### f_vector_push_back_ref_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `guarda` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_push_back_ref_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.push_back(1);
  sink(h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | — (código 0) | 🛑 heap-use-after-free |
| `preserve` | capacidad 256, con espacio para la mutación | — (código 0) | — (código 0) |

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
b5dcfb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30ccfb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x562110b5d5cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c5cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x562110b5c661  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30b661) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x562110b4a416  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9416) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x562110b49dfc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f8dfc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x562110a5e3af  (/tmp/mi-linter-runtime-validation/runtime_asan+0x20d3af) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x562110b0589b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b489b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f2c4da27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f2c4da278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x5621108f12c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x562110a56fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x562110b5db37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x562110b5d27f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x562110b4b650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x562110af0f17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x562110b0588e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b488e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7f2c4da27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7f2c4da278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x5621108f12c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x20d3f2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b5c4cbdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b5c4cbdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b5c4cbdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b5c4cbdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b5c4cbdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b5c4cbe0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7b5c4cbe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b5c4cbe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b5c4cbe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b5c4cbe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b5c4cbe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==31==ABORTING
````

</details>

### f_vector_push_back_ref_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_vector_push_back_ref_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.push_back(1);
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
    [with _Iterator = gnu_cxx::normal_iterator<int*, std::vector<int, 
    std::allocator<int> > >; _Sequence = std::debug::vector<int>; _Category 
    = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fff2e52ff80 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7fff2e530040
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
44661  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30b661) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55568e332416  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9416) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55568e331dfc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f8dfc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55568e24698f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x20d98f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55568e2ed9ff  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b49ff) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fe1b0827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fe1b08278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55568e0d92c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55568e23efe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55568e345b37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55568e34527f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55568e344097  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30b097) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55568e332416  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9416) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55568e331dfc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f8dfc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55568e2d91a2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a01a2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55568e2ed9f2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b49f2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7fe1b0827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7fe1b08278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55568e0d92c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x20d9d2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c01af9dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c01af9dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c01af9dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c01af9dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c01af9dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c01af9e0000: fa fa fd fa fa fa fd fa fa fa[fd]fd fa fa fa fa
  0x7c01af9e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c01af9e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c01af9e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c01af9e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c01af9e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==35==ABORTING
````

</details>

### f_vector_push_back_ref_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `llamada` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_push_back_ref_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_vector_push_back(c);
  sink(h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | — (código 0) | 🛑 heap-use-after-free |
| `preserve` | capacidad 256, con espacio para la mutación | — (código 0) | — (código 0) |

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
7c5cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c5cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5637c387b661  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30b661) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5637c3869416  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9416) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5637c3868dfc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f8dfc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5637c3777a73  (/tmp/mi-linter-runtime-validation/runtime_asan+0x207a73) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5637c377dfa8  (/tmp/mi-linter-runtime-validation/runtime_asan+0x20dfa8) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x5637c3824b63  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b4b63) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7f67ea027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7f67ea0278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x5637c36102c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5637c3775fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5637c387cb37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5637c387c27f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5637c386a650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5637c380ff17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5637c3824b56  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b4b56) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7f67ea027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7f67ea0278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x5637c36102c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x20dfdd) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b97e91dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b97e91dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b97e91dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b97e91dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b97e91dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b97e91e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7b97e91e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b97e91e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b97e91e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b97e91e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b97e91e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==37==ABORTING
````

</details>

## Handle: puntero

### f_vector_push_back_ptr_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `recto` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_push_back_ptr_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.push_back(1);
  sink(*h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | — (código 0) | 🛑 heap-use-after-free |
| `preserve` | capacidad 256, con espacio para la mutación | — (código 0) | — (código 0) |

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
510cfb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30ccfb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55b26b5105cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c5cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55b26b50f661  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30b661) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55b26b4fd416  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9416) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55b26b4fcdfc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f8dfc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55b26b412275  (/tmp/mi-linter-runtime-validation/runtime_asan+0x20e275) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55b26b4b8ccd  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b4ccd) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7ff60da27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7ff60da278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55b26b2a42c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55b26b409fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55b26b510b37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55b26b51027f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55b26b4fe650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55b26b4a3f17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55b26b4b8cc0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b4cc0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7ff60da27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7ff60da278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x55b26b2a42c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x20e2e1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c260cbdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c260cbdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c260cbdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c260cbdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c260cbdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c260cbe0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7c260cbe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c260cbe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c260cbe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c260cbe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c260cbe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==41==ABORTING
````

</details>

### f_vector_push_back_ptr_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `guarda` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_push_back_ptr_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.push_back(1);
  sink(*h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | — (código 0) | 🛑 heap-use-after-free |
| `preserve` | capacidad 256, con espacio para la mutación | — (código 0) | — (código 0) |

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
14dcfb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30ccfb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55f9c614d5cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c5cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55f9c614c661  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30b661) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55f9c613a416  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9416) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55f9c6139dfc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f8dfc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55f9c604f7c3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x20e7c3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55f9c60f5e43  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b4e43) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f4200427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f42004278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55f9c5ee12c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55f9c6046fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55f9c614db37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55f9c614d27f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55f9c613b650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55f9c60e0f17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55f9c60f5e36  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b4e36) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7f4200427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7f42004278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x55f9c5ee12c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x20e832) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b71ff5dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b71ff5dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b71ff5dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b71ff5dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b71ff5dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b71ff5e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7b71ff5e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b71ff5e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b71ff5e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b71ff5e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b71ff5e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==45==ABORTING
````

</details>

### f_vector_push_back_ptr_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_vector_push_back_ptr_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.push_back(1);
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
    [with _Iterator = gnu_cxx::normal_iterator<int*, std::vector<int, 
    std::allocator<int> > >; _Sequence = std::debug::vector<int>; _Category 
    = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffd173cff40 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffd173d0000
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
db661  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30b661) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x564735fc9416  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9416) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x564735fc8dfc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f8dfc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x564735ededa3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x20eda3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x564735f84fb9  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b4fb9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f16bba27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f16bba278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x564735d702c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x564735ed5fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x564735fdcb37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x564735fdc27f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x564735fdb097  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30b097) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x564735fc9416  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9416) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x564735fc8dfc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f8dfc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x564735f701a2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a01a2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x564735f84fac  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b4fac) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f16bba27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f16bba278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x564735d702c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x20ee12) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b36babdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b36babdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b36babdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b36babdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b36babdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b36babe0000: fa fa fd fa fa fa fd fa fa fa[fd]fd fa fa fa fa
  0x7b36babe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b36babe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b36babe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b36babe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b36babe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==49==ABORTING
````

</details>

### f_vector_push_back_ptr_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `llamada` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_push_back_ptr_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_vector_push_back(c);
  sink(*h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | — (código 0) | 🛑 heap-use-after-free |
| `preserve` | capacidad 256, con espacio para la mutación | — (código 0) | — (código 0) |

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
ed5cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c5cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x560fcd2ec661  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30b661) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x560fcd2da416  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9416) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x560fcd2d9dfc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f8dfc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x560fcd1e8a73  (/tmp/mi-linter-runtime-validation/runtime_asan+0x207a73) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x560fcd1f03bc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x20f3bc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x560fcd29612f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b512f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7f8743427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7f87434278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x560fcd0812c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x560fcd1e6fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x560fcd2edb37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x560fcd2ed27f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x560fcd2db650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x560fcd280f17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x560fcd296122  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b5122) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7f8743427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7f87434278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x560fcd0812c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x20f420) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bb7425dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bb7425dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bb7425dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bb7425dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bb7425dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bb7425e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7bb7425e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bb7425e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bb7425e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bb7425e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bb7425e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==51==ABORTING
````

</details>
