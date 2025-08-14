<script setup lang="ts">
import { LucideBrush, LucideCircle } from "lucide-vue-next";
import { Separator } from "@/components/ui/separator";
import { usePreferredDark } from "@vueuse/core";
import { ColorModeSampleCard } from "@/components/settings/appearance";
import { Label } from "@/components/ui/label";
import { computed, type MaybeRefOrGetter, toValue } from "vue";
import { useConfiguredColorMode } from "@/composables/useConfiguredColorMode.ts";

const preferredDark = usePreferredDark();
const { store: colorMode } = useConfiguredColorMode();

type ColorModeMeta = {
  class: MaybeRefOrGetter<string>
  value: string
  label: string
}

const COLOR_MODES: ColorModeMeta[] = [
  {
    class: computed(() => preferredDark.value ? 'dark default' : 'light default'),
    value: "auto",
    label: "System",
  },
  {
    class: "light default",
    value: "light",
    label: "Light",
  },
  {
    class: "dark default",
    value: "dark",
    label: "Dark",
  },
  {
    class: "light theme-parchment",
    value: "parchment",
    label: "Parchment",
  },
  {
    class: "dark theme-parchment",
    value: "parchment-dark",
    label: "Parchment (Dark)",
  },
];
</script>

<template>
  <div class="space-y-4">
    <div>
      <h2 class="text-xl font-bold">
        <LucideBrush class="inline-block mr-1" />
        Appearance
      </h2>
      <Separator />
    </div>
    <div class="grid grid-cols-[repeat(auto-fill,minmax(min(200px,100%),1fr))] gap-2">
      <template v-for="mode in COLOR_MODES" :key="mode.value">
        <div
            class="border rounded-sm bg-secondary"
            :class="{ 'border-accent-foreground': colorMode === mode.value }"
            @click="colorMode = mode.value as 'auto'"
        >
          <ColorModeSampleCard class="rounded-t-sm pointer-events-nonex" :class="toValue(mode.class)" />
          <div class="flex items-center gap-1 p-1">
            <div class="size-3 border border-primary rounded-full p-0.25">
              <LucideCircle v-if="colorMode === mode.value" class="size-full fill-primary" />
            </div>
            <Label>
              {{ mode.label }}
            </Label>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>
