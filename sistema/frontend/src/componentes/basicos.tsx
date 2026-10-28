// Piezas de interfaz sin lógica de negocio: insignia, campo, aviso, avatar, estado de carga.
import { useId, type InputHTMLAttributes, type ReactNode } from "react";
import { mensajeDe, type ErrorApi } from "../dominio/errores";
import type { Tono } from "../dominio/revisiones";
import { iniciales } from "../dominio/usuarios";
import type { Carga } from "../estado/carga";
import { Icono, type NombreIcono } from "./iconos";

export function Insignia({ tono, icono, children }: { tono: Tono; icono?: NombreIcono; children: ReactNode }) {
  return (
    <span className={`insignia insignia-${tono}`}>
      {icono && <Icono nombre={icono} tamano={14} />}
      {children}
    </span>
  );
}

export function Avatar({ nombre }: { nombre: string }) {
  return (
    <span className="avatar" aria-hidden="true">
      {iniciales(nombre)}
    </span>
  );
}

export function Logo() {
  return (
    <span className="logo">
      <span className="logo-marca">
        <Icono nombre="escudo" />
      </span>
      <strong>Centinela</strong>
      <code>C++</code>
    </span>
  );
}

export function Alerta({ tono = "peligro", children }: { tono?: "peligro" | "info" | "exito"; children: ReactNode }) {
  const icono: NombreIcono = tono === "peligro" ? "alerta" : tono === "exito" ? "checkCirculo" : "info";
  return (
    <div className={`alerta alerta-${tono}`} role={tono === "peligro" ? "alert" : "status"}>
      <Icono nombre={icono} />
      <div>{children}</div>
    </div>
  );
}

type PropsCampo = { etiqueta: string; error?: string | undefined; ayuda?: ReactNode } & Omit<InputHTMLAttributes<HTMLInputElement>, "id">;

/** Un campo con su etiqueta y su error, enlazados para lectores de pantalla. */
export function Campo({ etiqueta, error, ayuda, ...input }: PropsCampo) {
  const id = useId();
  return (
    <div className="campo">
      <label htmlFor={id}>{etiqueta}</label>
      <input id={id} aria-invalid={error !== undefined} aria-describedby={error !== undefined ? `${id}-error` : undefined} {...input} />
      {ayuda}
      {error !== undefined && (
        <p className="campo-error" id={`${id}-error`}>
          {error}
        </p>
      )}
    </div>
  );
}

export function Selector<V extends string>({ etiqueta, valor, opciones, alCambiar, deshabilitado, oculta }: { etiqueta: string; valor: V; opciones: readonly { readonly valor: V; readonly texto: string }[]; alCambiar: (v: V) => void; deshabilitado?: boolean; oculta?: boolean }) {
  const id = useId();
  return (
    <span className="selector">
      <label htmlFor={id} className={oculta ? "solo-lector" : undefined}>
        {etiqueta}
      </label>
      <select id={id} value={valor} disabled={deshabilitado} onChange={(e) => alCambiar(opciones.find((o) => o.valor === e.target.value)?.valor ?? valor)}>
        {opciones.map((o) => (
          <option key={o.valor} value={o.valor}>
            {o.texto}
          </option>
        ))}
      </select>
    </span>
  );
}

/** Pinta una `Carga`: «Cargando…», el error con «Reintentar», o el contenido. */
export function SegunCarga<T>({ carga, reintentar, children }: { carga: Carga<T>; reintentar: () => void; children: (valor: T) => ReactNode }) {
  switch (carga.tipo) {
    case "Cargando":
      return (
        <p className="cargando" role="status">
          <Icono nombre="girar" /> Cargando…
        </p>
      );
    case "Error":
      return <ErrorCarga error={carga.error} reintentar={reintentar} />;
    case "Listo":
      return <>{children(carga.valor)}</>;
  }
}

export function ErrorCarga({ error, reintentar }: { error: ErrorApi; reintentar: () => void }) {
  return (
    <div className="error-carga">
      <Alerta>{mensajeDe(error)}</Alerta>
      <button type="button" className="boton" onClick={reintentar}>
        <Icono nombre="girar" /> Reintentar
      </button>
    </div>
  );
}

export function Vacio({ titulo, children }: { titulo: string; children?: ReactNode }) {
  return (
    <div className="vacio">
      <strong>{titulo}</strong>
      {children}
    </div>
  );
}
