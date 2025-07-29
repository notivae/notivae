<script setup lang="ts">
import { ref, watch, useTemplateRef } from "vue";
import { LucideLoader, LucideUserRound, LucideUserRoundPlus, LucideUserRoundX } from "lucide-vue-next";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useServerFeatures } from "@/composables/useServerFeatures.ts";
import { useMutation } from "@tanstack/vue-query";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { AxiosError } from "axios";
import { postApiAuthMagicRegister } from "@/services/api/auth/magic/register.ts";

import logoSrc from "@/assets/logo.svg";

definePage({
  meta: {
    requiresAuth: false,
    followNextIfAuthenticated: true,
  }
});

const { data: serverFeatures } = useServerFeatures();

const { mutateAsync, isError, isPending, isSuccess, error } = useMutation({
  mutationKey: ['api', 'auth', 'magic', 'register'],
  mutationFn: async () => {
    return await postApiAuthMagicRegister({
      new_user: {
        username: username.value,
        display_name: displayName.value,
      },
      email: email.value,
    });
  },
  onSuccess: () => {
    email.value = "";
    username.value = "";
    displayName.value = "";
  }
});

function isValidForm(): boolean {
  return !!formRef.value?.checkValidity();
}

async function handleSend() {
  if (!isValidForm()) return;

  isDirtyInput.value = false;
  await mutateAsync();
}

const formRef = useTemplateRef("request-form");
const username = ref("");
const displayName = ref("");
const email = ref("");
const isDirtyInput = ref(false);

watch([username, displayName, email], () => {
  isDirtyInput.value = true;
});
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
            Create Account via Magic-Link
          </CardTitle>
          <CardDescription>
            Enter your email to create an account using a one-time login link.
            Check your spam or junk folder if you don't see the email.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div class="grid gap-6">
            <form ref="request-form" @submit.prevent="handleSend()" class="flex flex-col gap-4">
              <fieldset class="flex flex-col gap-1">
                <Label for="email-input">
                  Email
                </Label>
                <Input
                    v-model="email"
                    id="email-input"
                    type="email"
                    required
                    :disabled="isPending"
                    placeholder="john@company.com"
                    autofocus
                />
              </fieldset>
              <fieldset class="flex flex-col gap-1">
                <Label for="username-input">Username</Label>
                <Input
                    v-model="username"
                    id="username-input"
                    required
                    :disabled="isPending"
                    placeholder="johndoe"
                />
              </fieldset>
              <fieldset class="flex flex-col gap-1">
                <Label for="display-name-input">Display Name</Label>
                <Input
                    v-model="displayName"
                    id="display-name-input"
                    required
                    :disabled="isPending"
                    placeholder="John Doe"
                />
              </fieldset>
              <Button variant="secondary" type="submit" class="group" :disabled="isPending || !isValidForm()">
                <LucideLoader v-if="isPending" class="animate-spin" />
                <template v-else>
                  <LucideUserRound class="block group-hover:hidden" />
                  <LucideUserRoundPlus class="hidden group-hover:block" />
                </template>
                {{ serverFeatures?.account_creation === 'open' ? "Create Account" : "Request Account" }}
              </Button>
            </form>
            <Alert v-if="isSuccess && !isDirtyInput" variant="success">
              <LucideUserRound />
              <AlertTitle>
                Magic-Link confirmation Email was sent
              </AlertTitle>
              <AlertDescription>
                We've sent a magic login link to your email. Please check your inbox (and spam folder).
              </AlertDescription>
            </Alert>
            <Alert v-if="isError && !isDirtyInput" variant="destructive">
              <LucideUserRoundX />
              <AlertTitle>
                Unable to register via Magic-Link
              </AlertTitle>
              <AlertDescription>
                <p>
                  Please check your input or try again later.
                </p>
                <p v-if="error instanceof AxiosError" class="font-mono text-sm">
                  ({{ error.response?.status }}: {{ error.response?.data.detail }})
                </p>
              </AlertDescription>
            </Alert>
            <div v-if="serverFeatures?.account_creation !== 'closed'" class="text-center text-sm">
              Already have an account?
              <router-link :to="{ name: '/auth/login/', query: { ...$route.query } }" class="underline underline-offset-4">
                Log in instead
              </router-link>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  </div>
</template>
