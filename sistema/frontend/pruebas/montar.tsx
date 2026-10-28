// Monta el panel entero (rutas, guardias, avisos) en una ruta dada, con la API y el reloj que pase la prueba.
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter, useLocation } from "react-router";
import type { Api } from "../src/api/puerto";
import { App } from "../src/App";
import { ProveedorAvisos } from "../src/componentes/avisos";
import { Proveedor, type Reloj } from "../src/estado/contexto";

function Ubicacion() {
  const { pathname } = useLocation();
  return <output data-testid="ubicacion">{pathname}</output>;
}

export function montar(ruta: string, api: Api, reloj?: Reloj) {
  const usuario = userEvent.setup();
  const r = render(
    <Proveedor api={api} intervaloMs={30} {...(reloj ? { reloj } : {})}>
      <ProveedorAvisos duracionMs={60_000}>
        <MemoryRouter initialEntries={[ruta]}>
          <App />
          <Ubicacion />
        </MemoryRouter>
      </ProveedorAvisos>
    </Proveedor>,
  );
  return { ...r, usuario, ubicacion: () => screen.getByTestId("ubicacion").textContent };
}
