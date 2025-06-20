import { createRouter, createWebHashHistory } from "vue-router";

export default createRouter({
    history: createWebHashHistory(),
    routes: [
        {
            name: 'home',
            path: '/',
            component: () => import('@/pages/HomePage.vue'),
        },
    ],
});
