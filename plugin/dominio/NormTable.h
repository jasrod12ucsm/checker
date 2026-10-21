//===- NormTable.h - La tabla normativa (generada) --------------*- C++ -*-===//
//
// Única puerta a norma/matriz.json desde C++. Los datos salen de
// generado/NormTable.inc; aquí sólo hay consultas.
//
//===----------------------------------------------------------------------===//
#ifndef UCSM_DOMINIO_NORMTABLE_H
#define UCSM_DOMINIO_NORMTABLE_H

#include "Lenguaje.h"

#include <cstddef>
#include <optional>

namespace ucsm::dominio {

struct Effect {
  EffectKind Kind;
  Condition Cond;     // Condition::None salvo en Depends
  const char *Clause; // "" en Preserves
};

constexpr bool sameEffect(const Effect &A, const Effect &B) { return A.Kind == B.Kind && A.Cond == B.Cond; }

/// Conjunto de relaciones (bitmask cerrado sobre Relation).
class RelationSet {
public:
  constexpr RelationSet() = default;
  static constexpr RelationSet of(Relation R) { return RelationSet(bit(R)); }
  static constexpr RelationSet ordered() {
    return RelationSet(bit(Relation::Before) | bit(Relation::Same) | bit(Relation::After));
  }
  constexpr RelationSet with(Relation R) const { return RelationSet(Bits | bit(R)); }
  constexpr RelationSet operator&(RelationSet O) const { return RelationSet(Bits & O.Bits); }
  constexpr bool contains(Relation R) const { return Bits & bit(R); }
  constexpr bool empty() const { return Bits == 0; }
  constexpr bool operator==(RelationSet O) const { return Bits == O.Bits; }

private:
  constexpr explicit RelationSet(unsigned B) : Bits(B) {}
  static constexpr unsigned bit(Relation R) { return 1u << static_cast<unsigned>(R); }
  unsigned Bits = 0;
};

inline constexpr Relation AllRelations[] = {Relation::Same, Relation::Before, Relation::After, Relation::Any};

/// ¿La norma tiene esta mutación?
bool isKnown(const Mutation &M);
/// Cuánto crece size(). nullopt si la mutación no está en la norma.
std::optional<Growth> growthOf(const Mutation &M);
/// El efecto de la norma. Pointer se consulta como Reference.
std::optional<Effect> effectOf(const Mutation &M, HandleCategory C, Relation R);
/// Las relaciones que la norma admite para esta mutación y categoría.
RelationSet relationsOf(const Mutation &M, HandleCategory C);

/// Para recorrer la tabla en las pruebas.
std::size_t mutationCount();
Mutation mutationAt(std::size_t I);

} // namespace ucsm::dominio

#endif
