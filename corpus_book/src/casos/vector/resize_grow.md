# `std::vector::resize_grow`

Mutación: `c.resize(c.size()+100);`

- Iterador retenido: 🟡 `POLICY`
- Referencia/puntero retenido: 🟡 `POLICY`
- Casos `UB` detectados estáticamente: 0/3

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🟡 calla](#f_vector_resize_grow_it_recto) | [🟡 calla](#f_vector_resize_grow_it_guarda) | [🔴 calla](#f_vector_resize_grow_it_bucle) | [🟡 calla](#f_vector_resize_grow_it_llamada) |
| **referencia** | [🟡 calla](#f_vector_resize_grow_ref_recto) | [🟡 calla](#f_vector_resize_grow_ref_guarda) | [🔴 calla](#f_vector_resize_grow_ref_bucle) | [🟡 calla](#f_vector_resize_grow_ref_llamada) |
| **puntero** | [🟡 calla](#f_vector_resize_grow_ptr_recto) | [🟡 calla](#f_vector_resize_grow_ptr_guarda) | [🔴 calla](#f_vector_resize_grow_ptr_bucle) | [🟡 calla](#f_vector_resize_grow_ptr_llamada) |

## Handle: iterador

### f_vector_resize_grow_it_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `recto` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_resize_grow_it_recto(std::vector<int>& c) {
  auto it = c.begin();
  c.resize(c.size()+100);
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
    iterator "this" @ 0x7ffc4e54a8f0 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffc4e54a980
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
61fd52  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cd52) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x56346761fcfb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30ccfb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x56346761f5cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c5cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x563467626f58  (/tmp/mi-linter-runtime-validation/runtime_asan+0x313f58) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x56346760d23d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa23d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5634675389f0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2259f0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5634675cd74d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2ba74d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f9c79a27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f9c79a278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x5634673b32c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x563467518fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x56346761fb37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x56346761f27f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x56346760d650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5634675b2f17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5634675cd740  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2ba740) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7f9c79a27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7f9c79a278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x5634673b32c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x225ad2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bcc78bdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bcc78bdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bcc78bdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bcc78bdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bcc78bdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bcc78be0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7bcc78be0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bcc78be0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bcc78be0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bcc78be0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bcc78be0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==211==ABORTING
````

</details>

### f_vector_resize_grow_it_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `guarda` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_resize_grow_it_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.resize(c.size()+100);
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
    iterator "this" @ 0x7fff22dba2f0 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7fff22dba3b0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
9add52  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cd52) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x558b9e9adcfb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30ccfb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x558b9e9ad5cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c5cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x558b9e9b4f58  (/tmp/mi-linter-runtime-validation/runtime_asan+0x313f58) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x558b9e99b23d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa23d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x558b9e8c6f14  (/tmp/mi-linter-runtime-validation/runtime_asan+0x225f14) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x558b9e95b8c3  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2ba8c3) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7fc14f427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7fc14f4278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x558b9e7412c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x558b9e8a6fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x558b9e9adb37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x558b9e9ad27f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x558b9e99b650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x558b9e940f17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x558b9e95b8b6  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2ba8b6) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7fc14f427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7fc14f4278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x558b9e7412c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x225ffc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bf14e5dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf14e5dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf14e5dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf14e5dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf14e5dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bf14e5e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7bf14e5e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf14e5e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf14e5e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf14e5e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf14e5e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

### f_vector_resize_grow_it_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_vector_resize_grow_it_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.resize(c.size()+100);
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
    iterator "this" @ 0x7ffc6bfc0f80 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffc6bfc1040
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
bc5cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c5cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5606f29c3f58  (/tmp/mi-linter-runtime-validation/runtime_asan+0x313f58) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5606f29aa23d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa23d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5606f28d6504  (/tmp/mi-linter-runtime-validation/runtime_asan+0x226504) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5606f296aa39  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2baa39) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7ffb2a227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7ffb2a2278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x5606f27502c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5606f28b5fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5606f29bcb37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5606f29bc27f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5606f29bb097  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30b097) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5606f29a9416  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9416) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5606f29a8dfc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f8dfc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5606f29501a2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a01a2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5606f296aa2c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2baa2c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7ffb2a227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7ffb2a2278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x5606f27502c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x2265ef) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c1b293dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c1b293dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c1b293dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c1b293dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c1b293dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c1b293e0000: fa fa fd fa fa fa fd fa fa fa[fd]fd fa fa fa fa
  0x7c1b293e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c1b293e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c1b293e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c1b293e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c1b293e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

### f_vector_resize_grow_it_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `llamada` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_resize_grow_it_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_vector_resize_grow(c);
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
    iterator "this" @ 0x7fff5dd10980 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7fff5dd10a40
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
66cfb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30ccfb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55aac99665cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c5cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55aac996df58  (/tmp/mi-linter-runtime-validation/runtime_asan+0x313f58) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55aac995423d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa23d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55aac98626be  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2086be) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55aac9880b0f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x226b0f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55aac9914baf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2babaf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f2111a27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f2111a278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55aac96fa2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55aac985ffe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55aac9966b37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55aac996627f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55aac9954650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55aac98f9f17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55aac9914ba2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2baba2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7f2111a27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7f2111a278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x55aac96fa2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x226bf7) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b5110bdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b5110bdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b5110bdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b5110bdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b5110bdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b5110be0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7b5110be0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b5110be0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b5110be0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b5110be0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b5110be0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

## Handle: referencia

### f_vector_resize_grow_ref_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `recto` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_resize_grow_ref_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.resize(c.size()+100);
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
3a9d52  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cd52) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5644ce3a9cfb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30ccfb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5644ce3a95cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c5cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5644ce3b0f58  (/tmp/mi-linter-runtime-validation/runtime_asan+0x313f58) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5644ce39723d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa23d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5644ce2c3ecd  (/tmp/mi-linter-runtime-validation/runtime_asan+0x226ecd) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5644ce357d25  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bad25) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f4653427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f46534278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x5644ce13d2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5644ce2a2fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5644ce3a9b37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5644ce3a927f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5644ce397650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5644ce33cf17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5644ce357d18  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bad18) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7f4653427780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7f46534278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x5644ce13d2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x226f05) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b76525dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b76525dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b76525dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b76525dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b76525dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b76525e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7b76525e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b76525e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b76525e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b76525e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b76525e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

### f_vector_resize_grow_ref_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `guarda` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_resize_grow_ref_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.resize(c.size()+100);
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
9e1d52  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cd52) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5653a99e1cfb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30ccfb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5653a99e15cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c5cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5653a99e8f58  (/tmp/mi-linter-runtime-validation/runtime_asan+0x313f58) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5653a99cf23d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa23d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5653a98fc421  (/tmp/mi-linter-runtime-validation/runtime_asan+0x227421) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5653a998fe9b  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bae9b) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f5df5e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f5df5e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x5653a97752c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5653a98dafe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5653a99e1b37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5653a99e127f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5653a99cf650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5653a9974f17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5653a998fe8e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bae8e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7f5df5e27780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7f5df5e278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x5653a97752c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x227459) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b8df4fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b8df4fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b8df4fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b8df4fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b8df4fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b8df4fe0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7b8df4fe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b8df4fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b8df4fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b8df4fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b8df4fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

### f_vector_resize_grow_ref_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_vector_resize_grow_ref_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.resize(c.size()+100);
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
    iterator "this" @ 0x7ffeb46d4fb0 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffeb46d5070
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
7b5cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c5cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5560f3182f58  (/tmp/mi-linter-runtime-validation/runtime_asan+0x313f58) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5560f316923d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa23d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5560f3096a0e  (/tmp/mi-linter-runtime-validation/runtime_asan+0x227a0e) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5560f312a011  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bb011) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7fbade227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7fbade2278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x5560f2f0f2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x5560f3074fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x5560f317bb37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x5560f317b27f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x5560f317a097  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30b097) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x5560f3168416  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9416) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x5560f3167dfc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f8dfc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x5560f310f1a2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a01a2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x5560f312a004  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bb004) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7fbade227780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7fbade2278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x5560f2f0f2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x227a46) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bdadd3dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bdadd3dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bdadd3dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bdadd3dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bdadd3dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bdadd3e0000: fa fa fd fa fa fa fd fa fa fa[fd]fd fa fa fa fa
  0x7bdadd3e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bdadd3e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bdadd3e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bdadd3e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bdadd3e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

### f_vector_resize_grow_ref_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `llamada` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_resize_grow_ref_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_vector_resize_grow(c);
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
0fcfb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30ccfb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x557d5ab0f5cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c5cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x557d5ab16f58  (/tmp/mi-linter-runtime-validation/runtime_asan+0x313f58) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x557d5aafd23d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa23d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x557d5aa0b6be  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2086be) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x557d5aa2b018  (/tmp/mi-linter-runtime-validation/runtime_asan+0x228018) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x557d5aabe187  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bb187) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7f5655627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7f56556278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x557d5a8a32c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x557d5aa08fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x557d5ab0fb37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x557d5ab0f27f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x557d5aafd650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x557d5aaa2f17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x557d5aabe17a  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bb17a) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7f5655627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7f56556278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x557d5a8a32c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x22804d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b86547dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b86547dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b86547dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b86547dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b86547dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b86547e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7b86547e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b86547e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b86547e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b86547e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b86547e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

## Handle: puntero

### f_vector_resize_grow_ptr_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `recto` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_resize_grow_ptr_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.resize(c.size()+100);
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
19ad52  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cd52) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x559b1b19acfb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30ccfb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x559b1b19a5cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c5cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x559b1b1a1f58  (/tmp/mi-linter-runtime-validation/runtime_asan+0x313f58) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x559b1b18823d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa23d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x559b1b0b6301  (/tmp/mi-linter-runtime-validation/runtime_asan+0x228301) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x559b1b1492fd  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bb2fd) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f2741627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f27416278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x559b1af2e2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x559b1b093fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x559b1b19ab37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x559b1b19a27f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x559b1b188650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x559b1b12df17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x559b1b1492f0  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bb2f0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7f2741627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7f27416278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x559b1af2e2c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x228365) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b57407dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b57407dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b57407dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b57407dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b57407dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b57407e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7b57407e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b57407e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b57407e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b57407e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b57407e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==239==ABORTING
````

</details>

### f_vector_resize_grow_ptr_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `guarda` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_resize_grow_ptr_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.resize(c.size()+100);
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
04fd52  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cd52) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x562c2204fcfb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30ccfb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x562c2204f5cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c5cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x562c22056f58  (/tmp/mi-linter-runtime-validation/runtime_asan+0x313f58) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x562c2203d23d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa23d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x562c21f6b855  (/tmp/mi-linter-runtime-validation/runtime_asan+0x228855) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x562c21ffe473  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bb473) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7fd341827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7fd3418278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x562c21de32c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x562c21f48fe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x562c2204fb37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x562c2204f27f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x562c2203d650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x562c21fe2f17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x562c21ffe466  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bb466) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7fd341827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7fd3418278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x562c21de32c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x2288b9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7c03409dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c03409dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c03409dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c03409dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c03409dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7c03409e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7c03409e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c03409e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c03409e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c03409e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7c03409e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==243==ABORTING
````

</details>

### f_vector_resize_grow_ptr_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_vector_resize_grow_ptr_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.resize(c.size()+100);
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
    iterator "this" @ 0x7fff1f0d8190 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7fff1f0d8250
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
d45cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c5cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55f1a78dbf58  (/tmp/mi-linter-runtime-validation/runtime_asan+0x313f58) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55f1a78c223d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa23d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55f1a77f0e42  (/tmp/mi-linter-runtime-validation/runtime_asan+0x228e42) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55f1a78835e9  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bb5e9) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f78a8827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f78a88278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55f1a76682c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55f1a77cdfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55f1a78d4b37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55f1a78d427f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55f1a78d3097  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30b097) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55f1a78c1416  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f9416) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55f1a78c0dfc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2f8dfc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55f1a78681a2  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2a01a2) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55f1a78835dc  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bb5dc) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x7f78a8827780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #9 0x7f78a88278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x55f1a76682c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x228ea6) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7b98a79dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b98a79dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b98a79dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b98a79dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b98a79dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b98a79e0000: fa fa fd fa fa fa fd fa fa fa[fd]fd fa fa fa fa
  0x7b98a79e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b98a79e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b98a79e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b98a79e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b98a79e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

### f_vector_resize_grow_ptr_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `llamada` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_vector_resize_grow_ptr_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_vector_resize_grow(c);
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
93cfb  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30ccfb) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55dd641935cf  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c5cf) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55dd6419af58  (/tmp/mi-linter-runtime-validation/runtime_asan+0x313f58) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55dd6418123d  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa23d) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x55dd6408f6be  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2086be) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #7 0x55dd640b044c  (/tmp/mi-linter-runtime-validation/runtime_asan+0x22944c) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #8 0x55dd6414275f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bb75f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #9 0x7fa82b627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #10 0x7fa82b6278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #11 0x55dd63f272c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

previously allocated by thread T0 here:
    #0 0x55dd6408cfe1  (/tmp/mi-linter-runtime-validation/runtime_asan+0x205fe1) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #1 0x55dd64193b37  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30cb37) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #2 0x55dd6419327f  (/tmp/mi-linter-runtime-validation/runtime_asan+0x30c27f) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #3 0x55dd64181650  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2fa650) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #4 0x55dd64126f17  (/tmp/mi-linter-runtime-validation/runtime_asan+0x29ff17) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #5 0x55dd64142752  (/tmp/mi-linter-runtime-validation/runtime_asan+0x2bb752) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)
    #6 0x7fa82b627780  (/usr/lib/libc.so.6+0x27780) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #7 0x7fa82b6278b8  (/usr/lib/libc.so.6+0x278b8) (BuildId: d320029ad1a23be2f4bce117fd321cbd23a2014b)
    #8 0x55dd63f272c4  (/tmp/mi-linter-runtime-validation/runtime_asan+0xa02c4) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/mi-linter-runtime-validation/runtime_asan+0x2294b0) (BuildId: 1f3ed25c3f43f7562b7f5aa4a6b3d2b532436d53) 
Shadow bytes around the buggy address:
  0x7bd82a7dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd82a7dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd82a7dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd82a7dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bd82a7dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bd82a7e0000: fa fa 00 00 00 fa fa fa[fd]fd fd fd fa fa fa fa
  0x7bd82a7e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd82a7e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd82a7e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd82a7e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bd82a7e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
