#include <string>
#include <vector>

// PR de ejemplo: una caché de nombres con dos errores de invalidación.
struct Cache {
  std::vector<std::string> nombres;

  const std::string& ultimo_tras_limpiar() {
    const std::string& r = nombres[0];
    nombres.clear();
    return r;  // la referencia quedó colgando
  }

  std::size_t agregar_y_medir(const std::string& n) {
    std::string& primero = nombres[0];
    nombres.push_back(n);       // puede reubicar si la capacidad está agotada
    return primero.size();
  }
};

int main() {
  Cache c;
  c.nombres = {"a", "b"};
  return static_cast<int>(c.agregar_y_medir("c") + c.ultimo_tras_limpiar().size());
}
