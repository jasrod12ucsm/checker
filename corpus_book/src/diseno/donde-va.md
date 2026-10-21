# Dónde va cada cosa

> Adaptación de la skill `donde-va`: **antes de crear un archivo**, contestar
> cuatro preguntas y ubicarlo en este árbol. Si un archivo no cabe en el
> árbol, el árbol está incompleto o el archivo sobra. Se decide antes de
> escribirlo.

## Las cuatro preguntas

1. **¿Necesita Clang?** Si no, va en `plugin/dominio/`. Si sí, ¿traduce
   (`acl/`) o habla con el motor (`checker/`)?
2. **¿Es la norma o la aplica?** La norma vive en `norma/matriz.json`. Nadie
   escribe una regla de invalidación en otro sitio.
3. **¿Mide o detecta?** Medir es `bench/`. Detectar es `plugin/`. Nunca se
   importan entre sí.
4. **¿Qué más hay que tocar para que exista de verdad?** (abajo, «recetas»).

## El árbol propuesto

```
checker/
├── norma/
│   ├── matriz.json              FUENTE ÚNICA: 101 mutaciones, 348 reglas (categoría × relación), con cláusula
│   └── gen_tabla.py             matriz.json → build/plugin/generado/NormTable.inc (lo llama CMake)
├── plugin/                      C++17, CMake, LLVM 21
│   ├── CMakeLists.txt           tres targets: dominio (sin Clang), acl+checker, plugin .so
│   ├── dominio/                 ❗ SIN include dirs de Clang: un #include "clang/…" no compila
│   │   ├── Lenguaje.h           ContainerKind, HandleKind, HandleCategory, Mutation, Relation
│   │   ├── Position.h           Position + relate + transport
│   │   ├── Effect.h             Effect, Condition
│   │   ├── Validity.h           Validity + join
│   │   ├── HandleState.h        HandleState (inmutable, Profile para FoldingSet)
│   │   ├── Decisions.h/.cpp     obtain, apply, onUse, escape (funciones puras)
│   │   └── generado/NormTable.inc   ⚠ no se edita a mano
│   ├── acl/
│   │   ├── ClangRecognizer.h/.cpp   CallEvent/SVal → Obtention | Mutation | IteratorMove | NotOurs
│   │   └── Containers.cpp           CXXRecordDecl en std:: → ContainerKind
│   ├── checker/
│   │   ├── InvalidationChecker.cpp  callbacks: cargar → decidir → aplicar
│   │   ├── StateTraits.h            REGISTER_MAP_WITH_PROGRAMSTATE(HandleMap / IteratorMap)
│   │   └── Messages.cpp             texto de avisos y notas (RF-11, RF-12)
│   ├── registro/Plugin.cpp          clang_registerCheckers + clang_analyzerAPIVersionString
│   └── tests/
│       ├── dominio/                 GoogleTest, una prueba por ley, sin Clang
│       └── lit/                     un .cpp por regla con // expected-warning{{…}} y -verify
├── bench/                       Python 3.12 — contexto Evaluación
│   ├── gen_corpus.py            matriz.json → test/corpus.cpp + corpus_truth.json
│   ├── experimento.py           ejecutor, normalizador, cotejo, métricas (4 condiciones)
│   ├── codigo_real.py, inyeccion.py   proyectos reales y defectos sembrados
│   ├── run_runtime_validation.py   contexto Validación dinámica
│   ├── gen_book.py, render_diagramas.py
│   └── pruebas_evaluacion.py    una prueba por ley de la evaluación
├── test/                        banco: corpus.cpp, corpus_truth.json
│   ├── experimento/             ejecucion.json, cotejo.json, metricas.json
│   └── codigo_real/             avisos.json, inyeccion.json
├── libro/                       páginas y diagramas escritos a mano
└── corpus_book/                 ⚠ GENERADO por gen_book.py: no se edita a mano
```

## Índice: si escribes X, va en Y

| Si escribes… | Va en | Además tocas |
|---|---|---|
| una regla de invalidación nueva o corregida | `norma/matriz.json` | regenerar tabla y banco; correr las leyes de la norma |
| un tipo del lenguaje ubicuo | `plugin/dominio/` | su ley, si tiene |
| una decisión «dado este estado y este evento» | `plugin/dominio/Decisions.cpp` | prueba de la ley que cumple |
| cómo reconocer una llamada de la STL | `plugin/acl/ClangRecognizer.cpp` | prueba `lit` con esa llamada |
| un callback nuevo de CSA | `plugin/checker/InvalidationChecker.cpp` | la lista `Checker<…>` y el diagrama 5.4 |
| un texto de aviso o nota | `plugin/checker/Messages.cpp` | la prueba `lit` que lo espera literal |
| una opción del checker (`PolicyMode`) | `plugin/registro/Plugin.cpp` (`addCheckerOption`) | el libro y el registro de configuración |
| un formato de salida nuevo que leer | `bench/evaluacion/normalizar.py` | su ley de idempotencia |
| una métrica | `bench/evaluacion/metricas.py` | nunca promediando razones |
| una página del libro | `libro/` | la entrada en `SUMMARY` de `gen_book.py` |
| un diagrama | `libro/diagramas/*.puml` | `python3 bench/render_diagramas.py` |

## Lo que no se edita

| Archivo | Por qué | En su lugar |
|---|---|---|
| `corpus_book/src/**` | lo borra y rehace `gen_book.py` | `libro/` o el generador |
| `plugin/dominio/generado/**` | sale de `matriz.json` | `norma/matriz.json` |
| `test/corpus.cpp`, `corpus_truth.json` con el banco congelado | cambiar el banco a mitad de la evaluación invalida la comparación | una versión nueva del banco, con su tag |
| `src/MiLinter.cpp`, `src/CatchByValueCheck.*` | prototipo LibTooling retirado (D-01) | `plugin/` |

## Las tres cosas que más se equivocan

1. **Poner una regla en un `if` de un callback.** Si aparece
   `if (Kind == Vector && Name == "push_back")` en `checker/`, la regla se
   escapó de la norma. Va a `matriz.json`.
2. **Guardar algo que se puede preguntar.** La capacidad, el tamaño o el
   «es el primero» se preguntan al estado del camino. No se copian a un campo.
3. **Contar un fallo como «sin avisos».** Un `Timeout` o un `Crash` es una
   incidencia, y se ve en el informe.
