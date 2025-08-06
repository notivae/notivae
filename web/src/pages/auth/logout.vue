<script setup lang="ts">
import { useAuthStore } from "@/stores/auth.ts";

definePage({
  meta: {
    requiresAuth: false,
  },
  beforeEnter: async (to, _from, next) => {
    const auth = useAuthStore();
    try {
      await auth.logout();
      return next({ path: (to.query.next as string) ?? '/' });
    } catch (error) {
      console.error(error);
      if (error instanceof Error) {
        return next({ name: '/error', query: { name: error.name, message: error.message } });
      }
    }
  },
});
</script>

<template>
  You shouldn't see this ever.
</template>
