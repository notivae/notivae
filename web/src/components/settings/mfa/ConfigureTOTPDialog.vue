<script setup lang="ts">
import { AlertDialog, AlertDialogFooter, AlertDialogHeader, AlertDialogContent, AlertDialogTrigger, AlertDialogDescription, AlertDialogTitle } from "@/components/ui/alert-dialog";
import { Button } from "@/components/ui/button";
import { ref } from "vue";
import { useMutation } from "@tanstack/vue-query";
import {
  postApiAuthMFATotpConfirm,
  postApiAuthMFATotpInit,
} from "@/services/api/auth/mfa/totp.ts";
import { ErrorBox } from "@/components/common/error-box";
import { computedAsync, whenever } from "@vueuse/core";
import { LucideLoader, LucideRectangleEllipsis, LucideScanQrCode, LucideTabletSmartphone } from "lucide-vue-next";
import OtpPinInput from "@/components/auth/OtpPinInput.vue";
import { useMfaDetails } from "@/composables/api/useMfaDetails.ts";
import { logicAnd, logicNot } from "@vueuse/math";
import { Input } from "@/components/ui/input";
import { toDataURL as createQrDataURL } from "qrcode";
import { Separator } from "@/components/ui/separator";

const { refetch: refetchMfaInfo } = useMfaDetails();
const isOpen = ref(false);
const otp = ref("");

const { data: totpInit, mutateAsync: initTotpMfa, isPending: isInitializing, error: initError } = useMutation({
  mutationFn: async () => {
    const response = await postApiAuthMFATotpInit();
    return response.data;
  },
});

const { mutateAsync: verifyOtp, isPending: isVerifying, isSuccess: isVerified, error: verifyError } = useMutation({
  mutationFn: async () => {
    await postApiAuthMFATotpConfirm({
      otp: otp.value,
    });
  },
});

whenever(isOpen, async () => {
  await initTotpMfa();
});
whenever(logicAnd(isVerified, logicNot(isOpen)), async () => {
  await refetchMfaInfo();
});

const qrCodeSrc = computedAsync(async () => {
  if (!totpInit) return null;
  return await createQrDataURL(totpInit.value!.provisioning_uri, {
    scale: 8,
    margin: 0,
    color: { light: "#0000" },  // hide background-color
  });
});

async function handleComplete() {
  await verifyOtp();
}
</script>

<template>
  <AlertDialog v-model:open="isOpen">
    <AlertDialogTrigger as-child>
      <slot />
    </AlertDialogTrigger>
    <AlertDialogContent>
      <template v-if="isInitializing">
        <LucideLoader class="animate-spin mx-auto" />
      </template>
      <template v-else-if="initError">
        <ErrorBox :error="initError" />
      </template>
      <template v-else-if="isVerified">
        2FA setup complete. Your account is now protected with an extra layer of security.
      </template>
      <template v-else>
        <AlertDialogHeader>
          <AlertDialogTitle>
            Enable Two-Factor Authentication (2FA)
          </AlertDialogTitle>
          <AlertDialogDescription>
            This process will activate Time-based One-Time Passwords (TOTP) for stronger account protection.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <Separator />
        <div class="space-y-1">
          <h3 class="text-sm font-medium">
            <LucideTabletSmartphone class="inline-block size-5" />
            Install an Authenticator App
          </h3>
          <p class="text-muted-foreground text-sm">
            You’ll need a TOTP-compatible app on your mobile device (e.g., Google Authenticator, Authy, Microsoft Authenticator) to scan a QR code and generate secure codes.
          </p>
        </div>
        <Separator />
        <div class="space-y-1">
          <h3 class="text-sm font-medium">
            <LucideScanQrCode class="inline-block size-5" />
            Scan the QR Code
          </h3>
          <p class="text-muted-foreground text-sm">
            Use your authenticator app to scan the QR code below. This will automatically add your account for generating login codes.
          </p>
          <img
              v-if="qrCodeSrc"
              :src="qrCodeSrc"
              alt="QR Code"
              class="mx-auto my-4 w-full max-w-60 aspect-square rendering-pixelated dark:invert"
              style="image-rendering: pixelated;"
          />
          <p class="text-muted-foreground text-sm">
            Alternatively, you can enter this secret key manually into your 2FA app if scanning the QR code fails.
          </p>
          <Input readonly :model-value="totpInit!.secret" class="select-all" />
        </div>
        <Separator />
        <div class="space-y-1">
          <h3 class="text-sm font-medium">
            <LucideRectangleEllipsis class="inline-block size-5" />
            Enter Verification Code
          </h3>
          <p class="text-muted-foreground text-sm">
            Enter the 6-digit code from your authenticator app to verify and complete setup.
          </p>
          <OtpPinInput v-model="otp" @complete="handleComplete" />
          <ErrorBox :error="verifyError" />
        </div>
        <Separator />
      </template>
      <AlertDialogFooter>
        <Button variant="outline" :disabled="isVerifying" @click="isOpen = false">
          <template v-if="isVerified">
            Finish Setup
          </template>
          <template v-else>
            Cancel Setup
          </template>
        </Button>
      </AlertDialogFooter>
    </AlertDialogContent>
  </AlertDialog>
</template>
