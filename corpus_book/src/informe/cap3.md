# Capítulo 3 — Análisis costo beneficio del proyecto

El análisis económico evalúa Centinela C++ desde la perspectiva de los equipos que lo adoptan: se valoriza el esfuerzo de construirlo, se suman los costos de operarlo y se simulan los beneficios por horas de ingeniería ahorradas. No son ingresos por ventas ni ahorros ya medidos en equipos reales; son escenarios con supuestos declarados, y su sensibilidad a esos supuestos se muestra en 3.6.3.

## 3.1 Consideraciones metodológicas previas

El presupuesto combina recursos valorizados (las horas del equipo y de la asesoría tienen costo de oportunidad aunque no se paguen) y desembolsos (servidor, dominio, energía, internet). Los beneficios son horas que ahorrarían los equipos adoptantes; no entran como dinero a los autores. El flujo se interpreta como evaluación económica agregada.

El horizonte es de cinco años, 2027 a 2031. La tasa de descuento es 12 %, un supuesto del equipo como costo de oportunidad del capital; como no es una tasa de mercado verificada, el VAN se recalcula también con 8 % y 16 % (3.6.3).

El modelo de operación es *single-tenant*: cada organización que adopta Centinela C++ tiene su propia instancia, en un servidor virtual con su dominio y HTTPS, y el equipo del proyecto mantiene el software para todas.

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
| Servidor virtual para pruebas y demostración | 3 meses × 40 | 120,00 |
| Dominio | 1 año | 60,00 |
| **Inversión total (I0)** | | **22 537,50** |

Tabla: Resumen por naturaleza

| Categoría | Monto S/ | Participación |
|---|---|---|
| Directos (desarrollo, contingencia, asesoría, servidor y dominio) | 21 507,50 | 95,4 % |
| Indirectos (depreciación, energía e internet) | 1 030,00 | 4,6 % |
| **Total** | **22 537,50** | **100 %** |

Tabla: Costos de operación por año

| Concepto | Cálculo | Monto S/ por año |
|---|---|---|
| Mantenimiento del software (fijo) | 50 h × 45 | 2 250,00 |
| Servidor virtual por organización adoptante | 12 × 40 | 480,00 |
| Dominio por organización adoptante | 1 × 60 | 60,00 |

El mantenimiento es fijo: corrige errores, actualiza LLVM y las dependencias y atiende cambios de la API de GitHub para todas las instancias. El servidor y el dominio crecen con cada organización adoptante (S/ 540 por año cada una).

## 3.3 Beneficios del proyecto

### Fundamento de la cuantificación

Se cuantifican dos beneficios por equipo adoptante: las horas que cuesta un defecto de invalidación que llega a producción y que Centinela detiene en el *pull request*, y las horas de revisión manual que ahorra un aviso automático. El escenario base supone 27 horas por defecto evitado (diagnóstico de una falla intermitente, corrección, prueba y despliegue) y media hora por aviso que ahorra una búsqueda manual en la revisión. **Son supuestos del equipo, no mediciones ni cifras de una fuente**: por eso la sección 3.6.3 recalcula el VAN con 13,5 y 40 horas por defecto. La tarifa de un desarrollador de C++ se tomó de S/ 35 a S/ 55 por hora según el escenario.

Los beneficios no se derivan del banco: que el checker detecte 342 de 342 en el banco muestra su capacidad técnica, no cuántos defectos tiene el código de un cliente.

### Flujos de beneficio cuantificados

Tabla: Beneficio por equipo y año

| Parámetro | Pesimista | Base | Optimista |
|---|---|---|---|
| Defectos evitados | 2 | 3 | 4 |
| Avisos que ahorran revisión manual | 20 | 40 | 60 |
| Tarifa por hora S/ | 35 | 45 | 55 |
| Ahorro por defectos S/ | 1 890 | 3 645 | 5 940 |
| Ahorro en revisión S/ | 350 | 900 | 1 650 |
| Beneficio anual S/ | 2 240 | 4 545 | 7 590 |
| Menos servidor y dominio S/ | 540 | 540 | 540 |
| **Beneficio neto por equipo S/** | **1 700** | **4 005** | **7 050** |

Ahorro por defectos = defectos × 27 h × tarifa. Ahorro en revisión = avisos × 0,5 h × tarifa.

### Senda de adopción

Tabla: Organizaciones adoptantes por año

| Escenario | 2027 | 2028 | 2029 | 2030 | 2031 |
|---|---|---|---|---|---|
| Pesimista | 1 | 2 | 3 | 5 | 7 |
| Base | 2 | 5 | 9 | 14 | 20 |
| Optimista | 3 | 8 | 15 | 25 | 40 |

### Beneficios intangibles

Tabla: Beneficios no monetizados

| Beneficio | Destinatario | Condición |
|---|---|---|
| Revisión de *pull requests* con reglas de la norma, igual para todo el equipo | Equipos adoptantes | Repositorio conectado y política elegida. |
| Banco reutilizable de 750 casos | Investigadores y desarrolladores de analizadores | Etiquetas y licencia documentadas. |
| Experiencia en análisis estático y servicios web seguros | Integrantes | Desarrollo y evaluación realizados. |
| Evidencia sobre la cobertura de CSA | Comunidad LLVM | Medición reproducible. |

No se les asigna valor para no inventarlo; eso no hace del total un límite inferior, porque los beneficios cuantificados también pueden estar sobreestimados.

## 3.4 Flujo de caja del proyecto

El año cero contiene la inversión. Cada año siguiente: organizaciones adoptantes × beneficio neto por equipo − mantenimiento fijo (S/ 2 250).

Tabla: Flujos netos en soles

| Escenario | Año 0 | 2027 | 2028 | 2029 | 2030 | 2031 |
|---|---|---|---|---|---|---|
| Pesimista | −22 537,50 | −550 | 1 150 | 2 850 | 6 250 | 9 650 |
| Base | −22 537,50 | 5 760 | 17 775 | 33 795 | 53 820 | 77 850 |
| Optimista | −22 537,50 | 18 900 | 54 150 | 103 500 | 174 000 | 279 750 |

## 3.5 Valor actual neto

### Cálculo del VAN

VAN = −I0 + Σ Ft / (1 + k)^t, con I0 = S/ 22 537,50 y k = 0,12.

Tabla: VAN a 12 %

| Escenario | VAN S/ | Interpretación |
|---|---|---|
| Pesimista | −10 635,57 | No recupera la inversión: siete organizaciones al quinto año no bastan. |
| Base | 99 207,86 | Positivo con los supuestos declarados. |
| Optimista | 380 492,61 | Positivo con los supuestos declarados. |

### Análisis del VAN

El resultado depende de la adopción. En el escenario pesimista el VAN es negativo porque el servicio tiene costos que el checker solo no tenía: el mantenimiento fijo y un servidor por organización. Si nadie adoptara el servicio y se mantuviera el mantenimiento, el VAN sería −S/ 30 648,25. El proyecto se justifica económicamente solo si llega a un número de organizaciones cercano al del escenario base; 3.6.3 da el umbral.

## 3.6 Tasa interna de retorno

### Cálculo de la TIR

La TIR es la tasa que anula el VAN. Se calculó por bisección sobre los flujos de la tabla anterior.

Tabla: TIR

| Escenario | TIR | Tasa de comparación |
|---|---|---|
| Pesimista | −3,46 % | 12 % |
| Base | 83,06 % | 12 % |
| Optimista | 181,52 % | 12 % |

### Análisis de la TIR

En los escenarios base y optimista la TIR supera ampliamente la tasa de comparación, porque los beneficios crecen con cada organización mientras la inversión se hace una vez. En el pesimista es negativa: ni sin descontar se recupera la inversión en cinco años. Las TIR altas no son rendimientos que vayan a obtener los autores; son indicadores del modelo.

### Punto de equilibrio y sensibilidad

Tabla: Sensibilidad del VAN del escenario base

| Variable | Valor | VAN S/ |
|---|---|---|
| Tasa de descuento | 8 % | 117 405,30 |
| Tasa de descuento | 12 % | 99 207,86 |
| Tasa de descuento | 16 % | 84 078,47 |
| Horas por defecto evitado | 13,5 | 40 116,03 |
| Horas por defecto evitado | 27 | 99 207,86 |
| Horas por defecto evitado | 40 | 156 111,09 |

La proporción crítica de la senda base de adopción es 23,6 %: con menos de una cuarta parte de las organizaciones del escenario base (unas cinco al quinto año), el VAN es negativo. Aun con la mitad de las horas por defecto el escenario base sigue siendo positivo, así que el resultado es más sensible a la adopción que al supuesto de horas.

## 3.7 Evaluación del impacto estratégico

Para el cliente, Centinela C++ detiene una clase de defectos graves en el lugar donde ya decide qué entra a su código, sin pedirle que instale nada. Para el proyecto, deja un checker medido, un banco reutilizable y un servicio que lo pone en uso.

La viabilidad técnica está demostrada con el software construido y probado. La económica es favorable solo si se consigue adopción: el escenario pesimista no recupera la inversión, y el umbral de 23,6 % de la senda base fija cuántas organizaciones se necesitan. La decisión que sigue es validar la adopción con un piloto en un equipo real antes de invertir en el *multi-tenant*.
