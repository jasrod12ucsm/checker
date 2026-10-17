# mi-linter

Linter de C++ construido sobre Clang LibTooling. Ejemplo minimo pero completo:
detecta excepciones capturadas por valor (`catch (std::exception e)`), que
provocan *object slicing*, y propone el fix-it `catch (const std::exception &e)`.

## Dependencias (Arch Linux)

    sudo pacman -S llvm clang cmake ninja

`clang` trae los headers de Clang y `ClangConfig.cmake`; `llvm` trae los headers
de LLVM y `LLVMConfig.cmake`. Hacen falta los dos.

En Debian/Ubuntu: `sudo apt install llvm-dev libclang-dev clang cmake ninja-build`

## Compilar

    cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release
    cmake --build build

## Ejecutar

    ./build/mi-linter test/catch_by_value.cpp -- -std=c++17

Sobre un proyecto real con `compile_commands.json`:

    ./build/mi-linter -p /ruta/al/build $(find /ruta/src -name '*.cpp')

Codigo de salida 1 si hay hallazgos, para usarlo como gate en CI.

## Explorar el AST

    clang-query test/catch_by_value.cpp -- -std=c++17
    > set traversal IgnoreUnlessSpelledInSource
    > m varDecl(isExceptionVariable(), hasType(hasCanonicalType(recordType())))

    clang++ -Xclang -ast-dump -fsyntax-only test/catch_by_value.cpp -std=c++17

## Estructura

    CMakeLists.txt              build contra el LLVM/Clang del sistema
    src/MiLinter.cpp            driver: CLI, ClangTool, registro de reglas
    src/CatchByValueCheck.h     declaracion de la regla
    src/CatchByValueCheck.cpp   matcher + callback + diagnostico + fix-it
    test/catch_by_value.cpp     casos positivos y negativos
# checker
