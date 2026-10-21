# 4.2 Requerimientos no funcionales

## Requerimientos de producto

| Código | Característica | Criterio medible | Medido hoy |
|---|---|---|---|
| **RNF-01** | Precisión | 0 avisos confirmados sobre casos `SAFE` del banco y 0 avisos falsos confirmados en código real | 0 de 306 `SAFE`; 0 en 781 unidades reales |
| **RNF-02** | Cobertura | cobertura por caso y sobre el handle sostenido mayor que la de CSA en el mismo banco | 342/342 y 328/328, frente a 80/342 y 48/328 de CSA |
| **RNF-03** | Robustez | el checker no aborta `clang`; toda unidad que no termina se registra como incidente | 0 incidentes en 3 000 ejecuciones del banco y en 682 unidades de RocksDB |
| **RNF-04** | Tiempo | sobrecosto mediano por caso frente a CSA sin el checker menor que 10 % | 0.650 s frente a 0.652 s (`Possibly`): +0.3 % |
| **RNF-05** | Memoria | memoria residente máxima por caso frente a CSA sin el checker menor que 5 % más | 119.1 MB frente a 119.9 MB: +0.7 % |
| **RNF-06** | Claridad del diagnóstico | todo aviso nombra handle, contenedor, operación y línea de la mutación; el posible dice qué falta | RF-11 |
| **RNF-07** | Mantenibilidad | el núcleo de dominio compila sin las cabeceras de Clang, y corregir una regla de la norma no toca código C++ | target `ucsm_dominio` sin `include` de Clang; la norma es un archivo de datos |
| **RNF-08** | Reproducibilidad | la misma imagen da las mismas cifras; cada ejecución registra versiones y sha256 | `metricas.json` (`meta`) |

## Requerimientos organizacionales

| Código | Descripción | Aceptación |
|---|---|---|
| RNO-01 | Entrega reproducible | código, norma, banco, arnés e imagen Docker en el repositorio |
| RNO-02 | Desarrollo incremental | cada incremento (I0–I5) entra con sus pruebas `lit` y gtest |
| RNO-03 | Versionado | cada resultado principal corresponde a un *tag* (`banco-N`, `exp-…`) |
| RNO-04 | Documentación | el libro del proyecto se regenera con cada cambio (`bench/gen_book.py`) |

## Normas y estándares

| Referencia | Para qué | Cómo se verifica |
|---|---|---|
| ISO/IEC 14882:2017 (N4659) | la semántica de invalidación de cada operación | cada regla de `matriz.json` cita su cláusula; gtest `Norma.InvalidarODependerCitaSuClausula` |
| SEI CERT CTR51-CPP | uso de iteradores, referencias y punteros válidos | el alcance del checker es esta regla para los contenedores de la STL |
| Convenciones de LLVM | estilo y avisos del código del plugin | se compila con `-Wall -Wextra -Werror=switch` (`UCSM_WARNINGS`) |
| APA 7 | citas y referencias del informe | revisión |

## Requerimientos externos

| Categoría | Requisito | Aceptación |
|---|---|---|
| Interoperabilidad | la salida es SARIF 2.1 de CSA | el arnés la lee sin adaptadores |
| Ética | ningún resultado se escribe a mano | toda cifra sale de `test/experimento/` o de `test/codigo_real/` |
| Privacidad | el banco no contiene datos personales | el banco es código generado |
| Licencias | los proyectos analizados conservan su licencia; no se redistribuye su código | sólo se guardan avisos y *commits* |
