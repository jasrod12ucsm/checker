// CU-S02: aprobar o rechazar registros, cambiar el rol, desactivar y reactivar cuentas, crear usuarios.
import { useState, type FormEvent } from "react";
import { useAvisar } from "../componentes/avisos";
import { Alerta, Avatar, Campo, Insignia, SegunCarga, Selector } from "../componentes/basicos";
import { Icono } from "../componentes/iconos";
import { Cabecera, useRecontarPendientes } from "../componentes/marco";
import { Modal } from "../componentes/modal";
import { esCodigo, mensajeDe, type ErrorApi } from "../dominio/errores";
import { diaRelativo, fechaRelativa } from "../dominio/fechas";
import { validarNuevoUsuario, type ErroresDe } from "../dominio/formularios";
import type { EstadoUsuario, Rol, Usuario } from "../dominio/modelo";
import { nombreRol } from "../dominio/permisos";
import { accionPara, ordenarUsuarios, pendientes, puedeCambiarRol, reemplazar } from "../dominio/usuarios";
import type { CambioUsuario } from "../api/puerto";
import { useCarga, useVigilarSesion } from "../estado/carga";
import { useApi, useReloj, useUsuario } from "../estado/contexto";

const ROLES: readonly { readonly valor: Rol; readonly texto: string }[] = [
  { valor: "desarrollador", texto: "Desarrollador" },
  { valor: "administrador", texto: "Administrador" },
];

function InsigniaUsuario({ estado }: { estado: EstadoUsuario }) {
  switch (estado) {
    case "Activo":
      return (
        <Insignia tono="exito" icono="checkCirculo">
          Activo
        </Insignia>
      );
    case "Pendiente":
      return (
        <Insignia tono="aviso" icono="reloj">
          Pendiente
        </Insignia>
      );
    case "Desactivado":
      return (
        <Insignia tono="neutro" icono="prohibido">
          Desactivado
        </Insignia>
      );
  }
}

export function Usuarios() {
  const api = useApi();
  const yo = useUsuario();
  const reloj = useReloj();
  const vigilar = useVigilarSesion();
  const avisar = useAvisar();
  const recontar = useRecontarPendientes();
  const { carga, recargar, fijar } = useCarga(() => api.usuarios(), []);
  const [rolAlAprobar, setRolAlAprobar] = useState<Readonly<Record<string, Rol>>>({});
  const [ocupado, setOcupado] = useState<string | null>(null);
  const [creando, setCreando] = useState(false);

  async function actualizar(u: Usuario, c: CambioUsuario, exito: (n: Usuario) => string) {
    setOcupado(u.id);
    const r = vigilar(await api.actualizarUsuario(u.id, c));
    setOcupado(null);
    if (!r.ok) return avisar(mensajeDe(r.error), "peligro");
    fijar((us) => reemplazar(us, r.valor));
    recontar();
    avisar(exito(r.valor));
  }

  const ahora = reloj.ahora();
  return (
    <>
      <Cabecera titulo="Usuarios" descripcion="Aprueba registros, asigna roles y controla quién puede ingresar.">
        <button type="button" className="boton" onClick={() => setCreando(true)}>
          <Icono nombre="agregarUsuario" /> Crear usuario
        </button>
      </Cabecera>
      <SegunCarga carga={carga} reintentar={() => void recargar()}>
        {(us) => {
          const porAprobar = pendientes(us);
          return (
            <>
              <section aria-labelledby="titulo-pendientes">
                <h2 id="titulo-pendientes" className="titulo-seccion">
                  Pendientes de aprobación{" "}
                  <Insignia tono="aviso" icono="reloj">
                    {porAprobar.length}
                  </Insignia>
                </h2>
                {porAprobar.length === 0 ? (
                  <p className="tenue">No hay registros por aprobar.</p>
                ) : (
                  <>
                    <div className="tabla-caja tabla-aviso">
                      <table>
                        <thead>
                          <tr>
                            <th>Nombre</th>
                            <th>Correo</th>
                            <th>Se registró</th>
                            <th>Rol al aprobar</th>
                            <th aria-label="Acciones" />
                          </tr>
                        </thead>
                        <tbody>
                          {porAprobar.map((u) => {
                            const rol = rolAlAprobar[u.id] ?? "desarrollador";
                            return (
                              <tr key={u.id}>
                                <td>
                                  <span className="persona">
                                    <Avatar nombre={u.nombre} /> <strong>{u.nombre}</strong>
                                  </span>
                                </td>
                                <td>
                                  <code>{u.email}</code>
                                </td>
                                <td className="tenue">{fechaRelativa(u.creadoEn, ahora)}</td>
                                <td>
                                  <Selector etiqueta={`Rol al aprobar a ${u.nombre}`} oculta valor={rol} opciones={ROLES} alCambiar={(r) => setRolAlAprobar({ ...rolAlAprobar, [u.id]: r })} />
                                </td>
                                <td className="acciones">
                                  <button
                                    type="button"
                                    className="boton boton-primario"
                                    disabled={ocupado === u.id}
                                    aria-label={`Aprobar a ${u.nombre}`}
                                    onClick={() => void actualizar(u, { estado: "Activo", rol }, (n) => `Se aprobó a ${n.nombre} como ${nombreRol(n.rol)}.`)}
                                  >
                                    <Icono nombre="check" /> Aprobar
                                  </button>
                                  <button
                                    type="button"
                                    className="boton boton-peligro"
                                    disabled={ocupado === u.id}
                                    aria-label={`Rechazar a ${u.nombre}`}
                                    onClick={() => void actualizar(u, { estado: "Desactivado" }, (n) => `Se rechazó el registro de ${n.nombre}.`)}
                                  >
                                    Rechazar
                                  </button>
                                </td>
                              </tr>
                            );
                          })}
                        </tbody>
                      </table>
                    </div>
                    <p className="tenue nota">Rechazar deja la cuenta desactivada; puedes activarla más tarde desde la tabla de usuarios.</p>
                  </>
                )}
              </section>

              <section aria-labelledby="titulo-todos">
                <h2 id="titulo-todos" className="titulo-seccion">
                  Todos los usuarios <span className="tenue">{us.length}</span>
                </h2>
                <div className="tabla-caja">
                  <table>
                    <thead>
                      <tr>
                        <th>Nombre</th>
                        <th>Correo</th>
                        <th>Rol</th>
                        <th>Estado</th>
                        <th>Alta</th>
                        <th aria-label="Acciones" />
                      </tr>
                    </thead>
                    <tbody>
                      {ordenarUsuarios(us, yo.id).map((u) => {
                        const accion = accionPara(u, yo.id);
                        return (
                          <tr key={u.id}>
                            <td>
                              <span className="persona">
                                <Avatar nombre={u.nombre} /> <strong>{u.nombre}</strong>
                                {u.id === yo.id && <span className="insignia insignia-neutro">tú</span>}
                              </span>
                            </td>
                            <td>
                              <code>{u.email}</code>
                            </td>
                            <td>
                              <Selector
                                etiqueta={`Rol de ${u.nombre}`}
                                oculta
                                valor={u.rol}
                                opciones={ROLES}
                                deshabilitado={!puedeCambiarRol(u, yo.id) || u.estado === "Pendiente" || ocupado === u.id}
                                alCambiar={(rol) => void actualizar(u, { rol }, (n) => `${n.nombre} ahora es ${nombreRol(n.rol)}.`)}
                              />
                            </td>
                            <td>
                              <InsigniaUsuario estado={u.estado} />
                            </td>
                            <td className="tenue">{diaRelativo(u.creadoEn, ahora)}</td>
                            <td className="acciones">
                              {accion.tipo === "Propio" && <span className="tenue nota-fila">No puedes desactivar ni cambiar el rol de tu propio usuario.</span>}
                              {accion.tipo === "Cambiar" && (
                                <button
                                  type="button"
                                  className="boton"
                                  disabled={ocupado === u.id}
                                  aria-label={`${accion.texto} a ${u.nombre}`}
                                  onClick={() => void actualizar(u, { estado: accion.hacia }, (n) => (n.estado === "Activo" ? `Se activó a ${n.nombre}.` : `Se desactivó a ${n.nombre}; sus sesiones se cerraron.`))}
                                >
                                  {accion.texto}
                                </button>
                              )}
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              </section>
            </>
          );
        }}
      </SegunCarga>
      {creando && (
        <CrearUsuario
          alCerrar={() => setCreando(false)}
          alCrear={(u) => {
            fijar((us) => reemplazar(us, u));
            setCreando(false);
            avisar(`Se creó la cuenta de ${u.nombre} como ${nombreRol(u.rol)}.`);
          }}
        />
      )}
    </>
  );
}

function CrearUsuario({ alCerrar, alCrear }: { alCerrar: () => void; alCrear: (u: Usuario) => void }) {
  const api = useApi();
  const vigilar = useVigilarSesion();
  const [f, setF] = useState<{ email: string; nombre: string; clave: string; rol: Rol }>({ email: "", nombre: "", clave: "", rol: "desarrollador" });
  const [errores, setErrores] = useState<ErroresDe<"email" | "nombre" | "clave">>({});
  const [fallo, setFallo] = useState<ErrorApi | null>(null);
  const [enviando, setEnviando] = useState(false);

  async function enviar(e: FormEvent) {
    e.preventDefault();
    const v = validarNuevoUsuario(f);
    if (!v.ok) return setErrores(v.error);
    setErrores({});
    setEnviando(true);
    const r = vigilar(await api.crearUsuario(v.valor));
    setEnviando(false);
    if (!r.ok) return esCodigo(r.error, "EmailEnUso") ? setErrores({ email: mensajeDe(r.error) }) : setFallo(r.error);
    alCrear(r.valor);
  }

  return (
    <Modal
      titulo="Crear usuario"
      alCerrar={alCerrar}
      pie={
        <>
          <button type="button" className="boton" onClick={alCerrar}>
            Cancelar
          </button>
          <button type="submit" form="crear-usuario" className="boton boton-primario" disabled={enviando}>
            Crear
          </button>
        </>
      }
    >
      <p className="tenue">La cuenta queda activa; comparte la clave con la persona por un medio seguro.</p>
      {fallo !== null && <Alerta>{mensajeDe(fallo)}</Alerta>}
      <form id="crear-usuario" onSubmit={(e) => void enviar(e)} noValidate>
        <Campo etiqueta="Correo" type="email" value={f.email} onChange={(e) => setF({ ...f, email: e.target.value })} error={errores.email} />
        <Campo etiqueta="Nombre" value={f.nombre} onChange={(e) => setF({ ...f, nombre: e.target.value })} error={errores.nombre} />
        <Campo etiqueta="Clave inicial" type="password" autoComplete="new-password" value={f.clave} onChange={(e) => setF({ ...f, clave: e.target.value })} error={errores.clave} />
        <div className="campo">
          <Selector etiqueta="Rol" valor={f.rol} opciones={ROLES} alCambiar={(rol) => setF({ ...f, rol })} />
        </div>
      </form>
    </Modal>
  );
}
