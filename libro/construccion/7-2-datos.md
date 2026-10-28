# 7.2 Construcción de la base de datos

El proyecto tiene **dos almacenes** con necesidades distintas:

| Almacén | Para qué | Tecnología |
|---|---|---|
| Base del servicio | usuarios, sesiones, repositorios, revisiones, hallazgos y la cola de trabajos de Centinela; muchos usuarios a la vez y transacciones | SQLite (relacional), `sistema/paquetes/adaptadores/sqlite/src/esquema.sql` |
| Datos de la evaluación del motor | la norma, el banco, las ejecuciones y las métricas; se escriben una vez por experimento y deben ser versionables y auditables | archivos JSON en el repositorio (sección 7.2.8) |

## a) Análisis de requisitos

Tabla: Requisitos de datos del servicio

| Dato | Para qué | Restricción |
|---|---|---|
| usuarios | ingresar y autorizar | correo único; solo el hash scrypt de la clave; rol `administrador` o `desarrollador`; estado `Pendiente`, `Activo` o `Desactivado` |
| sesiones | recordar quién ingresó | se guarda el hash del token, nunca el token; vencen a las 8 horas |
| repositorios | saber qué revisar y cómo | nombre único `propietario/nombre`; política `Silent` o `Possibly`; secreto del *webhook* |
| revisiones | el resultado de cada commit revisado | un commit de un PR se revisa una sola vez; el estado decide qué columnas tienen valor |
| hallazgos | lo que el checker encontró | pertenecen a una revisión; su ruta se guarda entera; quién lo clasificó y cuándo, los dos o ninguno |
| descartes | falsos positivos marcados | uno por repositorio y huella |
| trabajos | la cola del trabajador | se escribe en la misma transacción que la revisión |

## b) Diseño conceptual

![Modelo entidad-relación del servicio](../diagramas/sistema-er.svg)

Un repositorio tiene muchas revisiones y cada revisión muchos hallazgos. Los
descartes cuelgan del repositorio, no de la revisión: así un falso positivo
marcado una vez vale para los commits siguientes.

## c) Diseño lógico

Cada agregado del dominio es una tabla. El estado de la revisión, que en el
dominio es una unión (`Pendiente | EnAnalisis | Publicada | Fallida`), se
guarda **aplanado**: la columna `estado` dice la variante y solo sus columnas
tienen valor. Dos restricciones `CHECK` lo garantizan en la base: una
revisión tiene veredicto si y solo si está publicada, y motivo si y solo si
falló.

**Normalización.** El esquema está en tercera forma normal:

| Forma | Cómo se cumple |
|---|---|
| 1FN | cada columna guarda un solo valor; los hallazgos de una revisión son filas de `hallazgos`, no una lista dentro de la revisión |
| 2FN | toda clave es simple (un UUID), salvo la de `descartes` (`repositorio_id`, `huella`), y su columna restante (quién y cuándo) depende de las dos |
| 3FN | ninguna columna depende de otra que no sea la clave: el nombre del repositorio no se copia en la revisión, se une por `repositorio_id`; el resumen de una revisión publicada (archivos analizados, no compilados, confirmados, posibles, suprimidos) no se deriva de `hallazgos`: es lo que se publicó en GitHub en ese momento, y una clasificación posterior cambia el hallazgo pero no lo ya publicado; los archivos analizados y no compilados no tienen fila propia |

La única excepción consciente es `hallazgos.ruta`, la secuencia de pasos
(archivo, línea, mensaje) que explica el aviso: se guarda como JSON en una
columna `TEXT`. Nunca se consulta por un paso, siempre se lee entera junto
con su hallazgo y no se modifica; una tabla `pasos` sólo agregaría una
unión en cada lectura. Al leerla se valida con zod como cualquier otra
columna.

El esquema completo:

{{codigo sistema/paquetes/adaptadores/sqlite/src/esquema.sql 1-91}}

## d) Diseño físico

| Decisión | Por qué |
|---|---|
| `journal_mode = WAL` | el servidor lee mientras el trabajador escribe |
| `foreign_keys = ON` y `busy_timeout = 5000` | integridad referencial; esperar en vez de fallar ante un bloqueo breve |
| índices `revisiones(repositorio_id, creada_en)`, `revisiones(creada_en)` (versión 3, por la prueba de volumen), `hallazgos(revision_id)`, `sesiones(usuario_id)` | las consultas del panel y del trabajador |
| `UNIQUE (repositorio_id, numero_pr, sha_cabeza)` | la regla RN-S02 también en la base |
| identificadores UUID en `TEXT` e instantes en milisegundos (`INTEGER`) | los genera el servicio, no la base |
| sin particionamiento | un equipo genera del orden de miles de revisiones al año; SQLite no particiona y, a ese volumen, los índices bastan. Si un cliente llegara a millones de hallazgos, el adaptador se cambia por PostgreSQL con particiones por fecha sin tocar el dominio |

**Permisos.** SQLite no tiene usuarios ni roles: quien puede abrir el
archivo puede leerlo todo. Por eso el control de acceso está en dos capas:
el archivo vive en un volumen de Docker al que solo accede el proceso del
servicio, y cada operación pasa por el permiso del rol en el dominio
(`Autorizado<P>`, sección 5.4). El hash de la clave y el secreto del
*webhook* nunca salen por la API sin ese permiso.

## e) Implementación

El esquema se aplica al abrir una base nueva y su versión se guarda en
`PRAGMA user_version` (hoy, la 3). Una base de la versión 1 o 2 se migra sola al
abrirla, en una transacción, con `migraciones.sql` (en la 2, el `activo` booleano de
los usuarios pasa a `estado` y los hallazgos ganan quién y cuándo se
clasificaron; en la 3 se agrega el índice de la lista general por fecha); una base de una versión desconocida no arranca. Toda fila leída pasa por un esquema zod antes de volverse un tipo
del dominio; una fila que el dominio no admite es un error, no un valor a
medias:

{{codigo sistema/paquetes/adaptadores/sqlite/src/filas.ts aRevision}}

## f) Pruebas de los datos

Tabla: Pruebas de la base de datos del servicio

| Prueba | Qué comprueba |
|---|---|
| «cada estado de la revisión se guarda y se recupera igual» | ida y vuelta de las cuatro variantes |
| «la base no admite dos revisiones del mismo sha de un PR» | la restricción `UNIQUE` |
| «la cola entrega en orden y no entrega dos veces lo tomado» | `UPDATE … RETURNING` atómico |
| «una transacción que lanza no deja nada escrito» | atomicidad |
| «una fila que el dominio no admite es un error» | lectura validada |

Están en `sistema/paquetes/adaptadores/sqlite/src/almacen.test.ts`, y el
flujo completo sobre SQLite en `sistema/pruebas/producto-sqlite.test.ts`.

| Tipo de prueba | Qué se hizo | Resultado |
|---|---|---|
| Rendimiento | la demostración de punta a punta sobre SQLite: encolar, analizar dos archivos con `clang` y publicar | 0,28 s por revisión (tres corridas) |
| Recuperación | «un trabajo interrumpido se marca fallido al arrancar» (`casos.test.ts`) y «una transacción que lanza no deja nada escrito» (`almacen.test.ts`) | en verde |
| Seguridad | consultas siempre preparadas con parámetros (`db.prepare`, ningún SQL armado con texto del usuario); claves solo como hash scrypt; sesión solo como sha256 del token; pruebas de la API sin sesión (401) y con firma mala (401) | en verde |
| Carga sostenida | no se hizo: el servicio es de un solo equipo; queda como trabajo futuro | — |

## g) Despliegue y mantenimiento

La base vive en el volumen `/datos` del contenedor (`centinela-datos` en
`docker-compose.yml`). Respaldarla es copiar `centinela.db` con
`sqlite3 centinela.db ".backup respaldo.db"`, que es seguro con el servicio en
marcha; el respaldo es manual y se recomienda diario. Un cambio de esquema
sube `user_version` y agrega su migración; un binario no arranca sobre una
base de una versión más nueva que la suya.

**Monitoreo.** `GET /salud` responde `{ok: true}` cuando el servidor está en
marcha, y sirve para la comprobación de salud de Docker o de un balanceador.
El servidor y el trabajador escriben una bitácora JSON por línea (revisión
publicada, revisión fallida con su motivo, revisiones interrumpidas al
arrancar), que `docker compose logs` muestra y que cualquier colector de
bitácoras puede leer.

## h) Datos de la evaluación del motor

> **Aquí no hay un SGBD**, y es una decisión. Los datos de la evaluación se
> escriben una vez por ejecución y se leen para cotejar. No hay usuarios
> concurrentes ni transacciones. Lo que importa es que sean **versionables,
> auditables y reproducibles**. Por eso son archivos JSON en el repositorio,
> con claves estables e integridad comprobada por programa.

### a) Análisis de requisitos

Tabla: Requisitos de datos de la evaluación del motor

| Dato | Para qué | Volumen hoy | Restricción |
|---|---|---|---|
| reglas de la norma | generar la tabla del plugin y las etiquetas | 101 mutaciones, 348 reglas | cada regla cita su cláusula C++17 |
| casos del banco | ejecutar y cotejar | 750 casos (342 UB, 306 SAFE, 102 POLICY) | la etiqueta sale de la norma, nunca a mano |
| validación dinámica | comprobar las etiquetas | 852 ejecuciones | 0 contradicciones |
| ejecuciones | evidencia | 750 × 4 condiciones = 3 000 | toda ejecución tiene un `outcome` |
| cotejos y métricas | resultados | uno por caso y condición | reconstruibles desde las ejecuciones |
| código real | evidencia fuera del banco | 4 proyectos, 781 unidades | se guardan avisos y *commit*, no el código |

### b) Diseño conceptual

![Modelo de datos](../diagramas/7-modelo-datos.svg)

`Mutacion` y `Regla` son la raíz: cada caso instancia una regla y su etiqueta
sale de ella. `Ejecucion` registra cómo terminó `clang`; `Cotejo` admite el
veredicto `Incident` y separa los avisos posibles (`PolicyWarned`).

### c) Diseño lógico

| Entidad | Archivo | Clave | Integridad |
|---|---|---|---|
| Mutación y Regla | `norma/matriz.json` | `id` de la mutación + (`categoria`, `relacion`) | `efecto ∈ {preserves, invalidates, depends}`; `clausula` no vacía; `condicion` sólo si `depends` (`gen_tabla.py` lo comprueba) |
| Caso | `test/corpus_truth.json` | nombre de la función | `esperado` = peor efecto de `handles` (RN-001) |
| Validación | `test/runtime_validation_results.json` | caso + escenario | ninguna contradicción con la etiqueta |
| Condición | `test/experimento/metricas.json` → `meta.condiciones` | nombre | las condiciones experimentales difieren de `Reference` sólo en el checker (RN-002) |
| Ejecución | `test/experimento/ejecucion.json` → `runs` | caso + condición | `outcome` es uno de cinco |
| Aviso | dentro de cada ejecución (`warnings`) | ejecución + línea + columna | `clase` es `Confirmed`, `Possible` u `Other` |
| Cotejo | `test/experimento/cotejo.json` → `matches` | caso + condición | un `Incident` nunca es `TN` (RN-005) |
| Métrica | `test/experimento/metricas.json` → `metricas` | condición + grupo + valor | `null` cuando el denominador es 0 |
| Código real | `test/codigo_real/avisos.json`, `inyeccion.json` | proyecto + archivo | `commit` del proyecto registrado |

**Normalización.** La etiqueta vive **sólo** en el caso; el cotejo la
consulta por nombre. Tipos: enteros para conteos, texto controlado para
clases, `null` explícito para lo no definido, UTF-8.

### d) Diseño físico

```
norma/matriz.json                       la norma (fuente única)
test/
├── corpus.cpp, corpus_truth.json       el banco y sus etiquetas
├── runtime_validation_results.json     validación dinámica
├── experimento/
│   ├── ejecucion.json                  meta + runs (3 000)
│   ├── cotejo.json                     matches + no_atribuidos
│   └── metricas.json                   meta + tiempos + métricas por grupo
└── codigo_real/
    ├── avisos.json                     ninja, leveldb, yaml-cpp, RocksDB
    └── inyeccion.json                  defectos sembrados
```

`meta` lleva la versión de `clang` y de libstdc++, el sha256 del plugin, del
banco y de las etiquetas, y la orden exacta de cada condición (RN-007). Los
«índices» son diccionarios por clave que el arnés construye al cargar; con
este volumen no hace falta más.

### e) Implementación

- `bench/gen_corpus.py` + `bench/etiquetar.py`: escriben el banco y sus
  etiquetas desde la norma.
- `bench/experimento.py`: escribe `ejecucion.json`, `cotejo.json` y
  `metricas.json`.
- `bench/codigo_real.py` y `bench/inyeccion.py`: escriben `test/codigo_real/`.
- `bench/gen_book.py`: lee esos archivos y genera las tablas del libro. Ninguna
  cifra se escribe a mano.

### f) Pruebas de los datos

Tabla: Pruebas de los datos de la evaluación

| Prueba | Comprueba | Dónde |
|---|---|---|
| leyes de la norma | cláusula presente, efecto válido, tabla total | `gen_tabla.py`, gtests `Norma.*` |
| coherencia norma–banco | la etiqueta de cada caso es la que da su regla | gtest `Banco.ElVeredictoDelNucleoEsLaEtiqueta` |
| conteos | las métricas son la suma de los cotejos (monoide) | `bench/pruebas_evaluacion.py` |
| incidentes visibles | ningún `Crash` o `Timeout` figura como `TN` | `bench/pruebas_evaluacion.py` |
| métricas indefinidas | 0/0 es `null`, no 0 % | `bench/pruebas_evaluacion.py` |

### g) Despliegue y mantenimiento

- El experimento del informe corresponde al *tag* `banco-1`: el banco
  sellado y los archivos de `test/experimento/` del mismo *commit*.
- Un cambio de forma en los archivos se hace junto con el cambio del arnés y
  del generador del libro, en el mismo *commit*.
- Respaldo: el remoto de GitHub.
