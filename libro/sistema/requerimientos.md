# Requerimientos y casos de uso del sistema

Los requerimientos completos están en el
[capítulo 4](../diseno/cap4/4-1-funcionales.md) y los casos de uso en la
[sección 5.1](../diseno/cap5/5-1-casos-de-uso.md). Aquí está **dónde se
valida cada uno en el código**, con el fragmento de la regla y el de la
prueba.

| Requisito | Casos de uso | Regla en el código | Prueba |
|---|---|---|---|
| RF-S01 Registrarse, autenticarse y controlar el acceso | CU-S01, CU-S02 | `contextos/identidad` | `identidad.test.ts`, `casos.test.ts`, `api.test.ts` |
| RF-S02 Conectar repositorios | CU-S03 | `contextos/repositorios` | `repositorios.test.ts`, `api.test.ts` |
| RF-S03 Revisar cada pull request | CU-S04, CU-S05 | `contextos/revisiones`, `producto/casos-revisiones.ts` | `casos.test.ts`, `api.test.ts`, `clang.test.ts` |
| RF-S04 Consultar revisiones | CU-S06 | `producto/casos-revisiones.ts` | `api.test.ts` |
| RF-S05 Clasificar hallazgos | CU-S07 | `contextos/revisiones/comandos.ts` | `revisiones.test.ts`, `casos.test.ts` |

## RF-S01: registro sin nada predefinido, ingreso y permisos

No hay usuarios de fábrica. La primera persona que se registra queda como
administradora; las siguientes, pendientes hasta que un administrador las
apruebe:

{{codigo sistema/paquetes/contextos/identidad/src/comandos.ts registrar}}

{{codigo sistema/pruebas/api.test.ts "los siguientes quedan pendientes, sin sesión, hasta que un administrador los aprueba"}}

Una cuenta pasa por tres estados. Un registro rechazado no se borra: queda
`Desactivado`, y el ingreso le dice a cada persona cuál es su caso:

![Estados de una cuenta](../diagramas/sistema-estados-usuario.svg)

{{codigo sistema/paquetes/contextos/identidad/src/usuario.ts exigirActivo}}

{{codigo sistema/pruebas/api.test.ts "rechazar un registro deja la cuenta desactivada y el ingreso lo dice; no se puede volver a Pendiente"}}

El permiso es un **testigo**: `Autorizado<P>` solo se obtiene con
`Autorizado.para`, que comprueba que el usuario está activo y que su rol
tiene el permiso.

{{codigo sistema/paquetes/contextos/identidad/src/autorizado.ts Autorizado}}

Y el ingreso no distingue un correo inexistente de una clave equivocada:

{{codigo sistema/paquetes/contextos/identidad/src/sesion.ts ingresar}}

{{codigo sistema/pruebas/api.test.ts "ingresar pone una cookie httpOnly, SameSite=Strict y Secure, y no devuelve el hash"}}

## RF-S02: conectar un repositorio

{{codigo sistema/paquetes/contextos/repositorios/src/repositorio.ts conectar}}

## RF-S03: un commit se revisa una vez y el veredicto mira solo lo no suprimido

{{codigo sistema/paquetes/contextos/revisiones/src/comandos.ts solicitar}}

{{codigo sistema/paquetes/contextos/revisiones/src/comandos.ts publicar}}

El *webhook* solo se acepta con la firma del secreto del repositorio:

{{codigo sistema/paquetes/adaptadores/cripto/src/index.ts firmaValida}}

La prueba del flujo completo, con GitHub y el analizador como dobles:

{{codigo sistema/paquetes/producto/src/casos.test.ts "con un hallazgo en una línea del diff, comenta en esa línea y bloquea el merge"}}

Y la del analizador con `clang` y el checker de verdad (corre dentro de la
imagen):

{{codigo sistema/paquetes/adaptadores/analizador/src/clang.test.ts "en ejemplos/prueba.cpp da un confirmado en Silent y además un posible en Possibly"}}

## RF-S05: un falso positivo deja de reportarse

{{codigo sistema/paquetes/contextos/revisiones/src/comandos.ts clasificar}}

Clasificar deja registrado quién lo hizo y cuándo; el panel lo muestra como
«Marcado por …». El autor sale del testigo `Autorizado`, así que no se puede
clasificar a nombre de otro:

{{codigo sistema/paquetes/contextos/revisiones/src/revisiones.test.ts "un hallazgo nuevo no tiene autor; clasificarlo registra quién y cuándo"}}

{{codigo sistema/paquetes/producto/src/casos.test.ts "un falso positivo deja de reportarse al reintentar la revisión"}}
