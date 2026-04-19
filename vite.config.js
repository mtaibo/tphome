import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite' // <--- 1. Importar

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    tailwindcss(), // <--- 2. Añadir a la lista de plugins
  ],
})