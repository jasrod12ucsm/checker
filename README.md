# Centinela C++ y el checker `ucsm.ContainerInvalidation`

**Centinela C++** (`sistema/`) es un servicio web que revisa automáticamente
los *pull requests* de C++ de un equipo en GitHub: analiza los archivos que
cambiaron con el checker de este repositorio, comenta cada uso de un handle
invalidado en su línea y puede bloquear el merge. Tiene registro (sin usuarios predefinidos:
la primera cuenta administra), roles, panel y API.

```bash
docker compose build sistema
docker compose up sistema-demo              # demostración con un GitHub simulado: http://localhost:8080
docker compose run --rm sistema-pruebas     # 140 pruebas, con clang y el checker reales
```

Para usarlo con GitHub de verdad: `sistema/.env.ejemplo` y el libro
(*Sistema → Ponerlo en marcha con GitHub*).

## El checker

Checker para Clang Static Analyzer (LLVM 21) que avisa del uso de un
iterador, una referencia o un puntero a un elemento de un contenedor de la
STL después de una operación que lo invalida según C++17. Las reglas de
invalidación están escritas como datos en `norma/matriz.json`, cada una con
su cláusula de la norma.

### En dos minutos

Solo hace falta Docker con `docker compose`:

```bash
git clone https://github.com/jasrod12ucsm/checker.git
cd checker
docker compose build                 # una sola vez: descarga LLVM 21 (imagen de unos 2 GB)
docker compose run --rm verificar    # construye el checker y verifica los requerimientos (~30 s)
```

Probarlo sobre un archivo:

```bash
docker compose run --rm shell
clang++ -std=c++17 --analyze -o /dev/null \
  -Xclang -load -Xclang build/plugin/libContainerInvalidation.so \
  -Xclang -analyzer-checker=ucsm.ContainerInvalidation \
  -Xclang -analyzer-config -Xclang ucsm.ContainerInvalidation:PolicyMode=Possibly \
  -Xclang -analyzer-output=text \
  ejemplos/prueba.cpp
```

## El libro del proyecto

Todo está documentado en el libro (mdbook): cómo usar el checker, correr los
bench y el corpus, el diseño, los resultados y **en qué parte del código se
valida cada requerimiento**, con los fragmentos de código.

```bash
python3 bench/gen_book.py
mdbook serve corpus_book --open
```

Las páginas escritas a mano están en `libro/`; empieza por
`libro/uso/index.md`.

## Resultado principal del checker

En un banco de 750 casos etiquetados desde la norma y validados con libstdc++
Debug Mode y ASan (852 ejecuciones, 0 contradicciones), CSA solo detecta 80
de 342 usos inválidos y ninguno sobre referencias o punteros retenidos. Con el
checker detecta los 342, sin falsos positivos en 306 casos seguros, con un
sobrecosto mediano de tiempo de 0.3 %.
