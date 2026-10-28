import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

// En desarrollo (`npm run dev`) la API es el servicio en :8080; en producción Fastify sirve `dist/`.
export default defineConfig({
  plugins: [react()],
  server: { proxy: { "/api": "http://127.0.0.1:8080" } },
  test: {
    environment: "jsdom",
    setupFiles: ["pruebas/preparar.ts"],
    include: ["src/**/*.test.{ts,tsx}", "pruebas/**/*.test.{ts,tsx}"],
    coverage: {
      provider: "v8",
      include: ["src/**/*.{ts,tsx}"],
      exclude: ["**/*.test.{ts,tsx}", "src/main.tsx"],
      reporter: ["text-summary", "json-summary"],
      thresholds: { lines: 90, functions: 90, branches: 80 },
    },
  },
});
