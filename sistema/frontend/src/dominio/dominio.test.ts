// Las reglas puras del panel, sin React ni red: cada prueba nombra la regla.
import { describe, expect, it } from "vitest";
import { esCodigo, mensajeDe } from "./errores";
import { diaRelativo, fecha, fechaHora, fechaRelativa, haceCuanto } from "./fechas";
import { nombreRepositorio, numeroPr, reglasClave, validarIngreso, validarNuevoUsuario, validarRegistro } from "./formularios";
import type { DetalleRevision, EstadoRevision, Hallazgo, Revision, Usuario } from "./modelo";
import { nombreRol, puede, seccionesDe } from "./permisos";
import { inalcanzable } from "./resultado";
import {
  agruparPorArchivo,
  commitCorto,
  conHallazgo,
  cuantosFalsos,
  cumpleFiltro,
  enlaceArchivos,
  etiquetaEstado,
  FILTROS_ESTADO,
  hayEnCurso,
  partesMensaje,
  puedeReintentar,
  textoPolitica,
  textoResumen,
  textoVeredicto,
} from "./revisiones";
import { accionPara, iniciales, ordenarUsuarios, pendientes, puedeCambiarRol, reemplazar } from "./usuarios";

const T = "2026-10-26T02:41:00.000Z";
const resumen = { archivosAnalizados: 2, noCompilados: 0, confirmados: 1, posibles: 1, suprimidos: 0 };
const ESTADOS: Record<string, EstadoRevision> = {
  pendiente: { tipo: "Pendiente", desde: T },
  analisis: { tipo: "EnAnalisis", desde: T },
  fallida: { tipo: "Fallida", desde: T, motivo: "clang falló" },
  aprobada: { tipo: "Publicada", desde: T, veredicto: "Aprobada", resumen: { ...resumen, confirmados: 0, posibles: 0 } },
  problemas: { tipo: "Publicada", desde: T, veredicto: "ConProblemas", resumen },
};

const hallazgo = (id: string, archivo: string, linea: number, clasificacion: Hallazgo["clasificacion"] = "SinRevisar"): Hallazgo => ({
  id,
  archivo,
  linea,
  columna: 1,
  clase: "Posible",
  mensaje: "m",
  ruta: [],
  huella: id,
  clasificacion,
  autoria: null,
});

const usuario = (id: string, nombre: string, estado: Usuario["estado"], rol: Usuario["rol"] = "desarrollador"): Usuario => ({ id, email: `${id}@x.pe`, nombre, rol, estado, creadoEn: T });

const revision = (id: string, estado: EstadoRevision, enlace: string | null = "https://github.com/o/r/pull/1"): Revision => ({
  id,
  repositorio: { id: "r", nombre: "o/r" },
  pr: { numero: 1, titulo: "t", autor: "a", shaCabeza: "0123456789abcdef", enlace },
  origen: "webhook",
  solicitadaPor: null,
  creadaEn: T,
  intentos: 1,
  estado,
});

describe("permisos (los mismos que el servicio)", () => {
  it("el administrador puede todo; el desarrollador no gestiona usuarios ni repositorios", () => {
    expect(puede("administrador", "gestionar-usuarios")).toBe(true);
    expect(puede("desarrollador", "gestionar-usuarios")).toBe(false);
    expect(puede("desarrollador", "gestionar-repositorios")).toBe(false);
    expect(puede("desarrollador", "clasificar-hallazgos")).toBe(true);
    expect(puede("desarrollador", "solicitar-revision")).toBe(true);
  });
  it("el menú del desarrollador no tiene «Usuarios»", () => {
    expect(seccionesDe("administrador").map((s) => s.titulo)).toEqual(["Revisiones", "Repositorios", "Usuarios"]);
    expect(seccionesDe("desarrollador").map((s) => s.titulo)).toEqual(["Revisiones", "Repositorios"]);
  });
  it("nombre del rol para la pantalla", () => {
    expect(nombreRol("administrador")).toBe("Administrador");
    expect(nombreRol("desarrollador")).toBe("Desarrollador");
  });
});

describe("formularios: validan todo a la vez, con las reglas del servicio", () => {
  it("la clave necesita 10 caracteres y letras y números", () => {
    expect(reglasClave("")).toEqual({ largo: false, letrasYNumeros: false });
    expect(reglasClave("abcdefghij")).toEqual({ largo: true, letrasYNumeros: false });
    expect(reglasClave("abc1")).toEqual({ largo: false, letrasYNumeros: true });
    expect(reglasClave("abcdefghi1")).toEqual({ largo: true, letrasYNumeros: true });
    expect(reglasClave("a1".repeat(65)).largo).toBe(false);
  });
  it("el registro junta todos los errores y recorta espacios", () => {
    const r = validarRegistro({ email: "x", nombre: "", clave: "abcdefghij", confirmacion: "otra" });
    expect(r).toEqual({ ok: false, error: { email: "Escribe un correo válido.", nombre: "Escribe tu nombre.", clave: "La clave debe tener letras y números.", confirmacion: "Las claves no coinciden." } });
    expect(validarRegistro({ email: " a@b.pe ", nombre: " Ana ", clave: "clave12345", confirmacion: "clave12345" })).toEqual({ ok: true, valor: { email: "a@b.pe", nombre: "Ana", clave: "clave12345" } });
  });
  it("nombre de más de 100 caracteres y correo de más de 254 se rechazan", () => {
    const r = validarNuevoUsuario({ email: `${"a".repeat(250)}@b.pe`, nombre: "n".repeat(101), clave: "clave12345", rol: "desarrollador" });
    expect(r.ok ? {} : r.error).toEqual({ email: "Escribe un correo válido.", nombre: "El nombre puede tener hasta 100 caracteres." });
    expect(validarNuevoUsuario({ email: "a@b.pe", nombre: "A", clave: "clave12345", rol: "administrador" })).toMatchObject({ ok: true, valor: { rol: "administrador" } });
  });
  it("el ingreso solo pide que no estén vacíos (el servicio decide si son correctos)", () => {
    expect(validarIngreso({ email: "", clave: "" })).toEqual({ ok: false, error: { email: "Escribe tu correo.", clave: "Escribe tu clave." } });
    expect(validarIngreso({ email: " a@b.pe ", clave: "x" })).toEqual({ ok: true, valor: { email: "a@b.pe", clave: "x" } });
  });
  it("el repositorio es dueño/nombre; acepta la URL de GitHub", () => {
    expect(nombreRepositorio("lab-sistemas/motor-rutas")).toEqual({ ok: true, valor: "lab-sistemas/motor-rutas" });
    expect(nombreRepositorio(" https://github.com/llvm/llvm-project.git ")).toEqual({ ok: true, valor: "llvm/llvm-project" });
    expect(nombreRepositorio("https://github.com/o/r/")).toEqual({ ok: true, valor: "o/r" });
    for (const malo of ["", "solo", "a/b/c", "-o/r", "o/r p", `${"o".repeat(40)}/r`]) expect(nombreRepositorio(malo).ok, malo).toBe(false);
  });
  it("el número de PR es un entero positivo; acepta «#214»", () => {
    expect(numeroPr("214")).toEqual({ ok: true, valor: 214 });
    expect(numeroPr(" #7 ")).toEqual({ ok: true, valor: 7 });
    for (const malo of ["", "0", "-3", "1.5", "abc"]) expect(numeroPr(malo).ok, malo).toBe(false);
  });
});

describe("revisiones", () => {
  it("cada estado tiene su etiqueta y su tono", () => {
    expect(Object.values(ESTADOS).map(etiquetaEstado)).toEqual([
      { texto: "Pendiente", tono: "info" },
      { texto: "En análisis", tono: "info" },
      { texto: "Fallida", tono: "neutro" },
      { texto: "Publicada · Aprobada", tono: "exito" },
      { texto: "Publicada · Con problemas", tono: "peligro" },
    ]);
  });
  it("el filtro «En curso» junta pendiente y en análisis; aprobada y con problemas son caras de publicada", () => {
    const pasan = (f: (typeof FILTROS_ESTADO)[number]["valor"]) => Object.keys(ESTADOS).filter((k) => cumpleFiltro(ESTADOS[k]!, f));
    expect(pasan("Todos")).toHaveLength(5);
    expect(pasan("EnCurso")).toEqual(["pendiente", "analisis"]);
    expect(pasan("Aprobada")).toEqual(["aprobada"]);
    expect(pasan("ConProblemas")).toEqual(["problemas"]);
    expect(pasan("Fallida")).toEqual(["fallida"]);
  });
  it("la lista se refresca sola solo mientras algo sigue en curso", () => {
    expect(hayEnCurso([revision("a", ESTADOS["aprobada"]!), revision("b", ESTADOS["analisis"]!)])).toBe(true);
    expect(hayEnCurso([revision("a", ESTADOS["aprobada"]!), revision("b", ESTADOS["fallida"]!)])).toBe(false);
    expect(hayEnCurso([])).toBe(false);
  });
  it("reintentar solo desde un estado terminado", () => {
    expect(Object.keys(ESTADOS).filter((k) => puedeReintentar(ESTADOS[k]!))).toEqual(["fallida", "aprobada", "problemas"]);
  });
  it("textos de resumen, política y veredicto", () => {
    expect(textoResumen(resumen)).toBe("1 confirmados · 1 posibles · 0 descartados");
    expect(textoPolitica("Silent")).toBe("Solo confirmados");
    expect(textoPolitica("Possibly")).toBe("También posibles");
    expect(textoVeredicto(ESTADOS["problemas"]!, "Possibly")).toBe("Veredicto: 1 uso confirmado y 1 posible de una referencia invalidada (política Possibly).");
    expect(textoVeredicto({ tipo: "Publicada", desde: T, veredicto: "ConProblemas", resumen: { ...resumen, confirmados: 2, posibles: 0 } }, undefined)).toBe("Veredicto: 2 usos confirmados de una referencia invalidada.");
    expect(textoVeredicto({ tipo: "Publicada", desde: T, veredicto: "ConProblemas", resumen: { ...resumen, confirmados: 0, posibles: 3 } }, "Possibly")).toMatch(/^Veredicto: 3 posibles de/);
    expect(textoVeredicto(ESTADOS["aprobada"]!, "Silent")).toBe("Sin usos de referencias invalidadas en 2 archivos (política Silent).");
    expect(textoVeredicto({ tipo: "Publicada", desde: T, veredicto: "Aprobada", resumen: { ...resumen, archivosAnalizados: 1 } }, undefined)).toBe("Sin usos de referencias invalidadas en 1 archivo.");
    expect(textoVeredicto(ESTADOS["fallida"]!, "Silent")).toBe("No se pudo completar: clang falló");
    expect(textoVeredicto(ESTADOS["pendiente"]!, "Silent")).toMatch(/En cola/);
    expect(textoVeredicto(ESTADOS["analisis"]!, "Silent")).toMatch(/Analizando/);
  });
  it("los hallazgos se agrupan por archivo, en orden de línea; los falsos positivos se ocultan si no se piden", () => {
    const hs = [hallazgo("3", "src/b.cpp", 5), hallazgo("1", "src/a.cpp", 20), hallazgo("2", "src/a.cpp", 7), hallazgo("4", "src/b.cpp", 1, "FalsoPositivo")];
    expect(agruparPorArchivo(hs, false).map((g) => [g.archivo, g.hallazgos.map((h) => h.id)])).toEqual([
      ["src/a.cpp", ["2", "1"]],
      ["src/b.cpp", ["3"]],
    ]);
    expect(agruparPorArchivo(hs, true)[1]!.hallazgos.map((h) => h.id)).toEqual(["4", "3"]);
    expect(agruparPorArchivo([hallazgo("9", "x.cpp", 1, "FalsoPositivo")], false)).toEqual([]);
    expect(cuantosFalsos(hs)).toBe(1);
  });
  it("un hallazgo clasificado reemplaza al anterior sin tocar los demás", () => {
    const d: DetalleRevision = { ...revision("r", ESTADOS["problemas"]!), hallazgos: [hallazgo("1", "a", 1), hallazgo("2", "a", 2)] };
    const nuevo = { ...hallazgo("2", "a", 2), clasificacion: "Confirmado" as const };
    expect(conHallazgo(d, nuevo).hallazgos.map((h) => h.clasificacion)).toEqual(["SinRevisar", "Confirmado"]);
  });
  it("commit corto, enlace a archivos y partes de código del mensaje", () => {
    expect(commitCorto("d3m0000000000001")).toBe("d3m0000");
    expect(enlaceArchivos(revision("r", ESTADOS["aprobada"]!))).toBe("https://github.com/o/r/pull/1/files");
    expect(enlaceArchivos(revision("r", ESTADOS["aprobada"]!, null))).toBeNull();
    expect(partesMensaje("Uso: 'std::vector::clear' (línea 10) por 'f'")).toEqual([
      { codigo: false, texto: "Uso: " },
      { codigo: true, texto: "std::vector::clear" },
      { codigo: false, texto: " (línea 10) por " },
      { codigo: true, texto: "f" },
    ]);
    expect(partesMensaje("sin código")).toEqual([{ codigo: false, texto: "sin código" }]);
  });
});

describe("usuarios", () => {
  const yo = usuario("yo", "Lucía Paredes", "Activo", "administrador");
  const todos = [usuario("p", "Rodrigo", "Pendiente"), usuario("d", "Sofía", "Desactivado"), usuario("b", "Bruno", "Activo"), yo, usuario("a", "Ana", "Activo")];
  it("pendientes de aprobación", () => {
    expect(pendientes(todos).map((u) => u.id)).toEqual(["p"]);
  });
  it("orden: primero tú, luego activos, desactivados y pendientes, por nombre", () => {
    expect(ordenarUsuarios(todos, "yo").map((u) => u.nombre)).toEqual(["Lucía Paredes", "Ana", "Bruno", "Sofía", "Rodrigo"]);
  });
  it("nadie se desactiva ni se cambia el rol a sí mismo; un pendiente se decide arriba", () => {
    expect(accionPara(yo, "yo")).toEqual({ tipo: "Propio" });
    expect(accionPara(todos[0]!, "yo")).toEqual({ tipo: "Decidir" });
    expect(accionPara(todos[1]!, "yo")).toEqual({ tipo: "Cambiar", hacia: "Activo", texto: "Activar" });
    expect(accionPara(todos[2]!, "yo")).toEqual({ tipo: "Cambiar", hacia: "Desactivado", texto: "Desactivar" });
    expect(puedeCambiarRol(yo, "yo")).toBe(false);
    expect(puedeCambiarRol(todos[2]!, "yo")).toBe(true);
  });
  it("iniciales: primera y última palabra", () => {
    expect(iniciales("Lucía Paredes")).toBe("LP");
    expect(iniciales("María del Carmen Ccama")).toBe("MC");
    expect(iniciales("ana")).toBe("A");
    expect(iniciales("  ")).toBe("?");
  });
  it("reemplazar actualiza o agrega", () => {
    const b2 = { ...todos[2]!, rol: "administrador" as const };
    expect(reemplazar(todos, b2).find((u) => u.id === "b")?.rol).toBe("administrador");
    expect(reemplazar(todos, usuario("n", "Nuevo", "Activo"))).toHaveLength(6);
  });
});

describe("fechas (hora de Lima, reloj pasado como argumento)", () => {
  const ahora = Date.parse("2026-10-27T15:00:00.000Z"); // 27 oct, 10:00 en Lima
  it("fecha y fecha con hora", () => {
    expect(fecha("2026-10-24T05:00:00.000Z")).toBe("24 oct 2026");
    expect(fechaHora("2026-10-27T02:41:00.000Z")).toBe("26 oct 2026, 21:41");
  });
  it("hoy, ayer o la fecha, según el día en Lima", () => {
    expect(fechaRelativa("2026-10-27T14:12:00.000Z", ahora)).toBe("hoy, 09:12");
    expect(fechaRelativa("2026-10-27T01:12:00.000Z", ahora)).toBe("ayer, 20:12");
    expect(fechaRelativa("2026-09-02T15:00:00.000Z", ahora)).toBe("2 sep 2026");
    expect(diaRelativo("2026-10-27T14:12:00.000Z", ahora)).toBe("hoy");
    expect(diaRelativo("2026-10-26T14:12:00.000Z", ahora)).toBe("ayer");
    expect(diaRelativo("2026-01-05T14:12:00.000Z", ahora)).toBe("5 ene 2026");
  });
  it("hace cuánto", () => {
    expect(haceCuanto(new Date(ahora - 20_000).toISOString(), ahora)).toBe("hace un momento");
    expect(haceCuanto(new Date(ahora - 120_000).toISOString(), ahora)).toBe("hace 2 min");
    expect(haceCuanto(new Date(ahora - 3 * 3_600_000).toISOString(), ahora)).toBe("hace 3 h");
    expect(haceCuanto("2026-10-01T15:00:00.000Z", ahora)).toBe("1 oct 2026");
    expect(haceCuanto(new Date(ahora + 5000).toISOString(), ahora)).toBe("hace un momento");
  });
});

describe("errores", () => {
  it("el servicio redacta los de negocio; el panel, los del camino", () => {
    expect(mensajeDe({ tipo: "Negocio", estado: 409, codigo: "EmailEnUso", mensaje: "Ya hay un usuario con ese correo." })).toBe("Ya hay un usuario con ese correo.");
    expect(mensajeDe({ tipo: "SinSesion", mensaje: "La sesión venció." })).toBe("La sesión venció.");
    expect(mensajeDe({ tipo: "Red", detalle: "x" })).toMatch(/No se pudo contactar/);
    expect(mensajeDe({ tipo: "RespuestaInvalida", detalle: "x" })).toMatch(/algo inesperado/);
  });
  it("esCodigo solo reconoce errores de negocio", () => {
    expect(esCodigo({ tipo: "Negocio", estado: 409, codigo: "EmailEnUso", mensaje: "" }, "EmailEnUso")).toBe(true);
    expect(esCodigo({ tipo: "Red", detalle: "EmailEnUso" }, "EmailEnUso")).toBe(false);
  });
  it("inalcanzable lanza si un caso imposible llega en ejecución", () => {
    expect(() => inalcanzable("x" as never)).toThrow("caso no contemplado");
  });
});
