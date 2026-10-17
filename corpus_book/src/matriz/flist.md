# Matriz: `std::forward_list`

## it_flist_push_front

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `push_front` | iterador | 🟢 `SAFE` | no | correcto |

```cpp
void it_flist_push_front(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.push_front(1);
  sink(*it);
}
```

## rf_flist_push_front

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `push_front` | referencia | 🟢 `SAFE` | no | correcto |

```cpp
void rf_flist_push_front(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.push_front(1);
  sink(r);
}
```

## it_flist_insert_after

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `insert_after` | iterador | 🟢 `SAFE` | no | correcto |

```cpp
void it_flist_insert_after(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.insert_after(c.before_begin(), 1);
  sink(*it);
}
```

## rf_flist_insert_after

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `insert_after` | referencia | 🟢 `SAFE` | no | correcto |

```cpp
void rf_flist_insert_after(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.insert_after(c.before_begin(), 1);
  sink(r);
}
```

## it_flist_erase_after

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `erase_after` | iterador | 🔴 `UB` | no | FALSO NEGATIVO |

```cpp
void it_flist_erase_after(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.erase_after(c.before_begin());
  sink(*it);
}
```

## rf_flist_erase_after

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `erase_after` | referencia | 🔴 `UB` | no | FALSO NEGATIVO |

```cpp
void rf_flist_erase_after(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.erase_after(c.before_begin());
  sink(r);
}
```

## it_flist_clear

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `clear` | iterador | 🔴 `UB` | sí | detectado |

```cpp
void it_flist_clear(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.clear();
  sink(*it);
}
```

## rf_flist_clear

| Operación | Dominio | Esperado | Aviso | Clasificación |
|---|---|---|---|---|
| `clear` | referencia | 🔴 `UB` | no | FALSO NEGATIVO |

```cpp
void rf_flist_clear(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.clear();
  sink(r);
}
```
