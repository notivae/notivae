<script setup lang="ts">
import App from "@/App.vue";
import { TooltipProvider } from "@/components/ui/tooltip";
</script>

<template>
  <TooltipProvider :delay-duration="500">
    <App />
  </TooltipProvider>
</template>
