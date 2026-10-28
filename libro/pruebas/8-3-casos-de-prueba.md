# 8.3 Casos de prueba

Un caso de prueba fija una entrada, la condición en que se aplica y el
resultado que se espera, para que cualquiera lo repita y obtenga lo mismo.
Aquí cada caso se diseñó con **valores límite** y **particiones de
equivalencia** (el valor justo en el borde, el de un lado y el del otro) y
cada uno está escrito también como prueba ejecutable con su mismo código en
`sistema/pruebas/casos-de-prueba.test.ts`: la tabla y el código no pueden
divergir sin que la prueba falle.

## Plantilla

Cada caso se documenta con estos campos:

| Campo | Contenido |
|---|---|
| Código | CP-nn, el mismo que lleva la prueba ejecutable |
| Requisito y caso de uso | qué RF-S y qué CU-S cubre |
| Precondición | el estado del sistema antes de la prueba |
| Entrada | los datos exactos que se envían |
| Pasos | qué se hace, en orden |
| Resultado esperado | la respuesta del sistema (código HTTP, mensaje, dato) |
| Resultado obtenido | lo que respondió el sistema en la ejecución del 28-10-2026 |
| Estado | aprobado o fallido |

Ejemplo completo, CP-04:

| Campo | CP-04 Clave del registro |
|---|---|
| Requisito y caso de uso | RF-S01 (política de claves: al menos 10 caracteres, con letras y números); CU-S01 |
| Precondición | instancia con una cuenta de administración; el correo de prueba no está registrado |
| Entrada | claves de 9, 10, 128 y 129 caracteres; una de solo letras y una de solo números |
| Pasos | 1. enviar `POST /api/registro` con cada clave; 2. leer el código de respuesta |
| Resultado esperado | 9 → 400; 10 → 201; 128 → 201; 129 → 400; solo letras → 400; solo números → 400 |
| Resultado obtenido | 400, 201, 201, 400, 400, 400 |
| Estado | aprobado |

## Casos

| Código | Qué prueba | Entrada | Esperado | Obtenido | Estado |
|---|---|---|---|---|---|
| CP-01 | correo obligatorio y con formato (CU-S01) | `""`, `ana`, `ana@`, `ana@ucsm`, `ana ucsm@x.pe` | 400 en todos | 400 en todos | aprobado |
| CP-02 | tamaño máximo del correo | 254 y 255 caracteres | 201 y 400 | 201 y 400 | aprobado |
| CP-03 | nombre obligatorio, de 1 a 100 caracteres | vacío, solo espacios, 100 y 101 | 400, 400, 201, 400 | 400, 400, 201, 400 | aprobado |
| CP-04 | clave de 10 a 128 caracteres con letras y números | 9, 10, 128, 129; solo letras; solo números | 400, 201, 201, 400, 400, 400 | igual | aprobado |
| CP-05 | tipo de dato de cada campo | correo numérico, nombre ausente, nombre como lista | 400 | 400 | aprobado |
| CP-06 | correo ya registrado, sin distinguir mayúsculas | `ADMIN@ucsm.edu.pe` | 409 | 409 | aprobado |
| CP-07 | ingreso: campos obligatorios y mismo error para correo inexistente y clave equivocada (CU-S01) | sin clave; correo inexistente; clave equivocada | 400; 401 y 401 con el mismo cuerpo | igual | aprobado |
| CP-08 | formato `dueño/repositorio` (CU-S03) | válidos: `a/b`, `lab-sistemas/motor-rutas`, `x/repo.con_puntos-y_guiones`; inválidos: vacío, sin barra, sin dueño, sin nombre, dueño que empieza con guion, tres partes, con espacio, dueño de 40 caracteres | 201 los válidos, 400 los inválidos | igual | aprobado |
| CP-09 | política y bloqueo obligatorios y de dominio cerrado | sin política; `Todo`; bloqueo `"si"`; `Silent` y `false` | 400, 400, 400, 201 | igual | aprobado |
| CP-10 | número de PR entero positivo (CU-S05) | `0`, `-1`, `1.5`, `"3"`; repositorio que no es UUID | 400 en todos | 400 en todos | aprobado |
| CP-11 | cálculo del resumen y del veredicto (CU-S06) | un PR con 1 confirmado y 2 posibles | resumen 1/2/0 igual al conteo de hallazgos; `ConProblemas` | igual | aprobado |
| CP-12 | cálculo tras clasificar (CU-S07) | marcar los 3 como falso positivo y reintentar | 0 confirmados, 0 posibles, 3 suprimidos; `Aprobada` | igual | aprobado |
| CP-13 | formato de fechas y del commit | la revisión del CP-11 | ISO 8601 en UTC con milisegundos; sha de 40 hexadecimales | igual | aprobado |
| CP-14 | vínculos (CU-S04, CU-S06) | la revisión del CP-11 | el PR enlaza a `github.com/<repo>/pull/7`; el estado del commit enlaza a `<url pública>/revisiones/<id>` y dice «1 confirmados, 2 posibles» | igual | aprobado |

Resultado: **14 de 14 aprobados** (`npx vitest run pruebas/casos-de-prueba.test.ts`).

## Lista de verificación de los formularios y las pantallas

La práctica pide revisar, en cada formulario, los campos obligatorios y
opcionales, el tamaño, el tipo de dato, los cálculos, el formato y los
vínculos. Cada casilla remite al caso o a la prueba que la comprueba. El
panel valida lo mismo antes de enviar (validación aplicativa, todos los
errores a la vez) y el servicio lo vuelve a validar, porque es quien decide.

| Formulario o pantalla | Obligatorios y opcionales | Tamaño | Tipo de dato | Cálculos | Formato | Vínculos |
|---|---|---|---|---|---|---|
| Registro | correo, nombre, clave y confirmación obligatorios (CP-01, CP-03; `acceso.test.tsx`) | correo ≤ 254, nombre ≤ 100, clave 10 a 128 (CP-02 a CP-04) | texto (CP-05) | — | correo con `@` y dominio (CP-01); reglas de la clave marcadas al escribir | «¿Ya tienes cuenta? Ingresa» |
| Ingreso | correo y clave obligatorios (CP-07) | correo ≤ 254, clave ≤ 128 | texto | — | — | «¿No tienes cuenta? Regístrate»; vuelve a la ruta que se pedía (`acceso.test.tsx`) |
| Crear usuario | los cuatro obligatorios; el rol tiene valor por defecto | como el registro | rol de dominio cerrado | — | como el registro | — |
| Conectar repositorio | nombre, política y bloqueo obligatorios (CP-09) | dueño ≤ 39, nombre ≤ 100 (CP-08) | booleano para el bloqueo (CP-09) | — | `dueño/nombre`; acepta la URL de GitHub y quita `.git` (`dominio.test.ts`) | los pasos *Settings → Webhooks → Add webhook* con la URL y el secreto para copiar |
| Revisar un PR ahora | repositorio y número obligatorios | — | entero positivo (CP-10); acepta `#12` | — | — | enlace a la revisión ya existente (`revisiones.test.tsx`) |
| Lista de revisiones | filtros opcionales | 200 más recientes (8.4.3) | — | «Se actualiza sola» mientras alguna sigue en curso | fecha relativa en hora de Lima; commit corto de 7 caracteres (`dominio.test.ts`) | cada fila abre su detalle; enlace al PR |
| Detalle de revisión | — | — | — | resumen y veredicto (CP-11, CP-12); contador de falsos positivos | fecha y hora; «Marcado por … · hace …» | PR y sus archivos en GitHub (CP-14) |
| Usuarios | rol al aprobar obligatorio | — | — | contador «N por aprobar» en el menú (`usuarios.test.tsx`) | iniciales del avatar | — |
