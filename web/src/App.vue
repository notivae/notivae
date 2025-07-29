<script setup lang="ts">
import { Toaster } from "@/components/ui/sonner";
import WSNotificationToToastListener from "@/components/singletons/WSNotificationToToastListener.vue";
</script>

<template>
  <!-- https://github.com/unovue/shadcn-vue/issues/462 -->
  <Toaster rich-colors theme="dark" :visible-toasts="5" class="pointer-events-auto" />
  <WSNotificationToToastListener />
  <Suspense>
    <router-view />
  </Suspense>
</template>
