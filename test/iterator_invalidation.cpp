// Los 8 casos del documento base, uno por funcion, para medir que cubre
// la linea base de Clang (alpha.cplusplus.*Iterator*).
#include <vector>
#include <map>
#include <list>
#include <deque>
#include <string>
#include <unordered_map>

// ---- CASO 1: range-for + insertar --------------------------------- UB
void caso1_rangefor_push(std::vector<int> &v) {
  for (int x : v) {
    if (x % 2 == 0) v.push_back(x);
  }
}

// ---- CASO 2: erase durante el recorrido ---------------------------- UB
void caso2_erase_en_bucle(std::vector<int> &v) {
  for (auto it = v.begin(); it != v.end(); ++it) {
    if (*it == 0) v.erase(it);
  }
}

// ---- CASO 3a: el mismo bucle en map -------------------------------- UB
void caso3a_map_erase_en_bucle(std::map<int,int> &m) {
  for (auto it = m.begin(); it != m.end(); ++it) {
    if (it->second < 0) m.erase(it);
  }
}
// ---- CASO 3b: erase(it++) en map ----------------------------------- OK
void caso3b_map_erase_postinc(std::map<int,int> &m) {
  for (auto it = m.begin(); it != m.end(); ) {
    if (it->second < 0) m.erase(it++);
    else ++it;
  }
}
// ---- CASO 3c: erase(it++) en vector -------------------------------- UB
void caso3c_vector_erase_postinc(std::vector<int> &v) {
  for (auto it = v.begin(); it != v.end(); ) {
    if (*it == 0) v.erase(it++);
    else ++it;
  }
}

// ---- CASO 4a: referencia invalidada por push_back ------------------ UB
void caso4a_ref_vector(std::vector<std::string> &v) {
  std::string &primero = v[0];
  v.push_back("nuevo");
  primero += "!";
}
// ---- CASO 4b: lo mismo con deque ----------------------------------- OK
void caso4b_ref_deque(std::deque<std::string> &d) {
  std::string &primero = d[0];
  d.push_back("nuevo");
  primero += "!";
}

// ---- CASO 5: alias legal en push_back ------------------------------ OK
void caso5_alias_legal(std::vector<int> &v) {
  v.push_back(v[0]);
}

// ---- CASO 6: la mutacion cruza una llamada ------------------------- UB
void registrar(std::vector<int> &v, int x) { v.push_back(x); }
void caso6_interprocedural(std::vector<int> &v) {
  for (auto it = v.begin(); it != v.end(); ++it) {
    registrar(v, *it * 2);
  }
}

// ---- CASO 7: alias entre parametros -------------- UB solo si origen==destino
void caso7_alias_parametros(std::vector<int> &origen, std::vector<int> &destino) {
  for (auto it = origen.begin(); it != origen.end(); ++it) {
    destino.push_back(*it);
  }
}

// ---- CASO 8: rehash dependiente de ejecucion ----------------------- UB
void caso8_rehash(std::unordered_map<int,int> &m) {
  for (auto &kv : m) {
    m.insert({kv.first * 1000, kv.second});
  }
}

// ---- Controles negativos: NO deben avisar --------------------------- OK
void ok_list_insert(std::list<int> &l) {
  for (auto it = l.begin(); it != l.end(); ++it) l.push_back(*it);
}
void ok_erase_reasignando(std::vector<int> &v) {
  for (auto it = v.begin(); it != v.end(); ) {
    if (*it == 0) it = v.erase(it);
    else ++it;
  }
}
void ok_indice(std::vector<int> &v) {
  const std::size_t n = v.size();
  for (std::size_t i = 0; i < n; ++i)
    if (v[i] % 2 == 0) v.push_back(v[i]);
}
