# Arquitectura: las guías de diseño en TypeScript

El motor se diseñó con cuatro guías (`bodega-arquitectura`, `rust-trinity`,
`modelado-funcional` y `donde-va`), escritas para Rust y llevadas a C++.
El servicio usa las mismas, llevadas a TypeScript. Esta tabla dice qué se
tradujo y cómo:

| Guía | En Rust | En el servicio (TypeScript) |
|---|---|---|
| Frontera por *crate* | un *crate* por capa; Cargo no deja importar lo que no está en `Cargo.toml` | un paquete npm (*workspace*) por capa, y una **prueba de aptitud** que lee las importaciones y falla si una capa importa lo que no debe |
| Cargar → decidir → efectos | el caso de uso lee, llama a una función pura y aplica efectos | igual: `casos-*.ts` lee del `Almacen`, llama a `solicitar`, `publicar`… y después guarda y llama a GitHub |
| Testigo de autorización | `Authorized<A>` con constructor privado | `Autorizado<P>`: clase con constructor privado y campo `#permiso`, que la vuelve nominal |
| `TryFrom` en las fronteras | conversión que puede fallar | esquemas `zod` en la entrada HTTP y en cada fila de la base |
| Errores en tres niveles | `enum` de dominio, de aplicación y de infraestructura | `ErrorIdentidad`, `ErrorRepositorios`, `ErrorRevisiones` → `ErrorProducto`; las excepciones quedan para infraestructura rota (`FilaCorrupta`, `ErrorGitHub`) |
| El código HTTP en un solo lugar | `IntoResponse` del adaptador | `adaptadores/http/src/errores.ts`, con un `switch` exhaustivo |
| Sin repositorio genérico | un puerto por necesidad | `Usuarios`, `Sesiones`, `Repositorios`, `Revisiones`, `Hallazgos`, `Descartes`, `Trabajos` |
| Unidad de trabajo y *outbox* | transacción + tabla de trabajos | `almacen.transaccion(...)`; la revisión y su trabajo se escriben juntos |
| Tipos que impiden errores | *newtypes*, `enum`, *type-state* | [Tipos que impiden errores](tipos.md) |

![Paquetes del servicio](../diagramas/sistema-paquetes.svg)

## La frontera, comprobada

{{codigo sistema/pruebas/arquitectura.test.ts 17-34}}

Si un contexto importa `fastify`, la prueba falla con el archivo y la
importación culpables.

## Cargar → decidir → efectos

El caso de uso de clasificar, entero: carga el hallazgo, decide con
`clasificar` (pura) y aplica los efectos en una transacción.

{{codigo sistema/paquetes/producto/src/casos-revisiones.ts clasificar}}

## Un solo lugar para los códigos HTTP

{{codigo sistema/paquetes/adaptadores/http/src/errores.ts respuestaDe}}

El `default` llama a `inalcanzable(e)`, que recibe `never`: si se agrega un
error al dominio y no se le da un código aquí, el proyecto no compila.

## La raíz de composición

`app/src/componer.ts` es el único archivo que conoce todos los adaptadores.
Las pruebas pasan sus propios dobles con el segundo argumento.

{{codigo sistema/paquetes/app/src/componer.ts componer}}
