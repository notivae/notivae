import path from "node:path";
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from "@tailwindcss/vite";
import { VitePWA } from "vite-plugin-pwa";


// https://vite.dev/config/
export default defineConfig({
    plugins: [
        vue(),
        tailwindcss(),
        VitePWA({
            registerType: "autoUpdate",
            includeAssets: ['favicon.ico'],
            pwaAssets: {},
            manifest: {
                name: "Notivae",
                short_name: "Notivae",
                description: "A self-hosted, real-time markdown editor for structured notes, collaborative learning, and knowledge management",
                theme_color: "#ffffff",
                icons: [
                    {src: 'pwa-64x64.png', sizes: '64x64', type: 'image/png'},
                    {src: 'pwa-192x192.png', sizes: '192x192', type: 'image/png'},
                    {src: 'pwa-512x512.png', sizes: '512x512', type: 'image/png', purpose: 'any'},
                    {src: 'maskable-icon-512x512.png', sizes: '512x512', type: 'image/png', purpose: 'maskable'},
                ],
                display: "standalone",
                categories: ["productivity"],
            },
        }),
    ],
    server: {
        proxy: {
            '/api': 'http://server:8000',
        }
    },
    resolve: {
        alias: {
            '@': path.resolve(__dirname, './src'),
        },
    },
});
