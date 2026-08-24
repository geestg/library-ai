import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
    plugins: [react()],
    resolve: {
        extensions: [
            ".tsx",
            ".ts",
            ".jsx",
            ".js",
            ".mjs",
            ".mts",
            ".json",
        ],
    },
    server: {
        proxy: {
                "/chat": {
                    target: "http://127.0.0.1:8014",
                    changeOrigin: true,
                },
            "/api/repository": {
                target: "http://127.0.0.1:8014",
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api/, ""),
            },
            "/api/documents": {
                target: "http://127.0.0.1:8014",
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api/, ""),
            },
            "/api/research": {
                target: "http://127.0.0.1:8100",
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api/, ""),
            },
            "/api/retrieval": {
                target: "http://127.0.0.1:8014",
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api/, ""),
            },
        },
    },
});
