<script setup lang="ts">
import { Toaster } from "@/components/ui/sonner";
</script>

<template>
  <!-- https://github.com/unovue/shadcn-vue/issues/462 -->
  <Toaster rich-colors theme="dark" :visible-toasts="5" class="pointer-events-auto" />
  <router-view />
</template>
