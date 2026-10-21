//===- Decisions.cpp --------------------------------------------------------===//
#include "Decisions.h"

#include "NormTable.h"

namespace ucsm::dominio {

HandleState obtain(const Origin &O) { return HandleState(O, Validity::valid()); }

SolverAnswer answer(Condition Cond, Growth G, Credit C) {
  switch (Cond) {
  case Condition::CapacityReached:
  case Condition::RehashTriggered:
    // El crédito sólo cubre inserciones de un elemento.
    if (G == Growth::One && C && *C >= 1)
      return SolverAnswer::OnlyNo;
    return SolverAnswer::Both;
  case Condition::NonBinding:
  case Condition::None: return SolverAnswer::Both;
  }
  return SolverAnswer::Both;
}

namespace {

/// Las relaciones candidatas: la geometría restringida a lo que la norma admite.
RelationSet candidates(const MutationEvent &E, const HandleState &H, HandleCategory Cat) {
  RelationSet Norm = relationsOf(E.M, Cat);
  if (Norm.contains(Relation::Any))
    return RelationSet::of(Relation::Any);
  RelationSet S =
      (E.RangeEnd ? relateRange(H.position(), E.PointPos, *E.RangeEnd) : relate(H.position(), E.PointPos)) &
      Norm;
  return S.empty() ? Norm : S;
}

} // namespace

ApplyResult apply(const MutationEvent &E, const HandleState &H, Credit C) {
  ValidityKind K = H.validity().kind();
  if (K == ValidityKind::Invalidated || K == ValidityKind::Diagnosed)
    return {H, false}; // absorbente

  HandleCategory Cat = categoryOf(H.kind());
  Growth G = growthOf(E.M).value_or(Growth::Unknown);
  RelationSet Rels = candidates(E, H, Cat);

  // ¿Todas las relaciones candidatas dicen lo mismo?
  std::optional<Effect> Common;
  std::optional<Relation> Only;
  bool Agree = true;
  unsigned Count = 0;
  for (Relation R : AllRelations) {
    if (!Rels.contains(R))
      continue;
    ++Count;
    Only = R;
    std::optional<Effect> Ef = effectOf(E.M, Cat, R);
    if (!Ef)
      continue;
    if (!Common)
      Common = Ef;
    else if (!sameEffect(*Common, *Ef))
      Agree = false;
  }
  if (!Common)
    return {H, false}; // la norma no dice nada: no se toca (lo prueba la ley de totalidad)
  if (!Agree) {
    Validity V = H.validity().join(Validity::relationUnknown(E));
    return {H.withValidity(V).withPosition(Position::unknown()), V != H.validity()};
  }

  // Si hubo varias relaciones con el mismo efecto, la posición nueva no se sabe.
  auto Transported = [&](const HandleState &S) {
    if (Count == 1)
      return S.withPosition(
          transport(E.M, G, *Only, S.position(), E.RangeEnd ? distance(E.PointPos, *E.RangeEnd) : 1));
    return S.withPosition(Position::unknown());
  };

  switch (Common->Kind) {
  case EffectKind::Preserves: return {Transported(H), false};
  case EffectKind::Invalidates: return {H.withValidity(Validity::invalidated(E)), true};
  case EffectKind::Depends:
    switch (answer(Common->Cond, G, C)) {
    case SolverAnswer::OnlyNo: return {Transported(H), false};
    case SolverAnswer::OnlyYes: return {H.withValidity(Validity::invalidated(E)), true};
    case SolverAnswer::Both: {
      Validity V = H.validity().join(Validity::dependsOn(Common->Cond, E));
      return {Transported(H).withValidity(V), V != H.validity()};
    }
    }
  }
  return {H, false};
}

Credit consume(const Mutation &M, Credit C) {
  switch (growthOf(M).value_or(Growth::Unknown)) {
  case Growth::One:
    if (C && *C > 0)
      return *C - 1;
    return C;
  case Growth::None:
  case Growth::Shrinks: return C;
  case Growth::Unknown:
  case Growth::Reset: return std::nullopt;
  }
  return std::nullopt;
}

namespace {

MissingGuarantee missingFor(const Validity &V) {
  switch (V.reason()) {
  case UnresolvedReason::DependsOnState:
    return V.condition() == Condition::NonBinding ? MissingGuarantee::ReobtainAfter
                                                  : MissingGuarantee::ReserveBefore;
  case UnresolvedReason::RelationUnknown: return MissingGuarantee::SizeAtLeastTwo;
  case UnresolvedReason::EscapedToOpaqueCode: return MissingGuarantee::ReobtainAfter;
  case UnresolvedReason::None: return MissingGuarantee::None;
  }
  return MissingGuarantee::None;
}

} // namespace

UseResult onUse(const HandleState &H, HandleCategory At, PolicyMode Mode) {
  const Validity &V = H.validity();
  switch (V.kind()) {
  case ValidityKind::Valid:
  case ValidityKind::UnresolvedDiagnosed:
  case ValidityKind::Diagnosed: return {{VerdictKind::Fine, At, V, MissingGuarantee::None}, H};
  case ValidityKind::Unresolved:
    if (Mode == PolicyMode::Silent)
      return {{VerdictKind::Fine, At, V, MissingGuarantee::None}, H};
    return {{VerdictKind::Possibly, At, V, missingFor(V)}, H.withValidity(V.diagnosed())};
  case ValidityKind::Invalidated:
    return {{VerdictKind::Confirmed, At, V, MissingGuarantee::None}, H.withValidity(V.diagnosed())};
  }
  return {{VerdictKind::Fine, At, V, MissingGuarantee::None}, H};
}

std::optional<HandleState> escape(const HandleState &H, SourceRef At) {
  if (H.validity().kind() >= ValidityKind::Invalidated)
    return H;
  return std::nullopt;
}

HandleState move(const HandleState &H, Step S) {
  switch (S.Kind) {
  case StepKind::Increment: return H.withPosition(H.position().advance(+1));
  case StepKind::Decrement: return H.withPosition(H.position().advance(-1));
  case StepKind::Advance: return H.withPosition(H.position().advance(S.N));
  case StepKind::UnknownStep: return H.withPosition(Position::unknown());
  }
  return H;
}

} // namespace ucsm::dominio
