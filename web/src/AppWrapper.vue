<script setup lang="ts">
import App from "@/App.vue";
import { TooltipProvider } from "@/components/ui/tooltip";
import { useConfiguredColorMode } from "@/composables/useConfiguredColorMode.ts";

useConfiguredColorMode();
</script>

<template>
  <TooltipProvider :delay-duration="500">
    <App />
  </TooltipProvider>
</template>
