// El servicio de verdad para las pruebas del panel: Fastify (rutas, cookies, validación, códigos) + los casos de uso
// reales. El almacén es el doble en memoria (SQLite tiene sus propias pruebas en el servicio); GitHub, clang y el hash
// de claves también son dobles (los de `sistema/pruebas/dobles.ts`). El panel le habla con
// su propio adaptador HTTP (`apiHttp`) a través de un `fetch` que entra por `app.inject` y guarda la cookie.
import type { Positivo } from "@centinela/kernel";
import { producto } from "@centinela/producto";
import { crearServidor } from "@centinela/http";
import type { Aviso } from "@centinela/revisiones";
import { dependencias } from "../../pruebas/dobles";
import { apiHttp, type Fetch } from "../src/api/http";
import type { Reloj } from "../src/estado/contexto";

export const CLAVE = "clave12345678";

export function servicio() {
  const t = dependencias();
  const p = producto(t.deps);
  const app = crearServidor(p, { urlPublica: "https://centinela.ucsm.edu.pe", cookieSegura: false });

  /** Un navegador: su propio frasco de cookies contra el mismo servicio. */
  function navegador() {
    let cookie = "";
    const fetch: Fetch = async (url, init) => {
      const headers = { ...(init.headers as Record<string, string>), ...(cookie === "" ? {} : { cookie }) };
      const r = await app.inject({ method: (init.method ?? "GET") as "GET", url, headers, ...(typeof init.body === "string" ? { payload: init.body } : {}) });
      for (const c of r.cookies) if (c.name === "centinela_sesion") cookie = c.value === "" ? "" : `${c.name}=${c.value}`;
      return new Response(r.statusCode === 204 ? null : r.body, { status: r.statusCode, headers: { "content-type": String(r.headers["content-type"] ?? "application/json") } });
    };
    return { api: apiHttp(fetch), olvidar: () => void (cookie = "") };
  }

  const reloj: Reloj = { ahora: () => t.reloj.ahora() };

  async function registrar(email: string, nombre: string) {
    const r = await p.identidad.registrar({ email, nombre, clave: CLAVE });
    if (!r.ok) throw new Error(JSON.stringify(r.error));
    return r.valor;
  }

  /** Un navegador que ya ingresó con esa cuenta. */
  async function conSesion(email: string) {
    const n = navegador();
    const r = await n.api.ingresar({ email, clave: CLAVE });
    if (!r.ok) throw new Error(JSON.stringify(r.error));
    return { ...n, usuario: r.valor };
  }

  /** El PR que GitHub (doble) devuelve, el archivo que cambió y lo que el checker (doble) avisa. */
  function prEnGitHub(numero: number, titulo: string, sha: string, avisos: readonly Aviso[] = []) {
    t.github.prs.set(numero, { numero: numero as Positivo, titulo, autor: "ana-dev", shaCabeza: sha });
    t.github.archivos = [...new Set(avisos.map((a) => a.archivo).concat("src/cache.cpp"))].map((ruta) => ({ ruta, eliminado: false, lineas: new Set([10, 15, 16, 17, 24]) }));
    t.analizador.avisos = [...avisos];
  }

  /** Procesa la cola como lo haría el trabajador. */
  async function trabajar() {
    while (await p.revisiones.procesarSiguiente());
  }

  return { t, p, app, reloj, navegador, registrar, conSesion, prEnGitHub, trabajar };
}

export type Servicio = ReturnType<typeof servicio>;

const pos = (n: number) => n as Positivo;

/** Los dos avisos de la demostración (libro, «API HTTP»): un posible y un confirmado en `src/cache.cpp`. */
export const AVISOS_DEMO: readonly Aviso[] = [
  {
    archivo: "src/cache.cpp",
    linea: pos(17),
    columna: pos(12),
    clase: "Posible",
    mensaje: "Uso de una referencia posiblemente invalidada: 'std::vector::push_back' (línea 16) si la capacidad está agotada reubica los elementos",
    ruta: [
      { archivo: "src/cache.cpp", linea: pos(15), mensaje: "El handle al elemento se obtiene de 'std::vector::operator[]'" },
      { archivo: "src/cache.cpp", linea: pos(16), mensaje: "Puede quedar invalidado por 'std::vector::push_back'" },
      { archivo: "src/cache.cpp", linea: pos(17), mensaje: "Uso" },
    ],
  },
  {
    archivo: "src/cache.cpp",
    linea: pos(24),
    columna: pos(52),
    clase: "Confirmado",
    mensaje: "Uso de una referencia invalidada: 'std::vector::clear' (línea 10) lo invalidó",
    ruta: [
      { archivo: "src/cache.cpp", linea: pos(10), mensaje: "Invalidado por 'std::vector::clear'" },
      { archivo: "src/cache.cpp", linea: pos(24), mensaje: "Uso" },
    ],
  },
];
