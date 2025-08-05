<script setup lang="ts">
import { useAuthStore } from "@/stores/auth.ts";
import { ref, useTemplateRef, watch } from "vue";
import type { UserMe } from "@/types/api.ts";
import { Input } from "@/components/ui/input";
import { Separator } from "@/components/ui/separator";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { LucideLoader, LucideMailCheck, LucideMailX, LucideUserRound } from "lucide-vue-next";
import { Badge } from "@/components/ui/badge";
import { useMutation } from "@tanstack/vue-query";
import { patchApiMeAccount } from "@/services/api/me/account.ts";

const auth = useAuthStore();

const { mutateAsync, isPending } = useMutation({
  mutationKey: ["user", "me"],
  mutationFn: async () => {
    await patchApiMeAccount({
      email: account.value.email,
      name: account.value.name,
      display_name: account.value.display_name,
    })
  },
  onSuccess: async () => {
    await auth.reloadAuth();
  }
});

function isFormValid() {
  return !!formRef.value?.checkValidity();
}

async function handleSubmit() {
  if (!isFormValid()) return;

  isDirty.value = false;
  await mutateAsync();
}

const formRef = useTemplateRef("request-form");
const account = ref<UserMe>(auth.user!);
const isDirty = ref(false);

watch(account, () => {
  isDirty.value = true;
}, { deep: true });
</script>

<template>
  <form ref="request-form" @submit.prevent="handleSubmit" class="space-y-4">
    <div>
      <h2 class="text-xl font-bold">
        <LucideUserRound class="inline-block mr-1" />
        Account
      </h2>
      <Separator />
    </div>

    <fieldset class="space-y-0.5">
      <Label for="name-input">Username</Label>
      <Input
          id="name-input"
          v-model.trim="account.name"
          required
          :disabled="isPending"
      />
      <span class="text-muted-foreground text-sm">Other users can <b>@mention</b> you</span>
    </fieldset>

    <fieldset class="space-y-0.5">
      <Label for="display-name-input">Displayname</Label>
      <Input
          id="display-name-input"
          v-model.trim="account.display_name"
          required
          :disabled="isPending"
      />
      <span class="text-muted-foreground text-sm">What's displayed to other users visually</span>
    </fieldset>

    <fieldset class="space-y-0.5">
      <Label for="email-input">
        Email
        <Badge v-if="account.email_verified" variant="success" title="Verified">
          <LucideMailCheck />
        </Badge>
        <Badge v-else variant="warning" title="Not Verified">
          <LucideMailX />
        </Badge>
      </Label>
      <Input
          id="email-input"
          v-model.trim="account.email"
          required
          :disabled="isPending"
      />
      <span class="text-muted-foreground text-sm">Private Email for notification</span>
    </fieldset>

    <Button type="submit" variant="secondary" :disabled="!isDirty || isPending || !isFormValid()">
      <template v-if="isPending">
        <LucideLoader class="animate-spin" />
        Saving Changes...
      </template>
      <template v-else>
        Save Changes
      </template>
    </Button>
  </form>
</template>
