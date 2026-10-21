# Trabajos relacionados y aporte

Esta página responde **qué hace este trabajo que otros no hacen**. Cada
afirmación sobre otra herramienta sale de su documentación, su código o su
artículo (referencias al final). Cada afirmación sobre la nuestra sale del
experimento ([Experimento](../resultados/experimento.md)) o del código.

> **Sobre la palabra «disruptivo».** En el artículo no conviene usarla: un
> revisor la acepta sólo ante una ruptura demostrada, y lo que hay aquí es un
> aporte **preciso y medible** dentro de un problema que otros ya atacan. La
> fórmula honesta es: *«a diferencia de X, que …, el checker …; en el banco,
> esto se traduce en …»*. Esa forma convence más que un adjetivo.

## 1. El problema ya tiene herramientas

La invalidación de handles (iteradores, referencias y punteros a elementos)
está descrita en la norma (cláusulas `[*.modifiers]` de C++17) y en la regla
CTR51-CPP del SEI CERT (Software Engineering Institute, 2024). La atacan cuatro
familias de herramientas:

| Familia | Herramienta | Técnica | Handles | Contenedores | Qué hace con lo que depende del estado (capacidad, *rehash*) |
|---|---|---|---|---|---|
| Ejecución simbólica | CSA `alpha.cplusplus.InvalidatedIterator` (Balogh, 2018; LLVM Project, 2026a) | caminos simbólicos, modelo de contenedor e iterador | **sólo iteradores** | los de la STL que modela `ContainerModeling` | no lo distingue; en nuestro banco: 0 avisos en los 102 `POLICY` |
| | CSA `cplusplus.InnerPointer` (LLVM Project, 2026a) | caminos simbólicos | punteros internos | **sólo `std::string`** | — |
| Flujo de datos / *lifetimes* | Clang *Lifetime Safety*, `-Wlifetime-safety-invalidation` (Saxena, 2026) | flujo de datos intraprocedural sobre préstamos (*loans*) | referencias e iteradores | `vector`, `deque`, `string`, `set`/`map` y variantes; **no** `list` | **invalida siempre**: la lista de métodos es por nombre y no modela capacidad ni posición; `int& r = v[0]; v.push_back(4)` todavía **no** se detecta (FIXME de las pruebas) |
| | Perfil *Lifetime* de C++ (Sutter, 2019) | reglas locales de dueño y puntero | punteros, referencias, iteradores | genérico | conservador: una operación no `const` sobre el dueño invalida |
| | Rust, verificador de préstamos (Klabnik y Nichols, 2023) | tipos: «compartido o mutable, no ambos» | referencias | todos | **rechaza** mutar mientras hay préstamo, aunque `reserve` lo hiciera seguro |
| Análisis interprocedural | Infer/Pulse `VECTOR_INVALIDATION` (Meta, 2026) | análisis de memoria interprocedural (Pulse) | direcciones dentro del contenedor | **sólo `std::vector`** (y `PULSE_REFERENCE_STABILITY` para mapas F14 de *folly*) | `push_back`, `reserve`, `shrink_to_fit`… están en la lista de operaciones que invalidan |
| Interpretación abstracta | IKOS4VecErr (Liu et al., 2025) | interpretación abstracta sobre IKOS: tamaño e iteradores | iteradores | **sólo `std::vector`** | modela el tamaño; 503 de 505 defectos en su banco hecho a mano |
| Patrones y consultas | cppcheck `invalidContainer` (Cppcheck team, 2026) | *value flow* sobre tokens | iteradores, referencias, punteros | por clase de contenedor: dos banderas, `unstableInsert` y `unstableErase` | no hay capacidad; `push_back` en `vector` siempre invalida |
| | CodeQL *Itergator* (Higgs, 2020) | flujo de datos global, condiciones necesarias pero no suficientes | iteradores | STL y tipos extendibles | no modela capacidad; el autor admite «un número significativo de falsos positivos» |
| | PVS-Studio V789 (PVS-Studio, s. f.) | patrón | iteradores del `for` por rango | — | — |
| Dinámicas | libstdc++ *Debug Mode*, AddressSanitizer (LLVM Project, s. f.) | instrumentación | iteradores (Debug); memoria (ASan) | todos | sólo ven **lo que ocurrió** en esa ejecución |

Notas de lectura:

- Clang *Lifetime Safety* es posterior a LLVM 21 (se integró en la rama
  principal el 6 de febrero de 2026, PR #179093). Es el trabajo más cercano y
  el más reciente: confirma que el problema importa **hoy** a la comunidad de
  Clang. Su enfoque es el opuesto al nuestro en un punto clave: **cualquier**
  método de la lista invalida a todos los préstamos del contenedor.
- IKOS4VecErr (ICFEM 2025) es el antecedente académico más cercano. Se compara
  con CSA, Infer, cppcheck e IKOS, pero sólo cubre `std::vector`.
- Ninguna de las fuentes revisadas publica una evaluación con **etiquetas
  derivadas de la norma**, **validación dinámica de esas etiquetas** y
  **cotejo por sitio** del aviso.

## 2. Qué hace este trabajo que los otros no

Cinco diferencias. Cada una con lo que dicen las fuentes y con la evidencia
propia.

### A1. La regla es la de la norma, por contenedor, categoría y posición

**Los otros.** Listas de métodos «que invalidan» (Clang *Lifetime Safety*,
Infer) o dos banderas por clase de contenedor (cppcheck). `map::insert` o
`list::push_back`, que en C++ **no** invalidan nada, quedan del lado de la
lista o del lado de la excepción según la herramienta, y la posición del
elemento no cuenta.

**Nosotros.** La norma está escrita **como datos** (`norma/matriz.json`: 101
mutaciones, 348 reglas, cada una con su cláusula). El efecto se consulta con la
tupla (contenedor, operación, punto) × categoría × **relación del elemento con
el punto** (antes, mismo, después). Así, `vector::erase` invalida desde el
punto hacia adelante y conserva lo anterior, y `deque::push_front` invalida los
iteradores pero conserva las referencias. De la misma tabla se generan el
código C++ (`NormTable.inc`) y las etiquetas del banco.

**Evidencia.** 0 falsos positivos en los 306 casos `SAFE`, que incluyen
mutaciones que en otras herramientas cuentan como invalidantes. Corregir una
regla es editar una línea con su cláusula; `gen_tabla.py` rechaza la norma si
rompe una ley (RF-17).

### A2. Referencias y punteros a elementos, en diez contenedores

**Los otros.** CSA sigue sólo iteradores; `InnerPointer` sólo `std::string`.
Infer e IKOS4VecErr, sólo `std::vector`. Clang *Lifetime Safety* aún no
detecta `int& r = v[0]; v.push_back(4);`.

**Nosotros.** Un handle es un iterador, una referencia o un puntero obtenido
con `begin()`, `find()`, `*it`, `c[i]`, `front()`, `insert().first`… en
`vector`, `deque`, `list`, `forward_list`, `set`, `multiset`, `map`,
`multimap`, `unordered_set` y `unordered_map`.

**Evidencia.** Sobre el handle que cada caso sostiene, CSA solo detecta 48 de
128 iteradores y **0 de 200** referencias y punteros. Con el checker: 128/128 y
200/200 (328/328 en total; 342/342 UB por caso).

### A3. Tres veredictos: confirmado, posible y nada, y el posible dice qué falta

**Los otros.** Ante `push_back` sin saber la capacidad hay dos salidas: avisar
siempre (Clang *Lifetime Safety*, Infer, cppcheck, el perfil *Lifetime*; Rust
directamente rechaza el programa) o no avisar nunca (CSA).

**Nosotros.** La validez es un semirretículo `Válido ⊑ No resuelto ⊑
Inválido`. Lo que depende del estado queda **No resuelto, con su razón**
(`DependsOnState(CapacityReached)`), y una opción (`PolicyMode`) decide si da
aviso **posible**, que nombra la garantía que falta («use `reserve(size() + n)`
antes»). El checker además **reconoce las garantías** que el propio código da:
`reserve(size() + k)` concede `k` inserciones sin reubicar y `it = c.erase(it)`
devuelve un handle nuevo y válido.

**Evidencia.** 102/102 `POLICY` con aviso posible en `Possibly`, 0/102 en
`Silent`; **0 avisos en los 54 casos con `reserve`** y en los 12 con handle
devuelto. Las herramientas que invalidan siempre avisarían en esos 66 casos
de buen uso. Esto se deduce de su documentación; **no** se midió (ver §3).

### A4. Una evaluación que se puede auditar

**Los otros.** Bancos hechos a mano (IKOS4VecErr: 505 defectos), ejemplos
anecdóticos en código real (*Itergator*) o sólo pruebas unitarias (Clang,
cppcheck).

**Nosotros.** El banco (750 casos: 342 `UB`, 306 `SAFE`, 102 `POLICY`) sale de
la misma norma, con una etiqueta por caso que es el JOIN de los handles que
usa. Las etiquetas se contrastan con **dos oráculos dinámicos independientes**
(libstdc++ *Debug Mode* y ASan/UBSan: 852 ejecuciones, 0 contradicciones). El
arnés corre cuatro condiciones, **atribuye cada aviso a su sitio** (no basta
«hubo un aviso en la función») y separa los incidentes (caída, tiempo agotado)
de los verdaderos negativos. El banco está sellado (`banco-1`, sha256) y el CI
falla si una métrica retrocede.

**Evidencia.** 3 000 ejecuciones, 0 incidentes, cifras reproducibles con
`docker compose run --rm experimento`.

### A5. Un plugin de CSA, no un analizador nuevo

**Los otros.** IKOS4VecErr modifica IKOS; *Itergator* exige CodeQL; Infer es
otro motor.

**Nosotros.** Un `.so` que se carga en el `clang` instalado
(`-Xclang -load`), sin parchear LLVM. Reutiliza la ejecución simbólica, el
*inlining* y el formato SARIF de CSA, y deja el modelo en un núcleo puro (sin
Clang) probado por leyes: 40 pruebas, 92.5 % de líneas cubiertas.

**Evidencia.** 781 unidades de cuatro proyectos reales (ninja, leveldb,
yaml-cpp, RocksDB) sin una caída de `clang` y sin avisos confirmados falsos.
Los 8 defectos sembrados y los 2 casos de buen uso sembrados dieron lo esperado.

## 3. Lo que NO se puede afirmar (amenazas a la validez)

Un revisor lo preguntará. Mejor decirlo antes:

1. **Circularidad.** El checker y las etiquetas salen de la misma norma, así
   que el 100 % del banco mide **fidelidad de la implementación a la norma**,
   no que la norma esté bien escrita. Lo mitigan los dos oráculos dinámicos
   (0 contradicciones), las 27 etiquetas que se corrigieron cuando hubo
   contradicción (D-18) y el código real con defectos sembrados.
2. **No se ejecutaron las otras herramientas sobre el banco.** La tabla de §1
   compara capacidades **documentadas**. Correr cppcheck, Infer y Clang
   *Lifetime Safety* sobre los 750 casos convertiría A1 y A3 en cifras. Es el
   trabajo pendiente más valioso para el artículo.
3. **Alcance.** C++17, diez contenedores, sin `std::string`; libstdc++ 13;
   análisis dentro de la unidad de traducción (el *inlining* de CSA, sin
   análisis entre unidades).
4. **Banco sintético.** Formas acotadas (`recto`, `guarda`, `llamada`,
   `bucle`). El código real muestra ausencia de caídas y de falsos positivos
   confirmados, no exhaustividad.

## 4. Frase de aporte para el artículo (borrador)

> Presentamos un checker para Clang Static Analyzer que modela la invalidación
> de iteradores, referencias y punteros en diez contenedores de la biblioteca
> estándar a partir de las reglas de C++17 escritas como datos, con su
> cláusula. A diferencia de los enfoques que tratan una lista de operaciones
> como siempre invalidantes, el checker aplica la regla según el contenedor,
> la categoría del handle y la posición del elemento; distingue lo que depende
> del estado del programa con un aviso posible que nombra la garantía que
> falta, y reconoce las garantías que el código da. En un banco de 750 casos
> derivado de la norma y validado dinámicamente, el checker detecta 342 de 342
> usos inválidos sin falsos positivos, frente a 80 de 342 de la configuración
> de referencia de CSA, que no detecta ninguno sobre referencias o punteros.

## Referencias (APA 7)

- Balogh, Á. (2018). *Finding iterator-related errors with the Clang Static Analyzer* [Presentación]. EuroLLVM 2018, Bristol, Reino Unido. https://llvm.org/devmtg/2018-04/slides/Balogh-Finding%20Iterator-related%20Errors%20with%20Clang%20Static%20Analyzer.pdf
- Cppcheck team. (2026). *lib/checkstl.cpp: `CheckStl::invalidContainer`* [Código fuente]. GitHub. https://github.com/danmar/cppcheck/blob/main/lib/checkstl.cpp
- Higgs, K. (2020, 9 de octubre). *Detecting iterator invalidation with CodeQL* [Entrada de blog]. Trail of Bits Blog. https://blog.trailofbits.com/2020/10/09/detecting-iterator-invalidation-with-codeql/
- Klabnik, S. y Nichols, C. (2023). *The Rust programming language* (2.ª ed.). No Starch Press.
- Liu, S., Chen, L., Fan, G., Yin, B., Huang, C. y Wang, J. (2025). Detecting vector container errors in C++ programs via abstract interpretation. En *Formal Methods and Software Engineering (ICFEM 2025)*, Lecture Notes in Computer Science (Vol. 16229, pp. 117–133). Springer Nature Singapore. https://doi.org/10.1007/978-981-95-4213-0_7
- LLVM Project. (2026a). *Available checkers — Clang Static Analyzer documentation*. https://clang.llvm.org/docs/analyzer/checkers.html
- LLVM Project. (s. f.). *AddressSanitizer*. Clang documentation. https://clang.llvm.org/docs/AddressSanitizer.html
- Meta. (2026). *List of all issue types: VECTOR_INVALIDATION*. Infer documentation. https://fbinfer.com/docs/all-issue-types/
- PVS-Studio. (s. f.). *V789. Iterators for the container, used in the range-based for loop, become invalid upon a function call*. https://pvs-studio.com/en/docs/warnings/v789/
- Saxena, U. (2026, 6 de febrero). *[LifetimeSafety] Detect use-after-invalidation for STL containers* (Pull request #179093). llvm/llvm-project, GitHub. https://github.com/llvm/llvm-project/pull/179093
- Software Engineering Institute. (2024). *CTR51-CPP. Use valid references, pointers, and iterators to reference elements of a container*. SEI CERT C++ Coding Standard. https://wiki.sei.cmu.edu/confluence/display/cplusplus/CTR51-CPP
- Sutter, H. (2019). *Lifetime safety: Preventing common dangling* (P1179R1). ISO/IEC JTC1/SC22/WG21. https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1179r1.pdf
