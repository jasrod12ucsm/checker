# Centinela C++: el sistema

**Centinela C++** es un servicio web que revisa automáticamente los *pull
requests* de C++ de un equipo. Cuando alguien abre o actualiza un PR en
GitHub, Centinela analiza los archivos que cambiaron con el checker
`ucsm.ContainerInvalidation`, comenta en la línea exacta cada uso de un
iterador, una referencia o un puntero invalidado, con la ruta del defecto, y
puede bloquear el merge hasta que se corrija.

| Pregunta | Respuesta |
|---|---|
| ¿Quién es el cliente? | un equipo que desarrolla en C++ y usa GitHub |
| ¿Qué problema le resuelve? | los usos de handles invalidados compilan sin aviso y fallan en producción; Clang Static Analyzer detecta 80 de 342 en el banco, el checker los 342 |
| ¿Cómo lo usa? | la primera persona que se registra queda como administradora y aprueba a las demás; conecta el repositorio una vez; desde ahí cada PR se revisa solo, y el equipo consulta y clasifica los hallazgos en el panel |
| ¿Qué tipo de servicio es? | *software as a service* de un solo cliente: la organización lo despliega con Docker; no trae usuarios predefinidos, cada persona se registra con su correo y su clave |
| ¿Qué no hace? | varios clientes aislados (*multi-tenant*), facturación, proveedores distintos de GitHub |

## En dos minutos, sin cuenta de GitHub

```bash
docker compose build sistema          # una vez; usa la imagen checker:llvm21
docker compose up sistema-demo
```

La demostración levanta un GitHub simulado con un repositorio y un PR de
ejemplo (`sistema/demo/pr/`), conecta el repositorio, envía el *webhook*
firmado y analiza el PR con `clang` y el checker reales. Como Centinela
arranca sin usuarios, la demostración se registra primero con una clave
aleatoria (queda de administradora):

```text
0. Registro de la primera cuenta (queda de administradora): demo-1f2a02@centinela.local
1. Repositorio demo/centinela-demo conectado. Webhook: http://localhost:8080/webhooks/github
2. GitHub avisa que se abrió el PR #1 → 202 {"tipo":"Encolada",...}
3. Revisión Publicada: ConProblemas {"archivosAnalizados":2,"noCompilados":0,"confirmados":1,"posibles":1,"suprimidos":0}
   - src/cache.cpp:17 [Posible] Uso de una referencia posiblemente invalidada: 'std::vector::push_back' (línea 16) ...
   - src/cache.cpp:24 [Confirmado] Uso de una referencia invalidada: 'std::vector::clear' (línea 10) lo invalidó
4. Lo que Centinela publicó en GitHub:
   estado del commit: pending — En cola
   estado del commit: pending — Analizando
   revisión con 2 comentarios en línea: src/cache.cpp:17, src/cache.cpp:24
   estado del commit: failure — 1 confirmados, 1 posibles
```

Después queda en marcha en `http://localhost:8080` e imprime el correo y la
clave de esa cuenta. Las pruebas:

```bash
docker compose run --rm sistema-pruebas   # 279 pruebas (servicio y panel), con clang y el checker reales
cd sistema && npm ci && npm test          # fuera de Docker: todas menos la de clang
```

## Las páginas de esta parte

| Página | Qué tiene |
|---|---|
| [Requerimientos y casos de uso](requerimientos.md) | RF-S01 a RF-S05 y CU-S01 a CU-S07, y dónde se prueba cada uno |
| [Modelo funcional del dominio](modelado.md) | eventos, comandos, contextos, flujos en DSL, significado y leyes |
| [Arquitectura](arquitectura.md) | las cuatro guías de diseño adaptadas a TypeScript |
| [Tipos que impiden errores](tipos.md) | marcas, uniones, estados en el tipo, testigos y garantías que no compilan |
| [Dónde va cada cosa](donde-va.md) | si escribes X, va en Y |
| [API HTTP](api.md) | rutas, cuerpos, respuestas y errores |
| [Base de datos](datos.md) | esquema SQLite y modelo entidad-relación |
| [Pruebas](pruebas.md) | niveles, órdenes y cobertura |
| [Ponerlo en marcha con GitHub](despliegue.md) | token, *webhook*, protección de rama |
