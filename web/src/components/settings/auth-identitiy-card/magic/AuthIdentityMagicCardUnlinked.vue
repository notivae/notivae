<script setup lang="ts">
import {
  AuthIdentityCard,
  AuthIdentityCardActions,
  AuthIdentityCardProviderIcon
} from "@/components/settings/auth-identitiy-card/_common";
import { LucideLink2, LucideLoader } from "lucide-vue-next";
import { Button } from "@/components/ui/button";
import { useMutation } from "@tanstack/vue-query";
import { postApiAuthMagicRegister } from "@/services/api/auth/magic/register.ts";
import { useAuthStore } from "@/stores/auth.ts";
import { useAuthIdentities } from "@/composables/api/useAuthIdentities.ts";
import { ErrorBox } from "@/components/common/error-box";

const auth = useAuthStore();
const { refetch: refetchAuthIdentities } = useAuthIdentities();

const { mutateAsync, isPending, error } = useMutation({
  mutationFn: async () => {
    await postApiAuthMagicRegister({
      email: auth.user!.email,
    });
  },
  onSuccess: async () => {
    await refetchAuthIdentities();
  },
});
</script>

<template>
  <AuthIdentityCard>
    <h3 class="flex items-center gap-1">
      <AuthIdentityCardProviderIcon provider="magic" class="inline-block" />
      Magic Link
    </h3>
    <ErrorBox :error="error" />
    <AuthIdentityCardActions>
      <Button variant="secondary" size="sm" @click="mutateAsync">
        <LucideLoader v-if="isPending" class="animate-spin" />
        <LucideLink2 v-else />
        Link
      </Button>
    </AuthIdentityCardActions>
  </AuthIdentityCard>
</template>
