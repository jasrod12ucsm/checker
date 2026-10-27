# 6.8 Servicios consumidos por el sistema

| Servicio | Para qué | Cómo | Si falla |
|---|---|---|---|
| API REST de GitHub (v3) | leer el PR y sus archivos cambiados, descargar el commit, publicar la revisión con comentarios en línea y el estado del commit | `GET /repos/{r}/pulls/{n}`, `GET …/pulls/{n}/files`, `GET /repos/{r}/tarball/{sha}`, `POST …/pulls/{n}/reviews`, `POST /repos/{r}/statuses/{sha}`; token en `CENTINELA_GITHUB_TOKEN` | la revisión queda `Fallida` con el mensaje de GitHub y se puede reintentar; al pedir una revisión manual, 502 |
| *Webhooks* de GitHub | enterarse de cada PR abierto o actualizado | GitHub llama a `POST /webhooks/github` con el secreto del repositorio | si no llega, el usuario usa «Revisar un PR ahora» |
| clang 21 + plugin `ucsm.ContainerInvalidation` | analizar cada archivo C++ cambiado | proceso local con `execFile` y argumentos separados (sin shell), un archivo por invocación, salida de texto de CSA (`-analyzer-output=text`) e *inlining* `all`, el mismo modo del experimento en código real (D-22) | el archivo cuenta como no compilado y se informa; no aborta la revisión |
| Sistema de archivos | descomprimir el commit en una carpeta temporal | `tar`, carpeta borrada al terminar | la revisión falla con el motivo |
| SQLite | persistencia (sección 6.9) | archivo local con `better-sqlite3` | el servicio no arranca |

El sistema no envía el código a ningún servicio externo: el análisis corre en
el mismo servidor de Centinela.
