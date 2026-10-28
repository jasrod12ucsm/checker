// Íconos de trazo (24×24, `currentColor`), dibujados aquí para no traer una librería por veinte figuras.
import type { ReactNode } from "react";

const TRAZOS = {
  escudo: <path d="M12 3l8 3v6c0 4.5-3.4 8.3-8 9-4.6-.7-8-4.5-8-9V6l8-3z M9 12l2 2 4-4" />,
  lista: <path d="M9 6h11 M9 12h11 M9 18h11 M4 6h.01 M4 12h.01 M4 18h.01" />,
  libro: <path d="M5 4h11a2 2 0 012 2v14H7a2 2 0 01-2-2V4z M5 18a2 2 0 012-2h11" />,
  usuarios: <path d="M16 20v-1a4 4 0 00-4-4H7a4 4 0 00-4 4v1 M9.5 11a3.5 3.5 0 100-7 3.5 3.5 0 000 7z M21 20v-1a4 4 0 00-3-3.9 M16 4.1a3.5 3.5 0 010 6.8" />,
  salir: <path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4 M16 17l5-5-5-5 M21 12H9" />,
  externo: <path d="M14 4h6v6 M20 4l-9 9 M18 14v5a1 1 0 01-1 1H5a1 1 0 01-1-1V7a1 1 0 011-1h5" />,
  reloj: <path d="M12 21a9 9 0 100-18 9 9 0 000 18z M12 7v5l3 2" />,
  alerta: <path d="M12 21a9 9 0 100-18 9 9 0 000 18z M12 8v4 M12 16h.01" />,
  triangulo: <path d="M10.3 3.9L2 18a2 2 0 001.7 3h16.6a2 2 0 001.7-3L13.7 3.9a2 2 0 00-3.4 0z M12 9v4 M12 17h.01" />,
  check: <path d="M5 12l5 5L20 7" />,
  checkCirculo: <path d="M12 21a9 9 0 100-18 9 9 0 000 18z M8.5 12l2.5 2.5 4.5-5" />,
  equis: <path d="M6 6l12 12 M18 6L6 18" />,
  equisCirculo: <path d="M12 21a9 9 0 100-18 9 9 0 000 18z M9 9l6 6 M15 9l-6 6" />,
  girar: <path d="M20 12a8 8 0 11-2.3-5.7L20 8.6 M20 4v4.6h-4.6" />,
  candado: <path d="M6 11h12v9H6z M8 11V8a4 4 0 018 0v3" />,
  archivo: <path d="M14 3H7a2 2 0 00-2 2v14a2 2 0 002 2h10a2 2 0 002-2V8l-5-5z M14 3v5h5" />,
  prohibido: <path d="M12 21a9 9 0 100-18 9 9 0 000 18z M5.6 5.6l12.8 12.8" />,
  mas: <path d="M12 5v14 M5 12h14" />,
  lapiz: <path d="M4 20h4L19 9l-4-4L4 16v4z" />,
  ojo: <path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z M12 15a3 3 0 100-6 3 3 0 000 6z" />,
  copiar: <path d="M9 9h11v11H9z M5 15H4V4h11v1" />,
  desconectar: <path d="M9 15l-3 3a3 3 0 01-4.2-4.2l3-3 M15 9l3-3a3 3 0 014.2 4.2l-3 3 M3 3l18 18" />,
  play: <path d="M7 4l13 8-13 8V4z" />,
  info: <path d="M12 21a9 9 0 100-18 9 9 0 000 18z M12 11v5 M12 8h.01" />,
  agregarUsuario: <path d="M14 20v-1a4 4 0 00-4-4H6a4 4 0 00-4 4v1 M8 11a3.5 3.5 0 100-7 3.5 3.5 0 000 7z M19 8v6 M16 11h6" />,
} satisfies Record<string, ReactNode>;

export type NombreIcono = keyof typeof TRAZOS;

export function Icono({ nombre, tamano = 16 }: { nombre: NombreIcono; tamano?: number }) {
  return (
    <svg className="icono" width={tamano} height={tamano} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      {TRAZOS[nombre]}
    </svg>
  );
}
