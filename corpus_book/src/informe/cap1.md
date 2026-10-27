# Capítulo 1 — Introducción y objetivos

## 1.1 Introducción

Un equipo que desarrolla en C++ integra cambios mediante *pull requests*: alguien propone código, otra persona lo revisa y, si está bien, se fusiona (*merge*) con la rama principal. Esa revisión humana es buena para el diseño y la legibilidad, pero mala para un tipo de defecto que no se ve en una sola línea: el uso de un iterador, una referencia o un puntero a un elemento de un contenedor de la biblioteca estándar después de una operación que lo invalidó. Que el uso sea válido o no depende del contenedor, de la operación y a veces de la capacidad disponible, y la norma de C++17 lo fija operación por operación (International Organization for Standardization, 2017). Un uso inválido es comportamiento indefinido: puede funcionar en las pruebas y fallar en producción.

Este proyecto construyó **Centinela C++**, un servicio web que revisa automáticamente los *pull requests* de C++ de un equipo en GitHub. Cuando se abre o actualiza un *pull request*, GitHub avisa a Centinela; Centinela descarga el commit, analiza los archivos que cambiaron, comenta en el mismo *pull request* cada uso inválido en su línea, con la ruta que lo explica (dónde se obtuvo el handle, qué lo invalidó y dónde se usa), y marca el estado del commit para bloquear el *merge* si el equipo lo pide. El equipo entra a Centinela con usuario y clave: el administrador conecta los repositorios y aprueba a las personas; los desarrolladores consultan las revisiones, piden una revisión cuando la necesitan y marcan los falsos positivos para que no se repitan.

El análisis lo hace el segundo producto del proyecto, el **checker `ucsm.ContainerInvalidation`**, una extensión de Clang Static Analyzer (CSA) que modela las reglas de invalidación de la norma para diez contenedores. Antes de ponerlo en el servicio se midió: con un banco de 750 casos etiquetados desde la norma y validados en ejecución, CSA de referencia detecta 80 de 342 usos inválidos y el checker los 342, sin falsas alarmas en los 306 casos seguros (sección 7.7).

El informe presenta el problema y los objetivos en este capítulo; los fundamentos, la metodología y el plan en el capítulo 2; el análisis económico en el capítulo 3; los requerimientos en el capítulo 4; la arquitectura en el capítulo 5; las pantallas, la API y la base de datos en el capítulo 6; y la construcción y el estado del software en el capítulo 7.

## 1.2 Planteamiento del problema

Revisar a mano un uso de un handle exige relacionar tres puntos que suelen estar lejos entre sí: dónde se obtuvo, qué operación modificó el contenedor y dónde se usa después. La regla CTR51-CPP del estándar SEI CERT trata exactamente este defecto (Software Engineering Institute, 2024). Los analizadores existentes ayudan poco: los *checkers* de iteradores de CSA están en el grupo experimental (LLVM Project, 2026a) y, medidos en este proyecto, detectan 48 de 328 usos inválidos sobre el handle que el caso sostiene, y ninguno sobre referencias o punteros.

Aunque existiera un detector bueno, no sirve si nadie lo ejecuta. En un equipo, el lugar donde un defecto se puede detener es el *pull request*: antes del *merge*, en la línea que cambió y con la persona que lo escribió. Si el análisis corre aparte, en la máquina de alguien o en un reporte que nadie lee, el defecto llega igual a la rama principal.

### Árbol de problemas

![Árbol de problemas](../diagramas/1-arbol-problemas.svg)

Tabla: Relaciones del árbol de problemas

| Nivel | Elemento |
|---|---|
| Efecto | Defectos de invalidación que llegan a producción como fallas intermitentes o vulnerabilidades de memoria. |
| Efecto | Tiempo de los revisores dedicado a buscar a mano estos defectos en cada *pull request*. |
| Efecto | Desconfianza en los avisos del análisis estático cuando sus falsas alarmas y omisiones no están medidas. |
| Problema central | Los equipos que desarrollan en C++ integran código con usos invalidados porque su revisión de *pull requests* no los detecta de forma automática y confiable. |
| Causa | El analizador de referencia detecta pocos usos inválidos y ninguno sobre referencias o punteros. |
| Causa | La regla depende del contenedor, la operación y la capacidad: es difícil aplicarla a mano. |
| Causa | El análisis estático no forma parte del flujo del *pull request*: nadie lo corre antes del *merge* ni comenta la línea afectada. |
| Causa | No había un banco etiquetado desde la norma para medir un detector de esta clase de defectos. |

### Formulación del problema

¿Cómo puede un equipo que desarrolla en C++ detectar, en cada *pull request* y antes del *merge*, los usos de iteradores, referencias y punteros invalidados, con un detector cuya precisión, exhaustividad y medida F1 frente a la configuración de referencia de Clang Static Analyzer estén medidas sobre un banco de casos derivado de la norma de C++17?

## 1.3 Descripción del proyecto

El proyecto entrega dos productos que trabajan juntos:

- **Centinela C++**, el sistema que usa el cliente: un servicio web con registro e ingreso, roles de administrador y desarrollador, gestión de repositorios de GitHub, recepción de *webhooks* firmados, una cola de revisiones, publicación de comentarios en línea y del estado del commit, un panel para consultar revisiones y clasificar hallazgos, y una API HTTP. Está escrito en TypeScript sobre Node.js y Fastify, guarda sus datos en SQLite y se despliega con Docker.
- **El checker `ucsm.ContainerInvalidation`**, el motor: un *plugin* de CSA (LLVM/Clang 21) que sigue cada handle hasta su contenedor y aplica las reglas de invalidación de la norma, escritas como datos en `norma/matriz.json` con su cláusula. Lo acompañan el banco de 750 casos, su validación dinámica y el arnés que lo compara con CSA.

Se construyó en incrementos (sección 7.6): primero la imagen de LLVM 21 y el registro del *plugin* (I0), después el núcleo de reglas, los handles, las posiciones, las garantías y las notas de ruta (I1 a I5), la evaluación con el banco y en código real, y por último el servicio Centinela C++ (I7). Cada incremento se cerró con pruebas automáticas.

Tabla: Ejes de construcción del banco

| Eje | Contenido | Finalidad |
|---|---|---|
| A | Contenedor (10 de la biblioteca estándar) | Distinguir garantías de invalidación. |
| B | Operación y condiciones | Identificar la regla aplicable. |
| C | Iterador, referencia o puntero | Medir los tres tipos de handle. |
| D | Forma sintáctica (recta, bucle, condición, función auxiliar) | Medir la sensibilidad a formas de código comparables. |
| E | Garantía previa: ninguna, `reserve` suficiente o handle devuelto por la mutación | Medir falsas alarmas en el buen uso de operaciones que pueden invalidar. |

## 1.4 Objetivos de la investigación

### Objetivo general

Desarrollar Centinela C++, un servicio web con autenticación y roles que revise automáticamente los *pull requests* de C++ de un equipo en GitHub y detecte los usos de iteradores, referencias y punteros invalidados mediante un checker para Clang Static Analyzer, cuya precisión, exhaustividad y medida F1 se midan frente a la configuración de referencia sobre un banco de casos derivado de la norma de C++17.

### Objetivos específicos

- OE1. Construir un banco de casos con usos válidos e inválidos de iteradores, referencias y punteros a elementos de los contenedores de la biblioteca estándar, con etiquetas justificadas por la norma de C++17 y validadas en ejecución, y medir sobre él la configuración de referencia de Clang Static Analyzer.
- OE2. Diseñar e implementar el checker `ucsm.ContainerInvalidation` para Clang Static Analyzer, que asocie cada handle a su contenedor de origen, modele su validez ante las operaciones de la norma y explique cada uso inválido con su ruta.
- OE3. Medir y comparar la precisión, la exhaustividad y la medida F1 de la configuración de referencia y del checker sobre el mismo banco, por contenedor, operación y tipo de handle, y comprobar su comportamiento en código real.
- OE4. Implementar Centinela C++, un servicio web con registro, autenticación y roles que conecte repositorios de GitHub, revise cada *pull request* con el checker, comente cada uso inválido en su línea, bloquee el *merge* cuando el equipo lo pida y permita consultar y clasificar los hallazgos.

### Matriz objetivo resultado capítulo

Tabla: Trazabilidad de objetivos y resultados

| Objetivo | Resultado | Capítulo que lo desarrolla |
|---|---|---|
| OE1 | Banco de 750 casos etiquetado desde la norma (342 inválidos, 306 seguros, 102 dependientes de la capacidad), validado en ejecución (852 ejecuciones, 0 contradicciones); CSA de referencia detecta 80 de 342. | 2: metodología; 4: RF-13 a RF-15; 7: construcción del banco y del arnés. |
| OE2 | Checker `ucsm.ContainerInvalidation` como *plugin* de CSA (LLVM 21): 101 mutaciones y 348 reglas de la norma como datos, con pruebas unitarias y de integración. | 4: RF-01 a RF-12, RF-16, RF-17; 5: arquitectura del motor; 7: construcción. |
| OE3 | Comparación en cuatro condiciones con cotejo por sitio: el checker detecta 342 de 342 sin falsas alarmas; en código real, 781 unidades de cuatro proyectos sin caídas y 10 de 10 defectos sembrados detectados. | 2: protocolo; 4: RF-13, RF-14, RNF-01 a RNF-05; 7: estado y resultados. |
| OE4 | Centinela C++: registro sin usuarios predefinidos, roles, repositorios, *webhook* firmado, cola de revisiones, comentarios en línea y estado del commit, clasificación de hallazgos; backend con 140 pruebas automáticas y *mockups* del panel. | 4: RF-S01 a RF-S05, RNF-S01 a RNF-S06; 5: casos de uso y arquitectura; 6: interfaces y datos; 7: construcción. |

## 1.5 Solución propuesta

### Justificación e importancia

La justificación para el cliente es práctica: el defecto se detiene en el *pull request*, que es donde el equipo ya decide qué entra a la rama principal, y se explica en la línea afectada, sin pedirle a nadie que instale ni ejecute un analizador. Que el *merge* se pueda bloquear convierte el aviso en una regla del equipo y no en una sugerencia.

La justificación técnica es que esta clase de defecto depende de reglas precisas por contenedor y operación que el analizador de referencia no modela, sobre todo para referencias y punteros. El checker las toma de la norma escrita como datos, de modo que cada aviso se puede rastrear hasta su cláusula.

La justificación académica es el banco: 750 casos etiquetados desde la norma, validados en ejecución y sellados, que permiten medir este y otros detectores con un procedimiento reproducible. No se afirma que sea la primera evaluación de este tipo.

La justificación económica se desarrolla en el capítulo 3 como escenarios de ahorro de horas de revisión y de corrección en los equipos que adopten el servicio; no son ahorros medidos en equipos reales.

### Descripción de la solución

Centinela C++ recibe el evento del *pull request* por un *webhook* firmado con HMAC-SHA256, guarda la revisión y su trabajo en la misma transacción y responde enseguida. Un trabajador toma el trabajo, descarga el commit, ejecuta clang con el checker sobre cada archivo C++ cambiado y publica en GitHub una revisión con un comentario por hallazgo y el estado `centinela/invalidacion` del commit. El panel web y la API permiten al equipo administrar usuarios y repositorios, consultar revisiones y clasificar hallazgos; un falso positivo marcado deja de reportarse en el repositorio.

El checker sigue en el estado del análisis cada handle con su contenedor y su posición, consulta la tabla de reglas generada desde `norma/matriz.json` en cada operación y, si el handle quedó invalidado, avisa en el uso con la ruta completa. La política `Silent` avisa solo lo confirmado; `Possibly` avisa también lo que depende de la capacidad. El arnés comparó el checker con CSA en cuatro condiciones sobre el mismo banco.

### Aporte

- Para el cliente: un servicio que lleva la detección de usos invalidados al *pull request*, con roles, trazabilidad de cada revisión y la decisión de bloquear el *merge*.
- Técnico: un checker que modela las reglas de la norma para iteradores, referencias y punteros en diez contenedores, con las reglas como datos verificables.
- Empírico: la medición de CSA y del checker sobre el mismo banco y en código real.
- Instrumental: el banco de 750 casos, su validación dinámica, el arnés y un libro del proyecto que permite reproducir todo en minutos.

### Alcances

Tabla: Delimitación por componente

| Componente | Incluido | Excluido |
|---|---|---|
| Servicio Centinela C++ | Registro sin usuarios predefinidos, ingreso con sesión, roles de administrador y desarrollador, repositorios de GitHub, *webhook* firmado, cola de revisiones, comentarios en línea y estado del commit, clasificación de hallazgos, panel web y API HTTP. | Varias organizaciones en una instancia (*multi-tenant*), facturación, proveedores distintos de GitHub (GitLab, Bitbucket). |
| Checker | Seguimiento y diagnóstico de las reglas de invalidación de la norma para 10 contenedores y los tres tipos de handle. | Uso después de liberación en general, contenedores de terceros. |
| Banco | 750 casos con etiqueta, cláusula y sitio esperado, validados en ejecución. | Casos cuya etiqueta no pueda justificarse con la norma. |
| Arnés | Cuatro condiciones, registros, cotejo por sitio y métricas. | Estudios de adopción con usuarios. |
| Datos | Base SQLite del servicio; archivos JSON versionados de la evaluación. | Datos de terceros fuera de los repositorios que el cliente conecta. |

Tabla: Contenedores cubiertos

| Familia | Contenedores | Mutaciones modeladas |
|---|---|---|
| Secuencias | `std::vector`, `std::deque`, `std::list`, `std::forward_list` | 59 |
| Asociativos ordenados | `std::map`, `std::multimap`, `std::set`, `std::multiset` | 25 |
| Asociativos no ordenados | `std::unordered_map`, `std::unordered_set` | 17 |

El desarrollo se hizo en GNU/Linux con la imagen Docker `checker:llvm21`, que fija LLVM/Clang 21.1.8 y libstdc++ 13, entre septiembre y noviembre de 2026.

### Limitaciones

- **Del análisis.** CSA explora caminos con límites; una llamada cuyo efecto no se conoce o una capacidad no resuelta pueden producir omisiones o avisos posibles. El modelo no conoce el contenido de los contenedores, así que puede explorar un camino imposible (el único falso positivo posible en código real, sección 7.7).
- **Del banco.** Es sintético y lo escribió el equipo con las formas que el checker reconoce; por eso se complementó con código real y defectos sembrados. Las conclusiones valen para el banco, las reglas y las versiones evaluadas.
- **Del servicio.** Atiende a una organización por instancia (*single-tenant*) y solo a GitHub; necesita una URL pública con HTTPS para recibir los *webhooks*. Analiza cada archivo cambiado sin la base de compilación del proyecto (`compile_commands.json`), con rutas de inclusión heurísticas: un archivo que no compila se informa como no analizado, nunca como limpio (RN-S05). Cada archivo tiene un tiempo máximo de análisis, y el contador de intentos fallidos de ingreso vive en memoria y se reinicia con el servicio.
- **De alcance.** Aliasing general y análisis interprocedural sin límites quedan fuera; se incluyen los casos concretos que el banco puede etiquetar.

### Tratamiento de datos y privacidad

Centinela C++ trata datos personales de los usuarios del equipo cliente: correo, nombre, el hash de su clave y sus sesiones; y procesa código fuente privado del cliente. En el Perú esto se rige por la Ley N.º 29733, Ley de Protección de Datos Personales (Congreso de la República del Perú, 2011). Medidas adoptadas:

- **Mínimo necesario.** Solo se piden correo, nombre y clave; no hay usuarios predefinidos.
- **Claves y sesiones.** La clave se guarda solo como hash scrypt con sal aleatoria (Percival y Josefsson, 2016); de la sesión se guarda solo el hash de su token, en una cookie `httpOnly` y `SameSite=Strict` (RNF-S01).
- **Código del cliente.** Se descarga en una carpeta temporal y se borra al terminar el análisis; el código no se envía a ningún servicio externo; el token de GitHub vive en una variable de entorno, fuera del repositorio.
- **Acceso.** Cada petición comprueba el permiso del rol en el servidor; el secreto del *webhook* solo lo ve el administrador.

El banco y los experimentos no contienen datos personales. El código real analizado es de proyectos públicos de licencia abierta.

## 1.6 Síntesis del diseño metodológico

Tabla: Diseño metodológico del proyecto

| Elemento | Definición |
|---|---|
| Tipo y enfoque | Investigación aplicada con enfoque cuantitativo. |
| Diseño | Comparación controlada y pareada de cuatro condiciones sobre el mismo banco; la comparación principal es CSA de referencia frente a la referencia con el checker (`Possibly`). |
| Unidad principal | Sitio de uso de un handle en una ubicación definida. |
| Instrumentos | Matriz normativa, banco de casos, registro de ejecución en SARIF, cotejo por sitio, pruebas automáticas del servicio. |
| Indicadores | VP, FP, VN, FN; precisión, exhaustividad y F1; tiempo y memoria; criterios de aceptación de los casos de uso del servicio. |
| Desarrollo de software | Incremental (I0 a I7), con pruebas automáticas como criterio de cierre de cada incremento. |
| Desarrollo detallado | Apartado 2.3. |

## 1.7 Stakeholders y roles

Tabla: Matriz de poder e interés

| Stakeholder | Poder / interés | Rol |
|---|---|---|
| Organización cliente (equipo que desarrolla en C++) | Alto / alto | Decide adoptar Centinela C++, provee el repositorio de GitHub y la URL donde se despliega. |
| Administrador del equipo | Alto / alto | Primera cuenta: conecta repositorios, configura la política y el bloqueo del *merge*, aprueba usuarios. |
| Desarrollador de C++ | Medio / alto | Recibe los comentarios en su *pull request*, consulta revisiones, pide revisiones y marca falsos positivos. |
| GitHub | Alto / medio | Proveedor externo: envía los *webhooks* y recibe comentarios y estados por su API. |
| Docente y asesoría | Alto / alto | Revisión académica, alcance y aceptación de entregables. |
| Equipo del proyecto | Alto / alto | Diseño, desarrollo, banco, medición y operación del servicio. |
| Comunidad LLVM | Bajo / medio | Posible destinataria del checker y del banco; sin compromiso de aceptación. |

## 1.8 Síntesis de antecedentes

Tabla: Antecedentes relevantes para el alcance

| Antecedente | Relación con el proyecto |
|---|---|
| Balogh (2018) | Diseño del modelado de iteradores en CSA, base de los *checkers* experimentales que se midieron. |
| Higgs (2020) | Detección de invalidación con consultas de CodeQL: otra vía para el mismo defecto. |
| Kashyap et al. (2019) | Generación de bancos de errores para evaluar detectores. |
| Zhang et al. (2023) | Pruebas de analizadores con transformaciones que preservan la semántica (eje D del banco). |
| Teodorescu y Lucanu (2024) | Marco de análisis de uso después de liberación en C++. |
| Christakis y Bird (2016) | Lo que los desarrolladores esperan de un analizador: avisos accionables, integrados en su flujo. |

Christakis y Bird (2016) mostraron que los desarrolladores quieren los avisos dentro de su flujo de trabajo y con pocas falsas alarmas; Centinela responde a lo primero llevando el aviso al *pull request*, y el banco a lo segundo, midiendo las falsas alarmas antes de desplegar. La revisión detallada está en 2.2.

## 1.9 Síntesis del estado del arte

Tabla: Enfoques considerados

| Enfoque | Ventaja para el problema | Restricción |
|---|---|---|
| Checker de CSA | Estado a lo largo de los caminos de análisis. | Complejidad del modelado y límites del motor. |
| Herramienta con LibTooling | Control total del ejecutable. | El seguimiento de estado por caminos hay que construirlo. |
| Consultas de CodeQL | Relaciones entre usos y operaciones en toda la base de código. | Extracción de la base y modelo de consultas propios. |
| Instrumentación dinámica (ASan, modo de depuración de libstdc++) | Observa el error en una ejecución concreta. | Solo ve lo que se ejecuta; sirvió como oráculo del banco. |
| Revisión en el *pull request* con un servicio (bot o GitHub App) | El aviso llega donde el equipo decide el *merge*. | Necesita un servicio desplegado y permisos sobre el repositorio. |

## 1.10 Estándares, técnicas y herramientas

La norma ISO/IEC 14882:2017 es la fuente semántica de las reglas y del banco, y la regla CTR51-CPP la referencia de codificación segura. El servicio sigue OWASP ASVS 4.0 en autenticación y sesiones (OWASP Foundation, 2021), HTTP y cookies según sus RFC (Fielding et al., 2022; Barth, 2011) y la verificación de *webhooks* de GitHub con HMAC (Krawczyk et al., 1997; GitHub, 2026a). El checker sigue las convenciones de LLVM (LLVM Project, 2026b) y su salida se lee en SARIF 2.1.0 (OASIS, 2020). El diseño del servicio aplica el diseño guiado por el dominio (Evans, 2003; Wlaschin, 2018) y la arquitectura de puertos y adaptadores (Cockburn, 2005). Las herramientas se detallan en 2.3.9.

## 1.11 Síntesis de requisitos y casos de uso

Los requisitos completos se desarrollan en el capítulo 4 y los casos de uso en la sección 5.1. Centinela C++ tiene cinco requerimientos funcionales (RF-S01 a RF-S05) y seis no funcionales (RNF-S01 a RNF-S06); su motor de análisis, diecisiete funcionales (RF-01 a RF-17) y ocho no funcionales (RNF-01 a RNF-08). Los actores del sistema son el administrador y el desarrollador del equipo cliente, que entran con usuario y clave, y GitHub, que envía los eventos. Cada caso de uso tiene un criterio de aceptación comprobado por una prueba automática.

## 1.12 Análisis de alternativas de solución

Se tomaron dos decisiones: cómo llevar el análisis al equipo (el producto) y con qué construir el detector (el motor). Cada alternativa se puntuó de 1 a 5 en cada criterio; el total es la suma ponderada.

Tabla: Matriz de decisión del producto

| Criterio | Peso | Servicio web propio (Centinela) | Acción de CI en el repositorio | Herramienta de línea de comandos |
|---|---|---|---|---|
| Aviso en la línea del *pull request* y bloqueo del *merge* | 30 % | 5 | 4 | 1 |
| Usuarios, roles y clasificación de hallazgos persistente | 25 % | 5 | 1 | 1 |
| Configuración única para todos los repositorios del equipo | 20 % | 5 | 2 | 1 |
| Esfuerzo de construcción y operación | 15 % | 2 | 4 | 5 |
| Independencia de un proveedor de CI | 10 % | 4 | 2 | 5 |
| **Total ponderado** | 100 % | **4,45** | **2,65** | **2,00** |

La acción de CI corre en cada repositorio, no recuerda clasificaciones ni tiene usuarios; la herramienta de línea de comandos depende de que alguien la ejecute. El servicio cuesta más construirlo y operarlo, pero es el único que cubre los casos de uso del equipo.

Tabla: Matriz de decisión del motor

| Criterio | Peso | Checker de CSA | LibTooling | CodeQL |
|---|---|---|---|---|
| Seguimiento de estado y caminos | 35 % | 5 | 2 | 3 |
| Integración con la configuración de referencia | 25 % | 5 | 1 | 1 |
| Viabilidad dentro del curso | 25 % | 3 | 2 | 3 |
| Reproducibilidad y licencia | 15 % | 5 | 5 | 3 |
| **Total ponderado** | 100 % | **4,50** | **2,20** | **2,50** |

Solo un checker de CSA permite medir la diferencia contra CSA cambiando un único factor. La viabilidad se comprobó en I0 con el registro del *plugin* en LLVM 21.

## 1.13 Síntesis de viabilidad técnica y económica

Tabla: Brechas técnicas y cómo se cerraron

| Necesidad | Cómo se cerró | Evidencia |
|---|---|---|
| Plataforma LLVM/Clang | Imagen `checker:llvm21` con LLVM 21.1.8 de apt.llvm.org (D-02). | `Dockerfile`; prueba `lit` de registro (I0). |
| API y estado de CSA | *Plugin* con núcleo puro y cáscara sobre CSA. | 40 pruebas del núcleo y 5 archivos `lit`. |
| Etiquetado normativo | Norma como datos con su cláusula, validada en ejecución. | 852 ejecuciones, 0 contradicciones. |
| Evaluación automática | Arnés con SARIF y cotejo por sitio. | 750 casos × 4 condiciones; 11 leyes probadas. |
| Servicio web | Backend TypeScript con arquitectura por capas. | 140 pruebas; demostración de punta a punta con clang real. |

La viabilidad técnica quedó demostrada con el software construido. La económica se evalúa en el capítulo 3: la inversión estimada es de S/ 22 537,50 y el VAN es positivo en los escenarios base y optimista y negativo en el pesimista, lo que muestra que el resultado depende de cuántos equipos adopten el servicio.

## 1.14 Compromisos del proyecto (*trade-offs*)

Tabla: Tensiones y decisiones de alcance

| Tensión | Variable protegida | Decisión |
|---|---|---|
| Un servicio para muchas organizaciones frente a uno por organización | Seguridad del código del cliente y plazo. | Una instancia por organización (*single-tenant*); el *multi-tenant* queda fuera. |
| Cobertura frente a tiempo | Etiquetas revisadas y comparación reproducible. | Diez contenedores con la norma completa como datos, antes que más formas de código. |
| Exhaustividad frente a precisión | Confianza del desarrollador en los avisos. | Dos políticas: `Silent` (solo confirmados) y `Possibly`; el repositorio elige. |
| Análisis completo del proyecto frente a análisis del cambio | Tiempo de respuesta en el *pull request*. | Se analizan los archivos cambiados; lo que no compila se informa. |
| Detalle técnico frente a lectura | Claridad para el usuario. | La ruta del aviso explica obtención, invalidación y uso en la línea. |

## 1.15 Síntesis de gestión y presupuesto

La organización, el cronograma y los costos se desarrollan en 2.4, 2.5 y 3.2. La EDT ordena el trabajo en seis entregables.

![Estructura de desglose del trabajo](../diagramas/1-edt.svg)

Tabla: EDT de entregables

| Código | Entregable | Actividades principales | Horas estimadas |
|---|---|---|---|
| E1 | Perfil y planificación | Problema, objetivos, alcance, requisitos y costos. | 40 |
| E2 | Banco y referencia | Norma como datos, 750 casos, validación dinámica, medición de CSA. | 80 |
| E3 | Checker | Imagen LLVM 21, núcleo, handles, posiciones, garantías, rutas y pruebas. | 120 |
| E4 | Evaluación | Arnés, experimento en cuatro condiciones, código real y defectos sembrados. | 50 |
| E5 | Servicio Centinela C++ | Backend, *mockups*, panel web, pruebas y despliegue con Docker. | 150 |
| E6 | Entrega | Libro del proyecto, informe, artículo, guía de reproducción y CI. | 30 |

La reserva de contingencia es la suma del valor monetario esperado de cada riesgo (EMV = probabilidad × impacto) y se calcula en 2.5.3.
