# La lógica de la detección

> Esta página responde cuatro preguntas antes de programar: **qué** demuestra
> un aviso, **de dónde** sale cada fallo, **qué hacer** cuando el fallo
> depende del estado, y **qué falta** saber. El DSL y las leyes dicen cómo se
> implementa. Esta página dice **por qué un aviso es verdad**.

## 1. La norma sola no demuestra nada

La norma es una **regla de inferencia**: «si pasa A, entonces el handle queda
inválido». No dice si A pasó. Un aviso necesita **premisas sobre el
programa**, y esas las da CSA camino por camino. Un uso inválido es la
conclusión de esta cadena, y **las seis premisas tienen que valer en el mismo
camino**:

```
P1  Obtención   h queda ligado al elemento e del contenedor c, en la posición p
P2  Mutación    después, una operación m actúa sobre ese mismo c, en el punto q
P3  Relación    e está en la relación r con q            (Same, Before, After, Any)
P4  Norma       effect(m, categoría(h), r) = Invalidates     ← la ÚNICA premisa de la norma
P5  Identidad   entre P1 y P6, h no se volvió a ligar a otro elemento
P6  Uso         h se desreferencia, se mueve o se compara
─────────────────────────────────────────────────────────────────────────
    en ese camino, el programa usa un handle inválido: comportamiento indefinido
```

**Qué demuestra.** Si las seis premisas valen en una ejecución real, la
norma dice que esa ejecución tiene comportamiento indefinido. CSA garantiza
P1, P2, P3, P5 y P6 **para un camino factible**: uno cuyas condiciones (los
`if`, los bucles) son satisfacibles a la vez. El aviso es ese camino, y sus
notas lo muestran paso a paso: *obtención → mutación → uso*. Cualquiera puede
seguirlo, y la validación dinámica lo reproduce ejecutando.

**Qué no demuestra.** Que el camino ocurra con las entradas que el programa
recibe de verdad. Es la misma garantía que da cualquier checker de CSA: «existe
una ejecución que respeta las condiciones del código y llega aquí».

**Dónde se puede equivocar**, y por eso cada premisa tiene su prueba:

| Premisa | Falla si… | Produce | Se prueba con |
|---|---|---|---|
| P1 | no se reconoce cómo se obtuvo el handle | FN | `lit`: un caso por forma de obtener (§4) |
| P2 | `c` tiene otro nombre (`auto& d = c; d.clear();`) y no se ve que es el mismo | FN | `lit` de alias (CSA da la misma región; se comprueba) |
| P3 | se calcula mal la posición tras otras mutaciones | FN o FP | leyes de `transport` |
| P4 | la tabla está mal | FN o FP | leyes de la norma + validación dinámica |
| P5 | se confunde «reasignar la variable» con «el mismo handle» | FP | ley «re-obtener no revive» |
| P6 | la carga ocurre dentro de código que no se analiza | FN | se mide por forma (`llamada`) |
| factibilidad | CSA cree factible un camino que no lo es (correlaciones que no ve) | FP | se mide en los casos `SAFE` |

## 2. Cómo se origina cada fallo, al milímetro

La norma no inventa las reglas: describe **qué hace la implementación con la
memoria**. Hay seis mecanismos y nada más. Cada fila de `matriz.json` cae en
uno de ellos:

| # | Mecanismo | Operaciones | Qué queda inválido | Qué pasa en memoria | Cómo se manifiesta |
|---|---|---|---|---|---|
| M1 | **Reubicación del búfer** | `vector`: `push_back`, `emplace_back`, `insert`, `resize`, `reserve` **si** `size` nuevo > `capacity`; `shrink_to_fit` si la implementación quiere | **todo**: iteradores, referencias, punteros | se pide un búfer nuevo, se mueven los elementos, **se libera el viejo** | `heap-use-after-free` (ASan), iterador singular (Debug) |
| M2 | **Corrimiento** | `vector` / `deque` interior: `insert`, `erase` sin reubicar | lo que está **en o después** del punto | los elementos se mueven una posición; la memoria sigue siendo del contenedor | **sin síntoma** casi siempre: se lee otro elemento, o uno ya destruido. ASan no lo ve |
| M3 | **Destrucción en el sitio** | `vector::pop_back`, `erase` del propio elemento, `clear` y `assign` de `vector` | el elemento destruido (y lo posterior) | se destruye el objeto, **la memoria no se libera** (`clear` conserva la capacidad) | sin síntoma con `int`; ASan calla |
| M4 | **Reubicación del mapa de bloques** | `deque`: inserción en un extremo | **sólo iteradores**; los elementos no se mueven | el arreglo de punteros a bloques se reubica; los bloques no | iterador singular (Debug); las referencias siguen bien |
| M5 | **Liberación del nodo** | contenedores de nodos y *unordered*: `erase`, `clear`, `pop_*`; `deque` en los extremos | el handle al nodo borrado | `delete` del nodo | `heap-use-after-free` |
| M6 | **Reorganización de cubetas** | *unordered*: `rehash`, `reserve`, inserción que supera el factor de carga | **sólo iteradores**; los nodos no se mueven | se rehace la tabla de cubetas | iterador singular (Debug); ASan calla |

Esta tabla explica dos resultados que ya tenemos:

- **Por qué la ejecución no detecta todos los UB.** M2, M3, y M4/M6 con
  referencias, no liberan memoria. ASan no tiene nada que atrapar. No es que
  la etiqueta esté mal: el UB está, pero no deja rastro.
- **Por qué hay casos que «dependen».** Sólo M1 (capacidad) y M6 (factor de
  carga) dependen del estado. Todo lo demás es seguro: o invalida siempre, o
  no invalida nunca.

**Lo que esta tabla no cubre** (fuera de alcance y declarado): `std::string`
(SSO), `swap` y `splice` (el handle cambia de contenedor) y el iterador
`end()`.

## 3. Cuando el fallo depende del estado: la garantía

Éste es el caso difícil: **un uso correcto de algo que puede fallar o no**.

```cpp
std::vector<int> v = …;
v.reserve(v.size() + 1);      // garantiza espacio para una inserción
const int& h = v[0];
v.push_back(7);               // M1 sólo si size()+1 > capacity(): aquí NO
use(h);                       // correcto: el programa lo garantizó
```

```cpp
void f(std::vector<int>& v) {
  const int& h = v[0];
  v.push_back(7);             // M1 si v estaba lleno: nadie lo sabe
  use(h);                     // depende de un estado que el programa no fijó
}
```

Las dos funciones son iguales para la norma: `DependsOn CapacityReached`. Lo
que las distingue es **si el programa estableció una garantía** que hace
falsa la condición. Así se decide:

| En el camino… | Veredicto | Mensaje |
|---|---|---|
| la condición es **verdadera** (`reserve` insuficiente, o un `if` que lo fija) | **confirmado** | «`h` quedó inválido: `push_back` reubica (capacidad agotada)» |
| la condición es **falsa**: hay una garantía | **nada** | — |
| no se sabe: **no hay garantía** | **posible** | «`h` puede quedar inválido si `push_back` reubica; nada garantiza capacidad. Use `reserve` o vuelva a obtener `h`» |

**Por qué el tercero es un fallo, y no una duda.** El programa es correcto
**sólo si** se cumple algo que la norma no promete y que el propio programa
no aseguró. Para alguna entrada válida, el programa tiene comportamiento
indefinido. Es un **defecto latente**: hoy puede andar (la capacidad sobra)
y mañana no (otra entrada, otra biblioteca). La regla CTR51-CPP de SEI CERT
lo trata igual: hay que **usar** referencias, punteros e iteradores **válidos**,
y «puede que sí sea válido» no alcanza.

Se separa del confirmado por honestidad: el confirmado dice «en este camino
falla»; el posible dice «en este camino **puede** fallar, y falta esta
garantía». Los dos tienen arreglo, y el mensaje lo nombra.

### El catálogo de garantías

Un aviso posible es un **falso positivo** si el programa sí tenía la
garantía y el checker no la vio. Por eso las garantías se catalogan igual que
las mutaciones:

| Condición | Garantías que la hacen falsa | Cómo la ve el checker | Incremento |
|---|---|---|---|
| `CapacityReached` (M1) | `reserve(size() + k)` y luego ≤ k inserciones | **crédito** de huecos por contenedor: `reserve` lo fija, cada inserción lo gasta | I4 |
| | `reserve(n)` sobre un vector recién construido vacío, y ≤ n inserciones | igual, con tamaño 0 conocido | I4 |
| | `if (v.size() < v.capacity())` antes de insertar | restricción en el camino sobre `size()` y `capacity()` | después de I4 (requiere modelar esas dos llamadas) |
| `RehashTriggered` (M6) | `reserve(n)` y ≤ n elementos en total | crédito, igual que en vector | I4 |
| `RelationUnknown` (`pop_back` y el primer elemento) | tamaño conocido ≥ 2 | restricción sobre el tamaño | después de I4 |
| `NonBinding` (`shrink_to_fit`) | **ninguna** | — | siempre posible |

**El crédito** es la abstracción mínima: un entero conocido o
`Desconocido`, por contenedor. `reserve(size() + k)` → `k`; cada inserción
resta 1; con crédito > 0 la condición es falsa; con `Desconocido`, no se
sabe. No inventa estado: sólo cuenta lo que el código dijo.

## 4. Las formas de obtener y de usar un handle

P1 y P6 dependen de reconocer **todas** las formas de obtener y de usar. Este
es el catálogo, y cada fila es una prueba `lit`:

| Obtener | Handle | Posición | Incremento |
|---|---|---|---|
| `c.begin()`, `c.cbegin()` | iterador | `First` | I2 |
| `c.end()` | iterador (no es de un elemento) | `PastEnd` | I2 |
| `*it`, `it->m`, `&*it` | elemento | la del iterador | I2 |
| `c.front()`, `c.back()`, `c[i]`, `c.at(i)`, `&c[i]` | elemento | `First`, `Last`, `Offset`/`Unknown` | I2 |
| `c.data()` | puntero al primer elemento | `First` | I3 |
| `c.find(k)`, `lower_bound`, `upper_bound` | iterador | `Unknown` | I3 |
| `it2 = it`, copia al pasar por valor | **el mismo estado** en otra región | la de `it` | I2 |
| **`it = c.erase(it)`, `it = c.insert(it, x)`** | iterador **nuevo y válido** | la del punto | I3 |
| `++it`, `--it`, `it + n`, `std::next` | el mismo iterador, otra posición | `Offset` | I3 |

| Usar | Cuenta como uso |
|---|---|
| `*it`, `it->m`, `*p`, `p->m`, leer o escribir `r` | sí |
| `++it`, `--it`, `it + n` | sí (mover un iterador inválido es UB) |
| `it == c.end()`, `it != it2` | sí |
| copiar el **valor** del elemento (`int x = r;`) | sí: es una carga |
| copiar el **handle** (`auto p2 = p;`) | no: sólo copia la dirección |

**La fila en negrita es la más importante para no dar falsos positivos.** El
idioma correcto para borrar mientras se recorre es
`it = c.erase(it);`: el iterador viejo queda inválido, pero el nuevo es
válido. Si el checker no reconoce que `erase` **devuelve** un handle nuevo,
avisa en el código bien escrito.

## 5. Lo que esto cambia

1. **El banco no mide falsos positivos de verdad.** Sus 246 casos `SAFE` (banco de 684, antes de D-20) eran
   mutaciones que nunca invalidan. No hay ni un caso de **buen uso de algo
   que puede fallar**: `reserve` antes de `push_back`, ni
   `it = c.erase(it)`. Hay que agregarlos (`Guarantee`, abajo), o el checker
   podría avisar en todo `push_back` y salir con precisión perfecta.
2. **`POLICY` tiene métricas propias.** Con casos sin garantía (el aviso
   posible es el acierto) y con garantía (el silencio es el acierto), los
   `POLICY` tienen su propia tabla de 2×2. Eso contesta la `PREGUNTA` de si
   los posibles cuentan: cuentan, **en su propia tabla**.
3. **D-16 cambia.** «Sin modelo de capacidad» daría aviso posible también en
   el código con `reserve`. El crédito de §3 es el mínimo para no hacerlo, y
   entra en I4.
4. **La detección gana tres eventos:** la copia de un handle, la obtención
   que devuelve una mutación (`erase`, `insert`) y la garantía (`reserve`).

### El eje nuevo del banco

```
data Guarantee = NoGuarantee                    // los 75 POLICY del banco de 684; hoy 102
                 OR Reserved                    // reserve(size() + k) antes, ≤ k mutaciones
                 OR ReturnedHandle              // it = c.erase(it) / it = c.insert(it, x)
```

| Casos nuevos | Cuántos | Etiqueta | Mide |
|---|---:|---|---|
| mutaciones `POLICY` de capacidad o rehash, con `Reserved`, 3 categorías × 3 formas (recto, guarda, llamada) | ≈ 60 | `SAFE` | que una garantía silencie el aviso posible |
| `erase` / `insert` con `ReturnedHandle`, en `bucle` | ≈ 20 | `SAFE` | que el idioma correcto no se marque |

(El conteo exacto sale de la matriz al generar.)

## 6. Resumen: lo que falta saber y lo que ya se sabe

| Pregunta | Respuesta | Dónde |
|---|---|---|
| ¿Qué demuestra un aviso? | un camino factible donde valen P1…P6 | §1 |
| ¿De dónde sale cada fallo? | seis mecanismos de memoria, cada fila de la norma cae en uno | §2 |
| ¿Cómo se marca «puede fallar»? | posible, nombrando la garantía que falta; confirmado si en el camino la condición es verdadera | §3 |
| ¿Cómo no se marca el buen uso? | catálogo de garantías + `erase` que devuelve un handle | §3, §4 |
| ¿Está todo el catálogo? | mutaciones: sí (57). Obtenciones y usos: sí (§4). Garantías: las cuatro de §3. Alias del contenedor: lo resuelve la región de CSA (prueba `lit` en I2) | — |
| ¿El banco mide todo eso? | **no**: faltan los casos de buen uso (§5) | Evaluación |
