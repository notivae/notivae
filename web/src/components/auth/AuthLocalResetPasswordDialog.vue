<script setup lang="ts">
import { Dialog, DialogTrigger, DialogFooter, DialogHeader, DialogTitle, DialogDescription, DialogContent } from "@/components/ui/dialog";
import { ref, watch } from "vue";
import { whenever } from "@vueuse/core";
import { Button } from "@/components/ui/button";
import { useMutation } from "@tanstack/vue-query";
import { postApiAuthLocalForgotPassword } from "@/services/api/auth/local/forgot-password.ts";
import { Input } from "@/components/ui/input";
import { ErrorBox } from "@/components/common/error-box";
import { LucideLoader, LucideRotateCcwKey } from "lucide-vue-next";
import { Alert, AlertTitle } from "@/components/ui/alert";
import { Label } from "@/components/ui/label";

const isOpen = ref(false);
const email = ref("");
const isDirty = ref(false);

whenever(isOpen, () => {
  email.value = "";
});
watch([email], () => {
  isDirty.value = true;
});

const { mutateAsync, isPending, isSuccess, error } = useMutation({
  mutationFn: async () => {
    await postApiAuthLocalForgotPassword({
      email: email.value,
    });
  },
})

async function handleSubmit() {
  if (isPending.value) return;

  isDirty.value = false;
  await mutateAsync();
}
</script>

<template>
  <Dialog v-model:open="isOpen">
    <DialogTrigger as-child>
      <slot />
    </DialogTrigger>
    <DialogContent>
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <DialogHeader>
          <DialogTitle>
            Reset your password
          </DialogTitle>
          <DialogDescription>
            Enter your email address, and we'll send you a link to reset your password.
            If an account with this email exists, you will receive instructions shortly.
          </DialogDescription>
        </DialogHeader>
        <fieldset class="space-y-1">
          <Label>Email</Label>
          <Input
              v-model.trim="email"
              type="email"
              required
              placeholder="johndoe@example.com"
              autocomplete="email"
          />
        </fieldset>
        <ErrorBox v-if="!isDirty" :error="error" />
        <Alert v-if="!isDirty && isSuccess" variant="success">
          <LucideRotateCcwKey />
          <AlertTitle>
            If an account exists for this email, you'll receive a reset link shortly.
          </AlertTitle>
        </Alert>
        <DialogFooter>
          <Button type="button" variant="outline" @click="isOpen = false">
            Cancel
          </Button>
          <Button type="submit" :disabled="isPending || !email.length">
            <LucideLoader v-if="isPending" class="animate-spin" />
            Reset
          </Button>
        </DialogFooter>
      </form>
    </DialogContent>
  </Dialog>
</template>
