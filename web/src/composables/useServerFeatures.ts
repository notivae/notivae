import { useQuery } from "@tanstack/vue-query";
import { getApiFeatures } from "@/services/api/features.ts";


export function useServerFeatures() {
    return useQuery({
        queryKey: ["features"],
        queryFn: async () => {
            const response = await getApiFeatures();
            return response.data;
        },
        staleTime: 1000 * 60 * 60,  // 1h
        retry: false,
    });
}
