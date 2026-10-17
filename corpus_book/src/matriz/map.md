# Matriz: `std::map`

## it_map_insert

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `insert` | iterador | 🟢 `SAFE` | no | correcto |

```cpp
void it_map_insert(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.insert({99, 1});
  sink(it->second);
}
```

## rf_map_insert

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `insert` | referencia | 🟢 `SAFE` | no | correcto |

```cpp
void rf_map_insert(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = it->second;
  c.insert({99, 1});
  sink(r);
}
```

## it_map_emplace

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `emplace` | iterador | 🟢 `SAFE` | no | correcto |

```cpp
void it_map_emplace(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.emplace(98, 1);
  sink(it->second);
}
```

## rf_map_emplace

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `emplace` | referencia | 🟢 `SAFE` | no | correcto |

```cpp
void rf_map_emplace(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = it->second;
  c.emplace(98, 1);
  sink(r);
}
```

## it_map_subscript

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `subscript` | iterador | 🟢 `SAFE` | no | correcto |

```cpp
void it_map_subscript(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c[97] = 1;
  sink(it->second);
}
```

## rf_map_subscript

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `subscript` | referencia | 🟢 `SAFE` | no | correcto |

```cpp
void rf_map_subscript(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = it->second;
  c[97] = 1;
  sink(r);
}
```

## it_map_erase_begin

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `erase_begin` | iterador | 🔴 `UB` | no | FALSO NEGATIVO |

```cpp
void it_map_erase_begin(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.erase(c.begin());
  sink(it->second);
}
```

## rf_map_erase_begin

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `erase_begin` | referencia | 🔴 `UB` | no | FALSO NEGATIVO |

```cpp
void rf_map_erase_begin(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = it->second;
  c.erase(c.begin());
  sink(r);
}
```

## it_map_clear

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `clear` | iterador | 🔴 `UB` | sí | detectado |

```cpp
void it_map_clear(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.clear();
  sink(it->second);
}
```

## rf_map_clear

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `clear` | referencia | 🔴 `UB` | no | FALSO NEGATIVO |

```cpp
void rf_map_clear(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = it->second;
  c.clear();
  sink(r);
}
```
