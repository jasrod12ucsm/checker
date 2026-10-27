# Pruebas del sistema

```bash
cd sistema
npm ci
npm test               # tsc (incluye las garantías que no deben compilar) + Vitest
npm run cobertura      # con umbrales: 90 % de líneas y funciones, 80 % de ramas
docker compose run --rm sistema-pruebas   # desde la raíz: todo, con clang y el checker reales
```

| Nivel | Archivos | Pruebas | Qué usa de verdad |
|---|---|---|---|
| Kernel y dominio | `kernel`, `contextos/*` | valores, autorización, sesiones, repositorios, transiciones, veredicto, huella, estado del commit | nada externo |
| Garantías de tipos | `*/garantias.test.ts` | transiciones y testigos que no deben compilar | el compilador |
| Casos de uso | `producto/src/casos.test.ts` | RF-S01 a RF-S05 | dobles de todos los puertos |
| Almacén | `adaptadores/sqlite` | ida y vuelta, `UNIQUE`, `CHECK`, cola, transacción, filas corruptas, migración de la versión 1 a la 2 | SQLite |
| Criptografía | `adaptadores/cripto` | scrypt, token, firma de GitHub | `node:crypto` |
| GitHub | `adaptadores/github` | PR, paginación, revisión, estado, *tarball*, errores | un servidor HTTP local |
| Analizador | `adaptadores/analizador` | lectura de la salida de `clang`; análisis real | `clang` 21 y el plugin (en Docker) |
| API | `pruebas/api.test.ts` | registro, aprobación y rechazo, cookies, 401/403/409/429, *webhook* firmado, flujo completo | Fastify, SQLite, scrypt, HMAC |
| Arquitectura | `pruebas/arquitectura.test.ts` | importaciones por capa; sin códigos HTTP fuera de `http`; sin reloj ni azar en el dominio; sin `throw` de negocio; sin `any` | el código fuente |
| Sistema | `app/src/componer.test.ts` | arranque sin usuarios, registro, servidor y trabajador juntos | todo menos GitHub y `clang` |

Resultado (2026-10-27): **140 pruebas en verde** dentro de la imagen; fuera
de Docker, 139 y la de `clang` se omite. Cobertura de líneas: **97,6 %**;
de ramas: 87,7 %; de funciones: 96,2 %. El CI de GitHub corre las mismas
pruebas y la demostración de punta a punta (`.github/workflows/ci.yml`).

## La prueba de un requisito, de punta a punta

[`sistema/pruebas/api.test.ts:161`](https://github.com/jasrod12ucsm/checker/blob/main/sistema/pruebas/api.test.ts#L161-L180)

```typescript
  it("detalle con hallazgos, clasificar y reintentar", async () => {
    const c = cuerpoPr();
    const { revisionId } = (await webhook(c, firmar(repo.webhook.secreto, c))).json();
    await p.revisiones.procesarSiguiente();
    const det = (await app.inject({ method: "GET", url: `/api/revisiones/${revisionId}`, headers: { cookie } })).json();
    expect(det).toMatchObject({ estado: { tipo: "Publicada", veredicto: "ConProblemas" }, hallazgos: [{ archivo: "src/a.cpp", linea: 11, clasificacion: "SinRevisar", clasificadoPor: null, clasificadoEn: null }] });

    const h = det.hallazgos[0].id;
    const cl = await app.inject({ method: "PATCH", url: `/api/hallazgos/${h}`, headers: { cookie }, payload: { clasificacion: "FalsoPositivo" } });
    expect(cl.json()).toMatchObject({ clasificacion: "FalsoPositivo", clasificadoPor: { nombre: "Admin" } });
    const otraVez = (await app.inject({ method: "GET", url: `/api/revisiones/${revisionId}`, headers: { cookie } })).json();
    expect(otraVez.hallazgos[0]).toMatchObject({ clasificadoPor: { nombre: "Admin" }, clasificadoEn: expect.stringMatching(/^\d{4}-/) });
    expect((await app.inject({ method: "PATCH", url: `/api/hallazgos/${h}`, headers: { cookie }, payload: { clasificacion: "Otra" } })).statusCode).toBe(400);

    expect((await app.inject({ method: "POST", url: `/api/revisiones/${revisionId}/reintento`, headers: { cookie } })).statusCode).toBe(202);
    expect((await app.inject({ method: "POST", url: `/api/revisiones/${revisionId}/reintento`, headers: { cookie } })).statusCode).toBe(409);
    await p.revisiones.procesarSiguiente();
    const otra = (await app.inject({ method: "GET", url: `/api/revisiones/${revisionId}`, headers: { cookie } })).json();
    expect(otra).toMatchObject({ intentos: 2, estado: { veredicto: "Aprobada", resumen: { suprimidos: 1 } } });
  });
```
