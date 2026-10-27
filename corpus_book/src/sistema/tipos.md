# Tipos que impiden errores

> `rust-trinity` en TypeScript. TypeScript compara tipos por su forma, no
> por su nombre: dos `string` son intercambiables aunque uno sea un correo y
> otro un identificador. Estas cuatro técnicas devuelven las garantías que
> Rust da por defecto.

## 1. Marcas: un correo no es un `string` cualquiera

[`sistema/paquetes/kernel/src/marca.ts:7`](https://github.com/jasrod12ucsm/checker/blob/main/sistema/paquetes/kernel/src/marca.ts#L7-L7)

```typescript
export type Marca<T, M extends string> = T & { readonly [marca]: M };
```

Un `Email` solo sale de la función que lo valida; `"x" as Email` fuera de
ella se nota en una revisión de código. Lo mismo `UsuarioId`,
`RepositorioId`, `NombreRepo`, `Huella` y `HashClave`.

[`sistema/paquetes/kernel/src/valores.ts:25`](https://github.com/jasrod12ucsm/checker/blob/main/sistema/paquetes/kernel/src/valores.ts#L25-L28)

```typescript
export function email(s: string): Resultado<Email, ErrorValor> {
  const t = s.trim().toLowerCase();
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(t) && t.length <= 254 ? ok(t as Email) : err(invalido("email", "no es un correo"));
}
```

## 2. `Resultado` en vez de excepciones

[`sistema/paquetes/kernel/src/resultado.ts:1`](https://github.com/jasrod12ucsm/checker/blob/main/sistema/paquetes/kernel/src/resultado.ts#L1-L6)

```typescript
/** Resultado de una operación que puede fallar con un error de dominio, sin excepciones. */
export type Resultado<T, E> =
  | { readonly ok: true; readonly valor: T }
  | { readonly ok: false; readonly error: E };

export const ok = <T>(valor: T): Resultado<T, never> => ({ ok: true, valor });
```

Cada caso de uso devuelve `Resultado<T, ErrorProducto>`. Quien lo llama no
puede usar el valor sin mirar antes `ok`, y el error es un tipo que el
compilador conoce entero.

## 3. El estado en el tipo (*type-state*)

`Revision<E>` lleva su estado como parámetro. Cada transición acepta solo el
estado de origen correcto:

[`sistema/paquetes/contextos/revisiones/src/comandos.ts:33`](https://github.com/jasrod12ucsm/checker/blob/main/sistema/paquetes/contextos/revisiones/src/comandos.ts#L33-L35)

```typescript
export function iniciar(r: Revision<Pendiente>, ahora: Instante): Revision<EnAnalisis> {
  return { ...r, estado: { tipo: "EnAnalisis", iniciadaEn: ahora } };
}
```

[`sistema/paquetes/contextos/revisiones/src/comandos.ts:74`](https://github.com/jasrod12ucsm/checker/blob/main/sistema/paquetes/contextos/revisiones/src/comandos.ts#L74-L76)

```typescript
export function fallar(r: Revision<EnAnalisis>, motivo: string, ahora: Instante): Revision<Fallida> {
  return { ...r, estado: { tipo: "Fallida", terminadaEn: ahora, motivo } };
}
```

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

[`sistema/paquetes/contextos/revisiones/src/garantias.test.ts:7`](https://github.com/jasrod12ucsm/checker/blob/main/sistema/paquetes/contextos/revisiones/src/garantias.test.ts#L7-L22)

```typescript
it("las transiciones dependen del estado", () => {
  const repo: Repositorio = { id: "00000000-0000-4000-8000-0000000000a1" as RepositorioId, nombre: "a/b" as NombreRepo, politica: "Silent", bloquearMerge: false, secretoWebhook: "s" as SecretoWebhook, activo: true, conectadoPor: "u" as UsuarioId, conectadoEn: instante(0) };
  const p = desenvolver(solicitar(repo, undefined, { id: "r" as RevisionId, pr: { numero: 1 as Positivo, titulo: "", autor: "", shaCabeza: "s" }, origen: "manual", solicitadaPor: null }, instante(0)));
  const id = () => "h" as HallazgoId;
  // @ts-expect-error una revisión pendiente no se publica sin pasar por el análisis
  publicar(p, { analizados: 0, noCompilados: [], avisos: [] }, new Set(), id, instante(1));
  // @ts-expect-error ni se marca como fallida
  fallar(p, "x", instante(1));
  const a = iniciar(p, instante(1));
  // @ts-expect-error una revisión en análisis no se vuelve a iniciar
  iniciar(a, instante(2));
  const cualquiera: Revision = a;
  // @ts-expect-error sin comprobar el estado no se puede iniciar
  iniciar(cualquiera, instante(2));
  if (esPendiente(cualquiera)) iniciar(cualquiera, instante(2));
});
```

[`sistema/paquetes/contextos/identidad/src/garantias.test.ts:6`](https://github.com/jasrod12ucsm/checker/blob/main/sistema/paquetes/contextos/identidad/src/garantias.test.ts#L6-L17)

```typescript
it("solo Autorizado.para da un testigo de autorización", () => {
  const admin: Usuario = { id: "00000000-0000-4000-8000-000000000001" as UsuarioId, email: "a@b.co" as Email, nombre: "A" as Texto, rol: "administrador", hashClave: "h" as HashClave, estado: "Activo", creadoEn: instante(0) };
  // @ts-expect-error el constructor es privado
  new Autorizado(admin.id, "gestionar-usuarios");
  // @ts-expect-error un objeto con la misma forma no es un testigo
  const falso: Autorizado<"gestionar-usuarios"> = { usuarioId: admin.id, permiso: "gestionar-usuarios" };
  const consultar = desenvolver(Autorizado.para(admin, "consultar-revisiones"));
  const datos = { id: admin.id, email: admin.email, nombre: admin.nombre, rol: "desarrollador" as const, hashClave: admin.hashClave };
  // @ts-expect-error el permiso de consultar no sirve para crear usuarios
  crearUsuario(consultar, false, datos, instante(0));
  void falso;
});
```

El estado de una cuenta usa la misma idea: el cambio que pide un
administrador es de tipo `Decision` (`Activo` o `Desactivado`), así que
devolver una cuenta a `Pendiente` no compila; solo el registro la deja así.

[`sistema/paquetes/contextos/identidad/src/garantias.test.ts:19`](https://github.com/jasrod12ucsm/checker/blob/main/sistema/paquetes/contextos/identidad/src/garantias.test.ts#L19-L24)

```typescript
it("ningún administrador puede devolver una cuenta a Pendiente", () => {
  const admin: Usuario = { id: "00000000-0000-4000-8000-000000000001" as UsuarioId, email: "a@b.co" as Email, nombre: "A" as Texto, rol: "administrador", hashClave: "h" as HashClave, estado: "Activo", creadoEn: instante(0) };
  const por = desenvolver(Autorizado.para(admin, "gestionar-usuarios"));
  // @ts-expect-error Pendiente no es una decisión: solo lo asigna el registro
  actualizarUsuario(por, admin, { estado: "Pendiente" });
});
```

## 6. Exhaustividad con `never`

Un `switch` sobre una unión termina en `inalcanzable(x)`, que recibe
`never`. Si a la unión se le agrega una variante y el `switch` no la trata,
`x` deja de ser `never` y el proyecto no compila:

[`sistema/paquetes/contextos/revisiones/src/informe.ts:14`](https://github.com/jasrod12ucsm/checker/blob/main/sistema/paquetes/contextos/revisiones/src/informe.ts#L14-L34)

```typescript
export function estadoCommit(repo: Repositorio, r: Revision): EstadoCommit {
  const e = r.estado;
  switch (e.tipo) {
    case "Pendiente":
      return { estado: "pending", descripcion: "En cola" };
    case "EnAnalisis":
      return { estado: "pending", descripcion: "Analizando" };
    case "Fallida":
      return { estado: "error", descripcion: `El análisis falló: ${e.motivo}`.slice(0, 140) };
    case "Publicada": {
      const n = e.resumen.confirmados + e.resumen.posibles;
      if (e.veredicto === "Aprobada") return { estado: "success", descripcion: "Sin usos de handles invalidados" };
      const texto = `${e.resumen.confirmados} confirmados, ${e.resumen.posibles} posibles`;
      return repo.bloquearMerge
        ? { estado: "failure", descripcion: texto }
        : { estado: "success", descripcion: `${texto} (${n === 1 ? "no bloquea" : "no bloquean"} el merge)` };
    }
    default:
      return inalcanzable(e);
  }
}
```
