import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
    plugins: [react()],
    server: {
        proxy: {
            "/research": {
                target: "http://127.0.0.1:8002",
                changeOrigin: true,
            },
            "/retrieval": {
                target: "http://127.0.0.1:8002",
                changeOrigin: true,
            },
            "/api/repository": {
                target: "http://127.0.0.1:8002",
                changeOrigin: true,
                rewrite: (path) =>
                    path.replace(
                        /^\/api/,
                        "",
                    ),
            },
            "/api/documents": {
                target: "http://127.0.0.1:8002",
                changeOrigin: true,
                rewrite: (path) =>
                    path.replace(
                        /^\/api/,
                        "",
                    ),
            },
        },
    },
});
