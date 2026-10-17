#include <stdexcept>

// --- Casos que DEBEN reportarse -------------------------------------------
void slicing_simple() {
  try { throw std::runtime_error("boom"); }
  catch (std::exception e) { (void)e; }              // <- hallazgo 1
}

struct MiError : std::runtime_error {
  using std::runtime_error::runtime_error;
  int codigo = 42;
};

void slicing_derivada() {
  try { throw MiError("boom"); }
  catch (std::runtime_error e) { (void)e; }          // <- hallazgo 2
}

// --- Casos que NO deben reportarse ----------------------------------------
void correcto_const_ref() {
  try { throw std::runtime_error("ok"); }
  catch (const std::exception &e) { (void)e; }
}

void correcto_ref_mutable() {
  try { throw std::runtime_error("ok"); }
  catch (std::exception &e) { (void)e; }
}

void escalar_por_valor() {
  try { throw 1; }
  catch (int v) { (void)v; }                          // escalar: copiar es correcto
}

void por_puntero() {
  try { throw new int(1); }
  catch (int *p) { delete p; }
}

void catch_todo() {
  try { throw 1; }
  catch (...) { }
}
