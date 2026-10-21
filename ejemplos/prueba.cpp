// Ejemplo para probar el checker a mano (libro: Uso → Levantar el checker).
#include <vector>

int confirmado(std::vector<int> &v) {
  int &r = v[0];
  v.clear();          // invalida todas las referencias
  return r;           // aviso confirmado
}

int posible(std::vector<int> &v) {
  int &r = v[0];
  v.push_back(4);     // invalida solo si se agota la capacidad
  return r;           // aviso posible (solo con PolicyMode=Possibly)
}

int con_garantia(std::vector<int> &v) {
  v.reserve(v.size() + 1);
  int &r = v[0];
  v.push_back(4);     // la reserva garantiza que no hay reubicación
  return r;           // sin aviso
}
