<script setup lang="ts">
import { Separator } from "@/components/ui/separator";
import { LucideFingerprint } from "lucide-vue-next";
import { AuthIdentityLocalCard } from "@/components/settings/auth-identitiy-card/local";
import { AuthIdentityMagicCard } from "@/components/settings/auth-identitiy-card/magic";
import { AuthIdentityOIDCCard } from "@/components/settings/auth-identitiy-card/oidc";
import { useServerFeatures } from "@/composables/useServerFeatures.ts";

const { data: serverFeatures } = useServerFeatures();
</script>

<template>
  <div class="space-y-4">
    <div>
      <h2 class="text-xl font-bold">
        <LucideFingerprint class="inline-block" />
        Authentication Identities
      </h2>
      <Separator />
    </div>
    <AuthIdentityLocalCard v-if="serverFeatures?.auth.local" />
    <AuthIdentityMagicCard v-if="serverFeatures?.auth.magic_link" />
    <AuthIdentityOIDCCard v-if="serverFeatures?.auth.oidc" />
  </div>
</template>
