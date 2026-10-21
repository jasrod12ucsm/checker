# `std::unordered_map::subscript`

Mutación: `c[97]=1;`

- Iterador retenido: 🟡 `POLICY`
- Referencia/puntero retenido: 🟢 `SAFE`
- Casos `UB` detectados estáticamente: 0/0

**En palabras:** después de `c[97]=1;` sobre un `std::unordered_map`, un iterador guardado **puede** quedar inválido según el estado del contenedor (capacidad o factor de carga); una referencia o puntero guardado sigue siendo **válido**: usarlo después es correcto.

Mapa de los 12 casos. Cada celda muestra la respuesta correcta (etiqueta) y, debajo, lo que hizo el analizador estático de Clang. Clic para ir al caso. Ver [Cómo leer este libro](../../guia.md).

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_umap_subscript_it_recto) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_umap_subscript_it_guarda) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_umap_subscript_it_bucle) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_umap_subscript_it_llamada) |
| **referencia** | [🟢 `SAFE`<br>✅ correcto, sin aviso](#f_umap_subscript_ref_recto) | [🟢 `SAFE`<br>✅ correcto, sin aviso](#f_umap_subscript_ref_guarda) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_umap_subscript_ref_bucle) | [🟢 `SAFE`<br>✅ correcto, sin aviso](#f_umap_subscript_ref_llamada) |
| **puntero** | [🟢 `SAFE`<br>✅ correcto, sin aviso](#f_umap_subscript_ptr_recto) | [🟢 `SAFE`<br>✅ correcto, sin aviso](#f_umap_subscript_ptr_guarda) | [🟡 `POLICY`<br>⚪ sin aviso (depende del estado)](#f_umap_subscript_ptr_bucle) | [🟢 `SAFE`<br>✅ correcto, sin aviso](#f_umap_subscript_ptr_llamada) |

## Handle: iterador

### f_umap_subscript_it_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `recto` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_umap_subscript_it_recto(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  c[97]=1;
  sink(it->second);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | factor de carga alcanzado; la inserción dispara rehash | sin detección | sin detección |
| `preserve` | reserve(256), sin rehash para la inserción evaluada | sin detección | sin detección |

### f_umap_subscript_it_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `guarda` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_umap_subscript_it_guarda(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c[97]=1;
  sink(it->second);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | factor de carga alcanzado; la inserción dispara rehash | sin detección | sin detección |
| `preserve` | reserve(256), sin rehash para la inserción evaluada | sin detección | sin detección |

### f_umap_subscript_it_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_umap_subscript_it_bucle(std::unordered_map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c[97]=1;
    sink(it->second);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | factor de carga alcanzado; la inserción dispara rehash | sin detección | sin detección |
| `preserve` | reserve(256), sin rehash para la inserción evaluada | sin detección | sin detección |

### f_umap_subscript_it_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `llamada` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_umap_subscript_it_llamada(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_umap_subscript(c);
  sink(it->second);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `force` | factor de carga alcanzado; la inserción dispara rehash | sin detección | sin detección |
| `preserve` | reserve(256), sin rehash para la inserción evaluada | sin detección | sin detección |

## Handle: referencia

### f_umap_subscript_ref_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_umap_subscript_ref_recto(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c[97]=1;
  sink(h.second);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_umap_subscript_ref_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_umap_subscript_ref_guarda(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c[97]=1;
  sink(h.second);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_umap_subscript_ref_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_umap_subscript_ref_bucle(std::unordered_map<int,int>& c) {
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
| `force` | factor de carga alcanzado; la inserción dispara rehash | sin detección | sin detección |
| `preserve` | reserve(256), sin rehash para la inserción evaluada | sin detección | sin detección |

### f_umap_subscript_ref_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_umap_subscript_ref_llamada(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_umap_subscript(c);
  sink(h.second);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

## Handle: puntero

### f_umap_subscript_ptr_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_umap_subscript_ptr_recto(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c[97]=1;
  sink(h->second);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_umap_subscript_ptr_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_umap_subscript_ptr_guarda(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c[97]=1;
  sink(h->second);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_umap_subscript_ptr_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `bucle` | 🟡 `POLICY` | ⚪ sin aviso (depende del estado) | ⚪ aviso posible |

```cpp
void f_umap_subscript_ptr_bucle(std::unordered_map<int,int>& c) {
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
| `force` | factor de carga alcanzado; la inserción dispara rehash | sin detección | sin detección |
| `preserve` | reserve(256), sin rehash para la inserción evaluada | sin detección | sin detección |

### f_umap_subscript_ptr_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_umap_subscript_ptr_llamada(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_umap_subscript(c);
  sink(h->second);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |
