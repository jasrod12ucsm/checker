# 6.1 Interfaz de usuario del sistema

Centinela C++ se usa desde el navegador. Toda pantalla, salvo el registro y el
ingreso, exige una sesión iniciada, y lo que muestra depende del rol: el menú
*Usuarios* y las acciones sobre repositorios solo aparecen para el
administrador. El servidor vuelve a comprobar el permiso en cada petición
(RN-S01 y la sección 5.4), así que ocultar un botón es comodidad, no seguridad.

| Usuario | Pantallas | Qué hace en ellas | Caso de uso |
|---|---|---|---|
| Cualquier persona | Registro, Ingreso | crea su cuenta; la primera queda de administradora; las demás esperan aprobación | CU-S01 |
| Administrador | Usuarios | aprueba o rechaza registros, cambia roles, crea y desactiva cuentas | CU-S02 |
| Administrador | Repositorios y sus modales | conecta un repositorio, copia la URL y el secreto del *webhook*, cambia la política o el bloqueo del merge, desconecta | CU-S03 |
| Desarrollador y administrador | Revisiones, Detalle | consulta las revisiones, abre una, ve cada hallazgo con su ruta y lo clasifica | CU-S06, CU-S07 |
| Desarrollador y administrador | Revisar un PR ahora, Reintentar | pide una revisión sin esperar el *webhook* o repite una | CU-S05 |
| GitHub | ninguna: el *webhook* | avisa de cada *pull request* abierto o actualizado | CU-S04 |

Decisiones de la interfaz, tomadas para que el usuario no lea mal un
resultado:

- «Sin hallazgos» nunca se confunde con «no se analizó»: una revisión fallida
  muestra el motivo y no muestra resumen; los archivos que no compilaron se
  avisan aparte.
- El estado se dice con texto e icono, no solo con color (Publicada ·
  Aprobada, Publicada · Con problemas, En análisis, Pendiente, Fallida).
- Lo que viene de C++ (rutas, nombres de función, commits) va en letra
  monoespaciada, tal como aparece en el código.
- Tema claro y oscuro, y diseño que se adapta a tableta.
