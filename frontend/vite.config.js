import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    vue(), tailwindcss(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['icons/icon-192.png', 'icons/icon-512.png'],
      manifest: {
        name: '灵感工坊', short_name: '灵感', description: '创作灵感记录与管理',
        theme_color: '#4c1d95', background_color: '#faf5ff', display: 'standalone', orientation: 'portrait',
        icons: [{ src: 'icons/icon-192.png', sizes: '192x192', type: 'image/png' }, { src: 'icons/icon-512.png', sizes: '512x512', type: 'image/png' }],
      },
      workbox: { globPatterns: ['**/*.{js,css,html,ico,png,svg,woff2}'] },
    }),
  ],
  server: { proxy: { '/api': 'http://localhost:8000' } },
})
