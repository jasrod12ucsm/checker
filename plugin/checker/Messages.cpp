//===- Messages.cpp ---------------------------------------------------------===//
#include "checker/Messages.h"

using namespace ucsm::dominio;

namespace ucsm::messages {
namespace {

/// «un iterador invalidado», «una referencia invalidada».
std::string what(HandleCategory C, const char *Adj) {
  switch (C) {
  case HandleCategory::Iterator: return std::string("un iterador ") + Adj + "o";
  case HandleCategory::Reference: return std::string("una referencia ") + Adj + "a";
  case HandleCategory::Pointer: return std::string("un puntero ") + Adj + "o";
  }
  return "un handle";
}

std::string opName(const MutationEvent &E) {
  return std::string("'") + nameOf(E.M.Container) + "::" + nameOf(E.M.Op) + "'";
}

std::string line(unsigned L) { return L ? " (línea " + std::to_string(L) + ")" : ""; }

std::string condition(Condition C) {
  switch (C) {
  case Condition::CapacityReached: return "si la capacidad está agotada reubica los elementos";
  case Condition::RehashTriggered: return "si supera el factor de carga rehace las cubetas";
  case Condition::NonBinding: return "puede reubicar los elementos (la implementación decide)";
  case Condition::None: return "";
  }
  return "";
}

} // namespace

std::string confirmed(const UseVerdict &V, unsigned MutationLine) {
  std::string S = "Uso de " + what(V.Category, "invalidad");
  if (const auto &E = V.Why.cause())
    S += ": " + opName(*E) + line(MutationLine) + " lo invalidó";
  return S;
}

std::string possibly(const UseVerdict &V, unsigned CauseLine) {
  std::string S = "Uso de " + what(V.Category, "posiblemente invalidad");
  const auto &E = V.Why.cause();
  switch (V.Why.reason()) {
  case UnresolvedReason::DependsOnState:
    if (E)
      S += ": " + opName(*E) + line(CauseLine) + " " + condition(V.Why.condition());
    break;
  case UnresolvedReason::RelationUnknown:
    if (E)
      S += ": " + opName(*E) + line(CauseLine) +
           " lo invalida si el elemento está en el punto de la operación";
    break;
  case UnresolvedReason::EscapedToOpaqueCode:
    S += ": el contenedor se pasó a código que no se analiza" + line(CauseLine);
    break;
  case UnresolvedReason::None: break;
  }
  switch (V.Missing) {
  case MissingGuarantee::ReserveBefore:
    S += "; nada garantiza espacio: use reserve(size() + n) antes, o vuelva a obtenerlo";
    break;
  case MissingGuarantee::SizeAtLeastTwo: S += "; nada garantiza que no sea ese elemento"; break;
  case MissingGuarantee::ReobtainAfter: S += "; vuelva a obtenerlo después de la operación"; break;
  case MissingGuarantee::None: break;
  }
  return S;
}

std::string invalidatedNote(const MutationEvent &E, HandleKind K) {
  return std::string(K == HandleKind::IteratorObject ? "El iterador" : "El handle al elemento") +
         " queda invalidado por " + opName(E);
}

std::string unresolvedNote(const Validity &V, HandleKind K) {
  std::string S = K == HandleKind::IteratorObject ? "El iterador" : "El handle al elemento";
  if (const auto &E = V.cause())
    return S + " puede quedar invalidado por " + opName(*E);
  return S + " puede quedar invalidado";
}

std::string obtainedNote(ContainerKind C, const std::string &Method, HandleKind K) {
  std::string S =
      K == HandleKind::IteratorObject ? "El iterador se obtiene" : "El handle al elemento se obtiene";
  return S + " de '" + nameOf(C) + "::" + Method + "'";
}

std::string derefNote() { return "El handle al elemento se obtiene al desreferenciar el iterador"; }

std::string guaranteeNote(unsigned K) {
  return "reserve garantiza " + std::to_string(K) + " inserción(es) sin reubicar";
}

} // namespace ucsm::messages
