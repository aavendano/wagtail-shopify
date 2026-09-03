import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "node:path";

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: path.resolve(__dirname, "../static/cms_ui"),
    emptyOutDir: true,
    manifest: false,
    rollupOptions: {
      input: {
        "spa-public": path.resolve(__dirname, "src/spa-public.jsx"),
        editor: path.resolve(__dirname, "src/editor.jsx"),
      },
      output: {
        entryFileNames: "[name].js",
        chunkFileNames: "chunks/[name]-[hash].js",
        assetFileNames: (assetInfo) => {
          if (assetInfo.name && assetInfo.name.endsWith(".css")) {
            const base = assetInfo.name.replace(/\.css$/, "");
            if (base.includes("spa-public") || base === "style") {
              return "spa-public.css";
            }
            if (base.includes("editor")) {
              return "editor.css";
            }
          }
          return "assets/[name]-[hash][extname]";
        },
      },
    },
  },
});
