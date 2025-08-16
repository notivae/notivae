import path from "node:path";
import { defineConfig } from "vite";
import Vue from "@vitejs/plugin-vue";
import VueRouter from "unplugin-vue-router/vite";
import TailwindCSS from "@tailwindcss/vite";
import { VitePWA } from "vite-plugin-pwa";


// https://vite.dev/config/
export default defineConfig({
    plugins: [
        VueRouter(),
        Vue(),
        TailwindCSS(),
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
            '/api': {
                target: 'http://server:8000',
                ws: true,
                changeOrigin: false,
                configure(proxy, _options) {
                    // removes the `Secure` part of the set-cookie header in order to enable login via mobile devices over network on an http-connection.
                    proxy.on('proxyRes', (proxyRes, _req, _res) => {
                        const cookies = proxyRes.headers['set-cookie'];
                        if (cookies) {
                            proxyRes.headers['set-cookie'] = cookies.map(cookie =>
                                cookie.replace(/;\s*Secure/i, '')
                            );
                        }
                    });
                },
            },
        }
    },
    resolve: {
        alias: {
            '@': path.resolve(__dirname, './src'),
        },
    },
});
