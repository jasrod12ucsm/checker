# Capítulo 7 — Construcción del software

Este capítulo documenta cómo se construyó **Centinela C++**, el servicio web
que revisa los *pull requests* de C++ de un equipo, y su **motor de análisis**,
el checker `ucsm.ContainerInvalidation`: con qué herramientas, en qué orden,
con qué controles de calidad y qué existe hoy (sección 7.7).

Se sigue el **Caso A** de la práctica (implementación de un sistema de
software). El Caso B (CRISP-DM) **no aplica**: el proyecto no entrena ningún
modelo, y el banco es un instrumento de medición con etiquetas normativas, no
un conjunto de entrenamiento.

| Tema de la práctica | Sección | Qué significa en este proyecto |
|---|---|---|
| Construcción del código | [7.1](7-1-codigo.md) | el servicio Centinela C++ en TypeScript y el plugin C++ para CSA, en incrementos con sus pruebas |
| Construcción de la base de datos | [7.2](7-2-datos.md) | la base relacional del servicio (SQLite) y los datos versionados de la evaluación del motor (JSON) |
| Control de versiones | [7.3](7-3-versiones.md) | Git + GitHub; desde I7, ramas cortas y *pull request*; *tags* `banco-1` y `v1.0.0` |
| Calidad del código | [7.4](7-4-calidad.md) | tipos estrictos y prueba de arquitectura en el servicio; estilo LLVM, frontera de capas impuesta por CMake, pruebas por ley y el banco como regresión en el motor |
| Desarrollo de componentes | [7.5](7-5-componentes.md) | los paquetes del servicio y los componentes del motor, cada uno con interfaz, dependencias y prueba propias |
| Plan de incrementos | [7.6](7-6-incrementos.md) | I0 a I6 del motor e I7 del servicio |
| Estado actual | [7.7](7-7-estado.md) | qué existe hoy y qué no |
