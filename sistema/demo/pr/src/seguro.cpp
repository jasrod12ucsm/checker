#include <vector>

// Uso correcto: reserve(size() + 1) garantiza que push_back no reubique.
int con_garantia(std::vector<int>& v) {
  v.reserve(v.size() + 1);
  int& x = v[0];
  v.push_back(1);
  return x;
}

int main() {
  std::vector<int> v{1};
  return con_garantia(v);
}
