<script setup lang="ts">
import logoSrc from "@/assets/logo.svg";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { computed, ref } from "vue";
import { useMutation } from "@tanstack/vue-query";
import { postApiAuthMFATotpVerify } from "@/services/api/auth/mfa/totp.ts";
import { useRouter } from "vue-router";
import { useQueryNext } from "@/composables/common/useQueryNext.ts";
import { ErrorBox } from "@/components/common/error-box";
import { Button } from "@/components/ui/button";
import { LucideLoader } from "lucide-vue-next";
import OtpPinInput from "@/components/auth/OtpPinInput.vue";

definePage({
  meta: {
    requiresAuth: false,
  },
});

const PIN_LENGTH = 6;

const router = useRouter();
const nextRoute = useQueryNext();
const otp = ref<string>("");
const otpIsValid = computed(() => otp.value.length === PIN_LENGTH);

const { mutateAsync, isPending, error } = useMutation({
  mutationFn: async () => {
    await postApiAuthMFATotpVerify({
      otp: otp.value,
    });
  },
  onSuccess: async () => {
    await router.push(nextRoute.value);
  },
});

async function handleComplete() {
  if (isPending.value) return;
  if (!otpIsValid.value) return;

  await mutateAsync();
}
</script>

<template>
  <div class="min-h-svh grid place-items-center gap-6 bg-muted p-6 md:p-10">
    <div class="flex flex-col w-full max-w-sm gap-6">
      <div class="flex items-center gap-2 self-center font-medium select-none">
        <img :src="logoSrc" alt="notivae logo" class="size-6" />
        Notivae
      </div>
      <Card class="w-full">
        <CardHeader>
          <CardTitle>
            Two-Factor Authentication
          </CardTitle>
          <CardDescription>
            Enter the 6-digit verification code from your authenticator app to continue.
          </CardDescription>
        </CardHeader>
        <CardContent class="space-y-4">
          <OtpPinInput v-model="otp" :disabled="isPending" @complete="handleComplete" />
          <div class="flex justify-around items-center gap-8">
            <router-link :to="{ name: '/auth/mfa/backup-code', query: { ...$route.query } }">
              <Button variant="link" size="sm">
                I want to use a backup code
              </Button>
            </router-link>
          </div>
          <ErrorBox :error="error" />
          <Button :disabled="isPending || !otpIsValid" @click="handleComplete" class="w-full">
            <LucideLoader v-if="isPending" class="animate-spin" />
            Verify
          </Button>
        </CardContent>
      </Card>
    </div>
  </div>
</template>
