// CU-S01: ingresar y registrarse. Nada viene predefinido: quien se registra primero administra;
// los demás esperan la aprobación de un administrador.
import { useState, type FormEvent, type ReactNode } from "react";
import { Link } from "react-router";
import { Alerta, Campo, Insignia, Logo } from "../componentes/basicos";
import { Icono } from "../componentes/iconos";
import { esCodigo, mensajeDe, type ErrorApi } from "../dominio/errores";
import { reglasClave, validarIngreso, validarRegistro, type ErroresDe } from "../dominio/formularios";
import { useCarga } from "../estado/carga";
import { useApi, useSesion } from "../estado/contexto";

function Tarjeta({ children }: { children: ReactNode }) {
  return (
    <div className="acceso">
      <Logo />
      <div className="tarjeta">{children}</div>
    </div>
  );
}

export function Ingreso() {
  const api = useApi();
  const { sesion, fijarUsuario } = useSesion();
  const [email, setEmail] = useState("");
  const [clave, setClave] = useState("");
  const [errores, setErrores] = useState<ErroresDe<"email" | "clave">>({});
  const [fallo, setFallo] = useState<ErrorApi | null>(null);
  const [enviando, setEnviando] = useState(false);
  const { carga: registro } = useCarga(() => api.estadoRegistro(), []);

  async function enviar(e: FormEvent) {
    e.preventDefault();
    const v = validarIngreso({ email, clave });
    if (!v.ok) return setErrores(v.error);
    setErrores({});
    setEnviando(true);
    const r = await api.ingresar(v.valor);
    setEnviando(false);
    if (!r.ok) return setFallo(r.error);
    fijarUsuario(r.valor);
  }

  const avisoSesion = sesion.tipo === "Anonima" ? sesion.aviso : undefined;
  const claveMal = fallo !== null && esCodigo(fallo, "CredencialesInvalidas");
  return (
    <Tarjeta>
      <h1>Ingresa</h1>
      <p className="tenue">Usa el correo con el que te registraste.</p>
      {fallo === null && avisoSesion !== undefined && <Alerta tono="info">{avisoSesion}</Alerta>}
      {fallo !== null && <Alerta>{mensajeDe(fallo)}</Alerta>}
      {registro.tipo === "Listo" && !registro.valor.hayUsuarios && (
        <Alerta tono="info">
          Centinela todavía no tiene cuentas. <Link to="/registro">Crea la primera</Link>: será la de administración.
        </Alerta>
      )}
      <form onSubmit={(e) => void enviar(e)} noValidate>
        <Campo etiqueta="Correo" type="email" autoComplete="email" value={email} onChange={(e) => setEmail(e.target.value)} error={errores.email} />
        <Campo etiqueta="Clave" type="password" autoComplete="current-password" value={clave} onChange={(e) => setClave(e.target.value)} error={errores.clave} aria-invalid={claveMal || errores.clave !== undefined} />
        <button type="submit" className="boton boton-primario boton-ancho" disabled={enviando}>
          {enviando ? "Ingresando…" : "Ingresar"}
        </button>
      </form>
      <p className="pie-acceso">
        ¿No tienes cuenta? <Link to="/registro">Regístrate</Link>
      </p>
    </Tarjeta>
  );
}

export function Registro() {
  const api = useApi();
  const { fijarUsuario } = useSesion();
  const [f, setF] = useState({ email: "", nombre: "", clave: "", confirmacion: "" });
  const [errores, setErrores] = useState<ErroresDe<"email" | "nombre" | "clave" | "confirmacion">>({});
  const [fallo, setFallo] = useState<ErrorApi | null>(null);
  const [pendiente, setPendiente] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);
  const { carga } = useCarga(() => api.estadoRegistro(), []);
  const primera = carga.tipo === "Listo" && !carga.valor.hayUsuarios;
  const reglas = reglasClave(f.clave);
  const cambiar = (campo: keyof typeof f) => (e: { target: { value: string } }) => setF({ ...f, [campo]: e.target.value });

  async function enviar(e: FormEvent) {
    e.preventDefault();
    const v = validarRegistro(f);
    if (!v.ok) return setErrores(v.error);
    setErrores({});
    setEnviando(true);
    const r = await api.registrar(v.valor);
    setEnviando(false);
    if (!r.ok) {
      if (esCodigo(r.error, "EmailEnUso")) return setErrores({ email: mensajeDe(r.error) });
      return setFallo(r.error);
    }
    if (r.valor.pendienteDeAprobacion) return setPendiente(r.valor.usuario.email);
    // La primera cuenta ya trae su sesión: la guardia la lleva a conectar repositorios.
    fijarUsuario(r.valor.usuario);
  }

  if (pendiente !== null)
    return (
      <Tarjeta>
        <div className="centrado">
          <span className="icono-grande icono-aviso">
            <Icono nombre="reloj" tamano={28} />
          </span>
          <Insignia tono="aviso" icono="reloj">
            Pendiente de aprobación
          </Insignia>
          <h1>Tu cuenta espera la aprobación de un administrador</h1>
          <p className="tenue">
            Creamos la cuenta de <strong>{pendiente}</strong>. Podrás ingresar en cuanto un administrador la apruebe.
          </p>
          <Link to="/ingreso" className="boton boton-ancho">
            Volver al ingreso
          </Link>
        </div>
      </Tarjeta>
    );

  return (
    <Tarjeta>
      <h1>Crea tu cuenta</h1>
      <p className="tenue">Revisión automática de invalidación de contenedores en tus PR de C++.</p>
      {primera && (
        <Alerta tono="info">
          <strong>Eres la primera persona: tu cuenta será la de administración.</strong>
          <br />
          Al crearla entrarás directo al panel para conectar repositorios y aprobar a tu equipo.
        </Alerta>
      )}
      {fallo !== null && <Alerta>{mensajeDe(fallo)}</Alerta>}
      <form onSubmit={(e) => void enviar(e)} noValidate>
        <Campo etiqueta="Correo" type="email" autoComplete="email" value={f.email} onChange={cambiar("email")} error={errores.email} />
        <Campo etiqueta="Nombre" autoComplete="name" value={f.nombre} onChange={cambiar("nombre")} error={errores.nombre} />
        <Campo
          etiqueta="Clave"
          type="password"
          autoComplete="new-password"
          value={f.clave}
          onChange={cambiar("clave")}
          error={errores.clave}
          ayuda={
            <ul className="reglas" aria-label="Requisitos de la clave">
              <li className={reglas.largo ? "cumple" : undefined}>
                <Icono nombre={reglas.largo ? "check" : "reloj"} tamano={14} /> Al menos 10 caracteres
              </li>
              <li className={reglas.letrasYNumeros ? "cumple" : undefined}>
                <Icono nombre={reglas.letrasYNumeros ? "check" : "reloj"} tamano={14} /> Letras y números
              </li>
            </ul>
          }
        />
        <Campo etiqueta="Confirmar clave" type="password" autoComplete="new-password" value={f.confirmacion} onChange={cambiar("confirmacion")} error={errores.confirmacion} />
        <button type="submit" className="boton boton-primario boton-ancho" disabled={enviando}>
          {enviando ? "Creando…" : "Crear cuenta"}
        </button>
      </form>
      <p className="pie-acceso">
        ¿Ya tienes cuenta? <Link to="/ingreso">Ingresa</Link>
      </p>
    </Tarjeta>
  );
}
