# 8.7 Soporte y mantenimiento

El plan de soporte se organiza con las prácticas de gestión de servicios de
ITIL 4 (Axelos, 2019), y el de mantenimiento con los tipos de mantenimiento
de ISO/IEC/IEEE 14764:2022 (International Organization for Standardization et al., 2022a). El objetivo es que, una
vez entregado, el servicio siga revisando *pull requests* sin perder
*webhooks* ni dar avisos incorrectos, y que cada cambio posterior conserve
la trazabilidad que el proyecto tuvo durante su construcción. El costo del
plan es el mantenimiento anual del capítulo 3, de 50 horas por año
(S/ 1 750).

## Modelo de soporte

Cada organización instala su propia instancia (*single-tenant*, 1.5.5), por
lo que el soporte tiene dos niveles. El primer nivel es el administrador de
la organización. Gestiona usuarios y repositorios desde el panel, consulta
la bitácora del servicio y reintenta las revisiones fallidas. El segundo
nivel es el equipo del proyecto. Corrige defectos del servicio y del
checker, publica versiones y actualiza las dependencias. Las solicitudes al
equipo se registran como *issues* del repositorio, con una etiqueta por tipo
(incidente, problema, solicitud, falso positivo, falso negativo) que
permite medirlas.

Tabla: Niveles de soporte

| Nivel | Quién | Qué atiende | Herramientas |
|---|---|---|---|
| Primero | administrador de la organización | usuarios y roles, repositorios, revisiones fallidas, clasificación de hallazgos, reenvío de *webhooks* | panel, bitácora JSON del contenedor, *Recent Deliveries* de GitHub |
| Segundo | equipo del proyecto | defectos del servicio y del checker, versiones, dependencias, cambios de la API de GitHub | *issues* y *pull requests* del repositorio, CI, banco del checker |

## Prácticas de ITIL 4 que se aplican

Tabla: Prácticas de ITIL 4 en Centinela C++

| Práctica de ITIL 4 | Cómo se aplica en Centinela C++ | Evidencia en el proyecto |
|---|---|---|
| Gestión de incidentes | se restablece el servicio lo antes posible: el *proxy* vuelve a la versión anterior o se reinicia el contenedor; las revisiones interrumpidas se marcan como fallidas al arrancar y el usuario las reintenta | 7.3 g); RNF-S04; procedimiento de 8.5 |
| Gestión de problemas | después del incidente se busca la causa: se escribe primero la prueba mínima que lo reproduce y luego la corrección | los defectos que destaparon las pruebas del capítulo 8 y los del checker que destapó el código real (D-22 y D-23, 7.7) |
| Habilitación de cambios | todo cambio entra por *pull request* con revisión cruzada y CI en verde; un cambio de alcance se registra con motivo, impacto y decisión | 2.5.6; 7.3 e) |
| Gestión de versiones y despliegue | versionado semántico y despliegue *blue-green* con respaldo previo de la base | 7.3 f); 8.5 |
| Monitoreo y gestión de eventos | `GET /salud` para el *proxy*; bitácora en JSON con nivel `info` y `error` por cada revisión y cada arranque | 6.7; `paquetes/app/src/componer.ts` |
| Gestión de solicitudes de servicio | alta de usuarios, cambio de rol y conexión de repositorios las resuelve el administrador desde el panel, sin intervención del equipo | RF-S01, RF-S02 |
| Gestión del conocimiento | el libro, el informe y el código se versionan juntos; cada incidente resuelto deja su prueba y su decisión escrita | 8.6; registro de decisiones de diseño (5.8) |
| Gestión de la configuración del servicio | la imagen Docker fija LLVM 21, Node y las dependencias; la configuración está en variables de entorno documentadas | `Dockerfile`; `sistema/.env.ejemplo`; 8.4.4 |

## Tipos de mantenimiento

ISO/IEC/IEEE 14764:2022 distingue el mantenimiento correctivo, que corrige
defectos encontrados después de la entrega; el preventivo, que corrige
defectos latentes antes de que fallen; el adaptativo, que mantiene el
producto útil cuando cambia su entorno; y el perfectivo o evolutivo, que
agrega funciones o mejora atributos de calidad.

Tabla: Plan de mantenimiento por tipo

| Tipo | Disparador | Acción | Frecuencia | Horas por año |
|---|---|---|---|---|
| Correctivo | un *issue* de incidente, un falso positivo o un falso negativo reportado | rama `fix/` o `hotfix/<versión>`, prueba que reproduce el defecto (caso `lit` si es del checker), corrección, banco completo y versión PATCH | a demanda | 15 |
| Preventivo | revisión programada | actualizar dependencias de npm y revisar avisos de seguridad (`npm audit`); volver a correr las pruebas no funcionales y de seguridad (41 comprobaciones); comprobar el respaldo de la base restaurándolo | trimestral | 12 |
| Adaptativo | nueva versión de LLVM o de libstdc++, cambio en la API REST o en los *webhooks* de GitHub | actualizar la imagen y repetir las cuatro condiciones del experimento (2.5.6); ajustar el cliente de GitHub con su prueba contra el GitHub simulado | cuando ocurre el cambio; al menos con cada versión mayor de LLVM | 13 |
| Evolutivo | una necesidad de los usuarios aprobada por el equipo | nueva función o regla de la norma con su requisito, su prueba y una versión MINOR | por versión | 10 |
| **Total** | | | | **50** |

## Acuerdo de nivel de servicio propuesto

Los tiempos son una propuesta del equipo para el servicio por suscripción
del capítulo 3; no se han medido con clientes.

Tabla: Tiempos de atención propuestos

| Prioridad | Ejemplo | Primera respuesta | Solución o alternativa |
|---|---|---|---|
| Alta | el servicio no recibe *webhooks* o todas las revisiones fallan | 4 horas hábiles | 1 día hábil (volver a la versión anterior) |
| Media | un falso positivo o un archivo que no se analiza | 1 día hábil | en la siguiente versión PATCH |
| Baja | una mejora o una regla nueva | 5 días hábiles | se planifica como mantenimiento evolutivo |

## Indicadores

El soporte se mide con cuatro indicadores que salen de los *issues* y de la
bitácora: el tiempo medio de restauración de los incidentes, el número de
incidentes que se repiten por la misma causa (debe ser cero si la gestión de
problemas funciona), la proporción de revisiones fallidas sobre el total y
el número de falsos positivos reportados por versión del checker.
