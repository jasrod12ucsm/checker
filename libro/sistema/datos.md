# Base de datos

La construcción de la base (análisis, diseño conceptual, lógico y físico,
implementación, pruebas y despliegue) está en la
[sección 7.2](../construccion/7-2-datos.md). Aquí está el esquema entero.

![Modelo entidad-relación](../diagramas/sistema-er.svg)

{{codigo sistema/paquetes/adaptadores/sqlite/src/esquema.sql 1-89}}

## Versiones del esquema y migraciones

La versión del esquema se guarda en `PRAGMA user_version`. Una base nueva se
crea directamente en la versión actual (2). Una base de una versión anterior se
actualiza sola al abrirla: `abrirAlmacen` corre los bloques de
`migraciones.sql` que le faltan, en una sola transacción, y verifica las claves
foráneas antes de confirmar. Una base de una versión más nueva que el binario
no se abre.

| Versión | Cambio |
|---|---|
| 1 | esquema inicial; la cuenta tenía `activo` (0 o 1) |
| 2 | `usuarios.estado` (`Pendiente`, `Activo`, `Desactivado`) en lugar de `activo`; `hallazgos.clasificado_por` y `clasificado_en`. Una cuenta inactiva de la versión 1 queda `Pendiente`, porque la versión 1 no distinguía un registro sin aprobar de una baja |

{{codigo sistema/paquetes/adaptadores/sqlite/src/migraciones.sql 1-21}}

{{codigo sistema/paquetes/adaptadores/sqlite/src/almacen.ts migrar}}

{{codigo sistema/paquetes/adaptadores/sqlite/src/almacen.test.ts "una base de la versión 1 se migra al abrirla: activos siguen activos, inactivos quedan pendientes"}}
