# `std::list::resize_grow`

Mutación: `c.resize(c.size()+100);`

- Iterador retenido: 🟢 `SAFE`
- Referencia/puntero retenido: 🟢 `SAFE`
- Casos `UB` detectados estáticamente: 0/0

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🟢 calla](#f_list_resize_grow_it_recto) | [🟢 calla](#f_list_resize_grow_it_guarda) | [🟢 calla](#f_list_resize_grow_it_bucle) | [🟢 calla](#f_list_resize_grow_it_llamada) |
| **referencia** | [🟢 calla](#f_list_resize_grow_ref_recto) | [🟢 calla](#f_list_resize_grow_ref_guarda) | [🟢 calla](#f_list_resize_grow_ref_bucle) | [🟢 calla](#f_list_resize_grow_ref_llamada) |
| **puntero** | [🟢 calla](#f_list_resize_grow_ptr_recto) | [🟢 calla](#f_list_resize_grow_ptr_guarda) | [🟢 calla](#f_list_resize_grow_ptr_bucle) | [🟢 calla](#f_list_resize_grow_ptr_llamada) |

## Handle: iterador

### f_list_resize_grow_it_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `recto` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_list_resize_grow_it_recto(std::list<int>& c) {
  auto it = c.begin();
  c.resize(c.size()+100);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

### f_list_resize_grow_it_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `guarda` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_list_resize_grow_it_guarda(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.resize(c.size()+100);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

### f_list_resize_grow_it_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `bucle` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_list_resize_grow_it_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.resize(c.size()+100);
    sink(*it);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

### f_list_resize_grow_it_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `llamada` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_list_resize_grow_it_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_list_resize_grow(c);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

## Handle: referencia

### f_list_resize_grow_ref_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `recto` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_list_resize_grow_ref_recto(std::list<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.resize(c.size()+100);
  sink(h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

### f_list_resize_grow_ref_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `guarda` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_list_resize_grow_ref_guarda(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.resize(c.size()+100);
  sink(h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

### f_list_resize_grow_ref_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `bucle` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_list_resize_grow_ref_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.resize(c.size()+100);
    sink(h);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

### f_list_resize_grow_ref_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `llamada` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_list_resize_grow_ref_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_list_resize_grow(c);
  sink(h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

## Handle: puntero

### f_list_resize_grow_ptr_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `recto` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_list_resize_grow_ptr_recto(std::list<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.resize(c.size()+100);
  sink(*h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

### f_list_resize_grow_ptr_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `guarda` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_list_resize_grow_ptr_guarda(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.resize(c.size()+100);
  sink(*h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

### f_list_resize_grow_ptr_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `bucle` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_list_resize_grow_ptr_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.resize(c.size()+100);
    sink(*h);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

### f_list_resize_grow_ptr_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `llamada` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_list_resize_grow_ptr_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_list_resize_grow(c);
  sink(*h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |
