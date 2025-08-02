<script setup lang="ts">
import { Label } from "@/components/ui/label";

defineProps<{
  kv: Record<string, unknown>
}>();
</script>

<template>
  <div class="grid grid-cols-[auto_1fr] gap-x-4 gap-y-1">
    <template v-for="[key, value] in Object.entries(kv)">
      <Label class="font-bold">{{ key }}</Label>
      <span>{{ value }}</span>
    </template>
  </div>
</template>
