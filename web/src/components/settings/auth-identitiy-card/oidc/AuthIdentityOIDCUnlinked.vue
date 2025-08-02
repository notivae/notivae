<script setup lang="ts">
import { computed } from "vue";
import {
  AuthIdentityCard,
  AuthIdentityCardActions,
  AuthIdentityCardProviderIcon,
} from "@/components/settings/auth-identitiy-card/_common";
import { Button } from "@/components/ui/button";
import { useBrowserLocation } from "@vueuse/core";

const locationRef = useBrowserLocation();
const redirectLink = computed(() => `/api/auth/oidc/redirect?${new URLSearchParams({ next: locationRef.value.href ?? "/" })}`);
</script>

<template>
  <AuthIdentityCard>
    <h3 class="flex items-center gap-1">
      <AuthIdentityCardProviderIcon provider="oidc" class="inline-block" />
      OIDC
    </h3>
    <AuthIdentityCardActions>
      <a :href="redirectLink">
        <Button variant="secondary" size="sm">
          Link
        </Button>
      </a>
    </AuthIdentityCardActions>
  </AuthIdentityCard>
</template>
