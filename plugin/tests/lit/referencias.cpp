// I2: referencias y punteros obtenidos de *it, &*it, c[i], front(); uso por carga.
// RUN: %analyze %s
#include <vector>
#include <list>
#include <map>
#include <deque>

void sink(int);

void vector_erase_ref(std::vector<int> &c) {
  auto it = c.begin();
  const int &h = *it;
  c.erase(c.begin());
  sink(h); // expected-warning {{Uso de una referencia invalidada: 'std::vector::erase' (línea 13) lo invalidó}}
}

void vector_clear_ptr(std::vector<int> &c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const int *h = &*it;
  c.clear();
  sink(*h); // expected-warning {{Uso de un puntero invalidado}}
}

void list_erase_ref(std::list<int> &c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const int &h = *it;
  c.erase(c.begin());
  sink(h); // expected-warning {{Uso de una referencia invalidada}}
}

void map_erase_field(std::map<int, int> &c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto *h = &*it;
  c.erase(c.begin());
  sink(h->second); // expected-warning {{Uso de un puntero invalidado}}
}

void subscript_and_front(std::vector<int> &c) {
  int &r = c[0];
  int &f = c.front();
  c.assign(3, 7);
  sink(r); // expected-warning {{Uso de una referencia invalidada}}
  sink(f); // expected-warning {{Uso de una referencia invalidada}}
}

void alias(std::vector<int> &c) {
  auto &d = c;
  const int &h = c[0];
  d.clear();
  sink(h); // expected-warning {{Uso de una referencia invalidada}}
}

void deque_insert_interior(std::deque<int> &c) {
  const int &h = c.front();
  c.insert(c.begin() + 1, 1); // en el medio: invalida todo
  sink(h); // expected-warning {{Uso de una referencia invalidada: 'std::deque::insert'}}
}

struct Out { int number; void touch(); };
void keep(const int &);
void use_by_reference(std::vector<Out> &c) {
  Out *first = &c[0];
  c.clear();
  keep(first->number); // expected-warning {{Uso de un puntero invalidado: 'std::vector::clear'}}
}

void use_by_method(std::vector<Out> &c) {
  Out *first = &c[0];
  c.clear();
  first->touch(); // expected-warning {{Uso de un puntero invalidado: 'std::vector::clear'}}
}

void pointer_value_is_not_a_use(std::vector<Out> &c, void (*f)(Out *)) {
  Out *first = &c[0];
  c.clear();
  f(first); // sin aviso: copiar un puntero inválido no es UB en C++17
}

// ── lo que NO se avisa ──────────────────────────────────────────────

void list_insert_preserves(std::list<int> &c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const int &h = *it;
  c.push_back(1);
  c.insert(c.begin(), 2);
  sink(h); // sin aviso: insertar en list no invalida
}

void deque_push_ref_preserved(std::deque<int> &c) {
  const int &h = c.front();
  c.push_back(1);
  sink(h); // sin aviso: deque conserva referencias al insertar en un extremo
}

void other_container(std::vector<int> &a, std::vector<int> &b) {
  const int &h = a[0];
  b.clear();
  sink(h); // sin aviso: otro contenedor
}

void reobtain(std::vector<int> &c) {
  c.clear();
  c.push_back(1);
  const int &h = c[0];
  sink(h); // sin aviso: obtenido después
}

void vector_erase_before_point(std::vector<int> &c) {
  const int &h = c[0];
  c.erase(c.begin() + 2);
  sink(h); // sin aviso: antes del punto del erase
}

void deque_insert_front_ref(std::deque<int> &c) {
  const int &h = c.front();
  c.insert(c.begin(), 1); // en un extremo: las referencias sobreviven (contradicción 5)
  sink(h);
}

void dependent_silent(std::vector<int> &c) {
  const int &h = c[0];
  c.push_back(1);
  sink(h); // PolicyMode=Silent: depende de la capacidad, sin aviso
}

void once(std::vector<int> &c) {
  const int &h = c[0];
  c.clear();
  sink(h); // expected-warning {{Uso de una referencia invalidada}}
  sink(h); // una vez por handle y camino
}
