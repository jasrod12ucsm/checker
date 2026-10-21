// CU-05: el plugin carga y registra el checker con su opción.
// RUN: %clang -cc1 -load %plugin -analyzer-checker-help | FileCheck %s --check-prefix=HELP
// RUN: %clang -cc1 -load %plugin -analyzer-checker-option-help | FileCheck %s --check-prefix=OPT
// HELP: ucsm.ContainerInvalidation
// OPT: ucsm.ContainerInvalidation:PolicyMode
