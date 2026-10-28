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
| Almacén | `adaptadores/sqlite` | ida y vuelta, `UNIQUE`, `CHECK`, cola, transacción, filas corruptas, migración de la versión 1 a la 3 y plan de consulta de la lista | SQLite |
| Criptografía | `adaptadores/cripto` | scrypt, token, firma de GitHub | `node:crypto` |
| GitHub | `adaptadores/github` | PR, paginación, revisión, estado, *tarball*, errores | un servidor HTTP local |
| Analizador | `adaptadores/analizador` | lectura de la salida de `clang`; análisis real | `clang` 21 y el plugin (en Docker) |
| API | `pruebas/api.test.ts` | registro, aprobación y rechazo, cookies, 401/403/409/429, *webhook* firmado, flujo completo | Fastify, SQLite, scrypt, HMAC |
| Arquitectura | `pruebas/arquitectura.test.ts` | importaciones por capa; sin códigos HTTP fuera de `http`; sin reloj ni azar en el dominio; sin `throw` de negocio; sin `any` | el código fuente |
| Casos de prueba | `pruebas/casos-de-prueba.test.ts` | CP-01 a CP-14: valores límite de cada campo, cálculos, formatos y vínculos | Fastify, SQLite, scrypt, HMAC |
| Sistema | `app/src/componer.test.ts` | arranque sin usuarios, registro, servidor y trabajador juntos | todo menos GitHub y `clang` |

Resultado (2026-10-28): **155 pruebas del servicio y 124 del panel en verde**
dentro de la imagen (279); fuera de Docker, 154 y la de `clang` se omite.
Cobertura del servicio: **97,7 %** de líneas, 88,8 % de ramas y 96,2 % de
funciones. Los casos de prueba con valores límite (`pruebas/casos-de-prueba.test.ts`),
el panel ([El panel web](panel.md)) y las pruebas no funcionales están en el
[capítulo 8](../pruebas/index.md). El CI de GitHub corre las mismas
pruebas y la demostración de punta a punta (`.github/workflows/ci.yml`).

## La prueba de un requisito, de punta a punta

{{codigo sistema/pruebas/api.test.ts "detalle con hallazgos, clasificar y reintentar"}}
