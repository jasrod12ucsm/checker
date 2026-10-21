# `std::forward_list::push_front`

Mutación: `c.push_front(1);`

- Iterador retenido: 🟢 `SAFE`
- Referencia/puntero retenido: 🟢 `SAFE`
- Casos `UB` detectados estáticamente: 0/0

**En palabras:** después de `c.push_front(1);` sobre un `std::forward_list`, un iterador guardado sigue siendo **válido**: usarlo después es correcto; una referencia o puntero guardado sigue siendo **válido**: usarlo después es correcto.

Mapa de los 12 casos. Cada celda muestra la respuesta correcta (etiqueta) y, debajo, lo que hizo el analizador estático de Clang. Clic para ir al caso. Ver [Cómo leer este libro](../../guia.md).

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🟢 `SAFE`<br>✅ correcto, sin aviso](#f_flist_push_front_it_recto) | [🟢 `SAFE`<br>✅ correcto, sin aviso](#f_flist_push_front_it_guarda) | [🟢 `SAFE`<br>✅ correcto, sin aviso](#f_flist_push_front_it_bucle) | [🟢 `SAFE`<br>✅ correcto, sin aviso](#f_flist_push_front_it_llamada) |
| **referencia** | [🟢 `SAFE`<br>✅ correcto, sin aviso](#f_flist_push_front_ref_recto) | [🟢 `SAFE`<br>✅ correcto, sin aviso](#f_flist_push_front_ref_guarda) | [🟢 `SAFE`<br>✅ correcto, sin aviso](#f_flist_push_front_ref_bucle) | [🟢 `SAFE`<br>✅ correcto, sin aviso](#f_flist_push_front_ref_llamada) |
| **puntero** | [🟢 `SAFE`<br>✅ correcto, sin aviso](#f_flist_push_front_ptr_recto) | [🟢 `SAFE`<br>✅ correcto, sin aviso](#f_flist_push_front_ptr_guarda) | [🟢 `SAFE`<br>✅ correcto, sin aviso](#f_flist_push_front_ptr_bucle) | [🟢 `SAFE`<br>✅ correcto, sin aviso](#f_flist_push_front_ptr_llamada) |

## Handle: iterador

### f_flist_push_front_it_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_flist_push_front_it_recto(std::forward_list<int>& c) {
  auto it = c.begin();
  c.push_front(1);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_flist_push_front_it_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_flist_push_front_it_guarda(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.push_front(1);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_flist_push_front_it_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_flist_push_front_it_bucle(std::forward_list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.push_front(1);
    sink(*it);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_flist_push_front_it_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_flist_push_front_it_llamada(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_flist_push_front(c);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

## Handle: referencia

### f_flist_push_front_ref_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_flist_push_front_ref_recto(std::forward_list<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.push_front(1);
  sink(h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_flist_push_front_ref_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_flist_push_front_ref_guarda(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.push_front(1);
  sink(h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_flist_push_front_ref_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_flist_push_front_ref_bucle(std::forward_list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.push_front(1);
    sink(h);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_flist_push_front_ref_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_flist_push_front_ref_llamada(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_flist_push_front(c);
  sink(h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

## Handle: puntero

### f_flist_push_front_ptr_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_flist_push_front_ptr_recto(std::forward_list<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.push_front(1);
  sink(*h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_flist_push_front_ptr_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_flist_push_front_ptr_guarda(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.push_front(1);
  sink(*h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_flist_push_front_ptr_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_flist_push_front_ptr_bucle(std::forward_list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.push_front(1);
    sink(*h);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_flist_push_front_ptr_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_flist_push_front_ptr_llamada(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_flist_push_front(c);
  sink(*h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |
