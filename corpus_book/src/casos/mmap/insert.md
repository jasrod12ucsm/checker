# `std::multimap::insert`

Mutación: `c.insert({99,1});`

- Iterador retenido: 🟢 `SAFE`
- Referencia/puntero retenido: 🟢 `SAFE`
- Casos `UB` detectados estáticamente: 0/0

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🟢 calla](#f_mmap_insert_it_recto) | [🟢 calla](#f_mmap_insert_it_guarda) | [🟢 calla](#f_mmap_insert_it_bucle) | [🟢 calla](#f_mmap_insert_it_llamada) |
| **referencia** | [🟢 calla](#f_mmap_insert_ref_recto) | [🟢 calla](#f_mmap_insert_ref_guarda) | [🟢 calla](#f_mmap_insert_ref_bucle) | [🟢 calla](#f_mmap_insert_ref_llamada) |
| **puntero** | [🟢 calla](#f_mmap_insert_ptr_recto) | [🟢 calla](#f_mmap_insert_ptr_guarda) | [🟢 calla](#f_mmap_insert_ptr_bucle) | [🟢 calla](#f_mmap_insert_ptr_llamada) |

## Handle: iterador

### f_mmap_insert_it_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `recto` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_mmap_insert_it_recto(std::multimap<int,int>& c) {
  auto it = c.begin();
  c.insert({99,1});
  sink(it->second);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

### f_mmap_insert_it_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `guarda` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_mmap_insert_it_guarda(std::multimap<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.insert({99,1});
  sink(it->second);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

### f_mmap_insert_it_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `bucle` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_mmap_insert_it_bucle(std::multimap<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.insert({99,1});
    sink(it->second);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

### f_mmap_insert_it_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| iterador | `llamada` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_mmap_insert_it_llamada(std::multimap<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_mmap_insert(c);
  sink(it->second);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

## Handle: referencia

### f_mmap_insert_ref_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `recto` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_mmap_insert_ref_recto(std::multimap<int,int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.insert({99,1});
  sink(h.second);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

### f_mmap_insert_ref_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `guarda` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_mmap_insert_ref_guarda(std::multimap<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.insert({99,1});
  sink(h.second);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

### f_mmap_insert_ref_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `bucle` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_mmap_insert_ref_bucle(std::multimap<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.insert({99,1});
    sink(h.second);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

### f_mmap_insert_ref_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| referencia | `llamada` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_mmap_insert_ref_llamada(std::multimap<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_mmap_insert(c);
  sink(h.second);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

## Handle: puntero

### f_mmap_insert_ptr_recto

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `recto` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_mmap_insert_ptr_recto(std::multimap<int,int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.insert({99,1});
  sink(h->second);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

### f_mmap_insert_ptr_guarda

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `guarda` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_mmap_insert_ptr_guarda(std::multimap<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.insert({99,1});
  sink(h->second);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

### f_mmap_insert_ptr_bucle

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `bucle` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_mmap_insert_ptr_bucle(std::multimap<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.insert({99,1});
    sink(h->second);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |

### f_mmap_insert_ptr_llamada

| Handle | Forma | Etiqueta | Análisis estático |
|---|---|---|---|
| puntero | `llamada` | 🟢 `SAFE` | ✅ silencio correcto |

```cpp
void f_mmap_insert_ptr_llamada(std::multimap<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_mmap_insert(c);
  sink(h->second);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | — (código 0) | — (código 0) |
