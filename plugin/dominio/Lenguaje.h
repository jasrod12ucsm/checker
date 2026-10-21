//===- Lenguaje.h - Lenguaje ubicuo de la detección -------------*- C++ -*-===//
//
// Tipos cerrados del DSL (libro/diseno/dsl/norma.md y deteccion.md).
// Este directorio NO incluye Clang: si un #include "clang/..." aparece aquí,
// no compila (CMake no da esos include dirs a este target).
//
//===----------------------------------------------------------------------===//
#ifndef UCSM_DOMINIO_LENGUAJE_H
#define UCSM_DOMINIO_LENGUAJE_H

#include <cstdint>

namespace ucsm::dominio {

enum class ContainerKind : std::uint8_t {
  Vector,
  Deque,
  List,
  ForwardList,
  Set,
  Multiset,
  Map,
  Multimap,
  UnorderedSet,
  UnorderedMap
};

enum class Operation : std::uint8_t {
  PushBack,
  EmplaceBack,
  PushFront,
  EmplaceFront,
  Insert,
  InsertAfter,
  Emplace,
  Subscript,
  Erase,
  EraseAfter,
  PopBack,
  PopFront,
  Clear,
  Assign,
  Resize,
  Reserve,
  ShrinkToFit,
  Rehash,
  Reverse,
  Sort
};

/// Dónde actúa la operación.
enum class Point : std::uint8_t { Front, Back, Interior, Whole, ByKey };

/// Cuánto cambia size(); lo usa el crédito de reserve (D-19).
enum class Growth : std::uint8_t { One, None, Shrinks, Unknown, Reset };

/// Categoría de la norma. Pointer sigue la regla de Reference.
enum class HandleCategory : std::uint8_t { Iterator, Reference, Pointer };

/// El elemento del handle frente al punto de la mutación.
enum class Relation : std::uint8_t { Same, Before, After, Any };

enum class EffectKind : std::uint8_t { Preserves, Depends, Invalidates };

enum class Condition : std::uint8_t { None, CapacityReached, RehashTriggered, NonBinding };

/// Qué región guarda el estado: el objeto iterador o el elemento (D-06).
enum class HandleKind : std::uint8_t { IteratorObject, Element };

struct Mutation {
  ContainerKind Container;
  Operation Op;
  Point At;
};

constexpr bool operator==(const Mutation &A, const Mutation &B) {
  return A.Container == B.Container && A.Op == B.Op && A.At == B.At;
}
constexpr bool operator!=(const Mutation &A, const Mutation &B) { return !(A == B); }

/// La categoría de la norma que corresponde a un tipo de handle guardado.
constexpr HandleCategory categoryOf(HandleKind K) {
  switch (K) {
  case HandleKind::IteratorObject: return HandleCategory::Iterator;
  case HandleKind::Element: return HandleCategory::Reference;
  }
  return HandleCategory::Reference;
}

const char *nameOf(ContainerKind K);
const char *nameOf(Operation Op);
const char *nameOf(HandleCategory C);

} // namespace ucsm::dominio

#endif
