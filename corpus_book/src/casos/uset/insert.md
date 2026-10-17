# `std::unordered_set::insert`

Mutación: `c.insert(99);`

- Iterador retenido: 🟡 `POLICY`
- Referencia/puntero retenido: 🟢 `SAFE`
- Casos `UB` detectados estáticamente: 0/1

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🟡 calla](#f_uset_insert_it_recto) | [🟡 calla](#f_uset_insert_it_guarda) | [🔴 calla](#f_uset_insert_it_bucle) | [🟡 calla](#f_uset_insert_it_llamada) |
| **referencia** | [🟢 calla](#f_uset_insert_ref_recto) | [🟢 calla](#f_uset_insert_ref_guarda) | [🟢 calla](#f_uset_insert_ref_bucle) | [🟢 calla](#f_uset_insert_ref_llamada) |
| **puntero** | [🟢 calla](#f_uset_insert_ptr_recto) | [🟢 calla](#f_uset_insert_ptr_guarda) | [🟢 calla](#f_uset_insert_ptr_bucle) | [🟢 calla](#f_uset_insert_ptr_llamada) |

## Handle: iterador

### f_uset_insert_it_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `recto` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_uset_insert_it_recto(std::unordered_set<int>& c) {
  auto it = c.begin();
  c.insert(99);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | factor de carga alcanzado; la inserción dispara rehash | 🛑 attempt to dereference a singular iterator | — (código 0) |
| `preserve` | reserve(256), sin rehash para la inserción evaluada | — (código 0) | — (código 0) |

<details>
<summary>stderr libstdc++ Debug · <code>force</code></summary>

````text
/usr/include/c++/16/debug/safe_iterator.h:352:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::reference 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator*() 
    const [with _Iterator = std::detail::_Node_iterator<int, true, false>; 
    _Sequence = std::debug::unordered_set<int>; _Category = 
    std::forward_iterator_tag; reference = const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffd03d7e080 {
      type = std::detail::_Node_iterator<int, true, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int> >' @ 0x7ffd03d7e150
    }
````

</details>

### f_uset_insert_it_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `guarda` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_uset_insert_it_guarda(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.insert(99);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | factor de carga alcanzado; la inserción dispara rehash | 🛑 attempt to dereference a singular iterator | — (código 0) |
| `preserve` | reserve(256), sin rehash para la inserción evaluada | — (código 0) | — (código 0) |

<details>
<summary>stderr libstdc++ Debug · <code>force</code></summary>

````text
/usr/include/c++/16/debug/safe_iterator.h:352:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::reference 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator*() 
    const [with _Iterator = std::detail::_Node_iterator<int, true, false>; 
    _Sequence = std::debug::unordered_set<int>; _Category = 
    std::forward_iterator_tag; reference = const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffec3f29370 {
      type = std::detail::_Node_iterator<int, true, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int> >' @ 0x7ffec3f29440
    }
````

</details>

### f_uset_insert_it_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ❌ falso negativo |

```cpp
void f_uset_insert_it_bucle(std::unordered_set<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.insert(99);
    sink(*it);
  }
}
```

> **Causa del falso negativo:** 4. La invalidacion por insercion/realojamiento no esta modelada

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

### f_uset_insert_it_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `llamada` | 🟡 `POLICY` | silencio (optimista) |

```cpp
void f_uset_insert_it_llamada(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_uset_insert(c);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | factor de carga alcanzado; la inserción dispara rehash | 🛑 attempt to dereference a singular iterator | — (código 0) |
| `preserve` | reserve(256), sin rehash para la inserción evaluada | — (código 0) | — (código 0) |

<details>
<summary>stderr libstdc++ Debug · <code>force</code></summary>

````text
/usr/include/c++/16/debug/safe_iterator.h:352:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::reference 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator*() 
    const [with _Iterator = std::detail::_Node_iterator<int, true, false>; 
    _Sequence = std::debug::unordered_set<int>; _Category = 
    std::forward_iterator_tag; reference = const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fff92abbbc0 {
      type = std::detail::_Node_iterator<int, true, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int> >' @ 0x7fff92abbc80
    }
````

</details>

## Handle: referencia

### f_uset_insert_ref_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `recto` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_uset_insert_ref_recto(std::unordered_set<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.insert(99);
  sink(h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

### f_uset_insert_ref_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `guarda` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_uset_insert_ref_guarda(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.insert(99);
  sink(h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

### f_uset_insert_ref_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `bucle` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_uset_insert_ref_bucle(std::unordered_set<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.insert(99);
    sink(h);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

### f_uset_insert_ref_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `llamada` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_uset_insert_ref_llamada(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_uset_insert(c);
  sink(h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

## Handle: puntero

### f_uset_insert_ptr_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `recto` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_uset_insert_ptr_recto(std::unordered_set<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.insert(99);
  sink(*h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

### f_uset_insert_ptr_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `guarda` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_uset_insert_ptr_guarda(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.insert(99);
  sink(*h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

### f_uset_insert_ptr_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `bucle` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_uset_insert_ptr_bucle(std::unordered_set<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.insert(99);
    sink(*h);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

### f_uset_insert_ptr_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `llamada` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_uset_insert_ptr_llamada(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_uset_insert(c);
  sink(*h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |
