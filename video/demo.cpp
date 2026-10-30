// Programa de la demostración: seis usos de un contenedor.
#include <vector>
#include <map>
void sink(int);

// 1. Referencia: erase borra el elemento y luego se lee. Defecto seguro.
void referencia(std::vector<int> &c) {
  int &h = c.front();
  c.erase(c.begin());
  sink(h);
}

// 2. Puntero: clear destruye todo. Defecto seguro.
void puntero(std::vector<int> &c) {
  int *p = &c[0];
  c.clear();
  sink(*p);
}

// 3. Iterador: erase libera el nodo de un map. Defecto seguro.
void iterador(std::map<int, int> &m) {
  auto it = m.begin();
  if (it == m.end()) return;
  m.erase(it);
  sink(it->second);
}

// 4. Depende de la capacidad: solo falla si push_back reubica. Aviso posible.
void depende(std::vector<int> &c) {
  int &h = c.front();
  c.push_back(1);
  sink(h);
}

// 5. Buen uso: reserve garantiza espacio. Sin aviso.
void con_reserva(std::vector<int> &c) {
  c.reserve(c.size() + 1);
  int &h = c.front();
  c.push_back(1);
  sink(h);
}

// 6. Buen uso: se usa el iterador que devuelve erase. Sin aviso.
void iterador_devuelto(std::vector<int> &c) {
  auto it = c.begin();
  if (it == c.end()) return;
  it = c.erase(it);
  if (it != c.end()) sink(*it);
}
