import { useColorMode } from "@vueuse/core";

export function useConfiguredColorMode() {
    return useColorMode({
        modes: {
            "light": "light theme-default",
            "dark": "dark theme-default",
            "parchment": "light theme-parchment",
            "parchment-dark": "dark theme-parchment",
        },
    });
}
