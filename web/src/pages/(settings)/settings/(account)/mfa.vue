<script setup lang="ts">
import { Separator } from "@/components/ui/separator";
import { LucideAlertOctagon, LucideAlertTriangle, LucideFingerprint } from "lucide-vue-next";
import { useMfaDetails } from "@/composables/api/useMfaDetails.ts";
import { Button } from "@/components/ui/button";
import { RegenerateBackupCodesDialog } from "@/components/settings/mfa";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import ConfigureTOTPDialog from "@/components/settings/mfa/ConfigureTOTPDialog.vue";
import DisableTOTPDialog from "@/components/settings/mfa/DisableTOTPDialog.vue";

const { data: mfaDetails, isSuccess } = useMfaDetails();
</script>

<template>
  <div v-if="isSuccess" class="space-y-4">
    <div>
      <h2 class="text-xl font-bold">
        <LucideFingerprint class="inline-block mr-1" />
        Multi-Factor Authentication
      </h2>
      <Separator />
    </div>

    <!-- Backup Codes Section -->
    <div class="space-y-2">
      <div>
        <h3 class="text-lg font-semibold">
          Backup Codes
        </h3>
        <Separator />
      </div>

      <!-- Texts -->
      <template v-if="mfaDetails!.backup_codes_remaining !== null">
        <p>
          You have active backup codes configured.
        </p>
        <p>
          Backup codes are single-use and should be stored securely.
          You can replace them at any time, which will invalidate the old ones.
        </p>
      </template>
      <template v-else>
        <p>
          You currently do not have any backup codes configured.
        </p>
        <p>
          Backup codes allow you to log in even if you lose access to your primary MFA device.
          It is highly recommended to generate and securely store them.
        </p>
      </template>

      <!-- Warnings -->
      <template v-if="mfaDetails!.backup_codes_remaining !== null">
        <Alert v-if="mfaDetails!.backup_codes_remaining <= 3" variant="destructive">
          <LucideAlertOctagon />
          <AlertTitle>
            Critical: You’re almost out of backup codes!
          </AlertTitle>
          <AlertDescription>
            It's strongly recommended to regenerate your backup codes now to avoid being locked out of your account.
          </AlertDescription>
        </Alert>
        <Alert v-else-if="mfaDetails!.backup_codes_remaining <= 6" variant="warning">
          <LucideAlertTriangle />
          <AlertTitle>
            You're running low on backup codes.
          </AlertTitle>
        </Alert>
      </template>

      <!-- Actions -->
      <div class="flex justify-end">
        <RegenerateBackupCodesDialog>
          <Button variant="secondary">
            <template v-if="mfaDetails!.backup_codes_remaining === null">
              Generate your backup codes
            </template>
            <template v-else>
              Replace your backup codes
            </template>
          </Button>
        </RegenerateBackupCodesDialog>
      </div>
    </div>

    <!-- TOTP Section -->
    <div class="space-y-2">
      <div>
        <h3 class="text-lg font-semibold">
          Authenticator App
        </h3>
        <Separator />
      </div>
      <template v-if="mfaDetails!.totp">
        <p>
          You currently have TOTP Multi-Factor Authentication enabled.
        </p>
        <div class="flex justify-end">
          <DisableTOTPDialog>
            <Button variant="secondary">
              Disable MFA via TOTP
            </Button>
          </DisableTOTPDialog>
        </div>
      </template>
      <template v-else-if="mfaDetails!.backup_codes_remaining !== null && mfaDetails!.backup_codes_remaining > 0">
        <p>
          Protect your account by enabling an Authenticator App. This adds a time-based code as a second verification step when logging in.
        </p>
        <div class="flex justify-end">
          <ConfigureTOTPDialog>
            <Button variant="secondary">
              Enable MFA via TOTP
            </Button>
          </ConfigureTOTPDialog>
        </div>
      </template>
      <template v-else>
        <p>
          For security reasons, backup codes must be configured before enabling TOTP MFA.
          This ensures you can regain access if your primary device is lost.
        </p>
        <div class="flex justify-end">
          <Button disabled variant="secondary">
            Enable MFA via TOTP
          </Button>
        </div>
      </template>
    </div>
  </div>
</template>
