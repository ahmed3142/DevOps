import { defineConfig } from "vitest/config";
import path from "node:path";

export default defineConfig({
  test: {
    environment: "node",
    include: ["tests/**/*.test.ts"],
  },
  resolve: {
    alias: {
      // Mirror the "@/*" path alias from tsconfig.json.
      "@": path.resolve(__dirname),
    },
  },
});
