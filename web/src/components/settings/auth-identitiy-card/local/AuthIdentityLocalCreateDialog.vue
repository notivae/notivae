<script setup lang="ts">
import { Dialog, DialogTrigger, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { computed, ref } from "vue";
import { useMutation } from "@tanstack/vue-query";
import { whenever } from "@vueuse/core";
import { LucideLoader } from "lucide-vue-next";
import { Label } from "@/components/ui/label";
import { useAuthStore } from "@/stores/auth.ts";
import { useAuthIdentities } from "@/composables/api/useAuthIdentities.ts";
import { postApiAuthLocalRegister } from "@/services/api/auth/local/register.ts";


const auth = useAuthStore();
const { refetch: refetchAuthIdentities } = useAuthIdentities();

const isOpen = ref(false);
const email = ref("");
const username = ref("");
const password = ref("");
const passwordConfirm = ref("");
const arePasswordsTheSame = computed(() => password.value === passwordConfirm.value);
const canSubmit = computed(() => password.value.length > 0 && arePasswordsTheSame.value);

whenever(isOpen, () => {
  resetFields();
});

function resetFields(): void {
  email.value = auth.user!.email;
  username.value = auth.user!.name;
  password.value = "";
  passwordConfirm.value = "";
}

const { mutateAsync, isPending } = useMutation({
  mutationFn: async () => {
    await postApiAuthLocalRegister({
      username: username.value,
      password: password.value,
      email: email.value,
    });
  },
  onSuccess: async () => {
    await refetchAuthIdentities();
    resetFields();
    isOpen.value = false;
  },
});

async function handleSubmit(): Promise<void> {
  if (isPending.value) return;
  if (!canSubmit.value) return;

  await mutateAsync();
}
</script>

<template>
  <Dialog v-model:open="isOpen">
    <DialogTrigger as-child>
      <slot />
    </DialogTrigger>
    <DialogContent>
      <form ref="change-form" @submit.prevent="handleSubmit" class="space-y-4">
        <DialogHeader>
          <DialogTitle>
            Create Local Auth Identity
          </DialogTitle>
          <DialogDescription>
            Set up a local login (email and password) for your account.
          </DialogDescription>
        </DialogHeader>
        <fieldset class="flex flex-col gap-1">
          <Label for="email-input">Email</Label>
          <Input
              v-model.trim="email"
              id="email-input"
              type="email"
              required
              :disabled="isPending"
              placeholder="john@company.com"
              autocomplete="email"
          />
        </fieldset>
        <fieldset class="flex flex-col gap-1">
          <Label for="username-input">Username</Label>
          <Input
              v-model.trim="username"
              id="username-input"
              required
              :disabled="isPending"
              placeholder="johndoe"
              autocomplete="username"
          />
        </fieldset>
        <fieldset class="space-y-1">
          <Label>Password</Label>
          <Input
              autofocus
              type="password"
              v-model.trim="password"
              required
              placeholder="******"
              autocomplete="new-password"
          />
        </fieldset>
        <fieldset class="space-y-1">
          <Label>Confirm Password</Label>
          <Input
              type="password"
              v-model.trim="passwordConfirm"
              required
              placeholder="******"
              autocomplete="new-password"
          />
        </fieldset>
        <DialogFooter>
          <Button variant="outline" @click="isOpen = false" :disabled="isPending">
            Close
          </Button>
          <Button type="submit" variant="default" :disabled="isPending || !canSubmit">
            <LucideLoader v-if="isPending" class="animate-spin" />
            Create
          </Button>
        </DialogFooter>
      </form>
    </DialogContent>
  </Dialog>
</template>
