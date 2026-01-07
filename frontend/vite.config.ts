import { TanStackRouterVite } from '@tanstack/router-vite-plugin'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
import tsconfigPaths from 'vite-tsconfig-paths'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), TanStackRouterVite(), tsconfigPaths()],
  server: {
    proxy: {
      '/server': {
        changeOrigin: true,
        target: 'http://heros-server.local:8000',
        secure: false,
 rewrite: (path) => path.replace(/^\/server/, ''),
      }},
        cors: { origin: "http://localhost" },
        allowedHosts: ["heros-server.local"]
  }
})
