//===- Position.cpp ---------------------------------------------------------===//
#include "Position.h"

namespace ucsm::dominio {

Position Position::advance(int Delta) const {
  switch (B) {
  case Base::First: return first(N + Delta);
  case Base::Anchor: return anchor(Id, N + Delta); // ancla-1 sigue siendo un elemento definido
  case Base::Last:
    if (N - Delta == -1)
      return pastEnd();
    return last(N - Delta);
  case Base::PastEnd: return Delta == -1 ? last(0) : unknown();
  case Base::Unknown: return unknown();
  }
  return unknown();
}

RelationSet relate(const Position &H, const Position &P) {
  using B = Position::Base;
  if (H.base() == B::Unknown || P.base() == B::Unknown)
    return RelationSet::ordered();
  if (P.base() == B::PastEnd)
    // Todo elemento está antes del final; un iterador end() es «el mismo».
    return RelationSet::of(H.base() == B::PastEnd ? Relation::Same : Relation::Before);
  if (H.base() == B::PastEnd)
    return RelationSet::of(Relation::After);
  if (H.base() == P.base() && H.anchorId() == P.anchorId()) {
    // First/Anchor: mayor offset = más adelante. Last: mayor offset = más atrás.
    int D = H.forward() ? H.offset() - P.offset() : P.offset() - H.offset();
    if (D == 0)
      return RelationSet::of(Relation::Same);
    return RelationSet::of(D > 0 ? Relation::After : Relation::Before);
  }
  // First+a frente a Last-b, o anclas distintas: no se sabe.
  return RelationSet::ordered();
}

RelationSet relateRange(const Position &H, const Position &First, const Position &Last) {
  RelationSet S;
  RelationSet AtFirst = relate(H, First);
  if (AtFirst.contains(Relation::Before))
    S = S.with(Relation::Before);
  if (AtFirst.contains(Relation::Same) || AtFirst.contains(Relation::After)) {
    RelationSet AtLast = relate(H, Last);
    if (AtLast.contains(Relation::Before))
      S = S.with(Relation::Same);
    if (AtLast.contains(Relation::Same) || AtLast.contains(Relation::After))
      S = S.with(Relation::After);
  }
  return S;
}

std::optional<int> distance(const Position &First, const Position &Last) {
  using B = Position::Base;
  if (First.base() == B::Unknown || Last.base() == B::Unknown)
    return std::nullopt;
  if (First.base() == Last.base() && First.anchorId() == Last.anchorId() && First.base() != B::PastEnd)
    return First.forward() ? Last.offset() - First.offset() : First.offset() - Last.offset();
  if (First.base() == B::Last && Last.base() == B::PastEnd)
    return First.offset() + 1;
  return std::nullopt;
}

Position transport(const Mutation &M, Growth G, Relation R, const Position &H, std::optional<int> Count) {
  using B = Position::Base;
  if (M.At == Point::Whole || M.At == Point::ByKey) {
    // reserve/shrink_to_fit de vector no reordenan; el resto (sort, reverse,
    // insertar en un árbol o en una tabla) puede cambiar el orden.
    if (M.Op == Operation::Reserve && M.Container == ContainerKind::Vector)
      return H;
    return Position::unknown();
  }
  if (H.base() == B::Unknown || H.base() == B::PastEnd)
    return H;
  if (R == Relation::Any)
    return Position::unknown();
  int Delta = 0;
  switch (G) {
  case Growth::One:
  case Growth::Shrinks:
    if (!Count)
      // Cuántos salieron no se sabe: sólo lo de antes del punto queda donde estaba.
      return (H.forward() && R == Relation::Before) ? H : Position::unknown();
    Delta = G == Growth::One ? *Count : -*Count;
    break;
  case Growth::None: return H;
  case Growth::Unknown:
  case Growth::Reset:
    // Lo que está antes del punto no se mueve; lo demás no se sabe.
    return (H.forward() && R == Relation::Before) ? H : Position::unknown();
  }
  // First+n (y ancla+n) se corre si el cambio fue en o antes de él
  // (R = Same/After); Last-n se corre si el cambio fue después (R = Before).
  // Todos los handles del contenedor se transportan con la misma mutación,
  // así que las distancias entre handles de la misma ancla se conservan.
  if (H.forward())
    return R == Relation::Before ? H : H.advance(Delta);
  return R == Relation::Before ? Position::last(H.offset() + Delta) : H;
}

} // namespace ucsm::dominio
