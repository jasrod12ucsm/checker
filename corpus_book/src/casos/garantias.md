# Casos de buen uso (garantías)

Casos `SAFE` sobre mutaciones que **pueden** invalidar, escritos como lo haría quien conoce la norma ([D-20](../diseno/decisiones.md)). Miden los falsos positivos de un checker que avisara en todo `push_back` o todo `erase`.

## `reserva`: `reserve(c.size() + k)` antes de las inserciones

54 casos; con aviso estático: 0.

| Caso | Contenedor | Operación | Sostiene | Forma | Estático |
|---|---|---|---|---|---|
| [`f_vector_push_back_it_recto_reserva`](#f_vector_push_back_it_recto_reserva) | `vector` | `push_back` | `it` | `recto` | ✅ correcto, sin aviso |
| [`f_vector_push_back_it_guarda_reserva`](#f_vector_push_back_it_guarda_reserva) | `vector` | `push_back` | `it` | `guarda` | ✅ correcto, sin aviso |
| [`f_vector_push_back_it_bucle_reserva`](#f_vector_push_back_it_bucle_reserva) | `vector` | `push_back` | `it` | `bucle` | ✅ correcto, sin aviso |
| [`f_vector_push_back_it_llamada_reserva`](#f_vector_push_back_it_llamada_reserva) | `vector` | `push_back` | `it` | `llamada` | ✅ correcto, sin aviso |
| [`f_vector_push_back_ref_recto_reserva`](#f_vector_push_back_ref_recto_reserva) | `vector` | `push_back` | `ref` | `recto` | ✅ correcto, sin aviso |
| [`f_vector_push_back_ref_guarda_reserva`](#f_vector_push_back_ref_guarda_reserva) | `vector` | `push_back` | `ref` | `guarda` | ✅ correcto, sin aviso |
| [`f_vector_push_back_ref_bucle_reserva`](#f_vector_push_back_ref_bucle_reserva) | `vector` | `push_back` | `ref` | `bucle` | ✅ correcto, sin aviso |
| [`f_vector_push_back_ref_llamada_reserva`](#f_vector_push_back_ref_llamada_reserva) | `vector` | `push_back` | `ref` | `llamada` | ✅ correcto, sin aviso |
| [`f_vector_push_back_ptr_recto_reserva`](#f_vector_push_back_ptr_recto_reserva) | `vector` | `push_back` | `ptr` | `recto` | ✅ correcto, sin aviso |
| [`f_vector_push_back_ptr_guarda_reserva`](#f_vector_push_back_ptr_guarda_reserva) | `vector` | `push_back` | `ptr` | `guarda` | ✅ correcto, sin aviso |
| [`f_vector_push_back_ptr_bucle_reserva`](#f_vector_push_back_ptr_bucle_reserva) | `vector` | `push_back` | `ptr` | `bucle` | ✅ correcto, sin aviso |
| [`f_vector_push_back_ptr_llamada_reserva`](#f_vector_push_back_ptr_llamada_reserva) | `vector` | `push_back` | `ptr` | `llamada` | ✅ correcto, sin aviso |
| [`f_vector_emplace_back_it_recto_reserva`](#f_vector_emplace_back_it_recto_reserva) | `vector` | `emplace_back` | `it` | `recto` | ✅ correcto, sin aviso |
| [`f_vector_emplace_back_it_guarda_reserva`](#f_vector_emplace_back_it_guarda_reserva) | `vector` | `emplace_back` | `it` | `guarda` | ✅ correcto, sin aviso |
| [`f_vector_emplace_back_it_bucle_reserva`](#f_vector_emplace_back_it_bucle_reserva) | `vector` | `emplace_back` | `it` | `bucle` | ✅ correcto, sin aviso |
| [`f_vector_emplace_back_it_llamada_reserva`](#f_vector_emplace_back_it_llamada_reserva) | `vector` | `emplace_back` | `it` | `llamada` | ✅ correcto, sin aviso |
| [`f_vector_emplace_back_ref_recto_reserva`](#f_vector_emplace_back_ref_recto_reserva) | `vector` | `emplace_back` | `ref` | `recto` | ✅ correcto, sin aviso |
| [`f_vector_emplace_back_ref_guarda_reserva`](#f_vector_emplace_back_ref_guarda_reserva) | `vector` | `emplace_back` | `ref` | `guarda` | ✅ correcto, sin aviso |
| [`f_vector_emplace_back_ref_bucle_reserva`](#f_vector_emplace_back_ref_bucle_reserva) | `vector` | `emplace_back` | `ref` | `bucle` | ✅ correcto, sin aviso |
| [`f_vector_emplace_back_ref_llamada_reserva`](#f_vector_emplace_back_ref_llamada_reserva) | `vector` | `emplace_back` | `ref` | `llamada` | ✅ correcto, sin aviso |
| [`f_vector_emplace_back_ptr_recto_reserva`](#f_vector_emplace_back_ptr_recto_reserva) | `vector` | `emplace_back` | `ptr` | `recto` | ✅ correcto, sin aviso |
| [`f_vector_emplace_back_ptr_guarda_reserva`](#f_vector_emplace_back_ptr_guarda_reserva) | `vector` | `emplace_back` | `ptr` | `guarda` | ✅ correcto, sin aviso |
| [`f_vector_emplace_back_ptr_bucle_reserva`](#f_vector_emplace_back_ptr_bucle_reserva) | `vector` | `emplace_back` | `ptr` | `bucle` | ✅ correcto, sin aviso |
| [`f_vector_emplace_back_ptr_llamada_reserva`](#f_vector_emplace_back_ptr_llamada_reserva) | `vector` | `emplace_back` | `ptr` | `llamada` | ✅ correcto, sin aviso |
| [`f_vector_insert_end_it_recto_reserva`](#f_vector_insert_end_it_recto_reserva) | `vector` | `insert_end` | `it` | `recto` | ✅ correcto, sin aviso |
| [`f_vector_insert_end_it_guarda_reserva`](#f_vector_insert_end_it_guarda_reserva) | `vector` | `insert_end` | `it` | `guarda` | ✅ correcto, sin aviso |
| [`f_vector_insert_end_it_bucle_reserva`](#f_vector_insert_end_it_bucle_reserva) | `vector` | `insert_end` | `it` | `bucle` | ✅ correcto, sin aviso |
| [`f_vector_insert_end_it_llamada_reserva`](#f_vector_insert_end_it_llamada_reserva) | `vector` | `insert_end` | `it` | `llamada` | ✅ correcto, sin aviso |
| [`f_vector_insert_end_ref_recto_reserva`](#f_vector_insert_end_ref_recto_reserva) | `vector` | `insert_end` | `ref` | `recto` | ✅ correcto, sin aviso |
| [`f_vector_insert_end_ref_guarda_reserva`](#f_vector_insert_end_ref_guarda_reserva) | `vector` | `insert_end` | `ref` | `guarda` | ✅ correcto, sin aviso |
| [`f_vector_insert_end_ref_bucle_reserva`](#f_vector_insert_end_ref_bucle_reserva) | `vector` | `insert_end` | `ref` | `bucle` | ✅ correcto, sin aviso |
| [`f_vector_insert_end_ref_llamada_reserva`](#f_vector_insert_end_ref_llamada_reserva) | `vector` | `insert_end` | `ref` | `llamada` | ✅ correcto, sin aviso |
| [`f_vector_insert_end_ptr_recto_reserva`](#f_vector_insert_end_ptr_recto_reserva) | `vector` | `insert_end` | `ptr` | `recto` | ✅ correcto, sin aviso |
| [`f_vector_insert_end_ptr_guarda_reserva`](#f_vector_insert_end_ptr_guarda_reserva) | `vector` | `insert_end` | `ptr` | `guarda` | ✅ correcto, sin aviso |
| [`f_vector_insert_end_ptr_bucle_reserva`](#f_vector_insert_end_ptr_bucle_reserva) | `vector` | `insert_end` | `ptr` | `bucle` | ✅ correcto, sin aviso |
| [`f_vector_insert_end_ptr_llamada_reserva`](#f_vector_insert_end_ptr_llamada_reserva) | `vector` | `insert_end` | `ptr` | `llamada` | ✅ correcto, sin aviso |
| [`f_uset_insert_it_recto_reserva`](#f_uset_insert_it_recto_reserva) | `uset` | `insert` | `it` | `recto` | ✅ correcto, sin aviso |
| [`f_uset_insert_it_guarda_reserva`](#f_uset_insert_it_guarda_reserva) | `uset` | `insert` | `it` | `guarda` | ✅ correcto, sin aviso |
| [`f_uset_insert_it_bucle_reserva`](#f_uset_insert_it_bucle_reserva) | `uset` | `insert` | `it` | `bucle` | ✅ correcto, sin aviso |
| [`f_uset_insert_it_llamada_reserva`](#f_uset_insert_it_llamada_reserva) | `uset` | `insert` | `it` | `llamada` | ✅ correcto, sin aviso |
| [`f_uset_insert_ref_bucle_reserva`](#f_uset_insert_ref_bucle_reserva) | `uset` | `insert` | `ref` | `bucle` | ✅ correcto, sin aviso |
| [`f_uset_insert_ptr_bucle_reserva`](#f_uset_insert_ptr_bucle_reserva) | `uset` | `insert` | `ptr` | `bucle` | ✅ correcto, sin aviso |
| [`f_umap_insert_it_recto_reserva`](#f_umap_insert_it_recto_reserva) | `umap` | `insert` | `it` | `recto` | ✅ correcto, sin aviso |
| [`f_umap_insert_it_guarda_reserva`](#f_umap_insert_it_guarda_reserva) | `umap` | `insert` | `it` | `guarda` | ✅ correcto, sin aviso |
| [`f_umap_insert_it_bucle_reserva`](#f_umap_insert_it_bucle_reserva) | `umap` | `insert` | `it` | `bucle` | ✅ correcto, sin aviso |
| [`f_umap_insert_it_llamada_reserva`](#f_umap_insert_it_llamada_reserva) | `umap` | `insert` | `it` | `llamada` | ✅ correcto, sin aviso |
| [`f_umap_insert_ref_bucle_reserva`](#f_umap_insert_ref_bucle_reserva) | `umap` | `insert` | `ref` | `bucle` | ✅ correcto, sin aviso |
| [`f_umap_insert_ptr_bucle_reserva`](#f_umap_insert_ptr_bucle_reserva) | `umap` | `insert` | `ptr` | `bucle` | ✅ correcto, sin aviso |
| [`f_umap_subscript_it_recto_reserva`](#f_umap_subscript_it_recto_reserva) | `umap` | `subscript` | `it` | `recto` | ✅ correcto, sin aviso |
| [`f_umap_subscript_it_guarda_reserva`](#f_umap_subscript_it_guarda_reserva) | `umap` | `subscript` | `it` | `guarda` | ✅ correcto, sin aviso |
| [`f_umap_subscript_it_bucle_reserva`](#f_umap_subscript_it_bucle_reserva) | `umap` | `subscript` | `it` | `bucle` | ✅ correcto, sin aviso |
| [`f_umap_subscript_it_llamada_reserva`](#f_umap_subscript_it_llamada_reserva) | `umap` | `subscript` | `it` | `llamada` | ✅ correcto, sin aviso |
| [`f_umap_subscript_ref_bucle_reserva`](#f_umap_subscript_ref_bucle_reserva) | `umap` | `subscript` | `ref` | `bucle` | ✅ correcto, sin aviso |
| [`f_umap_subscript_ptr_bucle_reserva`](#f_umap_subscript_ptr_bucle_reserva) | `umap` | `subscript` | `ptr` | `bucle` | ✅ correcto, sin aviso |

### f_vector_push_back_it_recto_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_vector_push_back_it_recto_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  c.push_back(1);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_vector_push_back_it_guarda_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_vector_push_back_it_guarda_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  c.push_back(1);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_vector_push_back_it_bucle_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_vector_push_back_it_bucle_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 3);
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.push_back(1);
    sink(*it);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_vector_push_back_it_llamada_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_vector_push_back_it_llamada_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_vector_push_back(c);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_vector_push_back_ref_recto_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_vector_push_back_ref_recto_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  const auto& h = *it;
  c.push_back(1);
  sink(h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_vector_push_back_ref_guarda_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_vector_push_back_ref_guarda_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.push_back(1);
  sink(h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_vector_push_back_ref_bucle_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_vector_push_back_ref_bucle_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 3);
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.push_back(1);
    sink(h);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_vector_push_back_ref_llamada_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_vector_push_back_ref_llamada_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_vector_push_back(c);
  sink(h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_vector_push_back_ptr_recto_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_vector_push_back_ptr_recto_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  const auto* h = &*it;
  c.push_back(1);
  sink(*h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_vector_push_back_ptr_guarda_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_vector_push_back_ptr_guarda_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.push_back(1);
  sink(*h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_vector_push_back_ptr_bucle_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_vector_push_back_ptr_bucle_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 3);
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.push_back(1);
    sink(*h);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_vector_push_back_ptr_llamada_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_vector_push_back_ptr_llamada_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_vector_push_back(c);
  sink(*h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_vector_emplace_back_it_recto_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_vector_emplace_back_it_recto_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  c.emplace_back(1);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_vector_emplace_back_it_guarda_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_vector_emplace_back_it_guarda_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  c.emplace_back(1);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_vector_emplace_back_it_bucle_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_vector_emplace_back_it_bucle_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 3);
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.emplace_back(1);
    sink(*it);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_vector_emplace_back_it_llamada_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_vector_emplace_back_it_llamada_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_vector_emplace_back(c);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_vector_emplace_back_ref_recto_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_vector_emplace_back_ref_recto_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  const auto& h = *it;
  c.emplace_back(1);
  sink(h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_vector_emplace_back_ref_guarda_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_vector_emplace_back_ref_guarda_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.emplace_back(1);
  sink(h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_vector_emplace_back_ref_bucle_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_vector_emplace_back_ref_bucle_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 3);
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.emplace_back(1);
    sink(h);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_vector_emplace_back_ref_llamada_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_vector_emplace_back_ref_llamada_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_vector_emplace_back(c);
  sink(h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_vector_emplace_back_ptr_recto_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_vector_emplace_back_ptr_recto_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  const auto* h = &*it;
  c.emplace_back(1);
  sink(*h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_vector_emplace_back_ptr_guarda_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_vector_emplace_back_ptr_guarda_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.emplace_back(1);
  sink(*h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_vector_emplace_back_ptr_bucle_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_vector_emplace_back_ptr_bucle_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 3);
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.emplace_back(1);
    sink(*h);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_vector_emplace_back_ptr_llamada_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_vector_emplace_back_ptr_llamada_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_vector_emplace_back(c);
  sink(*h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_vector_insert_end_it_recto_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_vector_insert_end_it_recto_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  c.insert(c.end(),1);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_vector_insert_end_it_guarda_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_vector_insert_end_it_guarda_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  c.insert(c.end(),1);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_vector_insert_end_it_bucle_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_vector_insert_end_it_bucle_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 3);
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.insert(c.end(),1);
    sink(*it);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_vector_insert_end_it_llamada_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_vector_insert_end_it_llamada_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_vector_insert_end(c);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_vector_insert_end_ref_recto_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_vector_insert_end_ref_recto_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  const auto& h = *it;
  c.insert(c.end(),1);
  sink(h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_vector_insert_end_ref_guarda_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_vector_insert_end_ref_guarda_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.insert(c.end(),1);
  sink(h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_vector_insert_end_ref_bucle_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_vector_insert_end_ref_bucle_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 3);
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.insert(c.end(),1);
    sink(h);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_vector_insert_end_ref_llamada_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_vector_insert_end_ref_llamada_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_vector_insert_end(c);
  sink(h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_vector_insert_end_ptr_recto_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_vector_insert_end_ptr_recto_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  const auto* h = &*it;
  c.insert(c.end(),1);
  sink(*h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_vector_insert_end_ptr_guarda_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_vector_insert_end_ptr_guarda_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.insert(c.end(),1);
  sink(*h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_vector_insert_end_ptr_bucle_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_vector_insert_end_ptr_bucle_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 3);
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.insert(c.end(),1);
    sink(*h);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_vector_insert_end_ptr_llamada_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_vector_insert_end_ptr_llamada_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_vector_insert_end(c);
  sink(*h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_uset_insert_it_recto_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_uset_insert_it_recto_reserva(std::unordered_set<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  c.insert(99);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_uset_insert_it_guarda_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_uset_insert_it_guarda_reserva(std::unordered_set<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  c.insert(99);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_uset_insert_it_bucle_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_uset_insert_it_bucle_reserva(std::unordered_set<int>& c) {
  c.reserve(c.size() + 3);
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.insert(99);
    sink(*it);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_uset_insert_it_llamada_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_uset_insert_it_llamada_reserva(std::unordered_set<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_uset_insert(c);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_uset_insert_ref_bucle_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_uset_insert_ref_bucle_reserva(std::unordered_set<int>& c) {
  c.reserve(c.size() + 3);
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
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_uset_insert_ptr_bucle_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_uset_insert_ptr_bucle_reserva(std::unordered_set<int>& c) {
  c.reserve(c.size() + 3);
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
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_umap_insert_it_recto_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_umap_insert_it_recto_reserva(std::unordered_map<int,int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  c.insert({99,1});
  sink(it->second);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_umap_insert_it_guarda_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_umap_insert_it_guarda_reserva(std::unordered_map<int,int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  c.insert({99,1});
  sink(it->second);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_umap_insert_it_bucle_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_umap_insert_it_bucle_reserva(std::unordered_map<int,int>& c) {
  c.reserve(c.size() + 3);
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.insert({99,1});
    sink(it->second);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_umap_insert_it_llamada_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_umap_insert_it_llamada_reserva(std::unordered_map<int,int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_umap_insert(c);
  sink(it->second);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_umap_insert_ref_bucle_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_umap_insert_ref_bucle_reserva(std::unordered_map<int,int>& c) {
  c.reserve(c.size() + 3);
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
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_umap_insert_ptr_bucle_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_umap_insert_ptr_bucle_reserva(std::unordered_map<int,int>& c) {
  c.reserve(c.size() + 3);
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
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_umap_subscript_it_recto_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_umap_subscript_it_recto_reserva(std::unordered_map<int,int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  c[97]=1;
  sink(it->second);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_umap_subscript_it_guarda_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_umap_subscript_it_guarda_reserva(std::unordered_map<int,int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  c[97]=1;
  sink(it->second);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_umap_subscript_it_bucle_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_umap_subscript_it_bucle_reserva(std::unordered_map<int,int>& c) {
  c.reserve(c.size() + 3);
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c[97]=1;
    sink(it->second);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_umap_subscript_it_llamada_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_umap_subscript_it_llamada_reserva(std::unordered_map<int,int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_umap_subscript(c);
  sink(it->second);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_umap_subscript_ref_bucle_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_umap_subscript_ref_bucle_reserva(std::unordered_map<int,int>& c) {
  c.reserve(c.size() + 3);
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
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_umap_subscript_ptr_bucle_reserva

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_umap_subscript_ptr_bucle_reserva(std::unordered_map<int,int>& c) {
  c.reserve(c.size() + 3);
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
| `natural` | estado inicial ordinario | sin detección | sin detección |

## `devuelto`: se usa el iterador que devuelve la mutación

12 casos; con aviso estático: 0.

| Caso | Contenedor | Operación | Sostiene | Forma | Estático |
|---|---|---|---|---|---|
| [`f_vector_erase_ret_it_bucle`](#f_vector_erase_ret_it_bucle) | `vector` | `erase_ret` | `it` | `bucle` | ✅ correcto, sin aviso |
| [`f_deque_erase_ret_it_bucle`](#f_deque_erase_ret_it_bucle) | `deque` | `erase_ret` | `it` | `bucle` | ✅ correcto, sin aviso |
| [`f_list_erase_ret_it_bucle`](#f_list_erase_ret_it_bucle) | `list` | `erase_ret` | `it` | `bucle` | ✅ correcto, sin aviso |
| [`f_set_erase_ret_it_bucle`](#f_set_erase_ret_it_bucle) | `set` | `erase_ret` | `it` | `bucle` | ✅ correcto, sin aviso |
| [`f_mset_erase_ret_it_bucle`](#f_mset_erase_ret_it_bucle) | `mset` | `erase_ret` | `it` | `bucle` | ✅ correcto, sin aviso |
| [`f_map_erase_ret_it_bucle`](#f_map_erase_ret_it_bucle) | `map` | `erase_ret` | `it` | `bucle` | ✅ correcto, sin aviso |
| [`f_mmap_erase_ret_it_bucle`](#f_mmap_erase_ret_it_bucle) | `mmap` | `erase_ret` | `it` | `bucle` | ✅ correcto, sin aviso |
| [`f_uset_erase_ret_it_bucle`](#f_uset_erase_ret_it_bucle) | `uset` | `erase_ret` | `it` | `bucle` | ✅ correcto, sin aviso |
| [`f_umap_erase_ret_it_bucle`](#f_umap_erase_ret_it_bucle) | `umap` | `erase_ret` | `it` | `bucle` | ✅ correcto, sin aviso |
| [`f_vector_insert_ret_it_bucle`](#f_vector_insert_ret_it_bucle) | `vector` | `insert_ret` | `it` | `bucle` | ✅ correcto, sin aviso |
| [`f_deque_insert_ret_it_bucle`](#f_deque_insert_ret_it_bucle) | `deque` | `insert_ret` | `it` | `bucle` | ✅ correcto, sin aviso |
| [`f_list_insert_ret_it_bucle`](#f_list_insert_ret_it_bucle) | `list` | `insert_ret` | `it` | `bucle` | ✅ correcto, sin aviso |

### f_vector_erase_ret_it_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_vector_erase_ret_it_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3;) {
    it = c.erase(it);
    if (it != c.end()) sink(*it);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_deque_erase_ret_it_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_deque_erase_ret_it_bucle(std::deque<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3;) {
    it = c.erase(it);
    if (it != c.end()) sink(*it);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_list_erase_ret_it_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_list_erase_ret_it_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3;) {
    it = c.erase(it);
    if (it != c.end()) sink(*it);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_set_erase_ret_it_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_set_erase_ret_it_bucle(std::set<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3;) {
    it = c.erase(it);
    if (it != c.end()) sink(*it);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_mset_erase_ret_it_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_mset_erase_ret_it_bucle(std::multiset<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3;) {
    it = c.erase(it);
    if (it != c.end()) sink(*it);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_map_erase_ret_it_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_map_erase_ret_it_bucle(std::map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3;) {
    it = c.erase(it);
    if (it != c.end()) sink(it->second);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_mmap_erase_ret_it_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_mmap_erase_ret_it_bucle(std::multimap<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3;) {
    it = c.erase(it);
    if (it != c.end()) sink(it->second);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_uset_erase_ret_it_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_uset_erase_ret_it_bucle(std::unordered_set<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3;) {
    it = c.erase(it);
    if (it != c.end()) sink(*it);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_umap_erase_ret_it_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_umap_erase_ret_it_bucle(std::unordered_map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3;) {
    it = c.erase(it);
    if (it != c.end()) sink(it->second);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_vector_insert_ret_it_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_vector_insert_ret_it_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3;) {
    it = c.insert(it, 1); ++it;
    if (it != c.end()) sink(*it);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_deque_insert_ret_it_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_deque_insert_ret_it_bucle(std::deque<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3;) {
    it = c.insert(it, 1); ++it;
    if (it != c.end()) sink(*it);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_list_insert_ret_it_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_list_insert_ret_it_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3;) {
    it = c.insert(it, 1); ++it;
    if (it != c.end()) sink(*it);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |
