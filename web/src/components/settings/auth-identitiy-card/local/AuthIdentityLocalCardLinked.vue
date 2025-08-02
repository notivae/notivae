<script setup lang="ts">
import { useAuthIdentities } from "@/composables/api/useAuthIdentities.ts";
import { computed } from "vue";
import {
  AuthIdentityCard, AuthIdentityCardActions, AuthIdentityCardKVGrid,
  AuthIdentityCardProviderIcon,
} from "@/components/settings/auth-identitiy-card/_common";
import { LucideLink2Off, LucideLoader, LucideSquareAsterisk } from "lucide-vue-next";
import { Button } from "@/components/ui/button";
import { useMutation } from "@tanstack/vue-query";
import { postApiAuthLocalUnlink } from "@/services/api/auth/local/unlink.ts";
import AuthIdentityLocalChangePasswordDialog from "@/components/settings/auth-identitiy-card/local/AuthIdentityLocalChangePasswordDialog.vue";


const { data: authIdentities, isPending, refetch: refetchAuthIdentities } = useAuthIdentities();

const canUnlink = computed(() => !isPending.value && authIdentities.value!.length > 1);
const identity = computed(() => authIdentities.value?.find(i => i.provider === "local"));

const { mutateAsync: unlink, isPending: isUnlinking } = useMutation({
  mutationFn: async () => {
    await postApiAuthLocalUnlink();
  },
  onSuccess: async () => {
    await refetchAuthIdentities();
  },
});
</script>

<template>
  <template v-if="isPending"></template>
  <AuthIdentityCard v-if="identity">
    <h3 class="flex items-center gap-1">
      <AuthIdentityCardProviderIcon provider="local" class="inline-block" />
      Local
    </h3>
    <AuthIdentityCardKVGrid :kv="{
      'Provider UserID': identity.provider_user_id,
      'Provider Email': identity.provider_email,
    }" />
    <AuthIdentityCardActions>
      <AuthIdentityLocalChangePasswordDialog>
        <Button variant="secondary" size="sm">
          <LucideSquareAsterisk />
          Change Password
        </Button>
      </AuthIdentityLocalChangePasswordDialog>
      <Button variant="outline" size="sm" @click="unlink" :disabled="!canUnlink">
        <LucideLoader v-if="isUnlinking" class="animate-spin" />
        <LucideLink2Off v-else />
        Unlink
      </Button>
    </AuthIdentityCardActions>
  </AuthIdentityCard>
  <div v-else class="text-destructive-foreground bg-destructive">ERROR</div>
</template>
