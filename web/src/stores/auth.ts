import { defineStore } from "pinia";
import { ref } from "vue";
import type { User } from "@/types/api.ts";
import { computed } from "vue";
import { useQuery, useQueryClient } from "@tanstack/vue-query";
import { getApiUserMe } from "@/services/api/user/me.ts";
import { postApiLogout } from "@/services/api/auth/logout.ts";


export const useAuthStore = defineStore('auth', () => {
    const user = ref<User | null>(null);

    const isLoggedIn = computed(() => !!user.value);

    const queryClient = useQueryClient();

    const { isLoading, isError, refetch } = useQuery({
        queryKey: ["user", "me"],
        queryFn: async () => {
            if (!navigator.onLine) throw new Error('Offline');
            const me = await getApiUserMe();
            user.value = me.data;
        },
        staleTime: 1000 * 60 * 5,
        retry: false,
    });

    async function reloadAuth() {
        try {
            await refetch();
        } catch {
            user.value = null;
        }
    }

    async function logout(): Promise<void> {
        await postApiLogout();
        user.value = null;
        await queryClient.invalidateQueries();
    }

    return {
        user,
        isLoggedIn,
        reloadAuth,
        logout,
        isLoading,
        isError,
    };
});
