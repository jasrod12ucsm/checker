# Dónde va cada cosa (servicio)

> `donde-va`, adaptado al servicio. Si vas a escribir X, va en Y. Si no
> está en la tabla, pregunta antes de inventar un lugar.

| Si escribes… | Va en | Ejemplo |
|---|---|---|
| un valor validado (correo, nombre, número de PR) | `paquetes/kernel/src/valores.ts` si es general; en el contexto si es suyo | `email`, `positivo`; `nombreRepo` en repositorios |
| una regla del negocio | una función pura del contexto que es dueño del dato | `solicitar` en `contextos/revisiones/src/comandos.ts` |
| un permiso nuevo | `Permiso` y `PERMISOS` en `contextos/identidad/src/usuario.ts` | `"clasificar-hallazgos"` |
| un error de negocio | la unión de errores del contexto (`errores.ts`) y su código en `adaptadores/http/src/errores.ts` | `ShaYaRevisado` → 409 |
| un caso de uso | `paquetes/producto/src/casos-<contexto>.ts`: cargar, decidir, efectos | `reintentar` |
| algo que el caso de uso necesita de afuera | un puerto en `producto/src/puertos.ts` y su adaptador | `Analizador` → `adaptadores/analizador` |
| una ruta HTTP | `adaptadores/http/src/servidor.ts`, su esquema en `esquemas.ts`, su JSON en `vistas.ts` | `PATCH /api/hallazgos/:id` |
| una columna o tabla | `adaptadores/sqlite/src/esquema.sql`, su lectura en `filas.ts`, su escritura en `almacen.ts` | `no_compilados` |
| una llamada a GitHub | `adaptadores/github/src/cliente.ts` | `publicarEstado` |
| cómo se invoca `clang` | `adaptadores/analizador/src/clang.ts`; cómo se lee su salida, `salida.ts` | `argumentos`, `leerSalida` |
| una variable de configuración | `app/src/configuracion.ts` (`CENTINELA_*`) y `sistema/.env.ejemplo` | `CENTINELA_PARALELO` |
| un doble de prueba compartido | `sistema/pruebas/dobles.ts` | `GitHubFalso` |

## Nombres

| Cosa | Forma | Ejemplo |
|---|---|---|
| orden del dominio | verbo en infinitivo | `publicar`, `clasificar` |
| estado | sustantivo o participio con mayúscula | `Pendiente`, `EnAnalisis`, `Publicada` |
| error | lo que pasó, en positivo | `RevisionEnCurso`, `EmailEnUso` |
| puerto | el plural de lo que guarda o el nombre del sistema externo | `Revisiones`, `GitHub` |
| adaptador | lo que usa | `abrirAlmacen`, `clienteGitHub`, `analizadorClang` |
| prueba | la regla en una frase | «un sha no se revisa dos veces» |

## Qué prueba va en qué nivel

| Quieres comprobar… | Nivel | Dónde |
|---|---|---|
| una regla del dominio | unidad, sin dobles | `contextos/*/src/*.test.ts` |
| que algo **no** compile | garantía de tipos | `*/garantias.test.ts` |
| un requisito de punta a punta sin red | caso de uso con dobles | `producto/src/casos.test.ts` |
| SQL, HMAC, scrypt, el cliente de GitHub | adaptador con lo real o un servidor local | `adaptadores/*/src/*.test.ts` |
| códigos HTTP, cookies, validación | API con `inject` | `pruebas/api.test.ts` |
| que la arquitectura no se degrade | aptitud | `pruebas/arquitectura.test.ts` |
| `clang` y el checker reales | integración en Docker | `adaptadores/analizador/src/clang.test.ts` |
