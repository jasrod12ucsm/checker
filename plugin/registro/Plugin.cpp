//===- Plugin.cpp - Registro del checker en Clang Static Analyzer -----------===//
//
// Se carga con:
//   clang++ --analyze -Xclang -load -Xclang libContainerInvalidation.so \
//           -Xclang -analyzer-checker=ucsm.ContainerInvalidation …
//
//===----------------------------------------------------------------------===//
#include "checker/InvalidationChecker.h"

#include "clang/StaticAnalyzer/Core/CheckerManager.h"
#include "clang/StaticAnalyzer/Frontend/CheckerRegistry.h"

using namespace clang;
using namespace clang::ento;

namespace {

void registerInvalidation(CheckerManager &Mgr) {
  auto *Chk = Mgr.registerChecker<ucsm::InvalidationChecker>();
  StringRef Mode = Mgr.getAnalyzerOptions().getCheckerStringOption(Chk, "PolicyMode");
  Chk->setPolicyMode(Mode == "Possibly" ? ucsm::dominio::PolicyMode::Possibly
                                        : ucsm::dominio::PolicyMode::Silent);
  Chk->setDebug(Mgr.getAnalyzerOptions().getCheckerBooleanOption(Chk, "Debug"));
}

bool shouldRegister(const CheckerManager &) { return true; }

} // namespace

extern "C" void clang_registerCheckers(CheckerRegistry &Registry) {
  Registry.addChecker(registerInvalidation, shouldRegister, "ucsm.ContainerInvalidation",
                      "Uso de iteradores, referencias o punteros a elementos de "
                      "contenedores de la STL después de una mutación que los invalida",
                      "", /*IsHidden=*/false);
  Registry.addCheckerOption("string", "ucsm.ContainerInvalidation", "PolicyMode", "Silent",
                            "Silent: sólo avisos confirmados. Possibly: también avisos "
                            "posibles cuando la invalidación depende del estado.",
                            "released");
  Registry.addCheckerOption("bool", "ucsm.ContainerInvalidation", "Debug", "false",
                            "Escribe en stderr cada obtención, mutación, uso y escape.", "released");
}

extern "C" const char clang_analyzerAPIVersionString[] = CLANG_ANALYZER_API_VERSION_STRING;
