# `std::set::emplace`

Mutación: `c.emplace(98);`

- Iterador retenido: 🟢 `SAFE`
- Referencia/puntero retenido: 🟢 `SAFE`
- Casos `UB` detectados estáticamente: 0/0

**En palabras:** después de `c.emplace(98);` sobre un `std::set`, un iterador guardado sigue siendo **válido**: usarlo después es correcto; una referencia o puntero guardado sigue siendo **válido**: usarlo después es correcto.

Mapa de los 12 casos. Cada celda muestra la respuesta correcta (etiqueta) y, debajo, lo que hizo el analizador estático de Clang. Clic para ir al caso. Ver [Cómo leer este libro](../../guia.md).

| | `recto` | `guarda` | `bucle` | `llamada` |
|---|---|---|---|---|
| **iterador** | [🟢 `SAFE`<br>✅ correcto, sin aviso](#f_set_emplace_it_recto) | [🟢 `SAFE`<br>✅ correcto, sin aviso](#f_set_emplace_it_guarda) | [🟢 `SAFE`<br>✅ correcto, sin aviso](#f_set_emplace_it_bucle) | [🟢 `SAFE`<br>✅ correcto, sin aviso](#f_set_emplace_it_llamada) |
| **referencia** | [🟢 `SAFE`<br>✅ correcto, sin aviso](#f_set_emplace_ref_recto) | [🟢 `SAFE`<br>✅ correcto, sin aviso](#f_set_emplace_ref_guarda) | [🟢 `SAFE`<br>✅ correcto, sin aviso](#f_set_emplace_ref_bucle) | [🟢 `SAFE`<br>✅ correcto, sin aviso](#f_set_emplace_ref_llamada) |
| **puntero** | [🟢 `SAFE`<br>✅ correcto, sin aviso](#f_set_emplace_ptr_recto) | [🟢 `SAFE`<br>✅ correcto, sin aviso](#f_set_emplace_ptr_guarda) | [🟢 `SAFE`<br>✅ correcto, sin aviso](#f_set_emplace_ptr_bucle) | [🟢 `SAFE`<br>✅ correcto, sin aviso](#f_set_emplace_ptr_llamada) |

## Handle: iterador

### f_set_emplace_it_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_set_emplace_it_recto(std::set<int>& c) {
  auto it = c.begin();
  c.emplace(98);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_set_emplace_it_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_set_emplace_it_guarda(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.emplace(98);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_set_emplace_it_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_set_emplace_it_bucle(std::set<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.emplace(98);
    sink(*it);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_set_emplace_it_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| iterador | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_set_emplace_it_llamada(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_set_emplace(c);
  sink(*it);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

## Handle: referencia

### f_set_emplace_ref_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_set_emplace_ref_recto(std::set<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.emplace(98);
  sink(h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_set_emplace_ref_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_set_emplace_ref_guarda(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.emplace(98);
  sink(h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_set_emplace_ref_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_set_emplace_ref_bucle(std::set<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.emplace(98);
    sink(h);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_set_emplace_ref_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| referencia | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_set_emplace_ref_llamada(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_set_emplace(c);
  sink(h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

## Handle: puntero

### f_set_emplace_ptr_recto

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `recto` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_set_emplace_ptr_recto(std::set<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.emplace(98);
  sink(*h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_set_emplace_ptr_guarda

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `guarda` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_set_emplace_ptr_guarda(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.emplace(98);
  sink(*h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_set_emplace_ptr_bucle

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `bucle` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_set_emplace_ptr_bucle(std::set<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.emplace(98);
    sink(*h);
  }
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |

### f_set_emplace_ptr_llamada

| Handle | Forma | Etiqueta | CSA | Plugin (`Possibly`) |
|---|---|---|---|---|
| puntero | `llamada` | 🟢 `SAFE` | ✅ correcto, sin aviso | ✅ correcto, sin aviso |

```cpp
void f_set_emplace_ptr_llamada(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_set_emplace(c);
  sink(*h);
}
```

| Escenario | Precondición | libstdc++ Debug | ASan/UBSan |
|---|---|---|---|
| `natural` | estado inicial ordinario | sin detección | sin detección |
