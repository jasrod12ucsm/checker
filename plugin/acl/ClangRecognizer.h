//===- ClangRecognizer.h - Clang → lenguaje ubicuo --------------*- C++ -*-===//
//
// Capa anticorrupción (deteccion.md §1). Sabe de CallEvent, Expr y SVal;
// devuelve valores del dominio. No decide nada: no conoce la norma.
//
//===----------------------------------------------------------------------===//
#ifndef UCSM_ACL_CLANGRECOGNIZER_H
#define UCSM_ACL_CLANGRECOGNIZER_H

#include "Decisions.h"

#include "clang/StaticAnalyzer/Core/PathSensitive/CallEvent.h"
#include "clang/StaticAnalyzer/Core/PathSensitive/CheckerContext.h"
#include "llvm/ADT/STLFunctionalExtras.h"

#include <optional>

namespace ucsm::acl {

using clang::ento::CallEvent;
using clang::ento::CheckerContext;
using clang::ento::MemRegion;
using clang::ento::SVal;

/// La región que identifica a un objeto iterador, desde cualquier SVal que lo
/// denote (loc de su región o LazyCompoundVal de una copia).
const MemRegion *iteratorRegion(SVal V);

/// La región del contenedor sobre el que se llama un método de la STL, si el
/// método es de uno de los diez contenedores.
struct ContainerCall {
  const MemRegion *Region;
  dominio::ContainerKind Kind;
  llvm::StringRef Method;
};
std::optional<ContainerCall> containerCall(const CallEvent &Call);

/// begin()/cbegin()/find()/lower_bound()/upper_bound(): un iterador nuevo.
std::optional<dominio::Position> iteratorObtention(const ContainerCall &CC, const CallEvent &Call);

/// front()/back()/operator[]/at()/data(): un handle a un elemento.
std::optional<dominio::Position> elementAccess(const ContainerCall &CC, const CallEvent &Call,
                                               CheckerContext &C);

/// Dónde está el iterador que denota una expresión, según el estado.
using PositionOf = llvm::function_ref<std::optional<dominio::Position>(SVal)>;

struct MutationCall {
  dominio::Mutation M;
  dominio::Position PointPos;
  std::optional<unsigned> Guarantee;                        // reserve(c.size() + k) → k
  bool ReturnsIterator;                                     // erase / insert / emplace posicionales
  std::optional<dominio::Position> RangeEnd = std::nullopt; // erase(first, last): last
};
/// Un mutador reconocido. nullopt: el método no muta o no está en la norma.
std::optional<MutationCall> mutation(const ContainerCall &CC, const CallEvent &Call, CheckerContext &C,
                                     PositionOf Pos);

/// Qué hace una llamada con un iterador que ya se sigue.
enum class IteratorOp { None, Deref, Increment, Decrement, Advance, Compare };
struct IteratorUse {
  IteratorOp Op;
  const MemRegion *Iterator;
  int Delta;    // Increment/Decrement/Advance; 0 si no es una constante
  bool InPlace; // ++it, it += n, std::advance: mueve `it`. it + n, std::next: da otro
};
/// La llamada usa un iterador seguido (isTracked lo dice).
std::optional<IteratorUse> iteratorUse(const CallEvent &Call, CheckerContext &C,
                                       llvm::function_ref<bool(const MemRegion *)> IsTracked);

/// La región seguida del iterador que se pasa como argumento I. Se busca en
/// orden: el parámetro (donde CSA construye la copia, también la convertida
/// iterator → const_iterator), el valor del argumento y la variable que nombra.
const MemRegion *argumentIterator(const CallEvent &Call, unsigned I, CheckerContext &C,
                                  llvm::function_ref<bool(const MemRegion *)> IsTracked);

/// La categoría de la norma observada en el sitio de una carga.
dominio::HandleCategory categoryAtLoad(const clang::Stmt *S);

/// ¿Es un constructor de copia/movimiento o una asignación entre iteradores?
/// Devuelve (desde, hacia).
std::optional<std::pair<const MemRegion *, const MemRegion *>> iteratorCopy(const CallEvent &Call);

} // namespace ucsm::acl

#endif
