// Garantías de tipos (equivalente a los compile_fail de Rust): cada `@ts-expect-error`
// DEBE ser un error de compilación; si deja de serlo, `npm run tipos` falla.
import { it } from "vitest";
import { email, desenvolver, type Email, type RevisionId, type UsuarioId } from "./index";

it("las marcas impiden mezclar valores", () => {
  // @ts-expect-error un string cualquiera no es un Email
  const e: Email = "ana@ejemplo.com";
  const bueno: Email = desenvolver(email("ana@ejemplo.com"));
  const u = "8f14e45f-ceea-4e7a-9b1d-3c1c2b9a0d11" as UsuarioId;
  // @ts-expect-error un UsuarioId no es un RevisionId
  const r: RevisionId = u;
  void [e, bueno, r];
});
