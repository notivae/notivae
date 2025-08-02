import { defineStore } from "pinia";
import { ref } from "vue";
import type { UserMe } from "@/types/api.ts";
import { computed } from "vue";
import { useQuery, useQueryClient } from "@tanstack/vue-query";
import { getApiMeAccount } from "@/services/api/me/account.ts";
import { postApiLogout } from "@/services/api/auth/logout.ts";


export const useAuthStore = defineStore('auth', () => {
    const user = ref<UserMe | null>(null);

    const isLoggedIn = computed(() => !!user.value);

    const queryClient = useQueryClient();

    const { isLoading, isError, refetch } = useQuery({
        queryKey: ["user", "me"],
        queryFn: async () => {
            if (!navigator.onLine) throw new Error('Offline');
            const me = await getApiMeAccount();
            user.value = me.data;
            return me.data;
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
