<script setup lang="ts">
import { useAuthIdentities } from "@/composables/api/useAuthIdentities.ts";
import { computed } from "vue";
import AuthIdentityLocalCardLinked
  from "@/components/settings/auth-identitiy-card/local/AuthIdentityLocalCardLinked.vue";
import AuthIdentityLocalCardUnlinked
  from "@/components/settings/auth-identitiy-card/local/AuthIdentityLocalCardUnlinked.vue";

const { data: authIdentities, isPending } = useAuthIdentities();

const identity = computed(() => authIdentities.value?.find(i => i.provider === "local"));
</script>

<template>
  <template v-if="isPending" />
  <AuthIdentityLocalCardLinked v-else-if="identity" />
  <AuthIdentityLocalCardUnlinked v-else />
</template>
