import { expect, it } from "vitest";
import { lineasDelParche } from "./parche";

it("cuenta las líneas agregadas y de contexto del lado nuevo, no las borradas", () => {
  const p = ["@@ -1,3 +1,4 @@", " a", "-b", "+B", "+B2", " c", "@@ -20,2 +21,2 @@", " x", "+y", "\\ No newline at end of file"].join("\n");
  expect([...lineasDelParche(p)]).toEqual([1, 2, 3, 4, 21, 22]);
});

it("un archivo binario no trae parche y no tiene líneas comentables", () => {
  expect(lineasDelParche(undefined).size).toBe(0);
});
