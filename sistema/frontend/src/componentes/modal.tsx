// Ventana modal accesible: `role="dialog"`, título enlazado, cierra con Escape o con la ✕, devuelve el foco al salir.
import { useEffect, useId, useRef, type ReactNode } from "react";
import { Icono } from "./iconos";

export function Modal({ titulo, alCerrar, pie, children }: { titulo: ReactNode; alCerrar: () => void; pie?: ReactNode; children: ReactNode }) {
  const id = useId();
  const caja = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const previo = document.activeElement as HTMLElement | null;
    caja.current?.querySelector<HTMLElement>("input, select, textarea, button:not(.modal-cerrar)")?.focus();
    const tecla = (e: KeyboardEvent) => {
      if (e.key === "Escape") alCerrar();
    };
    document.addEventListener("keydown", tecla);
    return () => {
      document.removeEventListener("keydown", tecla);
      previo?.focus();
    };
  }, [alCerrar]);
  return (
    <div className="modal-fondo" onMouseDown={(e) => e.target === e.currentTarget && alCerrar()}>
      <div className="modal" role="dialog" aria-modal="true" aria-labelledby={id} ref={caja}>
        <div className="modal-cuerpo">
          <button type="button" className="modal-cerrar" aria-label="Cerrar" onClick={alCerrar}>
            <Icono nombre="equis" />
          </button>
          <h2 id={id}>{titulo}</h2>
          {children}
        </div>
        {pie && <div className="modal-pie">{pie}</div>}
      </div>
    </div>
  );
}
