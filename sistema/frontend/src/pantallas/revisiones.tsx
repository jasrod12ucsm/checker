// CU-S05 y CU-S06: la lista de revisiones (se actualiza sola mientras alguna está en curso) y «Revisar un PR ahora».
import { useEffect, useMemo, useState, type FormEvent } from "react";
import { Link, useNavigate } from "react-router";
import { Alerta, Insignia, SegunCarga, Selector, Vacio } from "../componentes/basicos";
import { Icono, type NombreIcono } from "../componentes/iconos";
import { Cabecera } from "../componentes/marco";
import { Modal } from "../componentes/modal";
import { esCodigo, mensajeDe, type ErrorApi } from "../dominio/errores";
import { numeroPr } from "../dominio/formularios";
import type { EstadoRevision, Repositorio, Revision } from "../dominio/modelo";
import { puede } from "../dominio/permisos";
import { commitCorto, cumpleFiltro, etiquetaEstado, FILTROS_ESTADO, hayEnCurso, textoResumen, type FiltroEstado } from "../dominio/revisiones";
import { useCarga, useVigilarSesion } from "../estado/carga";
import { useApi, useIntervalo, useUsuario } from "../estado/contexto";

const ICONO_ESTADO: Readonly<Record<EstadoRevision["tipo"], NombreIcono>> = { Pendiente: "reloj", EnAnalisis: "girar", Fallida: "equisCirculo", Publicada: "checkCirculo" };

export function InsigniaEstado({ estado }: { estado: EstadoRevision }) {
  const e = etiquetaEstado(estado);
  const icono = estado.tipo === "Publicada" && estado.veredicto === "ConProblemas" ? "alerta" : ICONO_ESTADO[estado.tipo];
  return (
    <Insignia tono={e.tono} icono={icono}>
      {e.texto}
    </Insignia>
  );
}

/** La revisión más reciente de ese PR, para enlazarla cuando el servicio dice que el commit ya se revisó. */
export function revisionDelPr(rs: readonly Revision[], repositorioId: string, numero: number): Revision | undefined {
  return rs.filter((r) => r.repositorio?.id === repositorioId && r.pr.numero === numero).sort((a, b) => b.creadaEn.localeCompare(a.creadaEn))[0];
}

export function Revisiones() {
  const api = useApi();
  const intervaloMs = useIntervalo();
  const yo = useUsuario();
  const { carga, recargar } = useCarga(() => api.revisiones(), []);
  const { carga: repos } = useCarga(() => api.repositorios(), []);
  const [repo, setRepo] = useState("Todos");
  const [filtro, setFiltro] = useState<FiltroEstado>("Todos");
  const [revisando, setRevisando] = useState(false);

  const enCurso = carga.tipo === "Listo" && hayEnCurso(carga.valor);
  useEffect(() => {
    if (!enCurso) return;
    const t = setTimeout(() => void recargar(true), intervaloMs);
    return () => clearTimeout(t);
  }, [enCurso, carga, intervaloMs, recargar]);

  const repositorios = repos.tipo === "Listo" ? repos.valor : [];
  const opcionesRepo = useMemo(() => [{ valor: "Todos", texto: "Todos" }, ...repositorios.map((r) => ({ valor: r.id, texto: r.nombre }))], [repositorios]);
  const activos = repositorios.filter((r) => r.activo);

  return (
    <>
      <Cabecera titulo="Revisiones" descripcion="Cada PR de C++ que se abre o actualiza en los repositorios conectados.">
        {enCurso && (
          <span className="en-vivo">
            <span className="punto" /> Se actualiza sola
          </span>
        )}
        {puede(yo.rol, "solicitar-revision") && (
          <button type="button" className="boton boton-primario" onClick={() => setRevisando(true)}>
            <Icono nombre="play" /> Revisar un PR ahora
          </button>
        )}
      </Cabecera>
      <SegunCarga carga={carga} reintentar={() => void recargar()}>
        {(rs) => {
          const visibles = rs.filter((r) => (repo === "Todos" || r.repositorio?.id === repo) && cumpleFiltro(r.estado, filtro));
          if (rs.length === 0) return <SinRevisiones hayRepos={repositorios.length > 0} admin={puede(yo.rol, "gestionar-repositorios")} />;
          return (
            <>
              <div className="filtros">
                <Selector etiqueta="Repositorio" valor={repo} opciones={opcionesRepo} alCambiar={setRepo} />
                <Selector etiqueta="Estado" valor={filtro} opciones={FILTROS_ESTADO} alCambiar={setFiltro} />
                <span className="tenue cuenta-filas">{visibles.length === 1 ? "1 revisión" : `${visibles.length} revisiones`}</span>
              </div>
              {visibles.length === 0 ? (
                <Vacio titulo="Ninguna revisión cumple el filtro." />
              ) : (
                <div className="tabla-caja">
                  <table>
                    <thead>
                      <tr>
                        <th>Repositorio</th>
                        <th>Pull request</th>
                        <th>Autor</th>
                        <th>Commit</th>
                        <th>Estado</th>
                        <th>Resumen</th>
                      </tr>
                    </thead>
                    <tbody>
                      {visibles.map((r) => (
                        <tr key={r.id} className={r.estado.tipo === "Pendiente" || r.estado.tipo === "EnAnalisis" ? "fila-en-curso" : undefined}>
                          <td>
                            <code>{r.repositorio?.nombre ?? "—"}</code>
                          </td>
                          <td>
                            <span className="pr">
                              <code>#{r.pr.numero}</code>
                              <Link to={`/revisiones/${r.id}`}>{r.pr.titulo}</Link>
                              {r.pr.enlace && (
                                <a href={r.pr.enlace} target="_blank" rel="noreferrer" aria-label={`Abrir el PR #${r.pr.numero} en GitHub`}>
                                  <Icono nombre="externo" />
                                </a>
                              )}
                            </span>
                          </td>
                          <td>{r.pr.autor}</td>
                          <td>
                            <code>{commitCorto(r.pr.shaCabeza)}</code>
                          </td>
                          <td>
                            <InsigniaEstado estado={r.estado} />
                          </td>
                          <td className="tenue">{r.estado.tipo === "Publicada" ? textoResumen(r.estado.resumen) : "—"}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </>
          );
        }}
      </SegunCarga>
      {revisando && <RevisarAhora repositorios={activos} revisiones={carga.tipo === "Listo" ? carga.valor : []} alCerrar={() => setRevisando(false)} />}
    </>
  );
}

function SinRevisiones({ hayRepos, admin }: { hayRepos: boolean; admin: boolean }) {
  if (hayRepos) return <Vacio titulo="Todavía no hay revisiones.">Aparecerán aquí cuando se abra o actualice un PR en un repositorio conectado, o cuando pidas «Revisar un PR ahora».</Vacio>;
  return admin ? (
    <Vacio titulo="Todavía no hay repositorios conectados.">
      <Link to="/repositorios">Conecta el primero</Link> y configura su webhook en GitHub.
    </Vacio>
  ) : (
    <Vacio titulo="Todavía no hay repositorios conectados.">Pide a un administrador que conecte el repositorio de tu equipo.</Vacio>
  );
}

function RevisarAhora({ repositorios, revisiones, alCerrar }: { repositorios: readonly Repositorio[]; revisiones: readonly Revision[]; alCerrar: () => void }) {
  const api = useApi();
  const vigilar = useVigilarSesion();
  const navegar = useNavigate();
  const [repo, setRepo] = useState(repositorios[0]?.id ?? "");
  const [numero, setNumero] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [fallo, setFallo] = useState<{ error: ErrorApi; numero: number } | null>(null);
  const [enviando, setEnviando] = useState(false);

  async function enviar(e: FormEvent) {
    e.preventDefault();
    const n = numeroPr(numero);
    if (!n.ok) return setError(n.error);
    setError(null);
    setEnviando(true);
    const r = vigilar(await api.solicitar(repo, n.valor));
    setEnviando(false);
    if (!r.ok) return setFallo({ error: r.error, numero: n.valor });
    navegar(`/revisiones/${r.valor.id}`);
  }

  const yaRevisada = fallo !== null && esCodigo(fallo.error, "ShaYaRevisado") ? revisionDelPr(revisiones, repo, fallo.numero) : undefined;
  return (
    <Modal
      titulo="Revisar un PR ahora"
      alCerrar={alCerrar}
      pie={
        <>
          <button type="button" className="boton" onClick={alCerrar}>
            Cancelar
          </button>
          <button type="submit" form="revisar-ahora" className="boton boton-primario" disabled={enviando || repositorios.length === 0}>
            <Icono nombre="play" /> {enviando ? "Pidiendo…" : "Revisar"}
          </button>
        </>
      }
    >
      <p className="tenue">Centinela analiza el último commit del PR sin esperar el webhook.</p>
      {repositorios.length === 0 ? (
        <Alerta tono="info">No hay repositorios activos para revisar.</Alerta>
      ) : (
        <form id="revisar-ahora" onSubmit={(e) => void enviar(e)} noValidate>
          <div className="campo">
            <Selector etiqueta="Repositorio" valor={repo} opciones={repositorios.map((r) => ({ valor: r.id, texto: r.nombre }))} alCambiar={setRepo} />
            <p className="ayuda">Solo aparecen los repositorios activos.</p>
          </div>
          <div className="campo">
            <label htmlFor="numero-pr">Número de PR</label>
            <span className="con-prefijo">
              # <input id="numero-pr" inputMode="numeric" value={numero} onChange={(e) => setNumero(e.target.value)} aria-invalid={error !== null} />
            </span>
            {error !== null && <p className="campo-error">{error}</p>}
          </div>
        </form>
      )}
      {fallo !== null && (
        <Alerta tono={esCodigo(fallo.error, "ShaYaRevisado") ? "info" : "peligro"}>
          {mensajeDe(fallo.error)}
          {yaRevisada && (
            <>
              {" "}
              <Link to={`/revisiones/${yaRevisada.id}`}>Ir a la revisión</Link>
            </>
          )}
        </Alerta>
      )}
    </Modal>
  );
}
