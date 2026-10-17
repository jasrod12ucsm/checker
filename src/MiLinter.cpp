// mi-linter — herramienta LibTooling autonoma.
//
// Uso:
//   mi-linter archivo.cpp -- -std=c++17          (flags inline tras el `--`)
//   mi-linter -p build/ archivo.cpp              (flags desde compile_commands.json)
//
// Codigo de salida: 0 si no hay hallazgos, 1 si los hay (util en CI).

#include "CatchByValueCheck.h"

#include "clang/ASTMatchers/ASTMatchFinder.h"
#include "clang/Tooling/CommonOptionsParser.h"
#include "clang/Tooling/Tooling.h"
#include "llvm/Support/CommandLine.h"
#include "llvm/Support/raw_ostream.h"

using namespace clang::tooling;
using namespace clang::ast_matchers;

// Toda herramienta LibTooling agrupa sus flags propias bajo una categoria;
// las que no pertenecen a ella se ocultan del --help.
static llvm::cl::OptionCategory MiCategoria("opciones de mi-linter");

static llvm::cl::extrahelp ComunHelp(CommonOptionsParser::HelpMessage);
static llvm::cl::extrahelp MasAyuda(
    "\nDetecta excepciones capturadas por valor (object slicing).\n");

int main(int argc, const char **argv) {
  // FASE 1: parsear la linea de comandos y resolver la base de compilacion.
  auto Opciones = CommonOptionsParser::create(argc, argv, MiCategoria);
  if (!Opciones) {
    llvm::errs() << llvm::toString(Opciones.takeError());
    return 2;
  }

  // FASE 2: construir la herramienta sobre los ficheros pedidos.
  ClangTool Herramienta(Opciones->getCompilations(),
                        Opciones->getSourcePathList());

  // FASE 3: registrar las reglas. Anadir una regla nueva = dos lineas aqui.
  MatchFinder Buscador;
  milinter::CatchByValueCheck Regla;
  Regla.registrar(Buscador);

  // FASE 4: ejecutar. ClangTool parsea cada TU, construye su AST y lo recorre
  // disparando los callbacks registrados en el MatchFinder.
  const int Estado = Herramienta.run(newFrontendActionFactory(&Buscador).get());
  if (Estado != 0)
    llvm::errs() << "aviso: alguna unidad de traduccion no compilo limpiamente\n";

  llvm::outs() << "\nmi-linter: " << Regla.hallazgos() << " hallazgo(s)\n";
  return Regla.hallazgos() > 0 ? 1 : 0;
}
