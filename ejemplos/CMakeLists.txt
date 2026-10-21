# Proyecto mínimo con base de compilación, para probar RF-03 en segundos:
#   python3 bench/codigo_real.py . build/verificacion/ejemplos.json Possibly noredundancy ejemplos
cmake_minimum_required(VERSION 3.20)
project(ejemplos LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 17)
add_library(ejemplos STATIC prueba.cpp buen_uso.cpp)
