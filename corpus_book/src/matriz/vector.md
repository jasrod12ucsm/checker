# Matriz: `std::vector`

## it_vector_push_back

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `push_back` | iterador | 🟡 `POLICY` | no | silencio (optimista) |

```cpp
void it_vector_push_back(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.push_back(1);
  sink(*it);
}
```

## rf_vector_push_back

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `push_back` | referencia | 🟡 `POLICY` | no | silencio (optimista) |

```cpp
void rf_vector_push_back(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.push_back(1);
  sink(r);
}
```

## it_vector_emplace_back

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `emplace_back` | iterador | 🟡 `POLICY` | no | silencio (optimista) |

```cpp
void it_vector_emplace_back(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.emplace_back(1);
  sink(*it);
}
```

## rf_vector_emplace_back

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `emplace_back` | referencia | 🟡 `POLICY` | no | silencio (optimista) |

```cpp
void rf_vector_emplace_back(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.emplace_back(1);
  sink(r);
}
```

## it_vector_insert_begin

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `insert_begin` | iterador | 🔴 `UB` | no | FALSO NEGATIVO |

```cpp
void it_vector_insert_begin(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.insert(c.begin(), 1);
  sink(*it);
}
```

## rf_vector_insert_begin

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `insert_begin` | referencia | 🔴 `UB` | no | FALSO NEGATIVO |

```cpp
void rf_vector_insert_begin(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.insert(c.begin(), 1);
  sink(r);
}
```

## it_vector_insert_end

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `insert_end` | iterador | 🟡 `POLICY` | no | silencio (optimista) |

```cpp
void it_vector_insert_end(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.insert(c.end(), 1);
  sink(*it);
}
```

## rf_vector_insert_end

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `insert_end` | referencia | 🟡 `POLICY` | no | silencio (optimista) |

```cpp
void rf_vector_insert_end(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.insert(c.end(), 1);
  sink(r);
}
```

## it_vector_erase_begin

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `erase_begin` | iterador | 🔴 `UB` | no | FALSO NEGATIVO |

```cpp
void it_vector_erase_begin(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.erase(c.begin());
  sink(*it);
}
```

## rf_vector_erase_begin

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `erase_begin` | referencia | 🔴 `UB` | no | FALSO NEGATIVO |

```cpp
void rf_vector_erase_begin(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.erase(c.begin());
  sink(r);
}
```

## it_vector_clear

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `clear` | iterador | 🔴 `UB` | sí | detectado |

```cpp
void it_vector_clear(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.clear();
  sink(*it);
}
```

## rf_vector_clear

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `clear` | referencia | 🔴 `UB` | no | FALSO NEGATIVO |

```cpp
void rf_vector_clear(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.clear();
  sink(r);
}
```

## it_vector_resize_grow

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `resize_grow` | iterador | 🟡 `POLICY` | no | silencio (optimista) |

```cpp
void it_vector_resize_grow(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.resize(c.size() + 100);
  sink(*it);
}
```

## rf_vector_resize_grow

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `resize_grow` | referencia | 🟡 `POLICY` | no | silencio (optimista) |

```cpp
void rf_vector_resize_grow(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.resize(c.size() + 100);
  sink(r);
}
```

## it_vector_reserve

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `reserve` | iterador | 🟡 `POLICY` | no | silencio (optimista) |

```cpp
void it_vector_reserve(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.reserve(c.size() + 100);
  sink(*it);
}
```

## rf_vector_reserve

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `reserve` | referencia | 🟡 `POLICY` | no | silencio (optimista) |

```cpp
void rf_vector_reserve(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.reserve(c.size() + 100);
  sink(r);
}
```

## it_vector_shrink_to_fit

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `shrink_to_fit` | iterador | 🟡 `POLICY` | no | silencio (optimista) |

```cpp
void it_vector_shrink_to_fit(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.shrink_to_fit();
  sink(*it);
}
```

## rf_vector_shrink_to_fit

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `shrink_to_fit` | referencia | 🟡 `POLICY` | no | silencio (optimista) |

```cpp
void rf_vector_shrink_to_fit(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.shrink_to_fit();
  sink(r);
}
```

## it_vector_assign

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `assign` | iterador | 🔴 `UB` | sí | detectado |

```cpp
void it_vector_assign(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.assign(3, 7);
  sink(*it);
}
```

## rf_vector_assign

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `assign` | referencia | 🔴 `UB` | no | FALSO NEGATIVO |

```cpp
void rf_vector_assign(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.assign(3, 7);
  sink(r);
}
```

## it_vector_pop_back

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `pop_back` | iterador | 🟡 `POLICY` | no | silencio (optimista) |

```cpp
void it_vector_pop_back(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.pop_back();
  sink(*it);
}
```

## rf_vector_pop_back

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `pop_back` | referencia | 🟡 `POLICY` | no | silencio (optimista) |

```cpp
void rf_vector_pop_back(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.pop_back();
  sink(r);
}
```
