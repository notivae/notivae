import { defineConfig } from "vitepress";
import { groupIconMdPlugin, groupIconVitePlugin } from "vitepress-plugin-group-icons";


// https://vitepress.dev/reference/site-config
export const shared = defineConfig({
  title: "Notivae",
  description: "Notivae is a real-time, self-hosted note-taking and knowledge management platform built for students and teams",

  rewrites: {
    'en/:rest*': ':rest*',
  },

  srcDir: 'src/',
  srcExclude: ['**/README.md', '**/TODO.md'],
  lastUpdated: true,
  cleanUrls: true,
  metaChunk: true,
  ignoreDeadLinks: 'localhostLinks',
  markdown: {
    config(md) {
      md.use(groupIconMdPlugin);
    },
    image: {
      lazyLoading: true,
    },
  },

  head: [
    ['link', { rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' }],
    ['meta', { name: 'theme-color', content: '#ffffff' }],
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { property: 'og:locale', content: 'en' }],
    ['meta', { property: 'og:title', content: 'Notivae' }],
    ['meta', { property: 'og:site_name', content: 'Notivae' }],
    ['meta', { property: 'og:image', content: 'https://notivae.github.io/og-image.png' }],
    ['meta', { property: 'og:image:type', content: 'image/png' }],
    ['meta', { property: 'og:url', content: 'https://notivae.github.io/' }],
  ],

  sitemap: {
    hostname: 'https://notivae.github.io',
  },

  themeConfig: {
    socialLinks: [
      { icon: 'github', link: 'https://github.com/notivae/notivae' }
    ],
    footer: {
      copyright: `Copyright © 2025-present <a href='https://github.com/notivae/'>Notivae</a>`,
    },
    search: {
      provider: 'local',
    },
  },

  vite: {
    plugins: [
        groupIconVitePlugin(),
    ],
  },
});
