import { email, err, ok, texto, usuarioId, type UsuarioId } from "@centinela/kernel";
import { actualizarUsuario, claveNueva, crearUsuario, ingresar, registrar, validarSesion, type CambioUsuario, type HashClave, type Rol, type Usuario } from "@centinela/identidad";
import { autorizar, encontrado, type Dependencias, type R } from "./contexto";

// Un hash con el formato del adaptador que no corresponde a ninguna clave: se verifica
// contra él cuando el correo no existe, para que el tiempo de respuesta no lo delate.
const HASH_FICTICIO = "scrypt$AAAAAAAAAAAAAAAAAAAAAA==$AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==" as HashClave;

export interface NuevoUsuario {
  readonly email: string;
  readonly nombre: string;
  readonly clave: string;
  readonly rol: Rol;
}

export function casosIdentidad(d: Dependencias) {
  const { almacen: a } = d;

  async function datosValidos(n: Omit<NuevoUsuario, "rol">) {
    const e = email(n.email);
    if (!e.ok) return e;
    const nom = texto("nombre", n.nombre, 100);
    if (!nom.ok) return nom;
    const c = claveNueva(n.clave);
    if (!c.ok) return c;
    const id = usuarioId(d.ids.nuevo());
    if (!id.ok) return id;
    return ok({ id: id.valor, email: e.valor, nombre: nom.valor, hashClave: await d.claves.hashear(c.valor) });
  }

  return {
    /** Si todavía no hay usuarios, quien se registre primero será el administrador. */
    async estadoRegistro(): R<{ hayUsuarios: boolean }> {
      return ok({ hayUsuarios: a.usuarios.contar() > 0 });
    },

    /** Registro público (RF-S01): el primero queda administrador; el resto, pendiente de aprobación. */
    async registrar(n: Omit<NuevoUsuario, "rol">): R<Usuario> {
      const datos = await datosValidos(n);
      if (!datos.ok) return datos;
      return a.transaccion(() => {
        const u = registrar(a.usuarios.contar(), a.usuarios.porEmail(datos.valor.email) !== undefined, datos.valor, d.reloj.ahora());
        if (u.ok) a.usuarios.guardar(u.valor);
        return u;
      });
    },

    async iniciarSesion(correo: string, clave: string): R<{ token: string; usuario: Usuario }> {
      const e = email(correo);
      const u = e.ok ? a.usuarios.porEmail(e.valor) : undefined;
      const correcta = await d.claves.verificar(clave, u?.hashClave ?? HASH_FICTICIO);
      const t = d.secretos.token();
      const s = ingresar(u, correcta && u !== undefined, t.hash, d.reloj.ahora());
      if (!s.ok) return s;
      a.sesiones.guardar(s.valor);
      return ok({ token: t.token, usuario: u! });
    },

    async cerrarSesion(token: string): R<null> {
      a.sesiones.borrar(d.secretos.hashDeToken(token));
      return ok(null);
    },

    /** El usuario dueño del token, si la sesión sigue vigente. */
    async sesionActual(token: string | undefined): R<Usuario> {
      if (token === undefined) return err({ tipo: "SesionInvalida" });
      const s = a.sesiones.porHash(d.secretos.hashDeToken(token));
      return validarSesion(s, s && a.usuarios.porId(s.usuarioId), d.reloj.ahora());
    },

    async listarUsuarios(actor: Usuario): R<readonly Usuario[]> {
      const por = autorizar(actor, "gestionar-usuarios");
      if (!por.ok) return por;
      return ok(a.usuarios.listar());
    },

    async crearUsuario(actor: Usuario, n: NuevoUsuario): R<Usuario> {
      const por = autorizar(actor, "gestionar-usuarios");
      if (!por.ok) return por;
      const datos = await datosValidos(n);
      if (!datos.ok) return datos;
      return a.transaccion(() => {
        const u = crearUsuario(por.valor, a.usuarios.porEmail(datos.valor.email) !== undefined, { ...datos.valor, rol: n.rol }, d.reloj.ahora());
        if (u.ok) a.usuarios.guardar(u.valor);
        return u;
      });
    },

    /** Aprobar, rechazar, activar, desactivar o cambiar el rol de otro usuario. */
    async actualizarUsuario(actor: Usuario, id: UsuarioId, cambio: CambioUsuario): R<Usuario> {
      const por = autorizar(actor, "gestionar-usuarios");
      if (!por.ok) return por;
      return a.transaccion(() => {
        const objetivo = encontrado(a.usuarios.porId(id), { tipo: "UsuarioNoEncontrado" });
        if (!objetivo.ok) return objetivo;
        const u = actualizarUsuario(por.valor, objetivo.valor, cambio);
        if (!u.ok) return u;
        a.usuarios.guardar(u.valor);
        if (u.valor.estado !== "Activo") a.sesiones.borrarDeUsuario(id);
        return u;
      });
    },
  };
}
