import { useQuery } from "@tanstack/vue-query";
import { getApiUserAuthIdentities } from "@/services/api/user/auth-identities.ts";


export function useAuthIdentities() {
    return useQuery({
        queryKey: ["user", "identities"],
        queryFn: async () => {
            if (!navigator.onLine) throw new Error("Offline");
            const res = await getApiUserAuthIdentities();
            return res.data;
        },
        staleTime: 1000 * 60 * 5,
        retry: false,
    });
}
