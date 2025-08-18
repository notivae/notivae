<script setup lang="ts">
import { LucideUserRound } from "lucide-vue-next";
import SettingsHeading from "@/components/settings/common/SettingsHeading.vue";
import { SettingsDescription, SettingsSection } from "@/components/settings/common";
import { ChangeAvatarSection, ChangeAccountDetailsSection } from "@/components/pages/settings/account";
</script>

<template>
  <SettingsSection>
    <SettingsHeading variant="h1">
      <LucideUserRound />
      Account
    </SettingsHeading>
    <SettingsDescription>
      Here you can view and update your account details. Keep your info up to date so everything stays accurate and personal to you.
    </SettingsDescription>
  </SettingsSection>

  <ChangeAvatarSection />

  <ChangeAccountDetailsSection />
</template>
