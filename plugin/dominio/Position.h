//===- Position.h - Dónde está un elemento en su contenedor -----*- C++ -*-===//
//
// First+n, Last-n, Anchor(a)+n, PastEnd o Unknown. relate() da la geometría
// (qué relaciones son posibles); transport() mueve la posición cuando una
// mutación preserva el handle.
//
// Un ancla es un elemento definido cuya posición absoluta no se sabe (lo que
// da find(), o advance(it, k) con k desconocido). Dos handles con la misma
// ancla sí se pueden comparar: `jt = std::next(it)` queda en ancla+1. El id
// es opaco y único por camino (la cáscara conjura un símbolo).
//
//===----------------------------------------------------------------------===//
#ifndef UCSM_DOMINIO_POSITION_H
#define UCSM_DOMINIO_POSITION_H

#include "Lenguaje.h"
#include "NormTable.h"

#include <optional>

namespace ucsm::dominio {

class Position {
public:
  enum class Base : std::uint8_t { First, Last, Anchor, PastEnd, Unknown };

  static constexpr Position first(int N = 0) { return N < 0 ? unknown() : Position(Base::First, N); }
  /// Last-n: el n-ésimo contando desde el último (n ≥ 0).
  static constexpr Position last(int N = 0) { return N < 0 ? unknown() : Position(Base::Last, N); }
  static constexpr Position anchor(const void *Id, int N = 0) {
    return Id ? Position(Base::Anchor, N, Id) : unknown();
  }
  static constexpr Position pastEnd() { return Position(Base::PastEnd, 0); }
  static constexpr Position unknown() { return Position(Base::Unknown, 0); }

  constexpr Base base() const { return B; }
  /// First: distancia desde el primero. Last: distancia hacia atrás desde el último.
  constexpr int offset() const { return N; }
  /// Sólo en Anchor.
  constexpr const void *anchorId() const { return Id; }
  /// First y Anchor cuentan hacia adelante desde un elemento.
  constexpr bool forward() const { return B == Base::First || B == Base::Anchor; }

  /// ++it (+1), --it (-1), it + n.
  Position advance(int Delta) const;

  constexpr bool operator==(const Position &O) const { return B == O.B && N == O.N && Id == O.Id; }
  constexpr bool operator!=(const Position &O) const { return !(*this == O); }

private:
  constexpr Position(Base B, int N, const void *Id = nullptr) : B(B), N(N), Id(Id) {}
  Base B;
  int N;
  const void *Id;
};

/// Relaciones geométricamente posibles del elemento en H frente al punto P.
RelationSet relate(const Position &H, const Position &P);

/// Relaciones del elemento en H frente al rango semiabierto [First, Last) que
/// borra erase(first, last): Before si está antes de First, Same si está
/// dentro, After si está en Last o después. Con First = Last (rango vacío)
/// nada es Same: el elemento de `last` nunca se borra.
RelationSet relateRange(const Position &H, const Position &First, const Position &Last);

/// Last - First, si las dos cuentan desde la misma base.
std::optional<int> distance(const Position &First, const Position &Last);

/// La posición después de una mutación que preservó el handle, sabiendo en
/// qué relación estaba con el punto. Count: cuántos elementos entraron o
/// salieron (1 salvo en un rango); sin valor, no se sabe.
Position transport(const Mutation &M, Growth G, Relation R, const Position &H, std::optional<int> Count = 1);

} // namespace ucsm::dominio

#endif
