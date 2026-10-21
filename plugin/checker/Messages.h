//===- Messages.h - Textos de avisos y notas (RF-08) ------------*- C++ -*-===//
#ifndef UCSM_CHECKER_MESSAGES_H
#define UCSM_CHECKER_MESSAGES_H

#include "HandleState.h"

#include <string>

namespace ucsm::messages {

std::string confirmed(const dominio::UseVerdict &V, unsigned MutationLine);
std::string possibly(const dominio::UseVerdict &V, unsigned CauseLine);
std::string invalidatedNote(const dominio::MutationEvent &E, dominio::HandleKind K);
std::string unresolvedNote(const dominio::Validity &V, dominio::HandleKind K);
std::string guaranteeNote(unsigned K);
/// «El iterador se obtiene de 'vector::begin'».
std::string obtainedNote(dominio::ContainerKind C, const std::string &Method, dominio::HandleKind K);
/// «El handle al elemento se obtiene al desreferenciar el iterador».
std::string derefNote();

} // namespace ucsm::messages

#endif
