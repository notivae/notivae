import { useColorMode } from "@vueuse/core";

export function useConfiguredColorMode() {
    return useColorMode({
        modes: {
            "light": "light default",
            "dark": "dark default",
            "parchment": "light theme-parchment",
            "parchment-dark": "dark theme-parchment",
        },
    });
}
