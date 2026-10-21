// I4: lo que depende del estado. Aviso posible sin garantía; nada con garantía.
// RUN: %analyze %possibly %s
#include <vector>
#include <unordered_map>

void sink(int);

void no_guarantee(std::vector<int> &c) {
  const int &h = c[0];
  c.push_back(1);
  sink(h); // expected-warning {{Uso de una referencia posiblemente invalidada: 'std::vector::push_back' (línea 10) si la capacidad está agotada reubica los elementos; nada garantiza espacio}}
}

void reserved(std::vector<int> &c) {
  c.reserve(c.size() + 2);
  const int &h = c[0];
  c.push_back(1);
  c.push_back(2);
  sink(h); // sin aviso: reserve garantiza dos inserciones
}

void reserved_too_little(std::vector<int> &c) {
  c.reserve(c.size() + 1);
  const int &h = c[0];
  c.push_back(1);
  c.push_back(2);
  sink(h); // expected-warning {{posiblemente invalidada: 'std::vector::push_back' (línea 26)}}
}

void unordered_iter(std::unordered_map<int, int> &c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c[42] = 1;
  sink(it->second); // expected-warning {{Uso de un iterador posiblemente invalidado}}
}

void unordered_reserved(std::unordered_map<int, int> &c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  c.insert({42, 1});
  sink(it->second); // sin aviso
}

void pop_back_first(std::vector<int> &c) {
  const int &h = c[0];
  c.pop_back();
  sink(h); // expected-warning {{posiblemente invalidada: 'std::vector::pop_back' (línea 47) lo invalida si el elemento está en el punto}}
}

void shrink(std::vector<int> &c) {
  c.reserve(c.size() + 10);
  const int &h = c[0];
  c.shrink_to_fit();
  sink(h); // expected-warning {{posiblemente invalidada: 'std::vector::shrink_to_fit'}}
}

void opaque(std::vector<int> &);
void escaped(std::vector<int> &c) {
  const int &h = c[0];
  opaque(c);
  sink(h); // sin aviso: tras un escape el handle deja de seguirse (D-21)
}

void escaped_after_invalid(std::vector<int> &c) {
  const int &h = c[0];
  c.clear();
  opaque(c);
  sink(h); // expected-warning {{Uso de una referencia invalidada: 'std::vector::clear'}}
}

struct Holder {
  std::vector<int> v;
  void touch();
};
void opaque_this(Holder &o) {
  const int &h = o.v[0];
  o.touch(); // recibe `this`: el campo v escapa
  sink(h); // sin aviso (D-21)
}
