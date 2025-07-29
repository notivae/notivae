/// <reference types="vite/client" />
/// <reference types="unplugin-vue-router/client" />

export {}

declare module "vue-router" {
    interface RouteMeta {
        /** whether only authenticated users can access the current page. default: `true` */
        requiresAuth?: boolean
        /** if `true` and a user is authenticated, the `next` query parameter is followed */
        followNextIfAuthenticated?: boolean
    }
}
