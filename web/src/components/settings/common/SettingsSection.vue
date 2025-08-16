<script setup lang="ts">
import { Primitive } from "reka-ui";
import type { PrimitiveProps } from "reka-ui";

defineProps<PrimitiveProps>();
</script>

<template>
  <Primitive :as="as ?? 'div'" class="space-y-2">
    <slot />
  </Primitive>
</template>
