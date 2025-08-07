<script setup lang="ts">
import { AxiosError, HttpStatusCode } from "axios";

defineProps<{
  error: unknown
}>();

function formatSeconds(seconds: number) {
  if (seconds === undefined) return "~unknown~";
  if (seconds < 60) return seconds.toString();
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
}
</script>

<template>
  <p v-if="error !== null && error !== undefined" class="font-mono text-sm text-destructive-foreground/90">
    <template v-if="error instanceof AxiosError">
      <template v-if="error.response?.status === HttpStatusCode.TooManyRequests">
        You are currently doing too many requests.
        Try again in {{ formatSeconds(error.response?.headers["retry-after"]) }}.
      </template>
      <template v-else-if="error.response?.status === HttpStatusCode.Conflict">
        You stumbled across a conflict. Not sure how to handle that.
      </template>
      <template v-else-if="error.response?.status === HttpStatusCode.InternalServerError">
        The server has encountered a situation it does not know how to handle.
      </template>
      <template v-else-if="error.response?.status === HttpStatusCode.ServiceUnavailable">
        This service is currently unavailable.
      </template>
      <template v-else>
        ({{ error.response?.status }}: {{ error.response?.data.detail }})
      </template>
    </template>
    <template v-else-if="error instanceof Error">
      {{ error.name }}: {{ error.message }}
    </template>
    <template>
      {{ error }}
    </template>
  </p>
</template>
