<script setup lang="ts">
import { ref, watch, useTemplateRef, computed } from "vue";
import { LucideLoader, LucideUserRound, LucideUserRoundPlus, LucideUserRoundX } from "lucide-vue-next";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useServerFeatures } from "@/composables/api/useServerFeatures.ts";
import { useMutation } from "@tanstack/vue-query";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { postApiAuthLocalRegister } from "@/services/api/auth/local/register.ts";
import { useRouter } from "vue-router";
import { ErrorBox } from "@/components/common/error-box";

import logoSrc from "@/assets/logo.svg";

definePage({
  meta: {
    requiresAuth: false,
    followNextIfAuthenticated: true,
  }
});

const router = useRouter();
const { data: serverFeatures } = useServerFeatures();

const formRef = useTemplateRef("request-form");
const username = ref("");
const displayName = ref("");
const password = ref("");
const passwordRepeated = ref("");
const arePasswordsTheSame = computed(() => password.value === passwordRepeated.value);
const email = ref("");
const isDirtyInput = ref(false);

watch([username, displayName, password, passwordRepeated, email], () => {
  isDirtyInput.value = true;
});

const { mutateAsync, isError, isPending, error } = useMutation({
  mutationKey: ['api', 'auth', 'local', 'register'],
  mutationFn: async () => {
    if (!arePasswordsTheSame.value) {
      throw new Error("The password does not match the repeated value");
    }

    return await postApiAuthLocalRegister({
      username: username.value,
      display_name: displayName.value,
      password: password.value,
      email: email.value,
    });
  },
  onSuccess: async () => {
    username.value = "";
    displayName.value = "";
    password.value = "";
    passwordRepeated.value = "";
    email.value = "";
    await router.push({ name: "/auth/login/password/" });
  }
});

function isValidForm(): boolean {
  return !!formRef.value?.checkValidity() && arePasswordsTheSame.value;
}

async function handleSubmit() {
  if (isPending.value) return;
  if (!isValidForm()) return;

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
      <Card class="w-full">
        <CardHeader class="text-center">
          <CardTitle class="text-xl">
            Create Account via Password
          </CardTitle>
          <CardDescription>
            Sign up with your email and a password to start using Notivae.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div class="grid gap-6">
            <form ref="request-form" @submit.prevent="handleSubmit" class="flex flex-col gap-4">
              <fieldset class="flex flex-col gap-1">
                <Label for="email-input">
                  Email
                </Label>
                <Input
                    v-model.trim="email"
                    id="email-input"
                    type="email"
                    required
                    :disabled="isPending"
                    placeholder="john@company.com"
                    autocomplete="email"
                    autofocus
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
              <fieldset class="flex flex-col gap-1">
                <Label for="display-name-input">Display Name</Label>
                <Input
                    v-model.trim="displayName"
                    id="display-name-input"
                    required
                    :disabled="isPending"
                    placeholder="John Doe"
                />
              </fieldset>
              <fieldset class="flex flex-col gap-1">
                <Label for="password-input">Password</Label>
                <Input
                    v-model.trim="password"
                    id="password-input"
                    type="password"
                    required
                    :disabled="isPending"
                    :aria-invalid="isDirtyInput && (password.length || passwordRepeated.length) && !arePasswordsTheSame"
                    placeholder="******"
                    autocomplete="new-password"
                />
              </fieldset>
              <fieldset class="flex flex-col gap-1">
                <Label for="password-repeated-input">Password (repeated)</Label>
                <Input
                    v-model.trim="passwordRepeated"
                    id="password-repeated-input"
                    type="password"
                    required
                    :disabled="isPending"
                    :aria-invalid="isDirtyInput && (password.length || passwordRepeated.length) && !arePasswordsTheSame"
                    placeholder="******"
                    autocomplete="new-password"
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
            <Alert v-if="isError && !isDirtyInput" variant="destructive">
              <LucideUserRoundX />
              <AlertTitle>
                Unable to register via Password
              </AlertTitle>
              <AlertDescription>
                <p>
                  Please check your input or try again later.
                </p>
                <ErrorBox :error="error" />
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
