import { describe, expect, it } from "vitest";
import { leerSalida } from "./salida";

const SALIDA = `In file included from src/a.cpp:1:
./src/a.cpp:13:10: warning: Uso de una referencia posiblemente invalidada: 'std::vector::push_back' (línea 12) si la capacidad está agotada reubica los elementos [ucsm.ContainerInvalidation]
   13 |   return x;
      |          ^
./src/a.cpp:11:12: note: El handle al elemento se obtiene de 'std::vector::operator[]'
./src/a.cpp:12:3: note: El handle al elemento puede quedar invalidado por 'std::vector::push_back'
src/a.cpp:20:5: warning: Called C++ object pointer is null [core.CallAndMessage]
src/a.cpp:19:5: note: Assuming 'p' is null
src/a.cpp:7:10: warning: Uso de una referencia invalidada: 'std::vector::clear' (línea 6) lo invalidó [ucsm.ContainerInvalidation]
2 warnings generated.
`;

describe("lectura de la salida de clang", () => {
  const avisos = leerSalida(SALIDA);
  it("toma solo los avisos del checker, con su clase", () => {
    expect(avisos.map((a) => [a.archivo, a.linea, a.columna, a.clase])).toEqual([
      ["src/a.cpp", 13, 10, "Posible"],
      ["src/a.cpp", 7, 10, "Confirmado"],
    ]);
  });
  it("las notas siguientes son la ruta del aviso; las de otros checkers no", () => {
    expect(avisos[0]?.ruta.map((n) => n.linea)).toEqual([11, 12]);
    expect(avisos[1]?.ruta).toEqual([]);
  });
  it("una salida sin avisos da una lista vacía", () => {
    expect(leerSalida("")).toEqual([]);
  });
});
