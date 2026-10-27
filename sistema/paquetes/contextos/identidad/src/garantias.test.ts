// Garantías de tipos: cada `@ts-expect-error` debe ser un error de compilación.
import { it } from "vitest";
import { desenvolver, instante, type Email, type Texto, type UsuarioId } from "@centinela/kernel";
import { Autorizado, actualizarUsuario, crearUsuario, type HashClave, type Usuario } from "./index";

it("solo Autorizado.para da un testigo de autorización", () => {
  const admin: Usuario = { id: "00000000-0000-4000-8000-000000000001" as UsuarioId, email: "a@b.co" as Email, nombre: "A" as Texto, rol: "administrador", hashClave: "h" as HashClave, estado: "Activo", creadoEn: instante(0) };
  // @ts-expect-error el constructor es privado
  new Autorizado(admin.id, "gestionar-usuarios");
  // @ts-expect-error un objeto con la misma forma no es un testigo
  const falso: Autorizado<"gestionar-usuarios"> = { usuarioId: admin.id, permiso: "gestionar-usuarios" };
  const consultar = desenvolver(Autorizado.para(admin, "consultar-revisiones"));
  const datos = { id: admin.id, email: admin.email, nombre: admin.nombre, rol: "desarrollador" as const, hashClave: admin.hashClave };
  // @ts-expect-error el permiso de consultar no sirve para crear usuarios
  crearUsuario(consultar, false, datos, instante(0));
  void falso;
});

it("ningún administrador puede devolver una cuenta a Pendiente", () => {
  const admin: Usuario = { id: "00000000-0000-4000-8000-000000000001" as UsuarioId, email: "a@b.co" as Email, nombre: "A" as Texto, rol: "administrador", hashClave: "h" as HashClave, estado: "Activo", creadoEn: instante(0) };
  const por = desenvolver(Autorizado.para(admin, "gestionar-usuarios"));
  // @ts-expect-error Pendiente no es una decisión: solo lo asigna el registro
  actualizarUsuario(por, admin, { estado: "Pendiente" });
});
