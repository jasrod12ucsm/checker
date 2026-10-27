import { ok, repositorioId, type RepositorioId } from "@centinela/kernel";
import type { Usuario } from "@centinela/identidad";
import { conectar, configurar, desconectar, nombreRepo, type Ajustes, type Politica, type Repositorio } from "@centinela/repositorios";
import { autorizar, encontrado, type Dependencias, type R } from "./contexto";

export interface NuevaConexion {
  readonly nombre: string;
  readonly politica: Politica;
  readonly bloquearMerge: boolean;
}

export function casosRepositorios(d: Dependencias) {
  const { almacen: a } = d;
  return {
    async listar(actor: Usuario): R<readonly Repositorio[]> {
      const por = autorizar(actor, "consultar-revisiones");
      if (!por.ok) return por;
      return ok(a.repositorios.listar());
    },

    /** Conecta un repositorio y devuelve el secreto para configurar el webhook en GitHub. */
    async conectar(actor: Usuario, n: NuevaConexion): R<Repositorio> {
      const por = autorizar(actor, "gestionar-repositorios");
      if (!por.ok) return por;
      const nombre = nombreRepo(n.nombre);
      if (!nombre.ok) return nombre;
      const id = repositorioId(d.ids.nuevo());
      if (!id.ok) return id;
      return a.transaccion(() => {
        const datos = { id: id.valor, nombre: nombre.valor, politica: n.politica, bloquearMerge: n.bloquearMerge, secretoWebhook: d.secretos.secretoWebhook() };
        const r = conectar(por.valor, a.repositorios.porNombre(nombre.valor), datos, d.reloj.ahora());
        if (r.ok) a.repositorios.guardar(r.valor);
        return r;
      });
    },

    async configurar(actor: Usuario, id: RepositorioId, ajustes: Ajustes): R<Repositorio> {
      const por = autorizar(actor, "gestionar-repositorios");
      if (!por.ok) return por;
      return a.transaccion(() => {
        const repo = encontrado(a.repositorios.porId(id), { tipo: "RepositorioNoEncontrado" });
        if (!repo.ok) return repo;
        const r = configurar(por.valor, repo.valor, ajustes);
        if (r.ok) a.repositorios.guardar(r.valor);
        return r;
      });
    },

    async desconectar(actor: Usuario, id: RepositorioId): R<Repositorio> {
      const por = autorizar(actor, "gestionar-repositorios");
      if (!por.ok) return por;
      return a.transaccion(() => {
        const repo = encontrado(a.repositorios.porId(id), { tipo: "RepositorioNoEncontrado" });
        if (!repo.ok) return repo;
        const r = desconectar(por.valor, repo.valor);
        a.repositorios.guardar(r);
        return ok(r);
      });
    },
  };
}
