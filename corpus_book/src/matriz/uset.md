# Matriz: `std::unordered_set`

## it_uset_insert

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `insert` | iterador | 🟡 `POLICY` | no | silencio (optimista) |

```cpp
void it_uset_insert(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.insert(99);
  sink(*it);
}
```

## rf_uset_insert

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `insert` | referencia | 🟢 `SAFE` | no | correcto |

```cpp
void rf_uset_insert(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.insert(99);
  sink(r);
}
```

## it_uset_erase_begin

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `erase_begin` | iterador | 🔴 `UB` | no | FALSO NEGATIVO |

```cpp
void it_uset_erase_begin(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.erase(c.begin());
  sink(*it);
}
```

## rf_uset_erase_begin

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `erase_begin` | referencia | 🔴 `UB` | no | FALSO NEGATIVO |

```cpp
void rf_uset_erase_begin(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.erase(c.begin());
  sink(r);
}
```

## it_uset_clear

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `clear` | iterador | 🔴 `UB` | sí | detectado |

```cpp
void it_uset_clear(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.clear();
  sink(*it);
}
```

## rf_uset_clear

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `clear` | referencia | 🔴 `UB` | no | FALSO NEGATIVO |

```cpp
void rf_uset_clear(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.clear();
  sink(r);
}
```

## it_uset_rehash

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `rehash` | iterador | 🔴 `UB` | no | FALSO NEGATIVO |

```cpp
void it_uset_rehash(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.rehash(1024);
  sink(*it);
}
```

## rf_uset_rehash

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `rehash` | referencia | 🟢 `SAFE` | no | correcto |

```cpp
void rf_uset_rehash(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.rehash(1024);
  sink(r);
}
```

## it_uset_reserve

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `reserve` | iterador | 🔴 `UB` | no | FALSO NEGATIVO |

```cpp
void it_uset_reserve(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.reserve(1024);
  sink(*it);
}
```

## rf_uset_reserve

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `reserve` | referencia | 🟢 `SAFE` | no | correcto |

```cpp
void rf_uset_reserve(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.reserve(1024);
  sink(r);
}
```
