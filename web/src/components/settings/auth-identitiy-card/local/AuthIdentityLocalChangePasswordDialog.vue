<script setup lang="ts">
import { Dialog, DialogTrigger, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { computed, ref } from "vue";
import { useMutation } from "@tanstack/vue-query";
import { whenever } from "@vueuse/core";
import { postApiAuthLocalChangePassword } from "@/services/api/auth/local/change-password.ts";
import { LucideLoader } from "lucide-vue-next";
import { Label } from "@/components/ui/label";


const isOpen = ref(false);
const password = ref("");
const passwordConfirm = ref("");
const arePasswordsTheSame = computed(() => password.value === passwordConfirm.value);
const canSubmit = computed(() => password.value.length > 0 && arePasswordsTheSame.value);

whenever(isOpen, () => {
  password.value = "";
  passwordConfirm.value = "";
});

const { mutateAsync, isPending } = useMutation({
  mutationFn: async () => {
    await postApiAuthLocalChangePassword({
      new_password: password.value,
    });
  },
  onSuccess: async () => {
    password.value = "";
    passwordConfirm.value = "";
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
            Change Password
          </DialogTitle>
          <DialogDescription>
            Enter your new password and confirm it to update your credentials.
          </DialogDescription>
        </DialogHeader>
        <fieldset class="space-y-1">
          <Label>Password</Label>
          <Input
              type="password"
              v-model.trim="password"
              required
              autofocus
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
            Cancel
          </Button>
          <Button type="submit" variant="default" @click="handleSubmit" :disabled="isPending || !canSubmit">
            <LucideLoader v-if="isPending" class="animate-spin" />
            Save
          </Button>
        </DialogFooter>
      </form>
    </DialogContent>
  </Dialog>
</template>
