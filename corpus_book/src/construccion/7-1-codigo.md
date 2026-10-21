# 7.1 Construcción del código

## a) Preparación previa

### Entorno

| Herramienta | Versión | Para qué |
|---|---|---|
| Docker, imagen `checker:llvm21` | Ubuntu 24.04 + LLVM/Clang 21 | compilar y ejecutar el plugin con la misma API que el experimento |
| CMake + Ninja | ≥ 3.20 | construir los tres *targets* (dominio, plugin, pruebas) |
| `clangd` | 21 | navegación y diagnósticos en el editor, desde `compile_commands.json` |
| GoogleTest | de la distribución | pruebas del núcleo |
| `lit` + `FileCheck` | los de LLVM 21 | pruebas del checker con `-verify` (la convención de CSA) |
| Python | 3.12 | arnés, sin dependencias externas; leyes en `bench/pruebas_evaluacion.py` |
| mdbook + PlantUML (jar) | 0.5 / 1.2024 | libro y figuras |

### Estándares de codificación

| Tema | Estándar | Cómo se verifica | Estado |
|---|---|---|---|
| Estilo C++ | *LLVM Coding Standards* | `.clang-format` (`BasedOnStyle: LLVM`, 110 columnas); `clang-format --dry-run -Werror` en `calidad` | aplicado: 0 diferencias |
| Nombres | identificadores en inglés, `CamelCase` para tipos, como CSA; comentarios y documentación en español | revisión | aplicado |
| Estados | nunca `bool` ni texto para un estado: `enum class` o `std::variant` | revisión | aplicado (`Validity`, `Effect`, `Outcome`) |
| `switch` sobre enums del dominio | **sin `default:`**; `-Werror=switch` | el compilador | aplicado |
| Errores | sin excepciones ni RTTI (como LLVM); `std::optional` | `-fno-exceptions -fno-rtti` en `ucsm_dominio` y el plugin | aplicado |
| Inmutabilidad | los valores del dominio sólo tienen métodos `const` | revisión | aplicado |
| Python | anotaciones de tipo, `dataclass(frozen=True)`, `subprocess` con lista de argumentos | `mypy` en `calidad` | aplicado: 0 errores en 8 módulos |

### Planificación modular

Las responsabilidades están en el capítulo 5 y en
[Dónde va cada cosa](../diseno/donde-va.md). La regla que más protege:
**una regla de invalidación sólo se escribe en `norma/matriz.json`**.

## b) Escritura del código: en incrementos

Cada incremento **termina con el banco corrido** y sus resultados versionados
(ver [7.6](7-6-incrementos.md)). Una mejora no se da por hecha: se mide, y si
un incremento empeora algo (un SAFE con aviso), se ve en la tabla.

Buenas prácticas que se aplican:

- **DRY de verdad:** la norma existe una sola vez (D-05). La tabla C++ y las
  etiquetas se generan.
- **Funciones pequeñas y puras** en el núcleo. Los callbacks son de cuatro
  líneas: cargar, traducir, decidir, aplicar.
- **Reutilizar CSA** en vez de reimplementar: `CallDescriptionMap`, `NoteTag`,
  `REGISTER_MAP_WITH_PROGRAMSTATE`, `SymbolReaper`.

## c) Pruebas durante la codificación

| Nivel | Qué prueba | Herramienta | Cuándo |
|---|---|---|---|
| Leyes de la norma | las cuatro leyes sobre `matriz.json` | GoogleTest | cada cambio en la matriz |
| Leyes del núcleo | las siete leyes de la detección, con generadores | GoogleTest | TDD: la prueba de la ley antes que la decisión |
| Checker | cinco `.cpp` con `// expected-warning{{…}}` y `expected-note` (30 avisos y 9 notas) | `clang --analyze -load … -verify` vía `lit` | cada cambio en `acl/` o `checker/` |
| Integración | el banco completo en las cuatro condiciones | `bench/experimento.py` | cada incremento |
| Leyes del arnés | las once leyes de la evaluación | `bench/pruebas_evaluacion.py` | cada cambio en `bench/experimento.py` |

**Depuración** con las herramientas de CSA:

- `-analyzer-checker=debug.ExprInspection` con `clang_analyzer_dump(x)`;
- `-analyzer-dump-egraph` para ver el `ExplodedGraph`;
- `-analyzer-config ucsm.ContainerInvalidation:Debug=true` para
  volcar los mapas del estado en cada nodo.

## d) Revisión del código

Sin *push* directo a `main`. Cada rama se integra con un *pull request* que
**revisa la otra integrante del equipo** con esta lista:

1. ¿Alguna regla de invalidación fuera de `matriz.json`?
2. ¿Algún `bool`, texto o `default:` para un estado del dominio?
3. ¿El núcleo incluye algo de Clang? (Si compila, no.)
4. ¿Cada decisión nueva tiene la prueba de su ley?
5. ¿El PR adjunta la tabla del banco antes/después?

## e) Integración continua

`.github/workflows/ci.yml` corre en GitHub Actions, con la misma imagen
(ver [7.3](7-3-versiones.md)), los tres servicios de `docker compose`:

| Paso | Servicio | Qué falla |
|---|---|---|
| construir y probar | `plugin` | el plugin no compila; un gtest o un `lit` falla |
| calidad | `calidad` (`plugin/tests/calidad.sh`) | formato distinto del de `.clang-format`; un error de `mypy`; una ley del arnés; cobertura de líneas del núcleo < 90 % |
| banco | `experimento` (`bench/experimento.py` + `bench/regresion.py`) | un caso `SAFE` gana un aviso confirmado, un `UB` que se detectaba deja de detectarse, o hay un incidente |

Los tres pasos se corrieron con esa imagen en local y pasan. El *workflow*
corre en GitHub desde el primer *push* que lo incluya.

## f) Optimización

Sólo **medida**: tiempo y memoria máxima por caso frente a la condición de
referencia (RNF-04, RNF-05). Medido: +0.3 % de tiempo mediano y +0.7 % de
memoria. No hizo falta perfilar.
