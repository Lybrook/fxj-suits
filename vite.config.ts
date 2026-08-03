import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { VitePWA } from 'vite-plugin-pwa';

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      // Use our custom SW file so push handlers are included
      strategies: 'injectManifest',
      srcDir: 'public',
      filename: 'sw-custom.js',
      injectManifest: {
        injectionPoint: undefined,
      },
      includeAssets: ['favicon.ico', 'apple-touch-icon.png', 'mask-icon.svg'],
      manifest: {
        name: 'FXJ Suits | Law Firm Management',
        short_name: 'FXJ Suits',
        description: 'FXJ Suits — Gen Z-aligned Law Firm Management System by Fikia × Jenga Tech',
        theme_color: '#403301',
        background_color: '#FDF6DC',
        display: 'standalone',
        scope: '/',
        start_url: '/',
        icons: [
          { src: 'pwa-192x192.png', sizes: '192x192', type: 'image/png' },
          { src: 'pwa-512x512.png', sizes: '512x512', type: 'image/png' },
          { src: 'pwa-512x512.png', sizes: '512x512', type: 'image/png', purpose: 'any maskable' },
        ],
      },
    }),
  ],
  build: {
    chunkSizeWarningLimit: 1000,
  },
});