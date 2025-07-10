import { DefaultTheme, defineConfig } from "vitepress";

export const en = defineConfig({
    lang: 'en-US',
    themeConfig: {
        nav: nav(),
        sidebar: sidebar(),
    },
});

function nav(): DefaultTheme.NavItem[] {
    return [
        {
            text: "Docs",
            link: "/start/introduction",
        }
    ];
}

function sidebar(): DefaultTheme.SidebarItem[] {
    return [
        {
            text: 'Getting Started',
            items: [
                { text: 'Introduction', link: '/start/introduction' },
                { text: 'Requirements', link: '/start/requirements' },
                {
                    text: 'Installation', link: '/start/installation/',
                    collapsed: true,
                    items: [
                        { text: "Reverse Proxy", link: '/start/installation/reverse-proxy' },
                        { text: "Troubleshooting", link: '/start/installation/troubleshooting' },
                    ]
                },
            ]
        },
        {
            text: 'Core Concepts',
            items: [
                { text: 'Core Concepts', link: '/core-concepts/core-concepts' },
                { text: 'Access Control', link: '/core-concepts/access-control' },
            ]
        },
        {
            text: 'Self-Hosting',
            items: [
                {
                    text: 'Configuration', link: '/hosting/configuration/',
                    collapsed: true,
                    items: [
                        { text: "Mail", link: "/hosting/configuration/mail-support" },
                        { text: "Virus Scanning", link: "/hosting/configuration/virus-scanning-support" },
                    ],
                },
                {
                    text: 'Authentication', link: '/hosting/authentication',
                    collapsed: true,
                    items: [
                        { text: "Password", link: "/hosting/authentication/password" },
                        { text: "Discord", link: "/hosting/authentication/discord" },
                        { text: "GitHub", link: "/hosting/authentication/github" },
                        { text: "GitLab", link: "/hosting/authentication/gitlab" },
                        { text: "Google", link: "/hosting/authentication/google" },
                        { text: "Reddit", link: "/hosting/authentication/reddit" },
                        { text: "Spotify", link: "/hosting/authentication/spotify" },
                        { text: "Twitch", link: "/hosting/authentication/twitch" },
                        { text: "OIDC", link: "/hosting/authentication/oidc" },
                    ]
                },
                { text: 'Self-Hosting Guide', link: '/hosting/self-hosting' },
            ]
        },
        {
            text: 'Using Notivae',
            items: [
                { text: 'Editor Guide', link: '/usage/editor-guide' },
                { text: 'Workspace Management', link: '/usage/workspace-management' },
                { text: 'Document Structure', link: '/usage/document-structure' },
                { text: 'Sharing Documents', link: '/usage/sharing-documents' },
            ]
        },
        {
            text: "Intelligence",
            items: [
                { text: "Introduction", link: '/intelligence/introduction' },
                { text: "Installation", link: '/intelligence/installation' },
                {
                    text: "Features", link: '/intelligence/features/',
                    items: [],
                },
            ],
        },
        {
            text: 'Contributing',
            items: [
                { text: 'How to Contribute', link: '/other/contributing' },
                { text: 'Architecture Overview', link: '/other/architecture-overview' },
                { text: 'Design Decisions', link: '/other/design-decisions' },
                { text: 'Roadmap', link: '/other/roadmap' },
                { text: 'FAQ', link: '/other/faq' },
            ]
        }
    ];
}
