<script setup lang="ts">
import { toast } from "vue-sonner";
import { useWebSocketEvent } from "@/composables/useWebSocketEvent.ts";

useWebSocketEvent("notification", (notification) => {
  toast.message(notification.title, {
    description: notification.message,
  });
});
</script>

<template></template>
