# Matriz: `std::set`

## it_set_insert

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `insert` | iterador | 🟢 `SAFE` | no | correcto |

```cpp
void it_set_insert(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.insert(99);
  sink(*it);
}
```

## rf_set_insert

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `insert` | referencia | 🟢 `SAFE` | no | correcto |

```cpp
void rf_set_insert(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.insert(99);
  sink(r);
}
```

## it_set_emplace

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `emplace` | iterador | 🟢 `SAFE` | no | correcto |

```cpp
void it_set_emplace(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.emplace(98);
  sink(*it);
}
```

## rf_set_emplace

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `emplace` | referencia | 🟢 `SAFE` | no | correcto |

```cpp
void rf_set_emplace(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.emplace(98);
  sink(r);
}
```

## it_set_erase_begin

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `erase_begin` | iterador | 🔴 `UB` | no | FALSO NEGATIVO |

```cpp
void it_set_erase_begin(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.erase(c.begin());
  sink(*it);
}
```

## rf_set_erase_begin

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `erase_begin` | referencia | 🔴 `UB` | no | FALSO NEGATIVO |

```cpp
void rf_set_erase_begin(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.erase(c.begin());
  sink(r);
}
```

## it_set_clear

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `clear` | iterador | 🔴 `UB` | sí | detectado |

```cpp
void it_set_clear(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.clear();
  sink(*it);
}
```

## rf_set_clear

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `clear` | referencia | 🔴 `UB` | no | FALSO NEGATIVO |

```cpp
void rf_set_clear(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.clear();
  sink(r);
}
```
