<script setup lang="ts">
import { Label } from "@/components/ui/label";
import { LucideMinus } from "lucide-vue-next";

defineProps<{
  kv: Record<string, unknown>
}>();
</script>

<template>
  <div class="grid grid-cols-[auto_1fr] gap-x-4 gap-y-1">
    <template v-for="[key, value] in Object.entries(kv)">
      <Label class="font-bold whitespace-nowrap">
        {{ key }}
      </Label>
      <span v-if="value !== undefined && value !== null" class="break-words min-w-0">
        {{ value }}
      </span>
      <span v-else class="text-muted-foreground">
        <LucideMinus />
      </span>
    </template>
  </div>
</template>
