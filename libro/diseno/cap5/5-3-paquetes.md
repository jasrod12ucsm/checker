# 5.3 Paquetes

## Servicio: paquetes de TypeScript

![Paquetes del servicio](../../diagramas/sistema-paquetes.svg)

Cada caja es un paquete de npm (*workspace*) con su propio `package.json`.
Las dependencias van hacia adentro: los adaptadores dependen del producto, el
producto de los contextos y los contextos del kernel. Ningún contexto
importa Fastify, SQLite ni módulos de Node. La regla no es una convención:
`pruebas/arquitectura.test.ts` lee las importaciones de cada paquete y falla
si aparece una que su capa no permite.

Tabla: Paquetes del servicio y sus dependencias

| Paquete | Contiene |
|---|---|
| `kernel` | `Resultado`, tipos con marca (`Email`, `UsuarioId`…), `Instante`, puertos `Reloj` y `GeneradorIds` |
| `contextos/identidad` | usuarios, roles, permisos, sesiones y el testigo `Autorizado<P>` |
| `contextos/repositorios` | repositorio conectado, política y bloqueo del merge |
| `contextos/revisiones` | revisión con sus estados, hallazgos, huellas, veredicto y estado del commit |
| `producto` | casos de uso y los puertos que necesitan (almacén, GitHub, analizador…) |
| `adaptadores/*` | `http` (Fastify), `sqlite`, `github`, `analizador` (clang), `cripto` |
| `app` | raíz de composición: lee la configuración, conecta todo y arranca el servidor y el trabajador |

## Motor de análisis: paquetes de C++

![Paquetes](../../diagramas/5-3-paquetes.svg)

Tabla: Paquetes del motor y sus dependencias

| Paquete | Contiene | Depende de | No puede depender de |
|---|---|---|---|
| `norma` | `matriz.json`, `gen_tabla.py` | nada | — |
| `plugin/dominio` | tipos y decisiones puras; `NormTable.inc` generado | `norma` (sólo por el archivo generado) | **Clang** (el target no tiene sus include dirs) |
| `plugin/acl` | reconocimiento de contenedores, operaciones, handles y posiciones | `dominio`, AST y SVal de Clang | `checker` |
| `plugin/checker` | `InvalidationChecker`, rasgos de `ProgramState`, mensajes | `acl`, `dominio`, CSA Core | `bench` |
| `plugin/registro` | `clang_registerCheckers`, versión de la API, opciones | `checker` | — |
| `evaluacion` | banco, ejecutor, normalizador, cotejo, métricas | `norma` (etiquetas); la **salida** de `clang` | `plugin` como código: lo invoca como proceso |
| `validacion_dinamica` | arnés de ejecución con libstdc++ Debug y ASan | `norma` | `plugin` |
| `libro` | `gen_book.py`, `render_diagramas.py` | resultados de `evaluacion` y `validacion_dinamica` | — |

**Regla de dependencias:** todas las flechas van hacia el centro: `norma` y
`dominio`. Ninguna sale de ellos. Es la regla de dependencias del diseño guiado por el dominio (Evans, 2003), con un *target* de CMake como frontera:

```cmake
add_library(invalidacion_dominio STATIC dominio/Decisions.cpp …)
# SIN target_include_directories(${CLANG_INCLUDE_DIRS}):
# un #include "clang/…" en dominio/ no compila. La frontera se cumple sola.
add_library(ContainerInvalidation MODULE acl/… checker/… registro/Plugin.cpp)
target_link_libraries(ContainerInvalidation PRIVATE invalidacion_dominio)
```
