<script setup lang="ts">
import { useAuthIdentities } from "@/composables/api/useAuthIdentities.ts";
import { computed } from "vue";
import AuthIdentityOIDCLinked from "@/components/settings/auth-identitiy-card/oidc/AuthIdentityOIDCLinked.vue";
import AuthIdentityOIDCUnlinked from "@/components/settings/auth-identitiy-card/oidc/AuthIdentityOIDCUnlinked.vue";

const { data: authIdentities, isPending } = useAuthIdentities();

const identity = computed(() => authIdentities.value?.find(i => i.provider === "oidc"));
</script>

<template>
  <template v-if="isPending" />
  <AuthIdentityOIDCLinked v-else-if="identity" />
  <AuthIdentityOIDCUnlinked v-else />
</template>
