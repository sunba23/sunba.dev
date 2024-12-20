import { defineConfig } from 'vite'

export default defineConfig({
  build: {
    rollupOptions: {
      external: [],
    },
  },
  define: {
    'import.meta.env.VITE_WS_URL': JSON.stringify(process.env.VITE_WS_URL),
  },
});
