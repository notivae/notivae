<script setup lang="ts">
import { useAuthStore } from "@/stores/auth.ts";
import { ref, useTemplateRef, watch } from "vue";
import type { UserMe } from "@/types/api.ts";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { LucideLoader, LucideMailCheck, LucideMailX, LucideUserRound } from "lucide-vue-next";
import { Badge } from "@/components/ui/badge";
import { useMutation } from "@tanstack/vue-query";
import { patchApiMeAccount } from "@/services/api/me/account.ts";
import { postApiMeResendVerification } from "@/services/api/me/resend-verification.ts";
import { toast } from "vue-sonner";
import SettingsHeading from "@/components/settings/common/SettingsHeading.vue";
import { SettingsDescription, SettingsSection } from "@/components/settings/common";

const auth = useAuthStore();

const { mutateAsync, isPending } = useMutation({
  mutationKey: ["user", "me"],
  mutationFn: async () => {
    await patchApiMeAccount({
      email: account.value.email,
      name: account.value.name,
      display_name: account.value.display_name,
    });
  },
  onSuccess: async () => {
    await auth.reloadAuth();
  }
});

const {
  mutateAsync: resendVerificationMail,
  isPending: isSendingVerificationMail,
} = useMutation({
  mutationFn: async () => {
    const toastId = toast.loading("Requesting Verification Mail...");
    try {
      await postApiMeResendVerification();

      toast.success("Verification Mail was re-sent", {
        id: toastId,
      });
    } catch (error) {
      console.log(error);
      toast.error("Failed to re-send verification mail", {
        id: toastId,
        description: `${error}`,
      });
    }
  },
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
  <SettingsSection>
    <SettingsHeading variant="h1">
      <LucideUserRound />
      Account
    </SettingsHeading>
    <SettingsDescription>
      Here you can view and update your account details. Keep your info up to date so everything stays accurate and personal to you.
    </SettingsDescription>
  </SettingsSection>

  <SettingsSection as="form" ref="request-form" @submit.prevent="handleSubmit">
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
        <Badge v-else variant="warning" title="Not Verified. Click to re-send verification mail" class="cursor-pointer" role="button" @click="!isSendingVerificationMail && resendVerificationMail()">
          <LucideLoader v-if="isSendingVerificationMail" />
          <LucideMailX v-else />
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
  </SettingsSection>
</template>
