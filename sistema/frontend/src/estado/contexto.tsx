// Las dependencias de las pantallas viajan por contexto de React: la API (inyectada por `main.tsx` o la prueba),
// la sesión y el reloj. Ninguna pantalla crea su propia API ni lee `Date.now()` directamente.
import { createContext, useCallback, useContext, useMemo, useState, type ReactNode } from "react";
import type { Api } from "../api/puerto";
import type { Usuario } from "../dominio/modelo";

export interface Reloj {
  ahora(): number;
}

export const relojDelSistema: Reloj = { ahora: () => Date.now() };

/** La sesión del panel: se sabe o no se sabe todavía; si se sabe, hay usuario o no lo hay. */
export type EstadoSesion = { readonly tipo: "Consultando" } | { readonly tipo: "Anonima"; readonly aviso?: string } | { readonly tipo: "Iniciada"; readonly usuario: Usuario };

interface Contexto {
  readonly api: Api;
  readonly reloj: Reloj;
  readonly sesion: EstadoSesion;
  /** Cada cuánto se vuelve a pedir lo que sigue en curso (una revisión pendiente o en análisis). */
  readonly intervaloMs: number;
  /** Pone la sesión después de ingresar o de consultarla; `null` la deja anónima. */
  fijarUsuario(u: Usuario | null, aviso?: string): void;
}

const Ctx = createContext<Contexto | null>(null);

export function Proveedor({ api, reloj = relojDelSistema, intervaloMs = 3000, inicial = { tipo: "Consultando" }, children }: { api: Api; reloj?: Reloj; intervaloMs?: number; inicial?: EstadoSesion; children: ReactNode }) {
  const [sesion, setSesion] = useState<EstadoSesion>(inicial);
  const fijarUsuario = useCallback((u: Usuario | null, aviso?: string) => setSesion(u === null ? (aviso === undefined ? { tipo: "Anonima" } : { tipo: "Anonima", aviso }) : { tipo: "Iniciada", usuario: u }), []);
  const valor = useMemo(() => ({ api, reloj, sesion, intervaloMs, fijarUsuario }), [api, reloj, sesion, intervaloMs, fijarUsuario]);
  return <Ctx.Provider value={valor}>{children}</Ctx.Provider>;
}

function useCtx(): Contexto {
  const c = useContext(Ctx);
  if (c === null) throw new Error("Falta <Proveedor> alrededor del panel");
  return c;
}

export const useApi = (): Api => useCtx().api;
export const useReloj = (): Reloj => useCtx().reloj;
export const useIntervalo = (): number => useCtx().intervaloMs;
export function useSesion() {
  const { sesion, fijarUsuario } = useCtx();
  return { sesion, fijarUsuario };
}

/** El usuario de una pantalla protegida. Solo se usa bajo `RequiereSesion`, que ya garantizó que existe. */
export function useUsuario(): Usuario {
  const { sesion } = useCtx();
  if (sesion.tipo !== "Iniciada") throw new Error("useUsuario fuera de una ruta protegida");
  return sesion.usuario;
}
