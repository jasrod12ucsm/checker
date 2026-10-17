// GENERADO por bench/gen_runtime_harness.py — no editar a mano
#include <cstdlib>
#include <cstring>
#include <string_view>

volatile int runtime_sink = 0;
void sink(int value) { runtime_sink ^= value; }
void sink(char value) { runtime_sink ^= static_cast<unsigned char>(value); }
void sink(const void *value) { runtime_sink ^= value != nullptr; }

#include "corpus.cpp"

enum class Mode { Natural, ForceInvalidation, PreserveValidity };

Mode parse_mode(const char *arg) {
  if (std::strcmp(arg, "force") == 0) return Mode::ForceInvalidation;
  if (std::strcmp(arg, "preserve") == 0) return Mode::PreserveValidity;
  return Mode::Natural;
}

std::vector<int> make_vector(Mode mode, std::string_view op) {
  std::vector<int> c;
  if (mode == Mode::ForceInvalidation && op == "pop_back") { c.push_back(1); return c; }
  // shrink_to_fit es una solicitud no vinculante: se prepara holgura para
  // observar la decisión de esta implementación, no para imponerla.
  if (op == "shrink_to_fit") {
    if (mode == Mode::ForceInvalidation) c.reserve(256);
    c.push_back(1); c.push_back(2); c.push_back(3);
    if (mode == Mode::PreserveValidity) c.shrink_to_fit();
    return c;
  }
  if (mode == Mode::ForceInvalidation) {
    c.reserve(8);
    while (c.size() < c.capacity()) c.push_back(static_cast<int>(c.size() + 1));
    return c;
  }
  // resize_grow y reserve solicitan size()+100; 256 hace que esa solicitud
  // no exceda la capacidad de la configuración de preservación.
  if (mode == Mode::PreserveValidity) c.reserve(256);
  c.push_back(1); c.push_back(2); c.push_back(3);
  return c;
}

std::deque<int> make_deque(Mode, std::string_view) { return {1, 2, 3}; }
std::list<int> make_list(Mode, std::string_view) { return {1, 2, 3}; }
std::forward_list<int> make_flist(Mode, std::string_view) { return {1, 2, 3}; }

std::set<int> make_set(Mode, std::string_view) { return {1, 2, 3}; }
std::multiset<int> make_mset(Mode, std::string_view) { return {1, 2, 3}; }
std::map<int, int> make_map(Mode, std::string_view) { return {{1,1}, {2,2}, {3,3}}; }
std::multimap<int, int> make_mmap(Mode, std::string_view) { return {{1,1}, {2,2}, {3,3}}; }

std::unordered_set<int> make_uset(Mode mode, std::string_view) {
  std::unordered_set<int> c;
  if (mode == Mode::ForceInvalidation) {
    c.max_load_factor(1.0f); c.rehash(8);
    for (std::size_t i = 0; i < c.bucket_count(); ++i) c.insert(static_cast<int>(i));
  } else { c.reserve(256); c.insert(1); c.insert(2); c.insert(3); }
  return c;
}
std::unordered_map<int, int> make_umap(Mode mode, std::string_view) {
  std::unordered_map<int, int> c;
  if (mode == Mode::ForceInvalidation) {
    c.max_load_factor(1.0f); c.rehash(8);
    for (std::size_t i = 0; i < c.bucket_count(); ++i) c.emplace(static_cast<int>(i), 1);
  } else { c.reserve(256); c.emplace(1,1); c.emplace(2,2); c.emplace(3,3); }
  return c;
}

int main(int argc, char **argv) {
  if (argc != 3) return 64;
  const std::string_view id(argv[1]);
  const Mode mode = parse_mode(argv[2]);
  if (id == "f_vector_push_back_it_recto") {
    std::vector<int> c = make_vector(mode, "push_back");
    f_vector_push_back_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_push_back_it_guarda") {
    std::vector<int> c = make_vector(mode, "push_back");
    f_vector_push_back_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_push_back_it_bucle") {
    std::vector<int> c = make_vector(mode, "push_back");
    f_vector_push_back_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_push_back_it_llamada") {
    std::vector<int> c = make_vector(mode, "push_back");
    f_vector_push_back_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_push_back_ref_recto") {
    std::vector<int> c = make_vector(mode, "push_back");
    f_vector_push_back_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_push_back_ref_guarda") {
    std::vector<int> c = make_vector(mode, "push_back");
    f_vector_push_back_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_push_back_ref_bucle") {
    std::vector<int> c = make_vector(mode, "push_back");
    f_vector_push_back_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_push_back_ref_llamada") {
    std::vector<int> c = make_vector(mode, "push_back");
    f_vector_push_back_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_push_back_ptr_recto") {
    std::vector<int> c = make_vector(mode, "push_back");
    f_vector_push_back_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_push_back_ptr_guarda") {
    std::vector<int> c = make_vector(mode, "push_back");
    f_vector_push_back_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_push_back_ptr_bucle") {
    std::vector<int> c = make_vector(mode, "push_back");
    f_vector_push_back_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_push_back_ptr_llamada") {
    std::vector<int> c = make_vector(mode, "push_back");
    f_vector_push_back_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_emplace_back_it_recto") {
    std::vector<int> c = make_vector(mode, "emplace_back");
    f_vector_emplace_back_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_emplace_back_it_guarda") {
    std::vector<int> c = make_vector(mode, "emplace_back");
    f_vector_emplace_back_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_emplace_back_it_bucle") {
    std::vector<int> c = make_vector(mode, "emplace_back");
    f_vector_emplace_back_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_emplace_back_it_llamada") {
    std::vector<int> c = make_vector(mode, "emplace_back");
    f_vector_emplace_back_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_emplace_back_ref_recto") {
    std::vector<int> c = make_vector(mode, "emplace_back");
    f_vector_emplace_back_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_emplace_back_ref_guarda") {
    std::vector<int> c = make_vector(mode, "emplace_back");
    f_vector_emplace_back_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_emplace_back_ref_bucle") {
    std::vector<int> c = make_vector(mode, "emplace_back");
    f_vector_emplace_back_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_emplace_back_ref_llamada") {
    std::vector<int> c = make_vector(mode, "emplace_back");
    f_vector_emplace_back_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_emplace_back_ptr_recto") {
    std::vector<int> c = make_vector(mode, "emplace_back");
    f_vector_emplace_back_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_emplace_back_ptr_guarda") {
    std::vector<int> c = make_vector(mode, "emplace_back");
    f_vector_emplace_back_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_emplace_back_ptr_bucle") {
    std::vector<int> c = make_vector(mode, "emplace_back");
    f_vector_emplace_back_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_emplace_back_ptr_llamada") {
    std::vector<int> c = make_vector(mode, "emplace_back");
    f_vector_emplace_back_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_insert_begin_it_recto") {
    std::vector<int> c = make_vector(mode, "insert_begin");
    f_vector_insert_begin_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_insert_begin_it_guarda") {
    std::vector<int> c = make_vector(mode, "insert_begin");
    f_vector_insert_begin_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_insert_begin_it_bucle") {
    std::vector<int> c = make_vector(mode, "insert_begin");
    f_vector_insert_begin_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_insert_begin_it_llamada") {
    std::vector<int> c = make_vector(mode, "insert_begin");
    f_vector_insert_begin_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_insert_begin_ref_recto") {
    std::vector<int> c = make_vector(mode, "insert_begin");
    f_vector_insert_begin_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_insert_begin_ref_guarda") {
    std::vector<int> c = make_vector(mode, "insert_begin");
    f_vector_insert_begin_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_insert_begin_ref_bucle") {
    std::vector<int> c = make_vector(mode, "insert_begin");
    f_vector_insert_begin_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_insert_begin_ref_llamada") {
    std::vector<int> c = make_vector(mode, "insert_begin");
    f_vector_insert_begin_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_insert_begin_ptr_recto") {
    std::vector<int> c = make_vector(mode, "insert_begin");
    f_vector_insert_begin_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_insert_begin_ptr_guarda") {
    std::vector<int> c = make_vector(mode, "insert_begin");
    f_vector_insert_begin_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_insert_begin_ptr_bucle") {
    std::vector<int> c = make_vector(mode, "insert_begin");
    f_vector_insert_begin_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_insert_begin_ptr_llamada") {
    std::vector<int> c = make_vector(mode, "insert_begin");
    f_vector_insert_begin_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_insert_end_it_recto") {
    std::vector<int> c = make_vector(mode, "insert_end");
    f_vector_insert_end_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_insert_end_it_guarda") {
    std::vector<int> c = make_vector(mode, "insert_end");
    f_vector_insert_end_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_insert_end_it_bucle") {
    std::vector<int> c = make_vector(mode, "insert_end");
    f_vector_insert_end_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_insert_end_it_llamada") {
    std::vector<int> c = make_vector(mode, "insert_end");
    f_vector_insert_end_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_insert_end_ref_recto") {
    std::vector<int> c = make_vector(mode, "insert_end");
    f_vector_insert_end_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_insert_end_ref_guarda") {
    std::vector<int> c = make_vector(mode, "insert_end");
    f_vector_insert_end_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_insert_end_ref_bucle") {
    std::vector<int> c = make_vector(mode, "insert_end");
    f_vector_insert_end_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_insert_end_ref_llamada") {
    std::vector<int> c = make_vector(mode, "insert_end");
    f_vector_insert_end_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_insert_end_ptr_recto") {
    std::vector<int> c = make_vector(mode, "insert_end");
    f_vector_insert_end_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_insert_end_ptr_guarda") {
    std::vector<int> c = make_vector(mode, "insert_end");
    f_vector_insert_end_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_insert_end_ptr_bucle") {
    std::vector<int> c = make_vector(mode, "insert_end");
    f_vector_insert_end_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_insert_end_ptr_llamada") {
    std::vector<int> c = make_vector(mode, "insert_end");
    f_vector_insert_end_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_erase_begin_it_recto") {
    std::vector<int> c = make_vector(mode, "erase_begin");
    f_vector_erase_begin_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_erase_begin_it_guarda") {
    std::vector<int> c = make_vector(mode, "erase_begin");
    f_vector_erase_begin_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_erase_begin_it_bucle") {
    std::vector<int> c = make_vector(mode, "erase_begin");
    f_vector_erase_begin_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_erase_begin_it_llamada") {
    std::vector<int> c = make_vector(mode, "erase_begin");
    f_vector_erase_begin_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_erase_begin_ref_recto") {
    std::vector<int> c = make_vector(mode, "erase_begin");
    f_vector_erase_begin_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_erase_begin_ref_guarda") {
    std::vector<int> c = make_vector(mode, "erase_begin");
    f_vector_erase_begin_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_erase_begin_ref_bucle") {
    std::vector<int> c = make_vector(mode, "erase_begin");
    f_vector_erase_begin_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_erase_begin_ref_llamada") {
    std::vector<int> c = make_vector(mode, "erase_begin");
    f_vector_erase_begin_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_erase_begin_ptr_recto") {
    std::vector<int> c = make_vector(mode, "erase_begin");
    f_vector_erase_begin_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_erase_begin_ptr_guarda") {
    std::vector<int> c = make_vector(mode, "erase_begin");
    f_vector_erase_begin_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_erase_begin_ptr_bucle") {
    std::vector<int> c = make_vector(mode, "erase_begin");
    f_vector_erase_begin_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_erase_begin_ptr_llamada") {
    std::vector<int> c = make_vector(mode, "erase_begin");
    f_vector_erase_begin_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_clear_it_recto") {
    std::vector<int> c = make_vector(mode, "clear");
    f_vector_clear_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_clear_it_guarda") {
    std::vector<int> c = make_vector(mode, "clear");
    f_vector_clear_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_clear_it_bucle") {
    std::vector<int> c = make_vector(mode, "clear");
    f_vector_clear_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_clear_it_llamada") {
    std::vector<int> c = make_vector(mode, "clear");
    f_vector_clear_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_clear_ref_recto") {
    std::vector<int> c = make_vector(mode, "clear");
    f_vector_clear_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_clear_ref_guarda") {
    std::vector<int> c = make_vector(mode, "clear");
    f_vector_clear_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_clear_ref_bucle") {
    std::vector<int> c = make_vector(mode, "clear");
    f_vector_clear_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_clear_ref_llamada") {
    std::vector<int> c = make_vector(mode, "clear");
    f_vector_clear_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_clear_ptr_recto") {
    std::vector<int> c = make_vector(mode, "clear");
    f_vector_clear_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_clear_ptr_guarda") {
    std::vector<int> c = make_vector(mode, "clear");
    f_vector_clear_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_clear_ptr_bucle") {
    std::vector<int> c = make_vector(mode, "clear");
    f_vector_clear_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_clear_ptr_llamada") {
    std::vector<int> c = make_vector(mode, "clear");
    f_vector_clear_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_resize_grow_it_recto") {
    std::vector<int> c = make_vector(mode, "resize_grow");
    f_vector_resize_grow_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_resize_grow_it_guarda") {
    std::vector<int> c = make_vector(mode, "resize_grow");
    f_vector_resize_grow_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_resize_grow_it_bucle") {
    std::vector<int> c = make_vector(mode, "resize_grow");
    f_vector_resize_grow_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_resize_grow_it_llamada") {
    std::vector<int> c = make_vector(mode, "resize_grow");
    f_vector_resize_grow_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_resize_grow_ref_recto") {
    std::vector<int> c = make_vector(mode, "resize_grow");
    f_vector_resize_grow_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_resize_grow_ref_guarda") {
    std::vector<int> c = make_vector(mode, "resize_grow");
    f_vector_resize_grow_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_resize_grow_ref_bucle") {
    std::vector<int> c = make_vector(mode, "resize_grow");
    f_vector_resize_grow_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_resize_grow_ref_llamada") {
    std::vector<int> c = make_vector(mode, "resize_grow");
    f_vector_resize_grow_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_resize_grow_ptr_recto") {
    std::vector<int> c = make_vector(mode, "resize_grow");
    f_vector_resize_grow_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_resize_grow_ptr_guarda") {
    std::vector<int> c = make_vector(mode, "resize_grow");
    f_vector_resize_grow_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_resize_grow_ptr_bucle") {
    std::vector<int> c = make_vector(mode, "resize_grow");
    f_vector_resize_grow_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_resize_grow_ptr_llamada") {
    std::vector<int> c = make_vector(mode, "resize_grow");
    f_vector_resize_grow_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_reserve_it_recto") {
    std::vector<int> c = make_vector(mode, "reserve");
    f_vector_reserve_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_reserve_it_guarda") {
    std::vector<int> c = make_vector(mode, "reserve");
    f_vector_reserve_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_reserve_it_bucle") {
    std::vector<int> c = make_vector(mode, "reserve");
    f_vector_reserve_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_reserve_it_llamada") {
    std::vector<int> c = make_vector(mode, "reserve");
    f_vector_reserve_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_reserve_ref_recto") {
    std::vector<int> c = make_vector(mode, "reserve");
    f_vector_reserve_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_reserve_ref_guarda") {
    std::vector<int> c = make_vector(mode, "reserve");
    f_vector_reserve_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_reserve_ref_bucle") {
    std::vector<int> c = make_vector(mode, "reserve");
    f_vector_reserve_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_reserve_ref_llamada") {
    std::vector<int> c = make_vector(mode, "reserve");
    f_vector_reserve_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_reserve_ptr_recto") {
    std::vector<int> c = make_vector(mode, "reserve");
    f_vector_reserve_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_reserve_ptr_guarda") {
    std::vector<int> c = make_vector(mode, "reserve");
    f_vector_reserve_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_reserve_ptr_bucle") {
    std::vector<int> c = make_vector(mode, "reserve");
    f_vector_reserve_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_reserve_ptr_llamada") {
    std::vector<int> c = make_vector(mode, "reserve");
    f_vector_reserve_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_shrink_to_fit_it_recto") {
    std::vector<int> c = make_vector(mode, "shrink_to_fit");
    f_vector_shrink_to_fit_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_shrink_to_fit_it_guarda") {
    std::vector<int> c = make_vector(mode, "shrink_to_fit");
    f_vector_shrink_to_fit_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_shrink_to_fit_it_bucle") {
    std::vector<int> c = make_vector(mode, "shrink_to_fit");
    f_vector_shrink_to_fit_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_shrink_to_fit_it_llamada") {
    std::vector<int> c = make_vector(mode, "shrink_to_fit");
    f_vector_shrink_to_fit_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_shrink_to_fit_ref_recto") {
    std::vector<int> c = make_vector(mode, "shrink_to_fit");
    f_vector_shrink_to_fit_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_shrink_to_fit_ref_guarda") {
    std::vector<int> c = make_vector(mode, "shrink_to_fit");
    f_vector_shrink_to_fit_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_shrink_to_fit_ref_bucle") {
    std::vector<int> c = make_vector(mode, "shrink_to_fit");
    f_vector_shrink_to_fit_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_shrink_to_fit_ref_llamada") {
    std::vector<int> c = make_vector(mode, "shrink_to_fit");
    f_vector_shrink_to_fit_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_shrink_to_fit_ptr_recto") {
    std::vector<int> c = make_vector(mode, "shrink_to_fit");
    f_vector_shrink_to_fit_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_shrink_to_fit_ptr_guarda") {
    std::vector<int> c = make_vector(mode, "shrink_to_fit");
    f_vector_shrink_to_fit_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_shrink_to_fit_ptr_bucle") {
    std::vector<int> c = make_vector(mode, "shrink_to_fit");
    f_vector_shrink_to_fit_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_shrink_to_fit_ptr_llamada") {
    std::vector<int> c = make_vector(mode, "shrink_to_fit");
    f_vector_shrink_to_fit_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_assign_it_recto") {
    std::vector<int> c = make_vector(mode, "assign");
    f_vector_assign_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_assign_it_guarda") {
    std::vector<int> c = make_vector(mode, "assign");
    f_vector_assign_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_assign_it_bucle") {
    std::vector<int> c = make_vector(mode, "assign");
    f_vector_assign_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_assign_it_llamada") {
    std::vector<int> c = make_vector(mode, "assign");
    f_vector_assign_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_assign_ref_recto") {
    std::vector<int> c = make_vector(mode, "assign");
    f_vector_assign_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_assign_ref_guarda") {
    std::vector<int> c = make_vector(mode, "assign");
    f_vector_assign_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_assign_ref_bucle") {
    std::vector<int> c = make_vector(mode, "assign");
    f_vector_assign_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_assign_ref_llamada") {
    std::vector<int> c = make_vector(mode, "assign");
    f_vector_assign_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_assign_ptr_recto") {
    std::vector<int> c = make_vector(mode, "assign");
    f_vector_assign_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_assign_ptr_guarda") {
    std::vector<int> c = make_vector(mode, "assign");
    f_vector_assign_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_assign_ptr_bucle") {
    std::vector<int> c = make_vector(mode, "assign");
    f_vector_assign_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_assign_ptr_llamada") {
    std::vector<int> c = make_vector(mode, "assign");
    f_vector_assign_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_pop_back_it_recto") {
    std::vector<int> c = make_vector(mode, "pop_back");
    f_vector_pop_back_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_pop_back_it_guarda") {
    std::vector<int> c = make_vector(mode, "pop_back");
    f_vector_pop_back_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_pop_back_it_bucle") {
    std::vector<int> c = make_vector(mode, "pop_back");
    f_vector_pop_back_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_pop_back_it_llamada") {
    std::vector<int> c = make_vector(mode, "pop_back");
    f_vector_pop_back_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_pop_back_ref_recto") {
    std::vector<int> c = make_vector(mode, "pop_back");
    f_vector_pop_back_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_pop_back_ref_guarda") {
    std::vector<int> c = make_vector(mode, "pop_back");
    f_vector_pop_back_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_pop_back_ref_bucle") {
    std::vector<int> c = make_vector(mode, "pop_back");
    f_vector_pop_back_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_pop_back_ref_llamada") {
    std::vector<int> c = make_vector(mode, "pop_back");
    f_vector_pop_back_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_pop_back_ptr_recto") {
    std::vector<int> c = make_vector(mode, "pop_back");
    f_vector_pop_back_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_pop_back_ptr_guarda") {
    std::vector<int> c = make_vector(mode, "pop_back");
    f_vector_pop_back_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_pop_back_ptr_bucle") {
    std::vector<int> c = make_vector(mode, "pop_back");
    f_vector_pop_back_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_vector_pop_back_ptr_llamada") {
    std::vector<int> c = make_vector(mode, "pop_back");
    f_vector_pop_back_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_push_back_it_recto") {
    std::deque<int> c = make_deque(mode, "push_back");
    f_deque_push_back_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_push_back_it_guarda") {
    std::deque<int> c = make_deque(mode, "push_back");
    f_deque_push_back_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_push_back_it_bucle") {
    std::deque<int> c = make_deque(mode, "push_back");
    f_deque_push_back_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_push_back_it_llamada") {
    std::deque<int> c = make_deque(mode, "push_back");
    f_deque_push_back_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_push_back_ref_recto") {
    std::deque<int> c = make_deque(mode, "push_back");
    f_deque_push_back_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_push_back_ref_guarda") {
    std::deque<int> c = make_deque(mode, "push_back");
    f_deque_push_back_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_push_back_ref_bucle") {
    std::deque<int> c = make_deque(mode, "push_back");
    f_deque_push_back_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_push_back_ref_llamada") {
    std::deque<int> c = make_deque(mode, "push_back");
    f_deque_push_back_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_push_back_ptr_recto") {
    std::deque<int> c = make_deque(mode, "push_back");
    f_deque_push_back_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_push_back_ptr_guarda") {
    std::deque<int> c = make_deque(mode, "push_back");
    f_deque_push_back_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_push_back_ptr_bucle") {
    std::deque<int> c = make_deque(mode, "push_back");
    f_deque_push_back_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_push_back_ptr_llamada") {
    std::deque<int> c = make_deque(mode, "push_back");
    f_deque_push_back_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_push_front_it_recto") {
    std::deque<int> c = make_deque(mode, "push_front");
    f_deque_push_front_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_push_front_it_guarda") {
    std::deque<int> c = make_deque(mode, "push_front");
    f_deque_push_front_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_push_front_it_bucle") {
    std::deque<int> c = make_deque(mode, "push_front");
    f_deque_push_front_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_push_front_it_llamada") {
    std::deque<int> c = make_deque(mode, "push_front");
    f_deque_push_front_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_push_front_ref_recto") {
    std::deque<int> c = make_deque(mode, "push_front");
    f_deque_push_front_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_push_front_ref_guarda") {
    std::deque<int> c = make_deque(mode, "push_front");
    f_deque_push_front_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_push_front_ref_bucle") {
    std::deque<int> c = make_deque(mode, "push_front");
    f_deque_push_front_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_push_front_ref_llamada") {
    std::deque<int> c = make_deque(mode, "push_front");
    f_deque_push_front_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_push_front_ptr_recto") {
    std::deque<int> c = make_deque(mode, "push_front");
    f_deque_push_front_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_push_front_ptr_guarda") {
    std::deque<int> c = make_deque(mode, "push_front");
    f_deque_push_front_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_push_front_ptr_bucle") {
    std::deque<int> c = make_deque(mode, "push_front");
    f_deque_push_front_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_push_front_ptr_llamada") {
    std::deque<int> c = make_deque(mode, "push_front");
    f_deque_push_front_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_emplace_back_it_recto") {
    std::deque<int> c = make_deque(mode, "emplace_back");
    f_deque_emplace_back_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_emplace_back_it_guarda") {
    std::deque<int> c = make_deque(mode, "emplace_back");
    f_deque_emplace_back_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_emplace_back_it_bucle") {
    std::deque<int> c = make_deque(mode, "emplace_back");
    f_deque_emplace_back_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_emplace_back_it_llamada") {
    std::deque<int> c = make_deque(mode, "emplace_back");
    f_deque_emplace_back_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_emplace_back_ref_recto") {
    std::deque<int> c = make_deque(mode, "emplace_back");
    f_deque_emplace_back_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_emplace_back_ref_guarda") {
    std::deque<int> c = make_deque(mode, "emplace_back");
    f_deque_emplace_back_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_emplace_back_ref_bucle") {
    std::deque<int> c = make_deque(mode, "emplace_back");
    f_deque_emplace_back_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_emplace_back_ref_llamada") {
    std::deque<int> c = make_deque(mode, "emplace_back");
    f_deque_emplace_back_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_emplace_back_ptr_recto") {
    std::deque<int> c = make_deque(mode, "emplace_back");
    f_deque_emplace_back_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_emplace_back_ptr_guarda") {
    std::deque<int> c = make_deque(mode, "emplace_back");
    f_deque_emplace_back_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_emplace_back_ptr_bucle") {
    std::deque<int> c = make_deque(mode, "emplace_back");
    f_deque_emplace_back_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_emplace_back_ptr_llamada") {
    std::deque<int> c = make_deque(mode, "emplace_back");
    f_deque_emplace_back_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_insert_middle_it_recto") {
    std::deque<int> c = make_deque(mode, "insert_middle");
    f_deque_insert_middle_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_insert_middle_it_guarda") {
    std::deque<int> c = make_deque(mode, "insert_middle");
    f_deque_insert_middle_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_insert_middle_it_bucle") {
    std::deque<int> c = make_deque(mode, "insert_middle");
    f_deque_insert_middle_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_insert_middle_it_llamada") {
    std::deque<int> c = make_deque(mode, "insert_middle");
    f_deque_insert_middle_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_insert_middle_ref_recto") {
    std::deque<int> c = make_deque(mode, "insert_middle");
    f_deque_insert_middle_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_insert_middle_ref_guarda") {
    std::deque<int> c = make_deque(mode, "insert_middle");
    f_deque_insert_middle_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_insert_middle_ref_bucle") {
    std::deque<int> c = make_deque(mode, "insert_middle");
    f_deque_insert_middle_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_insert_middle_ref_llamada") {
    std::deque<int> c = make_deque(mode, "insert_middle");
    f_deque_insert_middle_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_insert_middle_ptr_recto") {
    std::deque<int> c = make_deque(mode, "insert_middle");
    f_deque_insert_middle_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_insert_middle_ptr_guarda") {
    std::deque<int> c = make_deque(mode, "insert_middle");
    f_deque_insert_middle_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_insert_middle_ptr_bucle") {
    std::deque<int> c = make_deque(mode, "insert_middle");
    f_deque_insert_middle_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_insert_middle_ptr_llamada") {
    std::deque<int> c = make_deque(mode, "insert_middle");
    f_deque_insert_middle_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_erase_begin_it_recto") {
    std::deque<int> c = make_deque(mode, "erase_begin");
    f_deque_erase_begin_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_erase_begin_it_guarda") {
    std::deque<int> c = make_deque(mode, "erase_begin");
    f_deque_erase_begin_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_erase_begin_it_bucle") {
    std::deque<int> c = make_deque(mode, "erase_begin");
    f_deque_erase_begin_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_erase_begin_it_llamada") {
    std::deque<int> c = make_deque(mode, "erase_begin");
    f_deque_erase_begin_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_erase_begin_ref_recto") {
    std::deque<int> c = make_deque(mode, "erase_begin");
    f_deque_erase_begin_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_erase_begin_ref_guarda") {
    std::deque<int> c = make_deque(mode, "erase_begin");
    f_deque_erase_begin_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_erase_begin_ref_bucle") {
    std::deque<int> c = make_deque(mode, "erase_begin");
    f_deque_erase_begin_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_erase_begin_ref_llamada") {
    std::deque<int> c = make_deque(mode, "erase_begin");
    f_deque_erase_begin_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_erase_begin_ptr_recto") {
    std::deque<int> c = make_deque(mode, "erase_begin");
    f_deque_erase_begin_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_erase_begin_ptr_guarda") {
    std::deque<int> c = make_deque(mode, "erase_begin");
    f_deque_erase_begin_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_erase_begin_ptr_bucle") {
    std::deque<int> c = make_deque(mode, "erase_begin");
    f_deque_erase_begin_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_erase_begin_ptr_llamada") {
    std::deque<int> c = make_deque(mode, "erase_begin");
    f_deque_erase_begin_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_clear_it_recto") {
    std::deque<int> c = make_deque(mode, "clear");
    f_deque_clear_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_clear_it_guarda") {
    std::deque<int> c = make_deque(mode, "clear");
    f_deque_clear_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_clear_it_bucle") {
    std::deque<int> c = make_deque(mode, "clear");
    f_deque_clear_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_clear_it_llamada") {
    std::deque<int> c = make_deque(mode, "clear");
    f_deque_clear_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_clear_ref_recto") {
    std::deque<int> c = make_deque(mode, "clear");
    f_deque_clear_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_clear_ref_guarda") {
    std::deque<int> c = make_deque(mode, "clear");
    f_deque_clear_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_clear_ref_bucle") {
    std::deque<int> c = make_deque(mode, "clear");
    f_deque_clear_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_clear_ref_llamada") {
    std::deque<int> c = make_deque(mode, "clear");
    f_deque_clear_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_clear_ptr_recto") {
    std::deque<int> c = make_deque(mode, "clear");
    f_deque_clear_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_clear_ptr_guarda") {
    std::deque<int> c = make_deque(mode, "clear");
    f_deque_clear_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_clear_ptr_bucle") {
    std::deque<int> c = make_deque(mode, "clear");
    f_deque_clear_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_clear_ptr_llamada") {
    std::deque<int> c = make_deque(mode, "clear");
    f_deque_clear_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_resize_grow_it_recto") {
    std::deque<int> c = make_deque(mode, "resize_grow");
    f_deque_resize_grow_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_resize_grow_it_guarda") {
    std::deque<int> c = make_deque(mode, "resize_grow");
    f_deque_resize_grow_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_resize_grow_it_bucle") {
    std::deque<int> c = make_deque(mode, "resize_grow");
    f_deque_resize_grow_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_resize_grow_it_llamada") {
    std::deque<int> c = make_deque(mode, "resize_grow");
    f_deque_resize_grow_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_resize_grow_ref_recto") {
    std::deque<int> c = make_deque(mode, "resize_grow");
    f_deque_resize_grow_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_resize_grow_ref_guarda") {
    std::deque<int> c = make_deque(mode, "resize_grow");
    f_deque_resize_grow_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_resize_grow_ref_bucle") {
    std::deque<int> c = make_deque(mode, "resize_grow");
    f_deque_resize_grow_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_resize_grow_ref_llamada") {
    std::deque<int> c = make_deque(mode, "resize_grow");
    f_deque_resize_grow_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_resize_grow_ptr_recto") {
    std::deque<int> c = make_deque(mode, "resize_grow");
    f_deque_resize_grow_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_resize_grow_ptr_guarda") {
    std::deque<int> c = make_deque(mode, "resize_grow");
    f_deque_resize_grow_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_resize_grow_ptr_bucle") {
    std::deque<int> c = make_deque(mode, "resize_grow");
    f_deque_resize_grow_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_resize_grow_ptr_llamada") {
    std::deque<int> c = make_deque(mode, "resize_grow");
    f_deque_resize_grow_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_pop_front_it_recto") {
    std::deque<int> c = make_deque(mode, "pop_front");
    f_deque_pop_front_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_pop_front_it_guarda") {
    std::deque<int> c = make_deque(mode, "pop_front");
    f_deque_pop_front_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_pop_front_it_bucle") {
    std::deque<int> c = make_deque(mode, "pop_front");
    f_deque_pop_front_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_pop_front_it_llamada") {
    std::deque<int> c = make_deque(mode, "pop_front");
    f_deque_pop_front_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_pop_front_ref_recto") {
    std::deque<int> c = make_deque(mode, "pop_front");
    f_deque_pop_front_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_pop_front_ref_guarda") {
    std::deque<int> c = make_deque(mode, "pop_front");
    f_deque_pop_front_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_pop_front_ref_bucle") {
    std::deque<int> c = make_deque(mode, "pop_front");
    f_deque_pop_front_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_pop_front_ref_llamada") {
    std::deque<int> c = make_deque(mode, "pop_front");
    f_deque_pop_front_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_pop_front_ptr_recto") {
    std::deque<int> c = make_deque(mode, "pop_front");
    f_deque_pop_front_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_pop_front_ptr_guarda") {
    std::deque<int> c = make_deque(mode, "pop_front");
    f_deque_pop_front_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_pop_front_ptr_bucle") {
    std::deque<int> c = make_deque(mode, "pop_front");
    f_deque_pop_front_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_deque_pop_front_ptr_llamada") {
    std::deque<int> c = make_deque(mode, "pop_front");
    f_deque_pop_front_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_push_back_it_recto") {
    std::list<int> c = make_list(mode, "push_back");
    f_list_push_back_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_push_back_it_guarda") {
    std::list<int> c = make_list(mode, "push_back");
    f_list_push_back_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_push_back_it_bucle") {
    std::list<int> c = make_list(mode, "push_back");
    f_list_push_back_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_push_back_it_llamada") {
    std::list<int> c = make_list(mode, "push_back");
    f_list_push_back_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_push_back_ref_recto") {
    std::list<int> c = make_list(mode, "push_back");
    f_list_push_back_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_push_back_ref_guarda") {
    std::list<int> c = make_list(mode, "push_back");
    f_list_push_back_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_push_back_ref_bucle") {
    std::list<int> c = make_list(mode, "push_back");
    f_list_push_back_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_push_back_ref_llamada") {
    std::list<int> c = make_list(mode, "push_back");
    f_list_push_back_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_push_back_ptr_recto") {
    std::list<int> c = make_list(mode, "push_back");
    f_list_push_back_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_push_back_ptr_guarda") {
    std::list<int> c = make_list(mode, "push_back");
    f_list_push_back_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_push_back_ptr_bucle") {
    std::list<int> c = make_list(mode, "push_back");
    f_list_push_back_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_push_back_ptr_llamada") {
    std::list<int> c = make_list(mode, "push_back");
    f_list_push_back_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_push_front_it_recto") {
    std::list<int> c = make_list(mode, "push_front");
    f_list_push_front_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_push_front_it_guarda") {
    std::list<int> c = make_list(mode, "push_front");
    f_list_push_front_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_push_front_it_bucle") {
    std::list<int> c = make_list(mode, "push_front");
    f_list_push_front_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_push_front_it_llamada") {
    std::list<int> c = make_list(mode, "push_front");
    f_list_push_front_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_push_front_ref_recto") {
    std::list<int> c = make_list(mode, "push_front");
    f_list_push_front_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_push_front_ref_guarda") {
    std::list<int> c = make_list(mode, "push_front");
    f_list_push_front_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_push_front_ref_bucle") {
    std::list<int> c = make_list(mode, "push_front");
    f_list_push_front_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_push_front_ref_llamada") {
    std::list<int> c = make_list(mode, "push_front");
    f_list_push_front_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_push_front_ptr_recto") {
    std::list<int> c = make_list(mode, "push_front");
    f_list_push_front_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_push_front_ptr_guarda") {
    std::list<int> c = make_list(mode, "push_front");
    f_list_push_front_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_push_front_ptr_bucle") {
    std::list<int> c = make_list(mode, "push_front");
    f_list_push_front_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_push_front_ptr_llamada") {
    std::list<int> c = make_list(mode, "push_front");
    f_list_push_front_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_insert_it_recto") {
    std::list<int> c = make_list(mode, "insert");
    f_list_insert_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_insert_it_guarda") {
    std::list<int> c = make_list(mode, "insert");
    f_list_insert_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_insert_it_bucle") {
    std::list<int> c = make_list(mode, "insert");
    f_list_insert_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_insert_it_llamada") {
    std::list<int> c = make_list(mode, "insert");
    f_list_insert_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_insert_ref_recto") {
    std::list<int> c = make_list(mode, "insert");
    f_list_insert_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_insert_ref_guarda") {
    std::list<int> c = make_list(mode, "insert");
    f_list_insert_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_insert_ref_bucle") {
    std::list<int> c = make_list(mode, "insert");
    f_list_insert_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_insert_ref_llamada") {
    std::list<int> c = make_list(mode, "insert");
    f_list_insert_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_insert_ptr_recto") {
    std::list<int> c = make_list(mode, "insert");
    f_list_insert_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_insert_ptr_guarda") {
    std::list<int> c = make_list(mode, "insert");
    f_list_insert_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_insert_ptr_bucle") {
    std::list<int> c = make_list(mode, "insert");
    f_list_insert_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_insert_ptr_llamada") {
    std::list<int> c = make_list(mode, "insert");
    f_list_insert_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_erase_begin_it_recto") {
    std::list<int> c = make_list(mode, "erase_begin");
    f_list_erase_begin_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_erase_begin_it_guarda") {
    std::list<int> c = make_list(mode, "erase_begin");
    f_list_erase_begin_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_erase_begin_it_bucle") {
    std::list<int> c = make_list(mode, "erase_begin");
    f_list_erase_begin_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_erase_begin_it_llamada") {
    std::list<int> c = make_list(mode, "erase_begin");
    f_list_erase_begin_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_erase_begin_ref_recto") {
    std::list<int> c = make_list(mode, "erase_begin");
    f_list_erase_begin_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_erase_begin_ref_guarda") {
    std::list<int> c = make_list(mode, "erase_begin");
    f_list_erase_begin_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_erase_begin_ref_bucle") {
    std::list<int> c = make_list(mode, "erase_begin");
    f_list_erase_begin_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_erase_begin_ref_llamada") {
    std::list<int> c = make_list(mode, "erase_begin");
    f_list_erase_begin_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_erase_begin_ptr_recto") {
    std::list<int> c = make_list(mode, "erase_begin");
    f_list_erase_begin_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_erase_begin_ptr_guarda") {
    std::list<int> c = make_list(mode, "erase_begin");
    f_list_erase_begin_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_erase_begin_ptr_bucle") {
    std::list<int> c = make_list(mode, "erase_begin");
    f_list_erase_begin_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_erase_begin_ptr_llamada") {
    std::list<int> c = make_list(mode, "erase_begin");
    f_list_erase_begin_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_clear_it_recto") {
    std::list<int> c = make_list(mode, "clear");
    f_list_clear_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_clear_it_guarda") {
    std::list<int> c = make_list(mode, "clear");
    f_list_clear_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_clear_it_bucle") {
    std::list<int> c = make_list(mode, "clear");
    f_list_clear_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_clear_it_llamada") {
    std::list<int> c = make_list(mode, "clear");
    f_list_clear_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_clear_ref_recto") {
    std::list<int> c = make_list(mode, "clear");
    f_list_clear_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_clear_ref_guarda") {
    std::list<int> c = make_list(mode, "clear");
    f_list_clear_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_clear_ref_bucle") {
    std::list<int> c = make_list(mode, "clear");
    f_list_clear_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_clear_ref_llamada") {
    std::list<int> c = make_list(mode, "clear");
    f_list_clear_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_clear_ptr_recto") {
    std::list<int> c = make_list(mode, "clear");
    f_list_clear_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_clear_ptr_guarda") {
    std::list<int> c = make_list(mode, "clear");
    f_list_clear_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_clear_ptr_bucle") {
    std::list<int> c = make_list(mode, "clear");
    f_list_clear_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_clear_ptr_llamada") {
    std::list<int> c = make_list(mode, "clear");
    f_list_clear_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_resize_grow_it_recto") {
    std::list<int> c = make_list(mode, "resize_grow");
    f_list_resize_grow_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_resize_grow_it_guarda") {
    std::list<int> c = make_list(mode, "resize_grow");
    f_list_resize_grow_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_resize_grow_it_bucle") {
    std::list<int> c = make_list(mode, "resize_grow");
    f_list_resize_grow_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_resize_grow_it_llamada") {
    std::list<int> c = make_list(mode, "resize_grow");
    f_list_resize_grow_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_resize_grow_ref_recto") {
    std::list<int> c = make_list(mode, "resize_grow");
    f_list_resize_grow_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_resize_grow_ref_guarda") {
    std::list<int> c = make_list(mode, "resize_grow");
    f_list_resize_grow_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_resize_grow_ref_bucle") {
    std::list<int> c = make_list(mode, "resize_grow");
    f_list_resize_grow_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_resize_grow_ref_llamada") {
    std::list<int> c = make_list(mode, "resize_grow");
    f_list_resize_grow_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_resize_grow_ptr_recto") {
    std::list<int> c = make_list(mode, "resize_grow");
    f_list_resize_grow_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_resize_grow_ptr_guarda") {
    std::list<int> c = make_list(mode, "resize_grow");
    f_list_resize_grow_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_resize_grow_ptr_bucle") {
    std::list<int> c = make_list(mode, "resize_grow");
    f_list_resize_grow_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_resize_grow_ptr_llamada") {
    std::list<int> c = make_list(mode, "resize_grow");
    f_list_resize_grow_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_pop_front_it_recto") {
    std::list<int> c = make_list(mode, "pop_front");
    f_list_pop_front_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_pop_front_it_guarda") {
    std::list<int> c = make_list(mode, "pop_front");
    f_list_pop_front_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_pop_front_it_bucle") {
    std::list<int> c = make_list(mode, "pop_front");
    f_list_pop_front_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_pop_front_it_llamada") {
    std::list<int> c = make_list(mode, "pop_front");
    f_list_pop_front_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_pop_front_ref_recto") {
    std::list<int> c = make_list(mode, "pop_front");
    f_list_pop_front_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_pop_front_ref_guarda") {
    std::list<int> c = make_list(mode, "pop_front");
    f_list_pop_front_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_pop_front_ref_bucle") {
    std::list<int> c = make_list(mode, "pop_front");
    f_list_pop_front_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_pop_front_ref_llamada") {
    std::list<int> c = make_list(mode, "pop_front");
    f_list_pop_front_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_pop_front_ptr_recto") {
    std::list<int> c = make_list(mode, "pop_front");
    f_list_pop_front_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_pop_front_ptr_guarda") {
    std::list<int> c = make_list(mode, "pop_front");
    f_list_pop_front_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_pop_front_ptr_bucle") {
    std::list<int> c = make_list(mode, "pop_front");
    f_list_pop_front_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_pop_front_ptr_llamada") {
    std::list<int> c = make_list(mode, "pop_front");
    f_list_pop_front_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_reverse_it_recto") {
    std::list<int> c = make_list(mode, "reverse");
    f_list_reverse_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_reverse_it_guarda") {
    std::list<int> c = make_list(mode, "reverse");
    f_list_reverse_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_reverse_it_bucle") {
    std::list<int> c = make_list(mode, "reverse");
    f_list_reverse_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_reverse_it_llamada") {
    std::list<int> c = make_list(mode, "reverse");
    f_list_reverse_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_reverse_ref_recto") {
    std::list<int> c = make_list(mode, "reverse");
    f_list_reverse_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_reverse_ref_guarda") {
    std::list<int> c = make_list(mode, "reverse");
    f_list_reverse_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_reverse_ref_bucle") {
    std::list<int> c = make_list(mode, "reverse");
    f_list_reverse_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_reverse_ref_llamada") {
    std::list<int> c = make_list(mode, "reverse");
    f_list_reverse_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_reverse_ptr_recto") {
    std::list<int> c = make_list(mode, "reverse");
    f_list_reverse_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_reverse_ptr_guarda") {
    std::list<int> c = make_list(mode, "reverse");
    f_list_reverse_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_reverse_ptr_bucle") {
    std::list<int> c = make_list(mode, "reverse");
    f_list_reverse_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_reverse_ptr_llamada") {
    std::list<int> c = make_list(mode, "reverse");
    f_list_reverse_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_sort_it_recto") {
    std::list<int> c = make_list(mode, "sort");
    f_list_sort_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_sort_it_guarda") {
    std::list<int> c = make_list(mode, "sort");
    f_list_sort_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_sort_it_bucle") {
    std::list<int> c = make_list(mode, "sort");
    f_list_sort_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_sort_it_llamada") {
    std::list<int> c = make_list(mode, "sort");
    f_list_sort_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_sort_ref_recto") {
    std::list<int> c = make_list(mode, "sort");
    f_list_sort_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_sort_ref_guarda") {
    std::list<int> c = make_list(mode, "sort");
    f_list_sort_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_sort_ref_bucle") {
    std::list<int> c = make_list(mode, "sort");
    f_list_sort_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_sort_ref_llamada") {
    std::list<int> c = make_list(mode, "sort");
    f_list_sort_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_sort_ptr_recto") {
    std::list<int> c = make_list(mode, "sort");
    f_list_sort_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_sort_ptr_guarda") {
    std::list<int> c = make_list(mode, "sort");
    f_list_sort_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_sort_ptr_bucle") {
    std::list<int> c = make_list(mode, "sort");
    f_list_sort_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_list_sort_ptr_llamada") {
    std::list<int> c = make_list(mode, "sort");
    f_list_sort_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_push_front_it_recto") {
    std::forward_list<int> c = make_flist(mode, "push_front");
    f_flist_push_front_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_push_front_it_guarda") {
    std::forward_list<int> c = make_flist(mode, "push_front");
    f_flist_push_front_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_push_front_it_bucle") {
    std::forward_list<int> c = make_flist(mode, "push_front");
    f_flist_push_front_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_push_front_it_llamada") {
    std::forward_list<int> c = make_flist(mode, "push_front");
    f_flist_push_front_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_push_front_ref_recto") {
    std::forward_list<int> c = make_flist(mode, "push_front");
    f_flist_push_front_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_push_front_ref_guarda") {
    std::forward_list<int> c = make_flist(mode, "push_front");
    f_flist_push_front_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_push_front_ref_bucle") {
    std::forward_list<int> c = make_flist(mode, "push_front");
    f_flist_push_front_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_push_front_ref_llamada") {
    std::forward_list<int> c = make_flist(mode, "push_front");
    f_flist_push_front_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_push_front_ptr_recto") {
    std::forward_list<int> c = make_flist(mode, "push_front");
    f_flist_push_front_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_push_front_ptr_guarda") {
    std::forward_list<int> c = make_flist(mode, "push_front");
    f_flist_push_front_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_push_front_ptr_bucle") {
    std::forward_list<int> c = make_flist(mode, "push_front");
    f_flist_push_front_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_push_front_ptr_llamada") {
    std::forward_list<int> c = make_flist(mode, "push_front");
    f_flist_push_front_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_insert_after_it_recto") {
    std::forward_list<int> c = make_flist(mode, "insert_after");
    f_flist_insert_after_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_insert_after_it_guarda") {
    std::forward_list<int> c = make_flist(mode, "insert_after");
    f_flist_insert_after_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_insert_after_it_bucle") {
    std::forward_list<int> c = make_flist(mode, "insert_after");
    f_flist_insert_after_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_insert_after_it_llamada") {
    std::forward_list<int> c = make_flist(mode, "insert_after");
    f_flist_insert_after_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_insert_after_ref_recto") {
    std::forward_list<int> c = make_flist(mode, "insert_after");
    f_flist_insert_after_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_insert_after_ref_guarda") {
    std::forward_list<int> c = make_flist(mode, "insert_after");
    f_flist_insert_after_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_insert_after_ref_bucle") {
    std::forward_list<int> c = make_flist(mode, "insert_after");
    f_flist_insert_after_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_insert_after_ref_llamada") {
    std::forward_list<int> c = make_flist(mode, "insert_after");
    f_flist_insert_after_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_insert_after_ptr_recto") {
    std::forward_list<int> c = make_flist(mode, "insert_after");
    f_flist_insert_after_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_insert_after_ptr_guarda") {
    std::forward_list<int> c = make_flist(mode, "insert_after");
    f_flist_insert_after_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_insert_after_ptr_bucle") {
    std::forward_list<int> c = make_flist(mode, "insert_after");
    f_flist_insert_after_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_insert_after_ptr_llamada") {
    std::forward_list<int> c = make_flist(mode, "insert_after");
    f_flist_insert_after_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_erase_after_it_recto") {
    std::forward_list<int> c = make_flist(mode, "erase_after");
    f_flist_erase_after_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_erase_after_it_guarda") {
    std::forward_list<int> c = make_flist(mode, "erase_after");
    f_flist_erase_after_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_erase_after_it_bucle") {
    std::forward_list<int> c = make_flist(mode, "erase_after");
    f_flist_erase_after_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_erase_after_it_llamada") {
    std::forward_list<int> c = make_flist(mode, "erase_after");
    f_flist_erase_after_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_erase_after_ref_recto") {
    std::forward_list<int> c = make_flist(mode, "erase_after");
    f_flist_erase_after_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_erase_after_ref_guarda") {
    std::forward_list<int> c = make_flist(mode, "erase_after");
    f_flist_erase_after_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_erase_after_ref_bucle") {
    std::forward_list<int> c = make_flist(mode, "erase_after");
    f_flist_erase_after_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_erase_after_ref_llamada") {
    std::forward_list<int> c = make_flist(mode, "erase_after");
    f_flist_erase_after_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_erase_after_ptr_recto") {
    std::forward_list<int> c = make_flist(mode, "erase_after");
    f_flist_erase_after_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_erase_after_ptr_guarda") {
    std::forward_list<int> c = make_flist(mode, "erase_after");
    f_flist_erase_after_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_erase_after_ptr_bucle") {
    std::forward_list<int> c = make_flist(mode, "erase_after");
    f_flist_erase_after_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_erase_after_ptr_llamada") {
    std::forward_list<int> c = make_flist(mode, "erase_after");
    f_flist_erase_after_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_clear_it_recto") {
    std::forward_list<int> c = make_flist(mode, "clear");
    f_flist_clear_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_clear_it_guarda") {
    std::forward_list<int> c = make_flist(mode, "clear");
    f_flist_clear_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_clear_it_bucle") {
    std::forward_list<int> c = make_flist(mode, "clear");
    f_flist_clear_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_clear_it_llamada") {
    std::forward_list<int> c = make_flist(mode, "clear");
    f_flist_clear_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_clear_ref_recto") {
    std::forward_list<int> c = make_flist(mode, "clear");
    f_flist_clear_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_clear_ref_guarda") {
    std::forward_list<int> c = make_flist(mode, "clear");
    f_flist_clear_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_clear_ref_bucle") {
    std::forward_list<int> c = make_flist(mode, "clear");
    f_flist_clear_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_clear_ref_llamada") {
    std::forward_list<int> c = make_flist(mode, "clear");
    f_flist_clear_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_clear_ptr_recto") {
    std::forward_list<int> c = make_flist(mode, "clear");
    f_flist_clear_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_clear_ptr_guarda") {
    std::forward_list<int> c = make_flist(mode, "clear");
    f_flist_clear_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_clear_ptr_bucle") {
    std::forward_list<int> c = make_flist(mode, "clear");
    f_flist_clear_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_flist_clear_ptr_llamada") {
    std::forward_list<int> c = make_flist(mode, "clear");
    f_flist_clear_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_insert_it_recto") {
    std::set<int> c = make_set(mode, "insert");
    f_set_insert_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_insert_it_guarda") {
    std::set<int> c = make_set(mode, "insert");
    f_set_insert_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_insert_it_bucle") {
    std::set<int> c = make_set(mode, "insert");
    f_set_insert_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_insert_it_llamada") {
    std::set<int> c = make_set(mode, "insert");
    f_set_insert_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_insert_ref_recto") {
    std::set<int> c = make_set(mode, "insert");
    f_set_insert_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_insert_ref_guarda") {
    std::set<int> c = make_set(mode, "insert");
    f_set_insert_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_insert_ref_bucle") {
    std::set<int> c = make_set(mode, "insert");
    f_set_insert_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_insert_ref_llamada") {
    std::set<int> c = make_set(mode, "insert");
    f_set_insert_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_insert_ptr_recto") {
    std::set<int> c = make_set(mode, "insert");
    f_set_insert_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_insert_ptr_guarda") {
    std::set<int> c = make_set(mode, "insert");
    f_set_insert_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_insert_ptr_bucle") {
    std::set<int> c = make_set(mode, "insert");
    f_set_insert_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_insert_ptr_llamada") {
    std::set<int> c = make_set(mode, "insert");
    f_set_insert_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_emplace_it_recto") {
    std::set<int> c = make_set(mode, "emplace");
    f_set_emplace_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_emplace_it_guarda") {
    std::set<int> c = make_set(mode, "emplace");
    f_set_emplace_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_emplace_it_bucle") {
    std::set<int> c = make_set(mode, "emplace");
    f_set_emplace_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_emplace_it_llamada") {
    std::set<int> c = make_set(mode, "emplace");
    f_set_emplace_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_emplace_ref_recto") {
    std::set<int> c = make_set(mode, "emplace");
    f_set_emplace_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_emplace_ref_guarda") {
    std::set<int> c = make_set(mode, "emplace");
    f_set_emplace_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_emplace_ref_bucle") {
    std::set<int> c = make_set(mode, "emplace");
    f_set_emplace_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_emplace_ref_llamada") {
    std::set<int> c = make_set(mode, "emplace");
    f_set_emplace_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_emplace_ptr_recto") {
    std::set<int> c = make_set(mode, "emplace");
    f_set_emplace_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_emplace_ptr_guarda") {
    std::set<int> c = make_set(mode, "emplace");
    f_set_emplace_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_emplace_ptr_bucle") {
    std::set<int> c = make_set(mode, "emplace");
    f_set_emplace_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_emplace_ptr_llamada") {
    std::set<int> c = make_set(mode, "emplace");
    f_set_emplace_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_erase_begin_it_recto") {
    std::set<int> c = make_set(mode, "erase_begin");
    f_set_erase_begin_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_erase_begin_it_guarda") {
    std::set<int> c = make_set(mode, "erase_begin");
    f_set_erase_begin_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_erase_begin_it_bucle") {
    std::set<int> c = make_set(mode, "erase_begin");
    f_set_erase_begin_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_erase_begin_it_llamada") {
    std::set<int> c = make_set(mode, "erase_begin");
    f_set_erase_begin_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_erase_begin_ref_recto") {
    std::set<int> c = make_set(mode, "erase_begin");
    f_set_erase_begin_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_erase_begin_ref_guarda") {
    std::set<int> c = make_set(mode, "erase_begin");
    f_set_erase_begin_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_erase_begin_ref_bucle") {
    std::set<int> c = make_set(mode, "erase_begin");
    f_set_erase_begin_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_erase_begin_ref_llamada") {
    std::set<int> c = make_set(mode, "erase_begin");
    f_set_erase_begin_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_erase_begin_ptr_recto") {
    std::set<int> c = make_set(mode, "erase_begin");
    f_set_erase_begin_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_erase_begin_ptr_guarda") {
    std::set<int> c = make_set(mode, "erase_begin");
    f_set_erase_begin_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_erase_begin_ptr_bucle") {
    std::set<int> c = make_set(mode, "erase_begin");
    f_set_erase_begin_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_erase_begin_ptr_llamada") {
    std::set<int> c = make_set(mode, "erase_begin");
    f_set_erase_begin_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_clear_it_recto") {
    std::set<int> c = make_set(mode, "clear");
    f_set_clear_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_clear_it_guarda") {
    std::set<int> c = make_set(mode, "clear");
    f_set_clear_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_clear_it_bucle") {
    std::set<int> c = make_set(mode, "clear");
    f_set_clear_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_clear_it_llamada") {
    std::set<int> c = make_set(mode, "clear");
    f_set_clear_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_clear_ref_recto") {
    std::set<int> c = make_set(mode, "clear");
    f_set_clear_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_clear_ref_guarda") {
    std::set<int> c = make_set(mode, "clear");
    f_set_clear_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_clear_ref_bucle") {
    std::set<int> c = make_set(mode, "clear");
    f_set_clear_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_clear_ref_llamada") {
    std::set<int> c = make_set(mode, "clear");
    f_set_clear_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_clear_ptr_recto") {
    std::set<int> c = make_set(mode, "clear");
    f_set_clear_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_clear_ptr_guarda") {
    std::set<int> c = make_set(mode, "clear");
    f_set_clear_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_clear_ptr_bucle") {
    std::set<int> c = make_set(mode, "clear");
    f_set_clear_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_set_clear_ptr_llamada") {
    std::set<int> c = make_set(mode, "clear");
    f_set_clear_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mset_insert_it_recto") {
    std::multiset<int> c = make_mset(mode, "insert");
    f_mset_insert_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mset_insert_it_guarda") {
    std::multiset<int> c = make_mset(mode, "insert");
    f_mset_insert_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mset_insert_it_bucle") {
    std::multiset<int> c = make_mset(mode, "insert");
    f_mset_insert_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mset_insert_it_llamada") {
    std::multiset<int> c = make_mset(mode, "insert");
    f_mset_insert_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mset_insert_ref_recto") {
    std::multiset<int> c = make_mset(mode, "insert");
    f_mset_insert_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mset_insert_ref_guarda") {
    std::multiset<int> c = make_mset(mode, "insert");
    f_mset_insert_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mset_insert_ref_bucle") {
    std::multiset<int> c = make_mset(mode, "insert");
    f_mset_insert_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mset_insert_ref_llamada") {
    std::multiset<int> c = make_mset(mode, "insert");
    f_mset_insert_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mset_insert_ptr_recto") {
    std::multiset<int> c = make_mset(mode, "insert");
    f_mset_insert_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mset_insert_ptr_guarda") {
    std::multiset<int> c = make_mset(mode, "insert");
    f_mset_insert_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mset_insert_ptr_bucle") {
    std::multiset<int> c = make_mset(mode, "insert");
    f_mset_insert_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mset_insert_ptr_llamada") {
    std::multiset<int> c = make_mset(mode, "insert");
    f_mset_insert_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mset_erase_begin_it_recto") {
    std::multiset<int> c = make_mset(mode, "erase_begin");
    f_mset_erase_begin_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mset_erase_begin_it_guarda") {
    std::multiset<int> c = make_mset(mode, "erase_begin");
    f_mset_erase_begin_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mset_erase_begin_it_bucle") {
    std::multiset<int> c = make_mset(mode, "erase_begin");
    f_mset_erase_begin_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mset_erase_begin_it_llamada") {
    std::multiset<int> c = make_mset(mode, "erase_begin");
    f_mset_erase_begin_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mset_erase_begin_ref_recto") {
    std::multiset<int> c = make_mset(mode, "erase_begin");
    f_mset_erase_begin_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mset_erase_begin_ref_guarda") {
    std::multiset<int> c = make_mset(mode, "erase_begin");
    f_mset_erase_begin_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mset_erase_begin_ref_bucle") {
    std::multiset<int> c = make_mset(mode, "erase_begin");
    f_mset_erase_begin_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mset_erase_begin_ref_llamada") {
    std::multiset<int> c = make_mset(mode, "erase_begin");
    f_mset_erase_begin_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mset_erase_begin_ptr_recto") {
    std::multiset<int> c = make_mset(mode, "erase_begin");
    f_mset_erase_begin_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mset_erase_begin_ptr_guarda") {
    std::multiset<int> c = make_mset(mode, "erase_begin");
    f_mset_erase_begin_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mset_erase_begin_ptr_bucle") {
    std::multiset<int> c = make_mset(mode, "erase_begin");
    f_mset_erase_begin_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mset_erase_begin_ptr_llamada") {
    std::multiset<int> c = make_mset(mode, "erase_begin");
    f_mset_erase_begin_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mset_clear_it_recto") {
    std::multiset<int> c = make_mset(mode, "clear");
    f_mset_clear_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mset_clear_it_guarda") {
    std::multiset<int> c = make_mset(mode, "clear");
    f_mset_clear_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mset_clear_it_bucle") {
    std::multiset<int> c = make_mset(mode, "clear");
    f_mset_clear_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mset_clear_it_llamada") {
    std::multiset<int> c = make_mset(mode, "clear");
    f_mset_clear_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mset_clear_ref_recto") {
    std::multiset<int> c = make_mset(mode, "clear");
    f_mset_clear_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mset_clear_ref_guarda") {
    std::multiset<int> c = make_mset(mode, "clear");
    f_mset_clear_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mset_clear_ref_bucle") {
    std::multiset<int> c = make_mset(mode, "clear");
    f_mset_clear_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mset_clear_ref_llamada") {
    std::multiset<int> c = make_mset(mode, "clear");
    f_mset_clear_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mset_clear_ptr_recto") {
    std::multiset<int> c = make_mset(mode, "clear");
    f_mset_clear_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mset_clear_ptr_guarda") {
    std::multiset<int> c = make_mset(mode, "clear");
    f_mset_clear_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mset_clear_ptr_bucle") {
    std::multiset<int> c = make_mset(mode, "clear");
    f_mset_clear_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mset_clear_ptr_llamada") {
    std::multiset<int> c = make_mset(mode, "clear");
    f_mset_clear_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_insert_it_recto") {
    std::map<int, int> c = make_map(mode, "insert");
    f_map_insert_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_insert_it_guarda") {
    std::map<int, int> c = make_map(mode, "insert");
    f_map_insert_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_insert_it_bucle") {
    std::map<int, int> c = make_map(mode, "insert");
    f_map_insert_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_insert_it_llamada") {
    std::map<int, int> c = make_map(mode, "insert");
    f_map_insert_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_insert_ref_recto") {
    std::map<int, int> c = make_map(mode, "insert");
    f_map_insert_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_insert_ref_guarda") {
    std::map<int, int> c = make_map(mode, "insert");
    f_map_insert_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_insert_ref_bucle") {
    std::map<int, int> c = make_map(mode, "insert");
    f_map_insert_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_insert_ref_llamada") {
    std::map<int, int> c = make_map(mode, "insert");
    f_map_insert_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_insert_ptr_recto") {
    std::map<int, int> c = make_map(mode, "insert");
    f_map_insert_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_insert_ptr_guarda") {
    std::map<int, int> c = make_map(mode, "insert");
    f_map_insert_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_insert_ptr_bucle") {
    std::map<int, int> c = make_map(mode, "insert");
    f_map_insert_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_insert_ptr_llamada") {
    std::map<int, int> c = make_map(mode, "insert");
    f_map_insert_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_emplace_it_recto") {
    std::map<int, int> c = make_map(mode, "emplace");
    f_map_emplace_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_emplace_it_guarda") {
    std::map<int, int> c = make_map(mode, "emplace");
    f_map_emplace_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_emplace_it_bucle") {
    std::map<int, int> c = make_map(mode, "emplace");
    f_map_emplace_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_emplace_it_llamada") {
    std::map<int, int> c = make_map(mode, "emplace");
    f_map_emplace_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_emplace_ref_recto") {
    std::map<int, int> c = make_map(mode, "emplace");
    f_map_emplace_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_emplace_ref_guarda") {
    std::map<int, int> c = make_map(mode, "emplace");
    f_map_emplace_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_emplace_ref_bucle") {
    std::map<int, int> c = make_map(mode, "emplace");
    f_map_emplace_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_emplace_ref_llamada") {
    std::map<int, int> c = make_map(mode, "emplace");
    f_map_emplace_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_emplace_ptr_recto") {
    std::map<int, int> c = make_map(mode, "emplace");
    f_map_emplace_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_emplace_ptr_guarda") {
    std::map<int, int> c = make_map(mode, "emplace");
    f_map_emplace_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_emplace_ptr_bucle") {
    std::map<int, int> c = make_map(mode, "emplace");
    f_map_emplace_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_emplace_ptr_llamada") {
    std::map<int, int> c = make_map(mode, "emplace");
    f_map_emplace_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_subscript_it_recto") {
    std::map<int, int> c = make_map(mode, "subscript");
    f_map_subscript_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_subscript_it_guarda") {
    std::map<int, int> c = make_map(mode, "subscript");
    f_map_subscript_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_subscript_it_bucle") {
    std::map<int, int> c = make_map(mode, "subscript");
    f_map_subscript_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_subscript_it_llamada") {
    std::map<int, int> c = make_map(mode, "subscript");
    f_map_subscript_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_subscript_ref_recto") {
    std::map<int, int> c = make_map(mode, "subscript");
    f_map_subscript_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_subscript_ref_guarda") {
    std::map<int, int> c = make_map(mode, "subscript");
    f_map_subscript_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_subscript_ref_bucle") {
    std::map<int, int> c = make_map(mode, "subscript");
    f_map_subscript_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_subscript_ref_llamada") {
    std::map<int, int> c = make_map(mode, "subscript");
    f_map_subscript_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_subscript_ptr_recto") {
    std::map<int, int> c = make_map(mode, "subscript");
    f_map_subscript_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_subscript_ptr_guarda") {
    std::map<int, int> c = make_map(mode, "subscript");
    f_map_subscript_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_subscript_ptr_bucle") {
    std::map<int, int> c = make_map(mode, "subscript");
    f_map_subscript_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_subscript_ptr_llamada") {
    std::map<int, int> c = make_map(mode, "subscript");
    f_map_subscript_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_erase_begin_it_recto") {
    std::map<int, int> c = make_map(mode, "erase_begin");
    f_map_erase_begin_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_erase_begin_it_guarda") {
    std::map<int, int> c = make_map(mode, "erase_begin");
    f_map_erase_begin_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_erase_begin_it_bucle") {
    std::map<int, int> c = make_map(mode, "erase_begin");
    f_map_erase_begin_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_erase_begin_it_llamada") {
    std::map<int, int> c = make_map(mode, "erase_begin");
    f_map_erase_begin_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_erase_begin_ref_recto") {
    std::map<int, int> c = make_map(mode, "erase_begin");
    f_map_erase_begin_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_erase_begin_ref_guarda") {
    std::map<int, int> c = make_map(mode, "erase_begin");
    f_map_erase_begin_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_erase_begin_ref_bucle") {
    std::map<int, int> c = make_map(mode, "erase_begin");
    f_map_erase_begin_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_erase_begin_ref_llamada") {
    std::map<int, int> c = make_map(mode, "erase_begin");
    f_map_erase_begin_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_erase_begin_ptr_recto") {
    std::map<int, int> c = make_map(mode, "erase_begin");
    f_map_erase_begin_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_erase_begin_ptr_guarda") {
    std::map<int, int> c = make_map(mode, "erase_begin");
    f_map_erase_begin_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_erase_begin_ptr_bucle") {
    std::map<int, int> c = make_map(mode, "erase_begin");
    f_map_erase_begin_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_erase_begin_ptr_llamada") {
    std::map<int, int> c = make_map(mode, "erase_begin");
    f_map_erase_begin_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_clear_it_recto") {
    std::map<int, int> c = make_map(mode, "clear");
    f_map_clear_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_clear_it_guarda") {
    std::map<int, int> c = make_map(mode, "clear");
    f_map_clear_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_clear_it_bucle") {
    std::map<int, int> c = make_map(mode, "clear");
    f_map_clear_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_clear_it_llamada") {
    std::map<int, int> c = make_map(mode, "clear");
    f_map_clear_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_clear_ref_recto") {
    std::map<int, int> c = make_map(mode, "clear");
    f_map_clear_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_clear_ref_guarda") {
    std::map<int, int> c = make_map(mode, "clear");
    f_map_clear_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_clear_ref_bucle") {
    std::map<int, int> c = make_map(mode, "clear");
    f_map_clear_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_clear_ref_llamada") {
    std::map<int, int> c = make_map(mode, "clear");
    f_map_clear_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_clear_ptr_recto") {
    std::map<int, int> c = make_map(mode, "clear");
    f_map_clear_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_clear_ptr_guarda") {
    std::map<int, int> c = make_map(mode, "clear");
    f_map_clear_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_clear_ptr_bucle") {
    std::map<int, int> c = make_map(mode, "clear");
    f_map_clear_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_map_clear_ptr_llamada") {
    std::map<int, int> c = make_map(mode, "clear");
    f_map_clear_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mmap_insert_it_recto") {
    std::multimap<int, int> c = make_mmap(mode, "insert");
    f_mmap_insert_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mmap_insert_it_guarda") {
    std::multimap<int, int> c = make_mmap(mode, "insert");
    f_mmap_insert_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mmap_insert_it_bucle") {
    std::multimap<int, int> c = make_mmap(mode, "insert");
    f_mmap_insert_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mmap_insert_it_llamada") {
    std::multimap<int, int> c = make_mmap(mode, "insert");
    f_mmap_insert_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mmap_insert_ref_recto") {
    std::multimap<int, int> c = make_mmap(mode, "insert");
    f_mmap_insert_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mmap_insert_ref_guarda") {
    std::multimap<int, int> c = make_mmap(mode, "insert");
    f_mmap_insert_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mmap_insert_ref_bucle") {
    std::multimap<int, int> c = make_mmap(mode, "insert");
    f_mmap_insert_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mmap_insert_ref_llamada") {
    std::multimap<int, int> c = make_mmap(mode, "insert");
    f_mmap_insert_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mmap_insert_ptr_recto") {
    std::multimap<int, int> c = make_mmap(mode, "insert");
    f_mmap_insert_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mmap_insert_ptr_guarda") {
    std::multimap<int, int> c = make_mmap(mode, "insert");
    f_mmap_insert_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mmap_insert_ptr_bucle") {
    std::multimap<int, int> c = make_mmap(mode, "insert");
    f_mmap_insert_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mmap_insert_ptr_llamada") {
    std::multimap<int, int> c = make_mmap(mode, "insert");
    f_mmap_insert_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mmap_erase_begin_it_recto") {
    std::multimap<int, int> c = make_mmap(mode, "erase_begin");
    f_mmap_erase_begin_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mmap_erase_begin_it_guarda") {
    std::multimap<int, int> c = make_mmap(mode, "erase_begin");
    f_mmap_erase_begin_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mmap_erase_begin_it_bucle") {
    std::multimap<int, int> c = make_mmap(mode, "erase_begin");
    f_mmap_erase_begin_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mmap_erase_begin_it_llamada") {
    std::multimap<int, int> c = make_mmap(mode, "erase_begin");
    f_mmap_erase_begin_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mmap_erase_begin_ref_recto") {
    std::multimap<int, int> c = make_mmap(mode, "erase_begin");
    f_mmap_erase_begin_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mmap_erase_begin_ref_guarda") {
    std::multimap<int, int> c = make_mmap(mode, "erase_begin");
    f_mmap_erase_begin_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mmap_erase_begin_ref_bucle") {
    std::multimap<int, int> c = make_mmap(mode, "erase_begin");
    f_mmap_erase_begin_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mmap_erase_begin_ref_llamada") {
    std::multimap<int, int> c = make_mmap(mode, "erase_begin");
    f_mmap_erase_begin_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mmap_erase_begin_ptr_recto") {
    std::multimap<int, int> c = make_mmap(mode, "erase_begin");
    f_mmap_erase_begin_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mmap_erase_begin_ptr_guarda") {
    std::multimap<int, int> c = make_mmap(mode, "erase_begin");
    f_mmap_erase_begin_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mmap_erase_begin_ptr_bucle") {
    std::multimap<int, int> c = make_mmap(mode, "erase_begin");
    f_mmap_erase_begin_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mmap_erase_begin_ptr_llamada") {
    std::multimap<int, int> c = make_mmap(mode, "erase_begin");
    f_mmap_erase_begin_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mmap_clear_it_recto") {
    std::multimap<int, int> c = make_mmap(mode, "clear");
    f_mmap_clear_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mmap_clear_it_guarda") {
    std::multimap<int, int> c = make_mmap(mode, "clear");
    f_mmap_clear_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mmap_clear_it_bucle") {
    std::multimap<int, int> c = make_mmap(mode, "clear");
    f_mmap_clear_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mmap_clear_it_llamada") {
    std::multimap<int, int> c = make_mmap(mode, "clear");
    f_mmap_clear_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mmap_clear_ref_recto") {
    std::multimap<int, int> c = make_mmap(mode, "clear");
    f_mmap_clear_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mmap_clear_ref_guarda") {
    std::multimap<int, int> c = make_mmap(mode, "clear");
    f_mmap_clear_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mmap_clear_ref_bucle") {
    std::multimap<int, int> c = make_mmap(mode, "clear");
    f_mmap_clear_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mmap_clear_ref_llamada") {
    std::multimap<int, int> c = make_mmap(mode, "clear");
    f_mmap_clear_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mmap_clear_ptr_recto") {
    std::multimap<int, int> c = make_mmap(mode, "clear");
    f_mmap_clear_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mmap_clear_ptr_guarda") {
    std::multimap<int, int> c = make_mmap(mode, "clear");
    f_mmap_clear_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mmap_clear_ptr_bucle") {
    std::multimap<int, int> c = make_mmap(mode, "clear");
    f_mmap_clear_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_mmap_clear_ptr_llamada") {
    std::multimap<int, int> c = make_mmap(mode, "clear");
    f_mmap_clear_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_insert_it_recto") {
    std::unordered_set<int> c = make_uset(mode, "insert");
    f_uset_insert_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_insert_it_guarda") {
    std::unordered_set<int> c = make_uset(mode, "insert");
    f_uset_insert_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_insert_it_bucle") {
    std::unordered_set<int> c = make_uset(mode, "insert");
    f_uset_insert_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_insert_it_llamada") {
    std::unordered_set<int> c = make_uset(mode, "insert");
    f_uset_insert_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_insert_ref_recto") {
    std::unordered_set<int> c = make_uset(mode, "insert");
    f_uset_insert_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_insert_ref_guarda") {
    std::unordered_set<int> c = make_uset(mode, "insert");
    f_uset_insert_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_insert_ref_bucle") {
    std::unordered_set<int> c = make_uset(mode, "insert");
    f_uset_insert_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_insert_ref_llamada") {
    std::unordered_set<int> c = make_uset(mode, "insert");
    f_uset_insert_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_insert_ptr_recto") {
    std::unordered_set<int> c = make_uset(mode, "insert");
    f_uset_insert_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_insert_ptr_guarda") {
    std::unordered_set<int> c = make_uset(mode, "insert");
    f_uset_insert_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_insert_ptr_bucle") {
    std::unordered_set<int> c = make_uset(mode, "insert");
    f_uset_insert_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_insert_ptr_llamada") {
    std::unordered_set<int> c = make_uset(mode, "insert");
    f_uset_insert_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_erase_begin_it_recto") {
    std::unordered_set<int> c = make_uset(mode, "erase_begin");
    f_uset_erase_begin_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_erase_begin_it_guarda") {
    std::unordered_set<int> c = make_uset(mode, "erase_begin");
    f_uset_erase_begin_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_erase_begin_it_bucle") {
    std::unordered_set<int> c = make_uset(mode, "erase_begin");
    f_uset_erase_begin_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_erase_begin_it_llamada") {
    std::unordered_set<int> c = make_uset(mode, "erase_begin");
    f_uset_erase_begin_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_erase_begin_ref_recto") {
    std::unordered_set<int> c = make_uset(mode, "erase_begin");
    f_uset_erase_begin_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_erase_begin_ref_guarda") {
    std::unordered_set<int> c = make_uset(mode, "erase_begin");
    f_uset_erase_begin_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_erase_begin_ref_bucle") {
    std::unordered_set<int> c = make_uset(mode, "erase_begin");
    f_uset_erase_begin_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_erase_begin_ref_llamada") {
    std::unordered_set<int> c = make_uset(mode, "erase_begin");
    f_uset_erase_begin_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_erase_begin_ptr_recto") {
    std::unordered_set<int> c = make_uset(mode, "erase_begin");
    f_uset_erase_begin_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_erase_begin_ptr_guarda") {
    std::unordered_set<int> c = make_uset(mode, "erase_begin");
    f_uset_erase_begin_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_erase_begin_ptr_bucle") {
    std::unordered_set<int> c = make_uset(mode, "erase_begin");
    f_uset_erase_begin_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_erase_begin_ptr_llamada") {
    std::unordered_set<int> c = make_uset(mode, "erase_begin");
    f_uset_erase_begin_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_clear_it_recto") {
    std::unordered_set<int> c = make_uset(mode, "clear");
    f_uset_clear_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_clear_it_guarda") {
    std::unordered_set<int> c = make_uset(mode, "clear");
    f_uset_clear_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_clear_it_bucle") {
    std::unordered_set<int> c = make_uset(mode, "clear");
    f_uset_clear_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_clear_it_llamada") {
    std::unordered_set<int> c = make_uset(mode, "clear");
    f_uset_clear_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_clear_ref_recto") {
    std::unordered_set<int> c = make_uset(mode, "clear");
    f_uset_clear_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_clear_ref_guarda") {
    std::unordered_set<int> c = make_uset(mode, "clear");
    f_uset_clear_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_clear_ref_bucle") {
    std::unordered_set<int> c = make_uset(mode, "clear");
    f_uset_clear_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_clear_ref_llamada") {
    std::unordered_set<int> c = make_uset(mode, "clear");
    f_uset_clear_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_clear_ptr_recto") {
    std::unordered_set<int> c = make_uset(mode, "clear");
    f_uset_clear_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_clear_ptr_guarda") {
    std::unordered_set<int> c = make_uset(mode, "clear");
    f_uset_clear_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_clear_ptr_bucle") {
    std::unordered_set<int> c = make_uset(mode, "clear");
    f_uset_clear_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_clear_ptr_llamada") {
    std::unordered_set<int> c = make_uset(mode, "clear");
    f_uset_clear_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_rehash_it_recto") {
    std::unordered_set<int> c = make_uset(mode, "rehash");
    f_uset_rehash_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_rehash_it_guarda") {
    std::unordered_set<int> c = make_uset(mode, "rehash");
    f_uset_rehash_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_rehash_it_bucle") {
    std::unordered_set<int> c = make_uset(mode, "rehash");
    f_uset_rehash_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_rehash_it_llamada") {
    std::unordered_set<int> c = make_uset(mode, "rehash");
    f_uset_rehash_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_rehash_ref_recto") {
    std::unordered_set<int> c = make_uset(mode, "rehash");
    f_uset_rehash_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_rehash_ref_guarda") {
    std::unordered_set<int> c = make_uset(mode, "rehash");
    f_uset_rehash_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_rehash_ref_bucle") {
    std::unordered_set<int> c = make_uset(mode, "rehash");
    f_uset_rehash_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_rehash_ref_llamada") {
    std::unordered_set<int> c = make_uset(mode, "rehash");
    f_uset_rehash_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_rehash_ptr_recto") {
    std::unordered_set<int> c = make_uset(mode, "rehash");
    f_uset_rehash_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_rehash_ptr_guarda") {
    std::unordered_set<int> c = make_uset(mode, "rehash");
    f_uset_rehash_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_rehash_ptr_bucle") {
    std::unordered_set<int> c = make_uset(mode, "rehash");
    f_uset_rehash_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_rehash_ptr_llamada") {
    std::unordered_set<int> c = make_uset(mode, "rehash");
    f_uset_rehash_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_reserve_it_recto") {
    std::unordered_set<int> c = make_uset(mode, "reserve");
    f_uset_reserve_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_reserve_it_guarda") {
    std::unordered_set<int> c = make_uset(mode, "reserve");
    f_uset_reserve_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_reserve_it_bucle") {
    std::unordered_set<int> c = make_uset(mode, "reserve");
    f_uset_reserve_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_reserve_it_llamada") {
    std::unordered_set<int> c = make_uset(mode, "reserve");
    f_uset_reserve_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_reserve_ref_recto") {
    std::unordered_set<int> c = make_uset(mode, "reserve");
    f_uset_reserve_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_reserve_ref_guarda") {
    std::unordered_set<int> c = make_uset(mode, "reserve");
    f_uset_reserve_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_reserve_ref_bucle") {
    std::unordered_set<int> c = make_uset(mode, "reserve");
    f_uset_reserve_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_reserve_ref_llamada") {
    std::unordered_set<int> c = make_uset(mode, "reserve");
    f_uset_reserve_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_reserve_ptr_recto") {
    std::unordered_set<int> c = make_uset(mode, "reserve");
    f_uset_reserve_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_reserve_ptr_guarda") {
    std::unordered_set<int> c = make_uset(mode, "reserve");
    f_uset_reserve_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_reserve_ptr_bucle") {
    std::unordered_set<int> c = make_uset(mode, "reserve");
    f_uset_reserve_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_uset_reserve_ptr_llamada") {
    std::unordered_set<int> c = make_uset(mode, "reserve");
    f_uset_reserve_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_insert_it_recto") {
    std::unordered_map<int, int> c = make_umap(mode, "insert");
    f_umap_insert_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_insert_it_guarda") {
    std::unordered_map<int, int> c = make_umap(mode, "insert");
    f_umap_insert_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_insert_it_bucle") {
    std::unordered_map<int, int> c = make_umap(mode, "insert");
    f_umap_insert_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_insert_it_llamada") {
    std::unordered_map<int, int> c = make_umap(mode, "insert");
    f_umap_insert_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_insert_ref_recto") {
    std::unordered_map<int, int> c = make_umap(mode, "insert");
    f_umap_insert_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_insert_ref_guarda") {
    std::unordered_map<int, int> c = make_umap(mode, "insert");
    f_umap_insert_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_insert_ref_bucle") {
    std::unordered_map<int, int> c = make_umap(mode, "insert");
    f_umap_insert_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_insert_ref_llamada") {
    std::unordered_map<int, int> c = make_umap(mode, "insert");
    f_umap_insert_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_insert_ptr_recto") {
    std::unordered_map<int, int> c = make_umap(mode, "insert");
    f_umap_insert_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_insert_ptr_guarda") {
    std::unordered_map<int, int> c = make_umap(mode, "insert");
    f_umap_insert_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_insert_ptr_bucle") {
    std::unordered_map<int, int> c = make_umap(mode, "insert");
    f_umap_insert_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_insert_ptr_llamada") {
    std::unordered_map<int, int> c = make_umap(mode, "insert");
    f_umap_insert_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_subscript_it_recto") {
    std::unordered_map<int, int> c = make_umap(mode, "subscript");
    f_umap_subscript_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_subscript_it_guarda") {
    std::unordered_map<int, int> c = make_umap(mode, "subscript");
    f_umap_subscript_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_subscript_it_bucle") {
    std::unordered_map<int, int> c = make_umap(mode, "subscript");
    f_umap_subscript_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_subscript_it_llamada") {
    std::unordered_map<int, int> c = make_umap(mode, "subscript");
    f_umap_subscript_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_subscript_ref_recto") {
    std::unordered_map<int, int> c = make_umap(mode, "subscript");
    f_umap_subscript_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_subscript_ref_guarda") {
    std::unordered_map<int, int> c = make_umap(mode, "subscript");
    f_umap_subscript_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_subscript_ref_bucle") {
    std::unordered_map<int, int> c = make_umap(mode, "subscript");
    f_umap_subscript_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_subscript_ref_llamada") {
    std::unordered_map<int, int> c = make_umap(mode, "subscript");
    f_umap_subscript_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_subscript_ptr_recto") {
    std::unordered_map<int, int> c = make_umap(mode, "subscript");
    f_umap_subscript_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_subscript_ptr_guarda") {
    std::unordered_map<int, int> c = make_umap(mode, "subscript");
    f_umap_subscript_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_subscript_ptr_bucle") {
    std::unordered_map<int, int> c = make_umap(mode, "subscript");
    f_umap_subscript_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_subscript_ptr_llamada") {
    std::unordered_map<int, int> c = make_umap(mode, "subscript");
    f_umap_subscript_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_erase_begin_it_recto") {
    std::unordered_map<int, int> c = make_umap(mode, "erase_begin");
    f_umap_erase_begin_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_erase_begin_it_guarda") {
    std::unordered_map<int, int> c = make_umap(mode, "erase_begin");
    f_umap_erase_begin_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_erase_begin_it_bucle") {
    std::unordered_map<int, int> c = make_umap(mode, "erase_begin");
    f_umap_erase_begin_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_erase_begin_it_llamada") {
    std::unordered_map<int, int> c = make_umap(mode, "erase_begin");
    f_umap_erase_begin_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_erase_begin_ref_recto") {
    std::unordered_map<int, int> c = make_umap(mode, "erase_begin");
    f_umap_erase_begin_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_erase_begin_ref_guarda") {
    std::unordered_map<int, int> c = make_umap(mode, "erase_begin");
    f_umap_erase_begin_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_erase_begin_ref_bucle") {
    std::unordered_map<int, int> c = make_umap(mode, "erase_begin");
    f_umap_erase_begin_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_erase_begin_ref_llamada") {
    std::unordered_map<int, int> c = make_umap(mode, "erase_begin");
    f_umap_erase_begin_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_erase_begin_ptr_recto") {
    std::unordered_map<int, int> c = make_umap(mode, "erase_begin");
    f_umap_erase_begin_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_erase_begin_ptr_guarda") {
    std::unordered_map<int, int> c = make_umap(mode, "erase_begin");
    f_umap_erase_begin_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_erase_begin_ptr_bucle") {
    std::unordered_map<int, int> c = make_umap(mode, "erase_begin");
    f_umap_erase_begin_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_erase_begin_ptr_llamada") {
    std::unordered_map<int, int> c = make_umap(mode, "erase_begin");
    f_umap_erase_begin_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_clear_it_recto") {
    std::unordered_map<int, int> c = make_umap(mode, "clear");
    f_umap_clear_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_clear_it_guarda") {
    std::unordered_map<int, int> c = make_umap(mode, "clear");
    f_umap_clear_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_clear_it_bucle") {
    std::unordered_map<int, int> c = make_umap(mode, "clear");
    f_umap_clear_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_clear_it_llamada") {
    std::unordered_map<int, int> c = make_umap(mode, "clear");
    f_umap_clear_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_clear_ref_recto") {
    std::unordered_map<int, int> c = make_umap(mode, "clear");
    f_umap_clear_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_clear_ref_guarda") {
    std::unordered_map<int, int> c = make_umap(mode, "clear");
    f_umap_clear_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_clear_ref_bucle") {
    std::unordered_map<int, int> c = make_umap(mode, "clear");
    f_umap_clear_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_clear_ref_llamada") {
    std::unordered_map<int, int> c = make_umap(mode, "clear");
    f_umap_clear_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_clear_ptr_recto") {
    std::unordered_map<int, int> c = make_umap(mode, "clear");
    f_umap_clear_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_clear_ptr_guarda") {
    std::unordered_map<int, int> c = make_umap(mode, "clear");
    f_umap_clear_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_clear_ptr_bucle") {
    std::unordered_map<int, int> c = make_umap(mode, "clear");
    f_umap_clear_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_clear_ptr_llamada") {
    std::unordered_map<int, int> c = make_umap(mode, "clear");
    f_umap_clear_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_rehash_it_recto") {
    std::unordered_map<int, int> c = make_umap(mode, "rehash");
    f_umap_rehash_it_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_rehash_it_guarda") {
    std::unordered_map<int, int> c = make_umap(mode, "rehash");
    f_umap_rehash_it_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_rehash_it_bucle") {
    std::unordered_map<int, int> c = make_umap(mode, "rehash");
    f_umap_rehash_it_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_rehash_it_llamada") {
    std::unordered_map<int, int> c = make_umap(mode, "rehash");
    f_umap_rehash_it_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_rehash_ref_recto") {
    std::unordered_map<int, int> c = make_umap(mode, "rehash");
    f_umap_rehash_ref_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_rehash_ref_guarda") {
    std::unordered_map<int, int> c = make_umap(mode, "rehash");
    f_umap_rehash_ref_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_rehash_ref_bucle") {
    std::unordered_map<int, int> c = make_umap(mode, "rehash");
    f_umap_rehash_ref_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_rehash_ref_llamada") {
    std::unordered_map<int, int> c = make_umap(mode, "rehash");
    f_umap_rehash_ref_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_rehash_ptr_recto") {
    std::unordered_map<int, int> c = make_umap(mode, "rehash");
    f_umap_rehash_ptr_recto(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_rehash_ptr_guarda") {
    std::unordered_map<int, int> c = make_umap(mode, "rehash");
    f_umap_rehash_ptr_guarda(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_rehash_ptr_bucle") {
    std::unordered_map<int, int> c = make_umap(mode, "rehash");
    f_umap_rehash_ptr_bucle(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  if (id == "f_umap_rehash_ptr_llamada") {
    std::unordered_map<int, int> c = make_umap(mode, "rehash");
    f_umap_rehash_ptr_llamada(c);
    return runtime_sink == -1; // evita eliminar el uso final durante optimización
  }
  return 65; // identificador de caso desconocido
}
