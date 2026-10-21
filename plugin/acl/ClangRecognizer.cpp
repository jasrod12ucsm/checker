//===- ClangRecognizer.cpp --------------------------------------------------===//
#include "acl/ClangRecognizer.h"

#include "clang/AST/DeclCXX.h"
#include "clang/AST/ExprCXX.h"
#include "llvm/ADT/StringSwitch.h"
#include <limits>

using namespace clang;
using namespace clang::ento;
using namespace ucsm::dominio;

namespace ucsm::acl {

const MemRegion *iteratorRegion(SVal V) {
  if (auto LCV = V.getAs<nonloc::LazyCompoundVal>())
    return LCV->getRegion()->getMostDerivedObjectRegion();
  if (const MemRegion *R = V.getAsRegion())
    return R->getMostDerivedObjectRegion();
  return nullptr;
}

namespace {

std::optional<ContainerKind> containerOf(const CXXRecordDecl *RD) {
  if (!RD || !RD->isInStdNamespace() || !RD->getIdentifier())
    return std::nullopt;
  return llvm::StringSwitch<std::optional<ContainerKind>>(RD->getName())
      .Case("vector", ContainerKind::Vector)
      .Case("deque", ContainerKind::Deque)
      .Case("list", ContainerKind::List)
      .Case("forward_list", ContainerKind::ForwardList)
      .Case("set", ContainerKind::Set)
      .Case("multiset", ContainerKind::Multiset)
      .Case("map", ContainerKind::Map)
      .Case("multimap", ContainerKind::Multimap)
      .Case("unordered_set", ContainerKind::UnorderedSet)
      .Case("unordered_map", ContainerKind::UnorderedMap)
      .Default(std::nullopt);
}

bool isSequence(ContainerKind K) {
  return K == ContainerKind::Vector || K == ContainerKind::Deque || K == ContainerKind::List ||
         K == ContainerKind::ForwardList;
}

const Expr *strip(const Expr *E) {
  while (E) {
    E = E->IgnoreParenImpCasts();
    if (const auto *M = dyn_cast<MaterializeTemporaryExpr>(E))
      E = M->getSubExpr();
    else if (const auto *B = dyn_cast<CXXBindTemporaryExpr>(E))
      E = B->getSubExpr();
    else if (const auto *C = dyn_cast<CXXConstructExpr>(E); C && C->getNumArgs() == 1)
      E = C->getArg(0); // conversión iterator → const_iterator
    else if (const auto *F = dyn_cast<CXXFunctionalCastExpr>(E))
      E = F->getSubExpr();
    else
      return E;
  }
  return E;
}

/// Si E es `obj.metodo()` con metodo ∈ Names, el nombre.
std::optional<StringRef> memberCallName(const Expr *E, std::initializer_list<StringRef> Names) {
  const auto *MC = dyn_cast_or_null<CXXMemberCallExpr>(strip(E));
  if (!MC || !MC->getMethodDecl() || !MC->getMethodDecl()->getIdentifier())
    return std::nullopt;
  StringRef N = MC->getMethodDecl()->getName();
  for (StringRef W : Names)
    if (N == W)
      return N;
  return std::nullopt;
}

std::optional<llvm::APSInt> constantOf(const Expr *E, CheckerContext &C) {
  if (!E)
    return std::nullopt;
  if (std::optional<llvm::APSInt> V = E->getIntegerConstantExpr(C.getASTContext()))
    return V;
  if (const llvm::APSInt *V = C.getSValBuilder().getKnownValue(C.getState(), C.getSVal(E)))
    return *V;
  return std::nullopt;
}

/// La constante, si cabe en un int. Una constante enorme (size_t(-1) en un
/// camino, un índice de 64 bits) no es una distancia que el dominio sepa usar:
/// getExtValue() aborta si no cabe en int64 (RocksDB, compaction_picker.cc).
std::optional<int> smallConstantOf(const Expr *E, CheckerContext &C) {
  std::optional<llvm::APSInt> V = constantOf(E, C);
  if (!V)
    return std::nullopt;
  llvm::APSInt Min = llvm::APSInt::get(std::numeric_limits<int>::min());
  llvm::APSInt Max = llvm::APSInt::get(std::numeric_limits<int>::max());
  if (llvm::APSInt::compareValues(*V, Min) < 0 || llvm::APSInt::compareValues(*V, Max) > 0)
    return std::nullopt;
  return static_cast<int>(V->getExtValue());
}

/// `c.size() + k` (o `k + c.size()`) → k.
std::optional<unsigned> sizePlus(const Expr *E, CheckerContext &C) {
  const auto *B = dyn_cast_or_null<BinaryOperator>(strip(E));
  if (!B || B->getOpcode() != BO_Add)
    return std::nullopt;
  const Expr *L = B->getLHS(), *R = B->getRHS();
  if (!memberCallName(L, {"size"}))
    std::swap(L, R);
  if (!memberCallName(L, {"size"}))
    return std::nullopt;
  if (auto K = smallConstantOf(R, C); K && *K >= 0)
    return static_cast<unsigned>(*K);
  return std::nullopt;
}

/// Si E (sin conversiones) nombra una variable, su región.
const MemRegion *variableRegion(const Expr *E, CheckerContext &C) {
  if (const auto *DR = dyn_cast_or_null<DeclRefExpr>(strip(E)))
    if (const auto *VD = dyn_cast<VarDecl>(DR->getDecl()))
      return C.getState()->getLValue(VD, C.getLocationContext()).getAsRegion();
  return nullptr;
}

/// Posición del iterador que se pasa como argumento I de insert/erase.
Position positionOfArg(const CallEvent &Call, unsigned I, CheckerContext &C, PositionOf Pos) {
  const Expr *E = Call.getArgExpr(I);
  if (memberCallName(E, {"begin", "cbegin"}))
    return Position::first(0);
  if (memberCallName(E, {"end", "cend"}))
    return Position::pastEnd();
  // c.begin() + k
  const Expr *S = strip(E);
  const Expr *Base = nullptr, *Off = nullptr;
  if (const auto *Op = dyn_cast<CXXOperatorCallExpr>(S);
      Op && Op->getOperator() == OO_Plus && Op->getNumArgs() == 2) {
    Base = Op->getArg(0);
    Off = Op->getArg(1);
  } else if (const auto *B = dyn_cast<BinaryOperator>(S); B && B->getOpcode() == BO_Add) {
    Base = B->getLHS();
    Off = B->getRHS();
  }
  if (Base && memberCallName(Base, {"begin", "cbegin"}))
    if (auto K = smallConstantOf(Off, C))
      return Position::first(*K);
  // La copia que recibe el parámetro (también la convertida a const_iterator),
  // el valor del argumento, o la variable que nombra.
  const MemRegion *Candidates[] = {Call.getParameterLocation(I, C.blockCount()),
                                   iteratorRegion(Call.getArgSVal(I)), variableRegion(E, C)};
  for (const MemRegion *R : Candidates)
    if (R)
      if (std::optional<Position> P = Pos(loc::MemRegionVal(R->getMostDerivedObjectRegion())))
        return *P;
  return Position::unknown();
}

/// El punto de una operación posicional, según dónde cae.
Point pointOf(const Position &P, bool Erasing) {
  switch (P.base()) {
  case Position::Base::First: return P.offset() == 0 ? Point::Front : Point::Interior;
  case Position::Base::PastEnd: return Point::Back;
  case Position::Base::Last: return (Erasing && P.offset() == 0) ? Point::Back : Point::Interior;
  case Position::Base::Anchor:
  case Position::Base::Unknown: return Point::Interior;
  }
  return Point::Interior;
}

bool paramIsIterator(const CallEvent &Call, unsigned I) {
  const auto *FD = dyn_cast_or_null<FunctionDecl>(Call.getDecl());
  if (!FD || FD->getNumParams() <= I)
    return false;
  QualType T = FD->getParamDecl(I)->getType().getNonReferenceType().getUnqualifiedType();
  const auto *RD = T->getAsCXXRecordDecl();
  if (!RD || !RD->getIdentifier())
    return false;
  StringRef N = RD->getName();
  return N.contains("iterator") || N.contains("Iterator");
}

bool firstParamIsIterator(const CallEvent &Call) { return paramIsIterator(Call, 0); }

/// erase(first, last) y erase_after(pos, last): dos iteradores.
bool isRange(const CallEvent &Call) {
  return Call.getNumArgs() == 2 && paramIsIterator(Call, 0) && paramIsIterator(Call, 1);
}

} // namespace

const MemRegion *argumentIterator(const CallEvent &Call, unsigned I, CheckerContext &C,
                                  llvm::function_ref<bool(const MemRegion *)> IsTracked) {
  const MemRegion *Candidates[] = {Call.getParameterLocation(I, C.blockCount()),
                                   iteratorRegion(Call.getArgSVal(I)), variableRegion(Call.getArgExpr(I), C)};
  for (const MemRegion *R : Candidates)
    if (R && IsTracked(R->getMostDerivedObjectRegion()))
      return R->getMostDerivedObjectRegion();
  return nullptr;
}

std::optional<ContainerCall> containerCall(const CallEvent &Call) {
  const auto *IC = dyn_cast<CXXInstanceCall>(&Call);
  if (!IC)
    return std::nullopt;
  const auto *MD = dyn_cast_or_null<CXXMethodDecl>(IC->getDecl());
  if (!MD)
    return std::nullopt;
  std::optional<ContainerKind> K = containerOf(MD->getParent());
  if (!K)
    return std::nullopt;
  const MemRegion *R = IC->getCXXThisVal().getAsRegion();
  if (!R)
    return std::nullopt;
  StringRef Name;
  if (MD->isOverloadedOperator())
    Name = MD->getOverloadedOperator() == OO_Subscript ? "operator[]" : "operator";
  else if (MD->getIdentifier())
    Name = MD->getName();
  return ContainerCall{R->getMostDerivedObjectRegion(), *K, Name};
}

std::optional<Position> iteratorObtention(const ContainerCall &CC, const CallEvent &Call) {
  if (CC.Method == "begin" || CC.Method == "cbegin")
    return Position::first(0);
  if (CC.Method == "find" || CC.Method == "lower_bound" || CC.Method == "upper_bound")
    return Position::unknown();
  return std::nullopt; // end() queda fuera del alcance (norma.md §7)
}

std::optional<Position> elementAccess(const ContainerCall &CC, const CallEvent &Call, CheckerContext &C) {
  if (CC.Method == "front" || CC.Method == "data")
    return Position::first(0);
  if (CC.Method == "back")
    return Position::last(0);
  if (CC.Method == "operator[]" || CC.Method == "at") {
    if (!isSequence(CC.Kind) && CC.Kind != ContainerKind::Vector)
      return Position::unknown(); // map[k]: elemento por clave
    if (Call.getNumArgs() == 1)
      if (auto K = smallConstantOf(Call.getArgExpr(0), C))
        return Position::first(*K);
    return Position::unknown();
  }
  return std::nullopt;
}

std::optional<MutationCall> mutation(const ContainerCall &CC, const CallEvent &Call, CheckerContext &C,
                                     PositionOf Pos) {
  ContainerKind K = CC.Kind;
  StringRef N = CC.Method;
  auto Make = [&](Operation Op, Point At, Position P, bool Ret = false,
                  std::optional<unsigned> G = std::nullopt,
                  std::optional<Position> End = std::nullopt) -> std::optional<MutationCall> {
    Mutation M{K, Op, At};
    if (!isKnown(M))
      return std::nullopt;
    return MutationCall{M, P, G, Ret, End};
  };
  auto Arg = [&](unsigned I) { return positionOfArg(Call, I, C, Pos); };

  if (N == "push_back")
    return Make(Operation::PushBack, Point::Back, Position::pastEnd());
  if (N == "emplace_back")
    return Make(Operation::EmplaceBack, Point::Back, Position::pastEnd());
  if (N == "push_front")
    return Make(Operation::PushFront, Point::Front, Position::first(0));
  if (N == "emplace_front")
    return Make(Operation::EmplaceFront, Point::Front, Position::first(0));
  if (N == "pop_back")
    return Make(Operation::PopBack, Point::Back, Position::last(0));
  if (N == "pop_front")
    return Make(Operation::PopFront, Point::Front, Position::first(0));
  if (N == "clear")
    return Make(Operation::Clear, Point::Whole, Position::unknown());
  if (N == "assign")
    return Make(Operation::Assign, Point::Whole, Position::unknown());
  if (N == "shrink_to_fit")
    return Make(Operation::ShrinkToFit, Point::Whole, Position::unknown());
  if (N == "rehash")
    return Make(Operation::Rehash, Point::Whole, Position::unknown());
  if (N == "reverse")
    return Make(Operation::Reverse, Point::Whole, Position::unknown());
  if (N == "sort")
    return Make(Operation::Sort, Point::Whole, Position::unknown());
  if (N == "reserve" && Call.getNumArgs() == 1)
    return Make(Operation::Reserve, Point::Whole, Position::unknown(), false,
                sizePlus(Call.getArgExpr(0), C));
  if (N == "resize" && Call.getNumArgs() >= 1) {
    bool Grows = sizePlus(Call.getArgExpr(0), C).has_value();
    return Make(Operation::Resize, Point::Back, Grows ? Position::pastEnd() : Position::unknown());
  }
  if (N == "operator[]" && (K == ContainerKind::Map || K == ContainerKind::UnorderedMap))
    return Make(Operation::Subscript, Point::ByKey, Position::unknown());

  bool Positional = Call.getNumArgs() >= 1 && firstParamIsIterator(Call);
  if (N == "insert" || N == "emplace" || N == "emplace_hint") {
    Operation Op = N == "insert" ? Operation::Insert : Operation::Emplace;
    if (!isSequence(K))
      return Make(Op, Point::ByKey, Position::unknown());
    if (!Positional)
      return std::nullopt;
    Position P = Arg(0);
    return Make(Op, pointOf(P, false), P, /*Ret=*/true);
  }
  if (N == "erase") {
    if (!Positional)
      return Make(Operation::Erase, Point::ByKey, Position::unknown());
    Position P = Arg(0);
    Point At = pointOf(P, true);
    std::optional<Position> End;
    if (isRange(Call)) {
      // [first, last): la norma se lee en el punto de first, y cada handle se
      // relaciona con el rango entero (relateRange). Un rango que llega a
      // end() en un deque borra el último elemento: es el punto Back.
      End = Arg(1);
      if (K == ContainerKind::Deque && End->base() == Position::Base::PastEnd && At == Point::Interior)
        At = Point::Back;
    }
    if (!isSequence(K) && At == Point::Back)
      At = Point::Interior;
    return Make(Operation::Erase, At, P, /*Ret=*/true, std::nullopt, End);
  }
  if (N == "insert_after" || N == "erase_after") {
    Operation Op = N == "insert_after" ? Operation::InsertAfter : Operation::EraseAfter;
    std::optional<Position> End;
    if (Op == Operation::EraseAfter && isRange(Call))
      End = Arg(1);
    if (memberCallName(Call.getArgExpr(0), {"before_begin", "cbefore_begin"}))
      return Make(Op, Point::Front, Position::first(0), true, std::nullopt, End);
    // Actúa DESPUÉS del iterador dado; erase_after(pos, last) borra (pos, last).
    Position P = Arg(0);
    return Make(Op, Point::Interior, P.advance(+1), true, std::nullopt, End);
  }
  return std::nullopt;
}

std::optional<IteratorUse> iteratorUse(const CallEvent &Call, CheckerContext &C,
                                       llvm::function_ref<bool(const MemRegion *)> IsTracked) {
  const auto *FD = dyn_cast_or_null<FunctionDecl>(Call.getDecl());
  if (!FD)
    return std::nullopt;

  // std::next / std::prev / std::advance(it, n)
  if (FD->isInStdNamespace() && FD->getIdentifier() && Call.getNumArgs() >= 1) {
    StringRef N = FD->getName();
    if (N == "next" || N == "prev" || N == "advance") {
      const MemRegion *It = iteratorRegion(Call.getArgSVal(0));
      if (!It || !IsTracked(It))
        return std::nullopt;
      int D = 1;
      if (Call.getNumArgs() >= 2) {
        D = smallConstantOf(Call.getArgExpr(1), C).value_or(0);
      }
      return IteratorUse{IteratorOp::Advance, It, N == "prev" ? -D : D, N == "advance"};
    }
  }

  if (!FD->isOverloadedOperator())
    return std::nullopt;
  OverloadedOperatorKind OO = FD->getOverloadedOperator();

  // El iterador puede ser `this` (miembro) o el primer argumento (libre).
  const MemRegion *It = nullptr;
  unsigned FirstArg = 0;
  if (const auto *IC = dyn_cast<CXXInstanceCall>(&Call)) {
    It = iteratorRegion(IC->getCXXThisVal());
  } else if (Call.getNumArgs() >= 1) {
    It = iteratorRegion(Call.getArgSVal(0));
    FirstArg = 1;
  }

  switch (OO) {
  case OO_EqualEqual:
  case OO_ExclaimEqual:
  case OO_Less:
  case OO_Greater:
  case OO_LessEqual:
  case OO_GreaterEqual:
  case OO_Spaceship: {
    if (It && IsTracked(It))
      return IteratorUse{IteratorOp::Compare, It, 0, false};
    for (unsigned I = FirstArg; I < Call.getNumArgs(); ++I)
      if (const MemRegion *R = iteratorRegion(Call.getArgSVal(I)); R && IsTracked(R))
        return IteratorUse{IteratorOp::Compare, R, 0, false};
    return std::nullopt;
  }
  default: break;
  }

  if (!It || !IsTracked(It))
    return std::nullopt;
  switch (OO) {
  case OO_Star:
    if (Call.getNumArgs() == FirstArg) // unario
      return IteratorUse{IteratorOp::Deref, It, 0, false};
    return std::nullopt;
  case OO_Arrow:
  case OO_Subscript: return IteratorUse{IteratorOp::Deref, It, 0, false};
  case OO_PlusPlus: return IteratorUse{IteratorOp::Increment, It, 1, true};
  case OO_MinusMinus: return IteratorUse{IteratorOp::Decrement, It, -1, true};
  case OO_PlusEqual:
  case OO_MinusEqual:
  case OO_Plus:
  case OO_Minus: {
    int D = 0;
    if (Call.getNumArgs() > FirstArg)
      D = smallConstantOf(Call.getArgExpr(FirstArg), C).value_or(0);
    if (OO == OO_MinusEqual || OO == OO_Minus)
      D = -D;
    return IteratorUse{IteratorOp::Advance, It, D, OO == OO_PlusEqual || OO == OO_MinusEqual};
  }
  default: return std::nullopt;
  }
}

std::optional<std::pair<const MemRegion *, const MemRegion *>> iteratorCopy(const CallEvent &Call) {
  if (const auto *Ctor = dyn_cast<CXXConstructorCall>(&Call)) {
    const auto *CD = dyn_cast_or_null<CXXConstructorDecl>(Ctor->getDecl());
    if (!CD || !(CD->isCopyOrMoveConstructor() || CD->isConvertingConstructor(false)) ||
        Call.getNumArgs() != 1)
      return std::nullopt;
    const MemRegion *From = iteratorRegion(Call.getArgSVal(0));
    const MemRegion *To = iteratorRegion(Ctor->getCXXThisVal());
    if (From && To)
      return std::make_pair(From, To);
    return std::nullopt;
  }
  if (const auto *Op = dyn_cast<CXXMemberOperatorCall>(&Call)) {
    const auto *MD = dyn_cast_or_null<CXXMethodDecl>(Op->getDecl());
    if (!MD || (!MD->isCopyAssignmentOperator() && !MD->isMoveAssignmentOperator()))
      return std::nullopt;
    const MemRegion *From = iteratorRegion(Call.getArgSVal(0));
    const MemRegion *To = iteratorRegion(Op->getCXXThisVal());
    if (From && To)
      return std::make_pair(From, To);
  }
  return std::nullopt;
}

HandleCategory categoryAtLoad(const Stmt *S) {
  const auto *E = dyn_cast_or_null<Expr>(S);
  if (!E)
    return HandleCategory::Reference;
  E = E->IgnoreParenImpCasts();
  if (const auto *U = dyn_cast<UnaryOperator>(E); U && U->getOpcode() == UO_Deref)
    return HandleCategory::Pointer;
  if (const auto *M = dyn_cast<MemberExpr>(E)) {
    if (M->isArrow())
      return HandleCategory::Pointer;
    return categoryAtLoad(M->getBase()); // h.second → la de h
  }
  if (isa<ArraySubscriptExpr>(E))
    return HandleCategory::Pointer;
  return HandleCategory::Reference;
}

} // namespace ucsm::acl
