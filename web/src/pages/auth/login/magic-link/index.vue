<script setup lang="ts">
import { ref, watch, useTemplateRef } from "vue";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useServerFeatures } from "@/composables/api/useServerFeatures.ts";
import { useMutation } from "@tanstack/vue-query";
import { postApiAuthMagicRequest } from "@/services/api/auth/magic/request.ts";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { LucideMail, LucideMailCheck, LucideMailQuestionMark, LucideMailX } from "lucide-vue-next";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { ErrorBox } from "@/components/common/error-box";

import logoSrc from "@/assets/logo.svg";

definePage({
  meta: {
    requiresAuth: false,
    followNextIfAuthenticated: true,
  }
});

const { data: serverFeatures } = useServerFeatures();

const formRef = useTemplateRef("request-form");
const email = ref("");
const lastSentMail = ref("");
const isDirtyInput = ref(false);

watch(email, () => {
  isDirtyInput.value = true;
});

const { mutateAsync, isError, isPending, isSuccess, error } = useMutation({
  mutationKey: ['api', 'auth', 'magic', 'request'],
  mutationFn: async () => {
    return await postApiAuthMagicRequest({
      email: email.value,
    });
  },
});

function isValidForm(): boolean {
  return !!formRef.value?.checkValidity();
}

async function handleSend() {
  if (!isValidForm()) return;

  lastSentMail.value = email.value;
  isDirtyInput.value = false;
  await mutateAsync();
}
</script>

<template>
  <div class="min-h-svh grid place-items-center gap-6 bg-muted p-6 md:p-10">
    <div class="flex flex-col w-full max-w-md gap-6">
      <div class="flex items-center gap-2 self-center font-medium select-none">
        <img :src="logoSrc" alt="notivae logo" class="size-6" />
        Notivae
      </div>
      <Card>
        <CardHeader class="text-center">
          <CardTitle class="text-xl">
            Login via Magic-Link
          </CardTitle>
          <CardDescription>
            Enter your email to receive a one-time login link. No password needed.
            The link will expire after 15 minutes. Check your spam folder if it doesn't arrive.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div class="grid gap-6">
            <form ref="request-form" @submit.prevent="handleSend()" class="flex flex-col gap-4">
              <label for="email-input" class="sr-only">Email</label>
              <Input
                  v-model.trim="email"
                  id="email-input"
                  type="email"
                  required
                  :disabled="isPending"
                  placeholder="user@example.com"
                  autofocus
              />
              <Button variant="secondary" type="submit" :disabled="isPending || !isValidForm()">
                <LucideMailQuestionMark v-if="isPending" />
                <LucideMail v-else />
                Send
              </Button>
            </form>
            <Alert v-if="isSuccess && !isDirtyInput" variant="success">
              <LucideMailCheck />
              <AlertTitle>
                Magic-Link Email was sent
              </AlertTitle>
              <AlertDescription>
                An Email with a Magic-Link was sent to your email address {{ lastSentMail }}.
              </AlertDescription>
            </Alert>
            <Alert v-if="isError && !isDirtyInput" variant="destructive">
              <LucideMailX />
              <AlertTitle>
                Magic-Link Email failed to send
              </AlertTitle>
              <AlertDescription>
                <p>
                  The email could not be sent to {{ lastSentMail }}. Please check the address and try again.
                </p>
                <ErrorBox :error="error" />
              </AlertDescription>
            </Alert>
            <div v-if="serverFeatures?.account_creation !== 'closed'" class="text-center text-sm">
              Don't have an account?
              <router-link :to="{ name: '/auth/login/magic-link/register', query: { ...$route.query } }" class="underline underline-offset-4">
                Register
              </router-link>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  </div>
</template>
