<script setup lang="ts">
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger
} from "@/components/ui/dropdown-menu";
import { SettingsHeading, SettingsSection } from "@/components/settings/common";
import { useAuthStore } from "@/stores/auth.ts";
import { LucideLoader, LucidePen, LucideUserRoundX } from "lucide-vue-next";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import { computed, ref } from "vue";
import { Button } from "@/components/ui/button";
import { useMutation } from "@tanstack/vue-query";
import { toast } from "vue-sonner";
import { pickFile } from "@/lib/file-picker.ts";
import { deleteApiUsersAvatar, putApiUsersAvatar } from "@/services/api/users/avatars.ts";
import { useRenderedBlurhash } from "@/composables/common/useRenderedBlurhash.ts";

const { user, reloadAuth } = useAuthStore();

function getAvatarSrcTimeStamped() {
  // added timestamp to prevent browser-caching
  return `/api/users/${encodeURIComponent(user!.id)}/avatar?ts=${Date.now()}`;
}

const avatarSrc = ref(user!.has_avatar ? getAvatarSrcTimeStamped() : null);
const avatarBlurhashSrc = useRenderedBlurhash(() => user!.avatar_blurhash);
const loadingStatus = ref<'idle' | 'loading' | 'loaded' | 'error'>('idle');

const { mutateAsync: uploadAvatar, isPending: uploadingAvatar } = useMutation({
  mutationFn: async (imgSrc: Blob) => {
    await putApiUsersAvatar(user!.id, imgSrc);
  },
  onSuccess: async () => {
    await reloadAuth();
    avatarSrc.value = getAvatarSrcTimeStamped();
  },
  onError: (error) => {
    toast.error("Unable to upload new profile", {
      description: `${error.name}: ${error.message}`,
    });
  },
});

const { mutateAsync: removeAvatar, isPending: removingAvatar } = useMutation({
  mutationFn: async () => {
    await deleteApiUsersAvatar(user!.id);
  },
  onSuccess: async () => {
    await reloadAuth();
    avatarSrc.value = null;
  },
  onError: (error) => {
    toast.error("Unable to remove profile", {
      description: `${error.name}: ${error.message}`,
    });
  },
});

const isPending = computed(() => uploadingAvatar.value || removingAvatar.value);

async function handleUploadAvatar() {
  const imageFile = await pickFile({ accept: "image/*" });
  await uploadAvatar(imageFile);
}

async function handleRemoveAvatar() {
  await removeAvatar();
}
</script>

<template>
  <SettingsSection>
    <SettingsHeading variant="h2">
      Profile Picture
    </SettingsHeading>

    <DropdownMenu>
      <DropdownMenuTrigger class="relative cursor-pointer">
        <Avatar :key="avatarSrc ?? ''" class="size-32 rounded-xl bg-secondary">
          <template v-if="avatarSrc">
            <AvatarImage v-show="loadingStatus === 'loaded'" v-if="avatarSrc" :src="avatarSrc" @loading-status-change="(v) => loadingStatus = v" />
            <AvatarImage v-if="avatarBlurhashSrc && loadingStatus === 'loading'" :src="avatarBlurhashSrc" />
          </template>
          <AvatarFallback>
            <LucideUserRoundX class="size-full p-4 text-muted-foreground" />
          </AvatarFallback>
        </Avatar>
        <Button variant="secondary" size="icon" :disabled="isPending" class="border border-background rounded-full absolute bottom-0 left-0 -translate-x-1/5 translate-y-1/5 pointer-events-none">
          <LucideLoader v-if="isPending" class="animate-spin" />
          <LucidePen v-else />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent>
        <DropdownMenuItem :disabled="isPending" @click="handleUploadAvatar">
          Upload a photo
        </DropdownMenuItem>
        <DropdownMenuItem :disabled="isPending || !avatarSrc" @click="handleRemoveAvatar">
          Remove photo
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  </SettingsSection>
</template>
