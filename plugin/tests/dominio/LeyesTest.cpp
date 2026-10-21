//===- LeyesTest.cpp - Una prueba por ley (norma.md §5, deteccion.md §5) ----===//
//
// Sin Clang. Los dominios son pequeños: se recorren enteros en lugar de
// muestrearlos.
//
//===----------------------------------------------------------------------===//
#include "Decisions.h"
#include "NormTable.h"

#include <gtest/gtest.h>

#include <vector>

using namespace ucsm::dominio;

namespace {

const HandleCategory Cats[] = {HandleCategory::Iterator, HandleCategory::Reference, HandleCategory::Pointer};
const HandleKind Kinds[] = {HandleKind::IteratorObject, HandleKind::Element};

std::vector<Position> positions() {
  return {Position::first(0), Position::first(1),  Position::first(3), Position::last(0),
          Position::last(2),  Position::pastEnd(), Position::unknown()};
}
std::vector<Credit> credits() { return {std::nullopt, 0u, 1u, 5u}; }

int order(EffectKind K) { return static_cast<int>(K); }

ContainerId C1(reinterpret_cast<const void *>(0x10));
SourceRef S1(reinterpret_cast<const void *>(0x20));
SourceRef S2(reinterpret_cast<const void *>(0x30));

HandleState handle(HandleKind K, Position P) { return obtain({C1, K, P, S1}); }
MutationEvent event(Mutation M, Position P) { return {C1, M, P, S2}; }

/// Estados iniciales de todas las clases de la cadena.
std::vector<HandleState> states(HandleKind K, Position P, Mutation Other) {
  HandleState H = handle(K, P);
  MutationEvent E = event(Other, Position::unknown());
  return {H,
          H.withValidity(Validity::dependsOn(Condition::CapacityReached, E)),
          H.withValidity(Validity::relationUnknown(E)),
          H.withValidity(Validity::dependsOn(Condition::CapacityReached, E).diagnosed()),
          H.withValidity(Validity::invalidated(E)),
          H.withValidity(Validity::invalidated(E).diagnosed())};
}

template <class F> void forAllMutations(F Fn) {
  for (std::size_t I = 0; I < mutationCount(); ++I)
    Fn(mutationAt(I));
}

} // namespace

// ── Norma ──────────────────────────────────────────────────────────────────

TEST(Norma, ReferenciaYPunteroSiguenLaMismaRegla) {
  forAllMutations([](Mutation M) {
    for (Relation R : AllRelations) {
      auto A = effectOf(M, HandleCategory::Reference, R);
      auto B = effectOf(M, HandleCategory::Pointer, R);
      ASSERT_EQ(A.has_value(), B.has_value());
      if (A)
        EXPECT_TRUE(sameEffect(*A, *B));
    }
  });
}

TEST(Norma, IteradorNuncaMejorQueReferencia) {
  forAllMutations([](Mutation M) {
    for (Relation R : AllRelations) {
      auto It = effectOf(M, HandleCategory::Iterator, R);
      auto Ref = effectOf(M, HandleCategory::Reference, R);
      if (It && Ref)
        EXPECT_GE(order(It->Kind), order(Ref->Kind)) << nameOf(M.Container) << "::" << nameOf(M.Op);
    }
  });
}

TEST(Norma, LaTablaEsTotal) {
  forAllMutations([](Mutation M) {
    EXPECT_TRUE(growthOf(M).has_value());
    for (HandleCategory C : Cats) {
      RelationSet S = relationsOf(M, C);
      EXPECT_FALSE(S.empty());
      for (Relation R : AllRelations)
        EXPECT_EQ(S.contains(R), effectOf(M, C, R).has_value());
    }
  });
}

TEST(Norma, InvalidarODependerCitaSuClausula) {
  forAllMutations([](Mutation M) {
    for (HandleCategory C : Cats)
      for (Relation R : AllRelations)
        if (auto E = effectOf(M, C, R); E && E->Kind != EffectKind::Preserves)
          EXPECT_STRNE(E->Clause, "");
  });
}

// ── Posiciones ────────────────────────────────────────────────────────────

TEST(Posicion, LaMismaAnclaSeCompara) {
  int A = 0;
  EXPECT_EQ(relate(Position::anchor(&A, 1), Position::anchor(&A, 0)), RelationSet::of(Relation::After));
  EXPECT_EQ(relate(Position::anchor(&A, 0), Position::anchor(&A, 0)), RelationSet::of(Relation::Same));
  EXPECT_EQ(relate(Position::anchor(&A, -1), Position::anchor(&A, 0)), RelationSet::of(Relation::Before));
}

TEST(Posicion, AnclasDistintasNoSeComparan) {
  int A = 0, B = 0;
  EXPECT_EQ(relate(Position::anchor(&A, 0), Position::anchor(&B, 0)), RelationSet::ordered());
  EXPECT_EQ(relate(Position::anchor(&A, 0), Position::first(0)), RelationSet::ordered());
}

TEST(Posicion, TransportarConservaLaDistanciaEntreHandlesDeLaMismaAncla) {
  int A = 0;
  Mutation Erase{ContainerKind::List, Operation::Erase, Point::Interior};
  Position P0 = Position::anchor(&A, 0); // el punto
  Position H1 = Position::anchor(&A, 1), H2 = Position::anchor(&A, 2);
  Position T1 = transport(Erase, Growth::Shrinks, Relation::After, H1);
  Position T2 = transport(Erase, Growth::Shrinks, Relation::After, H2);
  EXPECT_EQ(relate(T2, T1), relate(H2, H1));
  EXPECT_EQ(relate(Position::anchor(&A, -1), P0), RelationSet::of(Relation::Before));
}

TEST(Posicion, ElRangoEsSemiabierto) {
  Position F0 = Position::first(0), F2 = Position::first(2);
  EXPECT_EQ(relateRange(Position::first(1), F0, F2), RelationSet::of(Relation::Same));
  EXPECT_EQ(relateRange(F0, F0, F2), RelationSet::of(Relation::Same));
  EXPECT_EQ(relateRange(F2, F0, F2), RelationSet::of(Relation::After)); // last no se borra
  EXPECT_EQ(relateRange(Position::first(1), F2, Position::pastEnd()), RelationSet::of(Relation::Before));
}

TEST(Posicion, UnRangoVacioNoBorraNada) {
  // erase(c.begin(), it) con it == begin() (RocksDB, range_tombstone_fragmenter.cc).
  Position F0 = Position::first(0);
  EXPECT_FALSE(relateRange(F0, F0, F0).contains(Relation::Same));
}

TEST(Posicion, ElFinDelRangoProtegeAunConElPrincipioDesconocido) {
  int A = 0;
  Position It = Position::anchor(&A, 0);
  RelationSet S = relateRange(It, Position::unknown(), It);
  EXPECT_FALSE(S.contains(Relation::Same));
  EXPECT_TRUE(S.contains(Relation::After));
}

TEST(Posicion, TransportarUnRangoCorreLaDistancia) {
  Mutation Erase{ContainerKind::List, Operation::Erase, Point::Front};
  EXPECT_EQ(distance(Position::first(0), Position::first(3)), 3);
  EXPECT_EQ(transport(Erase, Growth::Shrinks, Relation::After, Position::first(5), 3), Position::first(2));
  EXPECT_EQ(transport(Erase, Growth::Shrinks, Relation::After, Position::first(5), std::nullopt),
            Position::unknown());
}

TEST(Deteccion, EraseDeRangoEnSetPreservaElFin) {
  Mutation M{ContainerKind::Set, Operation::Erase, Point::Front};
  HandleState H = obtain({C1, HandleKind::IteratorObject, Position::first(2), S1});
  MutationEvent E{C1, M, Position::first(0), S2, Position::first(2)};
  EXPECT_EQ(apply(E, H, std::nullopt).State.validity().kind(), ValidityKind::Valid);
  HandleState Dentro = obtain({C1, HandleKind::IteratorObject, Position::first(1), S1});
  EXPECT_EQ(apply(E, Dentro, std::nullopt).State.validity().kind(), ValidityKind::Invalidated);
}

TEST(Deteccion, EraseDeRangoEnVectorInvalidaElFin) {
  // [vector.modifiers]: invalida en el punto del borrado y después, incluido last.
  Mutation M{ContainerKind::Vector, Operation::Erase, Point::Front};
  HandleState H = obtain({C1, HandleKind::IteratorObject, Position::first(2), S1});
  MutationEvent E{C1, M, Position::first(0), S2, Position::first(2)};
  EXPECT_EQ(apply(E, H, std::nullopt).State.validity().kind(), ValidityKind::Invalidated);
}

// ── Detección: obtener ─────────────────────────────────────────────────────

TEST(Deteccion, ObtenerDaUnHandleValido) {
  for (HandleKind K : Kinds)
    for (Position P : positions())
      EXPECT_EQ(handle(K, P).validity().kind(), ValidityKind::Valid);
}

// ── Detección: aplicar ─────────────────────────────────────────────────────

TEST(Deteccion, InvalidoEsAbsorbente) {
  forAllMutations([](Mutation M) {
    for (HandleKind K : Kinds)
      for (Position P : positions())
        for (const HandleState &H : states(K, P, M))
          if (H.validity().kind() >= ValidityKind::Invalidated)
            for (Credit C : credits()) {
              ApplyResult R = apply(event(M, Position::first(0)), H, C);
              EXPECT_EQ(R.State, H);
              EXPECT_FALSE(R.Noted);
            }
  });
}

TEST(Deteccion, AplicarNuncaMejoraLaValidez) {
  forAllMutations([](Mutation M) {
    for (HandleKind K : Kinds)
      for (Position P : positions())
        for (Position Pt : positions())
          for (const HandleState &H : states(K, P, M))
            for (Credit C : credits())
              EXPECT_GE(apply(event(M, Pt), H, C).State.validity().kind(), H.validity().kind());
  });
}

TEST(Deteccion, AplicarEsIdempotenteEnLaValidez) {
  forAllMutations([](Mutation M) {
    for (HandleKind K : Kinds)
      for (Position P : positions())
        for (Position Pt : positions())
          for (Credit C : credits()) {
            HandleState H = handle(K, P);
            HandleState Once = apply(event(M, Pt), H, C).State;
            HandleState Twice = apply(event(M, Pt), Once, C).State;
            // Valid → Valid y Unresolved → Unresolved: repetir no sube de clase
            // salvo que la posición transportada cambie la relación.
            if (Once.validity().kind() != ValidityKind::Valid)
              EXPECT_EQ(Twice.validity().kind(), Once.validity().kind());
          }
  });
}

TEST(Deteccion, PreservarNoCambiaLaValidez) {
  Mutation Sort{ContainerKind::List, Operation::Sort, Point::Whole};
  for (HandleKind K : Kinds)
    for (const HandleState &H : states(K, Position::first(0), Sort))
      EXPECT_EQ(apply(event(Sort, Position::unknown()), H, std::nullopt).State.validity(), H.validity());
}

TEST(Deteccion, PreservarTransportaLaPosicion) {
  Mutation PushFront{ContainerKind::List, Operation::PushFront, Point::Front};
  HandleState H = handle(HandleKind::Element, Position::first(0));
  EXPECT_EQ(apply(event(PushFront, Position::first(0)), H, std::nullopt).State.position(),
            Position::first(1));
  Mutation EraseFront{ContainerKind::List, Operation::Erase, Point::Front};
  HandleState H2 = handle(HandleKind::Element, Position::first(2));
  EXPECT_EQ(apply(event(EraseFront, Position::first(0)), H2, std::nullopt).State.position(),
            Position::first(1));
}

TEST(Deteccion, LaCausaOriginalSeConserva) {
  Mutation Clear{ContainerKind::Vector, Operation::Clear, Point::Whole};
  Mutation Erase{ContainerKind::Vector, Operation::Erase, Point::Front};
  HandleState H = handle(HandleKind::Element, Position::first(0));
  HandleState A = apply(event(Erase, Position::first(0)), H, std::nullopt).State;
  HandleState B = apply(event(Clear, Position::unknown()), A, std::nullopt).State;
  ASSERT_TRUE(B.validity().cause().has_value());
  EXPECT_EQ(B.validity().cause()->M, Erase);
}

// ── Detección: garantías ───────────────────────────────────────────────────

TEST(Deteccion, SinGarantiaDependerEsPosible) {
  Mutation PushBack{ContainerKind::Vector, Operation::PushBack, Point::Back};
  for (Credit C : {Credit(std::nullopt), Credit(0u)}) {
    ApplyResult R =
        apply(event(PushBack, Position::pastEnd()), handle(HandleKind::Element, Position::first(0)), C);
    EXPECT_EQ(R.State.validity().kind(), ValidityKind::Unresolved);
    EXPECT_EQ(R.State.validity().reason(), UnresolvedReason::DependsOnState);
  }
}

TEST(Deteccion, ConGarantiaDependerEsPreservar) {
  Mutation PushBack{ContainerKind::Vector, Operation::PushBack, Point::Back};
  Mutation Insert{ContainerKind::UnorderedSet, Operation::Insert, Point::ByKey};
  EXPECT_EQ(apply(event(PushBack, Position::pastEnd()), handle(HandleKind::Element, Position::first(0)), 1u)
                .State.validity()
                .kind(),
            ValidityKind::Valid);
  EXPECT_EQ(
      apply(event(Insert, Position::unknown()), handle(HandleKind::IteratorObject, Position::first(0)), 3u)
          .State.validity()
          .kind(),
      ValidityKind::Valid);
}

TEST(Deteccion, LaGarantiaNoCubreLoQueNoSeCuenta) {
  // resize(n) crece una cantidad que no se cuenta: el crédito no lo cubre.
  Mutation Resize{ContainerKind::Vector, Operation::Resize, Point::Back};
  EXPECT_EQ(answer(Condition::CapacityReached, *growthOf(Resize), 100u), SolverAnswer::Both);
}

TEST(Deteccion, UnaInsercionGastaUnCredito) {
  Mutation PushBack{ContainerKind::Vector, Operation::PushBack, Point::Back};
  EXPECT_EQ(consume(PushBack, 2u), Credit(1u));
  EXPECT_EQ(consume(PushBack, 1u), Credit(0u));
  EXPECT_EQ(consume(PushBack, 0u), Credit(0u));
  EXPECT_EQ(consume(PushBack, std::nullopt), Credit(std::nullopt));
}

TEST(Deteccion, LoQueNoSeCuentaBorraElCredito) {
  forAllMutations([](Mutation M) {
    Growth G = *growthOf(M);
    if (G == Growth::Unknown || G == Growth::Reset)
      EXPECT_EQ(consume(M, 5u), Credit(std::nullopt)) << nameOf(M.Container) << "::" << nameOf(M.Op);
  });
}

TEST(Deteccion, LoQueReduceElTamanoNoGasta) {
  forAllMutations([](Mutation M) {
    if (*growthOf(M) == Growth::Shrinks)
      EXPECT_EQ(consume(M, 5u), Credit(5u));
  });
}

TEST(Deteccion, ShrinkToFitNuncaSeGarantiza) {
  Mutation S{ContainerKind::Vector, Operation::ShrinkToFit, Point::Whole};
  for (Credit C : credits())
    EXPECT_EQ(apply(event(S, Position::unknown()), handle(HandleKind::Element, Position::first(0)), C)
                  .State.validity()
                  .kind(),
              ValidityKind::Unresolved);
}

// ── Detección: usar ────────────────────────────────────────────────────────

TEST(Deteccion, LoValidoNoSeReporta) {
  for (HandleKind K : Kinds)
    for (HandleCategory C : Cats)
      for (PolicyMode Mode : {PolicyMode::Silent, PolicyMode::Possibly})
        EXPECT_EQ(onUse(handle(K, Position::first(0)), C, Mode).Verdict.Kind, VerdictKind::Fine);
}

TEST(Deteccion, NoResueltoNuncaSeInformaComoConfirmado) {
  Mutation M{ContainerKind::Vector, Operation::PushBack, Point::Back};
  HandleState H =
      handle(HandleKind::Element, Position::first(0))
          .withValidity(Validity::dependsOn(Condition::CapacityReached, event(M, Position::pastEnd())));
  EXPECT_EQ(onUse(H, HandleCategory::Reference, PolicyMode::Possibly).Verdict.Kind, VerdictKind::Possibly);
  EXPECT_EQ(onUse(H, HandleCategory::Reference, PolicyMode::Possibly).Verdict.Missing,
            MissingGuarantee::ReserveBefore);
  EXPECT_EQ(onUse(H, HandleCategory::Reference, PolicyMode::Silent).Verdict.Kind, VerdictKind::Fine);
}

TEST(Deteccion, SeAvisaUnaVezPorHandleYCamino) {
  Mutation M{ContainerKind::Vector, Operation::Clear, Point::Whole};
  HandleState H = handle(HandleKind::Element, Position::first(0))
                      .withValidity(Validity::invalidated(event(M, Position::unknown())));
  UseResult First = onUse(H, HandleCategory::Pointer, PolicyMode::Silent);
  EXPECT_EQ(First.Verdict.Kind, VerdictKind::Confirmed);
  EXPECT_EQ(First.State.validity().kind(), ValidityKind::Diagnosed);
  EXPECT_EQ(onUse(First.State, HandleCategory::Pointer, PolicyMode::Silent).Verdict.Kind, VerdictKind::Fine);
}

TEST(Deteccion, UnAvisoPosibleNoTapaUnoConfirmadoPosterior) {
  Mutation Push{ContainerKind::Vector, Operation::PushBack, Point::Back};
  Mutation Clear{ContainerKind::Vector, Operation::Clear, Point::Whole};
  HandleState H =
      apply(event(Push, Position::pastEnd()), handle(HandleKind::Element, Position::first(0)), std::nullopt)
          .State;
  UseResult U1 = onUse(H, HandleCategory::Reference, PolicyMode::Possibly);
  EXPECT_EQ(U1.Verdict.Kind, VerdictKind::Possibly);
  EXPECT_EQ(onUse(U1.State, HandleCategory::Reference, PolicyMode::Possibly).Verdict.Kind, VerdictKind::Fine);
  HandleState H2 = apply(event(Clear, Position::unknown()), U1.State, std::nullopt).State;
  EXPECT_EQ(onUse(H2, HandleCategory::Reference, PolicyMode::Possibly).Verdict.Kind, VerdictKind::Confirmed);
}

TEST(Deteccion, LaCategoriaDelMensajeEsLaDelSitioDeUso) {
  Mutation M{ContainerKind::List, Operation::Clear, Point::Whole};
  HandleState H = handle(HandleKind::Element, Position::first(0))
                      .withValidity(Validity::invalidated(event(M, Position::unknown())));
  for (HandleCategory C : Cats)
    EXPECT_EQ(onUse(H, C, PolicyMode::Silent).Verdict.Category, C);
}

TEST(Deteccion, MoverNoCambiaLaValidez) {
  Mutation M{ContainerKind::List, Operation::Clear, Point::Whole};
  for (const HandleState &H : states(HandleKind::IteratorObject, Position::first(0), M))
    for (Step S : {Step{StepKind::Increment}, Step{StepKind::Decrement}, Step{StepKind::Advance, 3},
                   Step{StepKind::UnknownStep}})
      EXPECT_EQ(move(H, S).validity(), H.validity());
}

TEST(Deteccion, EscaparOlvidaLoQueNoEstaInvalidado) {
  Mutation M{ContainerKind::List, Operation::Clear, Point::Whole};
  for (const HandleState &H : states(HandleKind::Element, Position::first(0), M)) {
    std::optional<HandleState> E = escape(H, S2);
    if (H.validity().kind() >= ValidityKind::Invalidated)
      EXPECT_EQ(E, std::optional<HandleState>(H)); // ninguna llamada revive un handle
    else
      EXPECT_FALSE(E.has_value());
  }
}

// ── Nombres y bordes de las posiciones ───────────────────────────────────

TEST(Lenguaje, TodoNombreDelLenguajeTieneTexto) {
  // Los avisos se arman con estos nombres: ninguno puede salir como «?».
  for (int I = 0; I <= static_cast<int>(ContainerKind::UnorderedMap); ++I)
    EXPECT_STRNE(nameOf(static_cast<ContainerKind>(I)), "?");
  for (int I = 0; I <= static_cast<int>(Operation::Sort); ++I)
    EXPECT_STRNE(nameOf(static_cast<Operation>(I)), "?");
  for (HandleCategory C : Cats)
    EXPECT_STRNE(nameOf(C), "?");
}

TEST(Lenguaje, TodaMutacionDeLaNormaEsConocida) {
  forAllMutations([](const Mutation &M) { EXPECT_TRUE(isKnown(M)); });
  EXPECT_FALSE(isKnown({ContainerKind::Set, Operation::PushBack, Point::Back}));
}

TEST(Posicion, DesdeElFinalAvanzarYRetrocederSonInversos) {
  EXPECT_EQ(Position::last(0).advance(1), Position::pastEnd());
  EXPECT_EQ(Position::pastEnd().advance(-1), Position::last(0));
  EXPECT_EQ(Position::last(2).advance(1), Position::last(1));
  EXPECT_EQ(Position::last(1).advance(-1), Position::last(2));
  // Pasar del final o no saber dónde se está no inventa un elemento.
  EXPECT_EQ(Position::pastEnd().advance(1), Position::unknown());
  EXPECT_EQ(Position::unknown().advance(1), Position::unknown());
}

TEST(Posicion, LaDistanciaSoloSeDaCuandoSeSabe) {
  EXPECT_EQ(distance(Position::last(2), Position::pastEnd()), std::optional<int>(3));
  EXPECT_EQ(distance(Position::last(3), Position::last(1)), std::optional<int>(2));
  EXPECT_EQ(distance(Position::first(0), Position::last(0)), std::nullopt);
  EXPECT_EQ(distance(Position::unknown(), Position::pastEnd()), std::nullopt);
}

TEST(Deteccion, CadaRazonDeNoResueltoDiceQueFalta) {
  Mutation M{ContainerKind::Vector, Operation::PushBack, Point::Back};
  MutationEvent E = event(M, Position::pastEnd());
  auto Falta = [&](Validity V) {
    return onUse(handle(HandleKind::Element, Position::first(0)).withValidity(V), HandleCategory::Reference,
                 PolicyMode::Possibly)
        .Verdict.Missing;
  };
  EXPECT_EQ(Falta(Validity::dependsOn(Condition::CapacityReached, E)), MissingGuarantee::ReserveBefore);
  EXPECT_EQ(Falta(Validity::dependsOn(Condition::NonBinding, E)), MissingGuarantee::ReobtainAfter);
  EXPECT_EQ(Falta(Validity::relationUnknown(E)), MissingGuarantee::SizeAtLeastTwo);
  EXPECT_EQ(Falta(Validity::escaped(S1)), MissingGuarantee::ReobtainAfter);
}

// ── Integración: la etiqueta del banco sale de la norma, pasando por el núcleo ─

namespace {
enum class Label { Safe, Policy, Ub };
struct BankCell {
  const char *Name;
  Mutation M;
  Position PointPos;
  HandleKind Kind;
  HandleCategory UseAs;
  Credit Reserved;
  Label Expected;
};
const BankCell Bank[] = {
#include "BancoCasos.inc"
};
} // namespace

TEST(Banco, ElVeredictoDelNucleoEsLaEtiqueta) {
  unsigned N = 0;
  for (const BankCell &B : Bank) {
    ++N;
    HandleState H = handle(B.Kind, Position::first(0));
    HandleState After = apply(event(B.M, B.PointPos), H, B.Reserved).State;
    VerdictKind V = onUse(After, B.UseAs, PolicyMode::Possibly).Verdict.Kind;
    VerdictKind Want = B.Expected == Label::Ub     ? VerdictKind::Confirmed
                       : B.Expected == Label::Safe ? VerdictKind::Fine
                                                   : VerdictKind::Possibly;
    EXPECT_EQ(V, Want) << B.Name;
  }
  EXPECT_EQ(N, 171u + 12u); // 57 pares × 3 sostenes + 12 celdas con reserve (sin bucle)
}
