# 6.5 Interfaz de servicios del sistema

Centinela C++ ofrece dos interfaces de servicio:

- **La API HTTP** (`/api/*`), que usa el panel web y que puede usar cualquier
  cliente con una sesión. Todo es JSON; la sesión viaja en la cookie
  `centinela_sesion` (`httpOnly`, `SameSite=Strict`, `Secure` en producción) y
  los errores tienen siempre la forma `{"error": {"codigo", "mensaje"}}`.
- **El *webhook*** (`POST /webhooks/github`), que usa GitHub. No lleva sesión:
  se autentica con la firma HMAC-SHA256 del cuerpo con el secreto del
  repositorio (cabecera `X-Hub-Signature-256`), comparada en tiempo constante.

| Método y ruta | Cuerpo | Respuesta | Errores | Permiso |
|---|---|---|---|---|
| `GET /api/registro` | — | 200 `{hayUsuarios}` | — | — |
| `POST /api/registro` | `{email, nombre, clave}` | 201 `{usuario, pendienteDeAprobacion}` (la primera cuenta recibe la cookie) | 400, 409 | — |
| `POST /api/sesion` | `{email, clave}` | 200 usuario + cookie | 401, 403 (cuenta pendiente o desactivada), 429 | — |
| `GET /api/sesion` | — | 200 usuario | 401 | sesión |
| `DELETE /api/sesion` | — | 204 | — | — |
| `GET /api/usuarios` | — | 200 lista | 401, 403 | gestionar-usuarios |
| `POST /api/usuarios` | `{email, nombre, clave, rol}` | 201 usuario | 400, 403, 409 | gestionar-usuarios |
| `PATCH /api/usuarios/:id` | `{estado?: Activo o Desactivado, rol?}` | 200 usuario | 400, 404, 409 | gestionar-usuarios |
| `GET /api/repositorios` | — | 200 lista | 401 | consultar-revisiones |
| `POST /api/repositorios` | `{nombre, politica, bloquearMerge}` | 201 con `webhook: {url, secreto}` | 400, 403, 409 | gestionar-repositorios |
| `PATCH /api/repositorios/:id` | `{politica?, bloquearMerge?}` | 200 | 400, 404, 409 | gestionar-repositorios |
| `DELETE /api/repositorios/:id` | — | 200 | 404 | gestionar-repositorios |
| `GET /api/revisiones?repositorio=` | — | 200 lista | 401 | consultar-revisiones |
| `POST /api/revisiones` | `{repositorioId, numeroPr}` | 202 revisión `Pendiente` | 404, 409, 502 | solicitar-revision |
| `GET /api/revisiones/:id` | — | 200 revisión con sus hallazgos | 404 | consultar-revisiones |
| `POST /api/revisiones/:id/reintento` | — | 202 | 404, 409 | solicitar-revision |
| `PATCH /api/hallazgos/:id` | `{clasificacion}` | 200 hallazgo con quién y cuándo lo clasificó | 400, 404 | clasificar-hallazgos |
| `POST /webhooks/github` | evento de GitHub | 202 encolada, 200 ignorado | 400, 401, 404 | firma HMAC |
| `GET /salud` | — | 200 `{ok: true}` | — | — |
