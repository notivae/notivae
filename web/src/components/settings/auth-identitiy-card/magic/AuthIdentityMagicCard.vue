<script setup lang="ts">
import { useAuthIdentities } from "@/composables/api/useAuthIdentities.ts";
import { computed } from "vue";
import AuthIdentityMagicCardLinked
  from "@/components/settings/auth-identitiy-card/magic/AuthIdentityMagicCardLinked.vue";
import AuthIdentityMagicCardUnlinked
  from "@/components/settings/auth-identitiy-card/magic/AuthIdentityMagicCardUnlinked.vue";

const { data: authIdentities, isPending } = useAuthIdentities();

const identity = computed(() => authIdentities.value?.find(i => i.provider === "magic"));
</script>

<template>
  <template v-if="isPending" />
  <AuthIdentityMagicCardLinked v-else-if="identity" />
  <AuthIdentityMagicCardUnlinked v-else />
</template>
