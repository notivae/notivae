<script setup lang="ts">
import { AxiosError } from "axios";

defineProps<{
  error: unknown
}>();
</script>

<template>
  <p v-if="error !== null && error !== undefined" class="font-mono text-sm text-destructive-foreground">
    <template v-if="error instanceof AxiosError">
      ({{ error.response?.status }}: {{ error.response?.data.detail }})
    </template>
    <template v-else-if="error instanceof Error">
      {{ error.name }}: {{ error.message }}
    </template>
    <template>
      {{ error }}
    </template>
  </p>
</template>
