# `std::unordered_set::insert`

Mutación: `c.insert(99);`

- Iterador retenido: 🟡 `POLICY`
- Referencia/puntero retenido: 🟢 `SAFE`
- Casos `UB` detectados estáticamente: 0/0

**En palabras:** después de `c.insert(99);` sobre un `std::unordered_set`, un iterador guardado **puede** quedar inválido según el estado del contenedor (capacidad o factor de carga); una referencia o puntero guardado sigue siendo **válido**: usarlo después es correcto.

Mapa de los 12 casos. Cada celda muestra la respuesta correcta (etiqueta) y, debajo, lo que hizo el analizador estático de Clang. Clic para ir al caso. Ver [Cómo leer este libro](../../guia.md).

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_uset_insert_it_recto) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_uset_insert_it_guarda) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_uset_insert_it_bucle) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_uset_insert_it_llamada) |
| **referencia** | [🟢 `SAFE`<br>✅ correcto, sin aviso](#f_uset_insert_ref_recto) | [🟢 `SAFE`<br>✅ correcto, sin aviso](#f_uset_insert_ref_guarda) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_uset_insert_ref_bucle) | [🟢 `SAFE`<br>✅ correcto, sin aviso](#f_uset_insert_ref_llamada) |
| **puntero** | [🟢 `SAFE`<br>✅ correcto, sin aviso](#f_uset_insert_ptr_recto) | [🟢 `SAFE`<br>✅ correcto, sin aviso](#f_uset_insert_ptr_guarda) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_uset_insert_ptr_bucle) | [🟢 `SAFE`<br>✅ correcto, sin aviso](#f_uset_insert_ptr_llamada) |

## Handle: iterador

### f_uset_insert_it_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_uset_insert_it_recto(std::unordered_set<int>& c) {
  auto it = c.begin();
  c.insert(99);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | factor de carga alcanzado; la inserción dispara rehash | 🛑 attempt to dereference a singular iterator | sin detección |
| `preserve` | reserve(256), sin rehash para la inserción evaluada | sin detección | sin detección |

<details>
<summary>stderr libstdc++ Debug · <code>force</code></summary>

````text
/usr/include/c++/13/debug/safe_iterator.h:298:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::reference 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator*() 
    const [with _Iterator = std::detail::_Node_iterator<int, true, false>; 
    _Sequence = std::debug::unordered_set<int>; _Category = 
    std::forward_iterator_tag; reference = const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fff2d199930 {
      type = std::detail::_Node_iterator<int, true, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int> >' @ 0x7fff2d199a00
    }
````

</details>

### f_uset_insert_it_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

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
| `force` | factor de carga alcanzado; la inserción dispara rehash | 🛑 attempt to dereference a singular iterator | sin detección |
| `preserve` | reserve(256), sin rehash para la inserción evaluada | sin detección | sin detección |

<details>
<summary>stderr libstdc++ Debug · <code>force</code></summary>

````text
/usr/include/c++/13/debug/safe_iterator.h:298:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::reference 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator*() 
    const [with _Iterator = std::detail::_Node_iterator<int, true, false>; 
    _Sequence = std::debug::unordered_set<int>; _Category = 
    std::forward_iterator_tag; reference = const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffd3dc12aa0 {
      type = std::detail::_Node_iterator<int, true, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int> >' @ 0x7ffd3dc12b70
    }
````

</details>

### f_uset_insert_it_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_uset_insert_it_bucle(std::unordered_set<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.insert(99);
    sink(*it);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | factor de carga alcanzado; la inserción dispara rehash | 🛑 attempt to dereference a singular iterator | sin detección |
| `preserve` | reserve(256), sin rehash para la inserción evaluada | sin detección | sin detección |

<details>
<summary>stderr libstdc++ Debug · <code>force</code></summary>

````text
/usr/include/c++/13/debug/safe_iterator.h:298:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::reference 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator*() 
    const [with _Iterator = std::detail::_Node_iterator<int, true, false>; 
    _Sequence = std::debug::unordered_set<int>; _Category = 
    std::forward_iterator_tag; reference = const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffd7ec92610 {
      type = std::detail::_Node_iterator<int, true, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int> >' @ 0x7ffd7ec926e0
    }
````

</details>

### f_uset_insert_it_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

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
| `force` | factor de carga alcanzado; la inserción dispara rehash | 🛑 attempt to dereference a singular iterator | sin detección |
| `preserve` | reserve(256), sin rehash para la inserción evaluada | sin detección | sin detección |

<details>
<summary>stderr libstdc++ Debug · <code>force</code></summary>

````text
/usr/include/c++/13/debug/safe_iterator.h:298:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::reference 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator*() 
    const [with _Iterator = std::detail::_Node_iterator<int, true, false>; 
    _Sequence = std::debug::unordered_set<int>; _Category = 
    std::forward_iterator_tag; reference = const int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffd775da3c0 {
      type = std::detail::_Node_iterator<int, true, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int> >' @ 0x7ffd775da480
    }
````

</details>

## Handle: referencia

### f_uset_insert_ref_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

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
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_uset_insert_ref_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

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
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_uset_insert_ref_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

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
| `force` | factor de carga alcanzado; la inserción dispara rehash | 🛑 attempt to increment a singular iterator | sin detección |
| `preserve` | reserve(256), sin rehash para la inserción evaluada | sin detección | sin detección |

<details>
<summary>stderr libstdc++ Debug · <code>force</code></summary>

````text
/usr/include/c++/13/debug/safe_iterator.h:326:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>& 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator++() 
    [with _Iterator = std::detail::_Node_iterator<int, true, false>; 
    _Sequence = std::debug::unordered_set<int>; _Category = 
    std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffce5db2340 {
      type = std::detail::_Node_iterator<int, true, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int> >' @ 0x7ffce5db2410
    }
````

</details>

### f_uset_insert_ref_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

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
| `natural` | estado inicial ordinario | sin detección | sin detección |

## Handle: puntero

### f_uset_insert_ptr_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

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
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_uset_insert_ptr_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

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
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_uset_insert_ptr_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

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
| `force` | factor de carga alcanzado; la inserción dispara rehash | 🛑 attempt to increment a singular iterator | sin detección |
| `preserve` | reserve(256), sin rehash para la inserción evaluada | sin detección | sin detección |

<details>
<summary>stderr libstdc++ Debug · <code>force</code></summary>

````text
/usr/include/c++/13/debug/safe_iterator.h:326:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>& 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator++() 
    [with _Iterator = std::detail::_Node_iterator<int, true, false>; 
    _Sequence = std::debug::unordered_set<int>; _Category = 
    std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fff8b1765c0 {
      type = std::detail::_Node_iterator<int, true, false> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::unordered_set<int, std::hash<int>, std::equal_to<int>, std::allocator<int> >' @ 0x7fff8b176690
    }
````

</details>

### f_uset_insert_ptr_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

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
| `natural` | estado inicial ordinario | sin detección | sin detección |
