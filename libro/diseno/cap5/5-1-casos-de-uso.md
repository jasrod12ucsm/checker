# 5.1 Casos de uso

![Casos de uso](../../diagramas/5-1-casos-de-uso.svg)

El sistema es **Centinela C++**, un servicio web. Sus actores son quienes lo
usan: el **administrador** y el **desarrollador** del equipo cliente, y
**GitHub**, que avisa de cada *pull request*. El administrador hereda lo
que hace el desarrollador. El checker no es un actor: es la parte del
sistema que analiza el código (caso incluido en CU-S04).

| Caso | Actor | Flujo principal | Requisitos |
|---|---|---|---|
| **CU-S01** Registrarse e iniciar sesión | Desarrollador, Administrador | 1. abre Centinela y se registra con correo, nombre y clave; 2. si es la primera cuenta, queda como administradora y entra; si no, queda pendiente de aprobación; 3. ya aprobada, escribe su correo y su clave; 4. el sistema verifica la clave y abre una sesión de 8 horas; 5. ve el panel con las opciones de su rol y al salir cierra la sesión | RF-S01 |
| **CU-S02** Aprobar y gestionar usuarios | Administrador | 1. abre «Usuarios» y ve los registros pendientes; 2. aprueba a cada uno con un rol, o lo rechaza (queda `Desactivado` y se puede reactivar después); 3. puede desactivar a un usuario (sus sesiones se cierran), reactivarlo, cambiarle el rol o crear uno directamente | RF-S01 |
| **CU-S03** Conectar y configurar un repositorio | Administrador | 1. abre «Repositorios» y escribe `propietario/nombre`; 2. elige la política (`Silent`: solo confirmados; `Possibly`: también posibles) y si un problema bloquea el merge; 3. el sistema muestra la URL y el secreto del *webhook*; 4. el administrador los pega en GitHub (*Settings → Webhooks*, evento *Pull requests*) | RF-S02 |
| **CU-S04** Revisar un pull request automáticamente | GitHub | 1. un desarrollador abre o actualiza un *pull request*; 2. GitHub envía el *webhook* firmado; 3. el sistema verifica la firma, encola la revisión y marca el commit como `pending`; 4. analiza con `clang` y el checker cada archivo C++ cambiado; 5. comenta cada hallazgo en su línea con la ruta del defecto; 6. marca el commit `success` o `failure` | RF-S03, RF-01 a RF-12 |
| **CU-S05** Solicitar o reintentar una revisión | Desarrollador | 1. en el panel elige un repositorio y un número de PR («revisar ahora»), o abre una revisión fallida o ya publicada y pulsa «reintentar»; 2. el sistema la encola y sigue como CU-S04 desde el paso 4 | RF-S03 |
| **CU-S06** Consultar revisiones y hallazgos | Desarrollador | 1. abre el panel y filtra por repositorio; 2. elige una revisión; 3. ve su estado, el veredicto, el resumen y cada hallazgo con su archivo, línea, clase, mensaje y ruta; 4. sigue el enlace al *pull request* | RF-S04, RF-11, RF-12 |
| **CU-S07** Clasificar un hallazgo | Desarrollador | 1. en el detalle de una revisión marca un hallazgo como confirmado o como falso positivo; 2. el sistema guarda la clasificación con quién la hizo y cuándo; 3. un falso positivo deja de comentarse y de bloquear en las revisiones siguientes del repositorio | RF-S05 |

## Relaciones

| Relación | Por qué |
|---|---|
| CU-S04 incluye «Analizar el código» | el análisis lo hace el checker dentro de `clang`, un archivo por invocación |
| CU-S05 incluye CU-S04 | pedir o reintentar una revisión sigue el mismo flujo, sin esperar el *webhook* |
| CU-S07 extiende CU-S06 | se clasifica desde el detalle de una revisión |
| Administrador hereda de Desarrollador | el administrador también consulta, clasifica y pide revisiones |

## Criterios de aceptación

| Caso de uso | Criterio (dado, cuando, entonces) | Comprobado |
|---|---|---|
| CU-S01 | Dada una instancia nueva, cuando alguien se registra, entonces queda como administrador y entra; cuando otro se registra después, queda pendiente y no puede entrar. Dado un usuario activo, cuando ingresa con su clave, entonces recibe una cookie de sesión `httpOnly` y `SameSite=Strict`; con una clave incorrecta o un correo inexistente recibe el mismo error, y tras 10 fallos, un bloqueo | `api.test.ts` «RF-S01 registro» y «RF-S01 autenticación» |
| CU-S02 | Dado un registro pendiente, cuando un administrador lo aprueba, entonces puede entrar; dado un administrador, cuando intenta cambiarse su propio rol, entonces se rechaza; cuando crea un usuario con un correo en uso, entonces se rechaza; dado un desarrollador, cuando intenta crear uno, entonces recibe «sin permiso» | `casos.test.ts`, `api.test.ts` |
| CU-S03 | Dado un repositorio conectado, cuando se pide la lista, entonces el administrador ve el secreto del *webhook* y el desarrollador no | `api.test.ts` |
| CU-S04 | Dado un *pull request* con un uso inválido en una línea cambiada, cuando GitHub envía el *webhook* firmado, entonces el sistema comenta esa línea y pone el commit en `failure` si el repositorio bloquea el merge; con la firma mala responde 401 | `casos.test.ts`, `api.test.ts`; demostración: 2 comentarios y `failure` |
| CU-S05 | Dada una revisión en curso, cuando se pide reintentarla, entonces se rechaza; dada una fallida, vuelve a la cola con un intento más | `casos.test.ts`, `api.test.ts` |
| CU-S06 | Dada una revisión publicada, cuando se abre su detalle, entonces trae cada hallazgo con su ruta | `api.test.ts` |
| CU-S07 | Dado un hallazgo marcado como falso positivo, cuando se reintenta la revisión, entonces queda suprimido y el veredicto es «aprobada» | `casos.test.ts`, `producto-sqlite.test.ts` |

## Excepciones relevantes

| Caso | Excepción | Qué pasa |
|---|---|---|
| CU-S01 | sesión vencida (8 horas) o usuario desactivado mientras tenía sesión | la API responde 401 y el panel vuelve al ingreso |
| CU-S01 | cuenta pendiente de aprobación | no entra (403): «Tu cuenta espera la aprobación de un administrador.» |
| CU-S01 | cuenta desactivada o rechazada | no entra (403): «Tu cuenta está desactivada: pide a un administrador que la reactive.» |
| CU-S03 | el repositorio ya está conectado | se informa; desconectarlo conserva sus revisiones |
| CU-S04 | el mismo commit llega dos veces (por ejemplo, `synchronize` repetido) | se ignora: un commit se revisa una sola vez (RN-S02) |
| CU-S04 | un archivo no compila (faltan cabeceras generadas) | se informa como no analizado en el resumen; no se da por limpio (RN-S05) |
| CU-S04 | `clang` o GitHub fallan, o el proceso se cae a mitad | la revisión queda `Fallida` con su motivo y el commit en `error`; se puede reintentar (CU-S05) |
| CU-S04 | un hallazgo cae fuera de las líneas del diff | GitHub no acepta comentarios ahí: va en el resumen de la revisión |
| CU-S05 | GitHub no encuentra el *pull request* | el panel muestra el error de GitHub (502) |
