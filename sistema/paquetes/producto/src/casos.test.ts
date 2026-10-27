import { beforeEach, describe, expect, it } from "vitest";
import { desenvolver, type Positivo, type RepositorioId, type RevisionId } from "@centinela/kernel";
import type { Usuario } from "@centinela/identidad";
import type { Aviso } from "@centinela/revisiones";
import { dependencias, firmaFalsa } from "../../../pruebas/dobles";
import { producto, type Producto, type Webhook } from "./index";

let p: Producto;
let t: ReturnType<typeof dependencias>;
let admin: Usuario;
let dev: Usuario;

const CLAVE = "clave12345678";
beforeEach(async () => {
  t = dependencias();
  p = producto(t.deps);
  admin = desenvolver(await p.identidad.registrar({ email: "admin@ucsm.edu.pe", nombre: "Admin", clave: CLAVE }));
  dev = desenvolver(await p.identidad.crearUsuario(admin, { email: "dev@ucsm.edu.pe", nombre: "Dev", clave: CLAVE, rol: "desarrollador" }));
});

describe("RF-S01 autenticación", () => {
  it("inicia sesión con la clave correcta y la sesión identifica al usuario", async () => {
    const s = desenvolver(await p.identidad.iniciarSesion("DEV@ucsm.edu.pe", CLAVE));
    expect(desenvolver(await p.identidad.sesionActual(s.token)).id).toBe(dev.id);
  });
  it("rechaza la clave incorrecta y el correo inexistente con el mismo error", async () => {
    expect(await p.identidad.iniciarSesion("dev@ucsm.edu.pe", "otra1234567")).toEqual({ ok: false, error: { tipo: "CredencialesInvalidas" } });
    expect(await p.identidad.iniciarSesion("nadie@ucsm.edu.pe", CLAVE)).toEqual({ ok: false, error: { tipo: "CredencialesInvalidas" } });
  });
  it("cerrar sesión invalida el token", async () => {
    const s = desenvolver(await p.identidad.iniciarSesion("dev@ucsm.edu.pe", CLAVE));
    await p.identidad.cerrarSesion(s.token);
    expect((await p.identidad.sesionActual(s.token)).ok).toBe(false);
  });
  it("la sesión vence a las 8 horas", async () => {
    const s = desenvolver(await p.identidad.iniciarSesion("dev@ucsm.edu.pe", CLAVE));
    t.reloj.avanzar(8 * 3600 * 1000);
    expect(await p.identidad.sesionActual(s.token)).toEqual({ ok: false, error: { tipo: "SesionInvalida" } });
  });
  it("desactivar a un usuario cierra sus sesiones y le impide entrar", async () => {
    const s = desenvolver(await p.identidad.iniciarSesion("dev@ucsm.edu.pe", CLAVE));
    desenvolver(await p.identidad.actualizarUsuario(admin, dev.id, { estado: "Desactivado" }));
    expect((await p.identidad.sesionActual(s.token)).ok).toBe(false);
    expect(await p.identidad.iniciarSesion("dev@ucsm.edu.pe", CLAVE)).toEqual({ ok: false, error: { tipo: "UsuarioDesactivado" } });
  });
  it("solo el administrador gestiona usuarios", async () => {
    expect(await p.identidad.crearUsuario(dev, { email: "x@ucsm.edu.pe", nombre: "X", clave: CLAVE, rol: "administrador" })).toEqual({ ok: false, error: { tipo: "SinPermiso", permiso: "gestionar-usuarios" } });
    expect(await p.identidad.crearUsuario(admin, { email: "dev@ucsm.edu.pe", nombre: "X", clave: CLAVE, rol: "desarrollador" })).toEqual({ ok: false, error: { tipo: "EmailEnUso" } });
  });
  it("nada viene predefinido: el primero que se registra es el administrador", async () => {
    expect(admin).toMatchObject({ rol: "administrador", estado: "Activo" });
    expect(desenvolver(await p.identidad.estadoRegistro())).toEqual({ hayUsuarios: true });
  });
  it("quien se registra después espera la aprobación de un administrador", async () => {
    const nuevo = desenvolver(await p.identidad.registrar({ email: "nueva@ucsm.edu.pe", nombre: "Nueva", clave: CLAVE }));
    expect(nuevo).toMatchObject({ rol: "desarrollador", estado: "Pendiente" });
    expect(await p.identidad.iniciarSesion("nueva@ucsm.edu.pe", CLAVE)).toEqual({ ok: false, error: { tipo: "UsuarioPendiente" } });
    desenvolver(await p.identidad.actualizarUsuario(admin, nuevo.id, { estado: "Activo" }));
    expect((await p.identidad.iniciarSesion("nueva@ucsm.edu.pe", CLAVE)).ok).toBe(true);
  });
  it("el registro valida correo, clave y correo en uso", async () => {
    expect(await p.identidad.registrar({ email: "dev@ucsm.edu.pe", nombre: "X", clave: CLAVE })).toEqual({ ok: false, error: { tipo: "EmailEnUso" } });
    expect((await p.identidad.registrar({ email: "x@ucsm.edu.pe", nombre: "X", clave: "corta" })).ok).toBe(false);
  });
  it("el administrador rechaza un registro: la cuenta queda desactivada y no entra", async () => {
    const nuevo = desenvolver(await p.identidad.registrar({ email: "rechazada@ucsm.edu.pe", nombre: "R", clave: CLAVE }));
    expect(desenvolver(await p.identidad.actualizarUsuario(admin, nuevo.id, { estado: "Desactivado" })).estado).toBe("Desactivado");
    expect(await p.identidad.iniciarSesion("rechazada@ucsm.edu.pe", CLAVE)).toEqual({ ok: false, error: { tipo: "UsuarioDesactivado" } });
  });
  it("un desarrollador no aprueba a nadie", async () => {
    expect(await p.identidad.actualizarUsuario(dev, admin.id, { estado: "Desactivado" })).toMatchObject({ ok: false, error: { tipo: "SinPermiso" } });
  });
});

describe("RF-S02 repositorios", () => {
  it("el administrador conecta un repositorio; el desarrollador no", async () => {
    expect(await p.repositorios.conectar(dev, { nombre: "ucsm/demo", politica: "Silent", bloquearMerge: true })).toMatchObject({ ok: false, error: { tipo: "SinPermiso" } });
    const r = desenvolver(await p.repositorios.conectar(admin, { nombre: "ucsm/demo", politica: "Silent", bloquearMerge: true }));
    expect(r).toMatchObject({ nombre: "ucsm/demo", activo: true, secretoWebhook: "secreto" });
    expect(desenvolver(await p.repositorios.listar(dev))).toHaveLength(1);
  });
  it("configurar cambia la política", async () => {
    const r = desenvolver(await p.repositorios.conectar(admin, { nombre: "ucsm/demo", politica: "Silent", bloquearMerge: true }));
    expect(desenvolver(await p.repositorios.configurar(admin, r.id, { politica: "Possibly" })).politica).toBe("Possibly");
    expect((await p.repositorios.configurar(admin, "00000000-0000-4000-8000-ffffffffffff" as RepositorioId, {})).ok).toBe(false);
  });
});

describe("RF-S03 revisión automática", () => {
  const cuerpo = JSON.stringify({ x: 1 });
  const webhook = (accion = "opened", sha = "abc", extra: Partial<Webhook> = {}): Webhook => ({
    evento: "pull_request",
    repositorio: "ucsm/demo",
    cuerpo,
    firma: firmaFalsa(cuerpo),
    pullRequest: { accion, numero: 7, titulo: "Caché", autor: "ana", shaCabeza: sha },
    ...extra,
  });
  const aviso = (archivo: string, linea: number, clase: Aviso["clase"] = "Confirmado"): Aviso => ({
    archivo,
    linea: linea as Positivo,
    columna: 5 as Positivo,
    clase,
    mensaje: "Uso de una referencia invalidada: 'std::vector::clear' (línea 6) lo invalidó",
    ruta: [],
  });
  let repoId: RepositorioId;
  beforeEach(async () => {
    repoId = desenvolver(await p.repositorios.conectar(admin, { nombre: "ucsm/demo", politica: "Possibly", bloquearMerge: true })).id;
    t.github.archivos = [
      { ruta: "src/a.cpp", eliminado: false, lineas: new Set([10, 11, 12]) },
      { ruta: "README.md", eliminado: false, lineas: new Set([1]) },
    ];
  });

  it("un webhook de otro repositorio o con firma inválida se rechaza", async () => {
    expect(await p.revisiones.recibirWebhook(webhook("opened", "abc", { repositorio: "otro/repo" }))).toEqual({ ok: false, error: { tipo: "RepositorioNoEncontrado" } });
    expect(await p.revisiones.recibirWebhook(webhook("opened", "abc", { firma: "mala" }))).toEqual({ ok: false, error: { tipo: "FirmaInvalida" } });
  });
  it("ping y acciones que no cambian el código se ignoran", async () => {
    expect(await p.revisiones.recibirWebhook({ ...webhook(), evento: "ping" })).toMatchObject({ ok: true, valor: { tipo: "Ignorado" } });
    expect(await p.revisiones.recibirWebhook(webhook("closed"))).toMatchObject({ ok: true, valor: { tipo: "Ignorado", motivo: "acción closed" } });
  });
  it("abrir un PR encola la revisión y pone el commit en pending; el mismo sha no se encola dos veces", async () => {
    expect(await p.revisiones.recibirWebhook(webhook())).toMatchObject({ ok: true, valor: { tipo: "Encolada" } });
    expect(t.github.estados.at(-1)?.estado.estado).toBe("pending");
    expect(await p.revisiones.recibirWebhook(webhook("synchronize"))).toMatchObject({ ok: true, valor: { tipo: "Ignorado", motivo: "RevisionEnCurso" } });
  });
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
  it("un hallazgo fuera del diff va en el cuerpo de la revisión", async () => {
    t.analizador.avisos = [aviso("src/a.cpp", 40, "Posible")];
    await p.revisiones.recibirWebhook(webhook());
    await p.revisiones.procesarSiguiente();
    expect(t.github.revisiones[0]?.comentarios).toEqual([]);
    expect(t.github.revisiones[0]?.cuerpo).toContain("`src/a.cpp:40` (posible)");
  });
  it("sin archivos C++ cambiados no analiza, no comenta y aprueba", async () => {
    t.github.archivos = [{ ruta: "README.md", eliminado: false, lineas: new Set([1]) }];
    await p.revisiones.recibirWebhook(webhook());
    await p.revisiones.procesarSiguiente();
    expect(t.analizador.llamadas).toEqual([]);
    expect(t.github.revisiones).toEqual([]);
    expect(t.github.estados.at(-1)?.estado.estado).toBe("success");
  });
  it("si el análisis falla, la revisión queda Fallida, el commit en error y la fuente se libera", async () => {
    t.analizador.error = new Error("clang murió");
    const w = desenvolver(await p.revisiones.recibirWebhook(webhook()));
    await p.revisiones.procesarSiguiente();
    const id = (w as { revisionId: RevisionId }).revisionId;
    expect(desenvolver(await p.revisiones.detalle(dev, id)).revision.estado).toMatchObject({ tipo: "Fallida", motivo: "clang murió" });
    expect(t.github.estados.at(-1)?.estado.estado).toBe("error");
    expect(t.liberados).toEqual(["abc"]);
  });
  it("si GitHub rechaza la publicación, la revisión queda Fallida", async () => {
    t.analizador.avisos = [aviso("src/a.cpp", 11)];
    t.github.fallarPublicacion = true;
    await p.revisiones.recibirWebhook(webhook());
    await p.revisiones.procesarSiguiente();
    expect(desenvolver(await p.revisiones.listar(dev))[0]?.estado.tipo).toBe("Fallida");
  });
  it("revisar ahora pide el PR a GitHub; si no existe, lo dice", async () => {
    expect(await p.revisiones.solicitarRevision(dev, repoId, 9)).toMatchObject({ ok: false, error: { tipo: "ErrorGitHub" } });
    t.github.prs.set(9, { numero: 9 as Positivo, titulo: "T", autor: "b", shaCabeza: "def" });
    expect(await p.revisiones.solicitarRevision(dev, repoId, 9)).toMatchObject({ ok: true, valor: { origen: "manual", solicitadaPor: dev.id } });
  });
  it("un trabajo interrumpido se marca fallido al arrancar", async () => {
    await p.revisiones.recibirWebhook(webhook());
    const r = desenvolver(await p.revisiones.listar(dev))[0]!;
    t.deps.almacen.revisiones.guardar({ ...r, estado: { tipo: "EnAnalisis", iniciadaEn: t.reloj.ahora() } });
    expect(p.revisiones.recuperarInterrumpidas()).toBe(1);
    expect(desenvolver(await p.revisiones.listar(dev))[0]?.estado.tipo).toBe("Fallida");
  });

  describe("RF-S04 y RF-S05: consultar y clasificar", () => {
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
    it("no se reintenta una revisión en curso ni se clasifica un hallazgo que no existe", async () => {
      const id = (desenvolver(await p.revisiones.recibirWebhook(webhook())) as { revisionId: RevisionId }).revisionId;
      expect(await p.revisiones.reintentar(dev, id)).toEqual({ ok: false, error: { tipo: "RevisionEnCurso" } });
      expect(await p.revisiones.clasificar(dev, "00000000-0000-4000-8000-ffffffffffff" as never, "Confirmado")).toEqual({ ok: false, error: { tipo: "HallazgoNoEncontrado" } });
    });
    it("un usuario desactivado no consulta", async () => {
      const inactivo = { ...dev, estado: "Desactivado" as const };
      expect(await p.revisiones.listar(inactivo)).toEqual({ ok: false, error: { tipo: "UsuarioDesactivado" } });
    });
  });
});
