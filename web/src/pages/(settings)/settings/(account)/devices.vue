<script setup lang="ts">
import { LucideLoader, LucideMonitorSmartphone, LucideX } from "lucide-vue-next";
import { Separator } from "@/components/ui/separator";
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


const hideRevoked = ref(true);

const { data: authSessions, isPending, error, refetch: refetchAuthSessions } = useQuery({
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
</script>

<template>
  <div class="space-y-4">
    <div>
      <h2 class="text-xl font-bold">
        <LucideMonitorSmartphone class="inline-block mr-1" />
        Devices
      </h2>
      <Separator />
    </div>
    <p class="text-muted-foreground text-sm">
      Here are all devices that are currently logged in with your Notivae account.
      You can log out each one individually or all other devices. <br/>
      If you see an entry you don't recognise, log out of that device and change your Notivae account password immediately.
    </p>
    <ErrorBox :error="error" />
    <template v-if="isPending">
      <LucideLoader class="animate-spin" />
    </template>
    <template v-else>
      <Separator />
      <div class="space-y-2">
        <h3 class="text-lg font-semibold">
          Current Device
        </h3>
        <AuthSessionDeviceCard v-if="currentAuthSession" :session="currentAuthSession" />
      </div>
      <Separator />
      <div class="space-y-2">
        <h3 class="text-lg font-semibold">
          Other Devices
        </h3>
        <div class="flex justify-end">
          <div class="flex gap-1">
            <Label id="hide-revoked">Hide Revoked</Label>
            <Checkbox for="hide-revoked" v-model="hideRevoked" />
          </div>
        </div>
        <ErrorBox :error="revokeError" />
        <template v-for="session in authSessions!" :key="session.id">
          <AuthSessionDeviceCard v-if="!session.is_current && !(session.revoked && hideRevoked)" :session="session">
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
      </div>
      <Separator />
      <div class="space-y-2">
        <h3 class="text-lg font-semibold">
          Log out of all known devices
        </h3>
        <p class="text-muted-foreground text-sm">
          You'll have to log back in on all logged out devices.
        </p>
        <ErrorBox :error="revokeError" />
        <Button variant="destructive" :disabled="isRevoking" @click="revoke(authSessions!.map(s => s.id))">
          <LucideLoader v-if="isPending" />
          Log Out All Known Devices
        </Button>
      </div>
    </template>
  </div>
</template>
