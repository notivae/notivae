import { createRouter, createWebHashHistory } from "vue-router";
import { routes, handleHotUpdate } from "vue-router/auto-routes";
import { useAuthStore } from "@/stores/auth.ts";

export const router = createRouter({
    history: createWebHashHistory(),
    routes,
});

router.beforeEach(async (to, _from, next) => {
    const auth = useAuthStore();
    const requiresAuth = to.meta.requiresAuth !== false;

    if (requiresAuth && !auth.isLoggedIn) {
        await auth.reloadAuth();

        if (!auth.isLoggedIn) {
            return next({ name: '/auth/login/', query: { next: to.fullPath } });
        }
    }

    next();
});

if (import.meta.hot) {
    handleHotUpdate(router);
}
