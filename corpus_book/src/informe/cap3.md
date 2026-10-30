# Capítulo 3 — Análisis costo beneficio del proyecto

El análisis económico evalúa Centinela C++ como un servicio que una organización contrata mediante una suscripción mensual. Se valoriza el esfuerzo de construirlo, se suman los costos de mantenerlo y se estiman los ingresos por suscripciones en tres escenarios de adopción. Cada parámetro proviene de una fuente pública o se declara como supuesto; los supuestos se someten a un análisis de sensibilidad en la sección 3.6.3. Los cálculos se reproducen con `bench/informe/evaluacion_economica.py`.

## 3.1 Consideraciones metodológicas previas

El presupuesto combina recursos valorizados y desembolsos. Las horas del equipo y de la asesoría se valorizan aunque no se paguen, porque tienen un costo de oportunidad; el servidor, el dominio, la energía y el internet son desembolsos. Los ingresos son las suscripciones que pagarían las organizaciones que adopten el servicio.

El modelo de operación es de una instancia por organización (*single-tenant*): cada organización despliega Centinela C++ en su propio servidor con la imagen Docker del proyecto, y el equipo mantiene el software para todas. El precio se fija por desarrollador activo al mes, que es la forma en que GitHub cobra sus productos de análisis de código (GitHub, 2025).

El horizonte es de cinco años, de 2027 a 2031. La tasa de descuento es la tasa activa promedio en moneda nacional (TAMN), de 16,59 % anual al 9 de julio de 2026 (Superintendencia de Banca, Seguros y AFP, 2026), que representa lo que costaría financiar la inversión con un préstamo. Para la sensibilidad se usan la tasa social de descuento del Ministerio de Economía y Finanzas, de 8 % (Ministerio de Economía y Finanzas, 2019), y la tasa promedio de las operaciones de los últimos 30 días (FTAMN), de 32,39 %. Los montos en dólares se convierten a soles con el tipo de cambio interbancario de S/ 3,44 por dólar de mediados de octubre de 2026 (Banco Central de Reserva del Perú, 2026). El flujo se calcula antes de impuestos y sin comisiones de cobro.

## 3.2 Costos del proyecto

Tabla: Costos de inversión

| Concepto | Cantidad y tarifa | Monto S/ |
|---|---|---|
| Desarrollo del equipo | 470 h × 35 (detalle por EDT en 2.5.3) | 16 450,00 |
| Reserva de contingencia | suma del EMV de R1 a R10 (2.5.3) | 2 957,50 |
| Asesoría valorizada | 24 h × 80 | 1 920,00 |
| Licencias | herramientas de código abierto | 0,00 |
| Depreciación del equipo de cómputo | 3 meses | 400,00 |
| Energía incremental | 3 meses × 90 | 270,00 |
| Internet | 3 meses × 120 | 360,00 |
| Servidor virtual para pruebas y demostración | 3 meses × US$ 24 × 3,44 | 247,68 |
| Dominio | 1 año | 60,00 |
| **Inversión total (I0)** | | **22 665,18** |

El servidor corresponde al plan básico de DigitalOcean con 2 procesadores virtuales y 4 GB de memoria, de US$ 24 al mes (DigitalOcean, 2026), suficiente para ejecutar el servicio y Clang.

Tabla: Resumen por naturaleza

| Categoría | Monto S/ | Participación |
|---|---|---|
| Directos (desarrollo, contingencia, asesoría, servidor y dominio) | 21 635,18 | 95,5 % |
| Indirectos (depreciación, energía e internet) | 1 030,00 | 4,5 % |
| **Total** | **22 665,18** | **100 %** |

Tabla: Costos de operación por año

| Concepto | Cálculo | Monto S/ por año |
|---|---|---|
| Mantenimiento del software (fijo) | 50 h × 35 | 1 750,00 |
| Dominio del proyecto | 1 × 60 | 60,00 |
| **Total** | | **1 810,00** |

El mantenimiento corrige errores, actualiza LLVM y las dependencias y atiende los cambios de la API de GitHub para todas las instancias. El servidor de cada organización lo paga la propia organización, por lo que no forma parte de los costos del proyecto; se incluye en la comprobación del lado del cliente (sección 3.3.1).

## 3.3 Beneficios del proyecto

### Fundamento de la cuantificación

El beneficio del proyecto es el ingreso por suscripciones. El precio se fijó en US$ 5 por desarrollador activo al mes. Como referencia, GitHub cobra US$ 30 por desarrollador activo al mes por GitHub Code Security (GitHub, 2025) y US$ 10 por GitHub Code Quality (GitHub, 2026c). Centinela C++ cubre una sola clase de defecto, por lo que su precio se fijó en la mitad del menor de esos dos productos. El número de desarrolladores activos por organización y el número de organizaciones que adoptan el servicio son supuestos del equipo, porque no existe un registro de los equipos que podrían contratarlo. Por eso se presentan tres escenarios y el umbral de adopción a partir del cual el proyecto es rentable.

Para que una organización contrate el servicio, su costo debe ser menor que el ahorro que obtiene. Según un estudio del National Institute of Standards and Technology, corregir un defecto de programación cuesta en promedio 3,2 horas si se encuentra durante la programación y 14,8 horas si se encuentra después de entregar el software (Tassey, 2002, tabla 7-5). Detenerlo en la revisión ahorra, entonces, unas 11,6 horas. El costo por hora de un ingeniero de sistemas se calculó con los sueldos que publica Ponte en Carrera, de S/ 2 876 en promedio y hasta S/ 5 000 mensuales (Agencia Peruana de Noticias Andina, 2023), más las cargas del empleador.

Tabla: Parámetros del análisis y sus fuentes

| Parámetro | Valor | Fuente |
|---|---|---|
| Precio de la suscripción | US$ 5 por desarrollador activo al mes | Fijado por debajo de GitHub Code Quality (US$ 10) y GitHub Code Security (US$ 30) (GitHub, 2025, 2026c) |
| Tipo de cambio | S/ 3,44 por US$ | Banco Central de Reserva del Perú (2026) |
| Tasa de descuento | 16,59 % (8 % y 32,39 % en la sensibilidad) | Superintendencia de Banca, Seguros y AFP (2026); Ministerio de Economía y Finanzas (2019) |
| Horas ahorradas por defecto detenido en la revisión | 11,6 h (14,8 h − 3,2 h) | Tassey (2002, tabla 7-5) |
| Sueldo mensual de un ingeniero de sistemas | S/ 2 876 en promedio; S/ 5 000 como máximo | Agencia Peruana de Noticias Andina (2023), con datos de Ponte en Carrera |
| Costo anual del empleador | 16,43 sueldos: 12 sueldos, 2 gratificaciones con su bonificación de 9 %, CTS y 9 % de aporte a EsSalud | Ley N.º 27735, Ley N.º 30334, Ley N.º 26790 (Congreso de la República del Perú, 1997, 2002, 2015) y Decreto Supremo N.º 001-97-TR (Ministerio de Trabajo y Promoción Social, 1997) |
| Horas de trabajo al año | 2 160 (48 h semanales, 30 días de vacaciones y 12 feriados) | Supuesto del equipo con la jornada máxima legal |
| Servidor por organización | US$ 24 al mes | DigitalOcean (2026) |
| Desarrolladores activos por organización | 5, 10 y 15 según el escenario | Supuesto del equipo |
| Organizaciones que adoptan el servicio | Tabla de la senda de adopción | Supuesto del equipo |

Con esos datos, el costo de una hora de trabajo para el empleador es de S/ 21,88 con el sueldo promedio y de S/ 38,03 con el máximo, y cada defecto detenido en la revisión ahorra entre S/ 253,76 y S/ 441,18. En el escenario base, una organización de diez desarrolladores paga S/ 2 064 al año por la suscripción y S/ 990,72 por su servidor, es decir, S/ 3 054,72. Recupera ese costo si el servicio le permite detener entre 7 y 12 defectos de este tipo al año, según el sueldo de sus ingenieros. El proyecto no midió cuántos defectos de invalidación introduce un equipo en un año; por eso esta comprobación indica la condición que debe cumplirse para que el cliente obtenga un beneficio, y no un resultado observado.

### Flujos de beneficio cuantificados

Tabla: Ingreso por organización y año

| Parámetro | Pesimista | Base | Optimista |
|---|---|---|---|
| Desarrolladores activos por organización | 5 | 10 | 15 |
| Precio por desarrollador y mes (US$) | 5 | 5 | 5 |
| Tipo de cambio (S/ por US$) | 3,44 | 3,44 | 3,44 |
| **Ingreso anual por organización S/** | **1 032,00** | **2 064,00** | **3 096,00** |

Ingreso anual por organización = desarrolladores × US$ 5 × 12 meses × 3,44.

### Senda de adopción

Tabla: Organizaciones adoptantes por año

| Escenario | 2027 | 2028 | 2029 | 2030 | 2031 |
|---|---|---|---|---|---|
| Pesimista | 1 | 2 | 3 | 5 | 7 |
| Base | 2 | 5 | 9 | 14 | 20 |
| Optimista | 3 | 8 | 15 | 25 | 40 |

La senda es un supuesto. Como referencia del tamaño del mercado, el 20,3 % de los 45 566 desarrolladores profesionales que respondieron la encuesta de Stack Overflow de 2024 usó C++ (Stack Overflow, 2024). Ese dato muestra que hay muchos equipos que trabajan con este lenguaje, pero no permite estimar cuántos adoptarían el servicio.

### Beneficios intangibles

Tabla: Beneficios no monetizados

| Beneficio | Destinatario | Condición |
|---|---|---|
| Revisión de *pull requests* con reglas de la norma, igual para todo el equipo | Equipos adoptantes | Repositorio conectado y política elegida. |
| Banco reutilizable de 750 casos | Investigadores y desarrolladores de analizadores | Etiquetas y licencia documentadas. |
| Experiencia en análisis estático y servicios web seguros | Integrantes | Desarrollo y evaluación realizados. |
| Evidencia sobre la cobertura de CSA | Comunidad LLVM | Medición reproducible. |

A estos beneficios no se les asignó un valor monetario, porque no hay una base para estimarlo.

## 3.4 Flujo de caja del proyecto

El año cero contiene la inversión. En cada año siguiente, el flujo es el número de organizaciones adoptantes por el ingreso anual por organización, menos el costo de operación de S/ 1 810.

Tabla: Flujos netos en soles

| Escenario | Año 0 | 2027 | 2028 | 2029 | 2030 | 2031 |
|---|---|---|---|---|---|---|
| Pesimista | −22 665,18 | −778,00 | 254,00 | 1 286,00 | 3 350,00 | 5 414,00 |
| Base | −22 665,18 | 2 318,00 | 8 510,00 | 16 766,00 | 27 086,00 | 39 470,00 |
| Optimista | −22 665,18 | 7 478,00 | 22 958,00 | 44 630,00 | 75 590,00 | 122 030,00 |

## 3.5 Valor actual neto

### Cálculo del VAN

VAN = −I0 + Σ Ft / (1 + k)^t, con I0 = S/ 22 665,18 y k = 0,1659.

Tabla: VAN a 16,59 %

| Escenario | VAN S/ | Interpretación |
|---|---|---|
| Pesimista | −18 008,06 | No recupera la inversión: siete organizaciones de cinco desarrolladores al quinto año no son suficientes. |
| Base | 29 142,80 | Recupera la inversión y genera un excedente con los supuestos declarados. |
| Optimista | 126 352,54 | Recupera la inversión y genera un excedente con los supuestos declarados. |

### Análisis del VAN

El resultado depende principalmente de la adopción. En el escenario pesimista, el VAN es negativo porque los ingresos de pocas organizaciones pequeñas apenas cubren el mantenimiento. En el escenario base, el proyecto recupera la inversión con veinte organizaciones al quinto año. La sección 3.6.3 indica el número de organizaciones a partir del cual el VAN es positivo.

## 3.6 Tasa interna de retorno

### Cálculo de la TIR

La TIR es la tasa de descuento con la que el VAN es igual a cero. Se calculó por bisección sobre los flujos de la sección 3.4.

Tabla: TIR

| Escenario | TIR | Tasa de comparación |
|---|---|---|
| Pesimista | −17,14 % | 16,59 % |
| Base | 46,39 % | 16,59 % |
| Optimista | 102,74 % | 16,59 % |

### Análisis de la TIR

En los escenarios base y optimista, la TIR supera la tasa de comparación, porque los ingresos crecen con cada organización mientras que la inversión se realiza una sola vez. En el pesimista es negativa, lo que significa que los flujos de los cinco años no alcanzan a cubrir la inversión ni siquiera sin descontarlos.

### Punto de equilibrio y sensibilidad

Tabla: Sensibilidad del VAN del escenario base

| Variable | Valor | VAN S/ |
|---|---|---|
| Tasa de descuento | 8 % | 46 858,10 |
| Tasa de descuento | 16,59 % | 29 142,80 |
| Tasa de descuento | 32,39 % | 9 688,45 |
| Precio por desarrollador y mes | US$ 3 | 6 081,28 |
| Precio por desarrollador y mes | US$ 5 | 29 142,80 |
| Precio por desarrollador y mes | US$ 10 | 86 796,60 |
| Desarrolladores por organización | 5 | 315,90 |
| Desarrolladores por organización | 15 | 57 969,70 |

El VAN del escenario base es igual a cero cuando la adopción llega al 49,5 % de la senda base, es decir, a unas diez organizaciones de diez desarrolladores en 2031. El resultado sigue siendo positivo con la tasa más alta y con un precio de US$ 3, pero es casi nulo si las organizaciones tienen solo cinco desarrolladores. Por tanto, el número de organizaciones y su tamaño influyen en el resultado más que la tasa de descuento.

## 3.7 Evaluación del impacto estratégico

Para el cliente, Centinela C++ detecta una clase de defectos graves en el momento en que decide qué cambios incorporar a su código, sin que sus desarrolladores tengan que instalar ninguna herramienta. Para el proyecto, deja un motor de análisis medido, un banco de casos reutilizable y un servicio que lo pone en uso.

La viabilidad técnica se comprobó con el software construido y probado. La viabilidad económica depende de la adopción: el escenario pesimista no recupera la inversión, y se necesitan alrededor de diez organizaciones de diez desarrolladores al quinto año para que el VAN sea positivo. Además, el cliente obtiene un beneficio solo si el servicio le permite detener entre 7 y 12 defectos de este tipo al año. Por ello, el paso siguiente es un piloto con un equipo real que mida cuántos defectos detecta el servicio y cuánto tiempo ahorra, antes de invertir en una versión para varias organizaciones (*multi-tenant*).
