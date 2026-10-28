// Avisos breves («Se aprobó a …»): una cola pequeña que se vacía sola. `duracionMs` se puede fijar en las pruebas.
import { createContext, useCallback, useContext, useMemo, useRef, useState, type ReactNode } from "react";
import { Icono } from "./iconos";

interface Aviso {
  readonly id: number;
  readonly contenido: ReactNode;
  readonly tono: "exito" | "peligro";
}

const Ctx = createContext<(contenido: ReactNode, tono?: "exito" | "peligro") => void>(() => undefined);

export function ProveedorAvisos({ duracionMs = 5000, children }: { duracionMs?: number; children: ReactNode }) {
  const [avisos, setAvisos] = useState<readonly Aviso[]>([]);
  const siguiente = useRef(1);
  const quitar = useCallback((id: number) => setAvisos((xs) => xs.filter((a) => a.id !== id)), []);
  const avisar = useCallback(
    (contenido: ReactNode, tono: "exito" | "peligro" = "exito") => {
      const id = siguiente.current++;
      setAvisos((xs) => [...xs.slice(-2), { id, contenido, tono }]);
      setTimeout(() => quitar(id), duracionMs);
    },
    [duracionMs, quitar],
  );
  const valor = useMemo(() => avisar, [avisar]);
  return (
    <Ctx.Provider value={valor}>
      {children}
      <div className="avisos" aria-live="polite">
        {avisos.map((a) => (
          <div key={a.id} className={`aviso aviso-${a.tono}`} role="status">
            <Icono nombre={a.tono === "exito" ? "checkCirculo" : "alerta"} />
            <span>{a.contenido}</span>
            <button type="button" aria-label="Cerrar aviso" onClick={() => quitar(a.id)}>
              <Icono nombre="equis" />
            </button>
          </div>
        ))}
      </div>
    </Ctx.Provider>
  );
}

export const useAvisar = () => useContext(Ctx);
