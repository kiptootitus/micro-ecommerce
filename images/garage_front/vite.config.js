import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
  host: '0.0.0.0',
  port: 5173,
  hmr: {
    host: 'localhost',
    protocol: 'wss', // Use WebSocket Secure for HTTPS
  },
}
})
