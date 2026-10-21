# Capítulo 7 — Construcción del software

> **Es un plan, no una crónica.** La práctica 7 pide implementar. Este
> capítulo fija **cómo** se va a construir el checker, en qué orden y con qué
> controles de calidad, antes de escribir su código. Lo que ya existe se
> marca como tal (§7.7). Lo demás se marca como previsto.

Se sigue el **Caso A** de la práctica (implementación de un sistema de
software). El Caso B (CRISP-DM) **no aplica**: el proyecto no entrena ningún
modelo, y el banco es un instrumento de medición con etiquetas normativas, no
un conjunto de entrenamiento.

| Tema de la práctica | Sección | Qué significa en este proyecto |
|---|---|---|
| Construcción del código | [7.1](7-1-codigo.md) | plugin C++ para CSA en incrementos, cada uno medido contra el banco |
| Construcción de la base de datos | [7.2](7-2-datos.md) | no hay SGBD: los datos son archivos JSON/CSV versionados con un esquema, claves e integridad comprobadas |
| Control de versiones | [7.3](7-3-versiones.md) | Git + GitHub, ramas cortas, *tags* por incremento y por experimento |
| Calidad del código | [7.4](7-4-calidad.md) | estilo LLVM, frontera de capas impuesta por CMake, pruebas por ley, el banco como regresión |
| Desarrollo de componentes | [7.5](7-5-componentes.md) | doce componentes con interfaz, dependencias y prueba propias |
| Plan de incrementos | [7.6](7-6-incrementos.md) | I0–I6, qué celda del banco ataca cada uno |
| Estado actual | [7.7](7-7-estado.md) | qué existe hoy y qué no |
