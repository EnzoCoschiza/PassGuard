import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

const repositoryName = process.env.GITHUB_REPOSITORY?.split("/")[1];
const shouldUseGitHubPagesBase = process.env.GITHUB_ACTIONS === "true" && repositoryName;

export default defineConfig({
  base: shouldUseGitHubPagesBase ? `/${repositoryName}/` : "/",
  plugins: [react()],
  server: {
    proxy: {
      "/health": "http://127.0.0.1:8000",
      "/password": "http://127.0.0.1:8000",
    },
  },
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: "./src/test/setup.ts",
  },
});
