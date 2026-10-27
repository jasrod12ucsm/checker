# Glosario

Tabla: Términos del proyecto

| Término | Definición en este proyecto |
|---|---|
| Arnés | Programa que ejecuta el banco en cada condición, registra y compara los resultados. |
| Banco | Conjunto de 750 casos con respuesta esperada justificada por la norma. |
| Callback | Función del checker que atiende un evento del motor de CSA. |
| Checker | Verificador que detecta una clase de problemas dentro de CSA. |
| Commit | Versión del código identificada por un sha; Centinela revisa el último commit de cada *pull request*. |
| CSA | Clang Static Analyzer. |
| EDT | Estructura de desglose del trabajo: entregables y actividades. |
| EMV | Valor monetario esperado: probabilidad de un riesgo por su impacto económico. |
| ExplodedGraph | Grafo del análisis de CSA que relaciona posiciones y estados. |
| F1 | Media armónica de precisión y exhaustividad. |
| FN y VN | Uso inválido sin aviso y sitio válido sin aviso. |
| Handle | Iterador, referencia o puntero a un elemento de un contenedor. |
| Hallazgo | Aviso del checker guardado por Centinela: archivo, línea, clase, mensaje, ruta y clasificación. |
| HMAC | Código de autenticación de mensajes con clave; GitHub firma cada *webhook* con HMAC-SHA256. |
| Invalidación | Pérdida de validez de un handle según las garantías de una operación de la norma. |
| Línea base | Configuración de referencia de CSA, medida en el experimento. |
| MemRegion | Representación de una región de memoria en CSA. |
| Merge | Fusión de un *pull request* con la rama principal; Centinela puede bloquearla. |
| *Mockup* | Diseño de alta fidelidad de una pantalla, previo a su programación. |
| *Multi-tenant* / *single-tenant* | Una instancia que atiende a varias organizaciones / una instancia por organización. |
| POLICY | Etiqueta de un caso cuyo resultado depende de una condición, como la capacidad. |
| Posible | Aviso de un handle que puede estar invalidado según el camino; se publica con la política `Possibly`. |
| ProgramState | Estado asociado a un camino del análisis de CSA. |
| *Pull request* | Propuesta de cambio en GitHub que se revisa antes del *merge*. |
| Revisión | Análisis de un commit de un *pull request* por Centinela, con su estado y su veredicto. |
| SAFE y UB | Etiquetas de un caso seguro y de un caso con comportamiento indefinido. |
| SARIF | Formato estándar de resultados de análisis estático. |
| VAN y TIR | Valor actual neto y tasa interna de retorno del escenario económico. |
| VP y FP | Aviso correcto y falsa alarma. |
| *Webhook* | Llamada HTTP que GitHub hace a Centinela cuando ocurre un evento. |
