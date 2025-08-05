<script setup lang="ts">
import { Separator } from "@/components/ui/separator";
import { LucideAlertOctagon, LucideAlertTriangle, LucideFingerprint } from "lucide-vue-next";
import { useMfaDetails } from "@/composables/api/useMfaDetails.ts";
import { Button } from "@/components/ui/button";
import { RegenerateBackupCodesDialog } from "@/components/settings/mfa";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";

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

      <template v-if="mfaDetails!.backup_codes_remaining !== null">
        <p>
          You have active backup codes configured. Backup codes are single-use and should be stored securely.
          You can replace them at any time, which will invalidate the old ones.
        </p>
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
        <div class="flex justify-end">
          <RegenerateBackupCodesDialog>
            <Button variant="secondary">
              Replace your backup codes
            </Button>
          </RegenerateBackupCodesDialog>
        </div>
      </template>
      <template v-else>
        <p>
          You currently do not have any backup codes configured. Backup codes allow you to log in even if you lose access to your primary MFA device.
          It is highly recommended to generate and securely store them.
        </p>
        <div>
          <RegenerateBackupCodesDialog>
            <Button variant="secondary">
              Generate your backup codes
            </Button>
          </RegenerateBackupCodesDialog>
        </div>
      </template>
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
        // Action: Button "Disable TOTP MFA"
      </template>
      <template v-else-if="mfaDetails!.backup_codes_remaining !== null && mfaDetails!.backup_codes_remaining > 0">
        // Action: Button -> Dialog "Enable TOTP MFA"
      </template>
      <template>
        // No Actions.
        // Message: "Ensure you have backup-codes configured"
      </template>
    </div>
  </div>
</template>
