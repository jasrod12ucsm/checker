# Matriz: `std::list`

## it_list_push_back

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `push_back` | iterador | 🟢 `SAFE` | no | correcto |

```cpp
void it_list_push_back(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.push_back(1);
  sink(*it);
}
```

## rf_list_push_back

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `push_back` | referencia | 🟢 `SAFE` | no | correcto |

```cpp
void rf_list_push_back(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.push_back(1);
  sink(r);
}
```

## it_list_push_front

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `push_front` | iterador | 🟢 `SAFE` | no | correcto |

```cpp
void it_list_push_front(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.push_front(1);
  sink(*it);
}
```

## rf_list_push_front

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `push_front` | referencia | 🟢 `SAFE` | no | correcto |

```cpp
void rf_list_push_front(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.push_front(1);
  sink(r);
}
```

## it_list_insert

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `insert` | iterador | 🟢 `SAFE` | no | correcto |

```cpp
void it_list_insert(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.insert(c.begin(), 1);
  sink(*it);
}
```

## rf_list_insert

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `insert` | referencia | 🟢 `SAFE` | no | correcto |

```cpp
void rf_list_insert(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.insert(c.begin(), 1);
  sink(r);
}
```

## it_list_erase_begin

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `erase_begin` | iterador | 🔴 `UB` | no | FALSO NEGATIVO |

```cpp
void it_list_erase_begin(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.erase(c.begin());
  sink(*it);
}
```

## rf_list_erase_begin

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `erase_begin` | referencia | 🔴 `UB` | no | FALSO NEGATIVO |

```cpp
void rf_list_erase_begin(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.erase(c.begin());
  sink(r);
}
```

## it_list_clear

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `clear` | iterador | 🔴 `UB` | sí | detectado |

```cpp
void it_list_clear(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.clear();
  sink(*it);
}
```

## rf_list_clear

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `clear` | referencia | 🔴 `UB` | no | FALSO NEGATIVO |

```cpp
void rf_list_clear(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.clear();
  sink(r);
}
```

## it_list_resize_grow

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `resize_grow` | iterador | 🟢 `SAFE` | no | correcto |

```cpp
void it_list_resize_grow(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.resize(c.size() + 100);
  sink(*it);
}
```

## rf_list_resize_grow

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `resize_grow` | referencia | 🟢 `SAFE` | no | correcto |

```cpp
void rf_list_resize_grow(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.resize(c.size() + 100);
  sink(r);
}
```

## it_list_pop_front

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `pop_front` | iterador | 🔴 `UB` | no | FALSO NEGATIVO |

```cpp
void it_list_pop_front(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.pop_front();
  sink(*it);
}
```

## rf_list_pop_front

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `pop_front` | referencia | 🔴 `UB` | no | FALSO NEGATIVO |

```cpp
void rf_list_pop_front(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.pop_front();
  sink(r);
}
```

## it_list_reverse

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `reverse` | iterador | 🟢 `SAFE` | no | correcto |

```cpp
void it_list_reverse(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.reverse();
  sink(*it);
}
```

## rf_list_reverse

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `reverse` | referencia | 🟢 `SAFE` | no | correcto |

```cpp
void rf_list_reverse(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.reverse();
  sink(r);
}
```
