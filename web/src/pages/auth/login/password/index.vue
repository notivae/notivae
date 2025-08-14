<script setup lang="ts">
import { ref, useTemplateRef, watch } from "vue";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useServerFeatures } from "@/composables/api/useServerFeatures.ts";
import { useMutation } from "@tanstack/vue-query";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { LucideLock, LucideLockOpen, LucideLoader, LucideArrowBigLeft } from "lucide-vue-next";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { postApiAuthLocalLogin } from "@/services/api/auth/local/login.ts";
import { useRoute, useRouter } from "vue-router";
import { ErrorBox } from "@/components/common/error-box";
import AuthLocalResetPasswordDialog from "@/components/auth/AuthLocalResetPasswordDialog.vue";
import { useQueryNext } from "@/composables/common/useQueryNext.ts";
import { IconNotivaeLogo } from "@/components/icons";

definePage({
  meta: {
    requiresAuth: false,
    followNextIfAuthenticated: true,
  }
});

const { data: serverFeatures } = useServerFeatures();
const router = useRouter();
const currentRoute = useRoute();
const nextRoute = useQueryNext();

const formRef = useTemplateRef("request-form");
const username_or_email = ref("");
const password = ref("");
const isDirtyInput = ref(false);

watch([username_or_email, password], () => {
  isDirtyInput.value = true;
});

const { mutateAsync: sendAuthentication, isError, isPending, error } = useMutation({
  mutationKey: ['api', 'auth', 'local', 'login'],
  mutationFn: async () => {
    const response = await postApiAuthLocalLogin({
      username_or_email: username_or_email.value,
      password: password.value,
    });
    if (response.data.requires_mfa) {
      await router.push({ name: "/auth/mfa/totp", query: { ...currentRoute.query } });
    } else {
      await router.push(nextRoute.value);
    }
  },
});

function isFormValid() {
  return !!formRef.value?.checkValidity();
}

async function handleSubmit() {
  if (!isFormValid()) return;

  isDirtyInput.value = false;
  await sendAuthentication();
}
</script>

<template>
  <div class="min-h-svh grid place-items-center gap-6 bg-muted p-6 md:p-10">
    <div class="flex flex-col w-full max-w-md gap-6">
      <div class="flex items-center justify-center gap-1 self-center text-xl font-medium font-mono">
        <IconNotivaeLogo class="size-5" />
        Notivae
      </div>
      <Card class="w-full relative">
        <router-link :to="{ name: '/auth/login/' }" class="absolute top-0.5 left-0.5">
          <Button variant="ghost" size="icon" class="rounded-full">
            <LucideArrowBigLeft />
          </Button>
        </router-link>
        <CardHeader class="text-center">
          <CardTitle class="text-xl">
            Login via Password
          </CardTitle>
          <CardDescription>
            Sign in using your email or username and password.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div class="grid gap-6">
            <form ref="request-form" @submit.prevent="handleSubmit" class="flex flex-col gap-4">
              <label for="username-or-email-input" class="sr-only">Username or Email</label>
              <Input
                  v-model.trim="username_or_email"
                  id="username-or-email-input"
                  required
                  placeholder="Username or Email"
                  :disabled="isPending"
                  autocomplete="username"
                  autofocus
              />
              <label for="password-input" class="sr-only">Password</label>
              <Input
                  v-model.trim="password"
                  id="password-input"
                  type="password"
                  required
                  placeholder="Password"
                  :disabled="isPending"
                  autocomplete="current-password"
              />
              <Button type="submit" variant="secondary" class="group" :disabled="isPending || !isFormValid()">
                <LucideLoader v-if="isPending" class="animate-spin" />
                <template v-else>
                  <LucideLock class="block group-hover:hidden" />
                  <LucideLockOpen class="hidden group-hover:block" />
                </template>
                {{ isPending ? "Logging in..." : "Login" }}
              </Button>
            </form>
            <Alert v-if="isError && !isDirtyInput" variant="destructive">
              <LucideLock />
              <AlertTitle>
                Authentication failed
              </AlertTitle>
              <AlertDescription>
                <p>
                  The credentials you entered are incorrect. Please try again.
                </p>
                <ErrorBox :error="error" />
              </AlertDescription>
            </Alert>
            <div class="flex justify-around items-center gap-8">
              <template v-if="serverFeatures?.account_creation !== 'closed'">
                <router-link :to="{ name: '/auth/login/password/register', query: { ...$route.query } }">
                  <Button variant="link">
                    Don't have an account?
                  </Button>
                </router-link>
              </template>
              <AuthLocalResetPasswordDialog>
                <Button variant="link">
                  Forgot Password?
                </Button>
              </AuthLocalResetPasswordDialog>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  </div>
</template>
