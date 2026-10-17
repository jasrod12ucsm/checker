# `std::vector::assign`

Mutación: `c.assign(3,7);`

- Iterador retenido: 🔴 `UB`
- Referencia/puntero retenido: 🔴 `UB`
- Casos `UB` detectados estáticamente: 4/12

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🔴 avisa](#f_vector_assign_it_recto) | [🔴 avisa](#f_vector_assign_it_guarda) | [🔴 avisa](#f_vector_assign_it_bucle) | [🔴 avisa](#f_vector_assign_it_llamada) |
| **referencia** | [🔴 calla](#f_vector_assign_ref_recto) | [🔴 calla](#f_vector_assign_ref_guarda) | [🔴 calla](#f_vector_assign_ref_bucle) | [🔴 calla](#f_vector_assign_ref_llamada) |
| **puntero** | [🔴 calla](#f_vector_assign_ptr_recto) | [🔴 calla](#f_vector_assign_ptr_guarda) | [🔴 calla](#f_vector_assign_ptr_bucle) | [🔴 calla](#f_vector_assign_ptr_llamada) |

## Handle: iterador

### f_vector_assign_it_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `recto` | 🔴 `UB` | ✅ detectado |

```cpp
void f_vector_assign_it_recto(std::vector<int>& c) {
  auto it = c.begin();
  c.assign(3,7);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | 🛑 attempt to dereference a singular iterator | — (código 0) |

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
    iterator "this" @ 0x7fffb5335940 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7fffb53359d0
    }
````

</details>

### f_vector_assign_it_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `guarda` | 🔴 `UB` | ✅ detectado |

```cpp
void f_vector_assign_it_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.assign(3,7);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | 🛑 attempt to dereference a singular iterator | — (código 0) |

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
    iterator "this" @ 0x7ffd495979b0 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffd49597a70
    }
````

</details>

### f_vector_assign_it_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ✅ detectado |

```cpp
void f_vector_assign_it_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.assign(3,7);
    sink(*it);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | 🛑 attempt to dereference a singular iterator | — (código 0) |

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
    iterator "this" @ 0x7ffe24cebf30 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffe24cebff0
    }
````

</details>

### f_vector_assign_it_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `llamada` | 🔴 `UB` | ✅ detectado |

```cpp
void f_vector_assign_it_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_vector_assign(c);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | 🛑 attempt to dereference a singular iterator | — (código 0) |

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
    iterator "this" @ 0x7ffe69759850 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffe69759910
    }
````

</details>

## Handle: referencia

### f_vector_assign_ref_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `recto` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_vector_assign_ref_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.assign(3,7);
  sink(h);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

### f_vector_assign_ref_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `guarda` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_vector_assign_ref_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.assign(3,7);
  sink(h);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

### f_vector_assign_ref_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_vector_assign_ref_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.assign(3,7);
    sink(h);
  }
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | 🛑 attempt to increment a singular iterator | — (código 0) |

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
    iterator "this" @ 0x7ffe3aa82d40 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7ffe3aa82e00
    }
````

</details>

### f_vector_assign_ref_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `llamada` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_vector_assign_ref_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_vector_assign(c);
  sink(h);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

## Handle: puntero

### f_vector_assign_ptr_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `recto` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_vector_assign_ptr_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.assign(3,7);
  sink(*h);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

### f_vector_assign_ptr_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `guarda` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_vector_assign_ptr_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.assign(3,7);
  sink(*h);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

### f_vector_assign_ptr_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_vector_assign_ptr_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.assign(3,7);
    sink(*h);
  }
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | 🛑 attempt to increment a singular iterator | — (código 0) |

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
    iterator "this" @ 0x7fff9007cb50 {
      type = gnu_cxx::normal_iterator<int*, std::vector<int, std::allocator<int> > > (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::vector<int, std::allocator<int> >' @ 0x7fff9007cc10
    }
````

</details>

### f_vector_assign_ptr_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `llamada` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_vector_assign_ptr_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_vector_assign(c);
  sink(*h);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |
