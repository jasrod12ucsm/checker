# 8.5 Estrategia de despliegue

Las pruebas dicen si una versión está lista; la estrategia de despliegue
dice cómo llega a quienes la usan sin interrumpirlos. Estas son las
estrategias que pide la práctica y cuál le corresponde a Centinela hoy.

| Estrategia | Cómo funciona | Ventaja | Riesgo | ¿Para Centinela? |
|---|---|---|---|---|
| *Big bang* | se reemplaza la versión entera de una vez | lo más simple | si falla, falla para todos y hay corte | no: un corte pierde *webhooks* de GitHub mientras el servicio no está |
| *Rolling* (progresivo) | se reemplazan las instancias de a una | sin corte con varias réplicas | conviven dos versiones con la misma base | no hoy: hay **una** instancia con SQLite en un archivo, que no se comparte entre réplicas |
| *Blue-green* | la versión nueva (verde) se levanta junto a la actual (azul) y el tráfico se cambia de golpe; volver atrás es cambiarlo de regreso | vuelta atrás inmediata | dos entornos; la base debe servir a ambos | **sí**, con un *proxy* delante y un respaldo de la base antes del cambio (ver el paso 6) |
| *Canary* | una parte pequeña del tráfico va a la versión nueva y se mide antes de ampliar | detecta fallas con poco daño | requiere enrutar por usuario o por repositorio y medir | a futuro: por repositorio (un repositorio piloto primero) cuando haya varias instancias |

## El procedimiento que se adopta (*blue-green*)

1. El CI de GitHub corre las pruebas de regresión (8.2.6) sobre el *commit*;
   solo una construcción en verde produce la imagen `centinela:<versión>`.
2. Se respalda la base: `sqlite3 /datos/centinela.db ".backup /datos/respaldo.db"`.
3. Se levanta la versión verde en otro puerto sobre el mismo volumen; al
   arrancar, migra el esquema (en una transacción) y marca como fallidas las
   revisiones que quedaron a medias (RNF-S04).
4. Prueba de humo contra la verde: `GET /salud` responde `{"ok":true}`, el
   panel carga, se ingresa y se abre la última revisión. (La seguridad, 41 de
   41, ya la comprobó el CI sobre esa misma imagen en el paso 1.)
5. Se cambia el *proxy* a la verde. Si algún *webhook* llegó justo en el
   cambio y no tuvo respuesta, se reenvía desde GitHub (*Recent Deliveries →
   Redeliver*); como un commit se revisa una sola vez (RN-S02), reenviar uno
   que sí había llegado no duplica la revisión (comprobado en 8.4.6).
6. Si algo falla, el *proxy* vuelve a la azul. La azul, que sigue en marcha,
   funciona con la base migrada mientras la migración sea aditiva (la v3 solo
   agrega un índice). Pero si hay que reiniciarla, no abrirá la base: un binario
   se niega a abrir una base de un esquema más nuevo que el suyo (prueba
   «una base de una versión más nueva que el binario no se abre» de
   `almacen.test.ts`). En ese caso se restaura el respaldo del paso 2 y se
   pierden las revisiones hechas por la verde, que GitHub vuelve a pedir con el
   siguiente *push* o se solicitan con «Revisar un PR ahora».
