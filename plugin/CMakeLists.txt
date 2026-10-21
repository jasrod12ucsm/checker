cmake_minimum_required(VERSION 3.20)
project(ucsm-container-invalidation LANGUAGES CXX)

# Checker de invalidación de handles para Clang Static Analyzer.
# Tres targets (libro/diseno/donde-va.md):
#   ucsm_dominio           núcleo puro, SIN include dirs de Clang
#   ContainerInvalidation  plugin .so: acl + checker + registro
#   dominio_tests          GoogleTest, una prueba por ley

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

find_package(Python3 REQUIRED COMPONENTS Interpreter)

set(UCSM_WARNINGS -Wall -Wextra -Werror=switch -Wno-unused-parameter)
set(REPO ${CMAKE_CURRENT_SOURCE_DIR}/..)

# --- La tabla normativa: se genera desde norma/matriz.json -------------------
set(TABLA ${CMAKE_CURRENT_BINARY_DIR}/generado/NormTable.inc)
add_custom_command(
  OUTPUT ${TABLA}
  COMMAND Python3::Interpreter ${REPO}/norma/gen_tabla.py ${REPO}/norma/matriz.json ${TABLA}
  DEPENDS ${REPO}/norma/matriz.json ${REPO}/norma/gen_tabla.py
  COMMENT "Generar la tabla normativa (matriz.json → NormTable.inc)")

# --- Núcleo: no sabe de Clang -----------------------------------------------
add_library(ucsm_dominio STATIC
  dominio/NormTable.cpp dominio/Position.cpp dominio/Decisions.cpp ${TABLA})
target_include_directories(ucsm_dominio PUBLIC dominio PRIVATE ${CMAKE_CURRENT_BINARY_DIR})
target_compile_options(ucsm_dominio PRIVATE ${UCSM_WARNINGS} -fno-exceptions -fno-rtti)

# Cobertura de líneas del núcleo con llvm-cov (servicio «calidad» de docker compose).
option(UCSM_COVERAGE "Instrumentar el núcleo y sus pruebas para llvm-cov" OFF)
if(UCSM_COVERAGE)
  target_compile_options(ucsm_dominio PRIVATE -fprofile-instr-generate -fcoverage-mapping)
endif()

# --- Pruebas del núcleo ------------------------------------------------------
enable_testing()
find_package(GTest)
if(GTest_FOUND)
  set(BANCO ${CMAKE_CURRENT_BINARY_DIR}/BancoCasos.inc)
  add_custom_command(
    OUTPUT ${BANCO}
    COMMAND Python3::Interpreter ${CMAKE_CURRENT_SOURCE_DIR}/tests/dominio/gen_casos_banco.py
            ${REPO}/norma/matriz.json ${REPO}/test/corpus_truth.json ${BANCO}
    DEPENDS ${REPO}/norma/matriz.json ${REPO}/test/corpus_truth.json
            tests/dominio/gen_casos_banco.py)
  add_executable(dominio_tests tests/dominio/LeyesTest.cpp ${BANCO})
  target_include_directories(dominio_tests PRIVATE ${CMAKE_CURRENT_BINARY_DIR})
  target_link_libraries(dominio_tests PRIVATE ucsm_dominio GTest::gtest_main)
  target_compile_options(dominio_tests PRIVATE ${UCSM_WARNINGS})
  if(UCSM_COVERAGE)
    target_compile_options(dominio_tests PRIVATE -fprofile-instr-generate -fcoverage-mapping)
    target_link_options(dominio_tests PRIVATE -fprofile-instr-generate)
  endif()
  add_test(NAME leyes COMMAND dominio_tests)
endif()

# --- Plugin de CSA -----------------------------------------------------------
find_package(LLVM REQUIRED CONFIG)
find_package(Clang REQUIRED CONFIG)
message(STATUS "LLVM ${LLVM_PACKAGE_VERSION} en ${LLVM_DIR}")

add_library(ContainerInvalidation MODULE
  acl/ClangRecognizer.cpp
  checker/InvalidationChecker.cpp
  checker/Messages.cpp
  registro/Plugin.cpp)
target_include_directories(ContainerInvalidation SYSTEM PRIVATE ${LLVM_INCLUDE_DIRS} ${CLANG_INCLUDE_DIRS})
target_include_directories(ContainerInvalidation PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
separate_arguments(LLVM_DEFS NATIVE_COMMAND "${LLVM_DEFINITIONS}")
target_compile_definitions(ContainerInvalidation PRIVATE ${LLVM_DEFS})
target_compile_options(ContainerInvalidation PRIVATE ${UCSM_WARNINGS} -fno-exceptions)
if(NOT LLVM_ENABLE_RTTI)
  target_compile_options(ContainerInvalidation PRIVATE -fno-rtti)
endif()
target_link_libraries(ContainerInvalidation PRIVATE ucsm_dominio)
# Los símbolos de Clang los pone el propio clang al cargar el plugin.
set_target_properties(ContainerInvalidation PROPERTIES PREFIX "lib")

# --- Pruebas lit del checker -------------------------------------------------
configure_file(tests/lit/lit.site.cfg.py.in ${CMAKE_CURRENT_BINARY_DIR}/tests/lit/lit.site.cfg.py @ONLY)
add_test(NAME lit COMMAND lit -v ${CMAKE_CURRENT_BINARY_DIR}/tests/lit)
