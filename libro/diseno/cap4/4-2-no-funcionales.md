# 4.2 Requerimientos no funcionales

## Requerimientos de producto

| Código | Característica | Criterio medible | Medido hoy |
|---|---|---|---|
| **RNF-01** | Precisión | 0 avisos confirmados sobre casos `SAFE` del banco y 0 avisos falsos confirmados en código real | 0 de 306 `SAFE`; 0 en 781 unidades reales |
| **RNF-02** | Cobertura | cobertura por caso y sobre el handle sostenido mayor que la de CSA en el mismo banco | 342/342 y 328/328, frente a 80/342 y 48/328 de CSA |
| **RNF-03** | Robustez | el checker no aborta `clang`; toda unidad que no termina se registra como incidente | 0 incidentes en 3 000 ejecuciones del banco y en 682 unidades de RocksDB |
| **RNF-04** | Tiempo | sobrecosto mediano por caso frente a CSA sin el checker menor que 10 % | 0,650 s frente a 0,652 s (`Possibly`): +0,3 % |
| **RNF-05** | Memoria | memoria residente máxima por caso frente a CSA sin el checker menor que 5 % más | 119,1 MB frente a 119,9 MB: +0,7 % |
| **RNF-06** | Claridad del diagnóstico | todo aviso nombra handle, contenedor, operación y línea de la mutación; el posible dice qué falta | RF-11 |
| **RNF-07** | Mantenibilidad | el núcleo de dominio compila sin las cabeceras de Clang, y corregir una regla de la norma no toca código C++ | target `ucsm_dominio` sin `include` de Clang; la norma es un archivo de datos |
| **RNF-S01** | Seguridad del acceso | claves con scrypt y sal aleatoria; token de sesión aleatorio de 256 bits guardado como hash; cookie `httpOnly`, `SameSite=Strict` y `Secure` detrás de HTTPS; bloqueo tras 10 fallos; cabeceras de seguridad (política de contenido, `nosniff`, no enmarcar) en toda respuesta | `cripto.test.ts`, `api.test.ts`; 41 de 41 comprobaciones contra el servicio en marcha (8.4.6) |
| **RNF-S02** | Autenticidad de los *webhooks* | solo se acepta un evento cuya firma HMAC-SHA256 corresponde al secreto del repositorio, comparada en tiempo constante | `cripto.test.ts`; firma mala: 401 |
| **RNF-S03** | Respuesta | el *webhook* responde sin esperar el análisis: el análisis corre en un trabajador aparte | `api.test.ts`: 202 con la revisión `Pendiente` |
| **RNF-S04** | Confiabilidad | encolar y guardar la revisión van en la misma transacción; una revisión interrumpida por una caída se marca como fallida al arrancar y se puede reintentar | `almacen.test.ts`, `casos.test.ts` |
| **RNF-S05** | Mantenibilidad del servicio | el dominio no importa Fastify, SQLite ni Node; cada paquete importa solo lo que su capa permite | `arquitectura.test.ts` |
| **RNF-S06** | Portabilidad | el servicio completo se levanta con una orden de Docker | `docker compose up sistema-demo`; arranca sin usuarios ni claves predefinidas |
| **RNF-S07** | Rendimiento | con 20 conexiones simultáneas y 1 000 revisiones, el p99 de cada consulta del panel es menor que 200 ms; el *webhook* se acusa en menos de 1 s aun con 50 PR a la vez | p99 de 45 ms en la más lenta (la lista); 50 *webhooks* acusados en 77 ms (8.4.1, 8.4.2) |
| **RNF-S08** | Capacidad | con 20 000 revisiones y 100 000 hallazgos la lista responde con p99 menor que 500 ms; un PR de 40 archivos se publica en menos de 1 minuto; un cuerpo de más de 5 MB se rechaza | 22 ms; 1,7 s; 413 (8.4.3) |
| **RNF-S09** | Usabilidad y accesibilidad | 0 violaciones de WCAG 2.1 AA (axe-core) en cada pantalla, en tema claro y oscuro; las tareas frecuentes (abrir una revisión, clasificar un hallazgo, aprobar un registro) en una acción desde su pantalla | 0 en 14 auditorías; 1 acción (8.4.5) |
| **RNF-S10** | Compatibilidad | el panel funciona en Chrome, Firefox y Safari (motores Blink, Gecko y WebKit) en celular (390 px), tableta (768 px) y escritorio (1440 px) sin desplazamiento horizontal | 11 de 11 recorridos y 24 de 24 combinaciones en los 4 navegadores (8.4.4) |
| **RNF-08** | Reproducibilidad | la misma imagen da las mismas cifras; cada ejecución registra versiones y sha256 | `metricas.json` (`meta`) |

## Requerimientos organizacionales

| Código | Descripción | Aceptación |
|---|---|---|
| RNO-01 | Entrega reproducible | código, norma, banco, arnés e imagen Docker en el repositorio |
| RNO-02 | Desarrollo incremental | cada incremento (I0 a I7) entra con sus pruebas `lit`, gtest o Vitest |
| RNO-03 | Versionado | el banco medido y cada versión del servicio corresponden a un *tag* (`banco-1`, `v1.0.0`) |
| RNO-04 | Documentación | el libro del proyecto se regenera con cada cambio (`bench/gen_book.py`) |

## Normas y estándares

| Referencia | Para qué | Cómo se verifica |
|---|---|---|
| ISO/IEC 14882:2017 (N4659) | la semántica de invalidación de cada operación | cada regla de `matriz.json` cita su cláusula; gtest `Norma.InvalidarODependerCitaSuClausula` |
| SEI CERT CTR51-CPP | uso de iteradores, referencias y punteros válidos | el alcance del checker es esta regla para los contenedores de la STL |
| Convenciones de LLVM | estilo y avisos del código del plugin | se compila con `-Wall -Wextra -Werror=switch` (`UCSM_WARNINGS`) |
| OWASP ASVS 4.0 (V2, V3) | autenticación y manejo de sesiones del servicio | RNF-S01; pruebas de `api.test.ts` |
| WCAG 2.1, nivel AA | accesibilidad del panel web | RNF-S09; axe-core y `contraste.test.ts` |
| ISO/IEC 25010:2011 | las características de calidad que organizan las pruebas no funcionales (eficiencia, compatibilidad, usabilidad, seguridad) | capítulo 8 |
| GitHub REST API v3 y *webhooks* | integración con los repositorios | cliente probado contra un GitHub simulado (`cliente.test.ts`) |
| APA 7 | citas y referencias del informe | revisión |

## Requerimientos externos

| Categoría | Requisito | Aceptación |
|---|---|---|
| Interoperabilidad | la salida es SARIF 2.1 de CSA | el arnés la lee sin adaptadores |
| Ética | ningún resultado se escribe a mano | toda cifra sale de `test/experimento/` o de `test/codigo_real/`; las de RNF-04 y RNF-05 las calcula `bench/rendimiento.py` desde `test/experimento/ejecucion.json` |
| Privacidad | el banco no contiene datos personales; el servicio guarda de cada usuario solo correo, nombre y el hash de su clave, y no guarda el código de los repositorios | el *tarball* se borra al terminar cada análisis (`cliente.test.ts`) |
| Licencias | los proyectos analizados conservan su licencia; no se redistribuye su código | sólo se guardan avisos y *commits* |
