import { useRoute } from "vue-router";
import { computed } from "vue";

export function useQueryNext(fallback: string = "/") {
    const currentRoute = useRoute();

    return computed<string>(() => (currentRoute.query.next as string) ?? fallback);
}
