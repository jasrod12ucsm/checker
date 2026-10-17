# Matriz: `std::string`

## it_string_push_back

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `push_back` | iterador | 🟡 `POLICY` | no | silencio (optimista) |

```cpp
void it_string_push_back(std::string& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.push_back('x');
  sink(*it);
}
```

## rf_string_push_back

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `push_back` | referencia | 🟡 `POLICY` | no | silencio (optimista) |

```cpp
void rf_string_push_back(std::string& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const char& r = *it;
  c.push_back('x');
  sink(r);
}
```

## it_string_append

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `append` | iterador | 🟡 `POLICY` | no | silencio (optimista) |

```cpp
void it_string_append(std::string& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.append("xyz");
  sink(*it);
}
```

## rf_string_append

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `append` | referencia | 🟡 `POLICY` | no | silencio (optimista) |

```cpp
void rf_string_append(std::string& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const char& r = *it;
  c.append("xyz");
  sink(r);
}
```

## it_string_insert_begin

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `insert_begin` | iterador | 🔴 `UB` | no | FALSO NEGATIVO |

```cpp
void it_string_insert_begin(std::string& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.insert(c.begin(), 'x');
  sink(*it);
}
```

## rf_string_insert_begin

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `insert_begin` | referencia | 🔴 `UB` | no | FALSO NEGATIVO |

```cpp
void rf_string_insert_begin(std::string& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const char& r = *it;
  c.insert(c.begin(), 'x');
  sink(r);
}
```

## it_string_erase_begin

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `erase_begin` | iterador | 🔴 `UB` | no | FALSO NEGATIVO |

```cpp
void it_string_erase_begin(std::string& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.erase(c.begin());
  sink(*it);
}
```

## rf_string_erase_begin

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `erase_begin` | referencia | 🔴 `UB` | no | FALSO NEGATIVO |

```cpp
void rf_string_erase_begin(std::string& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const char& r = *it;
  c.erase(c.begin());
  sink(r);
}
```

## it_string_clear

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `clear` | iterador | 🔴 `UB` | sí | detectado |

```cpp
void it_string_clear(std::string& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.clear();
  sink(*it);
}
```

## rf_string_clear

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `clear` | referencia | 🔴 `UB` | no | FALSO NEGATIVO |

```cpp
void rf_string_clear(std::string& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const char& r = *it;
  c.clear();
  sink(r);
}
```

## it_string_reserve

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `reserve` | iterador | 🟡 `POLICY` | no | silencio (optimista) |

```cpp
void it_string_reserve(std::string& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.reserve(c.size() + 100);
  sink(*it);
}
```

## rf_string_reserve

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `reserve` | referencia | 🟡 `POLICY` | no | silencio (optimista) |

```cpp
void rf_string_reserve(std::string& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const char& r = *it;
  c.reserve(c.size() + 100);
  sink(r);
}
```

## it_string_resize_grow

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `resize_grow` | iterador | 🟡 `POLICY` | no | silencio (optimista) |

```cpp
void it_string_resize_grow(std::string& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.resize(c.size() + 100);
  sink(*it);
}
```

## rf_string_resize_grow

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `resize_grow` | referencia | 🟡 `POLICY` | no | silencio (optimista) |

```cpp
void rf_string_resize_grow(std::string& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const char& r = *it;
  c.resize(c.size() + 100);
  sink(r);
}
```
