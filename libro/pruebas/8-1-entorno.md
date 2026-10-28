# 8.1 Entorno de ejecución de las pruebas

Todas las pruebas de este capítulo se ejecutaron el **28 de octubre de 2026**
en una sola máquina, una laptop de uno de los autores. El servicio corre
dentro de la imagen Docker `centinela:local` (la misma que se despliega), y
los navegadores corren en la máquina anfitriona contra ese contenedor.

## Máquina anfitriona

| Elemento | Especificación |
|---|---|
| Equipo | laptop Lenovo LOQ 15IRH8 |
| Procesador | Intel Core i7-13620H de 13.ª generación: 10 núcleos (6 de rendimiento y 4 de eficiencia), 16 hilos, hasta 4,9 GHz |
| Memoria | 16 GB (15 GiB utilizables por el sistema) |
| Almacenamiento | SSD NVMe Solidigm SSDPFINW512GZL de 512 GB |
| Gráficos | Intel UHD (Raptor Lake-P) y NVIDIA GeForce RTX 4050 Laptop (no se usan en las pruebas) |
| Sistema operativo | Ubuntu 24.04.4 LTS, núcleo Linux 7.0.0-38-generic, x86-64 |
| Contenedores | Docker Engine 29.2.1 con Docker Compose |
| Node.js en la anfitriona | v20.19.0 (para Playwright) |

## Dentro del contenedor

| Elemento | Versión |
|---|---|
| Base | Ubuntu 24.04.5 LTS (imagen `checker:llvm21`) |
| Compilador y analizador | Ubuntu clang 21.1.8 con el plugin `ucsm.ContainerInvalidation` |
| Node.js | v22.17.1 |
| Servicio | Fastify 5.12.7, better-sqlite3 12.11.1 (SQLite en modo WAL), zod 4.6.7 |
| Panel | React 19.2.9 compilado con Vite 7.3.7 |
| Pruebas | Vitest 3.2.7, Testing Library 16.3.3 y autocannon 8.0.0 en el contenedor; Playwright 1.63.0 y axe-core 4.13.0 en la anfitriona |

## Navegadores

Tabla: Navegadores usados en las pruebas

| Navegador | Motor | Versión |
|---|---|---|
| Google Chrome | Blink | 144.0.7559.132 |
| Chromium (snap) | Blink | 156.0.8078.47 |
| Firefox de Playwright | Gecko | ver 8.4.4 |
| WebKit de Playwright | WebKit (motor de Safari) | ver 8.4.4 |

## Límites de este entorno

- El generador de carga y el servicio comparten la misma máquina: las cifras
  de rendimiento son una cota inferior de lo que daría un servidor dedicado,
  porque autocannon le quita procesador al servicio.
- El servicio corre en **un solo proceso** de Node.js, como se despliega hoy
  (`docker compose up sistema`). Las cifras de saturación son de ese proceso.
- GitHub está simulado por un servidor local (`no-funcionales/github-varios.ts`)
  que responde como la API REST v3: así se mide a Centinela y no a la red ni
  a los límites de GitHub. El análisis sí es real: `clang` y el checker
  compilan y analizan cada archivo.
