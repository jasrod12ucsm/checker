cmake_minimum_required(VERSION 3.20)
project(mi-linter LANGUAGES CXX)

# --- 1. Localizar LLVM y Clang instalados en el sistema -----------------------
# find_package(Clang) hace internamente find_package(LLVM), pero pedirlo
# explicito da un mensaje de error mas claro si falta el paquete `llvm`.
find_package(LLVM  REQUIRED CONFIG)
find_package(Clang REQUIRED CONFIG)

message(STATUS "LLVM  ${LLVM_PACKAGE_VERSION}  -> ${LLVM_DIR}")
message(STATUS "Clang                          -> ${Clang_DIR}")

# --- 2. Opciones del proyecto -------------------------------------------------
set(CMAKE_CXX_STANDARD 17)            # LLVM 16+ exige C++17 minimo
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON) # genera compile_commands.json del propio linter

add_executable(mi-linter
  src/MiLinter.cpp
  src/CatchByValueCheck.cpp
)

# --- 3. Includes --------------------------------------------------------------
# SYSTEM evita que los -Wall del proyecto ahoguen la salida con warnings de LLVM.
target_include_directories(mi-linter SYSTEM PRIVATE
  ${LLVM_INCLUDE_DIRS}
  ${CLANG_INCLUDE_DIRS}
)
target_include_directories(mi-linter PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/src)

separate_arguments(LLVM_DEFINITIONS_LIST NATIVE_COMMAND "${LLVM_DEFINITIONS}")
target_compile_definitions(mi-linter PRIVATE ${LLVM_DEFINITIONS_LIST})

# --- 4. EL GOTCHA CLASICO -----------------------------------------------------
# LLVM se distribuye compilado sin RTTI. Si tu codigo si lo usa, el enlazado
# revienta con undefined reference a typeinfo. Hay que igualar la bandera.
if(NOT LLVM_ENABLE_RTTI)
  target_compile_options(mi-linter PRIVATE -fno-rtti)
endif()

# --- 5. Enlazado --------------------------------------------------------------
# Distros como Arch/Debian compilan LLVM y Clang como una unica lib dinamica.
# Compilaciones desde fuente suelen dar libs estaticas separadas.
if(CLANG_LINK_CLANG_DYLIB)
  target_link_libraries(mi-linter PRIVATE clang-cpp)
else()
  target_link_libraries(mi-linter PRIVATE
    clangTooling clangToolingCore clangASTMatchers
    clangFrontend clangSerialization clangSema
    clangAST clangLex clangBasic clangDriver clangEdit clangAnalysis
  )
endif()

if(LLVM_LINK_LLVM_DYLIB)
  target_link_libraries(mi-linter PRIVATE LLVM)
else()
  target_link_libraries(mi-linter PRIVATE LLVMSupport LLVMCore LLVMOption LLVMFrontendOpenMP)
endif()
