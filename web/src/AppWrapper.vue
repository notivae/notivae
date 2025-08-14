<script setup lang="ts">
import App from "@/App.vue";
import { TooltipProvider } from "@/components/ui/tooltip";
import { useColorMode } from "@vueuse/core";

useColorMode({ writeDefaults: false });
</script>

<template>
  <TooltipProvider :delay-duration="500">
    <App />
  </TooltipProvider>
</template>
