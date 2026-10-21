//===- InvalidationChecker.cpp ----------------------------------------------===//
#include "checker/InvalidationChecker.h"

#include "acl/ClangRecognizer.h"
#include "checker/Messages.h"

#include "clang/StaticAnalyzer/Core/BugReporter/BugReporter.h"
#include "clang/StaticAnalyzer/Core/PathSensitive/ProgramStateTrait.h"

#include <string>
#include <vector>

using namespace clang;
using namespace clang::ento;
using namespace ucsm::dominio;

namespace {

/// HandleState en el ProgramState: ImmutableMap pide Profile y ==.
struct Stored {
  HandleState S;

  bool operator==(const Stored &O) const { return S == O.S; }
  void Profile(llvm::FoldingSetNodeID &ID) const {
    const Origin &O = S.origin();
    ID.AddPointer(O.Container.opaque());
    ID.AddInteger(static_cast<unsigned>(O.Kind));
    ID.AddInteger(static_cast<unsigned>(O.Pos.base()));
    ID.AddInteger(O.Pos.offset());
    ID.AddPointer(O.Pos.anchorId());
    ID.AddPointer(O.At.opaque());
    const Validity &V = S.validity();
    ID.AddInteger(static_cast<unsigned>(V.kind()));
    ID.AddInteger(static_cast<unsigned>(V.reason()));
    ID.AddInteger(static_cast<unsigned>(V.condition()));
    ID.AddPointer(V.at().opaque());
    if (const auto &E = V.cause()) {
      ID.AddPointer(E->Container.opaque());
      ID.AddInteger(static_cast<unsigned>(E->M.Container));
      ID.AddInteger(static_cast<unsigned>(E->M.Op));
      ID.AddInteger(static_cast<unsigned>(E->M.At));
      ID.AddInteger(static_cast<unsigned>(E->PointPos.base()));
      ID.AddInteger(E->PointPos.offset());
      ID.AddPointer(E->PointPos.anchorId());
      ID.AddPointer(E->At.opaque());
      ID.AddBoolean(E->RangeEnd.has_value());
      if (E->RangeEnd) {
        ID.AddInteger(static_cast<unsigned>(E->RangeEnd->base()));
        ID.AddInteger(E->RangeEnd->offset());
        ID.AddPointer(E->RangeEnd->anchorId());
      }
    }
  }
};

} // namespace

// Región del elemento ↦ estado; región del objeto iterador ↦ estado;
// región del contenedor ↦ crédito de reserve (ausente = Unknown).
REGISTER_MAP_WITH_PROGRAMSTATE(ElementMap, const MemRegion *, Stored)
REGISTER_MAP_WITH_PROGRAMSTATE(IteratorMap, const MemRegion *, Stored)
REGISTER_MAP_WITH_PROGRAMSTATE(CreditMap, const MemRegion *, unsigned)

namespace ucsm {
namespace {

const MemRegion *regionOf(ContainerId Id) { return static_cast<const MemRegion *>(Id.opaque()); }
const Stmt *stmtOf(SourceRef S) { return static_cast<const Stmt *>(S.opaque()); }

unsigned lineOf(SourceRef S, CheckerContext &C) {
  const Stmt *St = stmtOf(S);
  if (!St)
    return 0;
  return C.getSourceManager().getPresumedLineNumber(St->getBeginLoc());
}

Credit creditOf(ProgramStateRef St, const MemRegion *Container) {
  if (const unsigned *K = St->get<CreditMap>(Container))
    return *K;
  return std::nullopt;
}

ProgramStateRef setCredit(ProgramStateRef St, const MemRegion *Container, Credit K) {
  return K ? St->set<CreditMap>(Container, *K) : St->remove<CreditMap>(Container);
}

const MemRegion *returnedIterator(const CallEvent &Call) {
  if (std::optional<SVal> V = Call.getReturnValueUnderConstruction())
    if (const MemRegion *R = acl::iteratorRegion(*V))
      return R;
  return acl::iteratorRegion(Call.getReturnValue());
}

/// `m.insert(x)` / `m.emplace(…)` devuelven pair<iterator, bool>: la región
/// de su campo `first`.
const MemRegion *returnedPairFirst(const CallEvent &Call, CheckerContext &C) {
  QualType T = Call.getResultType();
  const auto *RD = T->getAsCXXRecordDecl();
  if (!RD || !RD->isInStdNamespace() || !RD->getIdentifier() || RD->getName() != "pair")
    return nullptr;
  const MemRegion *R = nullptr;
  if (std::optional<SVal> V = Call.getReturnValueUnderConstruction())
    R = V->getAsRegion();
  if (!R)
    if (auto LCV = Call.getReturnValue().getAs<nonloc::LazyCompoundVal>())
      R = LCV->getRegion();
  const auto *Super = dyn_cast_or_null<SubRegion>(R);
  if (!Super)
    return nullptr;
  for (const FieldDecl *FD : RD->fields())
    if (FD->getName() == "first")
      return C.getStoreManager().getRegionManager().getFieldRegion(FD, Super);
  return nullptr;
}

const MemRegion *returnedElement(const CallEvent &Call) {
  if (const MemRegion *R = Call.getReturnValue().getAsRegion())
    return R->getBaseRegion();
  return nullptr;
}

/// Una posición desconocida de un handle NUEVO pasa a ser un ancla fresca:
/// un elemento definido, comparable con lo que se derive de él.
Position anchored(const Position &P, const CallEvent &Call, CheckerContext &C) {
  if (P.base() != Position::Base::Unknown)
    return P;
  static int Tag;
  SVal S = C.getSValBuilder().conjureSymbolVal(Call, C.getASTContext().IntTy, C.blockCount(), &Tag);
  return Position::anchor(S.getAsSymbol());
}

/// Notas de una transición: (región del handle, texto). Se muestran sólo en
/// el informe de ese handle.
using Notes = std::vector<std::pair<const MemRegion *, std::string>>;

void transition(CheckerContext &C, ProgramStateRef St, Notes N) {
  if (N.empty()) {
    C.addTransition(St);
    return;
  }
  const NoteTag *Tag = C.getNoteTag([N = std::move(N)](PathSensitiveBugReport &BR) -> std::string {
    for (const auto &[R, Msg] : N)
      if (BR.isInteresting(R))
        return Msg;
    return "";
  });
  C.addTransition(St, Tag);
}

} // namespace

void InvalidationChecker::trace(const SourceManager &SM, const Stmt *S, StringRef What,
                                const MemRegion *R) const {
  if (!Debug)
    return;
  llvm::errs() << "[ucsm] ";
  if (S)
    llvm::errs() << SM.getPresumedLineNumber(S->getBeginLoc()) << ": ";
  llvm::errs() << What;
  if (R)
    llvm::errs() << " " << R->getString();
  llvm::errs() << "\n";
}

ProgramStateRef InvalidationChecker::use(ProgramStateRef St, const MemRegion *R, bool IsIterator,
                                         HandleCategory At, const Stmt *S, CheckerContext &C) const {
  const Stored *H = IsIterator ? St->get<IteratorMap>(R) : St->get<ElementMap>(R);
  if (!H)
    return nullptr;
  trace(C, S, "uso", R);
  UseResult U = onUse(H->S, At, Mode);
  if (U.Verdict.Kind == VerdictKind::Fine)
    return nullptr;
  St = IsIterator ? St->set<IteratorMap>(R, Stored{U.State}) : St->set<ElementMap>(R, Stored{U.State});
  ExplodedNode *N = C.generateNonFatalErrorNode(St);
  if (!N)
    return nullptr;
  unsigned Line = lineOf(U.Verdict.Why.at(), C);
  bool Sure = U.Verdict.Kind == VerdictKind::Confirmed;
  auto Report = std::make_unique<PathSensitiveBugReport>(
      Sure ? Confirmed : Possible,
      Sure ? messages::confirmed(U.Verdict, Line) : messages::possibly(U.Verdict, Line), N);
  Report->markInteresting(R);
  if (S)
    Report->addRange(S->getSourceRange());
  C.emitReport(std::move(Report));
  return St;
}

void InvalidationChecker::checkPreCall(const CallEvent &Call, CheckerContext &C) const {
  ProgramStateRef St = C.getState();
  auto Tracked = [&](const MemRegion *R) { return St->get<IteratorMap>(R) != nullptr; };

  // *it, it->, ++it, it == …, std::next(it): mover o comparar es usar.
  if (auto U = acl::iteratorUse(Call, C, Tracked)) {
    if (ProgramStateRef N = use(St, U->Iterator, true, HandleCategory::Iterator, Call.getOriginExpr(), C))
      St = N;
    return;
  }
  // c.erase(it), c.insert(it, x): el argumento se usa.
  if (acl::containerCall(Call))
    for (unsigned I = 0; I < Call.getNumArgs(); ++I)
      if (const MemRegion *R = acl::argumentIterator(Call, I, C, Tracked))
        if (ProgramStateRef N = use(St, R, true, HandleCategory::Iterator, Call.getArgExpr(I), C))
          St = N;

  // Un elemento se usa también sin cargarlo: `p->metodo()`, o al ligarlo a un
  // parámetro por referencia (`f(p->campo)`). Pasar el puntero por valor no
  // es un uso: en C++17 sólo la indirección por un puntero inválido es UB.
  if (const auto *IC = dyn_cast<CXXInstanceCall>(&Call))
    if (const MemRegion *R = IC->getCXXThisVal().getAsRegion())
      if (const auto *MC = dyn_cast_or_null<CXXMemberCallExpr>(Call.getOriginExpr()))
        if (ProgramStateRef N =
                use(St, R->getBaseRegion(), false, acl::categoryAtLoad(MC->getCallee()), MC, C))
          St = N;
  if (const auto *FD = dyn_cast_or_null<FunctionDecl>(Call.getDecl()))
    for (unsigned I = 0; I < Call.getNumArgs() && I < FD->getNumParams(); ++I) {
      if (!FD->getParamDecl(I)->getType()->isReferenceType())
        continue;
      if (const MemRegion *R = Call.getArgSVal(I).getAsRegion())
        if (ProgramStateRef N = use(St, R->getBaseRegion(), false, acl::categoryAtLoad(Call.getArgExpr(I)),
                                    Call.getArgExpr(I), C))
          St = N;
    }
}

void InvalidationChecker::checkPostCall(const CallEvent &Call, CheckerContext &C) const {
  ProgramStateRef St = C.getState();
  SourceRef Here(Call.getOriginExpr());

  // auto it2 = it;  it = c.erase(it);  (copia no trivial)
  if (auto Copy = acl::iteratorCopy(Call)) {
    if (const Stored *From = St->get<IteratorMap>(Copy->first))
      C.addTransition(St->set<IteratorMap>(Copy->second, *From));
    else if (St->get<IteratorMap>(Copy->second))
      C.addTransition(St->remove<IteratorMap>(Copy->second));
    return;
  }

  auto Tracked = [&](const MemRegion *R) { return St->get<IteratorMap>(R) != nullptr; };
  if (auto U = acl::iteratorUse(Call, C, Tracked)) {
    const Stored *It = St->get<IteratorMap>(U->Iterator);
    if (!It)
      return;
    switch (U->Op) {
    case acl::IteratorOp::Deref:
      // El elemento hereda la validez del iterador: si ya era inválido, ya se avisó.
      if (const MemRegion *E = returnedElement(Call)) {
        trace(C, Call.getOriginExpr(), "obtener elemento por *it", E);
        Origin O{It->S.container(), HandleKind::Element, It->S.position(), Here};
        transition(C, St->set<ElementMap>(E, Stored{obtain(O).withValidity(It->S.validity())}),
                   {{E, messages::derefNote()}});
      }
      return;
    case acl::IteratorOp::Increment:
    case acl::IteratorOp::Decrement:
    case acl::IteratorOp::Advance: {
      Step S = U->Delta == 0 ? Step{StepKind::UnknownStep} : Step{StepKind::Advance, U->Delta};
      HandleState Moved = move(It->S, S);
      Moved = Moved.withPosition(anchored(Moved.position(), Call, C));
      if (U->InPlace) {
        C.addTransition(St->set<IteratorMap>(U->Iterator, Stored{Moved}));
      } else if (const MemRegion *R = returnedIterator(Call)) {
        C.addTransition(St->set<IteratorMap>(R, Stored{Moved}));
      }
      return;
    }
    case acl::IteratorOp::Compare:
    case acl::IteratorOp::None: return;
    }
    return;
  }

  std::optional<acl::ContainerCall> CC = acl::containerCall(Call);
  if (!CC)
    return;
  ContainerId Box(CC->Region);

  if (std::optional<Position> P = acl::iteratorObtention(*CC, Call)) {
    if (const MemRegion *R = returnedIterator(Call)) {
      trace(C, Call.getOriginExpr(), "obtener iterador", R);
      transition(C,
                 St->set<IteratorMap>(
                     R, Stored{obtain({Box, HandleKind::IteratorObject, anchored(*P, Call, C), Here})}),
                 {{R, messages::obtainedNote(CC->Kind, CC->Method.str(), HandleKind::IteratorObject)}});
    }
    return;
  }

  Notes N;
  auto PositionOf = [&](SVal V) -> std::optional<Position> {
    if (const MemRegion *R = acl::iteratorRegion(V))
      if (const Stored *S = St->get<IteratorMap>(R))
        return S->S.position();
    return std::nullopt;
  };

  if (std::optional<acl::MutationCall> M = acl::mutation(*CC, Call, C, PositionOf)) {
    MutationEvent E{Box, M->M, M->PointPos, Here, M->RangeEnd};
    trace(C, Call.getOriginExpr(), std::string("mutación ") + nameOf(M->M.Op), CC->Region);
    Credit K = creditOf(St, CC->Region);
    auto ApplyAll = [&](auto Map, bool IsIterator) {
      for (const auto &[R, H] : Map) {
        if (H.S.container() != Box)
          continue;
        ApplyResult A = apply(E, H.S, K);
        if (A.State == H.S)
          continue;
        if (A.Noted)
          trace(C, Call.getOriginExpr(), "  invalida/no resuelve", R);
        St = IsIterator ? St->set<IteratorMap>(R, Stored{A.State}) : St->set<ElementMap>(R, Stored{A.State});
        if (A.Noted)
          N.emplace_back(R, A.State.validity().kind() == ValidityKind::Invalidated
                                ? messages::invalidatedNote(E, H.S.kind())
                                : messages::unresolvedNote(A.State.validity(), H.S.kind()));
      }
    };
    ApplyAll(St->get<IteratorMap>(), true);
    ApplyAll(St->get<ElementMap>(), false);
    St = setCredit(St, CC->Region, consume(M->M, K));
    if (M->Guarantee)
      St = setCredit(St, CC->Region, *M->Guarantee);
    if (M->ReturnsIterator) {
      if (const MemRegion *R = returnedIterator(Call))
        St = St->set<IteratorMap>(R, Stored{obtain({Box, HandleKind::IteratorObject, M->PointPos, Here})});
    } else if (const MemRegion *R = returnedPairFirst(Call, C)) {
      St = St->set<IteratorMap>(
          R, Stored{obtain({Box, HandleKind::IteratorObject, anchored(M->PointPos, Call, C), Here})});
    }
  }

  // front(), back(), c[i], data(), y también map[k] después de su mutación.
  if (std::optional<Position> P = acl::elementAccess(*CC, Call, C))
    if (const MemRegion *R = returnedElement(Call)) {
      trace(C, Call.getOriginExpr(), "obtener elemento", R);
      St = St->set<ElementMap>(R, Stored{obtain({Box, HandleKind::Element, *P, Here})});
      N.emplace_back(R, messages::obtainedNote(CC->Kind, CC->Method.str(), HandleKind::Element));
    }

  transition(C, St, std::move(N));
}

void InvalidationChecker::checkLocation(SVal Loc, bool IsLoad, const Stmt *S, CheckerContext &C) const {
  const MemRegion *R = Loc.getAsRegion();
  if (!R)
    return;
  R = R->getBaseRegion(); // h.second, h->second: subregiones del elemento
  if (ProgramStateRef N = use(C.getState(), R, false, acl::categoryAtLoad(S), S, C))
    (void)N;
}

void InvalidationChecker::checkBind(SVal Loc, SVal Val, const Stmt *S, CheckerContext &C) const {
  // Copia trivial de un iterador: auto it2 = it;  it = c.erase(it);
  const MemRegion *To = Loc.getAsRegion();
  if (!To)
    return;
  To = To->getMostDerivedObjectRegion();
  ProgramStateRef St = C.getState();
  const MemRegion *From = acl::iteratorRegion(Val);
  if (From && From != To)
    if (const Stored *H = St->get<IteratorMap>(From)) {
      C.addTransition(St->set<IteratorMap>(To, *H));
      return;
    }
  if (St->get<IteratorMap>(To) && From != To)
    C.addTransition(St->remove<IteratorMap>(To));
}

void InvalidationChecker::checkDeadSymbols(SymbolReaper &SR, CheckerContext &C) const {
  ProgramStateRef St = C.getState();
  bool Changed = false;
  for (const auto &[R, H] : St->get<ElementMap>())
    if (!SR.isLiveRegion(R)) {
      trace(C, nullptr, "muere", R);
      St = St->remove<ElementMap>(R);
      Changed = true;
    }
  for (const auto &[R, H] : St->get<IteratorMap>())
    if (!SR.isLiveRegion(R)) {
      trace(C, nullptr, "muere", R);
      St = St->remove<IteratorMap>(R);
      Changed = true;
    }
  for (const auto &[R, K] : St->get<CreditMap>())
    if (!SR.isLiveRegion(R)) {
      St = St->remove<CreditMap>(R);
      Changed = true;
    }
  if (Changed)
    C.addTransition(St);
}

ProgramStateRef InvalidationChecker::checkRegionChanges(ProgramStateRef St, const InvalidatedSymbols *,
                                                        ArrayRef<const MemRegion *> Explicits,
                                                        ArrayRef<const MemRegion *>, const LocationContext *,
                                                        const CallEvent *Call) const {
  // Sólo una llamada que no reconocemos es un escape (deteccion.md §1).
  if (!Call || acl::containerCall(*Call) || acl::iteratorCopy(*Call))
    return St;
  // El contenedor escapa si la llamada recibe el contenedor o algo que lo
  // contiene (`this` cuando el contenedor es un campo).
  SourceRef At(Call->getOriginExpr());
  auto Escapes = [&](ContainerId Box) {
    const MemRegion *C = regionOf(Box);
    for (const MemRegion *X : Explicits)
      if (C == X || C->isSubRegionOf(X) || C->isSubRegionOf(X->getBaseRegion()))
        return true;
    return false;
  };
  for (const auto &[R, H] : St->get<IteratorMap>())
    if (Escapes(H.S.container())) {
      trace(St->getStateManager().getContext().getSourceManager(), Call->getOriginExpr(), "escape (olvida)",
            R);
      std::optional<HandleState> E = escape(H.S, At);
      St = E ? St->set<IteratorMap>(R, Stored{*E}) : St->remove<IteratorMap>(R);
    }
  for (const auto &[R, H] : St->get<ElementMap>())
    if (Escapes(H.S.container())) {
      trace(St->getStateManager().getContext().getSourceManager(), Call->getOriginExpr(), "escape (olvida)",
            R);
      std::optional<HandleState> E = escape(H.S, At);
      St = E ? St->set<ElementMap>(R, Stored{*E}) : St->remove<ElementMap>(R);
    }
  for (const auto &[R, K] : St->get<CreditMap>())
    if (Escapes(ContainerId(R)))
      St = St->remove<CreditMap>(R);
  return St;
}

} // namespace ucsm
