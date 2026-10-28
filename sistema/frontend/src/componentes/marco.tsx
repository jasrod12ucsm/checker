// El marco de las pantallas con sesión: menú lateral según el rol, la cuenta y «Cerrar sesión».
import { createContext, useContext, type ReactNode } from "react";
import { NavLink, useLocation } from "react-router";
import { nombreRol, puede, seccionesDe } from "../dominio/permisos";
import { ok } from "../dominio/resultado";
import { pendientes } from "../dominio/usuarios";
import { useCarga } from "../estado/carga";
import { useApi, useSesion, useUsuario } from "../estado/contexto";
import { Avatar, Logo } from "./basicos";
import { Icono, type NombreIcono } from "./iconos";

const Recontar = createContext<() => void>(() => undefined);

/** Para la pantalla que cambia usuarios: vuelve a contar los pendientes del menú. */
export const useRecontarPendientes = () => useContext(Recontar);

const ICONOS: Readonly<Record<string, NombreIcono>> = { "/revisiones": "lista", "/repositorios": "libro", "/usuarios": "usuarios" };

export function Marco({ children }: { children: ReactNode }) {
  const api = useApi();
  const yo = useUsuario();
  const { fijarUsuario } = useSesion();
  const { pathname } = useLocation();
  const admin = puede(yo.rol, "gestionar-usuarios");
  // El número junto a «Usuarios»: los registros que esperan aprobación. Se vuelve a contar al cambiar de pantalla.
  const { carga, recargar } = useCarga(() => (admin ? api.usuarios() : Promise.resolve(ok([]))), [admin, pathname]);
  const porAprobar = carga.tipo === "Listo" ? pendientes(carga.valor).length : 0;

  async function salir() {
    await api.salir();
    fijarUsuario(null);
  }

  return (
    <div className="marco">
      <aside className="lateral">
        <Logo />
        <nav aria-label="Secciones">
          {seccionesDe(yo.rol).map((s) => (
            <NavLink key={s.ruta} to={s.ruta} className={({ isActive }) => `enlace-seccion${isActive ? " activa" : ""}`}>
              <Icono nombre={ICONOS[s.ruta] ?? "lista"} />
              <span>{s.titulo}</span>
              {s.ruta === "/usuarios" && porAprobar > 0 && (
                <span className="contador" aria-label={`${porAprobar} por aprobar`}>
                  {porAprobar}
                </span>
              )}
            </NavLink>
          ))}
        </nav>
        <div className="cuenta">
          <div className="cuenta-persona">
            <Avatar nombre={yo.nombre} />
            <div>
              <strong>{yo.nombre}</strong>
              <span>{yo.email}</span>
              <span className="insignia insignia-neutro">{nombreRol(yo.rol)}</span>
            </div>
          </div>
          <button type="button" className="boton-texto" onClick={() => void salir()}>
            <Icono nombre="salir" /> Cerrar sesión
          </button>
        </div>
      </aside>
      <main className="contenido">
        <Recontar.Provider value={() => void recargar(true)}>{children}</Recontar.Provider>
      </main>
    </div>
  );
}

export function Cabecera({ titulo, descripcion, children }: { titulo: ReactNode; descripcion?: ReactNode; children?: ReactNode }) {
  return (
    <header className="cabecera">
      <div>
        <h1>{titulo}</h1>
        {descripcion && <p>{descripcion}</p>}
      </div>
      {children && <div className="cabecera-acciones">{children}</div>}
    </header>
  );
}
