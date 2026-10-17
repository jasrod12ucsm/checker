# `std::vector::emplace_back`

Mutación: `c.emplace_back(1);`

- Iterador retenido: 🟡 `POLICY`
- Referencia/puntero retenido: 🟡 `POLICY`
- Casos `UB` detectados estáticamente: 0/3

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🟡 calla](#f_vector_emplace_back_it_recto) | [🟡 calla](#f_vector_emplace_back_it_guarda) | [🔴 calla](#f_vector_emplace_back_it_bucle) | [🟡 calla](#f_vector_emplace_back_it_llamada) |
| **referencia** | [🟡 calla](#f_vector_emplace_back_ref_recto) | [🟡 calla](#f_vector_emplace_back_ref_guarda) | [🔴 calla](#f_vector_emplace_back_ref_bucle) | [🟡 calla](#f_vector_emplace_back_ref_llamada) |
| **puntero** | [🟡 calla](#f_vector_emplace_back_ptr_recto) | [🟡 calla](#f_vector_emplace_back_ptr_guarda) | [🔴 calla](#f_vector_emplace_back_ptr_bucle) | [🟡 calla](#f_vector_emplace_back_ptr_llamada) |

## Handle: iterador

### f_vector_emplace_back_it_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `recto` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_emplace_back_it_recto(std::vector<int>& c) {
  auto it = c.begin();
  c.emplace_back(1);
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
    iterator "this" @ 0x7ffe7374fa10 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffe7374faa0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
cde8d52  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cd52) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5604dcde8cfb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30ccfb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5604dcde85cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c5cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5604dcde7661  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30b661) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5604dcdd5416  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9416) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5604dcceb617  (/tmp/mi-linter-runtime-validation/runtime_asan+0x20f617) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5604dcd912a5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b52a5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f692b627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f692b6278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x5604dcb7c2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5604dcce1fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5604dcde8b37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5604dcde827f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5604dcdd6650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5604dcd7bf17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5604dcd91298  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b5298) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7f692b627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7f692b6278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x5604dcb7c2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x20f701) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b992a7dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b992a7dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b992a7dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b992a7dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b992a7dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b992a7e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7b992a7e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b992a7e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b992a7e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b992a7e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b992a7e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==55==ABORTING
````

</details>

### f_vector_emplace_back_it_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `guarda` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_emplace_back_it_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.emplace_back(1);
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
    iterator "this" @ 0x7ffed9e580d0 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffed9e58190
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
6647d52  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cd52) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x563f56647cfb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30ccfb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x563f566475cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c5cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x563f56646661  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30b661) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x563f56634416  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9416) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x563f5654ab35  (/tmp/mi-linter-runtime-validation/runtime_asan+0x20fb35) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x563f565f041b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b541b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f0d24c27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f0d24c278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x563f563db2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x563f56540fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x563f56647b37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x563f5664727f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x563f56635650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x563f565daf17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x563f565f040e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b540e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7f0d24c27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7f0d24c278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x563f563db2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x20fc25) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b3d23ddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b3d23ddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b3d23ddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b3d23ddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b3d23ddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b3d23de0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7b3d23de0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b3d23de0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b3d23de0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b3d23de0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b3d23de0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==59==ABORTING
````

</details>

### f_vector_emplace_back_it_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_vector_emplace_back_it_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.emplace_back(1);
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
    iterator "this" @ 0x7ffd308612c0 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffd30861380
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
d585cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c5cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x556affd57661  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30b661) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x556affd45416  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9416) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x556affc5c0f3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2100f3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x556affd01591  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b5591) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7ff1e7227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7ff1e72278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x556affaec2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x556affc51fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x556affd58b37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x556affd5827f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x556affd57097  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30b097) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x556affd45416  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9416) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x556affd44dfc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f8dfc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x556affcec1a2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a01a2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x556affd01584  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b5584) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7ff1e7227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7ff1e72278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x556affaec2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x2101e9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c11e63dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c11e63dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c11e63dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c11e63dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c11e63dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c11e63e0000: fa fa fd fa fa fa fd fa fa fa[fd]fd fa fa fa fa
  0x7c11e63e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c11e63e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c11e63e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c11e63e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c11e63e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==63==ABORTING
````

</details>

### f_vector_emplace_back_it_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `llamada` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_emplace_back_it_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_vector_emplace_back(c);
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
    iterator "this" @ 0x7ffcebc916f0 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffcebc917b0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
1edcfb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30ccfb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x564be31ed5cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c5cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x564be31ec661  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30b661) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x564be31da416  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9416) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x564be30e8be3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x207be3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x564be30f16ff  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2106ff) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x564be3196707  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b5707) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fd66a827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fd66a8278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x564be2f812c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x564be30e6fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x564be31edb37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x564be31ed27f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x564be31db650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x564be3180f17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x564be31966fa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b56fa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7fd66a827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7fd66a8278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x564be2f812c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x2107e7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c06699dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c06699dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c06699dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c06699dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c06699dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c06699e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7c06699e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c06699e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c06699e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c06699e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c06699e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==65==ABORTING
````

</details>

## Handle: referencia

### f_vector_emplace_back_ref_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `recto` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_emplace_back_ref_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.emplace_back(1);
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
5f8ed52  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cd52) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5570c5f8ecfb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30ccfb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5570c5f8e5cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c5cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5570c5f8d661  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30b661) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5570c5f7b416  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9416) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5570c5e92aa1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x210aa1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5570c5f3787d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b587d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7fa6e2627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7fa6e26278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x5570c5d222c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5570c5e87fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5570c5f8eb37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5570c5f8e27f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5570c5f7c650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5570c5f21f17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5570c5f37870  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b5870) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7fa6e2627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7fa6e26278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x5570c5d222c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x210ae1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bd6e17dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd6e17dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd6e17dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd6e17dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd6e17dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bd6e17e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7bd6e17e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd6e17e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd6e17e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd6e17e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd6e17e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==69==ABORTING
````

</details>

### f_vector_emplace_back_ref_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `guarda` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_emplace_back_ref_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.emplace_back(1);
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
876ed52  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cd52) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5636d876ecfb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30ccfb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5636d876e5cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c5cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5636d876d661  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30b661) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5636d875b416  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9416) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5636d8672fef  (/tmp/mi-linter-runtime-validation/runtime_asan+0x210fef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5636d87179f3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b59f3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7fa6ea627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7fa6ea6278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x5636d85022c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5636d8667fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5636d876eb37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5636d876e27f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5636d875c650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5636d8701f17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5636d87179e6  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b59e6) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7fa6ea627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7fa6ea6278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x5636d85022c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x211032) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bd6e97dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd6e97dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd6e97dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd6e97dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd6e97dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bd6e97e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7bd6e97e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd6e97e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd6e97e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd6e97e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd6e97e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==73==ABORTING
````

</details>

### f_vector_emplace_back_ref_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_vector_emplace_back_ref_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.emplace_back(1);
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
    iterator "this" @ 0x7ffd2aac1bd0 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffd2aac1c90
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
5d95cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c5cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55a1835d8661  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30b661) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55a1835c6416  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9416) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55a1834de5cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2115cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55a183582b69  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b5b69) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7efc39a27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7efc39a278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55a18336d2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55a1834d2fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55a1835d9b37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55a1835d927f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55a1835d8097  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30b097) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55a1835c6416  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9416) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55a1835c5dfc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f8dfc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55a18356d1a2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a01a2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55a183582b5c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b5b5c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7efc39a27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7efc39a278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55a18336d2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x211612) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b1c38bdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b1c38bdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b1c38bdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b1c38bdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b1c38bdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b1c38be0000: fa fa fd fa fa fa fd fa fa fa[fd]fd fa fa fa fa
  0x7b1c38be0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b1c38be0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b1c38be0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b1c38be0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b1c38be0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==77==ABORTING
````

</details>

### f_vector_emplace_back_ref_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `llamada` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_emplace_back_ref_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_vector_emplace_back(c);
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
812cfb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30ccfb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x558d7b8125cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c5cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x558d7b811661  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30b661) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x558d7b7ff416  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9416) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x558d7b70dbe3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x207be3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x558d7b717be8  (/tmp/mi-linter-runtime-validation/runtime_asan+0x211be8) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x558d7b7bbcdf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b5cdf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f2253027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f22530278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x558d7b5a62c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x558d7b70bfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x558d7b812b37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x558d7b81227f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x558d7b800650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x558d7b7a5f17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x558d7b7bbcd2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b5cd2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7f2253027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7f22530278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x558d7b5a62c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x211c1d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b52521dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b52521dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b52521dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b52521dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b52521dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b52521e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7b52521e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b52521e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b52521e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b52521e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b52521e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==79==ABORTING
````

</details>

## Handle: puntero

### f_vector_emplace_back_ptr_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `recto` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_emplace_back_ptr_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.emplace_back(1);
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
ab5dd52  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cd52) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x56262ab5dcfb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30ccfb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x56262ab5d5cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c5cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x56262ab5c661  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30b661) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x56262ab4a416  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9416) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x56262aa62eb5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x211eb5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x56262ab06e55  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b5e55) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f6c65627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f6c656278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x56262a8f12c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x56262aa56fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x56262ab5db37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x56262ab5d27f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x56262ab4b650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x56262aaf0f17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x56262ab06e48  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b5e48) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7f6c65627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7f6c656278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x56262a8f12c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x211f21) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b9c647dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9c647dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9c647dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9c647dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9c647dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b9c647e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7b9c647e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b9c647e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b9c647e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b9c647e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b9c647e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==83==ABORTING
````

</details>

### f_vector_emplace_back_ptr_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `guarda` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_emplace_back_ptr_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.emplace_back(1);
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
40a2d52  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cd52) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55d7a40a2cfb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30ccfb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55d7a40a25cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c5cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55d7a40a1661  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30b661) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55d7a408f416  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9416) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55d7a3fa8403  (/tmp/mi-linter-runtime-validation/runtime_asan+0x212403) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55d7a404bfcb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b5fcb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f7150427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f71504278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55d7a3e362c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55d7a3f9bfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55d7a40a2b37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55d7a40a227f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55d7a4090650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55d7a4035f17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55d7a404bfbe  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b5fbe) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7f7150427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7f71504278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x55d7a3e362c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x212472) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7ba14f5dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ba14f5dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ba14f5dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ba14f5dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ba14f5dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7ba14f5e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7ba14f5e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ba14f5e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ba14f5e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ba14f5e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ba14f5e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==87==ABORTING
````

</details>

### f_vector_emplace_back_ptr_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_vector_emplace_back_ptr_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.emplace_back(1);
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
    iterator "this" @ 0x7ffeeb24d680 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffeeb24d740
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
3b35cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c5cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x56061a3b2661  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30b661) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x56061a3a0416  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9416) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x56061a2b99e3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2129e3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x56061a35d141  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b6141) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7fb2bd627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7fb2bd6278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x56061a1472c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x56061a2acfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x56061a3b3b37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x56061a3b327f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x56061a3b2097  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30b097) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x56061a3a0416  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9416) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x56061a39fdfc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f8dfc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x56061a3471a2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a01a2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x56061a35d134  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b6134) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7fb2bd627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7fb2bd6278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x56061a1472c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x212a52) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bd2bc7dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd2bc7dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd2bc7dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd2bc7dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd2bc7dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bd2bc7e0000: fa fa fd fa fa fa fd fa fa fa[fd]fd fa fa fa fa
  0x7bd2bc7e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd2bc7e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd2bc7e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd2bc7e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd2bc7e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==91==ABORTING
````

</details>

### f_vector_emplace_back_ptr_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `llamada` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_emplace_back_ptr_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_vector_emplace_back(c);
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
8bacfb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30ccfb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5640c28ba5cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c5cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5640c28b9661  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30b661) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5640c28a7416  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9416) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5640c27b5be3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x207be3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5640c27c0ffc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x212ffc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x5640c28642b7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b62b7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f13a6627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f13a66278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x5640c264e2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5640c27b3fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5640c28bab37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5640c28ba27f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5640c28a8650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5640c284df17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5640c28642aa  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2b62aa) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7f13a6627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7f13a66278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x5640c264e2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x213060) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b43a57dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b43a57dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b43a57dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b43a57dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b43a57dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b43a57e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7b43a57e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b43a57e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b43a57e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b43a57e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b43a57e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==93==ABORTING
````

</details>
