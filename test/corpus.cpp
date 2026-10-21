// GENERADO por bench/gen_corpus.py — no editar a mano
#include <deque>
#include <forward_list>
#include <list>
#include <map>
#include <set>
#include <unordered_map>
#include <unordered_set>
#include <vector>

void sink(int);
void sink(char);
void sink(const void*);

void mutar_vector_push_back(std::vector<int>& c) { c.push_back(1); }
void mutar_vector_emplace_back(std::vector<int>& c) { c.emplace_back(1); }
void mutar_vector_insert_begin(std::vector<int>& c) { c.insert(c.begin(),1); }
void mutar_vector_insert_end(std::vector<int>& c) { c.insert(c.end(),1); }
void mutar_vector_erase_begin(std::vector<int>& c) { c.erase(c.begin()); }
void mutar_vector_clear(std::vector<int>& c) { c.clear(); }
void mutar_vector_resize_grow(std::vector<int>& c) { c.resize(c.size()+100); }
void mutar_vector_reserve(std::vector<int>& c) { c.reserve(c.size()+100); }
void mutar_vector_shrink_to_fit(std::vector<int>& c) { c.shrink_to_fit(); }
void mutar_vector_assign(std::vector<int>& c) { c.assign(3,7); }
void mutar_vector_pop_back(std::vector<int>& c) { c.pop_back(); }
void mutar_deque_push_back(std::deque<int>& c) { c.push_back(1); }
void mutar_deque_push_front(std::deque<int>& c) { c.push_front(1); }
void mutar_deque_emplace_back(std::deque<int>& c) { c.emplace_back(1); }
void mutar_deque_insert_middle(std::deque<int>& c) { c.insert(c.begin()+1,1); }
void mutar_deque_erase_begin(std::deque<int>& c) { c.erase(c.begin()); }
void mutar_deque_clear(std::deque<int>& c) { c.clear(); }
void mutar_deque_resize_grow(std::deque<int>& c) { c.resize(c.size()+100); }
void mutar_deque_pop_front(std::deque<int>& c) { c.pop_front(); }
void mutar_list_push_back(std::list<int>& c) { c.push_back(1); }
void mutar_list_push_front(std::list<int>& c) { c.push_front(1); }
void mutar_list_insert(std::list<int>& c) { c.insert(c.begin(),1); }
void mutar_list_erase_begin(std::list<int>& c) { c.erase(c.begin()); }
void mutar_list_clear(std::list<int>& c) { c.clear(); }
void mutar_list_resize_grow(std::list<int>& c) { c.resize(c.size()+100); }
void mutar_list_pop_front(std::list<int>& c) { c.pop_front(); }
void mutar_list_reverse(std::list<int>& c) { c.reverse(); }
void mutar_list_sort(std::list<int>& c) { c.sort(); }
void mutar_flist_push_front(std::forward_list<int>& c) { c.push_front(1); }
void mutar_flist_insert_after(std::forward_list<int>& c) { c.insert_after(c.before_begin(),1); }
void mutar_flist_erase_after(std::forward_list<int>& c) { c.erase_after(c.before_begin()); }
void mutar_flist_clear(std::forward_list<int>& c) { c.clear(); }
void mutar_set_insert(std::set<int>& c) { c.insert(99); }
void mutar_set_emplace(std::set<int>& c) { c.emplace(98); }
void mutar_set_erase_begin(std::set<int>& c) { c.erase(c.begin()); }
void mutar_set_clear(std::set<int>& c) { c.clear(); }
void mutar_mset_insert(std::multiset<int>& c) { c.insert(99); }
void mutar_mset_erase_begin(std::multiset<int>& c) { c.erase(c.begin()); }
void mutar_mset_clear(std::multiset<int>& c) { c.clear(); }
void mutar_map_insert(std::map<int,int>& c) { c.insert({99,1}); }
void mutar_map_emplace(std::map<int,int>& c) { c.emplace(98,1); }
void mutar_map_subscript(std::map<int,int>& c) { c[97]=1; }
void mutar_map_erase_begin(std::map<int,int>& c) { c.erase(c.begin()); }
void mutar_map_clear(std::map<int,int>& c) { c.clear(); }
void mutar_mmap_insert(std::multimap<int,int>& c) { c.insert({99,1}); }
void mutar_mmap_erase_begin(std::multimap<int,int>& c) { c.erase(c.begin()); }
void mutar_mmap_clear(std::multimap<int,int>& c) { c.clear(); }
void mutar_uset_insert(std::unordered_set<int>& c) { c.insert(99); }
void mutar_uset_erase_begin(std::unordered_set<int>& c) { c.erase(c.begin()); }
void mutar_uset_clear(std::unordered_set<int>& c) { c.clear(); }
void mutar_uset_rehash(std::unordered_set<int>& c) { c.rehash(1024); }
void mutar_uset_reserve(std::unordered_set<int>& c) { c.reserve(1024); }
void mutar_umap_insert(std::unordered_map<int,int>& c) { c.insert({99,1}); }
void mutar_umap_subscript(std::unordered_map<int,int>& c) { c[97]=1; }
void mutar_umap_erase_begin(std::unordered_map<int,int>& c) { c.erase(c.begin()); }
void mutar_umap_clear(std::unordered_map<int,int>& c) { c.clear(); }
void mutar_umap_rehash(std::unordered_map<int,int>& c) { c.rehash(1024); }

void f_vector_push_back_it_recto(std::vector<int>& c) {
  auto it = c.begin();
  c.push_back(1);
  sink(*it);
}
void f_vector_push_back_it_recto_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  c.push_back(1);
  sink(*it);
}
void f_vector_push_back_it_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.push_back(1);
  sink(*it);
}
void f_vector_push_back_it_guarda_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  c.push_back(1);
  sink(*it);
}
void f_vector_push_back_it_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.push_back(1);
    sink(*it);
  }
}
void f_vector_push_back_it_bucle_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 3);
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.push_back(1);
    sink(*it);
  }
}
void f_vector_push_back_it_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_vector_push_back(c);
  sink(*it);
}
void f_vector_push_back_it_llamada_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_vector_push_back(c);
  sink(*it);
}
void f_vector_push_back_ref_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.push_back(1);
  sink(h);
}
void f_vector_push_back_ref_recto_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  const auto& h = *it;
  c.push_back(1);
  sink(h);
}
void f_vector_push_back_ref_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.push_back(1);
  sink(h);
}
void f_vector_push_back_ref_guarda_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.push_back(1);
  sink(h);
}
void f_vector_push_back_ref_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.push_back(1);
    sink(h);
  }
}
void f_vector_push_back_ref_bucle_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 3);
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.push_back(1);
    sink(h);
  }
}
void f_vector_push_back_ref_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_vector_push_back(c);
  sink(h);
}
void f_vector_push_back_ref_llamada_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_vector_push_back(c);
  sink(h);
}
void f_vector_push_back_ptr_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.push_back(1);
  sink(*h);
}
void f_vector_push_back_ptr_recto_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  const auto* h = &*it;
  c.push_back(1);
  sink(*h);
}
void f_vector_push_back_ptr_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.push_back(1);
  sink(*h);
}
void f_vector_push_back_ptr_guarda_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.push_back(1);
  sink(*h);
}
void f_vector_push_back_ptr_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.push_back(1);
    sink(*h);
  }
}
void f_vector_push_back_ptr_bucle_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 3);
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.push_back(1);
    sink(*h);
  }
}
void f_vector_push_back_ptr_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_vector_push_back(c);
  sink(*h);
}
void f_vector_push_back_ptr_llamada_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_vector_push_back(c);
  sink(*h);
}
void f_vector_emplace_back_it_recto(std::vector<int>& c) {
  auto it = c.begin();
  c.emplace_back(1);
  sink(*it);
}
void f_vector_emplace_back_it_recto_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  c.emplace_back(1);
  sink(*it);
}
void f_vector_emplace_back_it_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.emplace_back(1);
  sink(*it);
}
void f_vector_emplace_back_it_guarda_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  c.emplace_back(1);
  sink(*it);
}
void f_vector_emplace_back_it_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.emplace_back(1);
    sink(*it);
  }
}
void f_vector_emplace_back_it_bucle_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 3);
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.emplace_back(1);
    sink(*it);
  }
}
void f_vector_emplace_back_it_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_vector_emplace_back(c);
  sink(*it);
}
void f_vector_emplace_back_it_llamada_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_vector_emplace_back(c);
  sink(*it);
}
void f_vector_emplace_back_ref_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.emplace_back(1);
  sink(h);
}
void f_vector_emplace_back_ref_recto_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  const auto& h = *it;
  c.emplace_back(1);
  sink(h);
}
void f_vector_emplace_back_ref_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.emplace_back(1);
  sink(h);
}
void f_vector_emplace_back_ref_guarda_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.emplace_back(1);
  sink(h);
}
void f_vector_emplace_back_ref_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.emplace_back(1);
    sink(h);
  }
}
void f_vector_emplace_back_ref_bucle_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 3);
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.emplace_back(1);
    sink(h);
  }
}
void f_vector_emplace_back_ref_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_vector_emplace_back(c);
  sink(h);
}
void f_vector_emplace_back_ref_llamada_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_vector_emplace_back(c);
  sink(h);
}
void f_vector_emplace_back_ptr_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.emplace_back(1);
  sink(*h);
}
void f_vector_emplace_back_ptr_recto_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  const auto* h = &*it;
  c.emplace_back(1);
  sink(*h);
}
void f_vector_emplace_back_ptr_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.emplace_back(1);
  sink(*h);
}
void f_vector_emplace_back_ptr_guarda_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.emplace_back(1);
  sink(*h);
}
void f_vector_emplace_back_ptr_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.emplace_back(1);
    sink(*h);
  }
}
void f_vector_emplace_back_ptr_bucle_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 3);
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.emplace_back(1);
    sink(*h);
  }
}
void f_vector_emplace_back_ptr_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_vector_emplace_back(c);
  sink(*h);
}
void f_vector_emplace_back_ptr_llamada_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_vector_emplace_back(c);
  sink(*h);
}
void f_vector_insert_begin_it_recto(std::vector<int>& c) {
  auto it = c.begin();
  c.insert(c.begin(),1);
  sink(*it);
}
void f_vector_insert_begin_it_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.insert(c.begin(),1);
  sink(*it);
}
void f_vector_insert_begin_it_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.insert(c.begin(),1);
    sink(*it);
  }
}
void f_vector_insert_begin_it_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_vector_insert_begin(c);
  sink(*it);
}
void f_vector_insert_begin_ref_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.insert(c.begin(),1);
  sink(h);
}
void f_vector_insert_begin_ref_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.insert(c.begin(),1);
  sink(h);
}
void f_vector_insert_begin_ref_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.insert(c.begin(),1);
    sink(h);
  }
}
void f_vector_insert_begin_ref_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_vector_insert_begin(c);
  sink(h);
}
void f_vector_insert_begin_ptr_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.insert(c.begin(),1);
  sink(*h);
}
void f_vector_insert_begin_ptr_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.insert(c.begin(),1);
  sink(*h);
}
void f_vector_insert_begin_ptr_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.insert(c.begin(),1);
    sink(*h);
  }
}
void f_vector_insert_begin_ptr_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_vector_insert_begin(c);
  sink(*h);
}
void f_vector_insert_end_it_recto(std::vector<int>& c) {
  auto it = c.begin();
  c.insert(c.end(),1);
  sink(*it);
}
void f_vector_insert_end_it_recto_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  c.insert(c.end(),1);
  sink(*it);
}
void f_vector_insert_end_it_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.insert(c.end(),1);
  sink(*it);
}
void f_vector_insert_end_it_guarda_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  c.insert(c.end(),1);
  sink(*it);
}
void f_vector_insert_end_it_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.insert(c.end(),1);
    sink(*it);
  }
}
void f_vector_insert_end_it_bucle_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 3);
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.insert(c.end(),1);
    sink(*it);
  }
}
void f_vector_insert_end_it_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_vector_insert_end(c);
  sink(*it);
}
void f_vector_insert_end_it_llamada_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_vector_insert_end(c);
  sink(*it);
}
void f_vector_insert_end_ref_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.insert(c.end(),1);
  sink(h);
}
void f_vector_insert_end_ref_recto_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  const auto& h = *it;
  c.insert(c.end(),1);
  sink(h);
}
void f_vector_insert_end_ref_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.insert(c.end(),1);
  sink(h);
}
void f_vector_insert_end_ref_guarda_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.insert(c.end(),1);
  sink(h);
}
void f_vector_insert_end_ref_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.insert(c.end(),1);
    sink(h);
  }
}
void f_vector_insert_end_ref_bucle_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 3);
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.insert(c.end(),1);
    sink(h);
  }
}
void f_vector_insert_end_ref_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_vector_insert_end(c);
  sink(h);
}
void f_vector_insert_end_ref_llamada_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_vector_insert_end(c);
  sink(h);
}
void f_vector_insert_end_ptr_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.insert(c.end(),1);
  sink(*h);
}
void f_vector_insert_end_ptr_recto_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  const auto* h = &*it;
  c.insert(c.end(),1);
  sink(*h);
}
void f_vector_insert_end_ptr_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.insert(c.end(),1);
  sink(*h);
}
void f_vector_insert_end_ptr_guarda_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.insert(c.end(),1);
  sink(*h);
}
void f_vector_insert_end_ptr_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.insert(c.end(),1);
    sink(*h);
  }
}
void f_vector_insert_end_ptr_bucle_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 3);
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.insert(c.end(),1);
    sink(*h);
  }
}
void f_vector_insert_end_ptr_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_vector_insert_end(c);
  sink(*h);
}
void f_vector_insert_end_ptr_llamada_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_vector_insert_end(c);
  sink(*h);
}
void f_vector_erase_begin_it_recto(std::vector<int>& c) {
  auto it = c.begin();
  c.erase(c.begin());
  sink(*it);
}
void f_vector_erase_begin_it_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.erase(c.begin());
  sink(*it);
}
void f_vector_erase_begin_it_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.erase(c.begin());
    sink(*it);
  }
}
void f_vector_erase_begin_it_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_vector_erase_begin(c);
  sink(*it);
}
void f_vector_erase_begin_ref_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.erase(c.begin());
  sink(h);
}
void f_vector_erase_begin_ref_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.erase(c.begin());
  sink(h);
}
void f_vector_erase_begin_ref_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.erase(c.begin());
    sink(h);
  }
}
void f_vector_erase_begin_ref_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_vector_erase_begin(c);
  sink(h);
}
void f_vector_erase_begin_ptr_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.erase(c.begin());
  sink(*h);
}
void f_vector_erase_begin_ptr_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.erase(c.begin());
  sink(*h);
}
void f_vector_erase_begin_ptr_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.erase(c.begin());
    sink(*h);
  }
}
void f_vector_erase_begin_ptr_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_vector_erase_begin(c);
  sink(*h);
}
void f_vector_clear_it_recto(std::vector<int>& c) {
  auto it = c.begin();
  c.clear();
  sink(*it);
}
void f_vector_clear_it_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.clear();
  sink(*it);
}
void f_vector_clear_it_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.clear();
    sink(*it);
  }
}
void f_vector_clear_it_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_vector_clear(c);
  sink(*it);
}
void f_vector_clear_ref_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.clear();
  sink(h);
}
void f_vector_clear_ref_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.clear();
  sink(h);
}
void f_vector_clear_ref_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.clear();
    sink(h);
  }
}
void f_vector_clear_ref_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_vector_clear(c);
  sink(h);
}
void f_vector_clear_ptr_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.clear();
  sink(*h);
}
void f_vector_clear_ptr_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.clear();
  sink(*h);
}
void f_vector_clear_ptr_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.clear();
    sink(*h);
  }
}
void f_vector_clear_ptr_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_vector_clear(c);
  sink(*h);
}
void f_vector_resize_grow_it_recto(std::vector<int>& c) {
  auto it = c.begin();
  c.resize(c.size()+100);
  sink(*it);
}
void f_vector_resize_grow_it_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.resize(c.size()+100);
  sink(*it);
}
void f_vector_resize_grow_it_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.resize(c.size()+100);
    sink(*it);
  }
}
void f_vector_resize_grow_it_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_vector_resize_grow(c);
  sink(*it);
}
void f_vector_resize_grow_ref_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.resize(c.size()+100);
  sink(h);
}
void f_vector_resize_grow_ref_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.resize(c.size()+100);
  sink(h);
}
void f_vector_resize_grow_ref_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.resize(c.size()+100);
    sink(h);
  }
}
void f_vector_resize_grow_ref_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_vector_resize_grow(c);
  sink(h);
}
void f_vector_resize_grow_ptr_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.resize(c.size()+100);
  sink(*h);
}
void f_vector_resize_grow_ptr_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.resize(c.size()+100);
  sink(*h);
}
void f_vector_resize_grow_ptr_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.resize(c.size()+100);
    sink(*h);
  }
}
void f_vector_resize_grow_ptr_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_vector_resize_grow(c);
  sink(*h);
}
void f_vector_reserve_it_recto(std::vector<int>& c) {
  auto it = c.begin();
  c.reserve(c.size()+100);
  sink(*it);
}
void f_vector_reserve_it_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.reserve(c.size()+100);
  sink(*it);
}
void f_vector_reserve_it_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.reserve(c.size()+100);
    sink(*it);
  }
}
void f_vector_reserve_it_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_vector_reserve(c);
  sink(*it);
}
void f_vector_reserve_ref_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.reserve(c.size()+100);
  sink(h);
}
void f_vector_reserve_ref_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.reserve(c.size()+100);
  sink(h);
}
void f_vector_reserve_ref_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.reserve(c.size()+100);
    sink(h);
  }
}
void f_vector_reserve_ref_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_vector_reserve(c);
  sink(h);
}
void f_vector_reserve_ptr_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.reserve(c.size()+100);
  sink(*h);
}
void f_vector_reserve_ptr_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.reserve(c.size()+100);
  sink(*h);
}
void f_vector_reserve_ptr_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.reserve(c.size()+100);
    sink(*h);
  }
}
void f_vector_reserve_ptr_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_vector_reserve(c);
  sink(*h);
}
void f_vector_shrink_to_fit_it_recto(std::vector<int>& c) {
  auto it = c.begin();
  c.shrink_to_fit();
  sink(*it);
}
void f_vector_shrink_to_fit_it_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.shrink_to_fit();
  sink(*it);
}
void f_vector_shrink_to_fit_it_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.shrink_to_fit();
    sink(*it);
  }
}
void f_vector_shrink_to_fit_it_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_vector_shrink_to_fit(c);
  sink(*it);
}
void f_vector_shrink_to_fit_ref_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.shrink_to_fit();
  sink(h);
}
void f_vector_shrink_to_fit_ref_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.shrink_to_fit();
  sink(h);
}
void f_vector_shrink_to_fit_ref_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.shrink_to_fit();
    sink(h);
  }
}
void f_vector_shrink_to_fit_ref_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_vector_shrink_to_fit(c);
  sink(h);
}
void f_vector_shrink_to_fit_ptr_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.shrink_to_fit();
  sink(*h);
}
void f_vector_shrink_to_fit_ptr_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.shrink_to_fit();
  sink(*h);
}
void f_vector_shrink_to_fit_ptr_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.shrink_to_fit();
    sink(*h);
  }
}
void f_vector_shrink_to_fit_ptr_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_vector_shrink_to_fit(c);
  sink(*h);
}
void f_vector_assign_it_recto(std::vector<int>& c) {
  auto it = c.begin();
  c.assign(3,7);
  sink(*it);
}
void f_vector_assign_it_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.assign(3,7);
  sink(*it);
}
void f_vector_assign_it_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.assign(3,7);
    sink(*it);
  }
}
void f_vector_assign_it_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_vector_assign(c);
  sink(*it);
}
void f_vector_assign_ref_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.assign(3,7);
  sink(h);
}
void f_vector_assign_ref_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.assign(3,7);
  sink(h);
}
void f_vector_assign_ref_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.assign(3,7);
    sink(h);
  }
}
void f_vector_assign_ref_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_vector_assign(c);
  sink(h);
}
void f_vector_assign_ptr_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.assign(3,7);
  sink(*h);
}
void f_vector_assign_ptr_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.assign(3,7);
  sink(*h);
}
void f_vector_assign_ptr_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.assign(3,7);
    sink(*h);
  }
}
void f_vector_assign_ptr_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_vector_assign(c);
  sink(*h);
}
void f_vector_pop_back_it_recto(std::vector<int>& c) {
  auto it = c.begin();
  c.pop_back();
  sink(*it);
}
void f_vector_pop_back_it_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.pop_back();
  sink(*it);
}
void f_vector_pop_back_it_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.pop_back();
    sink(*it);
  }
}
void f_vector_pop_back_it_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_vector_pop_back(c);
  sink(*it);
}
void f_vector_pop_back_ref_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.pop_back();
  sink(h);
}
void f_vector_pop_back_ref_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.pop_back();
  sink(h);
}
void f_vector_pop_back_ref_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.pop_back();
    sink(h);
  }
}
void f_vector_pop_back_ref_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_vector_pop_back(c);
  sink(h);
}
void f_vector_pop_back_ptr_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.pop_back();
  sink(*h);
}
void f_vector_pop_back_ptr_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.pop_back();
  sink(*h);
}
void f_vector_pop_back_ptr_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.pop_back();
    sink(*h);
  }
}
void f_vector_pop_back_ptr_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_vector_pop_back(c);
  sink(*h);
}
void f_deque_push_back_it_recto(std::deque<int>& c) {
  auto it = c.begin();
  c.push_back(1);
  sink(*it);
}
void f_deque_push_back_it_guarda(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.push_back(1);
  sink(*it);
}
void f_deque_push_back_it_bucle(std::deque<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.push_back(1);
    sink(*it);
  }
}
void f_deque_push_back_it_llamada(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_deque_push_back(c);
  sink(*it);
}
void f_deque_push_back_ref_recto(std::deque<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.push_back(1);
  sink(h);
}
void f_deque_push_back_ref_guarda(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.push_back(1);
  sink(h);
}
void f_deque_push_back_ref_bucle(std::deque<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.push_back(1);
    sink(h);
  }
}
void f_deque_push_back_ref_llamada(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_deque_push_back(c);
  sink(h);
}
void f_deque_push_back_ptr_recto(std::deque<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.push_back(1);
  sink(*h);
}
void f_deque_push_back_ptr_guarda(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.push_back(1);
  sink(*h);
}
void f_deque_push_back_ptr_bucle(std::deque<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.push_back(1);
    sink(*h);
  }
}
void f_deque_push_back_ptr_llamada(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_deque_push_back(c);
  sink(*h);
}
void f_deque_push_front_it_recto(std::deque<int>& c) {
  auto it = c.begin();
  c.push_front(1);
  sink(*it);
}
void f_deque_push_front_it_guarda(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.push_front(1);
  sink(*it);
}
void f_deque_push_front_it_bucle(std::deque<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.push_front(1);
    sink(*it);
  }
}
void f_deque_push_front_it_llamada(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_deque_push_front(c);
  sink(*it);
}
void f_deque_push_front_ref_recto(std::deque<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.push_front(1);
  sink(h);
}
void f_deque_push_front_ref_guarda(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.push_front(1);
  sink(h);
}
void f_deque_push_front_ref_bucle(std::deque<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.push_front(1);
    sink(h);
  }
}
void f_deque_push_front_ref_llamada(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_deque_push_front(c);
  sink(h);
}
void f_deque_push_front_ptr_recto(std::deque<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.push_front(1);
  sink(*h);
}
void f_deque_push_front_ptr_guarda(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.push_front(1);
  sink(*h);
}
void f_deque_push_front_ptr_bucle(std::deque<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.push_front(1);
    sink(*h);
  }
}
void f_deque_push_front_ptr_llamada(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_deque_push_front(c);
  sink(*h);
}
void f_deque_emplace_back_it_recto(std::deque<int>& c) {
  auto it = c.begin();
  c.emplace_back(1);
  sink(*it);
}
void f_deque_emplace_back_it_guarda(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.emplace_back(1);
  sink(*it);
}
void f_deque_emplace_back_it_bucle(std::deque<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.emplace_back(1);
    sink(*it);
  }
}
void f_deque_emplace_back_it_llamada(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_deque_emplace_back(c);
  sink(*it);
}
void f_deque_emplace_back_ref_recto(std::deque<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.emplace_back(1);
  sink(h);
}
void f_deque_emplace_back_ref_guarda(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.emplace_back(1);
  sink(h);
}
void f_deque_emplace_back_ref_bucle(std::deque<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.emplace_back(1);
    sink(h);
  }
}
void f_deque_emplace_back_ref_llamada(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_deque_emplace_back(c);
  sink(h);
}
void f_deque_emplace_back_ptr_recto(std::deque<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.emplace_back(1);
  sink(*h);
}
void f_deque_emplace_back_ptr_guarda(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.emplace_back(1);
  sink(*h);
}
void f_deque_emplace_back_ptr_bucle(std::deque<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.emplace_back(1);
    sink(*h);
  }
}
void f_deque_emplace_back_ptr_llamada(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_deque_emplace_back(c);
  sink(*h);
}
void f_deque_insert_middle_it_recto(std::deque<int>& c) {
  auto it = c.begin();
  c.insert(c.begin()+1,1);
  sink(*it);
}
void f_deque_insert_middle_it_guarda(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.insert(c.begin()+1,1);
  sink(*it);
}
void f_deque_insert_middle_it_bucle(std::deque<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.insert(c.begin()+1,1);
    sink(*it);
  }
}
void f_deque_insert_middle_it_llamada(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_deque_insert_middle(c);
  sink(*it);
}
void f_deque_insert_middle_ref_recto(std::deque<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.insert(c.begin()+1,1);
  sink(h);
}
void f_deque_insert_middle_ref_guarda(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.insert(c.begin()+1,1);
  sink(h);
}
void f_deque_insert_middle_ref_bucle(std::deque<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.insert(c.begin()+1,1);
    sink(h);
  }
}
void f_deque_insert_middle_ref_llamada(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_deque_insert_middle(c);
  sink(h);
}
void f_deque_insert_middle_ptr_recto(std::deque<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.insert(c.begin()+1,1);
  sink(*h);
}
void f_deque_insert_middle_ptr_guarda(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.insert(c.begin()+1,1);
  sink(*h);
}
void f_deque_insert_middle_ptr_bucle(std::deque<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.insert(c.begin()+1,1);
    sink(*h);
  }
}
void f_deque_insert_middle_ptr_llamada(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_deque_insert_middle(c);
  sink(*h);
}
void f_deque_erase_begin_it_recto(std::deque<int>& c) {
  auto it = c.begin();
  c.erase(c.begin());
  sink(*it);
}
void f_deque_erase_begin_it_guarda(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.erase(c.begin());
  sink(*it);
}
void f_deque_erase_begin_it_bucle(std::deque<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.erase(c.begin());
    sink(*it);
  }
}
void f_deque_erase_begin_it_llamada(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_deque_erase_begin(c);
  sink(*it);
}
void f_deque_erase_begin_ref_recto(std::deque<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.erase(c.begin());
  sink(h);
}
void f_deque_erase_begin_ref_guarda(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.erase(c.begin());
  sink(h);
}
void f_deque_erase_begin_ref_bucle(std::deque<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.erase(c.begin());
    sink(h);
  }
}
void f_deque_erase_begin_ref_llamada(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_deque_erase_begin(c);
  sink(h);
}
void f_deque_erase_begin_ptr_recto(std::deque<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.erase(c.begin());
  sink(*h);
}
void f_deque_erase_begin_ptr_guarda(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.erase(c.begin());
  sink(*h);
}
void f_deque_erase_begin_ptr_bucle(std::deque<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.erase(c.begin());
    sink(*h);
  }
}
void f_deque_erase_begin_ptr_llamada(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_deque_erase_begin(c);
  sink(*h);
}
void f_deque_clear_it_recto(std::deque<int>& c) {
  auto it = c.begin();
  c.clear();
  sink(*it);
}
void f_deque_clear_it_guarda(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.clear();
  sink(*it);
}
void f_deque_clear_it_bucle(std::deque<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.clear();
    sink(*it);
  }
}
void f_deque_clear_it_llamada(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_deque_clear(c);
  sink(*it);
}
void f_deque_clear_ref_recto(std::deque<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.clear();
  sink(h);
}
void f_deque_clear_ref_guarda(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.clear();
  sink(h);
}
void f_deque_clear_ref_bucle(std::deque<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.clear();
    sink(h);
  }
}
void f_deque_clear_ref_llamada(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_deque_clear(c);
  sink(h);
}
void f_deque_clear_ptr_recto(std::deque<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.clear();
  sink(*h);
}
void f_deque_clear_ptr_guarda(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.clear();
  sink(*h);
}
void f_deque_clear_ptr_bucle(std::deque<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.clear();
    sink(*h);
  }
}
void f_deque_clear_ptr_llamada(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_deque_clear(c);
  sink(*h);
}
void f_deque_resize_grow_it_recto(std::deque<int>& c) {
  auto it = c.begin();
  c.resize(c.size()+100);
  sink(*it);
}
void f_deque_resize_grow_it_guarda(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.resize(c.size()+100);
  sink(*it);
}
void f_deque_resize_grow_it_bucle(std::deque<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.resize(c.size()+100);
    sink(*it);
  }
}
void f_deque_resize_grow_it_llamada(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_deque_resize_grow(c);
  sink(*it);
}
void f_deque_resize_grow_ref_recto(std::deque<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.resize(c.size()+100);
  sink(h);
}
void f_deque_resize_grow_ref_guarda(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.resize(c.size()+100);
  sink(h);
}
void f_deque_resize_grow_ref_bucle(std::deque<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.resize(c.size()+100);
    sink(h);
  }
}
void f_deque_resize_grow_ref_llamada(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_deque_resize_grow(c);
  sink(h);
}
void f_deque_resize_grow_ptr_recto(std::deque<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.resize(c.size()+100);
  sink(*h);
}
void f_deque_resize_grow_ptr_guarda(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.resize(c.size()+100);
  sink(*h);
}
void f_deque_resize_grow_ptr_bucle(std::deque<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.resize(c.size()+100);
    sink(*h);
  }
}
void f_deque_resize_grow_ptr_llamada(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_deque_resize_grow(c);
  sink(*h);
}
void f_deque_pop_front_it_recto(std::deque<int>& c) {
  auto it = c.begin();
  c.pop_front();
  sink(*it);
}
void f_deque_pop_front_it_guarda(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.pop_front();
  sink(*it);
}
void f_deque_pop_front_it_bucle(std::deque<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.pop_front();
    sink(*it);
  }
}
void f_deque_pop_front_it_llamada(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_deque_pop_front(c);
  sink(*it);
}
void f_deque_pop_front_ref_recto(std::deque<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.pop_front();
  sink(h);
}
void f_deque_pop_front_ref_guarda(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.pop_front();
  sink(h);
}
void f_deque_pop_front_ref_bucle(std::deque<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.pop_front();
    sink(h);
  }
}
void f_deque_pop_front_ref_llamada(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_deque_pop_front(c);
  sink(h);
}
void f_deque_pop_front_ptr_recto(std::deque<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.pop_front();
  sink(*h);
}
void f_deque_pop_front_ptr_guarda(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.pop_front();
  sink(*h);
}
void f_deque_pop_front_ptr_bucle(std::deque<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.pop_front();
    sink(*h);
  }
}
void f_deque_pop_front_ptr_llamada(std::deque<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_deque_pop_front(c);
  sink(*h);
}
void f_list_push_back_it_recto(std::list<int>& c) {
  auto it = c.begin();
  c.push_back(1);
  sink(*it);
}
void f_list_push_back_it_guarda(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.push_back(1);
  sink(*it);
}
void f_list_push_back_it_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.push_back(1);
    sink(*it);
  }
}
void f_list_push_back_it_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_list_push_back(c);
  sink(*it);
}
void f_list_push_back_ref_recto(std::list<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.push_back(1);
  sink(h);
}
void f_list_push_back_ref_guarda(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.push_back(1);
  sink(h);
}
void f_list_push_back_ref_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.push_back(1);
    sink(h);
  }
}
void f_list_push_back_ref_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_list_push_back(c);
  sink(h);
}
void f_list_push_back_ptr_recto(std::list<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.push_back(1);
  sink(*h);
}
void f_list_push_back_ptr_guarda(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.push_back(1);
  sink(*h);
}
void f_list_push_back_ptr_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.push_back(1);
    sink(*h);
  }
}
void f_list_push_back_ptr_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_list_push_back(c);
  sink(*h);
}
void f_list_push_front_it_recto(std::list<int>& c) {
  auto it = c.begin();
  c.push_front(1);
  sink(*it);
}
void f_list_push_front_it_guarda(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.push_front(1);
  sink(*it);
}
void f_list_push_front_it_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.push_front(1);
    sink(*it);
  }
}
void f_list_push_front_it_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_list_push_front(c);
  sink(*it);
}
void f_list_push_front_ref_recto(std::list<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.push_front(1);
  sink(h);
}
void f_list_push_front_ref_guarda(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.push_front(1);
  sink(h);
}
void f_list_push_front_ref_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.push_front(1);
    sink(h);
  }
}
void f_list_push_front_ref_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_list_push_front(c);
  sink(h);
}
void f_list_push_front_ptr_recto(std::list<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.push_front(1);
  sink(*h);
}
void f_list_push_front_ptr_guarda(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.push_front(1);
  sink(*h);
}
void f_list_push_front_ptr_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.push_front(1);
    sink(*h);
  }
}
void f_list_push_front_ptr_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_list_push_front(c);
  sink(*h);
}
void f_list_insert_it_recto(std::list<int>& c) {
  auto it = c.begin();
  c.insert(c.begin(),1);
  sink(*it);
}
void f_list_insert_it_guarda(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.insert(c.begin(),1);
  sink(*it);
}
void f_list_insert_it_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.insert(c.begin(),1);
    sink(*it);
  }
}
void f_list_insert_it_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_list_insert(c);
  sink(*it);
}
void f_list_insert_ref_recto(std::list<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.insert(c.begin(),1);
  sink(h);
}
void f_list_insert_ref_guarda(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.insert(c.begin(),1);
  sink(h);
}
void f_list_insert_ref_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.insert(c.begin(),1);
    sink(h);
  }
}
void f_list_insert_ref_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_list_insert(c);
  sink(h);
}
void f_list_insert_ptr_recto(std::list<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.insert(c.begin(),1);
  sink(*h);
}
void f_list_insert_ptr_guarda(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.insert(c.begin(),1);
  sink(*h);
}
void f_list_insert_ptr_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.insert(c.begin(),1);
    sink(*h);
  }
}
void f_list_insert_ptr_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_list_insert(c);
  sink(*h);
}
void f_list_erase_begin_it_recto(std::list<int>& c) {
  auto it = c.begin();
  c.erase(c.begin());
  sink(*it);
}
void f_list_erase_begin_it_guarda(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.erase(c.begin());
  sink(*it);
}
void f_list_erase_begin_it_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.erase(c.begin());
    sink(*it);
  }
}
void f_list_erase_begin_it_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_list_erase_begin(c);
  sink(*it);
}
void f_list_erase_begin_ref_recto(std::list<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.erase(c.begin());
  sink(h);
}
void f_list_erase_begin_ref_guarda(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.erase(c.begin());
  sink(h);
}
void f_list_erase_begin_ref_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.erase(c.begin());
    sink(h);
  }
}
void f_list_erase_begin_ref_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_list_erase_begin(c);
  sink(h);
}
void f_list_erase_begin_ptr_recto(std::list<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.erase(c.begin());
  sink(*h);
}
void f_list_erase_begin_ptr_guarda(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.erase(c.begin());
  sink(*h);
}
void f_list_erase_begin_ptr_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.erase(c.begin());
    sink(*h);
  }
}
void f_list_erase_begin_ptr_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_list_erase_begin(c);
  sink(*h);
}
void f_list_clear_it_recto(std::list<int>& c) {
  auto it = c.begin();
  c.clear();
  sink(*it);
}
void f_list_clear_it_guarda(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.clear();
  sink(*it);
}
void f_list_clear_it_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.clear();
    sink(*it);
  }
}
void f_list_clear_it_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_list_clear(c);
  sink(*it);
}
void f_list_clear_ref_recto(std::list<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.clear();
  sink(h);
}
void f_list_clear_ref_guarda(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.clear();
  sink(h);
}
void f_list_clear_ref_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.clear();
    sink(h);
  }
}
void f_list_clear_ref_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_list_clear(c);
  sink(h);
}
void f_list_clear_ptr_recto(std::list<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.clear();
  sink(*h);
}
void f_list_clear_ptr_guarda(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.clear();
  sink(*h);
}
void f_list_clear_ptr_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.clear();
    sink(*h);
  }
}
void f_list_clear_ptr_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_list_clear(c);
  sink(*h);
}
void f_list_resize_grow_it_recto(std::list<int>& c) {
  auto it = c.begin();
  c.resize(c.size()+100);
  sink(*it);
}
void f_list_resize_grow_it_guarda(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.resize(c.size()+100);
  sink(*it);
}
void f_list_resize_grow_it_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.resize(c.size()+100);
    sink(*it);
  }
}
void f_list_resize_grow_it_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_list_resize_grow(c);
  sink(*it);
}
void f_list_resize_grow_ref_recto(std::list<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.resize(c.size()+100);
  sink(h);
}
void f_list_resize_grow_ref_guarda(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.resize(c.size()+100);
  sink(h);
}
void f_list_resize_grow_ref_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.resize(c.size()+100);
    sink(h);
  }
}
void f_list_resize_grow_ref_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_list_resize_grow(c);
  sink(h);
}
void f_list_resize_grow_ptr_recto(std::list<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.resize(c.size()+100);
  sink(*h);
}
void f_list_resize_grow_ptr_guarda(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.resize(c.size()+100);
  sink(*h);
}
void f_list_resize_grow_ptr_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.resize(c.size()+100);
    sink(*h);
  }
}
void f_list_resize_grow_ptr_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_list_resize_grow(c);
  sink(*h);
}
void f_list_pop_front_it_recto(std::list<int>& c) {
  auto it = c.begin();
  c.pop_front();
  sink(*it);
}
void f_list_pop_front_it_guarda(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.pop_front();
  sink(*it);
}
void f_list_pop_front_it_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.pop_front();
    sink(*it);
  }
}
void f_list_pop_front_it_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_list_pop_front(c);
  sink(*it);
}
void f_list_pop_front_ref_recto(std::list<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.pop_front();
  sink(h);
}
void f_list_pop_front_ref_guarda(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.pop_front();
  sink(h);
}
void f_list_pop_front_ref_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.pop_front();
    sink(h);
  }
}
void f_list_pop_front_ref_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_list_pop_front(c);
  sink(h);
}
void f_list_pop_front_ptr_recto(std::list<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.pop_front();
  sink(*h);
}
void f_list_pop_front_ptr_guarda(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.pop_front();
  sink(*h);
}
void f_list_pop_front_ptr_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.pop_front();
    sink(*h);
  }
}
void f_list_pop_front_ptr_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_list_pop_front(c);
  sink(*h);
}
void f_list_reverse_it_recto(std::list<int>& c) {
  auto it = c.begin();
  c.reverse();
  sink(*it);
}
void f_list_reverse_it_guarda(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.reverse();
  sink(*it);
}
void f_list_reverse_it_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.reverse();
    sink(*it);
  }
}
void f_list_reverse_it_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_list_reverse(c);
  sink(*it);
}
void f_list_reverse_ref_recto(std::list<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.reverse();
  sink(h);
}
void f_list_reverse_ref_guarda(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.reverse();
  sink(h);
}
void f_list_reverse_ref_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.reverse();
    sink(h);
  }
}
void f_list_reverse_ref_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_list_reverse(c);
  sink(h);
}
void f_list_reverse_ptr_recto(std::list<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.reverse();
  sink(*h);
}
void f_list_reverse_ptr_guarda(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.reverse();
  sink(*h);
}
void f_list_reverse_ptr_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.reverse();
    sink(*h);
  }
}
void f_list_reverse_ptr_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_list_reverse(c);
  sink(*h);
}
void f_list_sort_it_recto(std::list<int>& c) {
  auto it = c.begin();
  c.sort();
  sink(*it);
}
void f_list_sort_it_guarda(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.sort();
  sink(*it);
}
void f_list_sort_it_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.sort();
    sink(*it);
  }
}
void f_list_sort_it_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_list_sort(c);
  sink(*it);
}
void f_list_sort_ref_recto(std::list<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.sort();
  sink(h);
}
void f_list_sort_ref_guarda(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.sort();
  sink(h);
}
void f_list_sort_ref_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.sort();
    sink(h);
  }
}
void f_list_sort_ref_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_list_sort(c);
  sink(h);
}
void f_list_sort_ptr_recto(std::list<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.sort();
  sink(*h);
}
void f_list_sort_ptr_guarda(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.sort();
  sink(*h);
}
void f_list_sort_ptr_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.sort();
    sink(*h);
  }
}
void f_list_sort_ptr_llamada(std::list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_list_sort(c);
  sink(*h);
}
void f_flist_push_front_it_recto(std::forward_list<int>& c) {
  auto it = c.begin();
  c.push_front(1);
  sink(*it);
}
void f_flist_push_front_it_guarda(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.push_front(1);
  sink(*it);
}
void f_flist_push_front_it_bucle(std::forward_list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.push_front(1);
    sink(*it);
  }
}
void f_flist_push_front_it_llamada(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_flist_push_front(c);
  sink(*it);
}
void f_flist_push_front_ref_recto(std::forward_list<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.push_front(1);
  sink(h);
}
void f_flist_push_front_ref_guarda(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.push_front(1);
  sink(h);
}
void f_flist_push_front_ref_bucle(std::forward_list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.push_front(1);
    sink(h);
  }
}
void f_flist_push_front_ref_llamada(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_flist_push_front(c);
  sink(h);
}
void f_flist_push_front_ptr_recto(std::forward_list<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.push_front(1);
  sink(*h);
}
void f_flist_push_front_ptr_guarda(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.push_front(1);
  sink(*h);
}
void f_flist_push_front_ptr_bucle(std::forward_list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.push_front(1);
    sink(*h);
  }
}
void f_flist_push_front_ptr_llamada(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_flist_push_front(c);
  sink(*h);
}
void f_flist_insert_after_it_recto(std::forward_list<int>& c) {
  auto it = c.begin();
  c.insert_after(c.before_begin(),1);
  sink(*it);
}
void f_flist_insert_after_it_guarda(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.insert_after(c.before_begin(),1);
  sink(*it);
}
void f_flist_insert_after_it_bucle(std::forward_list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.insert_after(c.before_begin(),1);
    sink(*it);
  }
}
void f_flist_insert_after_it_llamada(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_flist_insert_after(c);
  sink(*it);
}
void f_flist_insert_after_ref_recto(std::forward_list<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.insert_after(c.before_begin(),1);
  sink(h);
}
void f_flist_insert_after_ref_guarda(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.insert_after(c.before_begin(),1);
  sink(h);
}
void f_flist_insert_after_ref_bucle(std::forward_list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.insert_after(c.before_begin(),1);
    sink(h);
  }
}
void f_flist_insert_after_ref_llamada(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_flist_insert_after(c);
  sink(h);
}
void f_flist_insert_after_ptr_recto(std::forward_list<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.insert_after(c.before_begin(),1);
  sink(*h);
}
void f_flist_insert_after_ptr_guarda(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.insert_after(c.before_begin(),1);
  sink(*h);
}
void f_flist_insert_after_ptr_bucle(std::forward_list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.insert_after(c.before_begin(),1);
    sink(*h);
  }
}
void f_flist_insert_after_ptr_llamada(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_flist_insert_after(c);
  sink(*h);
}
void f_flist_erase_after_it_recto(std::forward_list<int>& c) {
  auto it = c.begin();
  c.erase_after(c.before_begin());
  sink(*it);
}
void f_flist_erase_after_it_guarda(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.erase_after(c.before_begin());
  sink(*it);
}
void f_flist_erase_after_it_bucle(std::forward_list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.erase_after(c.before_begin());
    sink(*it);
  }
}
void f_flist_erase_after_it_llamada(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_flist_erase_after(c);
  sink(*it);
}
void f_flist_erase_after_ref_recto(std::forward_list<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.erase_after(c.before_begin());
  sink(h);
}
void f_flist_erase_after_ref_guarda(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.erase_after(c.before_begin());
  sink(h);
}
void f_flist_erase_after_ref_bucle(std::forward_list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.erase_after(c.before_begin());
    sink(h);
  }
}
void f_flist_erase_after_ref_llamada(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_flist_erase_after(c);
  sink(h);
}
void f_flist_erase_after_ptr_recto(std::forward_list<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.erase_after(c.before_begin());
  sink(*h);
}
void f_flist_erase_after_ptr_guarda(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.erase_after(c.before_begin());
  sink(*h);
}
void f_flist_erase_after_ptr_bucle(std::forward_list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.erase_after(c.before_begin());
    sink(*h);
  }
}
void f_flist_erase_after_ptr_llamada(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_flist_erase_after(c);
  sink(*h);
}
void f_flist_clear_it_recto(std::forward_list<int>& c) {
  auto it = c.begin();
  c.clear();
  sink(*it);
}
void f_flist_clear_it_guarda(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.clear();
  sink(*it);
}
void f_flist_clear_it_bucle(std::forward_list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.clear();
    sink(*it);
  }
}
void f_flist_clear_it_llamada(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_flist_clear(c);
  sink(*it);
}
void f_flist_clear_ref_recto(std::forward_list<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.clear();
  sink(h);
}
void f_flist_clear_ref_guarda(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.clear();
  sink(h);
}
void f_flist_clear_ref_bucle(std::forward_list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.clear();
    sink(h);
  }
}
void f_flist_clear_ref_llamada(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_flist_clear(c);
  sink(h);
}
void f_flist_clear_ptr_recto(std::forward_list<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.clear();
  sink(*h);
}
void f_flist_clear_ptr_guarda(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.clear();
  sink(*h);
}
void f_flist_clear_ptr_bucle(std::forward_list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.clear();
    sink(*h);
  }
}
void f_flist_clear_ptr_llamada(std::forward_list<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_flist_clear(c);
  sink(*h);
}
void f_set_insert_it_recto(std::set<int>& c) {
  auto it = c.begin();
  c.insert(99);
  sink(*it);
}
void f_set_insert_it_guarda(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.insert(99);
  sink(*it);
}
void f_set_insert_it_bucle(std::set<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.insert(99);
    sink(*it);
  }
}
void f_set_insert_it_llamada(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_set_insert(c);
  sink(*it);
}
void f_set_insert_ref_recto(std::set<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.insert(99);
  sink(h);
}
void f_set_insert_ref_guarda(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.insert(99);
  sink(h);
}
void f_set_insert_ref_bucle(std::set<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.insert(99);
    sink(h);
  }
}
void f_set_insert_ref_llamada(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_set_insert(c);
  sink(h);
}
void f_set_insert_ptr_recto(std::set<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.insert(99);
  sink(*h);
}
void f_set_insert_ptr_guarda(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.insert(99);
  sink(*h);
}
void f_set_insert_ptr_bucle(std::set<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.insert(99);
    sink(*h);
  }
}
void f_set_insert_ptr_llamada(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_set_insert(c);
  sink(*h);
}
void f_set_emplace_it_recto(std::set<int>& c) {
  auto it = c.begin();
  c.emplace(98);
  sink(*it);
}
void f_set_emplace_it_guarda(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.emplace(98);
  sink(*it);
}
void f_set_emplace_it_bucle(std::set<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.emplace(98);
    sink(*it);
  }
}
void f_set_emplace_it_llamada(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_set_emplace(c);
  sink(*it);
}
void f_set_emplace_ref_recto(std::set<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.emplace(98);
  sink(h);
}
void f_set_emplace_ref_guarda(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.emplace(98);
  sink(h);
}
void f_set_emplace_ref_bucle(std::set<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.emplace(98);
    sink(h);
  }
}
void f_set_emplace_ref_llamada(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_set_emplace(c);
  sink(h);
}
void f_set_emplace_ptr_recto(std::set<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.emplace(98);
  sink(*h);
}
void f_set_emplace_ptr_guarda(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.emplace(98);
  sink(*h);
}
void f_set_emplace_ptr_bucle(std::set<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.emplace(98);
    sink(*h);
  }
}
void f_set_emplace_ptr_llamada(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_set_emplace(c);
  sink(*h);
}
void f_set_erase_begin_it_recto(std::set<int>& c) {
  auto it = c.begin();
  c.erase(c.begin());
  sink(*it);
}
void f_set_erase_begin_it_guarda(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.erase(c.begin());
  sink(*it);
}
void f_set_erase_begin_it_bucle(std::set<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.erase(c.begin());
    sink(*it);
  }
}
void f_set_erase_begin_it_llamada(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_set_erase_begin(c);
  sink(*it);
}
void f_set_erase_begin_ref_recto(std::set<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.erase(c.begin());
  sink(h);
}
void f_set_erase_begin_ref_guarda(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.erase(c.begin());
  sink(h);
}
void f_set_erase_begin_ref_bucle(std::set<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.erase(c.begin());
    sink(h);
  }
}
void f_set_erase_begin_ref_llamada(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_set_erase_begin(c);
  sink(h);
}
void f_set_erase_begin_ptr_recto(std::set<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.erase(c.begin());
  sink(*h);
}
void f_set_erase_begin_ptr_guarda(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.erase(c.begin());
  sink(*h);
}
void f_set_erase_begin_ptr_bucle(std::set<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.erase(c.begin());
    sink(*h);
  }
}
void f_set_erase_begin_ptr_llamada(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_set_erase_begin(c);
  sink(*h);
}
void f_set_clear_it_recto(std::set<int>& c) {
  auto it = c.begin();
  c.clear();
  sink(*it);
}
void f_set_clear_it_guarda(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.clear();
  sink(*it);
}
void f_set_clear_it_bucle(std::set<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.clear();
    sink(*it);
  }
}
void f_set_clear_it_llamada(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_set_clear(c);
  sink(*it);
}
void f_set_clear_ref_recto(std::set<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.clear();
  sink(h);
}
void f_set_clear_ref_guarda(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.clear();
  sink(h);
}
void f_set_clear_ref_bucle(std::set<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.clear();
    sink(h);
  }
}
void f_set_clear_ref_llamada(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_set_clear(c);
  sink(h);
}
void f_set_clear_ptr_recto(std::set<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.clear();
  sink(*h);
}
void f_set_clear_ptr_guarda(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.clear();
  sink(*h);
}
void f_set_clear_ptr_bucle(std::set<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.clear();
    sink(*h);
  }
}
void f_set_clear_ptr_llamada(std::set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_set_clear(c);
  sink(*h);
}
void f_mset_insert_it_recto(std::multiset<int>& c) {
  auto it = c.begin();
  c.insert(99);
  sink(*it);
}
void f_mset_insert_it_guarda(std::multiset<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.insert(99);
  sink(*it);
}
void f_mset_insert_it_bucle(std::multiset<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.insert(99);
    sink(*it);
  }
}
void f_mset_insert_it_llamada(std::multiset<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_mset_insert(c);
  sink(*it);
}
void f_mset_insert_ref_recto(std::multiset<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.insert(99);
  sink(h);
}
void f_mset_insert_ref_guarda(std::multiset<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.insert(99);
  sink(h);
}
void f_mset_insert_ref_bucle(std::multiset<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.insert(99);
    sink(h);
  }
}
void f_mset_insert_ref_llamada(std::multiset<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_mset_insert(c);
  sink(h);
}
void f_mset_insert_ptr_recto(std::multiset<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.insert(99);
  sink(*h);
}
void f_mset_insert_ptr_guarda(std::multiset<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.insert(99);
  sink(*h);
}
void f_mset_insert_ptr_bucle(std::multiset<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.insert(99);
    sink(*h);
  }
}
void f_mset_insert_ptr_llamada(std::multiset<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_mset_insert(c);
  sink(*h);
}
void f_mset_erase_begin_it_recto(std::multiset<int>& c) {
  auto it = c.begin();
  c.erase(c.begin());
  sink(*it);
}
void f_mset_erase_begin_it_guarda(std::multiset<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.erase(c.begin());
  sink(*it);
}
void f_mset_erase_begin_it_bucle(std::multiset<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.erase(c.begin());
    sink(*it);
  }
}
void f_mset_erase_begin_it_llamada(std::multiset<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_mset_erase_begin(c);
  sink(*it);
}
void f_mset_erase_begin_ref_recto(std::multiset<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.erase(c.begin());
  sink(h);
}
void f_mset_erase_begin_ref_guarda(std::multiset<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.erase(c.begin());
  sink(h);
}
void f_mset_erase_begin_ref_bucle(std::multiset<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.erase(c.begin());
    sink(h);
  }
}
void f_mset_erase_begin_ref_llamada(std::multiset<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_mset_erase_begin(c);
  sink(h);
}
void f_mset_erase_begin_ptr_recto(std::multiset<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.erase(c.begin());
  sink(*h);
}
void f_mset_erase_begin_ptr_guarda(std::multiset<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.erase(c.begin());
  sink(*h);
}
void f_mset_erase_begin_ptr_bucle(std::multiset<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.erase(c.begin());
    sink(*h);
  }
}
void f_mset_erase_begin_ptr_llamada(std::multiset<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_mset_erase_begin(c);
  sink(*h);
}
void f_mset_clear_it_recto(std::multiset<int>& c) {
  auto it = c.begin();
  c.clear();
  sink(*it);
}
void f_mset_clear_it_guarda(std::multiset<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.clear();
  sink(*it);
}
void f_mset_clear_it_bucle(std::multiset<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.clear();
    sink(*it);
  }
}
void f_mset_clear_it_llamada(std::multiset<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_mset_clear(c);
  sink(*it);
}
void f_mset_clear_ref_recto(std::multiset<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.clear();
  sink(h);
}
void f_mset_clear_ref_guarda(std::multiset<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.clear();
  sink(h);
}
void f_mset_clear_ref_bucle(std::multiset<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.clear();
    sink(h);
  }
}
void f_mset_clear_ref_llamada(std::multiset<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_mset_clear(c);
  sink(h);
}
void f_mset_clear_ptr_recto(std::multiset<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.clear();
  sink(*h);
}
void f_mset_clear_ptr_guarda(std::multiset<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.clear();
  sink(*h);
}
void f_mset_clear_ptr_bucle(std::multiset<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.clear();
    sink(*h);
  }
}
void f_mset_clear_ptr_llamada(std::multiset<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_mset_clear(c);
  sink(*h);
}
void f_map_insert_it_recto(std::map<int,int>& c) {
  auto it = c.begin();
  c.insert({99,1});
  sink(it->second);
}
void f_map_insert_it_guarda(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.insert({99,1});
  sink(it->second);
}
void f_map_insert_it_bucle(std::map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.insert({99,1});
    sink(it->second);
  }
}
void f_map_insert_it_llamada(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_map_insert(c);
  sink(it->second);
}
void f_map_insert_ref_recto(std::map<int,int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.insert({99,1});
  sink(h.second);
}
void f_map_insert_ref_guarda(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.insert({99,1});
  sink(h.second);
}
void f_map_insert_ref_bucle(std::map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.insert({99,1});
    sink(h.second);
  }
}
void f_map_insert_ref_llamada(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_map_insert(c);
  sink(h.second);
}
void f_map_insert_ptr_recto(std::map<int,int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.insert({99,1});
  sink(h->second);
}
void f_map_insert_ptr_guarda(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.insert({99,1});
  sink(h->second);
}
void f_map_insert_ptr_bucle(std::map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.insert({99,1});
    sink(h->second);
  }
}
void f_map_insert_ptr_llamada(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_map_insert(c);
  sink(h->second);
}
void f_map_emplace_it_recto(std::map<int,int>& c) {
  auto it = c.begin();
  c.emplace(98,1);
  sink(it->second);
}
void f_map_emplace_it_guarda(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.emplace(98,1);
  sink(it->second);
}
void f_map_emplace_it_bucle(std::map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.emplace(98,1);
    sink(it->second);
  }
}
void f_map_emplace_it_llamada(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_map_emplace(c);
  sink(it->second);
}
void f_map_emplace_ref_recto(std::map<int,int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.emplace(98,1);
  sink(h.second);
}
void f_map_emplace_ref_guarda(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.emplace(98,1);
  sink(h.second);
}
void f_map_emplace_ref_bucle(std::map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.emplace(98,1);
    sink(h.second);
  }
}
void f_map_emplace_ref_llamada(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_map_emplace(c);
  sink(h.second);
}
void f_map_emplace_ptr_recto(std::map<int,int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.emplace(98,1);
  sink(h->second);
}
void f_map_emplace_ptr_guarda(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.emplace(98,1);
  sink(h->second);
}
void f_map_emplace_ptr_bucle(std::map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.emplace(98,1);
    sink(h->second);
  }
}
void f_map_emplace_ptr_llamada(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_map_emplace(c);
  sink(h->second);
}
void f_map_subscript_it_recto(std::map<int,int>& c) {
  auto it = c.begin();
  c[97]=1;
  sink(it->second);
}
void f_map_subscript_it_guarda(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c[97]=1;
  sink(it->second);
}
void f_map_subscript_it_bucle(std::map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c[97]=1;
    sink(it->second);
  }
}
void f_map_subscript_it_llamada(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_map_subscript(c);
  sink(it->second);
}
void f_map_subscript_ref_recto(std::map<int,int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c[97]=1;
  sink(h.second);
}
void f_map_subscript_ref_guarda(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c[97]=1;
  sink(h.second);
}
void f_map_subscript_ref_bucle(std::map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c[97]=1;
    sink(h.second);
  }
}
void f_map_subscript_ref_llamada(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_map_subscript(c);
  sink(h.second);
}
void f_map_subscript_ptr_recto(std::map<int,int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c[97]=1;
  sink(h->second);
}
void f_map_subscript_ptr_guarda(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c[97]=1;
  sink(h->second);
}
void f_map_subscript_ptr_bucle(std::map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c[97]=1;
    sink(h->second);
  }
}
void f_map_subscript_ptr_llamada(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_map_subscript(c);
  sink(h->second);
}
void f_map_erase_begin_it_recto(std::map<int,int>& c) {
  auto it = c.begin();
  c.erase(c.begin());
  sink(it->second);
}
void f_map_erase_begin_it_guarda(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.erase(c.begin());
  sink(it->second);
}
void f_map_erase_begin_it_bucle(std::map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.erase(c.begin());
    sink(it->second);
  }
}
void f_map_erase_begin_it_llamada(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_map_erase_begin(c);
  sink(it->second);
}
void f_map_erase_begin_ref_recto(std::map<int,int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.erase(c.begin());
  sink(h.second);
}
void f_map_erase_begin_ref_guarda(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.erase(c.begin());
  sink(h.second);
}
void f_map_erase_begin_ref_bucle(std::map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.erase(c.begin());
    sink(h.second);
  }
}
void f_map_erase_begin_ref_llamada(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_map_erase_begin(c);
  sink(h.second);
}
void f_map_erase_begin_ptr_recto(std::map<int,int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.erase(c.begin());
  sink(h->second);
}
void f_map_erase_begin_ptr_guarda(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.erase(c.begin());
  sink(h->second);
}
void f_map_erase_begin_ptr_bucle(std::map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.erase(c.begin());
    sink(h->second);
  }
}
void f_map_erase_begin_ptr_llamada(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_map_erase_begin(c);
  sink(h->second);
}
void f_map_clear_it_recto(std::map<int,int>& c) {
  auto it = c.begin();
  c.clear();
  sink(it->second);
}
void f_map_clear_it_guarda(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.clear();
  sink(it->second);
}
void f_map_clear_it_bucle(std::map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.clear();
    sink(it->second);
  }
}
void f_map_clear_it_llamada(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_map_clear(c);
  sink(it->second);
}
void f_map_clear_ref_recto(std::map<int,int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.clear();
  sink(h.second);
}
void f_map_clear_ref_guarda(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.clear();
  sink(h.second);
}
void f_map_clear_ref_bucle(std::map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.clear();
    sink(h.second);
  }
}
void f_map_clear_ref_llamada(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_map_clear(c);
  sink(h.second);
}
void f_map_clear_ptr_recto(std::map<int,int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.clear();
  sink(h->second);
}
void f_map_clear_ptr_guarda(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.clear();
  sink(h->second);
}
void f_map_clear_ptr_bucle(std::map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.clear();
    sink(h->second);
  }
}
void f_map_clear_ptr_llamada(std::map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_map_clear(c);
  sink(h->second);
}
void f_mmap_insert_it_recto(std::multimap<int,int>& c) {
  auto it = c.begin();
  c.insert({99,1});
  sink(it->second);
}
void f_mmap_insert_it_guarda(std::multimap<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.insert({99,1});
  sink(it->second);
}
void f_mmap_insert_it_bucle(std::multimap<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.insert({99,1});
    sink(it->second);
  }
}
void f_mmap_insert_it_llamada(std::multimap<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_mmap_insert(c);
  sink(it->second);
}
void f_mmap_insert_ref_recto(std::multimap<int,int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.insert({99,1});
  sink(h.second);
}
void f_mmap_insert_ref_guarda(std::multimap<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.insert({99,1});
  sink(h.second);
}
void f_mmap_insert_ref_bucle(std::multimap<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.insert({99,1});
    sink(h.second);
  }
}
void f_mmap_insert_ref_llamada(std::multimap<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_mmap_insert(c);
  sink(h.second);
}
void f_mmap_insert_ptr_recto(std::multimap<int,int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.insert({99,1});
  sink(h->second);
}
void f_mmap_insert_ptr_guarda(std::multimap<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.insert({99,1});
  sink(h->second);
}
void f_mmap_insert_ptr_bucle(std::multimap<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.insert({99,1});
    sink(h->second);
  }
}
void f_mmap_insert_ptr_llamada(std::multimap<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_mmap_insert(c);
  sink(h->second);
}
void f_mmap_erase_begin_it_recto(std::multimap<int,int>& c) {
  auto it = c.begin();
  c.erase(c.begin());
  sink(it->second);
}
void f_mmap_erase_begin_it_guarda(std::multimap<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.erase(c.begin());
  sink(it->second);
}
void f_mmap_erase_begin_it_bucle(std::multimap<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.erase(c.begin());
    sink(it->second);
  }
}
void f_mmap_erase_begin_it_llamada(std::multimap<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_mmap_erase_begin(c);
  sink(it->second);
}
void f_mmap_erase_begin_ref_recto(std::multimap<int,int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.erase(c.begin());
  sink(h.second);
}
void f_mmap_erase_begin_ref_guarda(std::multimap<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.erase(c.begin());
  sink(h.second);
}
void f_mmap_erase_begin_ref_bucle(std::multimap<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.erase(c.begin());
    sink(h.second);
  }
}
void f_mmap_erase_begin_ref_llamada(std::multimap<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_mmap_erase_begin(c);
  sink(h.second);
}
void f_mmap_erase_begin_ptr_recto(std::multimap<int,int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.erase(c.begin());
  sink(h->second);
}
void f_mmap_erase_begin_ptr_guarda(std::multimap<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.erase(c.begin());
  sink(h->second);
}
void f_mmap_erase_begin_ptr_bucle(std::multimap<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.erase(c.begin());
    sink(h->second);
  }
}
void f_mmap_erase_begin_ptr_llamada(std::multimap<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_mmap_erase_begin(c);
  sink(h->second);
}
void f_mmap_clear_it_recto(std::multimap<int,int>& c) {
  auto it = c.begin();
  c.clear();
  sink(it->second);
}
void f_mmap_clear_it_guarda(std::multimap<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.clear();
  sink(it->second);
}
void f_mmap_clear_it_bucle(std::multimap<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.clear();
    sink(it->second);
  }
}
void f_mmap_clear_it_llamada(std::multimap<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_mmap_clear(c);
  sink(it->second);
}
void f_mmap_clear_ref_recto(std::multimap<int,int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.clear();
  sink(h.second);
}
void f_mmap_clear_ref_guarda(std::multimap<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.clear();
  sink(h.second);
}
void f_mmap_clear_ref_bucle(std::multimap<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.clear();
    sink(h.second);
  }
}
void f_mmap_clear_ref_llamada(std::multimap<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_mmap_clear(c);
  sink(h.second);
}
void f_mmap_clear_ptr_recto(std::multimap<int,int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.clear();
  sink(h->second);
}
void f_mmap_clear_ptr_guarda(std::multimap<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.clear();
  sink(h->second);
}
void f_mmap_clear_ptr_bucle(std::multimap<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.clear();
    sink(h->second);
  }
}
void f_mmap_clear_ptr_llamada(std::multimap<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_mmap_clear(c);
  sink(h->second);
}
void f_uset_insert_it_recto(std::unordered_set<int>& c) {
  auto it = c.begin();
  c.insert(99);
  sink(*it);
}
void f_uset_insert_it_recto_reserva(std::unordered_set<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  c.insert(99);
  sink(*it);
}
void f_uset_insert_it_guarda(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.insert(99);
  sink(*it);
}
void f_uset_insert_it_guarda_reserva(std::unordered_set<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  c.insert(99);
  sink(*it);
}
void f_uset_insert_it_bucle(std::unordered_set<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.insert(99);
    sink(*it);
  }
}
void f_uset_insert_it_bucle_reserva(std::unordered_set<int>& c) {
  c.reserve(c.size() + 3);
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.insert(99);
    sink(*it);
  }
}
void f_uset_insert_it_llamada(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_uset_insert(c);
  sink(*it);
}
void f_uset_insert_it_llamada_reserva(std::unordered_set<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_uset_insert(c);
  sink(*it);
}
void f_uset_insert_ref_recto(std::unordered_set<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.insert(99);
  sink(h);
}
void f_uset_insert_ref_guarda(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.insert(99);
  sink(h);
}
void f_uset_insert_ref_bucle(std::unordered_set<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.insert(99);
    sink(h);
  }
}
void f_uset_insert_ref_bucle_reserva(std::unordered_set<int>& c) {
  c.reserve(c.size() + 3);
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.insert(99);
    sink(h);
  }
}
void f_uset_insert_ref_llamada(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_uset_insert(c);
  sink(h);
}
void f_uset_insert_ptr_recto(std::unordered_set<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.insert(99);
  sink(*h);
}
void f_uset_insert_ptr_guarda(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.insert(99);
  sink(*h);
}
void f_uset_insert_ptr_bucle(std::unordered_set<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.insert(99);
    sink(*h);
  }
}
void f_uset_insert_ptr_bucle_reserva(std::unordered_set<int>& c) {
  c.reserve(c.size() + 3);
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.insert(99);
    sink(*h);
  }
}
void f_uset_insert_ptr_llamada(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_uset_insert(c);
  sink(*h);
}
void f_uset_erase_begin_it_recto(std::unordered_set<int>& c) {
  auto it = c.begin();
  c.erase(c.begin());
  sink(*it);
}
void f_uset_erase_begin_it_guarda(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.erase(c.begin());
  sink(*it);
}
void f_uset_erase_begin_it_bucle(std::unordered_set<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.erase(c.begin());
    sink(*it);
  }
}
void f_uset_erase_begin_it_llamada(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_uset_erase_begin(c);
  sink(*it);
}
void f_uset_erase_begin_ref_recto(std::unordered_set<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.erase(c.begin());
  sink(h);
}
void f_uset_erase_begin_ref_guarda(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.erase(c.begin());
  sink(h);
}
void f_uset_erase_begin_ref_bucle(std::unordered_set<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.erase(c.begin());
    sink(h);
  }
}
void f_uset_erase_begin_ref_llamada(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_uset_erase_begin(c);
  sink(h);
}
void f_uset_erase_begin_ptr_recto(std::unordered_set<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.erase(c.begin());
  sink(*h);
}
void f_uset_erase_begin_ptr_guarda(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.erase(c.begin());
  sink(*h);
}
void f_uset_erase_begin_ptr_bucle(std::unordered_set<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.erase(c.begin());
    sink(*h);
  }
}
void f_uset_erase_begin_ptr_llamada(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_uset_erase_begin(c);
  sink(*h);
}
void f_uset_clear_it_recto(std::unordered_set<int>& c) {
  auto it = c.begin();
  c.clear();
  sink(*it);
}
void f_uset_clear_it_guarda(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.clear();
  sink(*it);
}
void f_uset_clear_it_bucle(std::unordered_set<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.clear();
    sink(*it);
  }
}
void f_uset_clear_it_llamada(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_uset_clear(c);
  sink(*it);
}
void f_uset_clear_ref_recto(std::unordered_set<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.clear();
  sink(h);
}
void f_uset_clear_ref_guarda(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.clear();
  sink(h);
}
void f_uset_clear_ref_bucle(std::unordered_set<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.clear();
    sink(h);
  }
}
void f_uset_clear_ref_llamada(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_uset_clear(c);
  sink(h);
}
void f_uset_clear_ptr_recto(std::unordered_set<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.clear();
  sink(*h);
}
void f_uset_clear_ptr_guarda(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.clear();
  sink(*h);
}
void f_uset_clear_ptr_bucle(std::unordered_set<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.clear();
    sink(*h);
  }
}
void f_uset_clear_ptr_llamada(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_uset_clear(c);
  sink(*h);
}
void f_uset_rehash_it_recto(std::unordered_set<int>& c) {
  auto it = c.begin();
  c.rehash(1024);
  sink(*it);
}
void f_uset_rehash_it_guarda(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.rehash(1024);
  sink(*it);
}
void f_uset_rehash_it_bucle(std::unordered_set<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.rehash(1024);
    sink(*it);
  }
}
void f_uset_rehash_it_llamada(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_uset_rehash(c);
  sink(*it);
}
void f_uset_rehash_ref_recto(std::unordered_set<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.rehash(1024);
  sink(h);
}
void f_uset_rehash_ref_guarda(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.rehash(1024);
  sink(h);
}
void f_uset_rehash_ref_bucle(std::unordered_set<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.rehash(1024);
    sink(h);
  }
}
void f_uset_rehash_ref_llamada(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_uset_rehash(c);
  sink(h);
}
void f_uset_rehash_ptr_recto(std::unordered_set<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.rehash(1024);
  sink(*h);
}
void f_uset_rehash_ptr_guarda(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.rehash(1024);
  sink(*h);
}
void f_uset_rehash_ptr_bucle(std::unordered_set<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.rehash(1024);
    sink(*h);
  }
}
void f_uset_rehash_ptr_llamada(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_uset_rehash(c);
  sink(*h);
}
void f_uset_reserve_it_recto(std::unordered_set<int>& c) {
  auto it = c.begin();
  c.reserve(1024);
  sink(*it);
}
void f_uset_reserve_it_guarda(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.reserve(1024);
  sink(*it);
}
void f_uset_reserve_it_bucle(std::unordered_set<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.reserve(1024);
    sink(*it);
  }
}
void f_uset_reserve_it_llamada(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_uset_reserve(c);
  sink(*it);
}
void f_uset_reserve_ref_recto(std::unordered_set<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.reserve(1024);
  sink(h);
}
void f_uset_reserve_ref_guarda(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.reserve(1024);
  sink(h);
}
void f_uset_reserve_ref_bucle(std::unordered_set<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.reserve(1024);
    sink(h);
  }
}
void f_uset_reserve_ref_llamada(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_uset_reserve(c);
  sink(h);
}
void f_uset_reserve_ptr_recto(std::unordered_set<int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.reserve(1024);
  sink(*h);
}
void f_uset_reserve_ptr_guarda(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.reserve(1024);
  sink(*h);
}
void f_uset_reserve_ptr_bucle(std::unordered_set<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.reserve(1024);
    sink(*h);
  }
}
void f_uset_reserve_ptr_llamada(std::unordered_set<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_uset_reserve(c);
  sink(*h);
}
void f_umap_insert_it_recto(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  c.insert({99,1});
  sink(it->second);
}
void f_umap_insert_it_recto_reserva(std::unordered_map<int,int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  c.insert({99,1});
  sink(it->second);
}
void f_umap_insert_it_guarda(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.insert({99,1});
  sink(it->second);
}
void f_umap_insert_it_guarda_reserva(std::unordered_map<int,int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  c.insert({99,1});
  sink(it->second);
}
void f_umap_insert_it_bucle(std::unordered_map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.insert({99,1});
    sink(it->second);
  }
}
void f_umap_insert_it_bucle_reserva(std::unordered_map<int,int>& c) {
  c.reserve(c.size() + 3);
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.insert({99,1});
    sink(it->second);
  }
}
void f_umap_insert_it_llamada(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_umap_insert(c);
  sink(it->second);
}
void f_umap_insert_it_llamada_reserva(std::unordered_map<int,int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_umap_insert(c);
  sink(it->second);
}
void f_umap_insert_ref_recto(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.insert({99,1});
  sink(h.second);
}
void f_umap_insert_ref_guarda(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.insert({99,1});
  sink(h.second);
}
void f_umap_insert_ref_bucle(std::unordered_map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.insert({99,1});
    sink(h.second);
  }
}
void f_umap_insert_ref_bucle_reserva(std::unordered_map<int,int>& c) {
  c.reserve(c.size() + 3);
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.insert({99,1});
    sink(h.second);
  }
}
void f_umap_insert_ref_llamada(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_umap_insert(c);
  sink(h.second);
}
void f_umap_insert_ptr_recto(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.insert({99,1});
  sink(h->second);
}
void f_umap_insert_ptr_guarda(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.insert({99,1});
  sink(h->second);
}
void f_umap_insert_ptr_bucle(std::unordered_map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.insert({99,1});
    sink(h->second);
  }
}
void f_umap_insert_ptr_bucle_reserva(std::unordered_map<int,int>& c) {
  c.reserve(c.size() + 3);
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.insert({99,1});
    sink(h->second);
  }
}
void f_umap_insert_ptr_llamada(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_umap_insert(c);
  sink(h->second);
}
void f_umap_subscript_it_recto(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  c[97]=1;
  sink(it->second);
}
void f_umap_subscript_it_recto_reserva(std::unordered_map<int,int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  c[97]=1;
  sink(it->second);
}
void f_umap_subscript_it_guarda(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c[97]=1;
  sink(it->second);
}
void f_umap_subscript_it_guarda_reserva(std::unordered_map<int,int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  c[97]=1;
  sink(it->second);
}
void f_umap_subscript_it_bucle(std::unordered_map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c[97]=1;
    sink(it->second);
  }
}
void f_umap_subscript_it_bucle_reserva(std::unordered_map<int,int>& c) {
  c.reserve(c.size() + 3);
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c[97]=1;
    sink(it->second);
  }
}
void f_umap_subscript_it_llamada(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_umap_subscript(c);
  sink(it->second);
}
void f_umap_subscript_it_llamada_reserva(std::unordered_map<int,int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_umap_subscript(c);
  sink(it->second);
}
void f_umap_subscript_ref_recto(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c[97]=1;
  sink(h.second);
}
void f_umap_subscript_ref_guarda(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c[97]=1;
  sink(h.second);
}
void f_umap_subscript_ref_bucle(std::unordered_map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c[97]=1;
    sink(h.second);
  }
}
void f_umap_subscript_ref_bucle_reserva(std::unordered_map<int,int>& c) {
  c.reserve(c.size() + 3);
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c[97]=1;
    sink(h.second);
  }
}
void f_umap_subscript_ref_llamada(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_umap_subscript(c);
  sink(h.second);
}
void f_umap_subscript_ptr_recto(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c[97]=1;
  sink(h->second);
}
void f_umap_subscript_ptr_guarda(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c[97]=1;
  sink(h->second);
}
void f_umap_subscript_ptr_bucle(std::unordered_map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c[97]=1;
    sink(h->second);
  }
}
void f_umap_subscript_ptr_bucle_reserva(std::unordered_map<int,int>& c) {
  c.reserve(c.size() + 3);
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c[97]=1;
    sink(h->second);
  }
}
void f_umap_subscript_ptr_llamada(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_umap_subscript(c);
  sink(h->second);
}
void f_umap_erase_begin_it_recto(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  c.erase(c.begin());
  sink(it->second);
}
void f_umap_erase_begin_it_guarda(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.erase(c.begin());
  sink(it->second);
}
void f_umap_erase_begin_it_bucle(std::unordered_map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.erase(c.begin());
    sink(it->second);
  }
}
void f_umap_erase_begin_it_llamada(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_umap_erase_begin(c);
  sink(it->second);
}
void f_umap_erase_begin_ref_recto(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.erase(c.begin());
  sink(h.second);
}
void f_umap_erase_begin_ref_guarda(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.erase(c.begin());
  sink(h.second);
}
void f_umap_erase_begin_ref_bucle(std::unordered_map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.erase(c.begin());
    sink(h.second);
  }
}
void f_umap_erase_begin_ref_llamada(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_umap_erase_begin(c);
  sink(h.second);
}
void f_umap_erase_begin_ptr_recto(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.erase(c.begin());
  sink(h->second);
}
void f_umap_erase_begin_ptr_guarda(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.erase(c.begin());
  sink(h->second);
}
void f_umap_erase_begin_ptr_bucle(std::unordered_map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.erase(c.begin());
    sink(h->second);
  }
}
void f_umap_erase_begin_ptr_llamada(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_umap_erase_begin(c);
  sink(h->second);
}
void f_umap_clear_it_recto(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  c.clear();
  sink(it->second);
}
void f_umap_clear_it_guarda(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.clear();
  sink(it->second);
}
void f_umap_clear_it_bucle(std::unordered_map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.clear();
    sink(it->second);
  }
}
void f_umap_clear_it_llamada(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_umap_clear(c);
  sink(it->second);
}
void f_umap_clear_ref_recto(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.clear();
  sink(h.second);
}
void f_umap_clear_ref_guarda(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.clear();
  sink(h.second);
}
void f_umap_clear_ref_bucle(std::unordered_map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.clear();
    sink(h.second);
  }
}
void f_umap_clear_ref_llamada(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_umap_clear(c);
  sink(h.second);
}
void f_umap_clear_ptr_recto(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.clear();
  sink(h->second);
}
void f_umap_clear_ptr_guarda(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.clear();
  sink(h->second);
}
void f_umap_clear_ptr_bucle(std::unordered_map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.clear();
    sink(h->second);
  }
}
void f_umap_clear_ptr_llamada(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_umap_clear(c);
  sink(h->second);
}
void f_umap_rehash_it_recto(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  c.rehash(1024);
  sink(it->second);
}
void f_umap_rehash_it_guarda(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.rehash(1024);
  sink(it->second);
}
void f_umap_rehash_it_bucle(std::unordered_map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    c.rehash(1024);
    sink(it->second);
  }
}
void f_umap_rehash_it_llamada(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  mutar_umap_rehash(c);
  sink(it->second);
}
void f_umap_rehash_ref_recto(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.rehash(1024);
  sink(h.second);
}
void f_umap_rehash_ref_guarda(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  c.rehash(1024);
  sink(h.second);
}
void f_umap_rehash_ref_bucle(std::unordered_map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.rehash(1024);
    sink(h.second);
  }
}
void f_umap_rehash_ref_llamada(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_umap_rehash(c);
  sink(h.second);
}
void f_umap_rehash_ptr_recto(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  const auto* h = &*it;
  c.rehash(1024);
  sink(h->second);
}
void f_umap_rehash_ptr_guarda(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  c.rehash(1024);
  sink(h->second);
}
void f_umap_rehash_ptr_bucle(std::unordered_map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto* h = &*it;
    c.rehash(1024);
    sink(h->second);
  }
}
void f_umap_rehash_ptr_llamada(std::unordered_map<int,int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto* h = &*it;
  mutar_umap_rehash(c);
  sink(h->second);
}
void f_vector_erase_ret_it_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3;) {
    it = c.erase(it);
    if (it != c.end()) sink(*it);
  }
}
void f_deque_erase_ret_it_bucle(std::deque<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3;) {
    it = c.erase(it);
    if (it != c.end()) sink(*it);
  }
}
void f_list_erase_ret_it_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3;) {
    it = c.erase(it);
    if (it != c.end()) sink(*it);
  }
}
void f_set_erase_ret_it_bucle(std::set<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3;) {
    it = c.erase(it);
    if (it != c.end()) sink(*it);
  }
}
void f_mset_erase_ret_it_bucle(std::multiset<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3;) {
    it = c.erase(it);
    if (it != c.end()) sink(*it);
  }
}
void f_map_erase_ret_it_bucle(std::map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3;) {
    it = c.erase(it);
    if (it != c.end()) sink(it->second);
  }
}
void f_mmap_erase_ret_it_bucle(std::multimap<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3;) {
    it = c.erase(it);
    if (it != c.end()) sink(it->second);
  }
}
void f_uset_erase_ret_it_bucle(std::unordered_set<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3;) {
    it = c.erase(it);
    if (it != c.end()) sink(*it);
  }
}
void f_umap_erase_ret_it_bucle(std::unordered_map<int,int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3;) {
    it = c.erase(it);
    if (it != c.end()) sink(it->second);
  }
}
void f_vector_insert_ret_it_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3;) {
    it = c.insert(it, 1); ++it;
    if (it != c.end()) sink(*it);
  }
}
void f_deque_insert_ret_it_bucle(std::deque<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3;) {
    it = c.insert(it, 1); ++it;
    if (it != c.end()) sink(*it);
  }
}
void f_list_insert_ret_it_bucle(std::list<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3;) {
    it = c.insert(it, 1); ++it;
    if (it != c.end()) sink(*it);
  }
}
