# Matriz: `std::deque`

## it_deque_push_back

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `push_back` | iterador | 🔴 `UB` | sí | detectado |

```cpp
void it_deque_push_back(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.push_back(1);
  sink(*it);
}
```

## rf_deque_push_back

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `push_back` | referencia | 🟢 `SAFE` | no | correcto |

```cpp
void rf_deque_push_back(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.push_back(1);
  sink(r);
}
```

## it_deque_push_front

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `push_front` | iterador | 🔴 `UB` | sí | detectado |

```cpp
void it_deque_push_front(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.push_front(1);
  sink(*it);
}
```

## rf_deque_push_front

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `push_front` | referencia | 🟢 `SAFE` | no | correcto |

```cpp
void rf_deque_push_front(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.push_front(1);
  sink(r);
}
```

## it_deque_emplace_back

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `emplace_back` | iterador | 🔴 `UB` | sí | detectado |

```cpp
void it_deque_emplace_back(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.emplace_back(1);
  sink(*it);
}
```

## rf_deque_emplace_back

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `emplace_back` | referencia | 🟢 `SAFE` | no | correcto |

```cpp
void rf_deque_emplace_back(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.emplace_back(1);
  sink(r);
}
```

## it_deque_insert_middle

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `insert_middle` | iterador | 🔴 `UB` | sí | detectado |

```cpp
void it_deque_insert_middle(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.insert(c.begin(), 1);
  sink(*it);
}
```

## rf_deque_insert_middle

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `insert_middle` | referencia | 🔴 `UB` | no | FALSO NEGATIVO |

```cpp
void rf_deque_insert_middle(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.insert(c.begin(), 1);
  sink(r);
}
```

## it_deque_erase_begin

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `erase_begin` | iterador | 🔴 `UB` | sí | detectado |

```cpp
void it_deque_erase_begin(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.erase(c.begin());
  sink(*it);
}
```

## rf_deque_erase_begin

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `erase_begin` | referencia | 🔴 `UB` | no | FALSO NEGATIVO |

```cpp
void rf_deque_erase_begin(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.erase(c.begin());
  sink(r);
}
```

## it_deque_clear

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `clear` | iterador | 🔴 `UB` | sí | detectado |

```cpp
void it_deque_clear(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.clear();
  sink(*it);
}
```

## rf_deque_clear

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `clear` | referencia | 🔴 `UB` | no | FALSO NEGATIVO |

```cpp
void rf_deque_clear(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.clear();
  sink(r);
}
```

## it_deque_resize_grow

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `resize_grow` | iterador | 🔴 `UB` | no | FALSO NEGATIVO |

```cpp
void it_deque_resize_grow(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.resize(c.size() + 100);
  sink(*it);
}
```

## rf_deque_resize_grow

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `resize_grow` | referencia | 🟢 `SAFE` | no | correcto |

```cpp
void rf_deque_resize_grow(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.resize(c.size() + 100);
  sink(r);
}
```

## it_deque_pop_front

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `pop_front` | iterador | 🔴 `UB` | no | FALSO NEGATIVO |

```cpp
void it_deque_pop_front(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.pop_front();
  sink(*it);
}
```

## rf_deque_pop_front

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `pop_front` | referencia | 🔴 `UB` | no | FALSO NEGATIVO |

```cpp
void rf_deque_pop_front(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.pop_front();
  sink(r);
}
```
