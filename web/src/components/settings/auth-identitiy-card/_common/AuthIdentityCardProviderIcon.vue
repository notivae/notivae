<script setup lang="ts">
import authLocalIconSrc from "@/assets/auth-provider/local.svg";
import authMagicLinkIconSrc from "@/assets/auth-provider/magic-link.svg";
import authOIDCIconSrc from "@/assets/auth-provider/oidc.svg";
import { Avatar, AvatarImage } from "@/components/ui/avatar";


const knownProviderIcons = {
  local: authLocalIconSrc,
  magic: authMagicLinkIconSrc,
  oidc: authOIDCIconSrc,
} as const;

defineProps<{
  provider: keyof typeof knownProviderIcons
}>();
</script>

<template>
  <Avatar v-if="knownProviderIcons[provider]" class="bg-muted" :title="provider">
    <AvatarImage :src="knownProviderIcons[provider]" class="dark:invert p-1" />
  </Avatar>
</template>
