#include "CatchByValueCheck.h"

#include "clang/AST/ASTContext.h"
#include "clang/AST/Decl.h"
#include "clang/ASTMatchers/ASTMatchers.h"
#include "clang/Basic/Diagnostic.h"
#include "clang/Basic/SourceManager.h"

using namespace clang;
using namespace clang::ast_matchers;

namespace milinter {

// ---------------------------------------------------------------------------
// FASE A: el patron sintactico.
//
//   varDecl(...)            -> una declaracion de variable
//   isExceptionVariable()   -> ...que es la variable de un `catch`
//   hasCanonicalType(       -> ...cuyo tipo, con typedefs y alias ya resueltos,
//     recordType())            es un struct/class (NO una referencia, NO un
//                              puntero, NO un escalar como `int`)
//
// El tipo canonico de `const std::exception &` es un LValueReferenceType, asi
// que las capturas correctas quedan descartadas sin escribir un solo `if`.
// Este matcher se descubre interactivamente con:  clang-query archivo.cpp --
// ---------------------------------------------------------------------------
void CatchByValueCheck::registrar(MatchFinder &Finder) {
  Finder.addMatcher(
      varDecl(isExceptionVariable(), hasType(hasCanonicalType(recordType())))
          .bind("exvar"),
      this);
}

// ---------------------------------------------------------------------------
// FASE B: el callback. Aqui filtramos ruido y emitimos el diagnostico.
// ---------------------------------------------------------------------------
void CatchByValueCheck::run(const MatchFinder::MatchResult &Result) {
  const auto *Var = Result.Nodes.getNodeAs<VarDecl>("exvar");
  if (!Var)
    return;

  const SourceManager &SM = *Result.SourceManager;
  const SourceLocation NombreLoc = Var->getLocation();

  // --- Filtros de contexto ------------------------------------------------
  // Sin estos, un linter nuevo escupe cientos de falsos positivos en headers
  // de terceros y dentro de macros que el usuario no puede editar.
  if (NombreLoc.isInvalid() || NombreLoc.isMacroID())
    return;
  if (!SM.isWrittenInMainFile(NombreLoc))
    return;

  // --- Construccion del fix-it -------------------------------------------
  // Queremos pasar de     catch (std::exception e)
  //                a      catch (const std::exception &e)
  // Son dos inserciones: "const " antes del tipo y "&" antes del nombre.
  const TypeSourceInfo *TSI = Var->getTypeSourceInfo();
  const SourceLocation TipoLoc =
      TSI ? TSI->getTypeLoc().getBeginLoc() : SourceLocation();

  DiagnosticsEngine &DE = Result.Context->getDiagnostics();

  // getCustomDiagID registra el mensaje una vez y devuelve un ID reutilizable.
  // El nivel (Warning/Error/Remark) decide si el build falla o solo avisa.
  const unsigned ID = DE.getCustomDiagID(
      DiagnosticsEngine::Warning,
      "excepcion '%0' capturada por valor; usa 'const %0 &' para evitar "
      "object slicing");

  DiagnosticBuilder Diag = DE.Report(NombreLoc, ID) << Var->getType().getAsString();

  Diag << FixItHint::CreateInsertion(NombreLoc, "&");
  if (TipoLoc.isValid() && !Var->getType().isConstQualified())
    Diag << FixItHint::CreateInsertion(TipoLoc, "const ");

  ++Hallazgos;
}

} // namespace milinter
