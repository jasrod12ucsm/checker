//===- InvalidationChecker.h - La cáscara CSA -------------------*- C++ -*-===//
//
// Cada callback: cargar (ProgramState) → traducir (acl) → decidir (dominio)
// → aplicar (addTransition, emitReport). Aquí no hay reglas de la norma.
//
//===----------------------------------------------------------------------===//
#ifndef UCSM_CHECKER_INVALIDATIONCHECKER_H
#define UCSM_CHECKER_INVALIDATIONCHECKER_H

#include "Decisions.h"

#include "clang/StaticAnalyzer/Core/BugReporter/BugType.h"
#include "clang/StaticAnalyzer/Core/Checker.h"
#include "clang/StaticAnalyzer/Core/PathSensitive/CallEvent.h"
#include "clang/StaticAnalyzer/Core/PathSensitive/CheckerContext.h"

namespace ucsm {

class InvalidationChecker
    : public clang::ento::Checker<clang::ento::check::PreCall, clang::ento::check::PostCall,
                                  clang::ento::check::Location, clang::ento::check::Bind,
                                  clang::ento::check::DeadSymbols, clang::ento::check::RegionChanges> {
public:
  void setPolicyMode(dominio::PolicyMode M) { Mode = M; }
  void setDebug(bool D) { Debug = D; }

  void checkPreCall(const clang::ento::CallEvent &Call, clang::ento::CheckerContext &C) const;
  void checkPostCall(const clang::ento::CallEvent &Call, clang::ento::CheckerContext &C) const;
  void checkLocation(clang::ento::SVal Loc, bool IsLoad, const clang::Stmt *S,
                     clang::ento::CheckerContext &C) const;
  void checkBind(clang::ento::SVal Loc, clang::ento::SVal Val, const clang::Stmt *S,
                 clang::ento::CheckerContext &C) const;
  void checkDeadSymbols(clang::ento::SymbolReaper &SR, clang::ento::CheckerContext &C) const;
  clang::ento::ProgramStateRef checkRegionChanges(clang::ento::ProgramStateRef State,
                                                  const clang::ento::InvalidatedSymbols *Invalidated,
                                                  llvm::ArrayRef<const clang::ento::MemRegion *> Explicits,
                                                  llvm::ArrayRef<const clang::ento::MemRegion *> Regions,
                                                  const clang::LocationContext *LCtx,
                                                  const clang::ento::CallEvent *Call) const;

private:
  /// Un uso de un handle: decide, y si hay aviso lo emite. Devuelve el estado
  /// siguiente (o nullptr si no cambió nada).
  clang::ento::ProgramStateRef use(clang::ento::ProgramStateRef St, const clang::ento::MemRegion *R,
                                   bool IsIterator, dominio::HandleCategory At, const clang::Stmt *S,
                                   clang::ento::CheckerContext &C) const;

  const clang::ento::BugType Confirmed{this, "Uso de un handle invalidado",
                                       "Invalidación de contenedores (STL)"};
  const clang::ento::BugType Possible{this, "Uso de un handle posiblemente invalidado",
                                      "Invalidación de contenedores (STL)"};
  /// Traza de eventos en stderr (opción Debug=true): para depurar código real.
  void trace(const clang::SourceManager &SM, const clang::Stmt *S, llvm::StringRef What,
             const clang::ento::MemRegion *R) const;
  void trace(clang::ento::CheckerContext &C, const clang::Stmt *S, llvm::StringRef What,
             const clang::ento::MemRegion *R) const {
    trace(C.getSourceManager(), S, What, R);
  }

  dominio::PolicyMode Mode = dominio::PolicyMode::Silent;
  bool Debug = false;
};

} // namespace ucsm

#endif
