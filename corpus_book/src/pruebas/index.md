# Capítulo 8 — Pruebas del software

Este capítulo prueba **Centinela C++**, el servicio web que revisa los *pull
requests*, junto con el checker que ejecuta dentro (el checker ya se midió
contra el banco y contra código real en los resultados del libro). Cada
prueba que se cita aquí está en el repositorio y se vuelve a correr con una
orden; ninguna cifra se escribió a mano: las de las pruebas no funcionales
salen de los archivos `sistema/no-funcionales/resultados/*.json`.

La estrategia sigue la pirámide de pruebas (Sommerville, 2020; Pressman y
Maxim, 2014): muchas pruebas unitarias rápidas en la base, menos de
integración y funcionales en el medio, y pocos recorridos de extremo a
extremo en la punta, que son los más lentos y los más frágiles. Encima de
eso, las pruebas no funcionales miden al servicio en marcha, desde fuera.

| Tipo de prueba | Qué se prueba | Herramienta | Dónde está | Resultado |
|---|---|---|---|---|
| Unitarias | funciones puras del dominio (servicio y panel) | Vitest | `paquetes/*/src/*.test.ts`, `frontend/src/**/*.test.ts` | en verde |
| Integración | cada adaptador contra la pieza real: SQLite, scrypt y HMAC, GitHub simulado por HTTP, `clang` | Vitest | `adaptadores/*`, `pruebas/api.test.ts` | en verde |
| Funcionales | cada requisito RF-S01 a RF-S05 por la API y por el panel, contra el servicio real | Vitest, Testing Library | `pruebas/`, `frontend/pruebas/` | en verde |
| Casos de prueba | valores límite de cada campo, cálculos, formatos y vínculos (CP-01 a CP-14) | Vitest | `pruebas/casos-de-prueba.test.ts` | 14 de 14 |
| De extremo a extremo | 11 recorridos de una persona en el navegador, con `clang` y el checker reales | Playwright | `no-funcionales/navegadores.ts` | ver 8.2.4 |
| Aceptación | los criterios «dado, cuando, entonces» de cada caso de uso | las anteriores | tabla 8.2.5 | 7 de 7 casos |
| Carga, estrés, volumen | rendimiento, punto de saturación y comportamiento con muchos datos | autocannon | `no-funcionales/medir.ts` | ver 8.4 |
| Configuración | navegadores, tamaños de pantalla, temas y ajustes del servicio | Playwright, `medir.ts` | `no-funcionales/` | ver 8.4.4 |
| Usabilidad | accesibilidad WCAG 2.1 AA, eficiencia de cada tarea, heurísticas | axe-core, Playwright | `no-funcionales/navegadores.ts` | ver 8.4.5 |
| Seguridad | confidencialidad, integridad, autenticación, autorización, disponibilidad | `medir.ts` | `no-funcionales/medir.ts seguridad` | 41 de 41 |
| Regresión y humo | todo lo anterior en cada *push*; la demostración como prueba de humo | GitHub Actions | `.github/workflows/ci.yml` | ver 8.2.6 |

**Cómo se vuelve a correr todo.**

```bash
# Desde la raíz del repositorio. Funcionales (servicio y panel) con clang y el checker reales:
docker compose run --rm sistema-pruebas
# No funcionales: carga, estrés, volumen, configuración y seguridad (unos 10 minutos):
docker compose run --rm sistema-no-funcionales
# Extremo a extremo, configuración en navegadores y accesibilidad (desde la máquina anfitriona):
docker compose up -d sistema-demo && docker compose logs sistema-demo | grep "sigue en marcha"
cd sistema && npx tsx no-funcionales/navegadores.ts <correo> <clave> ../libro/capturas
```
