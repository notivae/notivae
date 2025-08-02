<script setup lang="ts">
import { useAuthIdentities } from "@/composables/api/useAuthIdentities.ts";
import { computed } from "vue";
import {
  AuthIdentityCard,
  AuthIdentityCardActions, AuthIdentityCardKVGrid,
  AuthIdentityCardProviderIcon,
} from "@/components/settings/auth-identitiy-card/_common";
import { useMutation } from "@tanstack/vue-query";
import { postApiAuthOIDCUnlink } from "@/services/api/auth/oidc/unlink.ts";
import { Button } from "@/components/ui/button";
import { LucideLoader, LucideLink2Off } from "lucide-vue-next";

const { data: authIdentities, isPending, refetch: refetchAuthIdentities } = useAuthIdentities();

const canUnlink = computed(() => !isPending.value && authIdentities.value!.length > 1);
const identity = computed(() => authIdentities.value?.find(i => i.provider === "oidc"));

const { mutateAsync: unlink, isPending: isUnlinking } = useMutation({
  mutationFn: async () => {
    await postApiAuthOIDCUnlink();
  },
  onSuccess: async () => {
    await refetchAuthIdentities();
  },
});
</script>

<template>
  <template v-if="isPending" />
  <AuthIdentityCard v-else-if="identity">
    <h3 class="flex items-center gap-1">
      <AuthIdentityCardProviderIcon provider="oidc" class="inline-block" />
      OIDC
    </h3>
    <AuthIdentityCardKVGrid :kv="{
      'Provider UserID': identity.provider_user_id,
      'Provider Email': identity.provider_email,
      'Nickname': identity.userinfo?.nickname,
      'Preferred Username': identity.userinfo?.preferred_username,
      'Email': identity.userinfo?.email,
      'Locale': identity.userinfo?.locale,
    }" />
    <AuthIdentityCardActions>
        <Button variant="outline" size="sm" @click="unlink" :disabled="!canUnlink">
          <LucideLoader v-if="isUnlinking" class="animate-spin" />
          <LucideLink2Off v-else />
          Unlink
        </Button>
    </AuthIdentityCardActions>
  </AuthIdentityCard>
  <div v-else class="text-destructive-foreground bg-destructive">ERROR</div>
</template>
