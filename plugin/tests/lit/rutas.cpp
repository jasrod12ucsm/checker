// I5: la ruta del aviso trae obtención → mutación → uso (RF-12).
// RUN: %analyze -Xclang -analyzer-output=text %s
#include <vector>
#include <map>

void sink(int);

void ruta_iterador(std::vector<int> &c) {
  auto it = c.begin(); // expected-note {{El iterador se obtiene de 'std::vector::begin'}}
  c.clear();           // expected-note {{El iterador queda invalidado por 'std::vector::clear'}}
  sink(*it); // expected-warning {{Uso de un iterador invalidado: 'std::vector::clear' (línea 10) lo invalidó}} \
             // expected-note {{Uso de un iterador invalidado: 'std::vector::clear' (línea 10) lo invalidó}}
}

void ruta_referencia(std::vector<int> &c) {
  int &h = c.front(); // expected-note {{El handle al elemento se obtiene de 'std::vector::front'}}
  c.clear();          // expected-note {{El handle al elemento queda invalidado por 'std::vector::clear'}}
  sink(h); // expected-warning {{Uso de una referencia invalidada}} \
           // expected-note {{Uso de una referencia invalidada}}
}

void ruta_desreferencia(std::map<int, int> &c) {
  auto it = c.begin();  // la nota del iterador no sale: el aviso es sobre la referencia
  int &h = it->second;  // expected-note {{El handle al elemento se obtiene al desreferenciar el iterador}}
  c.clear();            // expected-note {{El handle al elemento queda invalidado por 'std::map::clear'}}
  sink(h); // expected-warning {{Uso de una referencia invalidada}} \
           // expected-note {{Uso de una referencia invalidada}}
}
