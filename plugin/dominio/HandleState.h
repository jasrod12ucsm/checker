//===- HandleState.h - Lo que el motor sabe de un handle --------*- C++ -*-===//
//
// Valores inmutables del contexto Detección (deteccion.md §2). Las
// identidades (ContainerId, SourceRef) son opacas: la cáscara guarda ahí un
// const MemRegion* o un const Stmt*, y el núcleo sólo los compara.
//
//===----------------------------------------------------------------------===//
#ifndef UCSM_DOMINIO_HANDLESTATE_H
#define UCSM_DOMINIO_HANDLESTATE_H

#include "Lenguaje.h"
#include "Position.h"

#include <optional>

namespace ucsm::dominio {

class ContainerId {
public:
  constexpr explicit ContainerId(const void *P = nullptr) : P(P) {}
  constexpr const void *opaque() const { return P; }
  constexpr bool operator==(ContainerId O) const { return P == O.P; }
  constexpr bool operator!=(ContainerId O) const { return P != O.P; }

private:
  const void *P;
};

class SourceRef {
public:
  constexpr explicit SourceRef(const void *P = nullptr) : P(P) {}
  constexpr const void *opaque() const { return P; }
  constexpr bool operator==(SourceRef O) const { return P == O.P; }

private:
  const void *P;
};

struct MutationEvent {
  ContainerId Container;
  Mutation M;
  Position PointPos; // dónde cae el punto; Unknown si no se sabe
  SourceRef At;
  /// erase(first, last): el fin (excluido) del rango que se borra. Sin valor,
  /// la mutación actúa sobre un solo elemento, el del punto.
  std::optional<Position> RangeEnd = std::nullopt;

  bool operator==(const MutationEvent &O) const {
    return Container == O.Container && M == O.M && PointPos == O.PointPos && At == O.At &&
           RangeEnd == O.RangeEnd;
  }
};

struct Origin {
  ContainerId Container;
  HandleKind Kind;
  Position Pos;
  SourceRef At;

  bool operator==(const Origin &O) const {
    return Container == O.Container && Kind == O.Kind && Pos == O.Pos && At == O.At;
  }
};

/// Cadena Valid ⊑ Unresolved ⊑ UnresolvedDiagnosed ⊑ Invalidated ⊑ Diagnosed.
/// UnresolvedDiagnosed: ya se dio el aviso posible; si después se invalida
/// de verdad, el aviso confirmado todavía sale.
enum class ValidityKind : std::uint8_t { Valid, Unresolved, UnresolvedDiagnosed, Invalidated, Diagnosed };

enum class UnresolvedReason : std::uint8_t { None, DependsOnState, RelationUnknown, EscapedToOpaqueCode };

class Validity {
public:
  static Validity valid() {
    return Validity(ValidityKind::Valid, UnresolvedReason::None, Condition::None, std::nullopt, SourceRef());
  }
  static Validity dependsOn(Condition C, const MutationEvent &M) {
    return Validity(ValidityKind::Unresolved, UnresolvedReason::DependsOnState, C, M, M.At);
  }
  static Validity relationUnknown(const MutationEvent &M) {
    return Validity(ValidityKind::Unresolved, UnresolvedReason::RelationUnknown, Condition::None, M, M.At);
  }
  static Validity escaped(SourceRef At) {
    return Validity(ValidityKind::Unresolved, UnresolvedReason::EscapedToOpaqueCode, Condition::None,
                    std::nullopt, At);
  }
  static Validity invalidated(const MutationEvent &M) {
    return Validity(ValidityKind::Invalidated, UnresolvedReason::None, Condition::None, M, M.At);
  }

  ValidityKind kind() const { return K; }
  UnresolvedReason reason() const { return Why; }
  Condition condition() const { return Cond; }
  /// La mutación que causó el estado, si la hay.
  const std::optional<MutationEvent> &cause() const { return Cause; }
  SourceRef at() const { return At; }

  /// JOIN del semirretículo: gana el mayor; ante empate se conserva el
  /// primero (la causa original viaja con el estado).
  Validity join(const Validity &O) const { return O.K > K ? O : *this; }
  Validity diagnosed() const {
    Validity V = *this;
    V.K = K == ValidityKind::Unresolved ? ValidityKind::UnresolvedDiagnosed : ValidityKind::Diagnosed;
    return V;
  }

  bool operator==(const Validity &O) const {
    return K == O.K && Why == O.Why && Cond == O.Cond && Cause == O.Cause && At == O.At;
  }
  bool operator!=(const Validity &O) const { return !(*this == O); }

private:
  Validity(ValidityKind K, UnresolvedReason Why, Condition Cond, std::optional<MutationEvent> Cause,
           SourceRef At)
      : K(K), Why(Why), Cond(Cond), Cause(Cause), At(At) {}
  ValidityKind K;
  UnresolvedReason Why;
  Condition Cond;
  std::optional<MutationEvent> Cause;
  SourceRef At;
};

class HandleState {
public:
  HandleState(const Origin &O, const Validity &V) : O(O), V(V) {}

  const Origin &origin() const { return O; }
  ContainerId container() const { return O.Container; }
  HandleKind kind() const { return O.Kind; }
  const Position &position() const { return O.Pos; }
  const Validity &validity() const { return V; }

  HandleState withValidity(const Validity &NV) const { return HandleState(O, NV); }
  HandleState withPosition(const Position &P) const {
    Origin N = O;
    N.Pos = P;
    return HandleState(N, V);
  }

  bool operator==(const HandleState &X) const { return O == X.O && V == X.V; }
  bool operator!=(const HandleState &X) const { return !(*this == X); }

private:
  Origin O;
  Validity V;
};

/// Inserciones garantizadas sin reubicar ni rehash (D-19). nullopt = Unknown.
using Credit = std::optional<unsigned>;

enum class PolicyMode : std::uint8_t { Silent, Possibly };

enum class VerdictKind : std::uint8_t { Fine, Confirmed, Possibly };

enum class MissingGuarantee : std::uint8_t { None, ReserveBefore, SizeAtLeastTwo, ReobtainAfter };

struct UseVerdict {
  VerdictKind Kind;
  HandleCategory Category; // la del SITIO de uso
  Validity Why;            // causa: Invalidated o Unresolved
  MissingGuarantee Missing;
};

} // namespace ucsm::dominio

#endif
