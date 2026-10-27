// El flujo completo de una revisión con el almacén SQLite real (los casos de uso ya se prueban con el de memoria).
import { expect, it } from "vitest";
import { desenvolver, type Positivo, type RevisionId } from "@centinela/kernel";
import { producto } from "@centinela/producto";
import { abrirAlmacen } from "@centinela/sqlite";
import { dependencias, firmaFalsa } from "./dobles";

it("webhook → análisis → clasificar → reintentar, sobre SQLite", async () => {
  const t = dependencias(abrirAlmacen(":memory:"));
  const p = producto(t.deps);
  const admin = desenvolver(await p.identidad.registrar({ email: "admin@ucsm.edu.pe", nombre: "Admin", clave: "clave12345678" }));
  desenvolver(await p.repositorios.conectar(admin, { nombre: "ucsm/demo", politica: "Possibly", bloquearMerge: true }));
  t.github.archivos = [{ ruta: "src/a.cpp", eliminado: false, lineas: new Set([11]) }];
  t.analizador.avisos = [{ archivo: "src/a.cpp", linea: 11 as Positivo, columna: 3 as Positivo, clase: "Confirmado", mensaje: "m", ruta: [{ archivo: "src/a.cpp", linea: 9 as Positivo, mensaje: "n" }] }];
  const cuerpo = "{}";
  const w = desenvolver(await p.revisiones.recibirWebhook({ evento: "pull_request", repositorio: "ucsm/demo", cuerpo, firma: firmaFalsa(cuerpo), pullRequest: { accion: "opened", numero: 7, titulo: "T", autor: "a", shaCabeza: "abc" } }));
  const id = (w as { revisionId: RevisionId }).revisionId;
  expect(await p.revisiones.procesarSiguiente()).toBe(true);
  const det = desenvolver(await p.revisiones.detalle(admin, id));
  expect(det.revision.estado).toMatchObject({ tipo: "Publicada", veredicto: "ConProblemas" });
  expect(det.hallazgos[0]?.ruta).toHaveLength(1);
  desenvolver(await p.revisiones.clasificar(admin, det.hallazgos[0]!.id, "FalsoPositivo"));
  desenvolver(await p.revisiones.reintentar(admin, id));
  await p.revisiones.procesarSiguiente();
  expect(desenvolver(await p.revisiones.detalle(admin, id)).revision.estado).toMatchObject({ veredicto: "Aprobada", resumen: { suprimidos: 1 } });
});
