// Raíz de composición: el único lugar que conoce todos los adaptadores y los conecta.
import { mkdirSync } from "node:fs";
import { dirname } from "node:path";
import { randomUUID } from "node:crypto";
import { instante } from "@centinela/kernel";
import { producto, type Bitacora, type Dependencias } from "@centinela/producto";
import { abrirAlmacen } from "@centinela/sqlite";
import { claves, secretos } from "@centinela/cripto";
import { clienteGitHub } from "@centinela/github";
import { analizadorClang, OPCIONES_CLANG } from "@centinela/analizador";
import { crearServidor } from "@centinela/http";
import type { Configuracion } from "./configuracion";

const bitacora: Bitacora = {
  info: (msg, datos) => console.log(JSON.stringify({ nivel: "info", msg, ...datos })),
  error: (msg, datos) => console.error(JSON.stringify({ nivel: "error", msg, ...datos })),
};

export function componer(c: Configuracion, sobre: Partial<Dependencias> = {}) {
  if (c.CENTINELA_BD !== ":memory:") mkdirSync(dirname(c.CENTINELA_BD), { recursive: true });
  const almacen = abrirAlmacen(c.CENTINELA_BD);
  const github = clienteGitHub({ api: c.CENTINELA_GITHUB_API, token: c.CENTINELA_GITHUB_TOKEN });
  const deps: Dependencias = {
    almacen,
    claves,
    secretos,
    github,
    fuentes: github,
    analizador: analizadorClang({
      ...OPCIONES_CLANG,
      clang: c.CENTINELA_CLANG,
      plugin: c.CENTINELA_PLUGIN,
      paralelo: c.CENTINELA_PARALELO,
      tiempoMaximoMs: c.CENTINELA_TIEMPO_MAXIMO_S * 1000,
    }),
    reloj: { ahora: () => instante(Date.now()) },
    ids: { nuevo: randomUUID },
    bitacora,
    urlPublica: c.CENTINELA_URL_PUBLICA,
    ...sobre,
  };
  const p = producto(deps);
  const servidor = crearServidor(p, {
    urlPublica: c.CENTINELA_URL_PUBLICA,
    cookieSegura: c.CENTINELA_COOKIE_SEGURA,
    ...(c.CENTINELA_FRONTEND === undefined ? {} : { frontend: c.CENTINELA_FRONTEND }),
  });

  let detenido = false;
  let enCurso: Promise<void> = Promise.resolve();
  /** El trabajador: procesa la cola mientras haya trabajos; si está vacía, espera el intervalo. */
  function trabajar() {
    enCurso = (async () => {
      while (!detenido) {
        let hubo = false;
        try {
          hubo = await p.revisiones.procesarSiguiente();
        } catch (e) {
          bitacora.error("el trabajador falló", { error: String(e) });
        }
        if (!hubo) await new Promise((ok) => setTimeout(ok, c.CENTINELA_INTERVALO_MS));
      }
    })();
  }

  async function arrancar() {
    const n = p.revisiones.recuperarInterrumpidas();
    if (n > 0) bitacora.info("revisiones interrumpidas marcadas como fallidas", { n });
    await servidor.listen({ port: c.CENTINELA_PUERTO, host: c.CENTINELA_HOST });
    trabajar();
    bitacora.info("Centinela C++ escuchando", { url: c.CENTINELA_URL_PUBLICA, puerto: c.CENTINELA_PUERTO });
  }

  async function detener() {
    detenido = true;
    await servidor.close();
    await enCurso;
    almacen.cerrar();
  }

  return { producto: p, servidor, arrancar, detener };
}
