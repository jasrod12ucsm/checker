# `std::forward_list::erase_after`

Mutación: `c.erase_after(c.before_begin());`

- Iterador retenido: 🔴 `UB`
- Referencia/puntero retenido: 🔴 `UB`
- Casos `UB` detectados estáticamente: 0/12

**En palabras:** después de `c.erase_after(c.before_begin());` sobre un `std::forward_list`, un iterador guardado queda **inválido**: usarlo después es un bug (UB); una referencia o puntero guardado queda **inválido**: usarlo después es un bug (UB).

Mapa de los 12 casos. Cada celda muestra la respuesta correcta (etiqueta) y, debajo, lo que hizo el analizador estático de Clang. Clic para ir al caso. Ver [Cómo leer este libro](../../guia.md).

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🔴 `UB`<br>❌ no detectado](#f_flist_erase_after_it_recto) | [🔴 `UB`<br>❌ no detectado](#f_flist_erase_after_it_guarda) | [🔴 `UB`<br>❌ no detectado](#f_flist_erase_after_it_bucle) | [🔴 `UB`<br>❌ no detectado](#f_flist_erase_after_it_llamada) |
| **referencia** | [🔴 `UB`<br>❌ no detectado](#f_flist_erase_after_ref_recto) | [🔴 `UB`<br>❌ no detectado](#f_flist_erase_after_ref_guarda) | [🔴 `UB`<br>❌ no detectado](#f_flist_erase_after_ref_bucle) | [🔴 `UB`<br>❌ no detectado](#f_flist_erase_after_ref_llamada) |
| **puntero** | [🔴 `UB`<br>❌ no detectado](#f_flist_erase_after_ptr_recto) | [🔴 `UB`<br>❌ no detectado](#f_flist_erase_after_ptr_guarda) | [🔴 `UB`<br>❌ no detectado](#f_flist_erase_after_ptr_bucle) | [🔴 `UB`<br>❌ no detectado](#f_flist_erase_after_ptr_llamada) |

## Handle: iterador

### f_flist_erase_after_it_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_flist_erase_after_it_recto(std::forward_list<int>& c) {
  auto it = c.begin();
  c.erase_after(c.before_begin());
  sink(*it);
}
```

> **Causa del falso negativo:** 2. Sin comparacion previa contra end(), el modelado no se activa

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
    const [with _Iterator = std::_Fwd_list_iterator<int>; _Sequence = std::
    debug::forward_list<int>; _Category = std::forward_iterator_tag; 
    reference = int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffd7994cfc0 {
      type = std::_Fwd_list_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::forward_list<int, std::allocator<int> >' @ 0x7ffd7994d0e0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
    #8 0x7c8f4a4651c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x7c8f4a46528a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x59e748c3c4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x59e748d25d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x59e748e41a67 in std::__new_allocator<std::_Fwd_list_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x59e748e417df in std::allocator_traits<std::allocator<std::_Fwd_list_node<int>>>::allocate(std::allocator<std::_Fwd_list_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x59e748e417df in std::_Fwd_list_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:360:15
    #4 0x59e748e61feb in std::_Fwd_list_node<int>* std::_Fwd_list_base<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:368:26
    #5 0x59e748e61be2 in void std::forward_list<int, std::allocator<int>>::_M_range_initialize<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.tcc:105:28
    #6 0x59e748e1e4f1 in std::forward_list<int, std::allocator<int>>::forward_list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:597:9
    #7 0x59e748db3f60 in make_flist(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:53:68
    #8 0x59e748de9822 in main /work/test/runtime_runner.cpp:2062:32
    #9 0x7c8f4a4651c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x7c8f4a46528a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x59e748c3c4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2752:8 in f_flist_erase_after_it_recto(std::forward_list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x78af497dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x78af497dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x78af497dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x78af497dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x78af497dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x78af497e0000: fa fa fd[fd]fa fa 00 00 fa fa 00 00 fa fa fa fa
  0x78af497e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x78af497e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x78af497e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x78af497e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x78af497e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1093==ABORTING
````

</details>

### f_flist_erase_after_it_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_flist_erase_after_it_guarda(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.erase_after(c.before_begin());
  sink(*it);
}
```

> **Causa del falso negativo:** 3. Se invalida por identidad del iterador, no por posicion

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
    const [with _Iterator = std::_Fwd_list_iterator<int>; _Sequence = std::
    debug::forward_list<int>; _Category = std::forward_iterator_tag; 
    reference = int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffc98c72f80 {
      type = std::_Fwd_list_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::forward_list<int, std::allocator<int> >' @ 0x7ffc98c730a0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
   #8 0x720f589b21c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x720f589b228a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x5bc706a5a4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5bc706b43d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5bc706c5fa67 in std::__new_allocator<std::_Fwd_list_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5bc706c5f7df in std::allocator_traits<std::allocator<std::_Fwd_list_node<int>>>::allocate(std::allocator<std::_Fwd_list_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5bc706c5f7df in std::_Fwd_list_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:360:15
    #4 0x5bc706c7ffeb in std::_Fwd_list_node<int>* std::_Fwd_list_base<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:368:26
    #5 0x5bc706c7fbe2 in void std::forward_list<int, std::allocator<int>>::_M_range_initialize<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.tcc:105:28
    #6 0x5bc706c3c4f1 in std::forward_list<int, std::allocator<int>>::forward_list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:597:9
    #7 0x5bc706bd1f60 in make_flist(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:53:68
    #8 0x5bc706c0797d in main /work/test/runtime_runner.cpp:2067:32
    #9 0x720f589b21c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x720f589b228a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x5bc706a5a4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2758:8 in f_flist_erase_after_it_guarda(std::forward_list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6e2f57bdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e2f57bdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e2f57bdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e2f57bdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6e2f57bdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6e2f57be0000: fa fa fd[fd]fa fa 00 00 fa fa 00 00 fa fa fa fa
  0x6e2f57be0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e2f57be0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e2f57be0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e2f57be0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e2f57be0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1096==ABORTING
````

</details>

### f_flist_erase_after_it_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_flist_erase_after_it_bucle(std::forward_list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.erase_after(c.before_begin());
    sink(*it);
  }
}
```

> **Causa del falso negativo:** 3. Se invalida por identidad del iterador, no por posicion

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
    const [with _Iterator = std::_Fwd_list_iterator<int>; _Sequence = std::
    debug::forward_list<int>; _Category = std::forward_iterator_tag; 
    reference = int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffe7a3309c0 {
      type = std::_Fwd_list_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::forward_list<int, std::allocator<int> >' @ 0x7ffe7a330ae0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
   #8 0x7ad8619a21c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x7ad8619a228a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x64b55c55b4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x64b55c644d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x64b55c760a67 in std::__new_allocator<std::_Fwd_list_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x64b55c7607df in std::allocator_traits<std::allocator<std::_Fwd_list_node<int>>>::allocate(std::allocator<std::_Fwd_list_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x64b55c7607df in std::_Fwd_list_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:360:15
    #4 0x64b55c780feb in std::_Fwd_list_node<int>* std::_Fwd_list_base<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:368:26
    #5 0x64b55c780be2 in void std::forward_list<int, std::allocator<int>>::_M_range_initialize<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.tcc:105:28
    #6 0x64b55c73d4f1 in std::forward_list<int, std::allocator<int>>::forward_list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:597:9
    #7 0x64b55c6d2f60 in make_flist(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:53:68
    #8 0x64b55c708ad8 in main /work/test/runtime_runner.cpp:2072:32
    #9 0x7ad8619a21c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x7ad8619a228a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x64b55c55b4b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2764:10 in f_flist_erase_after_it_bucle(std::forward_list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x76f860bdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x76f860bdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x76f860bdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x76f860bdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x76f860bdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x76f860be0000: fa fa fd[fd]fa fa 00 00 fa fa 00 00 fa fa fa fa
  0x76f860be0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x76f860be0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x76f860be0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x76f860be0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x76f860be0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1099==ABORTING
````

</details>

### f_flist_erase_after_it_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_flist_erase_after_it_llamada(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_flist_erase_after(c);
  sink(*it);
}
```

> **Causa del falso negativo:** 3. Se invalida por identidad del iterador, no por posicion

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
    const [with _Iterator = std::_Fwd_list_iterator<int>; _Sequence = std::
    debug::forward_list<int>; _Category = std::forward_iterator_tag; 
    reference = int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fff209fc260 {
      type = std::_Fwd_list_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::forward_list<int, std::allocator<int> >' @ 0x7fff209fc320
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
 #9 0x79bacdc791c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x79bacdc7928a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x5cefa8b664b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5cefa8c4fd31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5cefa8d6ba67 in std::__new_allocator<std::_Fwd_list_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5cefa8d6b7df in std::allocator_traits<std::allocator<std::_Fwd_list_node<int>>>::allocate(std::allocator<std::_Fwd_list_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5cefa8d6b7df in std::_Fwd_list_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:360:15
    #4 0x5cefa8d8bfeb in std::_Fwd_list_node<int>* std::_Fwd_list_base<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:368:26
    #5 0x5cefa8d8bbe2 in void std::forward_list<int, std::allocator<int>>::_M_range_initialize<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.tcc:105:28
    #6 0x5cefa8d484f1 in std::forward_list<int, std::allocator<int>>::forward_list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:597:9
    #7 0x5cefa8cddf60 in make_flist(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:53:68
    #8 0x5cefa8d13c33 in main /work/test/runtime_runner.cpp:2077:32
    #9 0x79bacdc791c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x79bacdc7928a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x5cefa8b664b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2771:8 in f_flist_erase_after_it_llamada(std::forward_list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x75daccfdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75daccfdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75daccfdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75daccfdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x75daccfdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x75daccfe0000: fa fa fd[fd]fa fa 00 00 fa fa 00 00 fa fa fa fa
  0x75daccfe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x75daccfe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x75daccfe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x75daccfe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x75daccfe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1102==ABORTING
````

</details>

## Handle: referencia

### f_flist_erase_after_ref_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_flist_erase_after_ref_recto(std::forward_list<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.erase_after(c.before_begin());
  sink(h);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | 🛑 heap-use-after-free |

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
   #8 0x7f9faadb01c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x7f9faadb028a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x5940699604b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x594069a49d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x594069b65a67 in std::__new_allocator<std::_Fwd_list_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x594069b657df in std::allocator_traits<std::allocator<std::_Fwd_list_node<int>>>::allocate(std::allocator<std::_Fwd_list_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x594069b657df in std::_Fwd_list_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:360:15
    #4 0x594069b85feb in std::_Fwd_list_node<int>* std::_Fwd_list_base<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:368:26
    #5 0x594069b85be2 in void std::forward_list<int, std::allocator<int>>::_M_range_initialize<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.tcc:105:28
    #6 0x594069b424f1 in std::forward_list<int, std::allocator<int>>::forward_list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:597:9
    #7 0x594069ad7f60 in make_flist(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:53:68
    #8 0x594069b0dd8e in main /work/test/runtime_runner.cpp:2082:32
    #9 0x7f9faadb01c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x7f9faadb028a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x5940699604b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2777:8 in f_flist_erase_after_ref_recto(std::forward_list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7bbfa9fdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bbfa9fdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bbfa9fdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bbfa9fdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bbfa9fdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bbfa9fe0000: fa fa fd[fd]fa fa 00 00 fa fa 00 00 fa fa fa fa
  0x7bbfa9fe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bbfa9fe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bbfa9fe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bbfa9fe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bbfa9fe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1105==ABORTING
````

</details>

### f_flist_erase_after_ref_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_flist_erase_after_ref_guarda(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.erase_after(c.before_begin());
  sink(h);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | 🛑 heap-use-after-free |

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
  #8 0x7f37562c41c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x7f37562c428a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x62d1412174b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x62d141300d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x62d14141ca67 in std::__new_allocator<std::_Fwd_list_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x62d14141c7df in std::allocator_traits<std::allocator<std::_Fwd_list_node<int>>>::allocate(std::allocator<std::_Fwd_list_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x62d14141c7df in std::_Fwd_list_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:360:15
    #4 0x62d14143cfeb in std::_Fwd_list_node<int>* std::_Fwd_list_base<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:368:26
    #5 0x62d14143cbe2 in void std::forward_list<int, std::allocator<int>>::_M_range_initialize<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.tcc:105:28
    #6 0x62d1413f94f1 in std::forward_list<int, std::allocator<int>>::forward_list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:597:9
    #7 0x62d14138ef60 in make_flist(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:53:68
    #8 0x62d1413c4ee9 in main /work/test/runtime_runner.cpp:2087:32
    #9 0x7f37562c41c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x7f37562c428a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x62d1412174b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2784:8 in f_flist_erase_after_ref_guarda(std::forward_list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7b57555dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b57555dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b57555dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b57555dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b57555dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b57555e0000: fa fa fd[fd]fa fa 00 00 fa fa 00 00 fa fa fa fa
  0x7b57555e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b57555e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b57555e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b57555e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b57555e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1108==ABORTING
````

</details>

### f_flist_erase_after_ref_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `bucle` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_flist_erase_after_ref_bucle(std::forward_list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.erase_after(c.before_begin());
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
    [with _Iterator = std::_Fwd_list_iterator<int>; _Sequence = std::
    debug::forward_list<int>; _Category = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffc3fa63060 {
      type = std::_Fwd_list_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::forward_list<int, std::allocator<int> >' @ 0x7ffc3fa63180
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
  #8 0x75141b4201c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x75141b42028a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x57a4c4c154b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x57a4c4cfed31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x57a4c4e1aa67 in std::__new_allocator<std::_Fwd_list_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x57a4c4e1a7df in std::allocator_traits<std::allocator<std::_Fwd_list_node<int>>>::allocate(std::allocator<std::_Fwd_list_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x57a4c4e1a7df in std::_Fwd_list_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:360:15
    #4 0x57a4c4e3afeb in std::_Fwd_list_node<int>* std::_Fwd_list_base<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:368:26
    #5 0x57a4c4e3abe2 in void std::forward_list<int, std::allocator<int>>::_M_range_initialize<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.tcc:105:28
    #6 0x57a4c4df74f1 in std::forward_list<int, std::allocator<int>>::forward_list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:597:9
    #7 0x57a4c4d8cf60 in make_flist(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:53:68
    #8 0x57a4c4dc3044 in main /work/test/runtime_runner.cpp:2092:32
    #9 0x75141b4201c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x75141b42028a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x57a4c4c154b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2791:10 in f_flist_erase_after_ref_bucle(std::forward_list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x71341a7dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x71341a7dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x71341a7dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x71341a7dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x71341a7dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x71341a7e0000: fa fa fd[fd]fa fa 00 00 fa fa 00 00 fa fa fa fa
  0x71341a7e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x71341a7e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x71341a7e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x71341a7e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x71341a7e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1111==ABORTING
````

</details>

### f_flist_erase_after_ref_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_flist_erase_after_ref_llamada(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_flist_erase_after(c);
  sink(h);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | 🛑 heap-use-after-free |

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
#9 0x7318840911c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x73188409128a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x619a93a144b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x619a93afdd31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x619a93c19a67 in std::__new_allocator<std::_Fwd_list_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x619a93c197df in std::allocator_traits<std::allocator<std::_Fwd_list_node<int>>>::allocate(std::allocator<std::_Fwd_list_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x619a93c197df in std::_Fwd_list_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:360:15
    #4 0x619a93c39feb in std::_Fwd_list_node<int>* std::_Fwd_list_base<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:368:26
    #5 0x619a93c39be2 in void std::forward_list<int, std::allocator<int>>::_M_range_initialize<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.tcc:105:28
    #6 0x619a93bf64f1 in std::forward_list<int, std::allocator<int>>::forward_list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:597:9
    #7 0x619a93b8bf60 in make_flist(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:53:68
    #8 0x619a93bc219f in main /work/test/runtime_runner.cpp:2097:32
    #9 0x7318840911c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x73188409128a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x619a93a144b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2799:8 in f_flist_erase_after_ref_llamada(std::forward_list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x6f38833dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f38833dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f38833dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f38833dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6f38833dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x6f38833e0000: fa fa fd[fd]fa fa 00 00 fa fa 00 00 fa fa fa fa
  0x6f38833e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f38833e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f38833e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f38833e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6f38833e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1114==ABORTING
````

</details>

## Handle: puntero

### f_flist_erase_after_ptr_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_flist_erase_after_ptr_recto(std::forward_list<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.erase_after(c.before_begin());
  sink(*h);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | 🛑 heap-use-after-free |

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
   #8 0x76d7342961c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x76d73429628a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x60be9aba14b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x60be9ac8ad31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x60be9ada6a67 in std::__new_allocator<std::_Fwd_list_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x60be9ada67df in std::allocator_traits<std::allocator<std::_Fwd_list_node<int>>>::allocate(std::allocator<std::_Fwd_list_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x60be9ada67df in std::_Fwd_list_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:360:15
    #4 0x60be9adc6feb in std::_Fwd_list_node<int>* std::_Fwd_list_base<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:368:26
    #5 0x60be9adc6be2 in void std::forward_list<int, std::allocator<int>>::_M_range_initialize<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.tcc:105:28
    #6 0x60be9ad834f1 in std::forward_list<int, std::allocator<int>>::forward_list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:597:9
    #7 0x60be9ad18f60 in make_flist(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:53:68
    #8 0x60be9ad4f2fa in main /work/test/runtime_runner.cpp:2102:32
    #9 0x76d7342961c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x76d73429628a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x60be9aba14b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2805:8 in f_flist_erase_after_ptr_recto(std::forward_list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x72f7335dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x72f7335dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x72f7335dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x72f7335dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x72f7335dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x72f7335e0000: fa fa fd[fd]fa fa 00 00 fa fa 00 00 fa fa fa fa
  0x72f7335e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x72f7335e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x72f7335e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x72f7335e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x72f7335e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1117==ABORTING
````

</details>

### f_flist_erase_after_ptr_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_flist_erase_after_ptr_guarda(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.erase_after(c.before_begin());
  sink(*h);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | 🛑 heap-use-after-free |

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
  #8 0x7f1aa0fd01c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x7f1aa0fd028a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x5e6da85644b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x5e6da864dd31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x5e6da8769a67 in std::__new_allocator<std::_Fwd_list_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x5e6da87697df in std::allocator_traits<std::allocator<std::_Fwd_list_node<int>>>::allocate(std::allocator<std::_Fwd_list_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x5e6da87697df in std::_Fwd_list_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:360:15
    #4 0x5e6da8789feb in std::_Fwd_list_node<int>* std::_Fwd_list_base<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:368:26
    #5 0x5e6da8789be2 in void std::forward_list<int, std::allocator<int>>::_M_range_initialize<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.tcc:105:28
    #6 0x5e6da87464f1 in std::forward_list<int, std::allocator<int>>::forward_list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:597:9
    #7 0x5e6da86dbf60 in make_flist(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:53:68
    #8 0x5e6da8712455 in main /work/test/runtime_runner.cpp:2107:32
    #9 0x7f1aa0fd01c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x7f1aa0fd028a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x5e6da85644b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2812:8 in f_flist_erase_after_ptr_guarda(std::forward_list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7b3aa03dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b3aa03dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b3aa03dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b3aa03dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b3aa03dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b3aa03e0000: fa fa fd[fd]fa fa 00 00 fa fa 00 00 fa fa fa fa
  0x7b3aa03e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b3aa03e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b3aa03e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b3aa03e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b3aa03e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1120==ABORTING
````

</details>

### f_flist_erase_after_ptr_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `bucle` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_flist_erase_after_ptr_bucle(std::forward_list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.erase_after(c.before_begin());
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
    [with _Iterator = std::_Fwd_list_iterator<int>; _Sequence = std::
    debug::forward_list<int>; _Category = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffedd3231c0 {
      type = std::_Fwd_list_iterator<int> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::forward_list<int, std::allocator<int> >' @ 0x7ffedd3232e0
    }
````

</details>

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
  #8 0x7eb0eed8a1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #9 0x7eb0eed8a28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x597449ce94b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x597449dd2d31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x597449eeea67 in std::__new_allocator<std::_Fwd_list_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x597449eee7df in std::allocator_traits<std::allocator<std::_Fwd_list_node<int>>>::allocate(std::allocator<std::_Fwd_list_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x597449eee7df in std::_Fwd_list_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:360:15
    #4 0x597449f0efeb in std::_Fwd_list_node<int>* std::_Fwd_list_base<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:368:26
    #5 0x597449f0ebe2 in void std::forward_list<int, std::allocator<int>>::_M_range_initialize<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.tcc:105:28
    #6 0x597449ecb4f1 in std::forward_list<int, std::allocator<int>>::forward_list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:597:9
    #7 0x597449e60f60 in make_flist(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:53:68
    #8 0x597449e975b0 in main /work/test/runtime_runner.cpp:2112:32
    #9 0x7eb0eed8a1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x7eb0eed8a28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x597449ce94b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2819:10 in f_flist_erase_after_ptr_bucle(std::forward_list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7ad0edfdfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ad0edfdfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ad0edfdfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ad0edfdff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ad0edfdff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7ad0edfe0000: fa fa fd[fd]fa fa 00 00 fa fa 00 00 fa fa fa fa
  0x7ad0edfe0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ad0edfe0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ad0edfe0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ad0edfe0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7ad0edfe0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1123==ABORTING
````

</details>

### f_flist_erase_after_ptr_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_flist_erase_after_ptr_llamada(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_flist_erase_after(c);
  sink(*h);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | 🛑 heap-use-after-free |

<details>
<summary>stderr ASan/UBSan · <code>natural</code></summary>

````text
#9 0x7f08b67aa1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x7f08b67aa28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x567d4b7d34b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

previously allocated by thread T0 here:
    #0 0x567d4b8bcd31 in operator new(unsigned long) (/work/build/runtime/runtime_asan+0x18fd31) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)
    #1 0x567d4b9d8a67 in std::__new_allocator<std::_Fwd_list_node<int>>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/new_allocator.h:151:27
    #2 0x567d4b9d87df in std::allocator_traits<std::allocator<std::_Fwd_list_node<int>>>::allocate(std::allocator<std::_Fwd_list_node<int>>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/alloc_traits.h:482:20
    #3 0x567d4b9d87df in std::_Fwd_list_base<int, std::allocator<int>>::_M_get_node() /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:360:15
    #4 0x567d4b9f8feb in std::_Fwd_list_node<int>* std::_Fwd_list_base<int, std::allocator<int>>::_M_create_node<int const&>(int const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:368:26
    #5 0x567d4b9f8be2 in void std::forward_list<int, std::allocator<int>>::_M_range_initialize<int const*>(int const*, int const*) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.tcc:105:28
    #6 0x567d4b9b54f1 in std::forward_list<int, std::allocator<int>>::forward_list(std::initializer_list<int>, std::allocator<int> const&) /usr/lib/gcc/x86_64-linux-gnu/13/../../../../include/c++/13/bits/forward_list.h:597:9
    #7 0x567d4b94af60 in make_flist(Mode, std::basic_string_view<char, std::char_traits<char>>) /work/test/runtime_runner.cpp:53:68
    #8 0x567d4b98170b in main /work/test/runtime_runner.cpp:2117:32
    #9 0x7f08b67aa1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #10 0x7f08b67aa28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: a4a7992a8e66555c8141ab2a08a8465ff6e0ea65)
    #11 0x567d4b7d34b4 in _start (/work/build/runtime/runtime_asan+0xa64b4) (BuildId: 83eaeac8831fc63ea553834d30adc07a420d58fd)

SUMMARY: AddressSanitizer: heap-use-after-free /work/test/corpus.cpp:2827:8 in f_flist_erase_after_ptr_llamada(std::forward_list<int, std::allocator<int>>&)
Shadow bytes around the buggy address:
  0x7b28b59dfd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b28b59dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b28b59dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b28b59dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b28b59dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b28b59e0000: fa fa fd[fd]fa fa 00 00 fa fa 00 00 fa fa fa fa
  0x7b28b59e0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b28b59e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b28b59e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b28b59e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b28b59e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1126==ABORTING
````

</details>
