import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// https://vite.dev/config/
export default defineConfig({
  plugins: [svelte()],
  resolve: {
    alias: {
      '@components': '/src/components',
    },
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000', // backend
        changeOrigin: true,
        // rewrite: (path) => path.replace(/^\/api/, ''), // Adjust path if needed
      },
    },
  },
})
