<script setup lang="ts">
import {
  AuthIdentityCard,
  AuthIdentityCardActions,
  AuthIdentityCardProviderIcon
} from "@/components/settings/auth-identitiy-card/_common";
import { LucideLink2 } from "lucide-vue-next";
import { Button } from "@/components/ui/button";
import AuthIdentityLocalCreateDialog
  from "@/components/settings/auth-identitiy-card/local/AuthIdentityLocalCreateDialog.vue";
</script>

<template>
  <AuthIdentityCard>
    <h3 class="flex items-center gap-1">
      <AuthIdentityCardProviderIcon provider="local" class="inline-block" />
      Local
    </h3>
    <AuthIdentityCardActions>
      <AuthIdentityLocalCreateDialog>
        <Button variant="secondary" size="sm">
          <LucideLink2 />
          Link
        </Button>
      </AuthIdentityLocalCreateDialog>
    </AuthIdentityCardActions>
  </AuthIdentityCard>
</template>
