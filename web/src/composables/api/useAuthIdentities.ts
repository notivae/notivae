import { useQuery } from "@tanstack/vue-query";
import { getApiMeAuthIdentities } from "@/services/api/me/auth-identities.ts";


export function useAuthIdentities() {
    return useQuery({
        queryKey: ["user", "auth-identities"],
        queryFn: async () => {
            if (!navigator.onLine) throw new Error("Offline");
            const res = await getApiMeAuthIdentities();
            return res.data;
        },
        staleTime: 1000 * 60 * 5,
        retry: false,
    });
}
