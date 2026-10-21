//===- NormTable.cpp - Consultas sobre la tabla generada --------------------===//
#include "NormTable.h"

namespace ucsm::dominio {
namespace {

struct MutationRow {
  ContainerKind Container;
  Operation Op;
  Point At;
  Growth Grows;
};

struct RuleRow {
  Mutation M;
  HandleCategory Category;
  Relation Rel;
  EffectKind Kind;
  Condition Cond;
  const char *Clause;
};

#include "generado/NormTable.inc"

HandleCategory normCategory(HandleCategory C) {
  return C == HandleCategory::Pointer ? HandleCategory::Reference : C;
}

} // namespace

std::size_t mutationCount() { return MutationCount; }

Mutation mutationAt(std::size_t I) {
  const MutationRow &R = Mutations[I];
  return {R.Container, R.Op, R.At};
}

std::optional<Growth> growthOf(const Mutation &M) {
  for (const MutationRow &R : Mutations)
    if (Mutation{R.Container, R.Op, R.At} == M)
      return R.Grows;
  return std::nullopt;
}

bool isKnown(const Mutation &M) { return growthOf(M).has_value(); }

std::optional<Effect> effectOf(const Mutation &M, HandleCategory C, Relation Rel) {
  HandleCategory N = normCategory(C);
  for (const RuleRow &R : Rules)
    if (R.M == M && R.Category == N && R.Rel == Rel)
      return Effect{R.Kind, R.Cond, R.Clause};
  return std::nullopt;
}

RelationSet relationsOf(const Mutation &M, HandleCategory C) {
  HandleCategory N = normCategory(C);
  RelationSet S;
  for (const RuleRow &R : Rules)
    if (R.M == M && R.Category == N)
      S = S.with(R.Rel);
  return S;
}

const char *nameOf(ContainerKind K) {
  switch (K) {
  case ContainerKind::Vector: return "std::vector";
  case ContainerKind::Deque: return "std::deque";
  case ContainerKind::List: return "std::list";
  case ContainerKind::ForwardList: return "std::forward_list";
  case ContainerKind::Set: return "std::set";
  case ContainerKind::Multiset: return "std::multiset";
  case ContainerKind::Map: return "std::map";
  case ContainerKind::Multimap: return "std::multimap";
  case ContainerKind::UnorderedSet: return "std::unordered_set";
  case ContainerKind::UnorderedMap: return "std::unordered_map";
  }
  return "?";
}

const char *nameOf(Operation Op) {
  switch (Op) {
  case Operation::PushBack: return "push_back";
  case Operation::EmplaceBack: return "emplace_back";
  case Operation::PushFront: return "push_front";
  case Operation::EmplaceFront: return "emplace_front";
  case Operation::Insert: return "insert";
  case Operation::InsertAfter: return "insert_after";
  case Operation::Emplace: return "emplace";
  case Operation::Subscript: return "operator[]";
  case Operation::Erase: return "erase";
  case Operation::EraseAfter: return "erase_after";
  case Operation::PopBack: return "pop_back";
  case Operation::PopFront: return "pop_front";
  case Operation::Clear: return "clear";
  case Operation::Assign: return "assign";
  case Operation::Resize: return "resize";
  case Operation::Reserve: return "reserve";
  case Operation::ShrinkToFit: return "shrink_to_fit";
  case Operation::Rehash: return "rehash";
  case Operation::Reverse: return "reverse";
  case Operation::Sort: return "sort";
  }
  return "?";
}

const char *nameOf(HandleCategory C) {
  switch (C) {
  case HandleCategory::Iterator: return "iterador";
  case HandleCategory::Reference: return "referencia";
  case HandleCategory::Pointer: return "puntero";
  }
  return "?";
}

} // namespace ucsm::dominio
