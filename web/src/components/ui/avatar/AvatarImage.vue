<script setup lang="ts">
import type { AvatarImageProps, AvatarImageEmits } from 'reka-ui'
import { AvatarImage, useForwardPropsEmits } from 'reka-ui'

const props = defineProps<AvatarImageProps>()

const emits = defineEmits<AvatarImageEmits>();

const forwardedProps = useForwardPropsEmits(props, emits);
</script>

<template>
  <AvatarImage
    data-slot="avatar-image"
    v-bind="forwardedProps"
    class="aspect-square size-full"
  >
    <slot />
  </AvatarImage>
</template>
