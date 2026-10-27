# Capítulo 5 — Arquitectura del proyecto

El sistema es **Centinela C++**: un servicio web en TypeScript que recibe
los *pull requests* de GitHub, los analiza con el checker y publica el
resultado. Cada sección muestra primero el servicio y después el **motor de
análisis** (el checker), que conserva su diseño propio.

El servicio tiene tres contextos (identidad, repositorios y revisiones),
una capa de casos de uso y adaptadores para HTTP, SQLite, GitHub, el
analizador y la criptografía (sección 5.3). El motor de análisis tiene
**cuatro contextos** con una dependencia común, la **norma**:

| Contexto | Corre en | Hace |
|---|---|---|
| **Norma** | archivo versionado | dice qué invalida cada operación (C++17) |
| **Detección** | dentro de `clang`, como plugin de CSA | sigue handles por cada camino y avisa del uso inválido |
| **Evaluación** | fuera de `clang`, en Python | ejecuta el banco en cuatro condiciones, coteja por sitio y mide |
| **Validación dinámica** | fuera de `clang`, ejecutando | confirma las etiquetas del banco con libstdc++ Debug y ASan |

Dentro de la detección hay tres capas, y **la frontera entre ellas la impone
CMake**, no una convención:

1. **Núcleo de dominio** (C++ puro): tipos del lenguaje ubicuo y decisiones
   `(estado, evento) → (estado', efectos)`. No ve Clang.
2. **Anticorrupción**: traduce `CallEvent`, `SVal` y `MemRegion` al lenguaje
   ubicuo.
3. **Cáscara**: los callbacks de CSA. Leen el `ProgramState`, llaman al
   núcleo y aplican sus efectos (`addTransition`, `emitReport`).

| Sección | Diagramas |
|---|---|
| [5.1 Casos de uso](5-1-casos-de-uso.md) | casos de uso del servicio |
| [5.2 Colaboración](5-2-colaboracion.md) | secuencia de una revisión; comunicación y secuencia del motor |
| [5.3 Paquetes](5-3-paquetes.md) | paquetes del servicio y del motor |
| [5.4 Clases](5-4-clases.md) | dominio del servicio; dominio, cáscara y evaluación del motor |
| [5.5 Estados](5-5-estados.md) | ciclo de una revisión; ciclo del handle y crédito de garantía |
| [5.6 Arquitectura lógica](5-6-arquitectura-logica.md) | capas del servicio y del motor |
| [5.7 Arquitectura física](5-7-arquitectura-fisica.md) | despliegue del servicio y del motor |
