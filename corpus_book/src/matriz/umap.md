# Matriz: `std::unordered_map`

## it_umap_insert

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `insert` | iterador | 🟡 `POLICY` | no | silencio (optimista) |

```cpp
void it_umap_insert(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.insert({99, 1});
  sink(it->second);
}
```

## rf_umap_insert

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `insert` | referencia | 🟢 `SAFE` | no | correcto |

```cpp
void rf_umap_insert(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = it->second;
  c.insert({99, 1});
  sink(r);
}
```

## it_umap_subscript

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `subscript` | iterador | 🟡 `POLICY` | no | silencio (optimista) |

```cpp
void it_umap_subscript(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c[97] = 1;
  sink(it->second);
}
```

## rf_umap_subscript

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `subscript` | referencia | 🟢 `SAFE` | no | correcto |

```cpp
void rf_umap_subscript(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = it->second;
  c[97] = 1;
  sink(r);
}
```

## it_umap_erase_begin

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `erase_begin` | iterador | 🔴 `UB` | no | FALSO NEGATIVO |

```cpp
void it_umap_erase_begin(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.erase(c.begin());
  sink(it->second);
}
```

## rf_umap_erase_begin

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `erase_begin` | referencia | 🔴 `UB` | no | FALSO NEGATIVO |

```cpp
void rf_umap_erase_begin(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = it->second;
  c.erase(c.begin());
  sink(r);
}
```

## it_umap_clear

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `clear` | iterador | 🔴 `UB` | sí | detectado |

```cpp
void it_umap_clear(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.clear();
  sink(it->second);
}
```

## rf_umap_clear

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `clear` | referencia | 🔴 `UB` | no | FALSO NEGATIVO |

```cpp
void rf_umap_clear(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = it->second;
  c.clear();
  sink(r);
}
```

## it_umap_rehash

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `rehash` | iterador | 🔴 `UB` | no | FALSO NEGATIVO |

```cpp
void it_umap_rehash(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.rehash(1024);
  sink(it->second);
}
```

## rf_umap_rehash

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `rehash` | referencia | 🟢 `SAFE` | no | correcto |

```cpp
void rf_umap_rehash(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = it->second;
  c.rehash(1024);
  sink(r);
}
```
