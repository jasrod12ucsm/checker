import { createHash, createHmac, randomBytes, scrypt, timingSafeEqual, type ScryptOptions } from "node:crypto";
import type { HashClave, HashToken } from "@centinela/identidad";
import type { SecretoWebhook } from "@centinela/repositorios";
import type { Claves, Secretos } from "@centinela/producto";

const PARAMS: ScryptOptions = { N: 16384, r: 8, p: 1 };
const LARGO = 64;

const derivar = (clave: string, sal: Buffer) =>
  new Promise<Buffer>((ok, mal) => scrypt(clave, sal, LARGO, PARAMS, (e, k) => (e ? mal(e) : ok(k))));

/** Claves con scrypt: `scrypt$<sal base64>$<clave derivada base64>`. */
export const claves: Claves = {
  async hashear(clave) {
    const sal = randomBytes(16);
    return `scrypt$${sal.toString("base64")}$${(await derivar(clave, sal)).toString("base64")}` as HashClave;
  },
  async verificar(clave, hash) {
    const [alg, sal, k] = hash.split("$");
    if (alg !== "scrypt" || !sal || !k) return false;
    const esperado = Buffer.from(k, "base64");
    const obtenido = await derivar(clave, Buffer.from(sal, "base64"));
    return esperado.length === obtenido.length && timingSafeEqual(esperado, obtenido);
  },
};

const sha256 = (s: string) => createHash("sha256").update(s).digest("hex");

export const secretos: Secretos = {
  token() {
    const token = randomBytes(32).toString("base64url");
    return { token, hash: sha256(token) as HashToken };
  },
  hashDeToken: (token) => sha256(token) as HashToken,
  secretoWebhook: () => randomBytes(24).toString("hex") as SecretoWebhook,
  firmaValida(secreto, cuerpo, firma) {
    if (firma === undefined || !firma.startsWith("sha256=")) return false;
    const esperada = Buffer.from(`sha256=${createHmac("sha256", secreto).update(cuerpo).digest("hex")}`);
    const recibida = Buffer.from(firma);
    return esperada.length === recibida.length && timingSafeEqual(esperada, recibida);
  },
};

/** Firma como la calcula GitHub; la usan las pruebas y el script de demostración. */
export const firmar = (secreto: string, cuerpo: string) => `sha256=${createHmac("sha256", secreto).update(cuerpo).digest("hex")}`;
