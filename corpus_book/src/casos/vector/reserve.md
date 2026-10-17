# `std::vector::reserve`

Mutación: `c.reserve(c.size()+100);`

- Iterador retenido: 🟡 `POLICY`
- Referencia/puntero retenido: 🟡 `POLICY`
- Casos `UB` detectados estáticamente: 0/3

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🟡 calla](#f_vector_reserve_it_recto) | [🟡 calla](#f_vector_reserve_it_guarda) | [🔴 calla](#f_vector_reserve_it_bucle) | [🟡 calla](#f_vector_reserve_it_llamada) |
| **referencia** | [🟡 calla](#f_vector_reserve_ref_recto) | [🟡 calla](#f_vector_reserve_ref_guarda) | [🔴 calla](#f_vector_reserve_ref_bucle) | [🟡 calla](#f_vector_reserve_ref_llamada) |
| **puntero** | [🟡 calla](#f_vector_reserve_ptr_recto) | [🟡 calla](#f_vector_reserve_ptr_guarda) | [🔴 calla](#f_vector_reserve_ptr_bucle) | [🟡 calla](#f_vector_reserve_ptr_llamada) |

## Handle: iterador

### f_vector_reserve_it_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `recto` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_reserve_it_recto(std::vector<int>& c) {
  auto it = c.begin();
  c.reserve(c.size()+100);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | 🛑 attempt to dereference a singular iterator | 🛑 heap-use-after-free |
| `preserve` | capacidad 256, suficiente para size()+100 | — (código 0) | — (código 0) |

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
    iterator "this" @ 0x7ffc8a2d2ce0 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffc8a2d2d70
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
)

0x7b9e425e0040 is located 0 bytes inside of 32-byte region [0x7b9e425e0040,0x7b9e425e0060)
freed by thread T0 here:
    #0 0x5587309c4f61  (/tmp/mi-linter-runtime-validation/runtime_asan+0x206f61) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x558730acad52  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cd52) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x558730acacfb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30ccfb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x558730ab8a88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2faa88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5587309e76c0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2296c0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x558730a798d5  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bb8d5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7f6e43427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7f6e434278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x55873085e2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5587309c3fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x558730acab37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x558730aca27f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x558730ab8650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x558730a5df17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x558730a798c8  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bb8c8) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7f6e43427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7f6e434278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x55873085e2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x2297a2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b9e425dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9e425dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9e425dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9e425dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b9e425dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b9e425e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7b9e425e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b9e425e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b9e425e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b9e425e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b9e425e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

### f_vector_reserve_it_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `guarda` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_reserve_it_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.reserve(c.size()+100);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | 🛑 attempt to dereference a singular iterator | 🛑 heap-use-after-free |
| `preserve` | capacidad 256, suficiente para size()+100 | — (código 0) | — (código 0) |

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
    iterator "this" @ 0x7ffc25692c80 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffc25692d40
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
)

0x7bd652be0040 is located 0 bytes inside of 32-byte region [0x7bd652be0040,0x7bd652be0060)
freed by thread T0 here:
    #0 0x557eacf06f61  (/tmp/mi-linter-runtime-validation/runtime_asan+0x206f61) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x557ead00cd52  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cd52) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x557ead00ccfb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30ccfb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x557eacffaa88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2faa88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x557eacf29be4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x229be4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x557eacfbba4b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bba4b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7fa653a27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7fa653a278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x557eacda02c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x557eacf05fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x557ead00cb37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x557ead00c27f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x557eacffa650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x557eacf9ff17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x557eacfbba3e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bba3e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7fa653a27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7fa653a278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x557eacda02c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x229ccc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bd652bdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd652bdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd652bdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd652bdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd652bdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bd652be0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7bd652be0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd652be0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd652be0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd652be0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd652be0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

### f_vector_reserve_it_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_vector_reserve_it_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.reserve(c.size()+100);
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
    iterator "this" @ 0x7ffd374569a0 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffd37456a60
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
c2ed52  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cd52) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x556e1bc2ecfb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30ccfb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x556e1bc1ca88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2faa88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x556e1bb4c1d4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x22a1d4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x556e1bbddbc1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bbbc1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7fd639027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7fd6390278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x556e1b9c22c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x556e1bb27fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x556e1bc2eb37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x556e1bc2e27f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x556e1bc2d097  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30b097) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x556e1bc1b416  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9416) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x556e1bc1adfc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f8dfc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x556e1bbc21a2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a01a2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x556e1bbddbb4  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bbbb4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7fd639027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7fd6390278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x556e1b9c22c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x22a2bf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bf6381dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf6381dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf6381dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf6381dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf6381dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bf6381e0000: fa fa fd fa fa fa fd fa fa fa[fd]fd fa fa fa fa
  0x7bf6381e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf6381e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf6381e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf6381e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf6381e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

### f_vector_reserve_it_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `llamada` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_reserve_it_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_vector_reserve(c);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | 🛑 attempt to dereference a singular iterator | 🛑 heap-use-after-free |
| `preserve` | capacidad 256, suficiente para size()+100 | — (código 0) | — (código 0) |

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
    iterator "this" @ 0x7ffc0b939b10 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffc0b939bd0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
f3fcf61  (/tmp/mi-linter-runtime-validation/runtime_asan+0x206f61) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55619f502d52  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cd52) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55619f502cfb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30ccfb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55619f4f0a88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2faa88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55619f3fe74e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x20874e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55619f4207df  (/tmp/mi-linter-runtime-validation/runtime_asan+0x22a7df) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55619f4b1d37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bbd37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x7fabaa627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x7fabaa6278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x55619f2962c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55619f3fbfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55619f502b37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55619f50227f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55619f4f0650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55619f495f17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55619f4b1d2a  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bbd2a) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7fabaa627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7fabaa6278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x55619f2962c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x22a8c7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bdba97dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bdba97dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bdba97dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bdba97dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bdba97dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bdba97e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7bdba97e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bdba97e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bdba97e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bdba97e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bdba97e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

## Handle: referencia

### f_vector_reserve_ref_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `recto` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_reserve_ref_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.reserve(c.size()+100);
  sink(h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | — (código 0) | 🛑 heap-use-after-free |
| `preserve` | capacidad 256, suficiente para size()+100 | — (código 0) | — (código 0) |

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
)

0x7b96783e0040 is located 0 bytes inside of 32-byte region [0x7b96783e0040,0x7b96783e0060)
freed by thread T0 here:
    #0 0x5627e8e94f61  (/tmp/mi-linter-runtime-validation/runtime_asan+0x206f61) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5627e8f9ad52  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cd52) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5627e8f9acfb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30ccfb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5627e8f88a88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2faa88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5627e8eb8b9d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x22ab9d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5627e8f49ead  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bbead) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7f6679227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7f66792278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x5627e8d2e2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5627e8e93fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5627e8f9ab37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5627e8f9a27f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5627e8f88650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5627e8f2df17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5627e8f49ea0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bbea0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7f6679227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7f66792278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x5627e8d2e2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x22abd5) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b96783dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b96783dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b96783dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b96783dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b96783dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b96783e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7b96783e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b96783e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b96783e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b96783e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b96783e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

### f_vector_reserve_ref_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `guarda` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_reserve_ref_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.reserve(c.size()+100);
  sink(h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | — (código 0) | 🛑 heap-use-after-free |
| `preserve` | capacidad 256, suficiente para size()+100 | — (código 0) | — (código 0) |

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
)

0x7bb9c33e0040 is located 0 bytes inside of 32-byte region [0x7bb9c33e0040,0x7bb9c33e0060)
freed by thread T0 here:
    #0 0x55937a8b5f61  (/tmp/mi-linter-runtime-validation/runtime_asan+0x206f61) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55937a9bbd52  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cd52) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55937a9bbcfb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30ccfb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55937a9a9a88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2faa88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55937a8da0f1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x22b0f1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55937a96b023  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bc023) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7f89c4227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7f89c42278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x55937a74f2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55937a8b4fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55937a9bbb37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55937a9bb27f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55937a9a9650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55937a94ef17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55937a96b016  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bc016) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7f89c4227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7f89c42278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x55937a74f2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x22b129) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bb9c33dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bb9c33dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bb9c33dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bb9c33dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bb9c33dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bb9c33e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7bb9c33e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bb9c33e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bb9c33e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bb9c33e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bb9c33e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==271==ABORTING
````

</details>

### f_vector_reserve_ref_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_vector_reserve_ref_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.reserve(c.size()+100);
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
    iterator "this" @ 0x7ffe2c5eadb0 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffe2c5eae70
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
1f1d52  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cd52) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55c1171f1cfb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30ccfb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55c1171dfa88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2faa88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55c1171106de  (/tmp/mi-linter-runtime-validation/runtime_asan+0x22b6de) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55c1171a1199  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bc199) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7fca8ea27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7fca8ea278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x55c116f852c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55c1170eafe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55c1171f1b37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55c1171f127f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55c1171f0097  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30b097) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55c1171de416  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9416) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55c1171dddfc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f8dfc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55c1171851a2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a01a2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55c1171a118c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bc18c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7fca8ea27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7fca8ea278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55c116f852c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x22b716) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bea8dbdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bea8dbdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bea8dbdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bea8dbdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bea8dbdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bea8dbe0000: fa fa fd fa fa fa fd fa fa fa[fd]fd fa fa fa fa
  0x7bea8dbe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bea8dbe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bea8dbe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bea8dbe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bea8dbe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==275==ABORTING
````

</details>

### f_vector_reserve_ref_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `llamada` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_reserve_ref_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_vector_reserve(c);
  sink(h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | — (código 0) | 🛑 heap-use-after-free |
| `preserve` | capacidad 256, suficiente para size()+100 | — (código 0) | — (código 0) |

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
cdf4f61  (/tmp/mi-linter-runtime-validation/runtime_asan+0x206f61) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55af5cefad52  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cd52) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55af5cefacfb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30ccfb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55af5cee8a88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2faa88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55af5cdf674e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x20874e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55af5ce19ce8  (/tmp/mi-linter-runtime-validation/runtime_asan+0x22bce8) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55af5ceaa30f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bc30f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x7f3fcb227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x7f3fcb2278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x55af5cc8e2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55af5cdf3fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55af5cefab37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55af5cefa27f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55af5cee8650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55af5ce8df17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55af5ceaa302  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bc302) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7f3fcb227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7f3fcb2278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x55af5cc8e2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x22bd1d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b6fca3dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b6fca3dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b6fca3dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b6fca3dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b6fca3dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b6fca3e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7b6fca3e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b6fca3e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b6fca3e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b6fca3e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b6fca3e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==277==ABORTING
````

</details>

## Handle: puntero

### f_vector_reserve_ptr_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `recto` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_reserve_ptr_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.reserve(c.size()+100);
  sink(*h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | — (código 0) | 🛑 heap-use-after-free |
| `preserve` | capacidad 256, suficiente para size()+100 | — (código 0) | — (código 0) |

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
)

0x7bfeff1e0040 is located 0 bytes inside of 32-byte region [0x7bfeff1e0040,0x7bfeff1e0060)
freed by thread T0 here:
    #0 0x55b17d3bbf61  (/tmp/mi-linter-runtime-validation/runtime_asan+0x206f61) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55b17d4c1d52  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cd52) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55b17d4c1cfb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30ccfb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55b17d4afa88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2faa88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55b17d3e0fd1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x22bfd1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55b17d471485  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bc485) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7fcf00027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7fcf000278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x55b17d2552c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55b17d3bafe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55b17d4c1b37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55b17d4c127f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55b17d4af650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55b17d454f17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55b17d471478  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bc478) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7fcf00027780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7fcf000278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x55b17d2552c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x22c035) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bfeff1dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bfeff1dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bfeff1dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bfeff1dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bfeff1dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bfeff1e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7bfeff1e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bfeff1e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bfeff1e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bfeff1e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bfeff1e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==281==ABORTING
````

</details>

### f_vector_reserve_ptr_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `guarda` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_reserve_ptr_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.reserve(c.size()+100);
  sink(*h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | — (código 0) | 🛑 heap-use-after-free |
| `preserve` | capacidad 256, suficiente para size()+100 | — (código 0) | — (código 0) |

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
)

0x7c2148be0040 is located 0 bytes inside of 32-byte region [0x7c2148be0040,0x7c2148be0060)
freed by thread T0 here:
    #0 0x558d56aadf61  (/tmp/mi-linter-runtime-validation/runtime_asan+0x206f61) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x558d56bb3d52  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cd52) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x558d56bb3cfb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30ccfb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x558d56ba1a88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2faa88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x558d56ad3525  (/tmp/mi-linter-runtime-validation/runtime_asan+0x22c525) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x558d56b635fb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bc5fb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7ff149a27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7ff149a278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x558d569472c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x558d56aacfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x558d56bb3b37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x558d56bb327f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x558d56ba1650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x558d56b46f17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x558d56b635ee  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bc5ee) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7ff149a27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7ff149a278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x558d569472c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x22c589) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c2148bdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c2148bdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c2148bdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c2148bdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c2148bdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c2148be0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7c2148be0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c2148be0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c2148be0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c2148be0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c2148be0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==285==ABORTING
````

</details>

### f_vector_reserve_ptr_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_vector_reserve_ptr_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.reserve(c.size()+100);
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
    iterator "this" @ 0x7fffad32cf30 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7fffad32cff0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
1bad52  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cd52) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55a4141bacfb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30ccfb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55a4141a8a88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2faa88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55a4140dab12  (/tmp/mi-linter-runtime-validation/runtime_asan+0x22cb12) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55a41416a771  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bc771) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7f543e227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7f543e2278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x55a413f4e2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55a4140b3fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55a4141bab37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55a4141ba27f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55a4141b9097  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30b097) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55a4141a7416  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9416) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55a4141a6dfc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f8dfc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55a41414e1a2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a01a2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55a41416a764  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bc764) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f543e227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f543e2278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55a413f4e2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x22cb76) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b743d3dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b743d3dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b743d3dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b743d3dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b743d3dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b743d3e0000: fa fa fd fa fa fa fd fa fa fa[fd]fd fa fa fa fa
  0x7b743d3e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b743d3e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b743d3e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b743d3e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b743d3e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==289==ABORTING
````

</details>

### f_vector_reserve_ptr_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `llamada` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_reserve_ptr_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_vector_reserve(c);
  sink(*h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | — (código 0) | 🛑 heap-use-after-free |
| `preserve` | capacidad 256, suficiente para size()+100 | — (código 0) | — (código 0) |

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
b9ebf61  (/tmp/mi-linter-runtime-validation/runtime_asan+0x206f61) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x556a9baf1d52  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cd52) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x556a9baf1cfb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30ccfb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x556a9badfa88  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2faa88) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x556a9b9ed74e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x20874e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x556a9ba1211c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x22d11c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x556a9baa18e7  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bc8e7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x7f41aae27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x7f41aae278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x556a9b8852c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x556a9b9eafe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x556a9baf1b37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x556a9baf127f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x556a9badf650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x556a9ba84f17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x556a9baa18da  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bc8da) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7f41aae27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7f41aae278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x556a9b8852c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x22d180) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b71a9fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b71a9fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b71a9fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b71a9fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b71a9fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b71a9fe0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7b71a9fe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b71a9fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b71a9fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b71a9fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b71a9fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==291==ABORTING
````

</details>
