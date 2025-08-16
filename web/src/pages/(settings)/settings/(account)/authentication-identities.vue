<script setup lang="ts">
import { LucideIdCard } from "lucide-vue-next";
import { AuthIdentityLocalCard } from "@/components/settings/auth-identitiy-card/local";
import { AuthIdentityMagicCard } from "@/components/settings/auth-identitiy-card/magic";
import { AuthIdentityOIDCCard } from "@/components/settings/auth-identitiy-card/oidc";
import { useServerFeatures } from "@/composables/api/useServerFeatures.ts";
import { SettingsDescription, SettingsHeading, SettingsSection } from "@/components/settings/common";

const { data: serverFeatures } = useServerFeatures();
</script>

<template>
  <SettingsSection>
    <SettingsHeading variant="h1">
      <LucideIdCard />
      Authentication Identities
    </SettingsHeading>
    <SettingsDescription>
      Manage the different ways you can sign in to your account. Connect or remove login options like local, magic-link, or other providers, and choose what works best for you.
    </SettingsDescription>
  </SettingsSection>

  <AuthIdentityLocalCard v-if="serverFeatures?.auth.local" />
  <AuthIdentityMagicCard v-if="serverFeatures?.auth.magic_link" />
  <AuthIdentityOIDCCard v-if="serverFeatures?.auth.oidc" />
</template>
