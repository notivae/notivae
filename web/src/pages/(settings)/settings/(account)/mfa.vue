<script setup lang="ts">
import { LucideAlertOctagon, LucideAlertTriangle, LucideFingerprint } from "lucide-vue-next";
import { useMfaDetails } from "@/composables/api/useMfaDetails.ts";
import { Button } from "@/components/ui/button";
import { RegenerateBackupCodesDialog } from "@/components/settings/mfa";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import ConfigureTOTPDialog from "@/components/settings/mfa/ConfigureTOTPDialog.vue";
import DisableTOTPDialog from "@/components/settings/mfa/DisableTOTPDialog.vue";
import { SettingsDescription, SettingsHeading, SettingsSection } from "@/components/settings/common";
import { ErrorBox } from "@/components/common/error-box";

const { data: mfaDetails, isSuccess, error } = useMfaDetails();
</script>

<template>
  <SettingsSection>
    <SettingsHeading variant="h1">
      <LucideFingerprint />
      Multi-Factor Authentication
    </SettingsHeading>
    <SettingsDescription>
      Add an extra layer of security to your account by setting up multi-factor authentication. With MFA enabled, you’ll need a second step when signing in, keeping your account safer from unauthorized access.
    </SettingsDescription>
  </SettingsSection>

  <ErrorBox :error="error" />

  <!-- Backup Codes Section -->
  <SettingsSection v-if="isSuccess">
    <SettingsHeading variant="h2">
      Backup Codes
    </SettingsHeading>

    <!-- Texts -->
    <template v-if="mfaDetails!.backup_codes_remaining !== null">
      <SettingsDescription>
        You have active backup codes configured.
        <br />
        Backup codes are single-use and should be stored securely.
        You can replace them at any time, which will invalidate the old ones.
      </SettingsDescription>
    </template>
    <template v-else>
      <SettingsDescription>
        You currently do not have any backup codes configured.
        <br />
        Backup codes allow you to log in even if you lose access to your primary MFA device.
        It is highly recommended to generate and securely store them.
      </SettingsDescription>
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
  </SettingsSection>

  <!-- TOTP Section -->
  <SettingsSection v-if="isSuccess">
    <SettingsHeading variant="h2">
      Authenticator App
    </SettingsHeading>

    <template v-if="mfaDetails!.totp">
      <SettingsDescription>
        You currently have TOTP Multi-Factor Authentication enabled.
      </SettingsDescription>
      <div class="flex justify-end">
        <DisableTOTPDialog>
          <Button variant="secondary">
            Disable MFA via TOTP
          </Button>
        </DisableTOTPDialog>
      </div>
    </template>
    <template v-else-if="mfaDetails!.backup_codes_remaining !== null && mfaDetails!.backup_codes_remaining > 0">
      <SettingsDescription>
        Protect your account by enabling an Authenticator App. This adds a time-based code as a second verification step when logging in.
      </SettingsDescription>
      <div class="flex justify-end">
        <ConfigureTOTPDialog>
          <Button variant="secondary">
            Enable MFA via TOTP
          </Button>
        </ConfigureTOTPDialog>
      </div>
    </template>
    <template v-else>
      <SettingsDescription>
        For security reasons, backup codes must be configured before enabling TOTP MFA.
        This ensures you can regain access if your primary device is lost.
      </SettingsDescription>
      <div class="flex justify-end">
        <Button disabled variant="secondary">
          Enable MFA via TOTP
        </Button>
      </div>
    </template>
  </SettingsSection>
</template>
