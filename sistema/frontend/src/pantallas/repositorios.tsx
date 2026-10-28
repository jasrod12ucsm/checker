// CU-S03: conectar repositorios de GitHub, ver su webhook, cambiar la política y desconectarlos.
// El desarrollador ve la tabla; solo el administrador la cambia.
import { useState, type FormEvent } from "react";
import { useAvisar } from "../componentes/avisos";
import { Alerta, Campo, Insignia, SegunCarga, Vacio } from "../componentes/basicos";
import { Icono } from "../componentes/iconos";
import { Cabecera } from "../componentes/marco";
import { Modal } from "../componentes/modal";
import { esCodigo, mensajeDe, type ErrorApi } from "../dominio/errores";
import { fecha } from "../dominio/fechas";
import { nombreRepositorio } from "../dominio/formularios";
import type { Politica, Repositorio, Webhook } from "../dominio/modelo";
import { puede } from "../dominio/permisos";
import { textoPolitica } from "../dominio/revisiones";
import { useCarga, useVigilarSesion } from "../estado/carga";
import { useApi, useUsuario } from "../estado/contexto";

type Dialogo =
  | { readonly tipo: "Ninguno" }
  | { readonly tipo: "Conectar" }
  | { readonly tipo: "Webhook"; readonly repo: Repositorio; readonly recien: boolean }
  | { readonly tipo: "Editar"; readonly repo: Repositorio }
  | { readonly tipo: "Desconectar"; readonly repo: Repositorio };

const reemplazar = (rs: readonly Repositorio[], r: Repositorio) => (rs.some((x) => x.id === r.id) ? rs.map((x) => (x.id === r.id ? r : x)) : [r, ...rs]);

export function Repositorios() {
  const api = useApi();
  const yo = useUsuario();
  const admin = puede(yo.rol, "gestionar-repositorios");
  const { carga, recargar, fijar } = useCarga(() => api.repositorios(), []);
  const [dialogo, setDialogo] = useState<Dialogo>({ tipo: "Ninguno" });
  const cerrar = () => setDialogo({ tipo: "Ninguno" });
  const guardado = (r: Repositorio) => fijar((rs) => reemplazar(rs, r));

  return (
    <>
      <Cabecera titulo="Repositorios" descripcion="Repositorios de GitHub que Centinela revisa y cómo reporta sus hallazgos.">
        {admin && (
          <button type="button" className="boton boton-primario" onClick={() => setDialogo({ tipo: "Conectar" })}>
            <Icono nombre="mas" /> Conectar repositorio
          </button>
        )}
      </Cabecera>
      <SegunCarga carga={carga} reintentar={() => void recargar()}>
        {(rs) =>
          rs.length === 0 ? (
            <Vacio titulo="Todavía no hay repositorios conectados.">{admin ? "Conecta el primero para que Centinela revise sus pull requests." : "Pide a un administrador que conecte el repositorio de tu equipo."}</Vacio>
          ) : (
            <>
              <div className="tabla-caja">
                <table>
                  <thead>
                    <tr>
                      <th>Repositorio</th>
                      <th>Política</th>
                      <th>Bloquea el merge</th>
                      <th>Estado</th>
                      <th>Conectado</th>
                      {admin && <th aria-label="Acciones" />}
                    </tr>
                  </thead>
                  <tbody>
                    {rs.map((r) => (
                      <tr key={r.id}>
                        <td>
                          <span className="con-icono">
                            <Icono nombre="libro" /> <code>{r.nombre}</code>
                          </span>
                        </td>
                        <td>
                          <code>{r.politica}</code>
                          <span className="tenue bloque">{textoPolitica(r.politica)}</span>
                        </td>
                        <td>
                          {r.bloquearMerge ? (
                            <span className="con-icono">
                              <Icono nombre="candado" /> Sí
                            </span>
                          ) : (
                            <span className="tenue">No</span>
                          )}
                        </td>
                        <td>
                          {r.activo ? (
                            <Insignia tono="exito" icono="checkCirculo">
                              Activo
                            </Insignia>
                          ) : (
                            <Insignia tono="neutro" icono="desconectar">
                              Desconectado
                            </Insignia>
                          )}
                        </td>
                        <td className="tenue">{fecha(r.conectadoEn)}</td>
                        {admin && (
                          <td className="acciones">
                            {r.activo && (
                              <>
                                {r.webhook && (
                                  <button type="button" className="boton-texto" onClick={() => setDialogo({ tipo: "Webhook", repo: r, recien: false })} aria-label={`Webhook de ${r.nombre}`}>
                                    Webhook
                                  </button>
                                )}
                                <button type="button" className="boton-texto" onClick={() => setDialogo({ tipo: "Editar", repo: r })} aria-label={`Editar ${r.nombre}`}>
                                  <Icono nombre="lapiz" /> Editar
                                </button>
                                <button type="button" className="boton boton-peligro" onClick={() => setDialogo({ tipo: "Desconectar", repo: r })} aria-label={`Desconectar ${r.nombre}`}>
                                  <Icono nombre="desconectar" /> Desconectar
                                </button>
                              </>
                            )}
                          </td>
                        )}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <p className="tenue nota">Al desconectar un repositorio, Centinela deja de revisar sus PR; las revisiones anteriores se conservan.</p>
            </>
          )
        }
      </SegunCarga>
      {dialogo.tipo === "Conectar" && (
        <Conectar
          alCerrar={cerrar}
          alConectar={(r) => {
            guardado(r);
            setDialogo({ tipo: "Webhook", repo: r, recien: true });
          }}
        />
      )}
      {dialogo.tipo === "Webhook" && dialogo.repo.webhook && <VerWebhook repo={dialogo.repo} webhook={dialogo.repo.webhook} recien={dialogo.recien} alCerrar={cerrar} />}
      {dialogo.tipo === "Editar" && (
        <Editar
          repo={dialogo.repo}
          alCerrar={cerrar}
          alGuardar={(r) => {
            guardado(r);
            cerrar();
          }}
        />
      )}
      {dialogo.tipo === "Desconectar" && (
        <Desconectar
          repo={dialogo.repo}
          alCerrar={cerrar}
          alDesconectar={(r) => {
            guardado(r);
            cerrar();
          }}
        />
      )}
    </>
  );
}

function OpcionesPolitica({ valor, alCambiar }: { valor: Politica; alCambiar: (p: Politica) => void }) {
  const opciones: readonly { p: Politica; titulo: string; texto: string }[] = [
    { p: "Silent", titulo: "solo confirmados", texto: "Comenta en el PR únicamente los usos de un handle que con seguridad quedó invalidado." },
    { p: "Possibly", titulo: "también posibles", texto: "Comenta además los usos que pueden quedar invalidados según el camino, como un push_back sin reserve." },
  ];
  return (
    <fieldset className="opciones">
      <legend>Política</legend>
      {opciones.map((o) => (
        <label key={o.p} className={`opcion${valor === o.p ? " elegida" : ""}`}>
          <input type="radio" name="politica" value={o.p} checked={valor === o.p} onChange={() => alCambiar(o.p)} />
          <span>
            <strong>
              <code>{o.p}</code> · {o.titulo}
            </strong>
            <span className="tenue bloque">{o.texto}</span>
          </span>
        </label>
      ))}
    </fieldset>
  );
}

function Bloqueo({ valor, alCambiar }: { valor: boolean; alCambiar: (b: boolean) => void }) {
  return (
    <label className="interruptor interruptor-grande">
      <input type="checkbox" role="switch" checked={valor} onChange={(e) => alCambiar(e.target.checked)} />
      <span>
        <strong>Bloquear el merge si hay problemas</strong>
        <span className="tenue bloque">
          El check <code>centinela/invalidacion</code> falla cuando la revisión encuentra problemas.
        </span>
      </span>
    </label>
  );
}

function PieFormulario({ formulario, texto, enviando, alCerrar, peligro }: { formulario: string; texto: string; enviando: boolean; alCerrar: () => void; peligro?: boolean }) {
  return (
    <>
      <button type="button" className="boton" onClick={alCerrar}>
        Cancelar
      </button>
      <button type="submit" form={formulario} className={`boton ${peligro ? "boton-peligro-lleno" : "boton-primario"}`} disabled={enviando}>
        {texto}
      </button>
    </>
  );
}

function Conectar({ alCerrar, alConectar }: { alCerrar: () => void; alConectar: (r: Repositorio) => void }) {
  const api = useApi();
  const vigilar = useVigilarSesion();
  const [nombre, setNombre] = useState("");
  const [politica, setPolitica] = useState<Politica>("Silent");
  const [bloquear, setBloquear] = useState(true);
  const [error, setError] = useState<string | undefined>(undefined);
  const [fallo, setFallo] = useState<ErrorApi | null>(null);
  const [enviando, setEnviando] = useState(false);

  async function enviar(e: FormEvent) {
    e.preventDefault();
    const n = nombreRepositorio(nombre);
    if (!n.ok) return setError(n.error);
    setError(undefined);
    setEnviando(true);
    const r = vigilar(await api.conectar({ nombre: n.valor, politica, bloquearMerge: bloquear }));
    setEnviando(false);
    if (!r.ok) return esCodigo(r.error, "RepositorioYaConectado") ? setError(mensajeDe(r.error)) : setFallo(r.error);
    alConectar(r.valor);
  }

  return (
    <Modal titulo="Conectar repositorio" alCerrar={alCerrar} pie={<PieFormulario formulario="conectar" texto="Conectar" enviando={enviando} alCerrar={alCerrar} />}>
      <p className="tenue">Después te daremos la URL del webhook y el secreto para GitHub.</p>
      {fallo !== null && <Alerta>{mensajeDe(fallo)}</Alerta>}
      <form id="conectar" onSubmit={(e) => void enviar(e)} noValidate>
        <Campo
          etiqueta="Repositorio"
          value={nombre}
          placeholder="propietario/nombre"
          onChange={(e) => setNombre(e.target.value)}
          error={error}
          ayuda={
            <p className="ayuda">
              Con el formato <code>propietario/nombre</code>, tal como aparece en GitHub.
            </p>
          }
        />
        <OpcionesPolitica valor={politica} alCambiar={setPolitica} />
        <Bloqueo valor={bloquear} alCambiar={setBloquear} />
      </form>
    </Modal>
  );
}

function Copiable({ etiqueta, valor, secreto }: { etiqueta: string; valor: string; secreto?: boolean }) {
  const [visible, setVisible] = useState(!secreto);
  const [copiado, setCopiado] = useState(false);
  async function copiar() {
    try {
      await navigator.clipboard.writeText(valor);
      setCopiado(true);
    } catch {
      setCopiado(false);
    }
  }
  return (
    <div className="campo">
      <span className="etiqueta">{etiqueta}</span>
      <div className="copiable">
        <input readOnly aria-label={etiqueta} type={visible ? "text" : "password"} value={valor} />
        {secreto && (
          <button type="button" className="boton" onClick={() => setVisible(!visible)}>
            <Icono nombre="ojo" /> {visible ? "Ocultar" : "Mostrar"}
          </button>
        )}
        <button type="button" className="boton" onClick={() => void copiar()} aria-label={`Copiar ${etiqueta.toLowerCase()}`}>
          <Icono nombre={copiado ? "check" : "copiar"} /> {copiado ? "Copiado" : "Copiar"}
        </button>
      </div>
    </div>
  );
}

function VerWebhook({ repo, webhook, recien, alCerrar }: { repo: Repositorio; webhook: Webhook; recien: boolean; alCerrar: () => void }) {
  return (
    <Modal
      titulo={
        <>
          Configura el webhook de <code>{repo.nombre}</code>
        </>
      }
      alCerrar={alCerrar}
      pie={
        <button type="button" className="boton boton-primario" onClick={alCerrar}>
          Listo
        </button>
      }
    >
      {recien && (
        <Insignia tono="exito" icono="checkCirculo">
          Conectado
        </Insignia>
      )}
      <Copiable etiqueta="URL del webhook" valor={webhook.url} />
      <Copiable etiqueta="Secreto" valor={webhook.secreto} secreto />
      <h3 className="rotulo">En GitHub</h3>
      <ol className="pasos">
        <li>
          Abre <strong>Settings → Webhooks → Add webhook</strong> en el repositorio.
        </li>
        <li>
          Pega la URL en <strong>Payload URL</strong> y elige <code>{webhook.tipoContenido}</code> en <strong>Content type</strong>.
        </li>
        <li>
          Pega el secreto en <strong>Secret</strong>.
        </li>
        <li>
          En los eventos, elige <strong>Let me select individual events</strong> y marca solo <strong>Pull requests</strong>.
        </li>
        <li>
          En <strong>Settings → Branches</strong>, crea una regla de protección para la rama principal y exige el check <code>centinela/invalidacion</code>.
        </li>
      </ol>
      <Alerta tono="info">El paso 5 es lo que permite que una revisión con problemas bloquee el merge.</Alerta>
    </Modal>
  );
}

function Editar({ repo, alCerrar, alGuardar }: { repo: Repositorio; alCerrar: () => void; alGuardar: (r: Repositorio) => void }) {
  const api = useApi();
  const vigilar = useVigilarSesion();
  const [politica, setPolitica] = useState<Politica>(repo.politica);
  const [bloquear, setBloquear] = useState(repo.bloquearMerge);
  const [fallo, setFallo] = useState<ErrorApi | null>(null);
  const [enviando, setEnviando] = useState(false);

  async function enviar(e: FormEvent) {
    e.preventDefault();
    setEnviando(true);
    const r = vigilar(await api.configurar(repo.id, { politica, bloquearMerge: bloquear }));
    setEnviando(false);
    if (!r.ok) return setFallo(r.error);
    alGuardar(r.valor);
  }

  return (
    <Modal
      titulo={
        <>
          Editar <code>{repo.nombre}</code>
        </>
      }
      alCerrar={alCerrar}
      pie={<PieFormulario formulario="editar" texto="Guardar" enviando={enviando} alCerrar={alCerrar} />}
    >
      {fallo !== null && <Alerta>{mensajeDe(fallo)}</Alerta>}
      <form id="editar" onSubmit={(e) => void enviar(e)}>
        <OpcionesPolitica valor={politica} alCambiar={setPolitica} />
        <Bloqueo valor={bloquear} alCambiar={setBloquear} />
      </form>
    </Modal>
  );
}

function Desconectar({ repo, alCerrar, alDesconectar }: { repo: Repositorio; alCerrar: () => void; alDesconectar: (r: Repositorio) => void }) {
  const api = useApi();
  const vigilar = useVigilarSesion();
  const avisar = useAvisar();
  const [fallo, setFallo] = useState<ErrorApi | null>(null);
  const [enviando, setEnviando] = useState(false);

  async function enviar(e: FormEvent) {
    e.preventDefault();
    setEnviando(true);
    const r = vigilar(await api.desconectar(repo.id));
    setEnviando(false);
    if (!r.ok) return setFallo(r.error);
    avisar(
      <>
        Se desconectó <strong>{repo.nombre}</strong>.
      </>,
    );
    alDesconectar(r.valor);
  }

  return (
    <Modal
      titulo={
        <>
          ¿Desconectar <code>{repo.nombre}</code>?
        </>
      }
      alCerrar={alCerrar}
      pie={<PieFormulario formulario="desconectar" texto="Desconectar" enviando={enviando} alCerrar={alCerrar} peligro />}
    >
      {fallo !== null && <Alerta>{mensajeDe(fallo)}</Alerta>}
      <form id="desconectar" onSubmit={(e) => void enviar(e)}>
        <p>Centinela dejará de revisar sus pull requests y de publicar el check. Las revisiones anteriores se conservan.</p>
        <p className="tenue">Borra también el webhook en GitHub para que deje de enviar eventos.</p>
      </form>
    </Modal>
  );
}
