import { leerConfiguracion } from "./configuracion";
import { componer } from "./componer";

const sistema = componer(leerConfiguracion(process.env));
await sistema.arrancar();
for (const senal of ["SIGINT", "SIGTERM"] as const) {
  process.once(senal, () => {
    void sistema.detener().then(() => process.exit(0));
  });
}
