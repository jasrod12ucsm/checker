// CU-S06 y CU-S07: el detalle de una revisión, sus hallazgos con la ruta que los explica, clasificarlos y reintentar.
import { useEffect, useState } from "react";
import { Link, useParams } from "react-router";
import { useAvisar } from "../componentes/avisos";
import { Alerta, SegunCarga } from "../componentes/basicos";
import { Icono, type NombreIcono } from "../componentes/iconos";
import { mensajeDe } from "../dominio/errores";
import { fechaHora, haceCuanto } from "../dominio/fechas";
import type { Clasificacion, DetalleRevision, Hallazgo, Repositorio } from "../dominio/modelo";
import { puede } from "../dominio/permisos";
import {
  agruparPorArchivo,
  CLASIFICACIONES,
  commitCorto,
  conHallazgo,
  cuantosFalsos,
  enCurso,
  enlaceArchivos,
  partesMensaje,
  puedeReintentar,
  textoVeredicto,
} from "../dominio/revisiones";
import { useCarga, useVigilarSesion } from "../estado/carga";
import { useApi, useIntervalo, useReloj, useUsuario } from "../estado/contexto";
import { InsigniaEstado } from "./revisiones";

function Mensaje({ texto }: { texto: string }) {
  return (
    <>
      {partesMensaje(texto).map((p, i) => (p.codigo ? <code key={i}>{p.texto}</code> : <span key={i}>{p.texto}</span>))}
    </>
  );
}

export function Detalle() {
  const { id = "" } = useParams();
  const api = useApi();
  const intervaloMs = useIntervalo();
  const { carga, recargar, fijar } = useCarga(() => api.revision(id), [id]);
  const { carga: repos } = useCarga(() => api.repositorios(), []);

  const seguir = carga.tipo === "Listo" && enCurso(carga.valor.estado);
  useEffect(() => {
    if (!seguir) return;
    const t = setTimeout(() => void recargar(true), intervaloMs);
    return () => clearTimeout(t);
  }, [seguir, carga, intervaloMs, recargar]);

  return (
    <SegunCarga carga={carga} reintentar={() => void recargar()}>
      {(d) => <Contenido d={d} repo={repos.tipo === "Listo" ? repos.valor.find((r) => r.id === d.repositorio?.id) : undefined} recargar={() => void recargar(true)} cambiar={(h) => fijar((x) => conHallazgo(x, h))} />}
    </SegunCarga>
  );
}

function Contenido({ d, repo, recargar, cambiar }: { d: DetalleRevision; repo: Repositorio | undefined; recargar: () => void; cambiar: (h: Hallazgo) => void }) {
  const api = useApi();
  const yo = useUsuario();
  const vigilar = useVigilarSesion();
  const avisar = useAvisar();
  const [mostrarFalsos, setMostrarFalsos] = useState(false);
  const [reintentando, setReintentando] = useState(false);
  const e = d.estado;
  const grupos = agruparPorArchivo(d.hallazgos, mostrarFalsos);
  const falsos = cuantosFalsos(d.hallazgos);
  const visibles = grupos.reduce((n, g) => n + g.hallazgos.length, 0);
  const archivos = enlaceArchivos(d);

  async function reintentar() {
    setReintentando(true);
    const r = vigilar(await api.reintentar(d.id));
    setReintentando(false);
    if (!r.ok) return avisar(mensajeDe(r.error), "peligro");
    avisar("Revisión en cola de nuevo.");
    recargar();
  }

  return (
    <>
      <nav className="migas" aria-label="Ruta">
        <Link to="/revisiones">Revisiones</Link>
        <span aria-hidden="true">›</span>
        <code>{d.repositorio?.nombre ?? "—"}</code>
        <span aria-hidden="true">›</span>
        <code>#{d.pr.numero}</code>
      </nav>
      <header className="cabecera-detalle">
        <h1>{d.pr.titulo}</h1>
        {d.pr.enlace && (
          <a href={d.pr.enlace} target="_blank" rel="noreferrer">
            #{d.pr.numero} en GitHub <Icono nombre="externo" />
          </a>
        )}
      </header>
      <dl className="datos">
        <div>
          <dt>Repositorio</dt>
          <dd>
            <code>{d.repositorio?.nombre ?? "—"}</code>
          </dd>
        </div>
        <div>
          <dt>Autor</dt>
          <dd>{d.pr.autor}</dd>
        </div>
        <div>
          <dt>Commit</dt>
          <dd>
            <code>{commitCorto(d.pr.shaCabeza)}</code>
          </dd>
        </div>
        <div>
          <dt>Origen</dt>
          <dd>
            <code>{d.origen}</code>
          </dd>
        </div>
        <div>
          <dt>Intentos</dt>
          <dd>{d.intentos}</dd>
        </div>
        <div>
          <dt>Creada</dt>
          <dd>{fechaHora(d.creadaEn)}</dd>
        </div>
        {(e.tipo === "Publicada" || e.tipo === "Fallida") && (
          <div>
            <dt>{e.tipo === "Publicada" ? "Publicada" : "Terminó"}</dt>
            <dd>{fechaHora(e.desde)}</dd>
          </div>
        )}
      </dl>

      <section className="panel veredicto">
        <div>
          <div className="veredicto-linea">
            <InsigniaEstado estado={e} />
            <span className="tenue">Check</span> <code>centinela/invalidacion</code>
            {repo?.bloquearMerge && e.tipo === "Publicada" && e.veredicto === "ConProblemas" && (
              <span className="texto-peligro">
                <Icono nombre="candado" /> bloquea el merge
              </span>
            )}
          </div>
          <p>{textoVeredicto(e, repo?.politica)}</p>
        </div>
        {puede(yo.rol, "solicitar-revision") && puedeReintentar(e) && (
          <div className="reintentar">
            <button type="button" className="boton" onClick={() => void reintentar()} disabled={reintentando}>
              <Icono nombre="girar" /> Reintentar
            </button>
            <span className="tenue">Por ejemplo, después de marcar falsos positivos.</span>
          </div>
        )}
      </section>

      {e.tipo === "Publicada" && (
        <>
          <div className="tarjetas">
            <Cifra icono="archivo" titulo="Archivos analizados" valor={e.resumen.archivosAnalizados} />
            <Cifra icono="alerta" titulo="Confirmados" valor={e.resumen.confirmados} tono="peligro" />
            <Cifra icono="triangulo" titulo="Posibles" valor={e.resumen.posibles} tono="aviso" />
            <Cifra icono="prohibido" titulo="Descartados como falso positivo" valor={e.resumen.suprimidos} />
          </div>
          {e.resumen.noCompilados > 0 && <Alerta tono="info">{e.resumen.noCompilados === 1 ? "1 archivo no compiló y no se analizó." : `${e.resumen.noCompilados} archivos no compilaron y no se analizaron.`}</Alerta>}

          <div className="titulo-seccion">
            <h2>
              Hallazgos <span className="tenue">{visibles === 0 ? "ninguno" : `${visibles} en ${grupos.length === 1 ? "1 archivo" : `${grupos.length} archivos`}`}</span>
            </h2>
            <label className="interruptor">
              <input type="checkbox" role="switch" checked={mostrarFalsos} onChange={(x) => setMostrarFalsos(x.target.checked)} />
              Mostrar falsos positivos ({falsos})
            </label>
          </div>
          {grupos.length === 0 ? (
            <div className="vacio">
              <strong>{d.hallazgos.length === 0 ? "El checker no encontró usos de referencias invalidadas." : "Todos los hallazgos están marcados como falso positivo."}</strong>
            </div>
          ) : (
            grupos.map((g) => (
              <section key={g.archivo} className="panel archivo" aria-label={g.archivo}>
                <header>
                  <span>
                    <Icono nombre="archivo" /> <code>{g.archivo}</code> <span className="tenue">· {g.hallazgos.length === 1 ? "1 hallazgo" : `${g.hallazgos.length} hallazgos`}</span>
                  </span>
                  {archivos && (
                    <a href={archivos} target="_blank" rel="noreferrer">
                      Ver archivo en el PR <Icono nombre="externo" />
                    </a>
                  )}
                </header>
                {g.hallazgos.map((h) => (
                  <TarjetaHallazgo key={h.id} h={h} cambiar={cambiar} puedeClasificar={puede(yo.rol, "clasificar-hallazgos")} />
                ))}
              </section>
            ))
          )}
        </>
      )}
    </>
  );
}

function Cifra({ icono, titulo, valor, tono }: { icono: NombreIcono; titulo: string; valor: number; tono?: "peligro" | "aviso" }) {
  return (
    <div className="panel cifra">
      <span className="tenue">
        <Icono nombre={icono} /> {titulo}
      </span>
      <strong className={tono ? `texto-${tono}` : undefined}>{valor}</strong>
    </div>
  );
}

function TarjetaHallazgo({ h, cambiar, puedeClasificar }: { h: Hallazgo; cambiar: (h: Hallazgo) => void; puedeClasificar: boolean }) {
  const api = useApi();
  const reloj = useReloj();
  const vigilar = useVigilarSesion();
  const avisar = useAvisar();
  const [guardando, setGuardando] = useState(false);

  async function clasificar(c: Clasificacion) {
    if (c === h.clasificacion) return;
    setGuardando(true);
    const r = vigilar(await api.clasificar(h.id, c));
    setGuardando(false);
    if (!r.ok) return avisar(mensajeDe(r.error), "peligro");
    cambiar(r.valor);
  }

  const ultimo = h.ruta.length - 1;
  return (
    <article className={`hallazgo${h.clasificacion === "FalsoPositivo" ? " descartado" : ""}`} aria-label={`Hallazgo en la línea ${h.linea}`}>
      <div className="hallazgo-texto">
        <div className="hallazgo-cabeza">
          <code className="posicion">
            {h.linea}:{h.columna}
          </code>
          <span className={`insignia insignia-${h.clase === "Confirmado" ? "peligro" : "aviso"}`}>
            <Icono nombre={h.clase === "Confirmado" ? "alerta" : "triangulo"} tamano={14} /> {h.clase}
          </span>
        </div>
        <p>
          <Mensaje texto={h.mensaje} />
        </p>
        {h.ruta.length > 0 && (
          <>
            <h3 className="rotulo">Ruta</h3>
            <ol className="ruta">
              {h.ruta.map((p, i) => (
                <li key={i} className={i === ultimo ? `paso-final paso-${h.clase === "Confirmado" ? "peligro" : "aviso"}` : undefined}>
                  <span className="paso-numero">{i + 1}</span>
                  <code className="tenue">línea {p.linea}</code>
                  <span>{i === ultimo ? <strong>Uso</strong> : <Mensaje texto={p.mensaje} />}</span>
                </li>
              ))}
            </ol>
          </>
        )}
      </div>
      <div className="clasificacion">
        <h3 className="rotulo">Clasificación</h3>
        <div className="segmentado" role="group" aria-label="Clasificación">
          {CLASIFICACIONES.map((c) => (
            <button key={c.valor} type="button" aria-pressed={h.clasificacion === c.valor} disabled={!puedeClasificar || guardando} onClick={() => void clasificar(c.valor)}>
              {h.clasificacion === c.valor && c.valor !== "SinRevisar" && <Icono nombre="check" tamano={14} />}
              {c.texto}
            </button>
          ))}
        </div>
        <p className="tenue">
          {h.autoria !== null
            ? `Marcado por ${h.autoria.por.nombre ?? "una cuenta eliminada"} · ${haceCuanto(h.autoria.en, reloj.ahora())}`
            : "Un falso positivo deja de reportarse en las próximas revisiones de este repositorio."}
        </p>
      </div>
    </article>
  );
}
