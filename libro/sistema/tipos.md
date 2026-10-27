# Tipos que impiden errores

> `rust-trinity` en TypeScript. TypeScript compara tipos por su forma, no
> por su nombre: dos `string` son intercambiables aunque uno sea un correo y
> otro un identificador. Estas cuatro técnicas devuelven las garantías que
> Rust da por defecto.

## 1. Marcas: un correo no es un `string` cualquiera

{{codigo sistema/paquetes/kernel/src/marca.ts Marca}}

Un `Email` solo sale de la función que lo valida; `"x" as Email` fuera de
ella se nota en una revisión de código. Lo mismo `UsuarioId`,
`RepositorioId`, `NombreRepo`, `Huella` y `HashClave`.

{{codigo sistema/paquetes/kernel/src/valores.ts email}}

## 2. `Resultado` en vez de excepciones

{{codigo sistema/paquetes/kernel/src/resultado.ts 1-6}}

Cada caso de uso devuelve `Resultado<T, ErrorProducto>`. Quien lo llama no
puede usar el valor sin mirar antes `ok`, y el error es un tipo que el
compilador conoce entero.

## 3. El estado en el tipo (*type-state*)

`Revision<E>` lleva su estado como parámetro. Cada transición acepta solo el
estado de origen correcto:

{{codigo sistema/paquetes/contextos/revisiones/src/comandos.ts iniciar}}

{{codigo sistema/paquetes/contextos/revisiones/src/comandos.ts fallar}}

Para pasar de una `Revision` cualquiera a una `Revision<Pendiente>` hay que
preguntar con `esPendiente`, que estrecha el tipo.

## 4. Testigos de autorización

`Autorizado<P>` (ver [Requerimientos](requerimientos.md)) tiene constructor
privado y un campo privado `#permiso`. Por el campo privado, un objeto con la
misma forma **no** es un `Autorizado`. `crearUsuario` exige
`Autorizado<"gestionar-usuarios">`: no se puede llamar con otro permiso ni
sin haber comprobado el rol.

## 5. Garantías que no deben compilar

El equivalente de las pruebas `compile_fail` de Rust: cada línea marcada con
`// @ts-expect-error` **tiene** que ser un error de tipos. Si alguien afloja
un tipo y la línea empieza a compilar, `npm run tipos` falla con *Unused
'@ts-expect-error' directive*.

{{codigo sistema/paquetes/contextos/revisiones/src/garantias.test.ts "las transiciones dependen del estado"}}

{{codigo sistema/paquetes/contextos/identidad/src/garantias.test.ts "solo Autorizado.para da un testigo de autorización"}}

El estado de una cuenta usa la misma idea: el cambio que pide un
administrador es de tipo `Decision` (`Activo` o `Desactivado`), así que
devolver una cuenta a `Pendiente` no compila; solo el registro la deja así.

{{codigo sistema/paquetes/contextos/identidad/src/garantias.test.ts "ningún administrador puede devolver una cuenta a Pendiente"}}

## 6. Exhaustividad con `never`

Un `switch` sobre una unión termina en `inalcanzable(x)`, que recibe
`never`. Si a la unión se le agrega una variante y el `switch` no la trata,
`x` deja de ser `never` y el proyecto no compila:

{{codigo sistema/paquetes/contextos/revisiones/src/informe.ts estadoCommit}}
