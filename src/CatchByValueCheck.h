#ifndef MI_LINTER_CATCH_BY_VALUE_CHECK_H
#define MI_LINTER_CATCH_BY_VALUE_CHECK_H

#include "clang/ASTMatchers/ASTMatchFinder.h"

namespace milinter {

/// Regla: detecta `catch (Excepcion e)` capturado por valor.
///
/// Capturar una excepcion polimorfica por valor produce *object slicing*: se
/// copia solo el subobjeto de la clase base y se pierde el tipo dinamico, con
/// el que se pierden el `what()` real y cualquier dato de la derivada.
/// La correccion es `catch (const Excepcion &e)`.
class CatchByValueCheck : public clang::ast_matchers::MatchFinder::MatchCallback {
public:
  /// Registra el patron sintactico que nos interesa en el MatchFinder.
  void registrar(clang::ast_matchers::MatchFinder &Finder);

  /// Se invoca una vez por cada nodo del AST que casa con el patron.
  void run(const clang::ast_matchers::MatchFinder::MatchResult &Result) override;

  unsigned hallazgos() const { return Hallazgos; }

private:
  unsigned Hallazgos = 0;
};

} // namespace milinter

#endif
