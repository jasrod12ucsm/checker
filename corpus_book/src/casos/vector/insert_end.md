# `std::vector::insert_end`

Mutación: `c.insert(c.end(),1);`

- Iterador retenido: 🟡 `POLICY`
- Referencia/puntero retenido: 🟡 `POLICY`
- Casos `UB` detectados estáticamente: 0/3

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🟡 calla](#f_vector_insert_end_it_recto) | [🟡 calla](#f_vector_insert_end_it_guarda) | [🔴 calla](#f_vector_insert_end_it_bucle) | [🟡 calla](#f_vector_insert_end_it_llamada) |
| **referencia** | [🟡 calla](#f_vector_insert_end_ref_recto) | [🟡 calla](#f_vector_insert_end_ref_guarda) | [🔴 calla](#f_vector_insert_end_ref_bucle) | [🟡 calla](#f_vector_insert_end_ref_llamada) |
| **puntero** | [🟡 calla](#f_vector_insert_end_ptr_recto) | [🟡 calla](#f_vector_insert_end_ptr_guarda) | [🔴 calla](#f_vector_insert_end_ptr_bucle) | [🟡 calla](#f_vector_insert_end_ptr_llamada) |

## Handle: iterador

### f_vector_insert_end_it_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `recto` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_insert_end_it_recto(std::vector<int>& c) {
  auto it = c.begin();
  c.insert(c.end(),1);
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
    iterator "this" @ 0x7fff2d33a170 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7fff2d33a290
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
64cfb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30ccfb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55baf19645cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c5cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55baf1968b18  (/tmp/mi-linter-runtime-validation/runtime_asan+0x310b18) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55baf19667dc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30e7dc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55baf1951513  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9513) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55baf187041f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x21841f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55baf190f5b5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b75b5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7faa03e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7faa03e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55baf16f82c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55baf185dfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55baf1964b37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55baf196427f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55baf1952650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55baf18f7f17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55baf190f5a8  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b75a8) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7faa03e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7faa03e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x55baf16f82c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x218520) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bda02fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bda02fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bda02fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bda02fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bda02fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bda02fe0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7bda02fe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bda02fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bda02fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bda02fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bda02fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==121==ABORTING
````

</details>

### f_vector_insert_end_it_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `guarda` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_insert_end_it_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.insert(c.end(),1);
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
    iterator "this" @ 0x7ffcc97e6340 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffcc97e6460
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
c3cfb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30ccfb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55b9f5bc35cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c5cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55b9f5bc7b18  (/tmp/mi-linter-runtime-validation/runtime_asan+0x310b18) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55b9f5bc57dc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30e7dc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55b9f5bb0513  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9513) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55b9f5acfb86  (/tmp/mi-linter-runtime-validation/runtime_asan+0x218b86) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55b9f5b6e72b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b772b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f9e01227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f9e012278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55b9f59572c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55b9f5abcfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55b9f5bc3b37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55b9f5bc327f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55b9f5bb1650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55b9f5b56f17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55b9f5b6e71e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b771e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7f9e01227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7f9e012278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x55b9f59572c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x218c8a) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bce003dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bce003dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bce003dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bce003dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bce003dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bce003e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7bce003e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bce003e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bce003e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bce003e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bce003e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==125==ABORTING
````

</details>

### f_vector_insert_end_it_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_vector_insert_end_it_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.insert(c.end(),1);
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
    iterator "this" @ 0x7ffe396a6f50 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffe396a7070
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
8b18  (/tmp/mi-linter-runtime-validation/runtime_asan+0x310b18) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x561f267867dc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30e7dc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x561f26771513  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9513) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x561f266913b4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2193b4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x561f2672f8a1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b78a1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f0e5be27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f0e5be278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x561f265182c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x561f2667dfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x561f26784b37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x561f2678427f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x561f26783097  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30b097) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x561f26771416  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9416) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x561f26770dfc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f8dfc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x561f267181a2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a01a2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x561f2672f894  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b7894) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f0e5be27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f0e5be278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x561f265182c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x2194b8) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b2e5afdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b2e5afdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b2e5afdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b2e5afdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b2e5afdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b2e5afe0000: fa fa fd fa fa fa fd fa fa fa[fd]fd fa fa fa fa
  0x7b2e5afe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b2e5afe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b2e5afe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b2e5afe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b2e5afe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==129==ABORTING
````

</details>

### f_vector_insert_end_it_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `llamada` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_insert_end_it_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_vector_insert_end(c);
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
    iterator "this" @ 0x7ffe2dfc6f10 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffe2dfc6fd0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
95cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c5cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x563bd699db18  (/tmp/mi-linter-runtime-validation/runtime_asan+0x310b18) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x563bd699b7dc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30e7dc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x563bd6986513  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9513) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x563bd6895244  (/tmp/mi-linter-runtime-validation/runtime_asan+0x208244) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x563bd68a69ff  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2199ff) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x563bd6944a17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b7a17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7f84b4227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7f84b42278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x563bd672d2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x563bd6892fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x563bd6999b37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x563bd699927f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x563bd6987650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x563bd692cf17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x563bd6944a0a  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b7a0a) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7f84b4227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7f84b42278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x563bd672d2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x219ae7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bb4b33dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bb4b33dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bb4b33dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bb4b33dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bb4b33dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bb4b33e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7bb4b33e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bb4b33e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bb4b33e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bb4b33e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bb4b33e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==131==ABORTING
````

</details>

## Handle: referencia

### f_vector_insert_end_ref_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `recto` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_insert_end_ref_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.insert(c.end(),1);
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
bccfb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30ccfb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55d8bfcbc5cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c5cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55d8bfcc0b18  (/tmp/mi-linter-runtime-validation/runtime_asan+0x310b18) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55d8bfcbe7dc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30e7dc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55d8bfca9513  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9513) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55d8bfbc9f74  (/tmp/mi-linter-runtime-validation/runtime_asan+0x219f74) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55d8bfc67b8d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b7b8d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fea86427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fea864278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55d8bfa502c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55d8bfbb5fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55d8bfcbcb37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55d8bfcbc27f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55d8bfcaa650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55d8bfc4ff17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55d8bfc67b80  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b7b80) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7fea86427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7fea864278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x55d8bfa502c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x219fbf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c1a855dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c1a855dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c1a855dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c1a855dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c1a855dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c1a855e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7c1a855e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c1a855e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c1a855e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c1a855e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c1a855e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==135==ABORTING
````

</details>

### f_vector_insert_end_ref_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `guarda` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_insert_end_ref_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.insert(c.end(),1);
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
8fcfb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30ccfb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x555fd318f5cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c5cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x555fd3193b18  (/tmp/mi-linter-runtime-validation/runtime_asan+0x310b18) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x555fd31917dc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30e7dc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x555fd317c513  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9513) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x555fd309d6d2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x21a6d2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x555fd313ad03  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b7d03) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f48aee27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f48aee278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x555fd2f232c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x555fd3088fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x555fd318fb37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x555fd318f27f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x555fd317d650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x555fd3122f17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x555fd313acf6  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b7cf6) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7f48aee27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7f48aee278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x555fd2f232c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x21a720) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b78adfdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b78adfdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b78adfdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b78adfdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b78adfdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b78adfe0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7b78adfe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b78adfe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b78adfe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b78adfe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b78adfe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==139==ABORTING
````

</details>

### f_vector_insert_end_ref_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_vector_insert_end_ref_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.insert(c.end(),1);
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
    iterator "this" @ 0x7fffee3245c0 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7fffee3246e0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
eb18  (/tmp/mi-linter-runtime-validation/runtime_asan+0x310b18) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55b82a6ac7dc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30e7dc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55b82a697513  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9513) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55b82a5b8f00  (/tmp/mi-linter-runtime-validation/runtime_asan+0x21af00) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55b82a655e79  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b7e79) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f9dd9627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f9dd96278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55b82a43e2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55b82a5a3fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55b82a6aab37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55b82a6aa27f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55b82a6a9097  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30b097) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55b82a697416  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9416) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55b82a696dfc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f8dfc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55b82a63e1a2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a01a2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55b82a655e6c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b7e6c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f9dd9627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f9dd96278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55b82a43e2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x21af51) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bbdd87dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bbdd87dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bbdd87dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bbdd87dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bbdd87dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bbdd87e0000: fa fa fd fa fa fa fd fa fa fa[fd]fd fa fa fa fa
  0x7bbdd87e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bbdd87e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bbdd87e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bbdd87e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bbdd87e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

### f_vector_insert_end_ref_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `llamada` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_insert_end_ref_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_vector_insert_end(c);
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
b5cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c5cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55c9b134fb18  (/tmp/mi-linter-runtime-validation/runtime_asan+0x310b18) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55c9b134d7dc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30e7dc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55c9b1338513  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9513) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55c9b1247244  (/tmp/mi-linter-runtime-validation/runtime_asan+0x208244) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55c9b125a548  (/tmp/mi-linter-runtime-validation/runtime_asan+0x21b548) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x55c9b12f6fef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b7fef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7fba1e627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7fba1e6278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x55c9b10df2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55c9b1244fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55c9b134bb37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55c9b134b27f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55c9b1339650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55c9b12def17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55c9b12f6fe2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b7fe2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7fba1e627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7fba1e6278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x55c9b10df2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x21b57d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bea1d7dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bea1d7dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bea1d7dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bea1d7dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bea1d7dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bea1d7e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7bea1d7e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bea1d7e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bea1d7e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bea1d7e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bea1d7e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

## Handle: puntero

### f_vector_insert_end_ptr_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `recto` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_insert_end_ptr_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.insert(c.end(),1);
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
03cfb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30ccfb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5631124035cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c5cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x563112407b18  (/tmp/mi-linter-runtime-validation/runtime_asan+0x310b18) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5631124057dc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30e7dc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5631123f0513  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9513) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5631123129e8  (/tmp/mi-linter-runtime-validation/runtime_asan+0x21b9e8) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5631123af165  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b8165) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f4e1d827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f4e1d8278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x5631121972c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5631122fcfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x563112403b37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x56311240327f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5631123f1650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x563112396f17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5631123af158  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b8158) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7f4e1d827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7f4e1d8278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x5631121972c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x21ba62) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b7e1c9dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b7e1c9dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b7e1c9dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b7e1c9dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b7e1c9dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b7e1c9e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7b7e1c9e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b7e1c9e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b7e1c9e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b7e1c9e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b7e1c9e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

### f_vector_insert_end_ptr_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `guarda` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_insert_end_ptr_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.insert(c.end(),1);
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
b9cfb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30ccfb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x560d3acb95cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c5cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x560d3acbdb18  (/tmp/mi-linter-runtime-validation/runtime_asan+0x310b18) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x560d3acbb7dc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30e7dc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x560d3aca6513  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9513) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x560d3abc9146  (/tmp/mi-linter-runtime-validation/runtime_asan+0x21c146) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x560d3ac652db  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b82db) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f7fc4e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f7fc4e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x560d3aa4d2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x560d3abb2fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x560d3acb9b37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x560d3acb927f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x560d3aca7650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x560d3ac4cf17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x560d3ac652ce  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b82ce) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7f7fc4e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7f7fc4e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x560d3aa4d2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x21c1c3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bafc3fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bafc3fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bafc3fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bafc3fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bafc3fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bafc3fe0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7bafc3fe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bafc3fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bafc3fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bafc3fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bafc3fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

### f_vector_insert_end_ptr_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_vector_insert_end_ptr_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.insert(c.end(),1);
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
    iterator "this" @ 0x7ffd099a70c0 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffd099a71e0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
fb18  (/tmp/mi-linter-runtime-validation/runtime_asan+0x310b18) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x555a19d5d7dc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30e7dc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x555a19d48513  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9513) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x555a19c6b974  (/tmp/mi-linter-runtime-validation/runtime_asan+0x21c974) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x555a19d07451  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b8451) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fae12a27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fae12a278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x555a19aef2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x555a19c54fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x555a19d5bb37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x555a19d5b27f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x555a19d5a097  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30b097) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x555a19d48416  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9416) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x555a19d47dfc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f8dfc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x555a19cef1a2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a01a2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x555a19d07444  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b8444) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7fae12a27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7fae12a278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x555a19aef2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x21c9f1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bce11bdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bce11bdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bce11bdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bce11bdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bce11bdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bce11be0000: fa fa fd fa fa fa fd fa fa fa[fd]fd fa fa fa fa
  0x7bce11be0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bce11be0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bce11be0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bce11be0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bce11be0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

### f_vector_insert_end_ptr_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `llamada` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_insert_end_ptr_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_vector_insert_end(c);
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
25cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c5cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x561624ae6b18  (/tmp/mi-linter-runtime-validation/runtime_asan+0x310b18) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x561624ae47dc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30e7dc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x561624acf513  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9513) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5616249de244  (/tmp/mi-linter-runtime-validation/runtime_asan+0x208244) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5616249f2fbc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x21cfbc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x561624a8e5c7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b85c7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #10 0x7ff0d6027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x7ff0d60278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #12 0x5616248762c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5616249dbfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x561624ae2b37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x561624ae227f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x561624ad0650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x561624a75f17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x561624a8e5ba  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b85ba) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7ff0d6027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7ff0d60278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x5616248762c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x21d020) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c20d51dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c20d51dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c20d51dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c20d51dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c20d51dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c20d51e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7c20d51e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c20d51e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c20d51e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c20d51e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c20d51e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
