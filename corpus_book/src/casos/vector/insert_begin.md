# `std::vector::insert_begin`

Mutación: `c.insert(c.begin(),1);`

- Iterador retenido: 🔴 `UB`
- Referencia/puntero retenido: 🔴 `UB`
- Casos `UB` detectados estáticamente: 0/12

**En palabras:** después de `c.insert(c.begin(),1);` sobre un `std::vector`, un iterador guardado queda **inválido**: usarlo después es un bug (UB); una referencia o puntero guardado queda **inválido**: usarlo después es un bug (UB).

Mapa de los 12 casos. Cada celda muestra la respuesta correcta (etiqueta) y, debajo, lo que hizo el analizador estático de Clang. Clic para ir al caso. Ver [Cómo leer este libro](../../guia.md).

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🔴 `UB`<br>❌ no detectado](#f_vector_insert_begin_it_recto) | [🔴 `UB`<br>❌ no detectado](#f_vector_insert_begin_it_guarda) | [🔴 `UB`<br>❌ no detectado](#f_vector_insert_begin_it_bucle) | [🔴 `UB`<br>❌ no detectado](#f_vector_insert_begin_it_llamada) |
| **referencia** | [🔴 `UB`<br>❌ no detectado](#f_vector_insert_begin_ref_recto) | [🔴 `UB`<br>❌ no detectado](#f_vector_insert_begin_ref_guarda) | [🔴 `UB`<br>❌ no detectado](#f_vector_insert_begin_ref_bucle) | [🔴 `UB`<br>❌ no detectado](#f_vector_insert_begin_ref_llamada) |
| **puntero** | [🔴 `UB`<br>❌ no detectado](#f_vector_insert_begin_ptr_recto) | [🔴 `UB`<br>❌ no detectado](#f_vector_insert_begin_ptr_guarda) | [🔴 `UB`<br>❌ no detectado](#f_vector_insert_begin_ptr_bucle) | [🔴 `UB`<br>❌ no detectado](#f_vector_insert_begin_ptr_llamada) |

## Handle: iterador

### f_vector_insert_begin_it_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_vector_insert_begin_it_recto(std::vector<int>& c) {
  auto it = c.begin();
  c.insert(c.begin(),1);
  sink(*it);
}
```

> **Causa del falso negativo:** 2. Sin comparacion previa contra end(), el modelado no se activa

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | 🛑 attempt to dereference a singular iterator | sin detección |

<details>
<summary>stderr libstdc++ Debug · <code>natural</code></summary>

````text
/usr/include/c++/13/debug/safe_iterator.h:298:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::reference 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator*() 
    const [with _Iterator = gnu_cxx::normal_iterator<int*, std::vector<int, 
    std::allocator<int> > >; _Sequence = std::debug::vector<int>; _Category 
    = std::forward_iterator_tag; reference = int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffc3cfa9b80 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffc3cfa9ca0
    }
````

</details>

### f_vector_insert_begin_it_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_vector_insert_begin_it_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.insert(c.begin(),1);
  sink(*it);
}
```

> **Causa del falso negativo:** 4. La invalidacion por insercion/realojamiento no esta modelada

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | 🛑 attempt to dereference a singular iterator | sin detección |

<details>
<summary>stderr libstdc++ Debug · <code>natural</code></summary>

````text
/usr/include/c++/13/debug/safe_iterator.h:298:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::reference 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator*() 
    const [with _Iterator = gnu_cxx::normal_iterator<int*, std::vector<int, 
    std::allocator<int> > >; _Sequence = std::debug::vector<int>; _Category 
    = std::forward_iterator_tag; reference = int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffd29e4ccf0 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffd29e4ce10
    }
````

</details>

### f_vector_insert_begin_it_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_vector_insert_begin_it_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.insert(c.begin(),1);
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
/usr/include/c++/13/debug/safe_iterator.h:298:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::reference 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator*() 
    const [with _Iterator = gnu_cxx::normal_iterator<int*, std::vector<int, 
    std::allocator<int> > >; _Sequence = std::debug::vector<int>; _Category 
    = std::forward_iterator_tag; reference = int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffcf5c30a30 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffcf5c30b50
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
ector<int, std::allocator<int>>&) /work/test/corpus.cpp:431:7
    #8 0x63c7a4fb2134 in main /work/test/runtime_runner.cpp:333:5
    #9 0x7932488c91c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x7932488c928a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x63c7a4e234b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x63c7a4f0cd31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x63c7a500cc77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x63c7a500c50f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x63c7a500c50f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x63c7a500b4b7 in void std::vector<int, std::allocator<int>>::_M_realloc_insert<int>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int>>>, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:459:33
    #5 0x63c7a4ff99f0 in int& std::vector<int, std::allocator<int>>::emplace_back<int>(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:123:4
    #6 0x63c7a4ff93bc in std::vector<int, std::allocator<int>>::push_back(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1299:9
    #7 0x63c7a4f9a41b in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:47:37
    #8 0x63c7a4fb2127 in main /work/test/runtime_runner.cpp:332:26
    #9 0x7932488c91c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x7932488c928a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x63c7a4e234b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:432:10 in f_vector_insert_begin_it_bucle(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x755247bdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x755247bdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x755247bdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x755247bdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x755247bdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x755247be0000: fa fa fd fa fa fa fd fa fa fa[fd]fd fa fa fa fa
  0x755247be0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x755247be0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x755247be0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x755247be0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x755247be0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==191==ABORTING
````

</details>

### f_vector_insert_begin_it_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_vector_insert_begin_it_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_vector_insert_begin(c);
  sink(*it);
}
```

> **Causa del falso negativo:** 4. La invalidacion por insercion/realojamiento no esta modelada

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | 🛑 attempt to dereference a singular iterator | sin detección |

<details>
<summary>stderr libstdc++ Debug · <code>natural</code></summary>

````text
/usr/include/c++/13/debug/safe_iterator.h:298:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::reference 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator*() 
    const [with _Iterator = gnu_cxx::normal_iterator<int*, std::vector<int, 
    std::allocator<int> > >; _Sequence = std::debug::vector<int>; _Category 
    = std::forward_iterator_tag; reference = int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffcb71ce960 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffcb71cea20
    }
````

</details>

## Handle: referencia

### f_vector_insert_begin_ref_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_vector_insert_begin_ref_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.insert(c.begin(),1);
  sink(h);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_vector_insert_begin_ref_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_vector_insert_begin_ref_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.insert(c.begin(),1);
  sink(h);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_vector_insert_begin_ref_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `bucle` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_vector_insert_begin_ref_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.insert(c.begin(),1);
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
/usr/include/c++/13/debug/safe_iterator.h:326:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>& 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator++() 
    [with _Iterator = gnu_cxx::normal_iterator<int*, std::vector<int, 
    std::allocator<int> > >; _Sequence = std::debug::vector<int>; _Category 
    = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffcb75ef410 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffcb75ef530
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
ctor<int, std::allocator<int>>&) /work/test/corpus.cpp:458:7
    #8 0x5ea8649ff70c in main /work/test/runtime_runner.cpp:353:5
    #9 0x742c305551c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x742c3055528a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x5ea8648704b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5ea864959d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5ea864a59c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5ea864a5950f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5ea864a5950f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x5ea864a584b7 in void std::vector<int, std::allocator<int>>::_M_realloc_insert<int>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int>>>, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:459:33
    #5 0x5ea864a469f0 in int& std::vector<int, std::allocator<int>>::emplace_back<int>(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:123:4
    #6 0x5ea864a463bc in std::vector<int, std::allocator<int>>::push_back(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1299:9
    #7 0x5ea8649e741b in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:47:37
    #8 0x5ea8649ff6ff in main /work/test/runtime_runner.cpp:352:26
    #9 0x742c305551c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x742c3055528a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x5ea8648704b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:459:10 in f_vector_insert_begin_ref_bucle(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x704c2f7dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x704c2f7dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x704c2f7dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x704c2f7dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x704c2f7dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x704c2f7e0000: fa fa fd fa fa fa fd fa fa fa[fd]fd fa fa fa fa
  0x704c2f7e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x704c2f7e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x704c2f7e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x704c2f7e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x704c2f7e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==200==ABORTING
````

</details>

### f_vector_insert_begin_ref_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_vector_insert_begin_ref_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_vector_insert_begin(c);
  sink(h);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

## Handle: puntero

### f_vector_insert_begin_ptr_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_vector_insert_begin_ptr_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.insert(c.begin(),1);
  sink(*h);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_vector_insert_begin_ptr_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_vector_insert_begin_ptr_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.insert(c.begin(),1);
  sink(*h);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_vector_insert_begin_ptr_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `bucle` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_vector_insert_begin_ptr_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.insert(c.begin(),1);
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
/usr/include/c++/13/debug/safe_iterator.h:326:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>& 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator++() 
    [with _Iterator = gnu_cxx::normal_iterator<int*, std::vector<int, 
    std::allocator<int> > >; _Sequence = std::debug::vector<int>; _Category 
    = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffe9fe36340 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffe9fe36460
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
ctor<int, std::allocator<int>>&) /work/test/corpus.cpp:486:7
    #8 0x5e8cc2a23ce4 in main /work/test/runtime_runner.cpp:373:5
    #9 0x79047b9e51c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x79047b9e528a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x5e8cc28944b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5e8cc297dd31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5e8cc2a7dc77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5e8cc2a7d50f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5e8cc2a7d50f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x5e8cc2a7c4b7 in void std::vector<int, std::allocator<int>>::_M_realloc_insert<int>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int>>>, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:459:33
    #5 0x5e8cc2a6a9f0 in int& std::vector<int, std::allocator<int>>::emplace_back<int>(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:123:4
    #6 0x5e8cc2a6a3bc in std::vector<int, std::allocator<int>>::push_back(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1299:9
    #7 0x5e8cc2a0b41b in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:47:37
    #8 0x5e8cc2a23cd7 in main /work/test/runtime_runner.cpp:372:26
    #9 0x79047b9e51c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x79047b9e528a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x5e8cc28944b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:487:10 in f_vector_insert_begin_ptr_bucle(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x75247addfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75247addfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75247addfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75247addff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75247addff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x75247ade0000: fa fa fd fa fa fa fd fa fa fa[fd]fd fa fa fa fa
  0x75247ade0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x75247ade0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x75247ade0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x75247ade0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x75247ade0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==209==ABORTING
````

</details>

### f_vector_insert_begin_ptr_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_vector_insert_begin_ptr_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_vector_insert_begin(c);
  sink(*h);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |
