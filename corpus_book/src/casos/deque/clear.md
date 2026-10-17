# `std::deque::clear`

Mutación: `c.clear();`

- Iterador retenido: 🔴 `UB`
- Referencia/puntero retenido: 🔴 `UB`
- Casos `UB` detectados estáticamente: 4/12

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🔴 avisa](#f_deque_clear_it_recto) | [🔴 avisa](#f_deque_clear_it_guarda) | [🔴 avisa](#f_deque_clear_it_bucle) | [🔴 avisa](#f_deque_clear_it_llamada) |
| **referencia** | [🔴 calla](#f_deque_clear_ref_recto) | [🔴 calla](#f_deque_clear_ref_guarda) | [🔴 calla](#f_deque_clear_ref_bucle) | [🔴 calla](#f_deque_clear_ref_llamada) |
| **puntero** | [🔴 calla](#f_deque_clear_ptr_recto) | [🔴 calla](#f_deque_clear_ptr_guarda) | [🔴 calla](#f_deque_clear_ptr_bucle) | [🔴 calla](#f_deque_clear_ptr_llamada) |

## Handle: iterador

### f_deque_clear_it_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `recto` | 🔴 `UB` | ✅ detectado |

```cpp
void f_deque_clear_it_recto(std::deque<int>& c) {
  auto it = c.begin();
  c.clear();
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
    const [with _Iterator = std::_Deque_iterator<int, int&, int*>; _Sequence 
    = std::debug::deque<int>; _Category = std::forward_iterator_tag; 
    reference = int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffdffe858a0 {
      type = std::_Deque_iterator<int, int&, int*> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::deque<int, std::allocator<int> >' @ 0x7ffdffe85940
    }
````

</details>

### f_deque_clear_it_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `guarda` | 🔴 `UB` | ✅ detectado |

```cpp
void f_deque_clear_it_guarda(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.clear();
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
    const [with _Iterator = std::_Deque_iterator<int, int&, int*>; _Sequence 
    = std::debug::deque<int>; _Category = std::forward_iterator_tag; 
    reference = int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffc1f0a0780 {
      type = std::_Deque_iterator<int, int&, int*> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::deque<int, std::allocator<int> >' @ 0x7ffc1f0a0870
    }
````

</details>

### f_deque_clear_it_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ✅ detectado |

```cpp
void f_deque_clear_it_bucle(std::deque<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.clear();
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
    const [with _Iterator = std::_Deque_iterator<int, int&, int*>; _Sequence 
    = std::debug::deque<int>; _Category = std::forward_iterator_tag; 
    reference = int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffe8e78cd60 {
      type = std::_Deque_iterator<int, int&, int*> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::deque<int, std::allocator<int> >' @ 0x7ffe8e78ce50
    }
````

</details>

### f_deque_clear_it_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `llamada` | 🔴 `UB` | ✅ detectado |

```cpp
void f_deque_clear_it_llamada(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_deque_clear(c);
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
    const [with _Iterator = std::_Deque_iterator<int, int&, int*>; _Sequence 
    = std::debug::deque<int>; _Category = std::forward_iterator_tag; 
    reference = int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffd0c7f2d60 {
      type = std::_Deque_iterator<int, int&, int*> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::deque<int, std::allocator<int> >' @ 0x7ffd0c7f2e50
    }
````

</details>

## Handle: referencia

### f_deque_clear_ref_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `recto` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_deque_clear_ref_recto(std::deque<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.clear();
  sink(h);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

### f_deque_clear_ref_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `guarda` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_deque_clear_ref_guarda(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.clear();
  sink(h);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

### f_deque_clear_ref_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_deque_clear_ref_bucle(std::deque<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.clear();
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
    [with _Iterator = std::_Deque_iterator<int, int&, int*>; _Sequence = 
    std::debug::deque<int>; _Category = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffdac548120 {
      type = std::_Deque_iterator<int, int&, int*> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::deque<int, std::allocator<int> >' @ 0x7ffdac548210
    }
````

</details>

### f_deque_clear_ref_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `llamada` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_deque_clear_ref_llamada(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_deque_clear(c);
  sink(h);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

## Handle: puntero

### f_deque_clear_ptr_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `recto` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_deque_clear_ptr_recto(std::deque<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.clear();
  sink(*h);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

### f_deque_clear_ptr_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `guarda` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_deque_clear_ptr_guarda(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.clear();
  sink(*h);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

### f_deque_clear_ptr_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_deque_clear_ptr_bucle(std::deque<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.clear();
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
    [with _Iterator = std::_Deque_iterator<int, int&, int*>; _Sequence = 
    std::debug::deque<int>; _Category = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fffdf8ca060 {
      type = std::_Deque_iterator<int, int&, int*> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::deque<int, std::allocator<int> >' @ 0x7fffdf8ca150
    }
````

</details>

### f_deque_clear_ptr_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `llamada` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_deque_clear_ptr_llamada(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_deque_clear(c);
  sink(*h);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |
