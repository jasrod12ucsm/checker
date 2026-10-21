# `std::vector::pop_back`

Mutación: `c.pop_back();`

- Iterador retenido: 🟡 `POLICY`
- Referencia/puntero retenido: 🟡 `POLICY`
- Casos `UB` detectados estáticamente: 0/0

**En palabras:** después de `c.pop_back();` sobre un `std::vector`, un iterador guardado **puede** quedar inválido según el estado del contenedor (capacidad o factor de carga); una referencia o puntero guardado **puede** quedar inválido según el estado del contenedor (capacidad o factor de carga).

Mapa de los 12 casos. Cada celda muestra la respuesta correcta (etiqueta) y, debajo, lo que hizo el analizador estático de Clang. Clic para ir al caso. Ver [Cómo leer este libro](../../guia.md).

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_pop_back_it_recto) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_pop_back_it_guarda) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_pop_back_it_bucle) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_pop_back_it_llamada) |
| **referencia** | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_pop_back_ref_recto) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_pop_back_ref_guarda) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_pop_back_ref_bucle) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_pop_back_ref_llamada) |
| **puntero** | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_pop_back_ptr_recto) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_pop_back_ptr_guarda) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_pop_back_ptr_bucle) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_vector_pop_back_ptr_llamada) |

## Handle: iterador

### f_vector_pop_back_it_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_pop_back_it_recto(std::vector<int>& c) {
  auto it = c.begin();
  c.pop_back();
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | 🛑 attempt to dereference a singular iterator | sin detección |
| `preserve` | 8 elementos: tres rondas de pop_back no alcanzan al iterador | sin detección | sin detección |

<details>
<summary>stderr libstdc++ Debug · <code>force</code></summary>

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
    iterator "this" @ 0x7ffe02062100 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffe02062180
    }
````

</details>

### f_vector_pop_back_it_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_pop_back_it_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.pop_back();
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | 🛑 attempt to dereference a singular iterator | sin detección |
| `preserve` | 8 elementos: tres rondas de pop_back no alcanzan al iterador | sin detección | sin detección |

<details>
<summary>stderr libstdc++ Debug · <code>force</code></summary>

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
    iterator "this" @ 0x7ffe933f7980 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffe933f7a40
    }
````

</details>

### f_vector_pop_back_it_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_pop_back_it_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.pop_back();
    sink(*it);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | 🛑 attempt to dereference a singular iterator | 🛑 heap-buffer-overflow |
| `preserve` | 8 elementos: tres rondas de pop_back no alcanzan al iterador | sin detección | sin detección |

<details>
<summary>stderr libstdc++ Debug · <code>force</code></summary>

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
    iterator "this" @ 0x7ffd3178f5d0 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffd3178f690
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
6038375d6b7c in main /work/test/runtime_runner.cpp:873:5
    #2 0x771822b001c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #3 0x771822b0028a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #4 0x60383743e4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

0x733821de0014 is located 0 bytes after 4-byte region [0x733821de0010,0x733821de0014)
allocated by thread T0 here:
    #0 0x603837527d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x603837627c77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x60383762750f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x60383762750f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x6038376264b7 in void std::vector<int, std::allocator<int>>::_M_realloc_insert<int>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int>>>, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:459:33
    #5 0x6038376149f0 in int& std::vector<int, std::allocator<int>>::emplace_back<int>(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:123:4
    #6 0x6038376143bc in std::vector<int, std::allocator<int>>::push_back(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1299:9
    #7 0x6038375b4d04 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:23:64
    #8 0x6038375d6b6f in main /work/test/runtime_runner.cpp:872:26
    #9 0x771822b001c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x771822b0028a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x60383743e4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-buffer-overflow /work/test/corpus.cpp:1164:10 in f_vector_pop_back_it_bucle(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x733821ddfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x733821ddfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x733821ddfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x733821ddff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x733821ddff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x733821de0000: fa fa[04]fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x733821de0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x733821de0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x733821de0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x733821de0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x733821de0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==558==ABORTING
````

</details>

### f_vector_pop_back_it_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_pop_back_it_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_vector_pop_back(c);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | 🛑 attempt to dereference a singular iterator | sin detección |
| `preserve` | 8 elementos: tres rondas de pop_back no alcanzan al iterador | sin detección | sin detección |

<details>
<summary>stderr libstdc++ Debug · <code>force</code></summary>

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
    iterator "this" @ 0x7ffc8fdc1ec0 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffc8fdc1f80
    }
````

</details>

## Handle: referencia

### f_vector_pop_back_ref_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_pop_back_ref_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.pop_back();
  sink(h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | sin detección | sin detección |
| `preserve` | 8 elementos: tres rondas de pop_back no alcanzan al iterador | sin detección | sin detección |

### f_vector_pop_back_ref_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_pop_back_ref_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.pop_back();
  sink(h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | sin detección | sin detección |
| `preserve` | 8 elementos: tres rondas de pop_back no alcanzan al iterador | sin detección | sin detección |

### f_vector_pop_back_ref_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_pop_back_ref_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.pop_back();
    sink(h);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | 🛑 attempt to increment a singular iterator | 🛑 heap-buffer-overflow |
| `preserve` | 8 elementos: tres rondas de pop_back no alcanzan al iterador | sin detección | sin detección |

<details>
<summary>stderr libstdc++ Debug · <code>force</code></summary>

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
    iterator "this" @ 0x7ffda362b090 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffda362b150
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
818e02aa054 in main /work/test/runtime_runner.cpp:893:5
    #2 0x7b49209861c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #3 0x7b492098628a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #4 0x5818e01114b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

0x77691fbe0014 is located 0 bytes after 4-byte region [0x77691fbe0010,0x77691fbe0014)
allocated by thread T0 here:
    #0 0x5818e01fad31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5818e02fac77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5818e02fa50f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5818e02fa50f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x5818e02f94b7 in void std::vector<int, std::allocator<int>>::_M_realloc_insert<int>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int>>>, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:459:33
    #5 0x5818e02e79f0 in int& std::vector<int, std::allocator<int>>::emplace_back<int>(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:123:4
    #6 0x5818e02e73bc in std::vector<int, std::allocator<int>>::push_back(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1299:9
    #7 0x5818e0287d04 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:23:64
    #8 0x5818e02aa047 in main /work/test/runtime_runner.cpp:892:26
    #9 0x7b49209861c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x7b492098628a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x5818e01114b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-buffer-overflow /work/test/corpus.cpp:1191:10 in f_vector_pop_back_ref_bucle(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x77691fbdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x77691fbdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x77691fbdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x77691fbdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x77691fbdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x77691fbe0000: fa fa[04]fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x77691fbe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x77691fbe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x77691fbe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x77691fbe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x77691fbe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==575==ABORTING
````

</details>

### f_vector_pop_back_ref_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_pop_back_ref_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_vector_pop_back(c);
  sink(h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | sin detección | sin detección |
| `preserve` | 8 elementos: tres rondas de pop_back no alcanzan al iterador | sin detección | sin detección |

## Handle: puntero

### f_vector_pop_back_ptr_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_pop_back_ptr_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.pop_back();
  sink(*h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | sin detección | sin detección |
| `preserve` | 8 elementos: tres rondas de pop_back no alcanzan al iterador | sin detección | sin detección |

### f_vector_pop_back_ptr_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_pop_back_ptr_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.pop_back();
  sink(*h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | sin detección | sin detección |
| `preserve` | 8 elementos: tres rondas de pop_back no alcanzan al iterador | sin detección | sin detección |

### f_vector_pop_back_ptr_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_pop_back_ptr_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.pop_back();
    sink(*h);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | 🛑 attempt to increment a singular iterator | 🛑 heap-buffer-overflow |
| `preserve` | 8 elementos: tres rondas de pop_back no alcanzan al iterador | sin detección | sin detección |

<details>
<summary>stderr libstdc++ Debug · <code>force</code></summary>

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
    iterator "this" @ 0x7ffedefe8e70 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffedefe8f30
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>force</code></summary>

````text
00fdd52e52c in main /work/test/runtime_runner.cpp:913:5
    #2 0x7125795ea1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #3 0x7125795ea28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #4 0x600fdd3954b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

0x6d45789e0014 is located 0 bytes after 4-byte region [0x6d45789e0010,0x6d45789e0014)
allocated by thread T0 here:
    #0 0x600fdd47ed31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x600fdd57ec77 in std::__new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x600fdd57e50f in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x600fdd57e50f in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:381:20
    #4 0x600fdd57d4b7 in void std::vector<int, std::allocator<int>>::_M_realloc_insert<int>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int>>>, int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:459:33
    #5 0x600fdd56b9f0 in int& std::vector<int, std::allocator<int>>::emplace_back<int>(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/vector.tcc:123:4
    #6 0x600fdd56b3bc in std::vector<int, std::allocator<int>>::push_back(int&&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/stl_vector.h:1299:9
    #7 0x600fdd50bd04 in make_vector(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:23:64
    #8 0x600fdd52e51f in main /work/test/runtime_runner.cpp:912:26
    #9 0x7125795ea1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x7125795ea28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x600fdd3954b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-buffer-overflow /work/test/corpus.cpp:1219:10 in f_vector_pop_back_ptr_bucle(std::vector<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6d45789dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d45789dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d45789dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d45789dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6d45789dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6d45789e0000: fa fa[04]fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d45789e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d45789e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d45789e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d45789e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6d45789e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==592==ABORTING
````

</details>

### f_vector_pop_back_ptr_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_vector_pop_back_ptr_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_vector_pop_back(c);
  sink(*h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | capacidad agotada antes de la mutación | sin detección | sin detección |
| `preserve` | 8 elementos: tres rondas de pop_back no alcanzan al iterador | sin detección | sin detección |
