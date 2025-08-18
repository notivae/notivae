<script setup lang="ts">
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { useRenderedBlurhash } from "@/composables/common/useRenderedBlurhash.ts";
import { computed, ref } from "vue";

const props = defineProps<{
  userId: string
  name: string
  avatarBlurhash: null | string
}>();

const avatarBlurhashSrc = useRenderedBlurhash(() => props.avatarBlurhash);
const avatarSrc = computed(() => props.userId ? `/api/users/${encodeURIComponent(props.userId)}/avatar` : null);
const loadingStatus = ref<'idle' | 'loading' | 'loaded' | 'error'>('idle');
</script>

<template>
  <Avatar class="size-8 rounded-lg">
    <template v-if="avatarSrc">
      <AvatarImage v-show="loadingStatus === 'loaded'" :src="avatarSrc" @loading-status-change="(v) => loadingStatus = v" />
      <AvatarImage v-if="avatarBlurhashSrc && loadingStatus === 'loading'" :src="avatarBlurhashSrc" />
    </template>
    <AvatarFallback class="rounded-lg">
      {{ name[0].toUpperCase() }}
    </AvatarFallback>
  </Avatar>
</template>
