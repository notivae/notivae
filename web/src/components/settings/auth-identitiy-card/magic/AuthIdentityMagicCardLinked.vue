<script setup lang="ts">
import {
  AuthIdentityCard,
  AuthIdentityCardActions, AuthIdentityCardKVGrid,
  AuthIdentityCardProviderIcon
} from "@/components/settings/auth-identitiy-card/_common";
import { LucideLink2Off, LucideLoader } from "lucide-vue-next";
import { Button } from "@/components/ui/button";
import { useMutation } from "@tanstack/vue-query";
import { postApiAuthMagicUnlink } from "@/services/api/auth/magic/unlink.ts";
import { useAuthIdentities } from "@/composables/api/useAuthIdentities.ts";
import { computed } from "vue";

const { data: authIdentities, isPending, refetch: refetchAuthIdentities } = useAuthIdentities();

const canUnlink = computed(() => !isPending.value && authIdentities.value!.length > 1);
const identity = computed(() => authIdentities.value?.find(i => i.provider === "magic"));

const { mutateAsync: unlink, isPending: isUnlinking } = useMutation({
  mutationFn: async () => {
    await postApiAuthMagicUnlink();
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
      <AuthIdentityCardProviderIcon provider="magic" class="inline-block" />
      Magic Link
    </h3>
    <AuthIdentityCardKVGrid :kv="{
      'Provider UserID': identity.provider_user_id,
      'Provider Email': identity.provider_email,
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
