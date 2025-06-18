import { DefaultTheme, defineConfig } from "vitepress";

export const en = defineConfig({
    lang: 'en-US',
    themeConfig: {
        nav: nav(),
        sidebar: sidebar(),
    },
});

function nav(): DefaultTheme.NavItem[] {
    return [];
}

function sidebar(): DefaultTheme.SidebarItem[] {
    return [];
}
