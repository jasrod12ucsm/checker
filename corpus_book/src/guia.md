
# Cómo leer este libro

## El problema que estudia el corpus

En C++ puedes guardar un **iterador**, una **referencia** o un **puntero** a un
elemento de un contenedor (`vector`, `map`, ...). Si después **modificas el
contenedor** (insertas, borras, limpias), lo que guardaste puede quedar **roto**:
el elemento se movió de lugar o dejó de existir.

```cpp
std::vector<int> v = {1, 2, 3};
auto it = v.begin();   // guardo un iterador al primer elemento
v.clear();             // modifico el contenedor: el elemento ya no existe
std::cout << *it;      // uso lo guardado -> BUG
```

Usar algo roto es **comportamiento indefinido** (*Undefined Behavior*, **UB**):
el estándar no dice qué pasa. Puede crashear, imprimir basura o, peor, parecer
que funciona. Que no explote no significa que esté bien.

Si se rompe o no depende del contenedor y de la operación. En `std::list`, por
ejemplo, `push_back` no rompe nada; en `std::vector` puede romperlo todo.

## Qué es un caso

Cada caso es una función pequeña con ese patrón: **guardar, modificar, usar**.
Su nombre dice exactamente qué prueba:

```text
f_deque_push_back_ref_bucle
  │     │         │    └── forma: cómo está escrito el código (recto, guarda, bucle, llamada)
  │     │         └─────── qué se guarda: it (iterador), ref (referencia), ptr (puntero)
  │     └───────────────── operación que modifica el contenedor
  └─────────────────────── contenedor
```

Las cuatro formas sintácticas prueban **el mismo bug escrito de cuatro maneras**,
para ver si la herramienta depende de cómo se escribe el código:

- **`recto`**: handle obtenido, mutación directa y uso, sin comparación contra `end()`.
- **`guarda`**: igual que `recto`, pero con `if (it == c.end()) return;` antes de mutar.
- **`bucle`**: mutación dentro de un `for` acotado a tres rondas; también participa el iterador de control.
- **`llamada`**: la mutación ocurre dentro de una función auxiliar `mutar_*` (cruza una llamada).

## La etiqueta: la respuesta correcta

Cada caso tiene una **etiqueta** que dice, según las reglas del estándar C++17,
si el programa tiene el bug o no. Es la "respuesta del examen":

| Etiqueta | Significa |
|---|---|
| 🔴 `UB` | **Hay bug**: se usa algo que quedó roto. |
| 🟢 `SAFE` | **No hay bug**: lo guardado sigue siendo válido. |
| 🟡 `POLICY` | **Depende del estado**: p. ej. `vector::push_back` solo rompe los iteradores si el vector se queda sin capacidad y se muda de memoria. |

## Lo que hizo el analizador estático

La herramienta evaluada es el **Clang Static Analyzer**: lee el código sin
ejecutarlo y avisa si cree que hay un bug. Para cada caso pueden pasar cuatro
cosas. **El color es la respuesta correcta; el texto, lo que hizo la herramienta:**

| Etiqueta | Clang | Se muestra | ¿Bien o mal? |
|---|---|---|---|
| 🔴 `UB` | avisa | ✅ detectado | Bien: encontró el bug. |
| 🔴 `UB` | no avisa | ❌ no detectado | **Mal**: había bug y no lo vio (*falso negativo*). |
| 🟢 `SAFE` | no avisa | ✅ correcto, sin aviso | Bien: no había bug y no dijo nada. |
| 🟢 `SAFE` | avisa | ❌ falsa alarma | Mal: avisó de un bug inexistente (*falso positivo*). |
| 🟡 `POLICY` | — | ⚪ depende del estado | No se puntúa: la respuesta depende de la ejecución. |

Entonces un 🟢 sin aviso **es un acierto**. Los que importan son los 🔴 ❌.

**Resultado:** Clang detecta 80 de 342 bugs
(23.4%) y no da ninguna falsa alarma. Se le escapan
casi todos, y en especial **todos** los casos en que lo guardado es una referencia
o un puntero.

## Lo que pasó al ejecutar (validación dinámica)

Para comprobar que los bugs son reales, cada caso también **se ejecuta** con dos
herramientas que vigilan el programa mientras corre:

| Herramienta | Qué detecta | Mensaje típico |
|---|---|---|
| **libstdc++ Debug Mode** | Uso de un iterador roto (la biblioteca lleva la cuenta de qué iteradores siguen vigentes). | `attempt to dereference a singular iterator` (*singular* = roto) |
| **ASan/UBSan** | Acceso a memoria que ya fue liberada. | `heap-use-after-free` |

Si estas herramientas no te suenan, lee primero
[Las herramientas de ejecución](herramientas.md): las explica desde cero.

En las tablas de cada caso:

- 🛑 **detectado**: la herramienta vio el bug al ejecutar.
- **sin detección**: el programa terminó sin que la herramienta notara nada.

Un caso 🔴 `UB` **sin detección** sigue siendo un bug: a veces la memoria rota
todavía contiene el valor viejo y el programa "funciona" por suerte. Por eso la
etiqueta la decide el estándar y no la ejecución. Los casos 🟢 `SAFE` nunca
produjeron una detección, lo que respalda que están bien etiquetados.

Los casos 🟡 `POLICY` se ejecutan dos veces: **`force`** (preparando el
contenedor para que la operación sí rompa lo guardado) y **`preserve`**
(preparándolo para que no lo rompa). En el resto de casos el escenario es
**`natural`** (un contenedor ordinario `{1, 2, 3}`).

## Recorrido sugerido

1. Lee un caso fácil: [`std::vector` → `clear`](casos/vector/clear.md). Todo es
   🔴 UB, y se ve qué detecta cada herramienta.
2. Compáralo con [`std::list` → `push_back`](casos/list/push_back.md), donde casi
   todo es 🟢 SAFE.
3. Mira un caso mixto: [`std::deque` → `push_back`](casos/deque/push_back.md),
   donde el iterador se rompe pero la referencia no.
4. Luego ve a los resultados: [Análisis estático](resultados/estatico.md) y el
   [catálogo de por qué Clang no detecta](resultados/fallos.md).
