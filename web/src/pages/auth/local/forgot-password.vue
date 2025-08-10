<script setup lang="ts">
import logoSrc from "@/assets/logo.svg";
import { useRoute, useRouter } from "vue-router";
import { computed, ref } from "vue";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { ErrorBox } from "@/components/common/error-box";
import { Button } from "@/components/ui/button";
import { LucideCircleX, LucideLoader } from "lucide-vue-next";
import { Input } from "@/components/ui/input";
import { useMutation } from "@tanstack/vue-query";
import { postApiAuthLocalChangePassword } from "@/services/api/auth/local/change-password.ts";

definePage({
  meta: {
    requiresAuth: false,
    followNextIfAuthenticated: true,
  },
});

const router = useRouter();
const currentRoute = useRoute();
const resetToken = computed(() => currentRoute.query.token as string);

const password = ref("");
const isDirtyInput = ref(false);

const { mutateAsync, isPending, isError, error } = useMutation({
  mutationFn: async () => {
    await postApiAuthLocalChangePassword({
      new_password: password.value,
      token: resetToken.value,
    });
  },
  onSuccess: async () => {
    await router.push({ name: '/auth/login/password/' });
  }
});

async function handleSubmit() {
  if (isPending.value) return;

  await mutateAsync();
}
</script>

<template>
  <div class="min-h-svh grid place-items-center gap-6 bg-muted p-6 md:p-10">
    <div class="flex flex-col w-full max-w-md gap-6">
      <div class="flex items-center gap-2 self-center font-medium">
        <img :src="logoSrc" alt="notivae logo" class="size-6" />
        Notivae
      </div>
      <Card class="w-full">
        <CardHeader class="text-center">
          <CardTitle class="text-xl">
            Reset you Password
          </CardTitle>
          <CardDescription>
            Enter your new password below. After setting it, you'll be able to log in with your new credentials.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div class="grid gap-6">
            <form ref="request-form" @submit.prevent="handleSubmit" class="flex flex-col gap-4">
              <label for="password-input" class="sr-only">New Password</label>
              <Input
                  v-model.trim="password"
                  id="password-input"
                  type="password"
                  required
                  placeholder="Password"
                  :disabled="isPending"
                  autocomplete="current-password"
              />
              <Button type="submit" variant="secondary" class="group" :disabled="isPending">
                <LucideLoader v-if="isPending" class="animate-spin" />
                Set Password
              </Button>
            </form>
            <Alert v-if="isError && !isDirtyInput" variant="destructive">
              <LucideCircleX />
              <AlertTitle>
                Password Reset failed
              </AlertTitle>
              <AlertDescription>
                <p>
                  The password reset link may be invalid, expired, or already used. Please request a new one and try again.
                </p>
                <ErrorBox :error="error" />
              </AlertDescription>
            </Alert>
          </div>
        </CardContent>
      </Card>
      <Alert v-if="!resetToken" variant="destructive">
        <LucideCircleX />
        <AlertTitle>
          Missing reset token!
        </AlertTitle>
        <AlertDescription>
          The reset token seems to be missing. Ensure you visited this page via the link from your mail.
        </AlertDescription>
      </Alert>
    </div>
  </div>
</template>
