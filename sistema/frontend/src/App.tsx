// Las rutas del panel y sus guardias. El enrutador (navegador o memoria) lo pone quien monta la aplicación.
import { useEffect, type ReactNode } from "react";
import { Link, Navigate, Outlet, Route, Routes, useLocation } from "react-router";
import { Logo, Vacio } from "./componentes/basicos";
import { Marco } from "./componentes/marco";
import { puede, type Permiso } from "./dominio/permisos";
import { useApi, useSesion, useUsuario } from "./estado/contexto";
import { Ingreso, Registro } from "./pantallas/acceso";
import { Detalle } from "./pantallas/detalle";
import { Repositorios } from "./pantallas/repositorios";
import { Revisiones } from "./pantallas/revisiones";
import { Usuarios } from "./pantallas/usuarios";

function Consultando() {
  return (
    <div className="acceso">
      <Logo />
      <p className="cargando" role="status">
        Cargando…
      </p>
    </div>
  );
}

/** Solo con sesión. Sin ella, al ingreso, recordando a dónde se quería ir. */
function RequiereSesion() {
  const { sesion } = useSesion();
  const { pathname, search } = useLocation();
  switch (sesion.tipo) {
    case "Consultando":
      return <Consultando />;
    case "Anonima":
      return <Navigate to="/ingreso" replace state={{ desde: `${pathname}${search}` }} />;
    case "Iniciada":
      return (
        <Marco>
          <Outlet />
        </Marco>
      );
  }
}

/** A dónde volver después de ingresar: la ruta protegida que se pidió (p. ej. el enlace de GitHub a una revisión). */
export function destino(estado: unknown, porDefecto: string): string {
  const desde = (estado as { desde?: unknown } | null)?.desde;
  return typeof desde === "string" && desde.startsWith("/") && !desde.startsWith("//") ? desde : porDefecto;
}

/**
 * Ingreso y registro: quien tiene sesión pasa al panel. Al ingresar, la pantalla solo fija el usuario y esta guardia
 * hace la única navegación; la primera cuenta (registro) va a conectar repositorios.
 */
function SoloAnonimo({ despues, children }: { despues: string; children: ReactNode }) {
  const { sesion } = useSesion();
  const { state } = useLocation();
  if (sesion.tipo === "Consultando") return <Consultando />;
  return sesion.tipo === "Iniciada" ? <Navigate to={destino(state, despues)} replace /> : <>{children}</>;
}

function RequierePermiso({ permiso, children }: { permiso: Permiso; children: ReactNode }) {
  const yo = useUsuario();
  return puede(yo.rol, permiso) ? (
    <>{children}</>
  ) : (
    <Vacio titulo="No tienes permiso para ver esta sección.">
      <Link to="/revisiones">Volver a las revisiones</Link>
    </Vacio>
  );
}

function NoEncontrada() {
  return (
    <Vacio titulo="Esta página no existe.">
      <Link to="/revisiones">Ir a las revisiones</Link>
    </Vacio>
  );
}

export function App() {
  const api = useApi();
  const { sesion, fijarUsuario } = useSesion();

  // Al abrir el panel se pregunta al servicio si la cookie todavía vale.
  useEffect(() => {
    if (sesion.tipo !== "Consultando") return;
    let vigente = true;
    void api.sesion().then((r) => vigente && fijarUsuario(r.ok ? r.valor : null));
    return () => {
      vigente = false;
    };
  }, [api, sesion.tipo, fijarUsuario]);

  return (
    <Routes>
      <Route path="/ingreso" element={<SoloAnonimo despues="/revisiones"><Ingreso /></SoloAnonimo>} />
      <Route path="/registro" element={<SoloAnonimo despues="/repositorios"><Registro /></SoloAnonimo>} />
      <Route element={<RequiereSesion />}>
        <Route path="/" element={<Navigate to="/revisiones" replace />} />
        <Route path="/revisiones" element={<Revisiones />} />
        <Route path="/revisiones/:id" element={<Detalle />} />
        <Route path="/repositorios" element={<Repositorios />} />
        <Route path="/usuarios" element={<RequierePermiso permiso="gestionar-usuarios"><Usuarios /></RequierePermiso>} />
        <Route path="*" element={<NoEncontrada />} />
      </Route>
    </Routes>
  );
}
