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

[`sistema/paquetes/contextos/identidad/src/comandos.ts:19`](https://github.com/jasrod12ucsm/checker/blob/main/sistema/paquetes/contextos/identidad/src/comandos.ts#L19-L28)

```typescript
export function registrar(
  cantidadUsuarios: number,
  emailEnUso: boolean,
  datos: Omit<DatosUsuario, "rol">,
  ahora: Instante,
): Resultado<Usuario, ErrorIdentidad> {
  if (emailEnUso) return err({ tipo: "EmailEnUso" });
  const primero = cantidadUsuarios === 0;
  return ok({ ...datos, rol: primero ? "administrador" : "desarrollador", estado: primero ? "Activo" : "Pendiente", creadoEn: ahora });
}
```

[`sistema/pruebas/api.test.ts:39`](https://github.com/jasrod12ucsm/checker/blob/main/sistema/pruebas/api.test.ts#L39-L50)

```typescript
  it("los siguientes quedan pendientes, sin sesión, hasta que un administrador los aprueba", async () => {
    const r = await app.inject({ method: "POST", url: "/api/registro", payload: { email: "nuevo@ucsm.edu.pe", nombre: "Nuevo", clave: CLAVE } });
    expect(r.json()).toMatchObject({ usuario: { rol: "desarrollador", estado: "Pendiente" }, pendienteDeAprobacion: true });
    expect(r.cookies.find((c) => c.name === COOKIE_SESION)).toBeUndefined();
    const intento = await entrar("nuevo@ucsm.edu.pe");
    expect(intento.r.statusCode).toBe(403);
    expect(intento.r.json().error.mensaje).toBe("Tu cuenta espera la aprobación de un administrador.");
    const { cookie } = await entrar();
    const id = r.json().usuario.id;
    expect((await app.inject({ method: "PATCH", url: `/api/usuarios/${id}`, headers: { cookie }, payload: { estado: "Activo", rol: "administrador" } })).json()).toMatchObject({ estado: "Activo", rol: "administrador" });
    expect((await entrar("nuevo@ucsm.edu.pe")).r.statusCode).toBe(200);
  });
```

Una cuenta pasa por tres estados. Un registro rechazado no se borra: queda
`Desactivado`, y el ingreso le dice a cada persona cuál es su caso:

![Estados de una cuenta](../diagramas/sistema-estados-usuario.svg)

[`sistema/paquetes/contextos/identidad/src/usuario.ts:53`](https://github.com/jasrod12ucsm/checker/blob/main/sistema/paquetes/contextos/identidad/src/usuario.ts#L53-L62)

```typescript
export function exigirActivo(u: Usuario): Resultado<Usuario, ErrorIdentidad> {
  switch (u.estado) {
    case "Activo":
      return ok(u);
    case "Pendiente":
      return err({ tipo: "UsuarioPendiente" });
    case "Desactivado":
      return err({ tipo: "UsuarioDesactivado" });
  }
}
```

[`sistema/pruebas/api.test.ts:51`](https://github.com/jasrod12ucsm/checker/blob/main/sistema/pruebas/api.test.ts#L51-L60)

```typescript
  it("rechazar un registro deja la cuenta desactivada y el ingreso lo dice; no se puede volver a Pendiente", async () => {
    const r = await app.inject({ method: "POST", url: "/api/registro", payload: { email: "rechazo@ucsm.edu.pe", nombre: "Rechazo", clave: CLAVE } });
    const { cookie } = await entrar();
    const url = `/api/usuarios/${r.json().usuario.id}`;
    expect((await app.inject({ method: "PATCH", url, headers: { cookie }, payload: { estado: "Desactivado" } })).json()).toMatchObject({ estado: "Desactivado" });
    const intento = await entrar("rechazo@ucsm.edu.pe");
    expect(intento.r.statusCode).toBe(403);
    expect(intento.r.json().error).toEqual({ codigo: "UsuarioDesactivado", mensaje: "Tu cuenta está desactivada: pide a un administrador que la reactive." });
    expect((await app.inject({ method: "PATCH", url, headers: { cookie }, payload: { estado: "Pendiente" } })).statusCode).toBe(400);
  });
```

El permiso es un **testigo**: `Autorizado<P>` solo se obtiene con
`Autorizado.para`, que comprueba que el usuario está activo y que su rol
tiene el permiso.

[`sistema/paquetes/contextos/identidad/src/autorizado.ts:10`](https://github.com/jasrod12ucsm/checker/blob/main/sistema/paquetes/contextos/identidad/src/autorizado.ts#L10-L29)

```typescript
export class Autorizado<P extends Permiso> {
  readonly #permiso: P;
  private constructor(
    readonly usuarioId: UsuarioId,
    permiso: P,
  ) {
    this.#permiso = permiso;
  }

  get permiso(): P {
    return this.#permiso;
  }

  static para<P extends Permiso>(usuario: Usuario, permiso: P): Resultado<Autorizado<P>, ErrorIdentidad> {
    const activo = exigirActivo(usuario);
    if (!activo.ok) return activo;
    if (!puede(usuario.rol, permiso)) return err({ tipo: "SinPermiso", permiso });
    return ok(new Autorizado(usuario.id, permiso));
  }
}
```

Y el ingreso no distingue un correo inexistente de una clave equivocada:

[`sistema/paquetes/contextos/identidad/src/sesion.ts:18`](https://github.com/jasrod12ucsm/checker/blob/main/sistema/paquetes/contextos/identidad/src/sesion.ts#L18-L28)

```typescript
export function ingresar(
  usuario: Usuario | undefined,
  claveCorrecta: boolean,
  tokenHash: HashToken,
  ahora: Instante,
): Resultado<Sesion, ErrorIdentidad> {
  if (usuario === undefined || !claveCorrecta) return err({ tipo: "CredencialesInvalidas" });
  const activo = exigirActivo(usuario);
  if (!activo.ok) return activo;
  return ok({ tokenHash, usuarioId: usuario.id, creada: ahora, expira: despues(ahora, DURACION_SESION_MS) });
}
```

[`sistema/pruebas/api.test.ts:72`](https://github.com/jasrod12ucsm/checker/blob/main/sistema/pruebas/api.test.ts#L72-L79)

```typescript
  it("ingresar pone una cookie httpOnly, SameSite=Strict y Secure, y no devuelve el hash", async () => {
    const { r } = await entrar();
    expect(r.statusCode).toBe(200);
    const c = r.cookies.find((x) => x.name === COOKIE_SESION)!;
    expect(c).toMatchObject({ httpOnly: true, sameSite: "Strict", secure: true, path: "/" });
    expect(r.json()).toEqual(expect.objectContaining({ email: "admin@ucsm.edu.pe", rol: "administrador" }));
    expect(r.body).not.toContain("scrypt");
  });
```

## RF-S02: conectar un repositorio

[`sistema/paquetes/contextos/repositorios/src/repositorio.ts:50`](https://github.com/jasrod12ucsm/checker/blob/main/sistema/paquetes/contextos/repositorios/src/repositorio.ts#L50-L59)

```typescript
export function conectar(
  por: Autorizado<"gestionar-repositorios">,
  existente: Repositorio | undefined,
  datos: DatosConexion,
  ahora: Instante,
): Resultado<Repositorio, ErrorRepositorios> {
  if (existente?.activo) return err({ tipo: "RepositorioYaConectado" });
  const base = { ...datos, activo: true, conectadoPor: por.usuarioId, conectadoEn: ahora };
  return ok(existente === undefined ? base : { ...base, id: existente.id });
}
```

## RF-S03: un commit se revisa una vez y el veredicto mira solo lo no suprimido

[`sistema/paquetes/contextos/revisiones/src/comandos.ts:19`](https://github.com/jasrod12ucsm/checker/blob/main/sistema/paquetes/contextos/revisiones/src/comandos.ts#L19-L31)

```typescript
export function solicitar(
  repo: Repositorio,
  existenteDelSha: Revision | undefined,
  s: Solicitud,
  ahora: Instante,
): Resultado<Revision<Pendiente>, ErrorRevisiones | { tipo: "RepositorioDesconectado" }> {
  if (!repo.activo) return err({ tipo: "RepositorioDesconectado" });
  if (existenteDelSha !== undefined) {
    const t = existenteDelSha.estado.tipo;
    return err(t === "Pendiente" || t === "EnAnalisis" ? { tipo: "RevisionEnCurso" } : { tipo: "ShaYaRevisado", estado: t });
  }
  return ok({ ...s, repositorioId: repo.id, creadaEn: ahora, intentos: 1, estado: { tipo: "Pendiente", encoladaEn: ahora } });
}
```

[`sistema/paquetes/contextos/revisiones/src/comandos.ts:46`](https://github.com/jasrod12ucsm/checker/blob/main/sistema/paquetes/contextos/revisiones/src/comandos.ts#L46-L72)

```typescript
export function publicar(
  r: Revision<EnAnalisis>,
  analisis: Analisis,
  descartadas: ReadonlySet<Huella>,
  nuevoId: () => HallazgoId,
  ahora: Instante,
): Publicacion {
  const vistos = new Set<string>();
  const hallazgos: Hallazgo[] = [];
  for (const a of analisis.avisos) {
    const clave = `${a.archivo}:${a.linea}:${a.columna}:${a.mensaje}`;
    if (vistos.has(clave)) continue;
    vistos.add(clave);
    const hu = huella(a);
    hallazgos.push({ ...a, id: nuevoId(), revisionId: r.id, huella: hu, clasificacion: descartadas.has(hu) ? "FalsoPositivo" : "SinRevisar", clasificadoPor: null });
  }
  const visibles = hallazgos.filter((h) => !suprimido(h));
  const resumen: Resumen = {
    archivosAnalizados: analisis.analizados,
    noCompilados: analisis.noCompilados.length,
    confirmados: visibles.filter((h) => h.clase === "Confirmado").length,
    posibles: visibles.filter((h) => h.clase === "Posible").length,
    suprimidos: hallazgos.length - visibles.length,
  };
  const veredicto = visibles.length === 0 ? "Aprobada" : "ConProblemas";
  return { revision: { ...r, estado: { tipo: "Publicada", terminadaEn: ahora, veredicto, resumen } }, hallazgos };
}
```

El *webhook* solo se acepta con la firma del secreto del repositorio:

[`sistema/paquetes/adaptadores/cripto/src/index.ts:36`](https://github.com/jasrod12ucsm/checker/blob/main/sistema/paquetes/adaptadores/cripto/src/index.ts#L36-L41)

```typescript
  firmaValida(secreto, cuerpo, firma) {
    if (firma === undefined || !firma.startsWith("sha256=")) return false;
    const esperada = Buffer.from(`sha256=${createHmac("sha256", secreto).update(cuerpo).digest("hex")}`);
    const recibida = Buffer.from(firma);
    return esperada.length === recibida.length && timingSafeEqual(esperada, recibida);
  },
```

La prueba del flujo completo, con GitHub y el analizador como dobles:

[`sistema/paquetes/producto/src/casos.test.ts:129`](https://github.com/jasrod12ucsm/checker/blob/main/sistema/paquetes/producto/src/casos.test.ts#L129-L139)

```typescript
  it("con un hallazgo en una línea del diff, comenta en esa línea y bloquea el merge", async () => {
    t.analizador.avisos = [aviso("src/a.cpp", 11)];
    await p.revisiones.recibirWebhook(webhook());
    expect(await p.revisiones.procesarSiguiente()).toBe(true);
    expect(t.analizador.llamadas[0]).toEqual({ dir: "/tmp/fuente-abc", archivos: ["src/a.cpp"], politica: "Possibly" });
    expect(t.liberados).toEqual(["abc"]);
    const rev = t.github.revisiones[0]!;
    expect(rev.comentarios).toEqual([expect.objectContaining({ ruta: "src/a.cpp", linea: 11 })]);
    expect(t.github.estados.at(-1)?.estado).toEqual({ estado: "failure", descripcion: "1 confirmados, 0 posibles" });
    expect(await p.revisiones.procesarSiguiente()).toBe(false);
  });
```

Y la del analizador con `clang` y el checker de verdad (corre dentro de la
imagen):

[`sistema/paquetes/adaptadores/analizador/src/clang.test.ts:24`](https://github.com/jasrod12ucsm/checker/blob/main/sistema/paquetes/adaptadores/analizador/src/clang.test.ts#L24-L39)

```typescript
  it("en ejemplos/prueba.cpp da un confirmado en Silent y además un posible en Possibly", async () => {
    const dir = mkdtempSync(join(tmpdir(), "centinela-"));
    try {
      cpSync(EJEMPLO, join(dir, "prueba.cpp"));
      writeFileSync(join(dir, "roto.cpp"), "#include \"no-existe.h\"\nint main() {}\n");
      const silent = await analizador.analizar(dir, ["prueba.cpp", "roto.cpp"], "Silent");
      expect(silent.analizados).toBe(1);
      expect(silent.noCompilados).toEqual(["roto.cpp"]);
      expect(silent.avisos.map((a) => [a.linea, a.clase])).toEqual([[7, "Confirmado"]]);
      const possibly = await analizador.analizar(dir, ["prueba.cpp"], "Possibly");
      expect(possibly.avisos.map((a) => a.clase).sort()).toEqual(["Confirmado", "Posible"]);
      expect(possibly.avisos.find((a) => a.clase === "Posible")?.ruta.length).toBeGreaterThan(0);
    } finally {
      rmSync(dir, { recursive: true });
    }
  }, 60_000);
```

## RF-S05: un falso positivo deja de reportarse

[`sistema/paquetes/contextos/revisiones/src/comandos.ts:88`](https://github.com/jasrod12ucsm/checker/blob/main/sistema/paquetes/contextos/revisiones/src/comandos.ts#L88-L97)

```typescript
export function clasificar(
  por: Autorizado<"clasificar-hallazgos">,
  h: Hallazgo,
  nueva: Clasificacion,
  ahora: Instante,
): { readonly hallazgo: Hallazgo; readonly descarte: CambioDescarte } {
  const antes = suprimido(h);
  const despues = nueva === "FalsoPositivo";
  return { hallazgo: { ...h, clasificacion: nueva, clasificadoPor: { por: por.usuarioId, en: ahora } }, descarte: antes === despues ? "ninguno" : despues ? "agregar" : "quitar" };
}
```

Clasificar deja registrado quién lo hizo y cuándo; el panel lo muestra como
«Marcado por …». El autor sale del testigo `Autorizado`, así que no se puede
clasificar a nombre de otro:

[`sistema/paquetes/contextos/revisiones/src/revisiones.test.ts:99`](https://github.com/jasrod12ucsm/checker/blob/main/sistema/paquetes/contextos/revisiones/src/revisiones.test.ts#L99-L102)

```typescript
  it("un hallazgo nuevo no tiene autor; clasificarlo registra quién y cuándo", () => {
    expect(h.clasificadoPor).toBeNull();
    expect(clasificar(por, h, "Confirmado", instante(7)).hallazgo.clasificadoPor).toEqual({ por: dev.id, en: instante(7) });
  });
```

[`sistema/paquetes/producto/src/casos.test.ts:185`](https://github.com/jasrod12ucsm/checker/blob/main/sistema/paquetes/producto/src/casos.test.ts#L185-L200)

```typescript
    it("un falso positivo deja de reportarse al reintentar la revisión", async () => {
      t.analizador.avisos = [aviso("src/a.cpp", 11)];
      const id = (desenvolver(await p.revisiones.recibirWebhook(webhook())) as { revisionId: RevisionId }).revisionId;
      await p.revisiones.procesarSiguiente();
      const det = desenvolver(await p.revisiones.detalle(dev, id));
      expect(det.repositorio.nombre).toBe("ucsm/demo");
      const h = det.hallazgos[0]!;
      expect(desenvolver(await p.revisiones.clasificar(dev, h.id, "FalsoPositivo")).clasificacion).toBe("FalsoPositivo");

      desenvolver(await p.revisiones.reintentar(dev, id));
      await p.revisiones.procesarSiguiente();
      const otra = desenvolver(await p.revisiones.detalle(dev, id));
      expect(otra.revision).toMatchObject({ intentos: 2, estado: { tipo: "Publicada", veredicto: "Aprobada", resumen: { suprimidos: 1 } } });
      expect(t.github.estados.at(-1)?.estado.estado).toBe("success");
      expect(t.github.revisiones).toHaveLength(1);
    });
```
