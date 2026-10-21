# Dónde se valida cada requerimiento

Cada requerimiento del [capítulo 4](../diseno/cap4/index.md) está en una
parte del código y se demuestra con una prueba que se puede correr. Esta
página muestra las dos cosas, con el código tal como está hoy en el
repositorio: los fragmentos se copian del código fuente cada vez que se
genera el libro.

Todos se comprueban juntos con:

```bash
docker compose run --rm verificar
```

## Tres tipos de prueba

| Tipo | Dónde | Qué prueba | Cómo se corre |
|---|---|---|---|
| **gtest** (C++) | `plugin/tests/dominio/LeyesTest.cpp` | el núcleo puro: la norma, las posiciones, la validez, las garantías. 40 pruebas | `./build/plugin/dominio_tests` |
| **lit** (C++ dentro de `clang`) | `plugin/tests/lit/*.cpp` | el checker de verdad, cargado en `clang`: cada `// expected-warning {{…}}` dice el aviso exacto que debe salir en esa línea, y una línea sin comentario no debe dar aviso (`-verify`). 5 archivos, 30 avisos | `lit build/plugin/tests/lit` |
| **arnés** (Python) | `bench/` | lo que no es un caso suelto sino una **medición**: correr el banco de 750 casos, contar aciertos, comparar con CSA solo, medir tiempo y memoria | `python3 bench/experimento.py` y los scripts de abajo |

Los requerimientos de lo que hace el checker (RF-01 a RF-12, RF-17) se
demuestran con gtest y `lit`. Los de la evaluación y la calidad medida (RF-13
a RF-15, RNF-01 a RNF-05) no se pueden escribir como un test de un caso: se
demuestran midiendo, con el arnés.

## Resumen

| Requerimiento | Se implementa en | Se demuestra con |
|---|---|---|
| [RF-01](#rf-01-registrar-el-checker) | `plugin/registro/Plugin.cpp` | `lit` `registro.cpp` |
| [RF-02](#rf-02-activar-y-desactivar-el-checker) | `bench/experimento.py` `Condicion` | experimento: las condiciones difieren solo en el checker |
| [RF-03](#rf-03-analizar-un-proyecto-desde-su-base-de-compilación) | `bench/codigo_real.py` `analizar` | `ejemplos/` en `verificar`; los 4 proyectos reales |
| [RF-04](#rf-04-elegir-la-política-ante-lo-que-depende-del-estado) | `Plugin.cpp` `registerInvalidation`, `Decisions.cpp` `onUse` | gtest `NoResueltoNuncaSeInformaComoConfirmado`; `lit` `garantias.cpp` |
| [RF-05](#rf-05-seguir-iteradores) | `acl/ClangRecognizer.cpp`, `checker/InvalidationChecker.cpp` | `lit` `iteradores.cpp` |
| [RF-06](#rf-06-seguir-referencias-y-punteros-a-elementos) | `ClangRecognizer.cpp` `elementAccess`, `InvalidationChecker::checkLocation` | `lit` `referencias.cpp` |
| [RF-07](#rf-07-no-avisar-en-los-usos-válidos) | `Decisions.cpp` `onUse` | gtest `LoValidoNoSeReporta`; `lit`; `ejemplos/buen_uso.cpp` |
| [RF-08](#rf-08-aplicar-la-regla-de-c17) | `NormTable.cpp` `effectOf`, `Decisions.cpp` `apply` | gtest `Banco.ElVeredictoDelNucleoEsLaEtiqueta` |
| [RF-09](#rf-09-tratar-lo-que-depende-del-estado) | `Decisions.cpp` `answer`, `consume`; `ClangRecognizer.cpp` `sizePlus` | gtest `ConGarantiaDependerEsPreservar`; `lit` `garantias.cpp` |
| [RF-10](#rf-10-tratar-las-llamadas-opacas) | `Decisions.cpp` `escape`, `InvalidationChecker::checkRegionChanges` | gtest `EscaparOlvidaLoQueNoEstaInvalidado`; `lit` `garantias.cpp` |
| [RF-11](#rf-11-explicar-la-causa-en-el-aviso) | `checker/Messages.cpp` | el texto de cada `expected-warning` |
| [RF-12](#rf-12-mostrar-la-ruta-del-defecto) | `InvalidationChecker.cpp` `transition` | `lit` `rutas.cpp` |
| [RF-13](#rf-13-ejecutar-el-experimento) | `bench/experimento.py` `ejecutar` | el experimento (muestra en `verificar`) |
| [RF-14](#rf-14-cotejar-por-sitio) | `experimento.py` `atribuir`, `cotejar` | `bench/pruebas_evaluacion.py` |
| [RF-15](#rf-15-generar-y-validar-el-banco) | `bench/gen_corpus.py`, `bench/run_runtime_validation.py` | sello `banco-1.json`; validación dinámica |
| [RF-16](#rf-16-construir-y-verificar-el-plugin) | `plugin/CMakeLists.txt` | el build y sus pruebas |
| [RF-17](#rf-17-mantener-la-norma-como-datos) | `norma/matriz.json`, `norma/gen_tabla.py` | `gen_tabla.py` al construir; gtests `Norma.*` |
| [RNF-01 a RNF-03](#rnf-01-a-rnf-03-precisión-cobertura-y-robustez) | todo el checker | `bench/regresion.py` sobre el experimento |
| [RNF-04 y RNF-05](#rnf-04-y-rnf-05-tiempo-y-memoria) | — | `bench/rendimiento.py` |
| [RNF-06](#rnf-06-claridad-del-diagnóstico) | `checker/Messages.cpp` | gtest `CadaRazonDeNoResueltoDiceQueFalta`; `lit` |
| [RNF-07](#rnf-07-mantenibilidad) | `plugin/CMakeLists.txt` | el núcleo compila sin Clang |
| [RNF-08](#rnf-08-reproducibilidad) | `experimento.py` `verificar` | `meta` de `metricas.json` |
| [RN-001 a RN-007](#reglas-de-negocio) | `bench/etiquetar.py`, `bench/experimento.py` | `bench/pruebas_evaluacion.py` |

---

## Requerimientos funcionales

### RF-01 Registrar el checker

El plugin se carga en `clang` y aparece en el catálogo de CSA como
`ucsm.ContainerInvalidation`, con sus opciones `PolicyMode` y `Debug`.

**Se implementa en:**

[`plugin/registro/Plugin.cpp:30`](https://github.com/jasrod12ucsm/checker/blob/main/plugin/registro/Plugin.cpp#L30-L41)

```cpp
extern "C" void clang_registerCheckers(CheckerRegistry &Registry) {
  Registry.addChecker(registerInvalidation, shouldRegister, "ucsm.ContainerInvalidation",
                      "Uso de iteradores, referencias o punteros a elementos de "
                      "contenedores de la STL después de una mutación que los invalida",
                      "", /*IsHidden=*/false);
  Registry.addCheckerOption("string", "ucsm.ContainerInvalidation", "PolicyMode", "Silent",
                            "Silent: sólo avisos confirmados. Possibly: también avisos "
                            "posibles cuando la invalidación depende del estado.",
                            "released");
  Registry.addCheckerOption("bool", "ucsm.ContainerInvalidation", "Debug", "false",
                            "Escribe en stderr cada obtención, mutación, uso y escape.", "released");
}
```

**Se demuestra con** la prueba `lit` `registro.cpp`, que pide a `clang` la
lista de checkers y de opciones y busca el nombre con `FileCheck`:

[`plugin/tests/lit/registro.cpp:1`](https://github.com/jasrod12ucsm/checker/blob/main/plugin/tests/lit/registro.cpp#L1-L5)

```cpp
// CU-05: el plugin carga y registra el checker con su opción.
// RUN: %clang -cc1 -load %plugin -analyzer-checker-help | FileCheck %s --check-prefix=HELP
// RUN: %clang -cc1 -load %plugin -analyzer-checker-option-help | FileCheck %s --check-prefix=OPT
// HELP: ucsm.ContainerInvalidation
// OPT: ucsm.ContainerInvalidation:PolicyMode
```

### RF-02 Activar y desactivar el checker

El checker se activa con `-analyzer-checker` y se carga con `-load`, sin
recompilar `clang`. En el experimento, las condiciones con y sin checker
**solo** difieren en esas opciones (RN-002):

[`bench/experimento.py:59`](https://github.com/jasrod12ucsm/checker/blob/main/bench/experimento.py#L59-L76)

```python
class Condicion:
    nombre: str                    # Reference | Experimental-Silent | Experimental-Possibly | Plugin-Possibly
    modo: str | None = None        # PolicyMode del plugin; None = sin plugin
    sin_alpha: bool = False        # quita alpha.cplusplus.* de base

    def argumentos(self) -> list[str]:
        checkers, opciones, carga = list(BASE_CHECKERS), list(BASE_OPCIONES), []
        if self.sin_alpha:
            checkers = [c for c in checkers if not c.startswith("alpha.")]
        if self.modo:
            carga = ["-Xclang", "-load", "-Xclang", str(PLUGIN)]
            checkers.append(NUESTRO)
            opciones.append(f"{NUESTRO}:PolicyMode={self.modo}")
        args = ["clang++", "--analyze", "--analyzer-output", "sarif", "-std=c++17", *carga,
                "-Xclang", f"-analyzer-checker={','.join(checkers)}"]
        for o in opciones:
            args += ["-Xclang", "-analyzer-config", "-Xclang", o]
        return args
```

**Se demuestra con** el experimento: `metricas.json` guarda en
`meta.condiciones` la línea de órdenes de cada condición, y las cuatro
condiciones corren sobre el mismo banco con el mismo `clang`. En `verificar`,
el paso del experimento lo hace sobre una muestra.

### RF-03 Analizar un proyecto desde su base de compilación

Para cada entrada de `compile_commands.json`, una invocación de `clang` con
las mismas opciones del proyecto más el checker:

[`bench/codigo_real.py:50`](https://github.com/jasrod12ucsm/checker/blob/main/bench/codigo_real.py#L50-L95)

```python
def analizar(entrada: dict, modo: str, inlining: str = "noredundancy") -> dict:
    args = entrada.get("arguments") or shlex.split(entrada["command"])
    archivo = entrada["file"]
    if not archivo.endswith((".cc", ".cpp", ".cxx")):
        return {"file": archivo, "omitido": True}
    # Quitar el compilador, -o y -c; agregar el análisis.
    resto, saltar = [], False
    for a in args[1:]:
        if saltar:
            saltar = False
            continue
        if a in ("-o", "-c"):
            saltar = a == "-o"
            continue
        if a == archivo or a.endswith(Path(archivo).name) and not a.startswith("-"):
            continue
        resto.append(a)
    # Sin color: la salida se interpreta con una expresión regular.
    resto = [a for a in resto if not a.startswith("-fdiagnostics-color") and a != "-fcolor-diagnostics"]
    cmd = ["clang++", *resto, "-fno-color-diagnostics", "--analyze", "-o", "/dev/null",
           "-Xclang", "-load", "-Xclang", str(PLUGIN),
           "-Xclang", "-analyzer-checker=ucsm.ContainerInvalidation",
           "-Xclang", "-analyzer-config", "-Xclang", f"ucsm.ContainerInvalidation:PolicyMode={modo}",
           "-Xclang", "-analyzer-output=text",
           # noredundancy (por defecto en CSA) no vuelve a analizar como raíz una
           # función ya inlinada: si el presupuesto cortó ese camino, no se ve.
           "-Xclang", f"-analyzer-inlining-mode={inlining}", archivo]
    t0 = time.time()
    p = subprocess.run(cmd, cwd=entrada["directory"], capture_output=True, text=True, timeout=900)
    avisos: list[dict] = []
    actual: dict | None = None
    for linea in p.stderr.splitlines():
        m = AVISO.match(linea)
        if not m:
            continue
        if m["kind"] == "warning" and m["chk"] == "ucsm.ContainerInvalidation":
            nuevo: dict = {"file": m["file"], "line": int(m["line"]), "msg": m["msg"],
                           "clase": "posible" if "posiblemente" in m["msg"] else "confirmado", "ruta": []}
            avisos.append(nuevo)
            actual = nuevo
        elif m["kind"] == "warning":
            actual = None
        elif actual is not None:
            actual["ruta"].append(f'{m["file"]}:{m["line"]}: {m["msg"]}')
    return {"file": archivo, "segundos": round(time.time() - t0, 2), "codigo": p.returncode,
            "error": p.stderr[-2000:] if p.returncode else "", "avisos": avisos}
```

**Se demuestra con** `ejemplos/`, un proyecto CMake de dos archivos que
`verificar` analiza así. Debe dar un aviso confirmado y uno posible en
`prueba.cpp`, y ninguno en `buen_uso.cpp`:

```bash
python3 bench/codigo_real.py . build/verificacion/ejemplos.json Possibly noredundancy ejemplos
# ejemplos: 2 TU, 2 avisos, 0 TU con error, 0.5 s
```

A escala, con los cuatro proyectos reales (781 unidades): ver
[Correr los bench](bench.md#código-real).

### RF-04 Elegir la política ante lo que depende del estado

`PolicyMode=Silent` (por omisión) solo da avisos confirmados;
`PolicyMode=Possibly` da también los posibles. La opción se lee al registrar
el checker:

[`plugin/registro/Plugin.cpp:18`](https://github.com/jasrod12ucsm/checker/blob/main/plugin/registro/Plugin.cpp#L18-L24)

```cpp
void registerInvalidation(CheckerManager &Mgr) {
  auto *Chk = Mgr.registerChecker<ucsm::InvalidationChecker>();
  StringRef Mode = Mgr.getAnalyzerOptions().getCheckerStringOption(Chk, "PolicyMode");
  Chk->setPolicyMode(Mode == "Possibly" ? ucsm::dominio::PolicyMode::Possibly
                                        : ucsm::dominio::PolicyMode::Silent);
  Chk->setDebug(Mgr.getAnalyzerOptions().getCheckerBooleanOption(Chk, "Debug"));
}
```

y decide el veredicto al usar un handle no resuelto:

[`plugin/dominio/Decisions.cpp:127`](https://github.com/jasrod12ucsm/checker/blob/main/plugin/dominio/Decisions.cpp#L127-L141)

```cpp
UseResult onUse(const HandleState &H, HandleCategory At, PolicyMode Mode) {
  const Validity &V = H.validity();
  switch (V.kind()) {
  case ValidityKind::Valid:
  case ValidityKind::UnresolvedDiagnosed:
  case ValidityKind::Diagnosed: return {{VerdictKind::Fine, At, V, MissingGuarantee::None}, H};
  case ValidityKind::Unresolved:
    if (Mode == PolicyMode::Silent)
      return {{VerdictKind::Fine, At, V, MissingGuarantee::None}, H};
    return {{VerdictKind::Possibly, At, V, missingFor(V)}, H.withValidity(V.diagnosed())};
  case ValidityKind::Invalidated:
    return {{VerdictKind::Confirmed, At, V, MissingGuarantee::None}, H.withValidity(V.diagnosed())};
  }
  return {{VerdictKind::Fine, At, V, MissingGuarantee::None}, H};
}
```

**Se demuestra con** el gtest:

[`plugin/tests/dominio/LeyesTest.cpp:327`](https://github.com/jasrod12ucsm/checker/blob/main/plugin/tests/dominio/LeyesTest.cpp#L327-L336)

```cpp
TEST(Deteccion, NoResueltoNuncaSeInformaComoConfirmado) {
  Mutation M{ContainerKind::Vector, Operation::PushBack, Point::Back};
  HandleState H =
      handle(HandleKind::Element, Position::first(0))
          .withValidity(Validity::dependsOn(Condition::CapacityReached, event(M, Position::pastEnd())));
  EXPECT_EQ(onUse(H, HandleCategory::Reference, PolicyMode::Possibly).Verdict.Kind, VerdictKind::Possibly);
  EXPECT_EQ(onUse(H, HandleCategory::Reference, PolicyMode::Possibly).Verdict.Missing,
            MissingGuarantee::ReserveBefore);
  EXPECT_EQ(onUse(H, HandleCategory::Reference, PolicyMode::Silent).Verdict.Kind, VerdictKind::Fine);
}
```

y con `lit` `garantias.cpp`, que corre con `PolicyMode=Possibly` (`%possibly`
en su línea `RUN`):

[`plugin/tests/lit/garantias.cpp:8`](https://github.com/jasrod12ucsm/checker/blob/main/plugin/tests/lit/garantias.cpp#L8-L12)

```cpp
void no_guarantee(std::vector<int> &c) {
  const int &h = c[0];
  c.push_back(1);
  sink(h); // expected-warning {{Uso de una referencia posiblemente invalidada: 'std::vector::push_back' (línea 10) si la capacidad está agotada reubica los elementos; nada garantiza espacio}}
}
```

### RF-05 Seguir iteradores

El checker registra un iterador al obtenerlo (`begin()`, `find()`,
`insert().first`…) y lo vigila al desreferenciarlo, moverlo o compararlo.

[`plugin/acl/ClangRecognizer.cpp:219`](https://github.com/jasrod12ucsm/checker/blob/main/plugin/acl/ClangRecognizer.cpp#L219-L225)

```cpp
std::optional<Position> iteratorObtention(const ContainerCall &CC, const CallEvent &Call) {
  if (CC.Method == "begin" || CC.Method == "cbegin")
    return Position::first(0);
  if (CC.Method == "find" || CC.Method == "lower_bound" || CC.Method == "upper_bound")
    return Position::unknown();
  return std::nullopt; // end() queda fuera del alcance (norma.md §7)
}
```

[`plugin/checker/InvalidationChecker.cpp:165`](https://github.com/jasrod12ucsm/checker/blob/main/plugin/checker/InvalidationChecker.cpp#L165-L188)

```cpp
ProgramStateRef InvalidationChecker::use(ProgramStateRef St, const MemRegion *R, bool IsIterator,
                                         HandleCategory At, const Stmt *S, CheckerContext &C) const {
  const Stored *H = IsIterator ? St->get<IteratorMap>(R) : St->get<ElementMap>(R);
  if (!H)
    return nullptr;
  trace(C, S, "uso", R);
  UseResult U = onUse(H->S, At, Mode);
  if (U.Verdict.Kind == VerdictKind::Fine)
    return nullptr;
  St = IsIterator ? St->set<IteratorMap>(R, Stored{U.State}) : St->set<ElementMap>(R, Stored{U.State});
  ExplodedNode *N = C.generateNonFatalErrorNode(St);
  if (!N)
    return nullptr;
  unsigned Line = lineOf(U.Verdict.Why.at(), C);
  bool Sure = U.Verdict.Kind == VerdictKind::Confirmed;
  auto Report = std::make_unique<PathSensitiveBugReport>(
      Sure ? Confirmed : Possible,
      Sure ? messages::confirmed(U.Verdict, Line) : messages::possibly(U.Verdict, Line), N);
  Report->markInteresting(R);
  if (S)
    Report->addRange(S->getSourceRange());
  C.emitReport(std::move(Report));
  return St;
}
```

**Se demuestra con** `lit` `iteradores.cpp`:

[`plugin/tests/lit/iteradores.cpp:14`](https://github.com/jasrod12ucsm/checker/blob/main/plugin/tests/lit/iteradores.cpp#L14-L18)

```cpp
void vector_iter_deref(std::vector<int> &c) {
  auto it = c.begin();
  c.insert(c.begin(), 1);
  sink(*it); // expected-warning {{Uso de un iterador invalidado: 'std::vector::insert'}}
}
```

[`plugin/tests/lit/iteradores.cpp:27`](https://github.com/jasrod12ucsm/checker/blob/main/plugin/tests/lit/iteradores.cpp#L27-L33)

```cpp
void copy_carries_state(std::list<int> &c) {
  auto it = c.begin();
  if (it == c.end()) return;
  auto it2 = it;
  c.erase(c.begin());
  sink(*it2); // expected-warning {{Uso de un iterador invalidado}}
}
```

### RF-06 Seguir referencias y punteros a elementos

Una referencia o un puntero a un elemento se registra al obtenerlo (`*it`,
`&*it`, `c[i]`, `front()`) y se vigila cuando se lee la memoria del elemento:

[`plugin/acl/ClangRecognizer.cpp:227`](https://github.com/jasrod12ucsm/checker/blob/main/plugin/acl/ClangRecognizer.cpp#L227-L241)

```cpp
std::optional<Position> elementAccess(const ContainerCall &CC, const CallEvent &Call, CheckerContext &C) {
  if (CC.Method == "front" || CC.Method == "data")
    return Position::first(0);
  if (CC.Method == "back")
    return Position::last(0);
  if (CC.Method == "operator[]" || CC.Method == "at") {
    if (!isSequence(CC.Kind) && CC.Kind != ContainerKind::Vector)
      return Position::unknown(); // map[k]: elemento por clave
    if (Call.getNumArgs() == 1)
      if (auto K = smallConstantOf(Call.getArgExpr(0), C))
        return Position::first(*K);
    return Position::unknown();
  }
  return std::nullopt;
}
```

[`plugin/checker/InvalidationChecker.cpp:343`](https://github.com/jasrod12ucsm/checker/blob/main/plugin/checker/InvalidationChecker.cpp#L343-L350)

```cpp
void InvalidationChecker::checkLocation(SVal Loc, bool IsLoad, const Stmt *S, CheckerContext &C) const {
  const MemRegion *R = Loc.getAsRegion();
  if (!R)
    return;
  R = R->getBaseRegion(); // h.second, h->second: subregiones del elemento
  if (ProgramStateRef N = use(C.getState(), R, false, acl::categoryAtLoad(S), S, C))
    (void)N;
}
```

**Se demuestra con** `lit` `referencias.cpp`. CSA solo no detecta ninguno de
estos:

[`plugin/tests/lit/referencias.cpp:10`](https://github.com/jasrod12ucsm/checker/blob/main/plugin/tests/lit/referencias.cpp#L10-L15)

```cpp
void vector_erase_ref(std::vector<int> &c) {
  auto it = c.begin();
  const int &h = *it;
  c.erase(c.begin());
  sink(h); // expected-warning {{Uso de una referencia invalidada: 'std::vector::erase' (línea 13) lo invalidó}}
}
```

[`plugin/tests/lit/referencias.cpp:17`](https://github.com/jasrod12ucsm/checker/blob/main/plugin/tests/lit/referencias.cpp#L17-L23)

```cpp
void vector_clear_ptr(std::vector<int> &c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const int *h = &*it;
  c.clear();
  sink(*h); // expected-warning {{Uso de un puntero invalidado}}
}
```

### RF-07 No avisar en los usos válidos

Un handle válido no produce aviso en ningún modo (primera línea de `onUse`,
en [RF-04](#rf-04-elegir-la-política-ante-lo-que-depende-del-estado)).

**Se demuestra con** el gtest:

[`plugin/tests/dominio/LeyesTest.cpp:320`](https://github.com/jasrod12ucsm/checker/blob/main/plugin/tests/dominio/LeyesTest.cpp#L320-L325)

```cpp
TEST(Deteccion, LoValidoNoSeReporta) {
  for (HandleKind K : Kinds)
    for (HandleCategory C : Cats)
      for (PolicyMode Mode : {PolicyMode::Silent, PolicyMode::Possibly})
        EXPECT_EQ(onUse(handle(K, Position::first(0)), C, Mode).Verdict.Kind, VerdictKind::Fine);
}
```

con las funciones de `lit` sin `expected-warning` (con `-verify`, un aviso
no esperado hace fallar la prueba):

[`plugin/tests/lit/iteradores.cpp:41`](https://github.com/jasrod12ucsm/checker/blob/main/plugin/tests/lit/iteradores.cpp#L41-L48)

```cpp
void erase_idiom(std::list<int> &c) {
  for (auto it = c.begin(); it != c.end();) {
    if (*it % 2)
      it = c.erase(it); // sin aviso: el iterador devuelto es válido
    else
      ++it;
  }
}
```

y con `ejemplos/buen_uso.cpp`, que `verificar` analiza y debe quedar sin
avisos:

[`ejemplos/buen_uso.cpp:23`](https://github.com/jasrod12ucsm/checker/blob/main/ejemplos/buen_uso.cpp#L23-L27)

```cpp
int lista_estable(std::list<int> &l) {
  int &r = l.front();
  l.push_back(4); // list nunca invalida en una inserción
  return r;
}
```

En el banco: 0 avisos confirmados en los 306 casos `SAFE`.

### RF-08 Aplicar la regla de C++17

El efecto de una mutación sobre un handle sale de la tabla generada desde
`norma/matriz.json`, según contenedor, operación, categoría y relación con el
punto:

[`plugin/dominio/NormTable.cpp:47`](https://github.com/jasrod12ucsm/checker/blob/main/plugin/dominio/NormTable.cpp#L47-L53)

```cpp
std::optional<Effect> effectOf(const Mutation &M, HandleCategory C, Relation Rel) {
  HandleCategory N = normCategory(C);
  for (const RuleRow &R : Rules)
    if (R.M == M && R.Category == N && R.Rel == Rel)
      return Effect{R.Kind, R.Cond, R.Clause};
  return std::nullopt;
}
```

[`plugin/dominio/Decisions.cpp:39`](https://github.com/jasrod12ucsm/checker/blob/main/plugin/dominio/Decisions.cpp#L39-L95)

```cpp
ApplyResult apply(const MutationEvent &E, const HandleState &H, Credit C) {
  ValidityKind K = H.validity().kind();
  if (K == ValidityKind::Invalidated || K == ValidityKind::Diagnosed)
    return {H, false}; // absorbente

  HandleCategory Cat = categoryOf(H.kind());
  Growth G = growthOf(E.M).value_or(Growth::Unknown);
  RelationSet Rels = candidates(E, H, Cat);

  // ¿Todas las relaciones candidatas dicen lo mismo?
  std::optional<Effect> Common;
  std::optional<Relation> Only;
  bool Agree = true;
  unsigned Count = 0;
  for (Relation R : AllRelations) {
    if (!Rels.contains(R))
      continue;
    ++Count;
    Only = R;
    std::optional<Effect> Ef = effectOf(E.M, Cat, R);
    if (!Ef)
      continue;
    if (!Common)
      Common = Ef;
    else if (!sameEffect(*Common, *Ef))
      Agree = false;
  }
  if (!Common)
    return {H, false}; // la norma no dice nada: no se toca (lo prueba la ley de totalidad)
  if (!Agree) {
    Validity V = H.validity().join(Validity::relationUnknown(E));
    return {H.withValidity(V).withPosition(Position::unknown()), V != H.validity()};
  }

  // Si hubo varias relaciones con el mismo efecto, la posición nueva no se sabe.
  auto Transported = [&](const HandleState &S) {
    if (Count == 1)
      return S.withPosition(
          transport(E.M, G, *Only, S.position(), E.RangeEnd ? distance(E.PointPos, *E.RangeEnd) : 1));
    return S.withPosition(Position::unknown());
  };

  switch (Common->Kind) {
  case EffectKind::Preserves: return {Transported(H), false};
  case EffectKind::Invalidates: return {H.withValidity(Validity::invalidated(E)), true};
  case EffectKind::Depends:
    switch (answer(Common->Cond, G, C)) {
    case SolverAnswer::OnlyNo: return {Transported(H), false};
    case SolverAnswer::OnlyYes: return {H.withValidity(Validity::invalidated(E)), true};
    case SolverAnswer::Both: {
      Validity V = H.validity().join(Validity::dependsOn(Common->Cond, E));
      return {Transported(H).withValidity(V), V != H.validity()};
    }
    }
  }
  return {H, false};
}
```

**Se demuestra con** el gtest que recorre todas las celdas del banco (57
pares × 3 categorías + 12 con `reserve`) y compara el veredicto del núcleo
con la etiqueta que calcula `bench/etiquetar.py`, la otra implementación de
la norma:

[`plugin/tests/dominio/LeyesTest.cpp:454`](https://github.com/jasrod12ucsm/checker/blob/main/plugin/tests/dominio/LeyesTest.cpp#L454-L467)

```cpp
TEST(Banco, ElVeredictoDelNucleoEsLaEtiqueta) {
  unsigned N = 0;
  for (const BankCell &B : Bank) {
    ++N;
    HandleState H = handle(B.Kind, Position::first(0));
    HandleState After = apply(event(B.M, B.PointPos), H, B.Reserved).State;
    VerdictKind V = onUse(After, B.UseAs, PolicyMode::Possibly).Verdict.Kind;
    VerdictKind Want = B.Expected == Label::Ub     ? VerdictKind::Confirmed
                       : B.Expected == Label::Safe ? VerdictKind::Fine
                                                   : VerdictKind::Possibly;
    EXPECT_EQ(V, Want) << B.Name;
  }
  EXPECT_EQ(N, 171u + 12u); // 57 pares × 3 sostenes + 12 celdas con reserve (sin bucle)
}
```

### RF-09 Tratar lo que depende del estado

Cuando la norma dice «depende de la capacidad» o «del *rehash*», el checker
no inventa la capacidad: busca una garantía. `c.reserve(c.size() + k)` da
crédito para `k` inserciones:

[`plugin/acl/ClangRecognizer.cpp:101`](https://github.com/jasrod12ucsm/checker/blob/main/plugin/acl/ClangRecognizer.cpp#L101-L113)

```cpp
std::optional<unsigned> sizePlus(const Expr *E, CheckerContext &C) {
  const auto *B = dyn_cast_or_null<BinaryOperator>(strip(E));
  if (!B || B->getOpcode() != BO_Add)
    return std::nullopt;
  const Expr *L = B->getLHS(), *R = B->getRHS();
  if (!memberCallName(L, {"size"}))
    std::swap(L, R);
  if (!memberCallName(L, {"size"}))
    return std::nullopt;
  if (auto K = smallConstantOf(R, C); K && *K >= 0)
    return static_cast<unsigned>(*K);
  return std::nullopt;
}
```

[`plugin/dominio/Decisions.cpp:10`](https://github.com/jasrod12ucsm/checker/blob/main/plugin/dominio/Decisions.cpp#L10-L22)

```cpp
SolverAnswer answer(Condition Cond, Growth G, Credit C) {
  switch (Cond) {
  case Condition::CapacityReached:
  case Condition::RehashTriggered:
    // El crédito sólo cubre inserciones de un elemento.
    if (G == Growth::One && C && *C >= 1)
      return SolverAnswer::OnlyNo;
    return SolverAnswer::Both;
  case Condition::NonBinding:
  case Condition::None: return SolverAnswer::Both;
  }
  return SolverAnswer::Both;
}
```

[`plugin/dominio/Decisions.cpp:97`](https://github.com/jasrod12ucsm/checker/blob/main/plugin/dominio/Decisions.cpp#L97-L109)

```cpp
Credit consume(const Mutation &M, Credit C) {
  switch (growthOf(M).value_or(Growth::Unknown)) {
  case Growth::One:
    if (C && *C > 0)
      return *C - 1;
    return C;
  case Growth::None:
  case Growth::Shrinks: return C;
  case Growth::Unknown:
  case Growth::Reset: return std::nullopt;
  }
  return std::nullopt;
}
```

**Se demuestra con** los gtests de crédito:

[`plugin/tests/dominio/LeyesTest.cpp:266`](https://github.com/jasrod12ucsm/checker/blob/main/plugin/tests/dominio/LeyesTest.cpp#L266-L278)

```cpp
TEST(Deteccion, ConGarantiaDependerEsPreservar) {
  Mutation PushBack{ContainerKind::Vector, Operation::PushBack, Point::Back};
  Mutation Insert{ContainerKind::UnorderedSet, Operation::Insert, Point::ByKey};
  EXPECT_EQ(apply(event(PushBack, Position::pastEnd()), handle(HandleKind::Element, Position::first(0)), 1u)
                .State.validity()
                .kind(),
            ValidityKind::Valid);
  EXPECT_EQ(
      apply(event(Insert, Position::unknown()), handle(HandleKind::IteratorObject, Position::first(0)), 3u)
          .State.validity()
          .kind(),
      ValidityKind::Valid);
}
```

[`plugin/tests/dominio/LeyesTest.cpp:286`](https://github.com/jasrod12ucsm/checker/blob/main/plugin/tests/dominio/LeyesTest.cpp#L286-L292)

```cpp
TEST(Deteccion, UnaInsercionGastaUnCredito) {
  Mutation PushBack{ContainerKind::Vector, Operation::PushBack, Point::Back};
  EXPECT_EQ(consume(PushBack, 2u), Credit(1u));
  EXPECT_EQ(consume(PushBack, 1u), Credit(0u));
  EXPECT_EQ(consume(PushBack, 0u), Credit(0u));
  EXPECT_EQ(consume(PushBack, std::nullopt), Credit(std::nullopt));
}
```

y con `lit`: dos inserciones con crédito para una dan aviso posible en la
segunda:

[`plugin/tests/lit/garantias.cpp:14`](https://github.com/jasrod12ucsm/checker/blob/main/plugin/tests/lit/garantias.cpp#L14-L20)

```cpp
void reserved(std::vector<int> &c) {
  c.reserve(c.size() + 2);
  const int &h = c[0];
  c.push_back(1);
  c.push_back(2);
  sink(h); // sin aviso: reserve garantiza dos inserciones
}
```

[`plugin/tests/lit/garantias.cpp:22`](https://github.com/jasrod12ucsm/checker/blob/main/plugin/tests/lit/garantias.cpp#L22-L28)

```cpp
void reserved_too_little(std::vector<int> &c) {
  c.reserve(c.size() + 1);
  const int &h = c[0];
  c.push_back(1);
  c.push_back(2);
  sink(h); // expected-warning {{posiblemente invalidada: 'std::vector::push_back' (línea 26)}}
}
```

### RF-10 Tratar las llamadas opacas

Si el contenedor pasa a una función cuyo cuerpo no se analiza, los handles
válidos o no resueltos dejan de seguirse; uno ya inválido sigue avisando:

[`plugin/dominio/Decisions.cpp:143`](https://github.com/jasrod12ucsm/checker/blob/main/plugin/dominio/Decisions.cpp#L143-L147)

```cpp
std::optional<HandleState> escape(const HandleState &H, SourceRef At) {
  if (H.validity().kind() >= ValidityKind::Invalidated)
    return H;
  return std::nullopt;
}
```

[`plugin/checker/InvalidationChecker.cpp:393`](https://github.com/jasrod12ucsm/checker/blob/main/plugin/checker/InvalidationChecker.cpp#L393-L428)

```cpp
ProgramStateRef InvalidationChecker::checkRegionChanges(ProgramStateRef St, const InvalidatedSymbols *,
                                                        ArrayRef<const MemRegion *> Explicits,
                                                        ArrayRef<const MemRegion *>, const LocationContext *,
                                                        const CallEvent *Call) const {
  // Sólo una llamada que no reconocemos es un escape (deteccion.md §1).
  if (!Call || acl::containerCall(*Call) || acl::iteratorCopy(*Call))
    return St;
  // El contenedor escapa si la llamada recibe el contenedor o algo que lo
  // contiene (`this` cuando el contenedor es un campo).
  SourceRef At(Call->getOriginExpr());
  auto Escapes = [&](ContainerId Box) {
    const MemRegion *C = regionOf(Box);
    for (const MemRegion *X : Explicits)
      if (C == X || C->isSubRegionOf(X) || C->isSubRegionOf(X->getBaseRegion()))
        return true;
    return false;
  };
  for (const auto &[R, H] : St->get<IteratorMap>())
    if (Escapes(H.S.container())) {
      trace(St->getStateManager().getContext().getSourceManager(), Call->getOriginExpr(), "escape (olvida)",
            R);
      std::optional<HandleState> E = escape(H.S, At);
      St = E ? St->set<IteratorMap>(R, Stored{*E}) : St->remove<IteratorMap>(R);
    }
  for (const auto &[R, H] : St->get<ElementMap>())
    if (Escapes(H.S.container())) {
      trace(St->getStateManager().getContext().getSourceManager(), Call->getOriginExpr(), "escape (olvida)",
            R);
      std::optional<HandleState> E = escape(H.S, At);
      St = E ? St->set<ElementMap>(R, Stored{*E}) : St->remove<ElementMap>(R);
    }
  for (const auto &[R, K] : St->get<CreditMap>())
    if (Escapes(ContainerId(R)))
      St = St->remove<CreditMap>(R);
  return St;
}
```

**Se demuestra con:**

[`plugin/tests/dominio/LeyesTest.cpp:377`](https://github.com/jasrod12ucsm/checker/blob/main/plugin/tests/dominio/LeyesTest.cpp#L377-L386)

```cpp
TEST(Deteccion, EscaparOlvidaLoQueNoEstaInvalidado) {
  Mutation M{ContainerKind::List, Operation::Clear, Point::Whole};
  for (const HandleState &H : states(HandleKind::Element, Position::first(0), M)) {
    std::optional<HandleState> E = escape(H, S2);
    if (H.validity().kind() >= ValidityKind::Invalidated)
      EXPECT_EQ(E, std::optional<HandleState>(H)); // ninguna llamada revive un handle
    else
      EXPECT_FALSE(E.has_value());
  }
}
```

[`plugin/tests/lit/garantias.cpp:59`](https://github.com/jasrod12ucsm/checker/blob/main/plugin/tests/lit/garantias.cpp#L59-L63)

```cpp
void escaped(std::vector<int> &c) {
  const int &h = c[0];
  opaque(c);
  sink(h); // sin aviso: tras un escape el handle deja de seguirse (D-21)
}
```

[`plugin/tests/lit/garantias.cpp:65`](https://github.com/jasrod12ucsm/checker/blob/main/plugin/tests/lit/garantias.cpp#L65-L70)

```cpp
void escaped_after_invalid(std::vector<int> &c) {
  const int &h = c[0];
  c.clear();
  opaque(c);
  sink(h); // expected-warning {{Uso de una referencia invalidada: 'std::vector::clear'}}
}
```

### RF-11 Explicar la causa en el aviso

El aviso nombra la categoría del handle, la operación que lo invalidó y su
línea; el posible dice además qué garantía falta:

[`plugin/checker/Messages.cpp:37`](https://github.com/jasrod12ucsm/checker/blob/main/plugin/checker/Messages.cpp#L37-L42)

```cpp
std::string confirmed(const UseVerdict &V, unsigned MutationLine) {
  std::string S = "Uso de " + what(V.Category, "invalidad");
  if (const auto &E = V.Why.cause())
    S += ": " + opName(*E) + line(MutationLine) + " lo invalidó";
  return S;
}
```

[`plugin/checker/Messages.cpp:44`](https://github.com/jasrod12ucsm/checker/blob/main/plugin/checker/Messages.cpp#L44-L71)

```cpp
std::string possibly(const UseVerdict &V, unsigned CauseLine) {
  std::string S = "Uso de " + what(V.Category, "posiblemente invalidad");
  const auto &E = V.Why.cause();
  switch (V.Why.reason()) {
  case UnresolvedReason::DependsOnState:
    if (E)
      S += ": " + opName(*E) + line(CauseLine) + " " + condition(V.Why.condition());
    break;
  case UnresolvedReason::RelationUnknown:
    if (E)
      S += ": " + opName(*E) + line(CauseLine) +
           " lo invalida si el elemento está en el punto de la operación";
    break;
  case UnresolvedReason::EscapedToOpaqueCode:
    S += ": el contenedor se pasó a código que no se analiza" + line(CauseLine);
    break;
  case UnresolvedReason::None: break;
  }
  switch (V.Missing) {
  case MissingGuarantee::ReserveBefore:
    S += "; nada garantiza espacio: use reserve(size() + n) antes, o vuelva a obtenerlo";
    break;
  case MissingGuarantee::SizeAtLeastTwo: S += "; nada garantiza que no sea ese elemento"; break;
  case MissingGuarantee::ReobtainAfter: S += "; vuelva a obtenerlo después de la operación"; break;
  case MissingGuarantee::None: break;
  }
  return S;
}
```

**Se demuestra con** el texto de cada `expected-warning` en `lit`, que se
compara palabra por palabra. Por ejemplo:

[`plugin/tests/lit/garantias.cpp:45`](https://github.com/jasrod12ucsm/checker/blob/main/plugin/tests/lit/garantias.cpp#L45-L49)

```cpp
void pop_back_first(std::vector<int> &c) {
  const int &h = c[0];
  c.pop_back();
  sink(h); // expected-warning {{posiblemente invalidada: 'std::vector::pop_back' (línea 47) lo invalida si el elemento está en el punto}}
}
```

### RF-12 Mostrar la ruta del defecto

Cada paso relevante deja una nota en la ruta (`NoteTag`): dónde se obtuvo el
handle y qué lo invalidó:

[`plugin/checker/InvalidationChecker.cpp:136`](https://github.com/jasrod12ucsm/checker/blob/main/plugin/checker/InvalidationChecker.cpp#L136-L148)

```cpp
void transition(CheckerContext &C, ProgramStateRef St, Notes N) {
  if (N.empty()) {
    C.addTransition(St);
    return;
  }
  const NoteTag *Tag = C.getNoteTag([N = std::move(N)](PathSensitiveBugReport &BR) -> std::string {
    for (const auto &[R, Msg] : N)
      if (BR.isInteresting(R))
        return Msg;
    return "";
  });
  C.addTransition(St, Tag);
}
```

**Se demuestra con** `lit` `rutas.cpp`, que corre con
`-analyzer-output=text` y comprueba cada nota con `expected-note`:

[`plugin/tests/lit/rutas.cpp:8`](https://github.com/jasrod12ucsm/checker/blob/main/plugin/tests/lit/rutas.cpp#L8-L13)

```cpp
void ruta_iterador(std::vector<int> &c) {
  auto it = c.begin(); // expected-note {{El iterador se obtiene de 'std::vector::begin'}}
  c.clear();           // expected-note {{El iterador queda invalidado por 'std::vector::clear'}}
  sink(*it); // expected-warning {{Uso de un iterador invalidado: 'std::vector::clear' (línea 10) lo invalidó}} \
             // expected-note {{Uso de un iterador invalidado: 'std::vector::clear' (línea 10) lo invalidó}}
}
```

### RF-13 Ejecutar el experimento

Una invocación de `clang` por caso y condición, con tiempo límite y medición
de memoria; cada resultado es un `Completed` o un incidente:

[`bench/experimento.py:211`](https://github.com/jasrod12ucsm/checker/blob/main/bench/experimento.py#L211-L238)

```python
def ejecutar(case: str, firma: str, cond: Condicion, tmp: Path) -> tuple[Run, dict | None]:
    sarif = tmp / f"{case}.{cond.nombre}.sarif"
    cmd = [*cond.argumentos(), "-Xclang", f"-analyze-function={firma}", "-o", str(sarif), str(BANCO)]
    t0 = time.time()
    with open(tmp / f"{case}.{cond.nombre}.err", "w+") as errf:
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=errf)
        reloj = threading.Timer(TIMEOUT, proc.kill)
        reloj.start()
        # wait4 da el máximo de memoria residente de ESTE clang, no del grupo.
        _, status, uso = os.wait4(proc.pid, 0)
        reloj.cancel()
        proc.returncode = os.waitstatus_to_exitcode(status)
        errf.seek(0)
        err = errf.read()
    rss = uso.ru_maxrss
    if time.time() - t0 >= TIMEOUT:
        return Run(case, cond.nombre, "Timeout", TIMEOUT, rss), None
    dt = round(time.time() - t0, 3)
    if proc.returncode < 0 or "PLEASE submit a bug report" in err:
        return Run(case, cond.nombre, "Crash", dt, rss, err[-3000:]), None
    if proc.returncode != 0:
        return Run(case, cond.nombre, "CompileError", dt, rss, err[-3000:]), None
    try:
        doc = json.loads(sarif.read_text())
        sarif.unlink()
    except (OSError, json.JSONDecodeError) as e:
        return Run(case, cond.nombre, "Unreadable", dt, rss, f"{e}\n{err[-2000:]}"), None
    return Run(case, cond.nombre, "Completed", dt, rss), doc
```

**Se demuestra con** la ejecución misma: `verificar` corre 81 casos × 4
condiciones; `docker compose run --rm experimento` los 750 (3 000
ejecuciones, 0 incidentes).

### RF-14 Cotejar por sitio

Un aviso cuenta solo si cae en la función del caso, y acierta solo si cae
sobre un handle que la norma da por inválido (RN-006):

[`bench/experimento.py:291`](https://github.com/jasrod12ucsm/checker/blob/main/bench/experimento.py#L291-L299)

```python
def atribuir(case: str, ws: list[Warning], rango: dict, src: list[str], caso: dict
             ) -> tuple[list[tuple[Warning, str]], list[Warning]]:
    """Ley «un aviso pertenece a lo más a un caso»: el de la función que lo contiene."""
    a, b = rango[case]
    dentro: list[Warning] = []
    fuera: list[Warning] = []
    for w in ws:
        (dentro if a <= w.line <= b else fuera).append(w)
    return [(w, sitio(caso, src[w.line - 1])) for w in dentro], fuera
```

[`bench/experimento.py:303`](https://github.com/jasrod12ucsm/checker/blob/main/bench/experimento.py#L303-L321)

```python
def cotejar(case: str, caso: dict, run: Run, avisos: list[tuple[Warning, str]]) -> Match:
    if run.outcome != "Completed":
        # Ley «un fallo nunca es un verdadero negativo».
        return Match(case, run.condicion, "Incident", [], False, 0, 0)
    conf = [(w, s) for w, s in avisos if w.clase == "Confirmed"]
    posibles = sum(w.clase == "Possible" for w, _ in avisos)
    etiqueta_de = {"sostenido": caso["handles"]["sostenido"], "control": caso["handles"]["control"]}
    # Un aviso acierta en un caso UB sólo si cae sobre un handle que la norma da por inválido.
    buenos = [s for _, s in conf if etiqueta_de.get(s) == "UB"]
    e = caso["esperado"]
    if e == "UB":
        v = "TP" if buenos else "FN"
    elif e == "SAFE":
        v = "FP" if conf else "TN"
    else:
        v = "PolicyWarned" if conf or posibles else "PolicySilent"
    return Match(case, run.condicion, v, [s for _, s in conf],
                 any(s == "sostenido" for s in buenos),
                 len(conf) - len(buenos) if e == "UB" else 0, posibles)
```

**Se demuestra con** las 11 leyes de `bench/pruebas_evaluacion.py`, que
prueban el cotejo con datos escritos a mano, sin `clang`:

[`bench/pruebas_evaluacion.py:44`](https://github.com/jasrod12ucsm/checker/blob/main/bench/pruebas_evaluacion.py#L44-L47)

```python
@prueba("cotejo por sitio: el aviso sobre el control cuenta si el control es UB")
def _():
    m = cotejar("f", UB_SOLO_CONTROL, ok(), [(csa, "control")])
    assert m.verdict == "TP" and not m.en_sostenido
```

[`bench/pruebas_evaluacion.py:50`](https://github.com/jasrod12ucsm/checker/blob/main/bench/pruebas_evaluacion.py#L50-L54)

```python
@prueba("cotejo por sitio: el aviso sobre un handle SAFE no es un acierto")
def _():
    caso = {**UB_REF_BUCLE, "handles": {"sostenido": "UB", "control": "SAFE"}}
    m = cotejar("f", caso, ok(), [(csa, "control")])
    assert m.verdict == "FN" and m.fuera_de_sitio == 1
```

### RF-15 Generar y validar el banco

El banco se genera desde la norma (ver [Usar el corpus](corpus.md)):

[`bench/gen_corpus.py:126`](https://github.com/jasrod12ucsm/checker/blob/main/bench/gen_corpus.py#L126-L144)

```python
def cuerpo(fn, ct, cn, op, stmt, decl, use, ctx, reserva=0):
    """La función C++ de un caso. reserva=k: reserve(c.size() + k) antes de obtener."""
    pre = [f"  c.reserve(c.size() + {reserva});"] if reserva else []
    if ctx == "bucle":
        body = [f"void {fn}({ct}& c) {{", *pre,
                # La cota conserva el patrón de mutar durante la iteración,
                # pero evita recorrer para siempre lo recién insertado.
                "  int rondas = 0;",
                f"  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {{"]
        if decl: body.append(f"    {decl}")
        body += [f"    {stmt}", f"    {use}", "  }", "}"]
        return body
    body = [f"void {fn}({ct}& c) {{", *pre, "  auto it = c.begin();"]
    if ctx in ("guarda", "llamada"):
        body.append("  if (it == c.end()) return;")
    if decl: body.append(f"  {decl}")
    body.append(f"  mutar_{cn}_{op}(c);" if ctx == "llamada" else f"  {stmt}")
    body += [f"  {use}", "}"]
    return body
```

y cada caso se ejecuta con los dos oráculos dinámicos:

[`bench/run_runtime_validation.py:33`](https://github.com/jasrod12ucsm/checker/blob/main/bench/run_runtime_validation.py#L33-L52)

```python
def observe(binary: Path, case: str, mode: str, timeout: float) -> dict:
    try:
        environment = os.environ.copy()
        # LeakSanitizer no puede iniciarse bajo algunos sandboxes/ptrace. No
        # medimos fugas en este experimento: medimos invalidación temporal.
        environment["ASAN_OPTIONS"] = "detect_leaks=0"
        result = run([str(binary), case, mode], timeout=timeout, env=environment)
    except subprocess.TimeoutExpired:
        return {"estado": "TIMEOUT", "codigo": None, "stderr": ""}
    stderr = result.stderr[-4000:]
    text = stderr.lower()
    markers = ("addresssanitizer", "undefinedbehaviorsanitizer", "error: attempt",
               "error: dereference", "error: increment", "error: comparing")
    if any(marker in text for marker in markers):
        state = "DETECTADO"
    elif result.returncode == 0:
        state = "SIN_DETECCION"
    else:
        state = "ABORTO_SIN_CLASIFICAR"
    return {"estado": state, "codigo": result.returncode, "stderr": stderr}
```

**Se demuestra con** dos pasos. `verificar` regenera el banco y comprueba que
su sha256 es el del sello `test/banco-1.json`. `verificar --completo` corre
la validación dinámica (852 ejecuciones) y falla si algún caso `SAFE` tiene
una detección.

### RF-16 Construir y verificar el plugin

[`plugin/CMakeLists.txt:21`](https://github.com/jasrod12ucsm/checker/blob/main/plugin/CMakeLists.txt#L21-L33)

```cmake
# --- La tabla normativa: se genera desde norma/matriz.json -------------------
set(TABLA ${CMAKE_CURRENT_BINARY_DIR}/generado/NormTable.inc)
add_custom_command(
  OUTPUT ${TABLA}
  COMMAND Python3::Interpreter ${REPO}/norma/gen_tabla.py ${REPO}/norma/matriz.json ${TABLA}
  DEPENDS ${REPO}/norma/matriz.json ${REPO}/norma/gen_tabla.py
  COMMENT "Generar la tabla normativa (matriz.json → NormTable.inc)")

# --- Núcleo: no sabe de Clang -----------------------------------------------
add_library(ucsm_dominio STATIC
  dominio/NormTable.cpp dominio/Position.cpp dominio/Decisions.cpp ${TABLA})
target_include_directories(ucsm_dominio PUBLIC dominio PRIVATE ${CMAKE_CURRENT_BINARY_DIR})
target_compile_options(ucsm_dominio PRIVATE ${UCSM_WARNINGS} -fno-exceptions -fno-rtti)
```

**Se demuestra con** el primer paso de `verificar` (o
`docker compose run --rm plugin`): construye el plugin y corre las 40 gtests
y los 5 `lit`.

### RF-17 Mantener la norma como datos

Las reglas viven en `norma/matriz.json`, cada una con su cláusula de C++17.
`gen_tabla.py` comprueba sus leyes antes de generar la tabla y, si una se
rompe, no la genera:

[`norma/gen_tabla.py:111`](https://github.com/jasrod12ucsm/checker/blob/main/norma/gen_tabla.py#L111-L135)

```python
def check_leyes(ms: list[Mutacion]) -> list[str]:
    errores = []
    for m in ms:
        for r in m.reglas:
            if r.categoria != "iterator":
                continue
            ref = efecto(m, "reference", r.relacion)
            # «un iterador nunca está mejor que una referencia al mismo elemento»
            if ref and ORDEN[r.efecto] < ORDEN[ref.efecto]:
                errores.append(f"ley iterador ⊒ referencia: {m.id}/{r.relacion}")
        for r in m.reglas:
            # «insertar en un contenedor de nodos no invalida nada» (salvo resize, que puede recortar)
            if m.contenedor in NODOS and m.operacion in INSERCIONES and r.efecto != "preserves":
                errores.append(f"ley inserción en nodos: {m.id}/{r.categoria}/{r.relacion}")
            # «lo que está antes del punto sobrevive en un vector sin reubicar»
            if m.contenedor == "vector" and r.relacion == "before" and not (
                    r.efecto == "preserves" or r.condicion == "capacity_reached"):
                errores.append(f"ley antes del punto en vector: {m.id}/{r.categoria}")
            # «una mutación de todo no depende de la relación»
            if (m.punto in ("whole",) or (m.punto == "by_key" and m.operacion in INSERCIONES)) \
                    and r.relacion != "any":
                errores.append(f"ley mutación de todo: {m.id}/{r.categoria}/{r.relacion}")
            if r.relacion == "any" and m.punto not in ("whole", "by_key"):
                errores.append(f"'any' sólo en whole/by_key: {m.id}")
    return errores
```

**Se demuestra con** el build (que llama a `gen_tabla.py`) y con los gtests
`Norma.*`:

[`plugin/tests/dominio/LeyesTest.cpp:80`](https://github.com/jasrod12ucsm/checker/blob/main/plugin/tests/dominio/LeyesTest.cpp#L80-L90)

```cpp
TEST(Norma, LaTablaEsTotal) {
  forAllMutations([](Mutation M) {
    EXPECT_TRUE(growthOf(M).has_value());
    for (HandleCategory C : Cats) {
      RelationSet S = relationsOf(M, C);
      EXPECT_FALSE(S.empty());
      for (Relation R : AllRelations)
        EXPECT_EQ(S.contains(R), effectOf(M, C, R).has_value());
    }
  });
}
```

[`plugin/tests/dominio/LeyesTest.cpp:92`](https://github.com/jasrod12ucsm/checker/blob/main/plugin/tests/dominio/LeyesTest.cpp#L92-L99)

```cpp
TEST(Norma, InvalidarODependerCitaSuClausula) {
  forAllMutations([](Mutation M) {
    for (HandleCategory C : Cats)
      for (Relation R : AllRelations)
        if (auto E = effectOf(M, C, R); E && E->Kind != EffectKind::Preserves)
          EXPECT_STRNE(E->Clause, "");
  });
}
```

---

## Requerimientos no funcionales

### RNF-01 a RNF-03: precisión, cobertura y robustez

| | Criterio |
|---|---|
| RNF-01 | 0 avisos confirmados sobre casos `SAFE` |
| RNF-02 | detectar más que CSA solo, en el caso y sobre el handle retenido |
| RNF-03 | `clang` nunca aborta; lo que no termina se registra como incidente |

**Se demuestra con** `bench/regresion.py`. Sobre el banco completo exige los
mínimos de `bench/regresion.json` (342 UB, 328 sobre el handle retenido, 0
falsos positivos, 0 incidentes):

[`bench/regresion.py:22`](https://github.com/jasrod12ucsm/checker/blob/main/bench/regresion.py#L22-L37)

```python
def banco_completo() -> list[str]:
    minimo = json.loads((RAIZ / "bench" / "regresion.json").read_text())
    medido = json.loads((RAIZ / "test" / "experimento" / "metricas.json").read_text())["metricas"]
    fallos = []
    for cond, umbral in minimo.items():
        m = medido[cond]["All"]
        if m["fp"] > umbral["fp_max"]:
            fallos.append(f"{cond}: {m['fp']} avisos confirmados sobre casos SAFE (máximo {umbral['fp_max']})")
        if m["tp"] < umbral["tp_min"]:
            fallos.append(f"{cond}: {m['tp']} UB detectados (antes {umbral['tp_min']})")
        if m["ubEnSostenido"] < umbral["sostenido_min"]:
            fallos.append(f"{cond}: {m['ubEnSostenido']} UB sobre el handle sostenido (antes {umbral['sostenido_min']})")
        if m["incidents"] > 0:
            fallos.append(f"{cond}: {m['incidents']} incidentes")
        print(f"{cond}: tp={m['tp']} fp={m['fp']} sostenido={m['ubEnSostenido']} incidentes={m['incidents']}")
    return fallos
```

y sobre la muestra de `verificar`, que con el checker no quede ningún UB sin
detectar, ningún falso positivo ni incidente, y que los `POLICY` reciban
aviso posible solo en `Possibly`:

[`bench/regresion.py:40`](https://github.com/jasrod12ucsm/checker/blob/main/bench/regresion.py#L40-L55)

```python
def muestra(ruta: Path) -> list[str]:
    medido = json.loads(ruta.read_text())["metricas"]
    fallos = []
    for cond, todo in medido.items():
        m = todo["All"]
        print(f"{cond}: tp={m['tp']} fn={m['fn']} fp={m['fp']} "
              f"POLICY={m['policyWarned']}/{m['policyWarned'] + m['policySilent']} incidentes={m['incidents']}")
        if m["fp"] or m["incidents"]:
            fallos.append(f"{cond}: {m['fp']} falsos positivos, {m['incidents']} incidentes")
        if cond in CON_CHECKER and m["fn"]:
            fallos.append(f"{cond}: {m['fn']} UB sin detectar")
        if cond.endswith("Possibly") and m["policySilent"]:
            fallos.append(f"{cond}: {m['policySilent']} casos POLICY sin aviso posible")
        if cond == "Experimental-Silent" and m["policyWarned"]:
            fallos.append(f"{cond}: {m['policyWarned']} avisos posibles en modo Silent")
    return fallos
```

### RNF-04 y RNF-05: tiempo y memoria

El checker no puede subir la mediana del tiempo por caso más de 10 % ni la
memoria residente máxima más de 5 %, frente a CSA sin él.

**Se demuestra con** `bench/rendimiento.py`, que lee las ejecuciones que
guardó el experimento (`test/experimento/ejecucion.json`):

[`bench/rendimiento.py:25`](https://github.com/jasrod12ucsm/checker/blob/main/bench/rendimiento.py#L25-L36)

```python
def main() -> int:
    runs = json.loads(EJECUCION.read_text())["runs"]
    sel = lambda c: [r for r in runs if r["condicion"] == c and r["outcome"] == "Completed"]
    base, con = sel(BASE), sel(CON)
    t0 = statistics.median(r["segundos"] for r in base)
    t1 = statistics.median(r["segundos"] for r in con)
    m0 = max(r["max_rss_kb"] for r in base) / 1024
    m1 = max(r["max_rss_kb"] for r in con) / 1024
    dt, dm = t1 / t0 - 1, m1 / m0 - 1
    print(f"RNF-04 tiempo mediano por caso: {t0:.3f} s → {t1:.3f} s ({100 * dt:+.1f} %, umbral {100 * UMBRAL_TIEMPO:.0f} %)")
    print(f"RNF-05 memoria residente máxima: {m0:.1f} MB → {m1:.1f} MB ({100 * dm:+.1f} %, umbral {100 * UMBRAL_MEMORIA:.0f} %)")
    return 0 if dt < UMBRAL_TIEMPO and dm < UMBRAL_MEMORIA else 1
```

```text
RNF-04 tiempo mediano por caso: 0.650 s → 0.652 s (+0.3 %, umbral 10 %)
RNF-05 memoria residente máxima: 119.1 MB → 119.9 MB (+0.7 %, umbral 5 %)
```

### RNF-06: claridad del diagnóstico

Todo aviso nombra handle, contenedor, operación y línea (RF-11); el posible
dice qué falta.

**Se demuestra con:**

[`plugin/tests/dominio/LeyesTest.cpp:422`](https://github.com/jasrod12ucsm/checker/blob/main/plugin/tests/dominio/LeyesTest.cpp#L422-L434)

```cpp
TEST(Deteccion, CadaRazonDeNoResueltoDiceQueFalta) {
  Mutation M{ContainerKind::Vector, Operation::PushBack, Point::Back};
  MutationEvent E = event(M, Position::pastEnd());
  auto Falta = [&](Validity V) {
    return onUse(handle(HandleKind::Element, Position::first(0)).withValidity(V), HandleCategory::Reference,
                 PolicyMode::Possibly)
        .Verdict.Missing;
  };
  EXPECT_EQ(Falta(Validity::dependsOn(Condition::CapacityReached, E)), MissingGuarantee::ReserveBefore);
  EXPECT_EQ(Falta(Validity::dependsOn(Condition::NonBinding, E)), MissingGuarantee::ReobtainAfter);
  EXPECT_EQ(Falta(Validity::relationUnknown(E)), MissingGuarantee::SizeAtLeastTwo);
  EXPECT_EQ(Falta(Validity::escaped(S1)), MissingGuarantee::ReobtainAfter);
}
```

### RNF-07: mantenibilidad

El núcleo no conoce Clang: el *target* `ucsm_dominio` no recibe las
cabeceras de Clang, así que un `#include` de Clang en `plugin/dominio/` no
compila. Corregir una regla es editar `matriz.json`, sin tocar C++.

[`plugin/CMakeLists.txt:29`](https://github.com/jasrod12ucsm/checker/blob/main/plugin/CMakeLists.txt#L29-L33)

```cmake
# --- Núcleo: no sabe de Clang -----------------------------------------------
add_library(ucsm_dominio STATIC
  dominio/NormTable.cpp dominio/Position.cpp dominio/Decisions.cpp ${TABLA})
target_include_directories(ucsm_dominio PUBLIC dominio PRIVATE ${CMAKE_CURRENT_BINARY_DIR})
target_compile_options(ucsm_dominio PRIVATE ${UCSM_WARNINGS} -fno-exceptions -fno-rtti)
```

**Se demuestra con** el build mismo y con los gtests, que enlazan solo contra
`ucsm_dominio`.

### RNF-08: reproducibilidad

Cada ejecución del experimento registra las versiones de `clang` y de
libstdc++ y el sha256 del plugin y del banco, y se niega a correr con un
banco sin sello:

[`bench/experimento.py:185`](https://github.com/jasrod12ucsm/checker/blob/main/bench/experimento.py#L185-L207)

```python
def verificar() -> dict:
    if not PLUGIN.exists():
        sys.exit(f"PluginNotLoadable: no existe {PLUGIN}")
    p = subprocess.run(["clang", "-cc1", "-load", str(PLUGIN), "-analyzer-checker-help"],
                       capture_output=True, text=True)
    if NUESTRO not in p.stdout:
        sys.exit(f"PluginNotLoadable:\n{p.stderr[-2000:]}")
    version = subprocess.run(["clang++", "--version"], capture_output=True, text=True).stdout.splitlines()[0]
    libstdcxx = subprocess.run(["sh", "-c", "dpkg-query -W -f='${Version}' libstdc++-13-dev 2>/dev/null"],
                               capture_output=True, text=True).stdout
    congelado = None
    for sello in sorted((RAIZ / "test").glob("banco-*.json")):
        s = json.loads(sello.read_text())
        if (s["corpus.cpp"], s["corpus_truth.json"]) == (sha256(BANCO), sha256(VERDAD)):
            congelado = s["banco"]
    if congelado is None and list((RAIZ / "test").glob("banco-*.json")):
        sys.exit("BankNotFrozen: el banco no coincide con ningún sello test/banco-*.json")
    return {"clang": version, "libstdcxx": libstdcxx or "desconocida",
            "plugin_sha256": sha256(PLUGIN), "banco_sha256": sha256(BANCO),
            "verdad_sha256": sha256(VERDAD),
            "banco_congelado": congelado,
            "condiciones": {c.nombre: c.argumentos() for c in CONDICIONES},
            "timeout": TIMEOUT}
```

---

## Reglas de negocio

| Regla | Se implementa en | Se demuestra con |
|---|---|---|
| RN-001 La etiqueta es el peor efecto de los handles del caso | `bench/etiquetar.py` `por_handle`, `etiqueta` | ley «la etiqueta es el JOIN de sus handles» |
| RN-002 Las condiciones difieren solo en el checker | `experimento.py` `Condicion` | `meta.condiciones` de `metricas.json` |
| RN-003 Lo que depende del estado nunca es confirmado | `Decisions.cpp` `onUse` | gtest `NoResueltoNuncaSeInformaComoConfirmado` |
| RN-004 Un aviso posible no es acierto ni falso positivo | `experimento.py` `cotejar` | ley «un aviso posible no es un acierto ni un falso positivo» |
| RN-005 Un fallo es un incidente, no un verdadero negativo | `experimento.py` `ejecutar`, `cotejar` | ley «un fallo nunca es un verdadero negativo» |
| RN-006 Un aviso acierta solo sobre un handle inválido | `experimento.py` `cotejar` | leyes de cotejo por sitio |
| RN-007 Cada resultado lleva versiones y sha256 | `experimento.py` `verificar` | `meta` de `metricas.json` |

Las leyes de RN-001, RN-004 y RN-005:

[`bench/pruebas_evaluacion.py:112`](https://github.com/jasrod12ucsm/checker/blob/main/bench/pruebas_evaluacion.py#L112-L118)

```python
@prueba("la etiqueta es el JOIN de sus handles (matriz completa)")
def _():
    for m in cargar().values():
        for so in ("it", "ref", "ptr"):
            for fo in ("recto", "guarda", "bucle", "llamada"):
                h = por_handle(m, so, fo)
                assert etiqueta(m, so, fo) == join(*(l for l in h.values() if l))
```

[`bench/pruebas_evaluacion.py:57`](https://github.com/jasrod12ucsm/checker/blob/main/bench/pruebas_evaluacion.py#L57-L61)

```python
@prueba("un aviso posible no es un acierto ni un falso positivo")
def _():
    assert cotejar("f", UB_REF_BUCLE, ok(), [(pos, "sostenido")]).verdict == "FN"
    assert cotejar("f", SAFE, ok(), [(pos, "sostenido")]).verdict == "TN"
    assert cotejar("f", POLICY, ok(), [(pos, "sostenido")]).verdict == "PolicyWarned"
```

[`bench/pruebas_evaluacion.py:37`](https://github.com/jasrod12ucsm/checker/blob/main/bench/pruebas_evaluacion.py#L37-L41)

```python
@prueba("un fallo nunca es un verdadero negativo")
def _():
    for o in ("CompileError", "Crash", "Timeout", "Unreadable"):
        r = Run("f", "Reference", o, 1.0, 1)
        assert cotejar("f", SAFE, r, []).verdict == "Incident"
```
