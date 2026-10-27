# 5.2 Colaboración

## Servicio: revisión de un pull request

![Secuencia de una revisión](../../diagramas/sistema-secuencia-pr.svg)

El *webhook* solo encola: verifica la firma, guarda la revisión `Pendiente`
y el trabajo **en la misma transacción** y responde 202. El análisis lo hace
el trabajador después, así GitHub no espera a `clang`. Cada caso de uso sigue
el mismo orden: **cargar** lo que necesita del almacén, **decidir** con una
función pura del dominio y aplicar los **efectos** (guardar, llamar a GitHub).

| Paso | Quién decide | Función del dominio |
|---|---|---|
| encolar | `revisiones` | `solicitar(repo, existenteDelSha, solicitud, ahora)` |
| empezar | `revisiones` | `iniciar(Revision<Pendiente>)` |
| resultado | `revisiones` | `publicar(Revision<EnAnalisis>, analisis, descartadas, …)` o `fallar(…)` |
| estado del commit | `revisiones` | `estadoCommit(repo, revision)` |

## Motor: diagrama de comunicación

![Colaboración](../../diagramas/5-2-colaboracion.svg)

El **motor de CSA conserva el control**. El checker no recorre el programa:
recibe eventos de un camino y responde con un estado nuevo. La tabla dice
**qué eventos** recibe y **qué hace cada capa** con ellos:

| Mensaje | De → a | Qué es en la API de CSA |
|---|---|---|
| 2 | `ExprEngine` → `CheckerManager` | el motor llega a una llamada, una carga/almacenamiento o un enlace (`bind`) |
| 2.1 | `CheckerManager` → cáscara | `checkPostCall`, `checkPreCall`, `checkLocation`, `checkBind`, `checkDeadSymbols`, `checkPointerEscape` |
| 2.2 | cáscara → `ProgramState` | `State->get<HandleMap>()`, `State->get<IteratorMap>()` |
| 2.3–2.4 | cáscara → anticorrupción → núcleo | `CallEvent` → `Obtention` │ `Mutation` │ `IteratorMove` │ `NotOurs` |
| 2.5 | núcleo → tabla | `NormTable::effect(contenedor, op, categoría, relación)` |
| 2.6 | núcleo → cáscara | un **valor**: estado nuevo + lista de efectos (nota, aviso) |
| 2.7 | cáscara → `ProgramState` | `C.addTransition(State', NoteTag)`: el estado nunca se muta en el sitio |
| 2.8 | cáscara → `BugReporter` | `C.generateNonFatalErrorNode()` + `emitReport(PathSensitiveBugReport)` |

## Motor: secuencia de un caso del banco

`f_vector_erase_begin_ref_recto`:

```cpp
auto it = c.begin();          // IteratorMap: it ↦ {c, First, Valid}
const auto& h = *it;          // HandleMap: región(*it) ↦ {c, Element, First, Valid}
c.erase(c.begin());           // vector::erase en First, relación Same → Invalidates
sink(h);                      // checkLocation(load, región de h) → Invalidated → aviso
```

![Secuencia](../../diagramas/5-2-secuencia.svg)

Tres hechos de CSA que el diseño aprovecha:

- `std::vector::operator*` y `begin` **no se inlinean** por defecto
  (`c++-container-inlining=false`). Su resultado es un símbolo conjurado: una
  **región nueva por cada obtención**. Ese es el handle (D-06).
- Usar `h` es **cargar** su región. `checkLocation` lo ve aunque no haya
  ninguna llamada. Por eso un AST matcher o un checker sólo de llamadas no
  basta para referencias y punteros.
- En la forma `llamada` (`mutar_vector_erase_begin(c)`) el motor **sí inlinea**
  la función del usuario. Dentro, `this` es la misma región que `c` en el
  llamador, y el `ContainerId` coincide.
