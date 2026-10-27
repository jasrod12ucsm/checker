# Modelo funcional del dominio

> Método de `modelado-funcional`, el mismo que se usó para el motor
> ([DSL del motor](../diseno/dsl/index.md)): primero los **eventos** que
> ocurren, después las **órdenes** que los provocan, los **contextos** que
> deciden, los **flujos** escritos como tipos y el **significado** de cada
> pieza con sus **leyes**. El código vino después.

## 1. Eventos del negocio

Lo que el cliente diría que pasó, en pasado:

| Evento | Lo provoca | Contexto |
|---|---|---|
| `UsuarioRegistrado` (administrador si es el primero; si no, pendiente) | CU-S01 | identidad |
| `UsuarioIngresó` | CU-S01 | identidad |
| `UsuarioCreado`, `UsuarioAprobado`, `UsuarioDesactivado`, `RolCambiado` | CU-S02 | identidad |
| `RepositorioConectado`, `PolíticaCambiada`, `RepositorioDesconectado` | CU-S03 | repositorios |
| `PullRequestAbierto` / `Actualizado` | GitHub | (externo) |
| `RevisiónSolicitada` | el *webhook* o «revisar ahora» | revisiones |
| `AnálisisIniciado` | el trabajador | revisiones |
| `RevisiónPublicada` (aprobada o con problemas) | el análisis | revisiones |
| `RevisiónFallida` | `clang`, GitHub o una caída | revisiones |
| `HallazgoClasificado` (`FalsoPositivo` agrega un descarte) | CU-S07 | revisiones |

## 2. Órdenes y quién decide

| Orden | Entrada | Decide | Resultado |
|---|---|---|---|
| `registrar` | cantidad de usuarios, correo en uso, datos | identidad | `Usuario` (administrador activo o desarrollador pendiente) o `EmailEnUso` |
| `actualizarUsuario` | `Autorizado<"gestionar-usuarios">`, usuario, `{estado?: Activo \| Desactivado, rol?}` | identidad | `Usuario` o `NoPuedeModificarseASiMismo` |
| `ingresar` | correo, clave | identidad | `Sesion` o `CredencialesInvalidas` / `UsuarioPendiente` / `UsuarioDesactivado` |
| `crearUsuario` | `Autorizado<"gestionar-usuarios">`, datos | identidad | `Usuario` o `EmailEnUso` |
| `conectar` | `Autorizado<"gestionar-repositorios">`, nombre, política | repositorios | `Repositorio` o `RepositorioYaConectado` |
| `solicitar` | repositorio, revisión existente del sha, PR | revisiones | `Revision<Pendiente>` o `RevisionEnCurso` / `ShaYaRevisado` |
| `iniciar` | `Revision<Pendiente>` | revisiones | `Revision<EnAnalisis>` |
| `publicar` | `Revision<EnAnalisis>`, análisis, huellas descartadas | revisiones | `Revision<Publicada>` + hallazgos |
| `fallar` | `Revision<EnAnalisis>`, motivo | revisiones | `Revision<Fallida>` |
| `reintentar` | `Autorizado<"solicitar-revision">`, revisión terminada | revisiones | `Revision<Pendiente>` o `RevisionEnCurso` |
| `clasificar` | `Autorizado<"clasificar-hallazgos">`, hallazgo, clasificación, instante | revisiones | hallazgo con su autoría (quién y cuándo) + cambio de descarte |

## 3. Contextos

| Contexto | Experto en | Dueño de | No sabe de |
|---|---|---|---|
| **identidad** | quién es quién y qué puede | `Usuario`, `Sesion`, `Rol`, `Permiso`, `Autorizado<P>` | repositorios, GitHub |
| **repositorios** | qué se revisa y cómo | `Repositorio`, `Politica`, `SecretoWebhook` | revisiones, HTTP |
| **revisiones** | el resultado de revisar un commit | `Revision<E>`, `Hallazgo`, `Huella`, veredicto, `EstadoCommit` | cómo se corre `clang`, cómo se guarda |

## 4. Flujos como tipos (DSL)

```text
-- Revisar un pull request (CU-S04)
flujo RevisarPullRequest =
    WebhookFirmado
    → verificar firma con el secreto del Repositorio      -- FirmaInvalida
    → solicitar(Repositorio, RevisionDelSha?, PR)           -- RevisionEnCurso | ShaYaRevisado → Ignorado
    → Revision<Pendiente>  ⟶ guardar + encolar (una transacción)
    ⟶ estado del commit: pending

flujo Analizar =
    Trabajo
    → iniciar : Revision<Pendiente> → Revision<EnAnalisis>
    → archivos C++ cambiados (GitHub) → código del commit (tarball)
    → Analizador : (dir, archivos, Politica) → Analisis { analizados, noCompilados, avisos }
    → publicar : (Revision<EnAnalisis>, Analisis, Set<Huella>) → (Revision<Publicada>, Hallazgo[])
    ⟶ comentarios en las líneas del diff + resumen ; estado del commit
    | si algo falla: fallar : Revision<EnAnalisis> → Revision<Fallida>

-- Clasificar (CU-S07)
flujo Clasificar =
    Autorizado<"clasificar-hallazgos"> × Hallazgo × Clasificacion × Instante
    → clasificar → (Hallazgo con clasificadoPor = {por, en}, CambioDescarte = agregar | quitar | ninguno)
    ⟶ guardar hallazgo ; agregar o quitar la Huella de los descartes del repositorio
```

`→` es una decisión pura del dominio; `⟶`, un efecto que aplica el caso de
uso.

## 5. Significado en una línea

| Pieza | Significa |
|---|---|
| `Revision` | el análisis de **un commit** (el sha de cabeza de un PR) de un repositorio |
| `Hallazgo` | un aviso del checker en ese commit, con su ruta |
| `Huella` | «el mismo problema» entre commits: archivo y mensaje sin números de línea |
| `Descarte` | el equipo dijo que esa huella es un falso positivo en ese repositorio |
| `Veredicto` | `ConProblemas` si queda algún hallazgo sin suprimir; si no, `Aprobada` |
| `EstadoUsuario` | `Pendiente` (se registró y espera aprobación), `Activo` (ingresa) o `Desactivado` (rechazado o dado de baja) |
| `Autoria` | quién clasificó un hallazgo y cuándo; van juntos o no van |
| `Autorizado<P>` | la prueba de que un usuario activo con el permiso `P` pidió la operación |
| `Politica` | qué reporta el checker: `Silent`, solo confirmados; `Possibly`, también posibles |

## 6. Leyes

Cada ley es una prueba con su nombre:

| Ley | Prueba |
|---|---|
| Un sha se revisa una sola vez | `revisiones.test.ts` «un sha no se revisa dos veces» |
| La huella no depende de la línea | «no depende de los números de línea del mensaje» |
| Un descartado no cuenta | «una huella descartada nace como falso positivo y no cuenta para el veredicto» |
| Clasificar dos veces lo mismo no cambia los descartes | «marcar falso positivo agrega la huella…; desmarcar la quita» |
| Reintentar solo desde un estado terminado | «no se reintenta lo que está en curso» |
| Las transiciones respetan el diagrama | `garantias.test.ts`: las equivocadas no compilan |
| Credenciales inválidas no revelan si el correo existe | `identidad.test.ts` |
| Nada viene predefinido: el primero en registrarse administra | `identidad.test.ts`, `casos.test.ts` |
| Nadie se desactiva ni se cambia el rol a sí mismo | `identidad.test.ts` |

## 7. Estados con nombre

No hay `boolean` ni `string` para el estado de una revisión: es una unión
con nombre, y cada variante lleva solo sus datos (el veredicto existe solo en
`Publicada`; el motivo, solo en `Fallida`).

[`sistema/paquetes/contextos/revisiones/src/revision.ts:14`](https://github.com/jasrod12ucsm/checker/blob/main/sistema/paquetes/contextos/revisiones/src/revision.ts#L14-L14)

```typescript
export type EstadoRevision = Pendiente | EnAnalisis | Publicada | Fallida;
```

![Estados de una revisión](../diagramas/sistema-estados-revision.svg)
