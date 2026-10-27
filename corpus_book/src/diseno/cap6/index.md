# Capítulo 6 — Interfaces y modelo de datos

Este capítulo describe cómo se usa Centinela C++: las pantallas del panel web
que usan el administrador y el desarrollador, la API HTTP que esas pantallas
consumen, el *webhook* que recibe de GitHub, los servicios externos que el
sistema usa y el modelo de su base de datos.

El checker `ucsm.ContainerInvalidation` no tiene pantallas propias: lo usa el
servicio dentro del trabajador de revisiones (sección 5.6) y su salida llega
al usuario como comentarios en el *pull request* y como hallazgos en el panel.

| Sección | Contenido |
|---|---|
| 6.1 | quién usa qué pantalla |
| 6.2 | navegación entre pantallas |
| 6.3 | *mockups* de cada pantalla y sus estados |
| 6.4 | elementos de la interfaz y reglas |
| 6.5 a 6.7 | API HTTP y *webhook* |
| 6.8 | servicios que consume (GitHub, clang) |
| 6.9 | modelo de la base de datos |
