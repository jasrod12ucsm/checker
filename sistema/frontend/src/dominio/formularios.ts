// Validación de los formularios antes de enviarlos. Junta todos los errores a la vez (validación aplicativa),
// con las mismas reglas que el servicio; el servicio sigue siendo quien decide.
import { err, ok, type Resultado } from "./resultado";
import type { Politica, Rol } from "./modelo";

export type ErroresDe<C extends string> = Partial<Record<C, string>>;

/** Las dos reglas de la clave (RN del servicio: al menos 10 caracteres, con letras y números), para mostrarlas en vivo. */
export function reglasClave(clave: string) {
  return { largo: clave.length >= 10 && clave.length <= 128, letrasYNumeros: /[A-Za-z]/.test(clave) && /[0-9]/.test(clave) };
}

const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function validarCuenta(email: string, nombre: string, clave: string): ErroresDe<"email" | "nombre" | "clave"> {
  const e: ErroresDe<"email" | "nombre" | "clave"> = {};
  if (!EMAIL.test(email.trim()) || email.trim().length > 254) e.email = "Escribe un correo válido.";
  if (nombre.trim().length === 0) e.nombre = "Escribe tu nombre.";
  else if (nombre.trim().length > 100) e.nombre = "El nombre puede tener hasta 100 caracteres.";
  const r = reglasClave(clave);
  if (!r.largo) e.clave = "La clave debe tener al menos 10 caracteres.";
  else if (!r.letrasYNumeros) e.clave = "La clave debe tener letras y números.";
  return e;
}

const sinErrores = <C extends string>(e: ErroresDe<C>) => Object.keys(e).length === 0;

export interface DatosRegistro {
  readonly email: string;
  readonly nombre: string;
  readonly clave: string;
}

export function validarRegistro(f: DatosRegistro & { readonly confirmacion: string }): Resultado<DatosRegistro, ErroresDe<"email" | "nombre" | "clave" | "confirmacion">> {
  const e: ErroresDe<"email" | "nombre" | "clave" | "confirmacion"> = validarCuenta(f.email, f.nombre, f.clave);
  if (f.confirmacion !== f.clave) e.confirmacion = "Las claves no coinciden.";
  return sinErrores(e) ? ok({ email: f.email.trim(), nombre: f.nombre.trim(), clave: f.clave }) : err(e);
}

export interface DatosIngreso {
  readonly email: string;
  readonly clave: string;
}

export function validarIngreso(f: DatosIngreso): Resultado<DatosIngreso, ErroresDe<"email" | "clave">> {
  const e: ErroresDe<"email" | "clave"> = {};
  if (f.email.trim().length === 0) e.email = "Escribe tu correo.";
  if (f.clave.length === 0) e.clave = "Escribe tu clave.";
  return sinErrores(e) ? ok({ email: f.email.trim(), clave: f.clave }) : err(e);
}

export interface DatosNuevoUsuario extends DatosRegistro {
  readonly rol: Rol;
}

export function validarNuevoUsuario(f: DatosNuevoUsuario): Resultado<DatosNuevoUsuario, ErroresDe<"email" | "nombre" | "clave">> {
  const e = validarCuenta(f.email, f.nombre, f.clave);
  return sinErrores(e) ? ok({ email: f.email.trim(), nombre: f.nombre.trim(), clave: f.clave, rol: f.rol }) : err(e);
}

/** `dueño/repositorio` de GitHub: letras, números, `-`, `_` y `.`. Acepta también la URL del repositorio. */
export function nombreRepositorio(texto: string): Resultado<string, string> {
  const limpio = texto
    .trim()
    .replace(/^https?:\/\/github\.com\//i, "")
    .replace(/\.git$/i, "")
    .replace(/\/+$/, "");
  return /^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})\/[A-Za-z0-9._-]{1,100}$/.test(limpio)
    ? ok(limpio)
    : err("Escribe el repositorio como dueño/nombre, por ejemplo lab-sistemas/motor-rutas.");
}

export interface DatosRepositorio {
  readonly nombre: string;
  readonly politica: Politica;
  readonly bloquearMerge: boolean;
}

/** Número de pull request para «Revisar un PR ahora»: entero positivo. */
export function numeroPr(texto: string): Resultado<number, string> {
  const n = Number(texto.trim().replace(/^#/, ""));
  return Number.isInteger(n) && n > 0 ? ok(n) : err("Escribe el número del pull request, por ejemplo 214.");
}
