<script setup lang="ts">
import { Dialog, DialogFooter, DialogTrigger, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { ref } from "vue";
import { useMutation } from "@tanstack/vue-query";
import { useMfaDetails } from "@/composables/api/useMfaDetails.ts";
import { deleteApiAuthMFATotp } from "@/services/api/auth/mfa/totp.ts";
import { ErrorBox } from "@/components/common/error-box";
import { LucideLoader } from "lucide-vue-next";

const { refetch: refetchMfaDetails } = useMfaDetails();
const isOpen = ref(false);

const { mutateAsync, isPending, error } = useMutation({
  mutationFn: async () => {
    await deleteApiAuthMFATotp();
  },
  onSuccess: async () => {
    await refetchMfaDetails();
  },
});

async function disableTotp() {
  await mutateAsync();
}
</script>

<template>
  <Dialog v-model:open="isOpen">
    <DialogTrigger as-child>
      <slot />
    </DialogTrigger>
    <DialogContent>
      <DialogHeader>
        <DialogTitle>
          Disable MFA via TOTP?
        </DialogTitle>
        <DialogDescription class="text-warning">
          Disabling your Authenticator App will reduce your account's security.
          You’ll no longer be prompted for a time-based code at login.
        </DialogDescription>
      </DialogHeader>
      <ErrorBox :error="error" />
      <DialogFooter>
        <Button variant="outline" :disabled="isPending" @click="isOpen = false">
          Cancel
        </Button>
        <Button :disabled="isPending" @click="disableTotp">
          <LucideLoader v-if="isPending" class="animate-spin" />
          Disable
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
