// Usos correctos: el checker no debe avisar en ninguno (RF-07).
#include <list>
#include <unordered_map>
#include <vector>

int reservado(std::vector<int> &v) {
  v.reserve(v.size() + 2);
  int &r = v[0];
  v.push_back(1);
  v.push_back(2); // reserve garantiza dos inserciones sin reubicar
  return r;
}

void borrar_impares(std::list<int> &l) {
  for (auto it = l.begin(); it != l.end();) {
    if (*it % 2)
      it = l.erase(it); // el iterador devuelto es válido
    else
      ++it;
  }
}

int lista_estable(std::list<int> &l) {
  int &r = l.front();
  l.push_back(4); // list nunca invalida en una inserción
  return r;
}

int mapa_con_reserva(std::unordered_map<int, int> &m) {
  m.reserve(m.size() + 1);
  auto it = m.begin();
  if (it == m.end())
    return 0;
  m.insert({42, 1}); // sin rehash: hay espacio para uno
  return it->second;
}
