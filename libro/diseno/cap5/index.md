# Capítulo 5 — Arquitectura del proyecto

> Versión rehecha el 2026-10-18. Reemplaza al capítulo 5 del informe y al
> libro de diagramas de `mi-linter`. El porqué está en
> [Por qué se rehízo el diseño](../critica.md).

La arquitectura tiene **cuatro contextos** con una dependencia común, la
**norma**:

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
| [5.1 Casos de uso](5-1-casos-de-uso.md) | casos de uso |
| [5.2 Colaboración](5-2-colaboracion.md) | comunicación + secuencia |
| [5.3 Paquetes](5-3-paquetes.md) | paquetes |
| [5.4 Clases](5-4-clases.md) | dominio, cáscara, evaluación |
| [5.5 Estados](5-5-estados.md) | ciclo del handle + crédito de garantía |
| [5.6 Arquitectura lógica](5-6-arquitectura-logica.md) | capas y flujo |
| [5.7 Arquitectura física](5-7-arquitectura-fisica.md) | despliegue |
