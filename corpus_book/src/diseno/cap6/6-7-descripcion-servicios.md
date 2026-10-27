# 6.7 Descripción de la interfaz de servicios

Reglas comunes a todas las rutas:

- **Validación en la frontera.** Cada cuerpo se valida con un esquema `zod`
  estricto antes de llegar al dominio: un campo de más, de menos o de otro
  tipo es un 400 con el nombre del campo. Las filas que se leen de la base
  también se validan.
- **Un solo mapa de errores.** Cada error del dominio tiene un código HTTP
  fijo en un único lugar (`errores.ts`): 400 datos inválidos, 401 sin sesión o
  credenciales incorrectas, 403 sin permiso o cuenta pendiente o desactivada (con un mensaje distinto para cada caso), 404 no existe,
  409 conflicto (correo en uso, repositorio ya conectado, revisión en curso,
  modificarse a sí mismo), 429 demasiados intentos y 502 error de GitHub.
- **Lo que no sale.** Las respuestas se arman con vistas explícitas: el hash
  de la clave nunca sale, y el secreto del *webhook* solo lo recibe quien
  administra repositorios.
- **Trabajo diferido.** `POST /api/revisiones`, el reintento y el *webhook*
  responden 202: la revisión queda `Pendiente` y el cliente consulta su
  estado después.

Respuesta del *webhook* según el evento:

| Evento | Respuesta |
|---|---|
| `pull_request` con acción `opened`, `synchronize` o `reopened`, firma válida | 202 `{tipo: "Encolada", revisionId}` |
| `ping`, otro evento u otra acción | 200 `{tipo: "Ignorado", motivo}` |
| commit ya revisado, revisión en curso o repositorio desconectado | 200 `{tipo: "Ignorado", motivo}` |
| repositorio no conectado | 404 |
| firma ausente o incorrecta | 401 |
| cuerpo que no es un evento válido | 400 |

Ejemplo de una revisión como la devuelve `GET /api/revisiones/:id` (se muestra
uno de sus dos hallazgos):

```json
{
  "id": "2d6acae0-41f9-4ee9-851e-d04ef168b7ce",
  "repositorio": { "id": "75f23122-…", "nombre": "demo/centinela-demo" },
  "pr": { "numero": 1, "titulo": "Agrega una caché de nombres", "autor": "ana-dev",
          "shaCabeza": "d3m0000…0001", "enlace": "https://github.com/demo/centinela-demo/pull/1" },
  "origen": "webhook", "intentos": 1,
  "estado": { "tipo": "Publicada", "veredicto": "ConProblemas",
              "resumen": { "archivosAnalizados": 2, "noCompilados": 0,
                           "confirmados": 1, "posibles": 1, "suprimidos": 0 } },
  "hallazgos": [ { "archivo": "src/cache.cpp", "linea": 24, "columna": 52,
                   "clase": "Confirmado", "huella": "…", "clasificacion": "Confirmado",
                   "clasificadoPor": { "id": "…", "nombre": "Lucía Paredes" },
                   "clasificadoEn": "2026-10-27T03:01:12.000Z",
                   "mensaje": "Uso de una referencia invalidada: …", "ruta": [ … ] } ]
}
```
