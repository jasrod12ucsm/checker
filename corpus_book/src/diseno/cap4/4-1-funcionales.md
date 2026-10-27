# 4.1 Requerimientos funcionales

## Requerimientos de software

### a) Propósito

Especificar **Centinela C++**, un servicio web que revisa automáticamente
los *pull requests* de C++ de un equipo y comenta en GitHub los usos de
iteradores, referencias y punteros invalidados, antes de que el código se
integre. Por dentro, el análisis lo hace el checker
`ucsm.ContainerInvalidation`, cuyas reglas salen de la norma de C++17 y que
se evaluó con un banco de 750 casos. Cada requisito se acompaña de la prueba
que lo demuestra y de la evidencia registrada.

### b) Componentes

| Componente | Qué es | Quién lo usa |
|---|---|---|
| **Centinela C++** (servicio web) | aplicación con autenticación, panel web y API: conecta repositorios de GitHub, recibe sus *webhooks*, revisa cada *pull request* y publica comentarios y el estado del commit | Administrador, Desarrollador, GitHub |
| **Motor de análisis**: el checker `ucsm.ContainerInvalidation` | plugin de Clang Static Analyzer (LLVM 21) que avisa del uso de un iterador, una referencia o un puntero a un elemento después de una mutación que lo invalida según C++17 | Centinela (lo invoca por cada archivo) |
| **Norma** `norma/matriz.json` | las reglas de invalidación de C++17 como datos: 101 mutaciones, 348 reglas, cada una con su cláusula | Mantenedor |
| **Banco y arnés** `bench/` | 750 casos etiquetados desde la norma, su validación dinámica y el experimento que mide al motor frente a CSA | Evaluador |
| **GitHub** | sistema externo: aloja los repositorios, envía los *webhooks* y aplica la protección de rama | — |

### c) Alcance del producto

Centinela es un servicio de un solo cliente (*single-tenant*): una
organización lo despliega con Docker y lo usa con su cuenta de GitHub. Tiene
dos roles, administrador y desarrollador. Revisa los archivos `.cpp`, `.cc` y
`.cxx` que cambian en un *pull request*, con la política (`Silent` o
`Possibly`) que el administrador eligió para el repositorio. El motor cubre
`vector`, `deque`, `list`, `forward_list`, `set`, `multiset`, `map`,
`multimap`, `unordered_set` y `unordered_map`, con las mutaciones de C++17 de
la norma, dentro de una unidad de traducción. No cubre `std::string`,
`std::array`, los adaptadores, C++20 ni el análisis entre unidades; no ofrece
varios clientes aislados (*multi-tenant*), facturación ni otros proveedores
que GitHub.

Limitaciones del servicio:

- Analiza **cada archivo cambiado por separado**, sin la base de compilación
  (`compile_commands.json`) del proyecto del cliente: agrega como rutas de
  inclusión la raíz, `include/`, `src/` y la carpeta del archivo. Un archivo
  que necesita otras rutas, macros o cabeceras generadas no compila, y se
  informa como **no analizado**, nunca como limpio (RN-S05). El análisis de un
  proyecto entero desde su base de compilación es del motor (RF-03) y se usó
  en la evaluación con código real, no en el servicio.
- Usa la misma configuración del motor que la evaluación con código real
  (`-analyzer-inlining-mode=all`, D-22), con un tiempo máximo de 120 s por
  archivo.
- Necesita una URL pública con HTTPS para recibir los *webhooks* de GitHub.
- El bloqueo tras 10 ingresos fallidos se lleva en la memoria del servidor:
  se reinicia si el servicio se reinicia.

### d) Referencias

Los requisitos derivan de los objetivos (sección 1.4), de la especificación
de C++17 (N4659, cláusulas de contenedores), de la regla SEI CERT CTR51-CPP,
del protocolo del banco y de la API REST y los *webhooks* de GitHub. La API de
checkers de LLVM 21 condiciona la implementación del motor.

### e) Funcionalidades del producto

| Grupo | Requisitos | Casos de uso |
|---|---|---|
| Acceder al sistema | RF-S01 | CU-S01, CU-S02 |
| Conectar repositorios | RF-S02 | CU-S03 |
| Revisar pull requests | RF-S03 | CU-S04, CU-S05 |
| Consultar revisiones | RF-S04 | CU-S06 |
| Clasificar hallazgos | RF-S05 | CU-S07 |
| Analizar código (motor) | RF-01 a RF-04 | CU-S04 (RF-03: verificación con código real) |
| Seguir handles (motor) | RF-05 a RF-07 | CU-S04 |
| Aplicar la norma (motor) | RF-08 a RF-10 | CU-S04 |
| Diagnosticar (motor) | RF-11, RF-12 | CU-S04, CU-S06 |
| Medir el motor | RF-13 a RF-15 | verificación (sección 7.4) |
| Mantener el motor | RF-16, RF-17 | verificación (sección 7.4) |

### f) Clases y características de usuarios

| Usuario | Qué hace con el sistema | Qué necesita saber |
|---|---|---|
| Administrador | es quien se registró primero o a quien otro administrador dio el rol; aprueba y gestiona los usuarios, conecta los repositorios, elige la política y si un problema bloquea el merge; también hace todo lo del desarrollador | administrar un repositorio de GitHub (token, *webhook*, protección de rama) |
| Desarrollador | se registra y espera la aprobación; recibe los comentarios en su *pull request*, consulta las revisiones en el panel, marca falsos positivos y pide revisiones | C++ y los contenedores de la STL |
| GitHub (sistema externo) | avisa de cada *pull request* abierto o actualizado y recibe los comentarios y el estado del commit | — |
| Evaluador y mantenedor (equipo del proyecto) | miden el motor con el banco y corrigen o amplían la norma; no usan el servicio | C++, CMake, la API de CSA, Python |

### g) Entorno operativo

| Elemento | Especificación (fijada en las imágenes `checker:llvm21` y `centinela:local`) |
|---|---|
| Sistema | GNU/Linux x86-64, Ubuntu 24.04 en Docker |
| Servicio web | Node.js 22, TypeScript 5.9, Fastify 5, SQLite (better-sqlite3 12) |
| Cliente | navegador web actual; GitHub.com con un token de acceso |
| Analizador | Clang/LLVM 21.1.8, Clang Static Analyzer, plugin `libContainerInvalidation.so` |
| Biblioteca estándar | libstdc++ 13.3 |
| Lenguaje analizado | C++17 (N4659) |
| Construcción y pruebas | CMake + Ninja, GoogleTest, `lit`; Vitest para el servicio |
| Arnés | Python 3.12, sin dependencias externas |

## Especificación de los requerimientos funcionales del sistema

### RF-S01 Registrar y autenticar usuarios y controlar su acceso

| Campo | Especificación |
|---|---|
| Descripción | Centinela no trae usuarios predefinidos: cada persona se registra con su correo, su nombre y su clave. La primera queda como administradora; las siguientes, como desarrolladoras pendientes hasta que un administrador las apruebe. Cada usuario está `Pendiente`, `Activo` o `Desactivado`; solo el activo entra con su correo y su clave, y solo hace lo que su rol permite. El administrador aprueba o rechaza registros, desactiva y reactiva cuentas, cambia el rol y también puede crear usuarios |
| Precondición | para registrarse, ninguna; para entrar, una cuenta en estado `Activo` |
| Flujo normal | 1. la persona se registra (la primera entra directamente como administradora); 2. un administrador aprueba a las siguientes y les da un rol; 3. el usuario escribe correo y clave en la pantalla de ingreso y el sistema verifica la clave contra su hash scrypt; 4. abre una sesión de 8 horas en una cookie `httpOnly`, `SameSite=Strict`; 5. cada pantalla consulta la sesión y el permiso antes de mostrar o hacer algo |
| Postcondición | sesión abierta; las operaciones fuera del rol responden «sin permiso» |
| Excepciones | correo o clave incorrectos: el mismo mensaje en ambos casos; 10 fallos seguidos: bloqueo de 15 minutos; cuenta `Pendiente`: no entra («Tu cuenta espera la aprobación de un administrador.»); cuenta `Desactivado` (rechazada o desactivada): no entra («Tu cuenta está desactivada: pide a un administrador que la reactive.»), y al desactivarla se cierran sus sesiones; nadie vuelve a `Pendiente`; correo ya registrado: se rechaza; clave de menos de 10 caracteres o sin letras y números: se rechaza; nadie se desactiva ni se cambia el rol a sí mismo |
| Prioridad | Alta |
| Objetivo | OE2 |
| Cómo se demuestra | pruebas de `identidad.test.ts`, `casos.test.ts` (RF-S01) y `api.test.ts` (RF-S01 registro y autenticación) |
| Evidencia | `npm test` en `sistema/`: verde |

### RF-S02 Conectar y configurar repositorios

| Campo | Especificación |
|---|---|
| Descripción | El administrador conecta un repositorio de GitHub por su nombre (`propietario/nombre`), elige la política del análisis (`Silent` o `Possibly`) y si un problema bloquea el merge; el sistema le da la URL y el secreto del *webhook* |
| Precondición | RF-S01 con rol administrador |
| Flujo normal | 1. el administrador escribe el nombre y elige política y bloqueo; 2. el sistema genera un secreto aleatorio y guarda el repositorio; 3. muestra la URL `/webhooks/github` y el secreto para configurarlos en GitHub |
| Postcondición | repositorio activo; sus *webhooks* se aceptan |
| Excepciones | nombre que no es `propietario/nombre`: se rechaza; repositorio ya conectado: se informa; desconectar no borra sus revisiones y reconectar le da un secreto nuevo |
| Prioridad | Alta |
| Objetivo | OE2 |
| Cómo se demuestra | `repositorios.test.ts`, `casos.test.ts` (RF-S02), `api.test.ts` (conectar, configurar y desconectar) |
| Evidencia | `npm test`: verde |

### RF-S03 Revisar automáticamente cada pull request

| Campo | Especificación |
|---|---|
| Descripción | Cuando se abre, reabre o actualiza un *pull request* de un repositorio conectado, el sistema analiza los archivos C++ que cambiaron con el checker, comenta cada hallazgo en su línea y pone el estado del commit en `failure` si hay problemas y el repositorio bloquea el merge |
| Precondición | RF-S02; el *webhook* de GitHub configurado con el secreto |
| Flujo normal | 1. GitHub envía el evento `pull_request` firmado; 2. el sistema verifica la firma HMAC-SHA256 y encola una revisión del commit de cabeza (estado `pending`); 3. el trabajador descarga el código, corre `clang` con el checker sobre cada archivo C++ cambiado y lee los avisos con su ruta; 4. suprime los hallazgos que el equipo marcó como falso positivo; 5. publica una revisión con comentarios en las líneas del diff y un resumen; 6. pone el estado del commit en `success` o `failure` |
| Postcondición | revisión `Publicada` con su veredicto, o `Fallida` con su motivo |
| Excepciones | firma inválida o repositorio no conectado: se rechaza; el mismo commit no se revisa dos veces; acciones que no cambian el código (cerrar, etiquetar): se ignoran; un archivo que no compila se informa como no analizado; si `clang` o GitHub fallan, la revisión queda `Fallida` y el commit en `error`; si el proceso se cae, al volver marca como fallidas las revisiones a medias |
| Prioridad | Alta |
| Objetivo | OE2 |
| Cómo se demuestra | `revisiones.test.ts`, `casos.test.ts` (RF-S03), `api.test.ts` (webhook), `clang.test.ts` (clang y checker reales) y la demostración `demo/demostrar.ts` |
| Evidencia | `docker compose run --rm sistema-pruebas`: verde; la demostración publica 2 comentarios y estado `failure` sobre el PR de ejemplo |

### RF-S04 Consultar revisiones y hallazgos

| Campo | Especificación |
|---|---|
| Descripción | Cualquier usuario activo ve la lista de revisiones (filtrable por repositorio) y el detalle de cada una: estado, veredicto, resumen y cada hallazgo con su archivo, línea, clase (confirmado o posible), mensaje y ruta (dónde se obtuvo el handle, qué lo invalidó y dónde se usó) |
| Precondición | RF-S01 |
| Flujo normal | 1. el usuario abre el panel; 2. elige una revisión; 3. el sistema muestra su detalle y el enlace al *pull request* |
| Postcondición | — (solo lectura) |
| Excepciones | revisión inexistente: «no existe»; usuario desactivado: sin acceso |
| Prioridad | Alta |
| Objetivo | OE2 |
| Cómo se demuestra | `casos.test.ts` (RF-S04 y RF-S05), `api.test.ts` (detalle con hallazgos) |
| Evidencia | `npm test`: verde |

### RF-S05 Clasificar hallazgos

| Campo | Especificación |
|---|---|
| Descripción | Un usuario marca un hallazgo como confirmado o como falso positivo. Un falso positivo ya no se comenta ni bloquea en las revisiones siguientes del mismo repositorio, aunque el código se mueva de línea |
| Precondición | RF-S04 |
| Flujo normal | 1. el usuario abre el hallazgo; 2. lo marca; 3. el sistema guarda la clasificación con quién la hizo y cuándo y, si es falso positivo, agrega su huella (archivo y mensaje, sin números de línea) a las descartadas del repositorio |
| Postcondición | las revisiones nuevas o reintentadas cuentan ese hallazgo como suprimido |
| Excepciones | hallazgo inexistente: «no existe»; desmarcar un falso positivo lo vuelve a reportar |
| Prioridad | Media |
| Objetivo | OE2 |
| Cómo se demuestra | `revisiones.test.ts` (clasificar, huella), `casos.test.ts` («un falso positivo deja de reportarse al reintentar la revisión») |
| Evidencia | `npm test`: verde |

## Especificación de los requerimientos del motor de análisis

Estos requisitos son del checker que Centinela invoca en RF-S03. Se
especificaron y se verificaron antes que el servicio, con el banco de casos.

### RF-01 Registrar el checker

| Campo | Especificación |
|---|---|
| Descripción | El checker se carga en `clang` como plugin y aparece en el catálogo de CSA con el nombre `ucsm.ContainerInvalidation` y sus opciones `PolicyMode` y `Debug` |
| Precondición | `libContainerInvalidation.so` construido contra el mismo LLVM 21 de la imagen |
| Flujo normal | `clang -cc1 -load libContainerInvalidation.so -analyzer-checker-help` |
| Postcondición | el checker figura en la lista con su descripción |
| Excepciones | versión de API distinta: `clang` rechaza el plugin con un error; nunca analiza en silencio sin él |
| Prioridad | Alta |
| Objetivo | OE2 |
| Cómo se demuestra | prueba `lit` `registro.cpp` |
| Evidencia | `registro.cpp` en verde |

### RF-02 Activar y desactivar el checker

| Campo | Especificación |
|---|---|
| Descripción | El checker se activa o se deja fuera con `-analyzer-checker`, sin recompilar `clang` |
| Precondición | RF-01 |
| Flujo normal | la misma orden de `clang` con y sin `ucsm.ContainerInvalidation` en `-analyzer-checker` |
| Postcondición | sólo la corrida con el checker da sus avisos; el resto de la configuración es idéntico |
| Excepciones | nombre de checker mal escrito: `clang` informa el error |
| Prioridad | Alta |
| Objetivo | OE2, OE3 |
| Cómo se demuestra | condiciones `Reference` y `Experimental` del experimento (RF-13) |
| Evidencia | `meta.condiciones` de `test/experimento/metricas.json`: difieren sólo en el checker |

### RF-03 Analizar un proyecto desde su base de compilación

| Campo | Especificación |
|---|---|
| Descripción | El checker analiza un proyecto entero a partir de su `compile_commands.json`, una unidad de traducción por invocación |
| Precondición | el proyecto genera `compile_commands.json` (CMake) |
| Flujo normal | `bench/codigo_real.py` lee la base, invoca `clang` con el checker por unidad y guarda los avisos |
| Postcondición | un registro por unidad: avisos, tiempo y código de salida |
| Excepciones | una unidad que no compila se registra como fallo, no como «sin avisos» |
| Prioridad | Alta |
| Objetivo | OE2 |
| Cómo se demuestra | `bench/codigo_real.py` sobre ninja, leveldb, yaml-cpp y RocksDB |
| Evidencia | 781 unidades, 0 caídas de `clang`, 0 avisos falsos confirmados (`test/codigo_real/avisos.json`) |

### RF-04 Elegir la política ante lo que depende del estado

| Campo | Especificación |
|---|---|
| Descripción | El usuario elige con `PolicyMode=Silent` (por omisión: sólo avisos confirmados) o `PolicyMode=Possibly` (también avisos posibles) |
| Precondición | RF-02 |
| Flujo normal | `-analyzer-config ucsm.ContainerInvalidation:PolicyMode=Possibly` |
| Postcondición | lo que depende del estado da aviso posible sólo con `Possibly`; los confirmados no cambian |
| Excepciones | valor no reconocido: se usa `Silent` |
| Prioridad | Alta |
| Objetivo | OE2 |
| Cómo se demuestra | `lit` `garantias.cpp`; condiciones `Experimental-Silent` y `Experimental-Possibly` |
| Evidencia | 102/102 casos `POLICY` con aviso posible en `Possibly`, 0/102 en `Silent` |

### RF-05 Seguir iteradores

| Campo | Especificación |
|---|---|
| Descripción | El checker sigue los iteradores obtenidos con `begin`, `find`, `lower_bound`, `upper_bound`, `insert` y `emplace` (también el `.first` del par), sus copias y sus movimientos (`++`, `--`, `+ k`, `std::next`, `std::advance`) |
| Precondición | RF-02 |
| Flujo normal | obtención → mutación → uso del iterador |
| Postcondición | aviso si la mutación lo invalida según la norma |
| Excepciones | iterador de origen desconocido: no se sigue (no se inventa un contenedor) |
| Prioridad | Alta |
| Objetivo | OE2 |
| Cómo se demuestra | `lit` `iteradores.cpp` (20 funciones) |
| Evidencia | `iteradores.cpp` en verde; banco: 128/128 UB de iterador |

### RF-06 Seguir referencias y punteros a elementos

| Campo | Especificación |
|---|---|
| Descripción | El checker sigue las referencias y los punteros obtenidos con `*it`, `it->`, `c[i]`, `at`, `front`, `back`, `data` y `&` |
| Precondición | RF-02 |
| Flujo normal | obtención → mutación → lectura, escritura, llamada a un método o paso por referencia del elemento |
| Postcondición | aviso si la mutación invalida la referencia según la norma |
| Excepciones | ninguna propia |
| Prioridad | Alta |
| Objetivo | OE2 |
| Cómo se demuestra | `lit` `referencias.cpp` (20 funciones); banco |
| Evidencia | 214/214 UB con referencia o puntero (CSA solo: 0 sobre el handle sostenido) |

### RF-07 No avisar en los usos válidos

| Campo | Especificación |
|---|---|
| Descripción | El checker no avisa en el iterador que devuelve la mutación (`it = c.erase(it)`), en uno obtenido de nuevo, en uno de otro contenedor ni al pasar un puntero por valor |
| Precondición | RF-05, RF-06 |
| Flujo normal | la mutación reemplaza la validez del handle reasignado |
| Postcondición | ningún aviso |
| Excepciones | — |
| Prioridad | Alta |
| Objetivo | OE2 |
| Cómo se demuestra | casos `SAFE` del banco; `lit` |
| Evidencia | 0 avisos en 306 casos `SAFE`, incluidos 12 de iterador devuelto |

### RF-08 Aplicar la regla de C++17

| Campo | Especificación |
|---|---|
| Descripción | Ante cada mutación, el checker aplica la regla que corresponde a la operación, al contenedor, a la categoría del handle y a la posición del elemento frente al punto de la mutación (antes, en, después, fin, dentro de un rango) |
| Precondición | la tabla normativa generada desde `matriz.json` (RF-17) |
| Flujo normal | reconocer la mutación → buscar la regla → actualizar la validez de cada handle del contenedor |
| Postcondición | cada handle queda válido, inválido o no resuelto |
| Excepciones | posición desconocida: el handle queda no resuelto, nunca válido por omisión |
| Prioridad | Alta |
| Objetivo | OE2 |
| Cómo se demuestra | gtest `Banco.ElVeredictoDelNucleoEsLaEtiqueta`; experimento |
| Evidencia | el núcleo coincide con la norma celda por celda; 342/342 UB detectados |

### RF-09 Tratar lo que depende del estado

| Campo | Especificación |
|---|---|
| Descripción | Cuando la invalidación depende de la capacidad o del factor de carga, el checker no la da por confirmada; un `reserve(c.size() + k)` previo cubre `k` inserciones |
| Precondición | RF-08 |
| Flujo normal | la regla dice «depende» → se gasta el crédito de `reserve` si lo hay; si no, el handle queda no resuelto |
| Postcondición | aviso posible (con `Possibly`) o ningún aviso (con la garantía) |
| Excepciones | `shrink_to_fit` nunca se garantiza |
| Prioridad | Alta |
| Objetivo | OE2 |
| Cómo se demuestra | `lit` `garantias.cpp`; casos con `reserve` del banco |
| Evidencia | 0 avisos en 54 casos con `reserve`; gtests de crédito |

### RF-10 Tratar las llamadas opacas

| Campo | Especificación |
|---|---|
| Descripción | Una llamada opaca que recibe el contenedor (o el objeto que lo contiene) hace olvidar los handles válidos; uno ya invalidado sigue invalidado |
| Precondición | RF-08 |
| Flujo normal | CSA notifica el escape → el checker borra los handles válidos de ese contenedor |
| Postcondición | sin aviso tras la llamada; aviso si el handle ya era inválido |
| Excepciones | — |
| Prioridad | Media |
| Objetivo | OE2 |
| Cómo se demuestra | `lit` `garantias.cpp` (`opaque`, `escaped_after_invalid`) |
| Evidencia | en verde; evitó falsos positivos en RocksDB |

### RF-11 Explicar la causa en el aviso

| Campo | Especificación |
|---|---|
| Descripción | El aviso dice la categoría del handle, el contenedor, la operación y su línea, y si es confirmado o posible; el posible dice qué garantía falta |
| Precondición | un uso inválido o no resuelto |
| Flujo normal | el checker arma el texto con los datos de la causa guardada en el estado |
| Postcondición | un aviso por handle y camino |
| Excepciones | — |
| Prioridad | Alta |
| Objetivo | OE2 |
| Cómo se demuestra | `expected-warning` en las pruebas `lit` |
| Evidencia | 30 avisos comprobados palabra por palabra en `lit` |

### RF-12 Mostrar la ruta del defecto

| Campo | Especificación |
|---|---|
| Descripción | El diagnóstico trae una nota donde se obtuvo el handle y otra en la mutación que lo invalidó, además de las notas de CSA hasta el uso |
| Precondición | RF-11 |
| Flujo normal | `-analyzer-output=text` o SARIF |
| Postcondición | la ruta *obtención → mutación → uso* visible en la salida |
| Excepciones | un handle copiado muestra la nota de la copia, no la de la obtención original |
| Prioridad | Media |
| Objetivo | OE2 |
| Cómo se demuestra | `lit` `rutas.cpp` con `-analyzer-output=text` y `expected-note` |
| Evidencia | 9 notas comprobadas en `rutas.cpp` |

### RF-13 Ejecutar el experimento

| Campo | Especificación |
|---|---|
| Descripción | El arnés corre cada caso del banco en cuatro condiciones: CSA; CSA + checker `Silent`; CSA + checker `Possibly`; checker sin los `alpha.cplusplus`. Una invocación por caso y condición |
| Precondición | plugin construido (RF-16) y banco generado (RF-15) |
| Flujo normal | `python3 bench/experimento.py` |
| Postcondición | `test/experimento/{ejecucion,cotejo,metricas}.json` con versiones y sha256 |
| Excepciones | compilación fallida, caída, tiempo agotado o salida ilegible: incidente registrado |
| Prioridad | Alta |
| Objetivo | OE1, OE3 |
| Cómo se demuestra | la ejecución misma |
| Evidencia | 3 000 ejecuciones, 0 incidentes |

### RF-14 Cotejar por sitio

| Campo | Especificación |
|---|---|
| Descripción | El arnés coteja cada aviso con el sitio: acierta sólo si cae sobre un handle que la norma da por inválido; separa confirmados, posibles e incidentes, y una caída nunca cuenta como acierto |
| Precondición | RF-13 |
| Flujo normal | normalizar SARIF → atribuir a función y sitio → cotejar → agregar |
| Postcondición | conteos TP/FP/FN/TN, posibles e incidentes por contenedor, operación, categoría y forma |
| Excepciones | denominador 0: métrica indefinida, no 0 % |
| Prioridad | Alta |
| Objetivo | OE3 |
| Cómo se demuestra | `python3 bench/pruebas_evaluacion.py` |
| Evidencia | 11 leyes de la evaluación en verde |

### RF-15 Generar y validar el banco

| Campo | Especificación |
|---|---|
| Descripción | El banco se genera desde la norma y sus etiquetas se validan ejecutando cada caso con libstdc++ Debug y con ASan/UBSan |
| Precondición | `norma/matriz.json` válida |
| Flujo normal | `bench/gen_corpus.py` → `bench/run_runtime_validation.py` |
| Postcondición | `test/corpus.cpp`, `test/corpus_truth.json` y los resultados de la validación |
| Excepciones | una ejecución contradice la etiqueta: el banco no se publica |
| Prioridad | Alta |
| Objetivo | OE1 |
| Cómo se demuestra | las dos órdenes |
| Evidencia | 750 casos; 852 ejecuciones, 0 contradicciones |

### RF-16 Construir y verificar el plugin

| Campo | Especificación |
|---|---|
| Descripción | El plugin se construye y se prueba en la imagen fijada con una sola orden |
| Precondición | Docker con la imagen `checker:llvm21` |
| Flujo normal | `docker compose run --rm plugin` (CMake, gtest, `lit`) |
| Postcondición | `libContainerInvalidation.so` y las pruebas en verde |
| Excepciones | una prueba falla: la orden termina con error |
| Prioridad | Alta |
| Objetivo | OE2 |
| Cómo se demuestra | la orden |
| Evidencia | 40 gtests y 5 archivos `lit` en verde; `calidad` en verde |

### RF-17 Mantener la norma como datos

| Campo | Especificación |
|---|---|
| Descripción | Corregir una regla en `matriz.json` regenera la tabla del plugin; `gen_tabla.py` rechaza una norma que rompe sus leyes |
| Precondición | RF-16 |
| Flujo normal | editar `matriz.json` → construir (RF-16) → regenerar el banco (RF-15) |
| Postcondición | checker y etiquetas dicen lo mismo |
| Excepciones | falta la cláusula o el efecto no es válido: no se genera la tabla |
| Prioridad | Media |
| Objetivo | OE1, OE2 |
| Cómo se demuestra | gtests `Norma.*` y comprobaciones de `gen_tabla.py` |
| Evidencia | `Norma.LaTablaEsTotal`, `Norma.InvalidarODependerCitaSuClausula` en verde |

## Matriz de trazabilidad de requerimientos

| Requisito | Objetivo | Caso de uso | Componente | Evidencia |
|---|---|---|---|---|
| RF-S01 | OE2 | CU-S01, CU-S02 | `sistema/paquetes/contextos/identidad`, `adaptadores/cripto`, `adaptadores/http` | `identidad.test.ts`, `api.test.ts` |
| RF-S02 | OE2 | CU-S03 | `contextos/repositorios` | `repositorios.test.ts`, `api.test.ts` |
| RF-S03 | OE2 | CU-S04, CU-S05 | `contextos/revisiones`, `producto`, `adaptadores/github`, `adaptadores/analizador` | `casos.test.ts`, `clang.test.ts`, demostración |
| RF-S04 | OE2 | CU-S06 | `producto`, `adaptadores/http` | `api.test.ts` |
| RF-S05 | OE2 | CU-S07 | `contextos/revisiones` | `revisiones.test.ts`, `casos.test.ts` |
| RF-01, RF-02 | OE2 | CU-S04 | `plugin/registro` | `registro.cpp`; condiciones del experimento |
| RF-03 | OE2 | verificación | `bench/codigo_real.py` | 781 unidades, 0 avisos falsos confirmados |
| RF-04 | OE2 | CU-S03, CU-S04 | `plugin/registro`, `plugin/dominio` | `garantias.cpp`; 102/102 `POLICY` |
| RF-05 a RF-07 | OE2 | CU-S04 | `plugin/acl`, `plugin/checker` | `iteradores.cpp`, `referencias.cpp`; 0 FP |
| RF-08 a RF-10 | OE2 | CU-S04 | `plugin/dominio` | gtests; 342/342 UB |
| RF-11, RF-12 | OE2 | CU-S04, CU-S06 | `plugin/checker/Messages.cpp` | `lit`; SARIF |
| RF-13, RF-14 | OE1, OE3 | verificación | `bench/experimento.py` | `metricas.json`; 11 leyes |
| RF-15 | OE1 | verificación | `bench/gen_corpus.py`, `bench/etiquetar.py` | 852 ejecuciones, 0 contradicciones |
| RF-16, RF-17 | OE2 | verificación | `plugin/CMakeLists.txt`, `norma/` | gtests, `lit` |

## Reglas de negocio

| ID | Regla |
|---|---|
| RN-S01 | No hay usuarios predefinidos: la primera cuenta registrada es administradora y `Activo`, y las demás quedan `Pendiente` hasta que un administrador las aprueba (`Activo`) o las rechaza (`Desactivado`). Solo un administrador aprueba usuarios y conecta repositorios; el desarrollador consulta, clasifica y pide revisiones |
| RN-S02 | Un commit (el sha de cabeza de un *pull request*) se revisa una sola vez; repetirlo es reintentar la misma revisión |
| RN-S03 | Un hallazgo marcado como falso positivo no cuenta para el veredicto ni se comenta en las revisiones siguientes del repositorio |
| RN-S04 | Una revisión tiene problemas si queda al menos un hallazgo sin suprimir; bloquea el merge solo si el repositorio lo pide |
| RN-S05 | Un archivo que no compila no se da por limpio: se informa como no analizado |
| RN-001 | La etiqueta de un caso sale de la norma: es el peor efecto que la norma da a cualquiera de sus handles (el sostenido y, en `bucle`, el iterador de control) |
| RN-002 | Las condiciones de referencia y experimental difieren sólo en el checker; la cuarta condición quita además los `alpha.cplusplus` y se informa aparte |
| RN-003 | Nada que dependa del estado se informa como confirmado, y nada no resuelto se da por válido sin una garantía |
| RN-004 | Un aviso posible nunca cuenta como acierto ni como falso positivo: se publica aparte |
| RN-005 | Una compilación fallida, una caída o un tiempo agotado es un incidente, nunca un verdadero negativo |
| RN-006 | Un aviso acierta sólo si cae sobre un handle que la norma da por inválido (cotejo por sitio) |
| RN-007 | Cada resultado lleva la versión de `clang`, de libstdc++ y el sha256 del plugin y del banco |

## Requerimientos de interfaces

| ID | Interfaz | Qué pasa por ella |
|---|---|---|
| INT-S01 | Panel web y API HTTP de Centinela | JSON bajo `/api` con cookie de sesión (sección 5.6) |
| INT-S02 | *Webhook* de GitHub | `POST /webhooks/github`, evento `pull_request`, firma `X-Hub-Signature-256` |
| INT-S03 | API REST de GitHub | datos del PR, archivos y diff, *tarball* del commit, revisión con comentarios, estado del commit |
| INT-S04 | Motor de análisis | `clang++ --analyze` con el plugin, una invocación por archivo; salida de texto con la ruta |
| INT-001 | API de checkers de CSA (LLVM 21) | `checkPostCall`, `checkPreCall`, `checkLocation`, `checkBind`, `checkPointerEscape`, `checkDeadSymbols`; `ProgramState` |
| INT-002 | Línea de comandos de `clang` | `-Xclang -load`, `-analyzer-checker`, `-analyzer-config ucsm.ContainerInvalidation:PolicyMode=…` |
| INT-003 | Base de compilación | `compile_commands.json` del proyecto analizado |
| INT-004 | Salida | avisos de CSA en texto, plist o SARIF; el arnés lee SARIF |
| INT-005 | Norma | `norma/matriz.json` → `NormTable.inc` generado en la construcción |
| INT-006 | Resultados | `test/experimento/ejecucion.json`, `cotejo.json`, `metricas.json` |

El checker no lee `compile_commands.json`: lo lee quien lo invoca
(`bench/codigo_real.py` o el sistema de construcción del usuario), que pasa a
`clang` las opciones de cada unidad.
