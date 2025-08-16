<script setup lang="ts">
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { IconAuthProviderLocal, IconAuthProviderMagicLink, IconAuthProviderOIDC } from "@/components/icons";


const knownProviderIcons = {
  local: IconAuthProviderLocal,
  magic: IconAuthProviderMagicLink,
  oidc: IconAuthProviderOIDC,
} as const;

defineProps<{
  provider: keyof typeof knownProviderIcons
}>();
</script>

<template>
  <Avatar v-if="knownProviderIcons[provider]" class="bg-muted" :title="provider">
    <AvatarFallback>
      <component :is="knownProviderIcons[provider]" />
    </AvatarFallback>
  </Avatar>
</template>
