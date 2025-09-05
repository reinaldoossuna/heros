import { TanStackRouterVite } from "@tanstack/router-vite-plugin"
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
import tsconfigPaths from "vite-tsconfig-paths"

// https://vite.dev/config/
export default defineConfig({
    plugins: [react(), TanStackRouterVite(), tsconfigPaths()],
    server: {
        proxy: {
            "/api": { changeOrigin: true, target: "http://localhost:8001", secure: false }

        }
        ,
        cors: { origin: "http://localhost" }
    },
})
