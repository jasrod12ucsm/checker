// Garantías de tipos: las transiciones solo aceptan el estado de origen correcto.
import { it } from "vitest";
import { desenvolver, instante, type HallazgoId, type Positivo, type RepositorioId, type RevisionId, type UsuarioId } from "@centinela/kernel";
import type { NombreRepo, Repositorio, SecretoWebhook } from "@centinela/repositorios";
import { esPendiente, fallar, iniciar, publicar, solicitar, type Revision } from "./index";

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
