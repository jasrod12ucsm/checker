# 5.6 Arquitectura lógica

![Arquitectura lógica](../../diagramas/5-6-arquitectura-logica.svg)

## Núcleo funcional, cáscara imperativa

CSA ya está construido como pide `modelado-funcional`: el `ProgramState` es
**inmutable** y un checker **no ejecuta** cambios, devuelve un estado nuevo.
El diseño lo lleva hasta el final:

```
callback de CSA
   │  CARGAR    leer HandleMap / IteratorMap del ProgramState
   │  TRADUCIR  acl: CallEvent, SVal → Obtención | Mutación | Uso | NotOurs
   │  DECIDIR   núcleo: (estado, evento) → (estado', [Nota | Aviso])     ← puro, probado sin Clang
   ▼  APLICAR   addTransition(estado', NoteTag) ; emitReport(aviso)
```

| Capa | Sabe de | No sabe de | Se prueba con |
|---|---|---|---|
| Núcleo | la norma, la validez, las posiciones | Clang, CSA, archivos | GoogleTest, una prueba por ley |
| Anticorrupción | AST y `SVal` de Clang, nombres de la STL | métricas, la norma | pruebas `lit` (`-verify`) |
| Cáscara | callbacks, `ProgramState`, `BugReporter` | la norma (la consulta por el núcleo) | pruebas `lit` + el banco |

## La evaluación es una tubería de funciones

```
generar banco → ejecutar (4 condiciones) → normalizar → cotejar → agregar → informe
                      └──────── registro de ejecución (versiones, comandos, incidencias) ────────┘
```

- Cada paso **recibe datos y devuelve datos**, y el anterior queda en disco
  (`test/experimento/ejecucion.json`). Se puede re-cotejar sin re-ejecutar.
- El arnés **no enlaza** el plugin: invoca `clang` como un proceso, con los
  argumentos en una lista (sin intérprete de órdenes). Lo único que ve del
  checker es su salida.
- Las métricas se calculan **en el arnés**, nunca en el checker.
