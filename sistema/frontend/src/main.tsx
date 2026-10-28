// Raíz de composición del panel: el único archivo que elige la implementación real de cada dependencia.
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router";
import { apiHttp } from "./api/http";
import { App } from "./App";
import { ProveedorAvisos } from "./componentes/avisos";
import { Proveedor } from "./estado/contexto";
import "./estilos.css";

const raiz = document.getElementById("raiz");
if (raiz === null) throw new Error("falta #raiz en index.html");

createRoot(raiz).render(
  <StrictMode>
    <Proveedor api={apiHttp()}>
      <ProveedorAvisos>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </ProveedorAvisos>
    </Proveedor>
  </StrictMode>,
);
