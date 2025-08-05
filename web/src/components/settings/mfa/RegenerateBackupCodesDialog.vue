<script setup lang="ts">
import { AlertDialog, AlertDialogTrigger, AlertDialogTitle, AlertDialogDescription, AlertDialogContent, AlertDialogFooter, AlertDialogHeader } from "@/components/ui/alert-dialog";
import { useMutation } from "@tanstack/vue-query";
import { postApiAuthMfaBackupRegenerate } from "@/services/api/auth/mfa/backup-codes.ts";
import { computed, ref, watch } from "vue";
import type { BackupCodes } from "@/types/api.ts";
import { Button } from "@/components/ui/button";
import { useClipboard, whenever } from "@vueuse/core";
import { LucideClipboardCheck, LucideClipboardCopy, LucideFileDown, LucideLoader } from "lucide-vue-next";
import { ErrorBox } from "@/components/common/error-box";
import { browserDownloadStringAsFile } from "@/lib/dynamic-download.ts";
import { useMfaDetails } from "@/composables/api/useMfaDetails.ts";
import { logicAnd, logicNot } from "@vueuse/math";

const { refetch: refetchMfaInfo } = useMfaDetails();
const backupCodes = ref<BackupCodes>([]);
const backupCodesJoined = computed<string>(() => backupCodes.value.join("\n"));
const { copy, copied: recentlyCopied, isSupported: clipboardSupported } = useClipboard({ source: backupCodesJoined });
const isOpen = ref(false);

watch(isOpen, () => {
  backupCodes.value = [];
});

const { mutateAsync: regenerateBackupCodes, isSuccess, isPending, error } = useMutation({
  mutationFn: async () => {
    const response = await postApiAuthMfaBackupRegenerate();
    backupCodes.value = response.data.backup_codes;
  },
});

whenever(logicAnd(isSuccess, logicNot(isOpen)), async () => {
  await refetchMfaInfo();
});

async function handleGenerate() {
  await regenerateBackupCodes();
}

async function startDownload() {
  browserDownloadStringAsFile(backupCodesJoined.value, "backup-codes.txt");
}
</script>

<template>
  <AlertDialog v-model:open="isOpen">
    <AlertDialogTrigger as-child>
      <slot />
    </AlertDialogTrigger>
    <AlertDialogContent>
      <AlertDialogHeader>
        <AlertDialogTitle>
          Regenerate Backup Codes?
        </AlertDialogTitle>
        <AlertDialogDescription>
          This will replace and invalidate your existing backup codes. Ensure you download or copy the new codes now, as they will not be shown again.
        </AlertDialogDescription>
      </AlertDialogHeader>
      <template v-if="backupCodes.length > 0">
        <div class="grid grid-cols-2 place-items-center gap-y-0.5 gap-x-2 w-fit mx-auto">
          <template v-for="backupCode of backupCodes" :key="backupCode">
            <Button variant="ghost" @click="copy(backupCode)" class="font-semibold">
              {{ backupCode.slice(0, 4) }}&nbsp;{{ backupCode.slice(4) }}
            </Button>
          </template>
        </div>
      </template>
      <ErrorBox :error="error" />
      <AlertDialogFooter>
        <Button variant="outline" @click="isOpen = false">
          Close
        </Button>
        <template v-if="backupCodes.length === 0">
          <Button variant="secondary" @click="handleGenerate" :disabled="isPending">
            <LucideLoader v-if="isPending" class="animate-spin" />
            {{ isPending ? "Generating codes..." : "Generate Backup Codes" }}
          </Button>
        </template>
        <template v-else>
          <Button v-if="clipboardSupported" variant="secondary" @click="copy()">
            <LucideClipboardCheck v-if="recentlyCopied" />
            <LucideClipboardCopy v-else />
            Copy Codes
          </Button>
          <Button variant="secondary" @click="startDownload">
            <LucideFileDown />
            Download Codes
          </Button>
        </template>
      </AlertDialogFooter>
    </AlertDialogContent>
  </AlertDialog>
</template>
