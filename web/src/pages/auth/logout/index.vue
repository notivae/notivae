<script setup lang="ts">
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth.ts";

definePage({
  meta: {
    requiresAuth: false,
  }
});

const router = useRouter();
const auth = useAuthStore();

try {
  await auth.logout();
  await router.replace({ name: '/' });
} catch (error) {
  console.error(error);
  if (error instanceof Error) {
    await router.push({ name: '/error', query: { name: error.name, message: error.message } });
  }
}
</script>

<template>
  You shouldn't see this ever.
</template>
