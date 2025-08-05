import { useQuery } from "@tanstack/vue-query";
import { getApiMeAuthMfaDetails } from "@/services/api/me/mfa-info.ts";


export function useMfaDetails() {
    return useQuery({
        queryKey: ["user", "mfa-info"],
        queryFn: async () => {
            if (!navigator.onLine) throw new Error("Offline");
            const res = await getApiMeAuthMfaDetails();
            return res.data;
        },
        staleTime: 1000 * 60 * 5,
        retry: false,
    });
}
