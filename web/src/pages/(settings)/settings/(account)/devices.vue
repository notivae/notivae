<script setup lang="ts">
import { LucideLoader, LucideMonitorSmartphone, LucideX } from "lucide-vue-next";
import { useMutation, useQuery } from "@tanstack/vue-query";
import { getApiAuthSessions } from "@/services/api/auth/sessions";
import { computed, ref } from "vue";
import { Button } from "@/components/ui/button";
import { postApiAuthSessionsRevoke } from "@/services/api/auth/sessions/revoke.ts";
import { AuthSessionDeviceCard } from "@/components/settings/devices";
import { Tooltip, TooltipTrigger, TooltipContent } from "@/components/ui/tooltip";
import { ErrorBox } from "@/components/common/error-box";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import { SettingsDescription, SettingsHeading, SettingsSection } from "@/components/settings/common";


const hideRevoked = ref(true);

const { data: authSessions, isPending, isSuccess, error, refetch: refetchAuthSessions } = useQuery({
  queryKey: ["api", "auth", "sessions"],
  queryFn: async () => {
    const response = await getApiAuthSessions();
    return response.data.sort((a, b) => a.id - b.id);
  },
  retry: false,
});

const { mutateAsync: revoke, isPending: isRevoking, error: revokeError } = useMutation({
  mutationFn: async (ids: number[]) => {
    await postApiAuthSessionsRevoke({
      session_ids: ids,
    });
  },
  onSuccess: async () => {
    await refetchAuthSessions()
  },
});

const currentAuthSession = computed(() => authSessions.value?.find(s => s.is_current));

const otherAuthSessions = computed(() => {
  return authSessions.value?.filter(s => !s.is_current && !(s.revoked && hideRevoked.value))
});
</script>

<template>
  <SettingsSection>
    <SettingsHeading variant="h1">
      <LucideMonitorSmartphone />
      Devices
    </SettingsHeading>
    <SettingsDescription>
      Here are all devices that are currently logged in with your Notivae account.
      You can log out each one individually or all other devices. <br/>
      If you see an entry you don't recognise, log out of that device and change your Notivae account password immediately.
    </SettingsDescription>
  </SettingsSection>

  <ErrorBox :error="error" />

  <template v-if="isPending">
    <LucideLoader class="animate-spin" />
  </template>
  <template v-else-if="isSuccess">
    <SettingsSection>
      <SettingsHeading variant="h2">
        Current Device
      </SettingsHeading>
      <AuthSessionDeviceCard v-if="currentAuthSession" :session="currentAuthSession" />
    </SettingsSection>

    <SettingsSection>
      <SettingsHeading variant="h2">
        Other Devices
        <div class="flex gap-1 ml-auto">
          <Label id="hide-revoked">Hide Revoked</Label>
          <Checkbox for="hide-revoked" v-model="hideRevoked" />
        </div>
      </SettingsHeading>
      <ErrorBox :error="revokeError" />
      <template v-for="session in otherAuthSessions!" :key="session.id">
        <AuthSessionDeviceCard v-memo="[session.revoked]" :session="session">
          <template #actions>
            <Tooltip>
              <TooltipTrigger>
                <Button
                    variant="ghost"
                    size="icon"
                    :disabled="isRevoking || session.revoked"
                    @click="revoke([session.id])"
                    class="rounded-full hover:text-destructive"
                >
                  <LucideX />
                </Button>
              </TooltipTrigger>
              <TooltipContent>
                <template v-if="session.revoked">
                  Already Revoked
                </template>
                <template v-else>
                  Revoke Access
                </template>
              </TooltipContent>
            </Tooltip>
          </template>
        </AuthSessionDeviceCard>
      </template>
      <div v-if="!otherAuthSessions!.length" class="text-muted-foreground text-sm">
        There are no other devices.
      </div>
    </SettingsSection>

    <SettingsSection>
      <SettingsHeading variant="h2">
        Log out of all known devices
      </SettingsHeading>
      <SettingsDescription>
        You'll have to log back in on all logged out devices.
      </SettingsDescription>
      <ErrorBox :error="revokeError" />
      <Button variant="destructive" :disabled="isRevoking" @click="revoke(authSessions!.map(s => s.id))">
        <LucideLoader v-if="isPending" />
        Log Out All Known Devices
      </Button>
    </SettingsSection>
  </template>
</template>
