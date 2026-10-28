// Cargar datos para una pantalla. El estado es una unión con nombre, no tres `boolean` que pueden contradecirse.
import { useCallback, useEffect, useRef, useState } from "react";
import type { ErrorApi } from "../dominio/errores";
import type { Resultado } from "../dominio/resultado";
import { useSesion } from "./contexto";

export type Carga<T> = { readonly tipo: "Cargando" } | { readonly tipo: "Error"; readonly error: ErrorApi } | { readonly tipo: "Listo"; readonly valor: T };

/**
 * Si cualquier llamada responde que la sesión venció, el panel vuelve al ingreso con ese aviso.
 * Devuelve el mismo resultado para que la pantalla siga su camino.
 */
export function useVigilarSesion() {
  const { fijarUsuario } = useSesion();
  return useCallback(
    <T>(r: Resultado<T, ErrorApi>): Resultado<T, ErrorApi> => {
      if (!r.ok && r.error.tipo === "SinSesion") fijarUsuario(null, r.error.mensaje);
      return r;
    },
    [fijarUsuario],
  );
}

/**
 * Pide `cargar()` al montar y cada vez que cambian `claves`. `recargar(true)` vuelve a pedir sin mostrar «Cargando»
 * (la actualización sola de la lista); `fijar` cambia el valor local tras una escritura que ya devolvió el dato nuevo.
 */
export function useCarga<T>(cargar: () => Promise<Resultado<T, ErrorApi>>, claves: readonly unknown[]) {
  const [carga, setCarga] = useState<Carga<T>>({ tipo: "Cargando" });
  const vigilar = useVigilarSesion();
  const vigente = useRef(0);
  const cargarRef = useRef(cargar);
  cargarRef.current = cargar;

  const recargar = useCallback(
    async (callado = false) => {
      const n = ++vigente.current;
      if (!callado) setCarga({ tipo: "Cargando" });
      const r = vigilar(await cargarRef.current());
      // Una respuesta vieja que llega tarde no pisa a la nueva.
      if (n !== vigente.current) return;
      setCarga(r.ok ? { tipo: "Listo", valor: r.valor } : { tipo: "Error", error: r.error });
    },
    [vigilar],
  );

  useEffect(() => {
    void recargar();
    return () => {
      vigente.current++;
    };
  }, claves);

  const fijar = useCallback((f: (x: T) => T) => setCarga((c) => (c.tipo === "Listo" ? { tipo: "Listo", valor: f(c.valor) } : c)), []);
  return { carga, recargar, fijar };
}
