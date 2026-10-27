# API HTTP

Todo es JSON. Un usuario sale como `{id, email, nombre, rol, estado, creadoEn}`, con
`estado` igual a `Pendiente`, `Activo` o `Desactivado`; el hash de la clave nunca
sale. Un hallazgo clasificado trae `clasificadoPor: {id, nombre}` y `clasificadoEn`
(fecha ISO); sin clasificar, los dos son `null`. La sesión viaja en la cookie `centinela_sesion` (`httpOnly`,
`SameSite=Strict`, `Secure` con `CENTINELA_COOKIE_SEGURA=true`). Los errores
tienen siempre la forma `{"error": {"codigo": "...", "mensaje": "..."}}`.

| Método y ruta | Cuerpo | Respuesta | Errores | Permiso |
|---|---|---|---|---|
| `GET /api/registro` | — | 200 `{hayUsuarios}` (si es `false`, quien se registre será administrador) | — | — |
| `POST /api/registro` | `{email, nombre, clave}` | 201 `{usuario, pendienteDeAprobacion}`; el primero recibe además la cookie | 400, 409 | — |
| `POST /api/sesion` | `{email, clave}` | 200 usuario + cookie | 401, 403 (`UsuarioPendiente` o `UsuarioDesactivado`), 429 | — |
| `GET /api/sesion` | — | 200 usuario | 401 | sesión |
| `DELETE /api/sesion` | — | 204 | — | — |
| `GET /api/usuarios` | — | 200 lista | 401, 403 | gestionar-usuarios |
| `POST /api/usuarios` | `{email, nombre, clave, rol}` | 201 usuario | 400, 403, 409 | gestionar-usuarios |
| `PATCH /api/usuarios/:id` | `{estado?, rol?}`; `estado` es `Activo` (aprobar o reactivar) o `Desactivado` (rechazar o dar de baja) | 200 usuario | 400, 404, 409 | gestionar-usuarios |
| `GET /api/repositorios` | — | 200 lista (`webhook` solo para el administrador) | 401 | consultar-revisiones |
| `POST /api/repositorios` | `{nombre, politica, bloquearMerge}` | 201 con `webhook: {url, secreto}` | 400, 403, 409 | gestionar-repositorios |
| `PATCH /api/repositorios/:id` | `{politica?, bloquearMerge?}` | 200 | 400, 404, 409 | gestionar-repositorios |
| `DELETE /api/repositorios/:id` | — | 200 (desconectado) | 404 | gestionar-repositorios |
| `GET /api/revisiones?repositorio=` | — | 200 lista | 401 | consultar-revisiones |
| `POST /api/revisiones` | `{repositorioId, numeroPr}` | 202 revisión `Pendiente` | 404, 409, 502 | solicitar-revision |
| `GET /api/revisiones/:id` | — | 200 revisión + `hallazgos` | 404 | consultar-revisiones |
| `POST /api/revisiones/:id/reintento` | — | 202 | 404, 409 | solicitar-revision |
| `PATCH /api/hallazgos/:id` | `{clasificacion}` | 200 hallazgo con `clasificadoPor` (id y nombre) y `clasificadoEn` | 400, 404 | clasificar-hallazgos |
| `POST /webhooks/github` | evento de GitHub | 202 encolada, 200 ignorado | 400, 401, 404 | firma HMAC |
| `GET /salud` | — | 200 `{ok: true}` | — | — |

Una revisión en JSON, tal como la devolvió la demostración
(`npx tsx demo/demostrar.ts --json`); se muestra el primero de sus dos
hallazgos:

```json
{
  "id": "2d6acae0-41f9-4ee9-851e-d04ef168b7ce",
  "repositorio": { "id": "75f23122-56e3-47e1-8bf1-9a7e0c148ce2", "nombre": "demo/centinela-demo" },
  "pr": {
    "numero": 1, "titulo": "Agrega una caché de nombres", "autor": "ana-dev",
    "shaCabeza": "d3m0000000000000000000000000000000000001",
    "enlace": "https://github.com/demo/centinela-demo/pull/1"
  },
  "origen": "webhook", "solicitadaPor": null, "creadaEn": "2026-10-27T02:45:19.470Z", "intentos": 1,
  "estado": {
    "tipo": "Publicada", "desde": "2026-10-27T02:45:19.817Z", "veredicto": "ConProblemas",
    "resumen": { "archivosAnalizados": 2, "noCompilados": 0, "confirmados": 1, "posibles": 1, "suprimidos": 0 }
  },
  "hallazgos": [
    {
      "id": "3d12473d-5f99-4508-9d78-b3a18958b09c",
      "archivo": "src/cache.cpp", "linea": 17, "columna": 12, "clase": "Posible",
      "mensaje": "Uso de una referencia posiblemente invalidada: 'std::vector::push_back' (línea 16) si la capacidad está agotada reubica los elementos; nada garantiza espacio: use reserve(size() + n) antes, o vuelva a obtenerlo",
      "ruta": [
        { "archivo": "src/cache.cpp", "linea": 24, "mensaje": "Calling 'Cache::agregar_y_medir'" },
        { "archivo": "src/cache.cpp", "linea": 15, "mensaje": "El handle al elemento se obtiene de 'std::vector::operator[]'" },
        { "archivo": "src/cache.cpp", "linea": 16, "mensaje": "El handle al elemento puede quedar invalidado por 'std::vector::push_back'" },
        { "archivo": "src/cache.cpp", "linea": 17, "mensaje": "Uso de una referencia posiblemente invalidada: …" }
      ],
      "huella": "4abb36d4", "clasificacion": "SinRevisar",
      "clasificadoPor": null, "clasificadoEn": null
    }
  ]
}
```

La ruta trae también las notas de CSA (en inglés), como la llamada desde
`main` en la línea 24.

Las entradas se validan con estos esquemas:

{{codigo sistema/paquetes/adaptadores/http/src/esquemas.ts 1-31}}
