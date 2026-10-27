# Capítulo 4 — Requerimientos funcionales y no funcionales

El producto es **Centinela C++**, un servicio web que revisa los *pull
requests* de C++ de un equipo con el checker `ucsm.ContainerInvalidation`.
Los requisitos RF-S y RNF-S son del servicio que usa el cliente; los RF y RNF
sin S, del motor de análisis que el servicio invoca. Los requisitos describen
lo que el sistema construido hace y cómo se comprueba. Cada uno dice **cómo se demuestra** con el analizador estático (un
comando, una prueba o una medición) y **qué evidencia** existe hoy; un
requisito que no se puede demostrar ejecutando algo no está en la lista. Los
códigos RF, RNF, RN e INT se definen una sola vez en este capítulo, y los
capítulos 1, 2, 5 y 7 usan los mismos.

- [4.1 Requerimientos funcionales](4-1-funcionales.md)
- [4.2 Requerimientos no funcionales](4-2-no-funcionales.md)

Dónde se valida cada requerimiento en el código, con sus fragmentos y la orden que lo comprueba: [Guía de uso → Dónde se valida cada requerimiento](../../uso/requerimientos.md).
