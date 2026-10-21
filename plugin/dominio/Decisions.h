//===- Decisions.h - Las decisiones puras del motor -------------*- C++ -*-===//
//
// Un substep del workflow «Seguir un handle» = una función pura. La cáscara
// carga el estado, llama aquí y aplica el resultado (deteccion.md §6).
//
//===----------------------------------------------------------------------===//
#ifndef UCSM_DOMINIO_DECISIONS_H
#define UCSM_DOMINIO_DECISIONS_H

#include "HandleState.h"

namespace ucsm::dominio {

enum class SolverAnswer : std::uint8_t { OnlyYes, OnlyNo, Both };

HandleState obtain(const Origin &O);

struct ApplyResult {
  HandleState State;
  bool Noted; // la validez cambió: va una nota en la ruta
};

/// Lo que una mutación de SU contenedor le hace a un handle.
/// Precondición: E.Container == H.container() y la mutación está en la norma.
ApplyResult apply(const MutationEvent &E, const HandleState &H, Credit C);

/// ¿Es factible la condición en este camino? (v1: sólo mira el crédito).
SolverAnswer answer(Condition Cond, Growth G, Credit C);

/// El crédito después de la mutación.
Credit consume(const Mutation &M, Credit C);

struct UseResult {
  UseVerdict Verdict;
  HandleState State;
};

/// Un uso del handle con la categoría observada en el sitio de uso.
UseResult onUse(const HandleState &H, HandleCategory At, PolicyMode Mode);

/// El contenedor escapó a código que no se ve (D-21): un handle válido o no
/// resuelto deja de seguirse (nullopt); uno ya invalidado se conserva, porque
/// ninguna llamada lo revive.
std::optional<HandleState> escape(const HandleState &H, SourceRef At);

enum class StepKind : std::uint8_t { Increment, Decrement, Advance, UnknownStep };
struct Step {
  StepKind Kind;
  int N = 0; // sólo en Advance
};

/// ++it, --it, it + n. No cambia la validez.
HandleState move(const HandleState &H, Step S);

} // namespace ucsm::dominio

#endif
