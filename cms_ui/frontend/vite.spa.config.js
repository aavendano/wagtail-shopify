import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "node:path";

/** Polaris CMS embed: one JS file (no chunks) so Shopify iframe never 404s lazy imports. */
export default defineConfig({
  base: "/static/cms_ui/",
  plugins: [react()],
  build: {
    outDir: path.resolve(__dirname, "../static/cms_ui"),
    emptyOutDir: false,
    manifest: false,
    cssCodeSplit: false,
    rollupOptions: {
      input: path.resolve(__dirname, "src/spa-public.jsx"),
      output: {
        entryFileNames: "cms-embedded.js",
        inlineDynamicImports: true,
        assetFileNames: (assetInfo) => {
          if (assetInfo.name && assetInfo.name.endsWith(".css")) {
            return "cms-embedded.css";
          }
          return "assets/[name]-[hash][extname]";
        },
      },
    },
  },
});
