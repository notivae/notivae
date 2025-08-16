<script setup lang="ts">
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { computed, ref } from "vue";
import { useMutation } from "@tanstack/vue-query";
import { postApiAuthMfaBackupVerify } from "@/services/api/auth/mfa/backup-codes.ts";
import { useRouter } from "vue-router";
import { useQueryNext } from "@/composables/common/useQueryNext.ts";
import { ErrorBox } from "@/components/common/error-box";
import { Button } from "@/components/ui/button";
import { LucideLoader } from "lucide-vue-next";
import BackupCodeInput from "@/components/auth/BackupCodeInput.vue";
import { IconNotivaeLogo } from "@/components/icons";

definePage({
  meta: {
    requiresAuth: false,
  },
});

const CODE_LENGTH = 8;

const router = useRouter();
const nextRoute = useQueryNext();
const backupCode = ref<string>("");
const codeIsValid = computed(() => backupCode.value.length === CODE_LENGTH);

const { mutateAsync, isPending, error } = useMutation({
  mutationFn: async () => {
    await postApiAuthMfaBackupVerify({
      backup_code: backupCode.value,
    });
  },
  onSuccess: async () => {
    await router.push(nextRoute.value);
  },
});

async function handleComplete() {
  if (isPending.value) return;
  if (!codeIsValid.value) return;

  await mutateAsync();
}
</script>

<template>
  <div class="min-h-svh grid place-items-center gap-6 bg-muted p-6 md:p-10">
    <div class="flex flex-col w-full max-w-sm gap-6">
      <div class="flex items-center justify-center gap-1 self-center text-xl font-medium font-mono">
        <IconNotivaeLogo class="size-5" />
        Notivae
      </div>
      <Card class="w-full">
        <CardHeader>
          <CardTitle>
            Backup Code
          </CardTitle>
          <CardDescription>
            Enter your 8-digit backup code to continue.
          </CardDescription>
        </CardHeader>
        <CardContent class="space-y-4">
          <BackupCodeInput v-model="backupCode" :disabled="isPending" @complete="handleComplete" />
          <ErrorBox :error="error" />
          <Button :disabled="isPending || !codeIsValid" @click="handleComplete" class="w-full">
            <LucideLoader v-if="isPending" class="animate-spin" />
            Verify
          </Button>
        </CardContent>
      </Card>
    </div>
  </div>
</template>
