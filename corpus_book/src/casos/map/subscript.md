# `std::map::subscript`

Mutación: `c[97]=1;`

- Iterador retenido: 🟢 `SAFE`
- Referencia/puntero retenido: 🟢 `SAFE`
- Casos `UB` detectados estáticamente: 0/0

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🟢 calla](#f_map_subscript_it_recto) | [🟢 calla](#f_map_subscript_it_guarda) | [🟢 calla](#f_map_subscript_it_bucle) | [🟢 calla](#f_map_subscript_it_llamada) |
| **referencia** | [🟢 calla](#f_map_subscript_ref_recto) | [🟢 calla](#f_map_subscript_ref_guarda) | [🟢 calla](#f_map_subscript_ref_bucle) | [🟢 calla](#f_map_subscript_ref_llamada) |
| **puntero** | [🟢 calla](#f_map_subscript_ptr_recto) | [🟢 calla](#f_map_subscript_ptr_guarda) | [🟢 calla](#f_map_subscript_ptr_bucle) | [🟢 calla](#f_map_subscript_ptr_llamada) |

## Handle: iterador

### f_map_subscript_it_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `recto` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_map_subscript_it_recto(std::map<int,int>& c) {
  auto it = c.begin();
  c[97]=1;
  sink(it->second);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

### f_map_subscript_it_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `guarda` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_map_subscript_it_guarda(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c[97]=1;
  sink(it->second);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

### f_map_subscript_it_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `bucle` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_map_subscript_it_bucle(std::map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c[97]=1;
    sink(it->second);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

### f_map_subscript_it_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `llamada` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_map_subscript_it_llamada(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_map_subscript(c);
  sink(it->second);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

## Handle: referencia

### f_map_subscript_ref_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `recto` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_map_subscript_ref_recto(std::map<int,int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c[97]=1;
  sink(h.second);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

### f_map_subscript_ref_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `guarda` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_map_subscript_ref_guarda(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c[97]=1;
  sink(h.second);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

### f_map_subscript_ref_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `bucle` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_map_subscript_ref_bucle(std::map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c[97]=1;
    sink(h.second);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

### f_map_subscript_ref_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `llamada` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_map_subscript_ref_llamada(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_map_subscript(c);
  sink(h.second);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

## Handle: puntero

### f_map_subscript_ptr_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `recto` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_map_subscript_ptr_recto(std::map<int,int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c[97]=1;
  sink(h->second);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

### f_map_subscript_ptr_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `guarda` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_map_subscript_ptr_guarda(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c[97]=1;
  sink(h->second);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

### f_map_subscript_ptr_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `bucle` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_map_subscript_ptr_bucle(std::map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c[97]=1;
    sink(h->second);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

### f_map_subscript_ptr_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `llamada` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_map_subscript_ptr_llamada(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_map_subscript(c);
  sink(h->second);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |
