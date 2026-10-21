# 7.3 Control de versiones

## a) Sistema elegido

**Git** (distribuido) con remoto en **GitHub**. Cada integrante trabaja con su
copia completa y el remoto es el punto de integración y de publicación de
resultados.

## b) Configuración del repositorio

- Estructura: la de [Dónde va cada cosa](../diseno/donde-va.md).
- `.gitignore`: `build/`, `corpus_book/book/`, `*.plist` sueltos en la raíz
  (hoy hay varios), cachés de Python.
- **Se versiona**: el código, `norma/`, el banco congelado, `libro/`, los
  `.puml` y sus SVG.
- `test/experimento/` y `test/codigo_real/` se versionan sólo cuando cambian
  por un experimento que va al informe, con su tag.

## c) Ramas

**GitHub Flow**, porque el equipo es de dos personas y el CI corre el banco
completo:

| Rama | Para | Vida |
|---|---|---|
| `main` | lo que compila, pasa pruebas y tiene el banco medido | permanente, protegida |
| `feat/<incremento>-<tema>` | un cambio del plan (`feat/I2-referencias`) | días |
| `fix/<tema>` | corregir un FN/FP encontrado | horas |
| `norma/<tema>` | cambio en `matriz.json` (exige revisión de la otra integrante) | días |
| `exp/<nombre>` | experimento descartable (p. ej. bifurcar por capacidad) | hasta decidir |

## d) Commits

- Pequeños y frecuentes, con mensaje en español, imperativo y con ámbito:
  `norma: deque::push_front preserva referencias [deque.modifiers]/1`,
  `núcleo: transportar posición en mutaciones que preservan`.
- El historial actual tiene tres commits llamados «cambios». A partir de I0
  se aplica esta convención.

## e) Revisión y fusión

*Pull request* obligatorio hacia `main`, con la lista de revisión de
[7.1 d)](7-1-codigo.md) y la tabla del banco antes/después. Fusión con
*squash* para que cada incremento sea un commit legible.

## f) Versionado y etiquetas

| Tag | Cuándo | Ejemplo |
|---|---|---|
| `vMAJOR.MINOR.PATCH` del plugin | al cerrar un incremento | `v0.2.0` = I2 |
| `banco-N` | al congelar una versión del banco; el sello `test/banco-N.json` guarda el sha256 del banco y de sus etiquetas, y `bench/experimento.py` se detiene si el banco no coincide | `banco-1` = 750 casos (sellado el 2026-10-20) |
| `exp-<incremento>-<fecha>` | cada experimento que va al informe | `exp-I6-2026-12-15` |

MAJOR sube si cambia la interfaz del checker (nombre u opciones); MINOR, si
cubre reglas nuevas; PATCH, si corrige.

## g) Integración y entrega continuas

![Integración continua](../diagramas/7-integracion-continua.svg)

La «entrega» de este proyecto es el `.so`, el banco y el informe. El CI
(`.github/workflows/ci.yml`, detalle en 7.1 e) publica `test/experimento/`
como artefacto. **No hay despliegue a un servidor.**
