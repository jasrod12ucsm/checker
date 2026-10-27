import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    include: ["paquetes/**/*.test.ts", "pruebas/**/*.test.ts"],
    exclude: ["**/node_modules/**", "frontend/**"],
    coverage: {
      provider: "v8",
      include: ["paquetes/**/src/**/*.ts"],
      exclude: ["**/*.test.ts", "paquetes/app/src/principal.ts"],
      reporter: ["text-summary", "json-summary"],
      thresholds: { lines: 90, functions: 90, branches: 80 },
    },
  },
});
