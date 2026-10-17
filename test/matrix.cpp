// GENERADO por bench/gen_matrix.py -- no editar a mano
// Matriz contenedor x operacion x dominio (iterador / referencia).
#include <deque>
#include <forward_list>
#include <list>
#include <map>
#include <set>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

void sink(int);
void sink(char);

void it_vector_push_back(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.push_back(1);
  sink(*it);
}
void rf_vector_push_back(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.push_back(1);
  sink(r);
}
void it_vector_emplace_back(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.emplace_back(1);
  sink(*it);
}
void rf_vector_emplace_back(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.emplace_back(1);
  sink(r);
}
void it_vector_insert_begin(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.insert(c.begin(), 1);
  sink(*it);
}
void rf_vector_insert_begin(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.insert(c.begin(), 1);
  sink(r);
}
void it_vector_insert_end(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.insert(c.end(), 1);
  sink(*it);
}
void rf_vector_insert_end(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.insert(c.end(), 1);
  sink(r);
}
void it_vector_erase_begin(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.erase(c.begin());
  sink(*it);
}
void rf_vector_erase_begin(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.erase(c.begin());
  sink(r);
}
void it_vector_clear(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.clear();
  sink(*it);
}
void rf_vector_clear(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.clear();
  sink(r);
}
void it_vector_resize_grow(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.resize(c.size() + 100);
  sink(*it);
}
void rf_vector_resize_grow(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.resize(c.size() + 100);
  sink(r);
}
void it_vector_reserve(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.reserve(c.size() + 100);
  sink(*it);
}
void rf_vector_reserve(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.reserve(c.size() + 100);
  sink(r);
}
void it_vector_shrink_to_fit(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.shrink_to_fit();
  sink(*it);
}
void rf_vector_shrink_to_fit(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.shrink_to_fit();
  sink(r);
}
void it_vector_assign(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.assign(3, 7);
  sink(*it);
}
void rf_vector_assign(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.assign(3, 7);
  sink(r);
}
void it_vector_pop_back(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.pop_back();
  sink(*it);
}
void rf_vector_pop_back(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.pop_back();
  sink(r);
}
void it_deque_push_back(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.push_back(1);
  sink(*it);
}
void rf_deque_push_back(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.push_back(1);
  sink(r);
}
void it_deque_push_front(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.push_front(1);
  sink(*it);
}
void rf_deque_push_front(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.push_front(1);
  sink(r);
}
void it_deque_emplace_back(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.emplace_back(1);
  sink(*it);
}
void rf_deque_emplace_back(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.emplace_back(1);
  sink(r);
}
void it_deque_insert_middle(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.insert(c.begin(), 1);
  sink(*it);
}
void rf_deque_insert_middle(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.insert(c.begin(), 1);
  sink(r);
}
void it_deque_erase_begin(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.erase(c.begin());
  sink(*it);
}
void rf_deque_erase_begin(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.erase(c.begin());
  sink(r);
}
void it_deque_clear(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.clear();
  sink(*it);
}
void rf_deque_clear(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.clear();
  sink(r);
}
void it_deque_resize_grow(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.resize(c.size() + 100);
  sink(*it);
}
void rf_deque_resize_grow(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.resize(c.size() + 100);
  sink(r);
}
void it_deque_pop_front(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.pop_front();
  sink(*it);
}
void rf_deque_pop_front(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.pop_front();
  sink(r);
}
void it_list_push_back(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.push_back(1);
  sink(*it);
}
void rf_list_push_back(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.push_back(1);
  sink(r);
}
void it_list_push_front(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.push_front(1);
  sink(*it);
}
void rf_list_push_front(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.push_front(1);
  sink(r);
}
void it_list_insert(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.insert(c.begin(), 1);
  sink(*it);
}
void rf_list_insert(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.insert(c.begin(), 1);
  sink(r);
}
void it_list_erase_begin(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.erase(c.begin());
  sink(*it);
}
void rf_list_erase_begin(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.erase(c.begin());
  sink(r);
}
void it_list_clear(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.clear();
  sink(*it);
}
void rf_list_clear(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.clear();
  sink(r);
}
void it_list_resize_grow(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.resize(c.size() + 100);
  sink(*it);
}
void rf_list_resize_grow(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.resize(c.size() + 100);
  sink(r);
}
void it_list_pop_front(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.pop_front();
  sink(*it);
}
void rf_list_pop_front(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.pop_front();
  sink(r);
}
void it_list_reverse(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.reverse();
  sink(*it);
}
void rf_list_reverse(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.reverse();
  sink(r);
}
void it_flist_push_front(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.push_front(1);
  sink(*it);
}
void rf_flist_push_front(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.push_front(1);
  sink(r);
}
void it_flist_insert_after(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.insert_after(c.before_begin(), 1);
  sink(*it);
}
void rf_flist_insert_after(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.insert_after(c.before_begin(), 1);
  sink(r);
}
void it_flist_erase_after(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.erase_after(c.before_begin());
  sink(*it);
}
void rf_flist_erase_after(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.erase_after(c.before_begin());
  sink(r);
}
void it_flist_clear(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.clear();
  sink(*it);
}
void rf_flist_clear(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.clear();
  sink(r);
}
void it_set_insert(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.insert(99);
  sink(*it);
}
void rf_set_insert(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.insert(99);
  sink(r);
}
void it_set_emplace(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.emplace(98);
  sink(*it);
}
void rf_set_emplace(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.emplace(98);
  sink(r);
}
void it_set_erase_begin(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.erase(c.begin());
  sink(*it);
}
void rf_set_erase_begin(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.erase(c.begin());
  sink(r);
}
void it_set_clear(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.clear();
  sink(*it);
}
void rf_set_clear(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.clear();
  sink(r);
}
void it_map_insert(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.insert({99, 1});
  sink(it->second);
}
void rf_map_insert(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = it->second;
  c.insert({99, 1});
  sink(r);
}
void it_map_emplace(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.emplace(98, 1);
  sink(it->second);
}
void rf_map_emplace(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = it->second;
  c.emplace(98, 1);
  sink(r);
}
void it_map_subscript(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c[97] = 1;
  sink(it->second);
}
void rf_map_subscript(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = it->second;
  c[97] = 1;
  sink(r);
}
void it_map_erase_begin(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.erase(c.begin());
  sink(it->second);
}
void rf_map_erase_begin(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = it->second;
  c.erase(c.begin());
  sink(r);
}
void it_map_clear(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.clear();
  sink(it->second);
}
void rf_map_clear(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = it->second;
  c.clear();
  sink(r);
}
void it_uset_insert(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.insert(99);
  sink(*it);
}
void rf_uset_insert(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.insert(99);
  sink(r);
}
void it_uset_erase_begin(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.erase(c.begin());
  sink(*it);
}
void rf_uset_erase_begin(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.erase(c.begin());
  sink(r);
}
void it_uset_clear(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.clear();
  sink(*it);
}
void rf_uset_clear(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.clear();
  sink(r);
}
void it_uset_rehash(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.rehash(1024);
  sink(*it);
}
void rf_uset_rehash(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.rehash(1024);
  sink(r);
}
void it_uset_reserve(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.reserve(1024);
  sink(*it);
}
void rf_uset_reserve(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = *it;
  c.reserve(1024);
  sink(r);
}
void it_umap_insert(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.insert({99, 1});
  sink(it->second);
}
void rf_umap_insert(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = it->second;
  c.insert({99, 1});
  sink(r);
}
void it_umap_subscript(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c[97] = 1;
  sink(it->second);
}
void rf_umap_subscript(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = it->second;
  c[97] = 1;
  sink(r);
}
void it_umap_erase_begin(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.erase(c.begin());
  sink(it->second);
}
void rf_umap_erase_begin(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = it->second;
  c.erase(c.begin());
  sink(r);
}
void it_umap_clear(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.clear();
  sink(it->second);
}
void rf_umap_clear(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = it->second;
  c.clear();
  sink(r);
}
void it_umap_rehash(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.rehash(1024);
  sink(it->second);
}
void rf_umap_rehash(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const int& r = it->second;
  c.rehash(1024);
  sink(r);
}
void it_string_push_back(std::string& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.push_back('x');
  sink(*it);
}
void rf_string_push_back(std::string& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const char& r = *it;
  c.push_back('x');
  sink(r);
}
void it_string_append(std::string& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.append("xyz");
  sink(*it);
}
void rf_string_append(std::string& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const char& r = *it;
  c.append("xyz");
  sink(r);
}
void it_string_insert_begin(std::string& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.insert(c.begin(), 'x');
  sink(*it);
}
void rf_string_insert_begin(std::string& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const char& r = *it;
  c.insert(c.begin(), 'x');
  sink(r);
}
void it_string_erase_begin(std::string& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.erase(c.begin());
  sink(*it);
}
void rf_string_erase_begin(std::string& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const char& r = *it;
  c.erase(c.begin());
  sink(r);
}
void it_string_clear(std::string& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.clear();
  sink(*it);
}
void rf_string_clear(std::string& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const char& r = *it;
  c.clear();
  sink(r);
}
void it_string_reserve(std::string& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.reserve(c.size() + 100);
  sink(*it);
}
void rf_string_reserve(std::string& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const char& r = *it;
  c.reserve(c.size() + 100);
  sink(r);
}
void it_string_resize_grow(std::string& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  c.resize(c.size() + 100);
  sink(*it);
}
void rf_string_resize_grow(std::string& c) {
  auto it = c.begin();
  if (it == c.end()) return;   // guarda: activa el modelado
  const char& r = *it;
  c.resize(c.size() + 100);
  sink(r);
}
