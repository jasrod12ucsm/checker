// I2/I3: iteradores: uso al desreferenciar, mover, comparar; copia; it = c.erase(it).
// RUN: %analyze %s
#include <vector>
#include <list>
#include <unordered_set>
#include <deque>
#include <iterator>
#include <set>
#include <map>
#include <string>

void sink(int);

void vector_iter_deref(std::vector<int> &c) {
  auto it = c.begin();
  c.insert(c.begin(), 1);
  sink(*it); // expected-warning {{Uso de un iterador invalidado: 'std::vector::insert'}}
}

void deque_iter_push(std::deque<int> &c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.push_front(1);
  ++it; // expected-warning {{Uso de un iterador invalidado}}
}

void copy_carries_state(std::list<int> &c) {
  auto it = c.begin();
  if (it == c.end()) return;
  auto it2 = it;
  c.erase(c.begin());
  sink(*it2); // expected-warning {{Uso de un iterador invalidado}}
}

void loop_erase(std::list<int> &c) {
  for (auto it = c.begin(); it != c.end(); ++it) { // expected-warning {{Uso de un iterador invalidado}}
    c.erase(c.begin());
  }
}

void erase_idiom(std::list<int> &c) {
  for (auto it = c.begin(); it != c.end();) {
    if (*it % 2)
      it = c.erase(it); // sin aviso: el iterador devuelto es válido
    else
      ++it;
  }
}

void erase_idiom_vector(std::vector<int> &c) {
  for (auto it = c.begin(); it != c.end();) {
    if (*it % 2)
      it = c.erase(it); // sin aviso
    else
      ++it;
  }
}

void unordered_ref_survives_rehash(std::unordered_set<int> &c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const int &h = *it;
  c.rehash(1024);
  sink(h); // sin aviso: rehash conserva referencias
  sink(*it); // expected-warning {{Uso de un iterador invalidado}}
}

void list_iter_other_node(std::list<int> &c) {
  auto it = c.begin();
  if (it == c.end()) return;
  ++it;
  if (it == c.end()) return;
  c.erase(c.begin());
  sink(*it); // sin aviso: it apunta al segundo nodo
}

// ── anclas: posiciones relativas sin saber la absoluta ──────────────

void next_idiom(std::list<int> &c, bool (*cond)(int)) {
  auto it = c.begin();
  while (it != c.end()) {
    auto jt = std::next(it);
    if (cond(*it))
      c.erase(it); // sin aviso: jt es el siguiente nodo
    it = jt;
  }
}

void anchored_after(std::list<int> &c, int k) {
  auto it = c.begin();
  std::advance(it, k);
  if (it == c.end()) return;
  auto jt = std::next(it);
  c.erase(it);
  if (jt != c.end()) sink(*jt); // sin aviso: ancla+1 frente a ancla+0
}

void anchored_same(std::list<int> &c, int k) {
  auto it = c.begin();
  std::advance(it, k);
  if (it == c.end()) return;
  auto jt = it;
  c.erase(it);
  sink(*jt); // expected-warning {{Uso de un iterador invalidado: 'std::list::erase'}}
}

void erase_invalid_arg(std::list<int> &c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.clear();
  c.erase(it); // expected-warning {{Uso de un iterador invalidado: 'std::list::clear'}}
}

void find_unrelated(std::set<int> &s) {
  auto a = s.find(1);
  auto b = s.find(2);
  if (a == s.end() || b == s.end()) return;
  s.erase(a);
  sink(*b); // anclas distintas: sin relación conocida (sólo aviso posible, no en Silent)
}

void insert_pair_first(std::map<std::string, int> &m, const std::string &k) {
  auto it = m.find(k);
  if (it == m.end()) {
    it = m.insert(std::make_pair(k, 0)).first;
    m.erase(it);
    sink(it->second); // expected-warning {{Uso de un iterador invalidado: 'std::map::erase'}}
  }
}

// erase(first, last) borra [first, last): last sigue siendo válido en los
// contenedores de nodos (RocksDB, range_tombstone_fragmenter.cc).
void range_erase_keeps_last(std::set<int> &c) {
  for (auto it = c.begin(); it != c.end(); ++it) {
    if (*it > 3) {
      c.erase(c.begin(), it);
      sink(*it); // sin aviso
      return;
    }
  }
}

void range_erase_inside(std::list<int> &c) {
  auto it = c.begin();
  if (it == c.end()) return;
  auto jt = std::next(it, 2);
  c.erase(it, jt);
  sink(*it); // expected-warning {{Uso de un iterador invalidado: 'std::list::erase'}}
}

void range_erase_vector_last(std::vector<int> &c) {
  auto last = c.begin() + 2;
  c.erase(c.begin(), last);
  sink(*last); // expected-warning {{Uso de un iterador invalidado: 'std::vector::erase'}}
}

void range_erase_empty(std::list<int> &c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.erase(it, it); // rango vacío
  sink(*it);       // sin aviso
}

// Un índice constante que no cabe en int64 no aborta el análisis (RocksDB).
void huge_index(std::vector<int> &c) {
  sink(c[static_cast<std::size_t>(-1)]);
}

