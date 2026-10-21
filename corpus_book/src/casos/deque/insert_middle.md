# `std::deque::insert_middle`

Mutación: `c.insert(c.begin()+1,1);`

- Iterador retenido: 🔴 `UB`
- Referencia/puntero retenido: 🔴 `UB`
- Casos `UB` detectados estáticamente: 5/12

**En palabras:** después de `c.insert(c.begin()+1,1);` sobre un `std::deque`, un iterador guardado queda **inválido**: usarlo después es un bug (UB); una referencia o puntero guardado queda **inválido**: usarlo después es un bug (UB).

Mapa de los 12 casos. Cada celda muestra la respuesta correcta (etiqueta) y, debajo, lo que hizo el analizador estático de Clang. Clic para ir al caso. Ver [Cómo leer este libro](../../guia.md).

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🔴 `UB`<br>❌ no detectado](#f_deque_insert_middle_it_recto) | [🔴 `UB`<br>✅ detectado](#f_deque_insert_middle_it_guarda) | [🔴 `UB`<br>✅ detectado](#f_deque_insert_middle_it_bucle) | [🔴 `UB`<br>✅ detectado](#f_deque_insert_middle_it_llamada) |
| **referencia** | [🔴 `UB`<br>❌ no detectado](#f_deque_insert_middle_ref_recto) | [🔴 `UB`<br>❌ no detectado](#f_deque_insert_middle_ref_guarda) | [🔴 `UB`<br>✅ detectado](#f_deque_insert_middle_ref_bucle) | [🔴 `UB`<br>❌ no detectado](#f_deque_insert_middle_ref_llamada) |
| **puntero** | [🔴 `UB`<br>❌ no detectado](#f_deque_insert_middle_ptr_recto) | [🔴 `UB`<br>❌ no detectado](#f_deque_insert_middle_ptr_guarda) | [🔴 `UB`<br>✅ detectado](#f_deque_insert_middle_ptr_bucle) | [🔴 `UB`<br>❌ no detectado](#f_deque_insert_middle_ptr_llamada) |

## Handle: iterador

### f_deque_insert_middle_it_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_deque_insert_middle_it_recto(std::deque<int>& c) {
  auto it = c.begin();
  c.insert(c.begin()+1,1);
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
    const [with _Iterator = std::_Deque_iterator<int, int&, int*>; _Sequence 
    = std::debug::deque<int>; _Category = std::forward_iterator_tag; 
    reference = int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffc407c5910 {
      type = std::_Deque_iterator<int, int&, int*> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::deque<int, std::allocator<int> >' @ 0x7ffc407c5ac0
    }
````

</details>

### f_deque_insert_middle_it_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `guarda` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_deque_insert_middle_it_guarda(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.insert(c.begin()+1,1);
  sink(*it);
}
```

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
    const [with _Iterator = std::_Deque_iterator<int, int&, int*>; _Sequence 
    = std::debug::deque<int>; _Category = std::forward_iterator_tag; 
    reference = int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffcd8e2f3c0 {
      type = std::_Deque_iterator<int, int&, int*> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::deque<int, std::allocator<int> >' @ 0x7ffcd8e2f570
    }
````

</details>

### f_deque_insert_middle_it_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_deque_insert_middle_it_bucle(std::deque<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.insert(c.begin()+1,1);
    sink(*it);
  }
}
```

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
    const [with _Iterator = std::_Deque_iterator<int, int&, int*>; _Sequence 
    = std::debug::deque<int>; _Category = std::forward_iterator_tag; 
    reference = int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7fffc8a87010 {
      type = std::_Deque_iterator<int, int&, int*> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::deque<int, std::allocator<int> >' @ 0x7fffc8a871c0
    }
````

</details>

### f_deque_insert_middle_it_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `llamada` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_deque_insert_middle_it_llamada(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_deque_insert_middle(c);
  sink(*it);
}
```

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
    const [with _Iterator = std::_Deque_iterator<int, int&, int*>; _Sequence 
    = std::debug::deque<int>; _Category = std::forward_iterator_tag; 
    reference = int&]

Error: attempt to dereference a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffe1d30a1c0 {
      type = std::_Deque_iterator<int, int&, int*> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::deque<int, std::allocator<int> >' @ 0x7ffe1d30a2b0
    }
````

</details>

## Handle: referencia

### f_deque_insert_middle_ref_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_deque_insert_middle_ref_recto(std::deque<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.insert(c.begin()+1,1);
  sink(h);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_deque_insert_middle_ref_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_deque_insert_middle_ref_guarda(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.insert(c.begin()+1,1);
  sink(h);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_deque_insert_middle_ref_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `bucle` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_deque_insert_middle_ref_bucle(std::deque<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.insert(c.begin()+1,1);
    sink(h);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | 🛑 attempt to increment a singular iterator | sin detección |

<details>
<summary>stderr libstdc++ Debug · <code>natural</code></summary>

````text
/usr/include/c++/13/debug/safe_iterator.h:326:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>& 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator++() 
    [with _Iterator = std::_Deque_iterator<int, int&, int*>; _Sequence = 
    std::debug::deque<int>; _Category = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffcf15df780 {
      type = std::_Deque_iterator<int, int&, int*> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::deque<int, std::allocator<int> >' @ 0x7ffcf15df930
    }
````

</details>

### f_deque_insert_middle_ref_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_deque_insert_middle_ref_llamada(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_deque_insert_middle(c);
  sink(h);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

## Handle: puntero

### f_deque_insert_middle_ptr_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `recto` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_deque_insert_middle_ptr_recto(std::deque<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.insert(c.begin()+1,1);
  sink(*h);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_deque_insert_middle_ptr_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `guarda` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_deque_insert_middle_ptr_guarda(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.insert(c.begin()+1,1);
  sink(*h);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_deque_insert_middle_ptr_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `bucle` | 🔴 `UB` | ✅ detectado | ✅ detectado |

```cpp
void f_deque_insert_middle_ptr_bucle(std::deque<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.insert(c.begin()+1,1);
    sink(*h);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | 🛑 attempt to increment a singular iterator | sin detección |

<details>
<summary>stderr libstdc++ Debug · <code>natural</code></summary>

````text
/usr/include/c++/13/debug/safe_iterator.h:326:
In function:
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>& 
    gnu_debug::_Safe_iterator<_Iterator, _Sequence, _Category>::operator++() 
    [with _Iterator = std::_Deque_iterator<int, int&, int*>; _Sequence = 
    std::debug::deque<int>; _Category = std::forward_iterator_tag]

Error: attempt to increment a singular iterator.

Objects involved in the operation:
    iterator "this" @ 0x7ffca318ab50 {
      type = std::_Deque_iterator<int, int&, int*> (mutable iterator);
      state = singular;
      references sequence with type 'std::debug::deque<int, std::allocator<int> >' @ 0x7ffca318ad00
    }
````

</details>

### f_deque_insert_middle_ptr_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `llamada` | 🔴 `UB` | ❌ no detectado | ✅ detectado |

```cpp
void f_deque_insert_middle_ptr_llamada(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_deque_insert_middle(c);
  sink(*h);
}
```

> **Causa del falso negativo:** 1. El dominio de referencias y punteros no esta modelado

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |
