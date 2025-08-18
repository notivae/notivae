<script setup lang="ts">
import { LucideLoader, LucideMailCheck, LucideMailX } from "lucide-vue-next";
import { FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import SettingsHeading from "../../../settings/common/SettingsHeading.vue";
import { Button } from "@/components/ui/button";
import { useMutation } from "@tanstack/vue-query";
import { patchApiMeAccount } from "@/services/api/me/account.ts";
import { useResendVerificationMailMutation } from "@/composables/api/useResendVerificationMailMutation.ts";
import { useForm } from "vee-validate";
import { toTypedSchema } from "@vee-validate/zod";
import * as z from "zod";
import { useAuthStore } from "@/stores/auth.ts";

const auth = useAuthStore();

const { mutateAsync, isPending } = useMutation({
  mutationKey: ["user", "me"],
  mutationFn: async () => {
    await patchApiMeAccount({
      email: isFieldDirty("email") ? values.email : undefined,
      name: isFieldDirty("name") ? values.name : undefined,
      display_name: isFieldDirty("displayName") ? values.displayName : undefined,
    });
  },
  onSuccess: async () => {
    await auth.reloadAuth();
    resetForm({
      values: {
        name: auth.user!.name,
        displayName: auth.user!.display_name ?? undefined,
        email: auth.user!.email,
      },
    });
  }
});

const {
  mutateAsync: resendVerificationMail,
  isPending: isSendingVerificationMail,
} = useResendVerificationMailMutation();

const { meta, validate, values, isFieldDirty, resetForm } = useForm({
  initialValues: {
    name: auth.user!.name,
    displayName: auth.user!.display_name ?? undefined,
    email: auth.user!.email,
  },
  validationSchema: toTypedSchema(z.object({
    name: z.string().trim().nonempty(),
    displayName: z.string().trim(),
    email: z.string().trim().toLowerCase().email(),
  })),
});

async function handleSubmit() {
  await mutateAsync();
}
</script>

<template>

  <form
      @submit.prevent="async () => {
        const { valid } = await validate();
        if (valid) await handleSubmit();
      }"
      class="space-y-4"
  >
    <SettingsHeading variant="h2">
      User details
    </SettingsHeading>

    <FormField v-slot="{ componentField }" name="name">
      <FormItem>
        <FormLabel>Username</FormLabel>
        <FormControl>
          <Input type="text" v-bind="componentField" :disabled="isPending" />
        </FormControl>
        <FormMessage />
        <FormDescription>
          Other users can <b>@mention</b> you
        </FormDescription>
      </FormItem>
    </FormField>

    <FormField v-slot="{ componentField }" name="displayName">
      <FormItem>
        <FormLabel>Display Name</FormLabel>
        <FormControl>
          <Input type="text" v-bind="componentField" :disabled="isPending" />
        </FormControl>
        <FormMessage />
        <FormDescription>
          What's displayed to other users visually
        </FormDescription>
      </FormItem>
    </FormField>

    <FormField v-slot="{ componentField }" name="email">
      <FormItem>
        <FormLabel>
          Email
          <Badge v-if="auth.user!.email_verified" variant="success" title="Verified">
            <LucideMailCheck />
          </Badge>
          <Badge v-else variant="warning" title="Not Verified. Click to re-send verification mail" class="cursor-pointer" role="button" @click="!isSendingVerificationMail && resendVerificationMail()">
            <LucideLoader v-if="isSendingVerificationMail" />
            <LucideMailX v-else />
          </Badge>
        </FormLabel>
        <FormControl>
          <Input type="email" v-bind="componentField" :disabled="isPending" />
        </FormControl>
        <FormMessage />
        <FormDescription>
          Private Email for notification
        </FormDescription>
      </FormItem>
    </FormField>

    <Button type="submit" variant="secondary" :disabled="!meta.dirty || !meta.valid || isPending">
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
