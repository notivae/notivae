<script setup lang="ts">
import { LucideBrush, LucideCircle } from "lucide-vue-next";
import { usePreferredDark } from "@vueuse/core";
import { ColorModeSampleCard } from "@/components/settings/appearance";
import { Label } from "@/components/ui/label";
import { computed, type MaybeRefOrGetter, toValue } from "vue";
import { useConfiguredColorMode } from "@/composables/useConfiguredColorMode.ts";
import { SettingsDescription, SettingsHeading, SettingsSection } from "@/components/settings/common";

const preferredDark = usePreferredDark();
const { store: colorMode } = useConfiguredColorMode();

type ColorModeMeta = {
  class: MaybeRefOrGetter<string>
  value: string
  label: string
}

const COLOR_MODES: ColorModeMeta[] = [
  {
    class: computed(() => preferredDark.value ? 'dark theme-default' : 'light theme-default'),
    value: "auto",
    label: "System",
  },
  {
    class: "light theme-default",
    value: "light",
    label: "Light",
  },
  {
    class: "dark theme-default",
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
  <SettingsSection>
    <SettingsHeading variant="h1">
      <LucideBrush />
      Appearance
    </SettingsHeading>
    <SettingsDescription>
      Switch up the look of the app by choosing a theme that suits you best. Pick the vibe you like and the app will update right away.
    </SettingsDescription>
  </SettingsSection>

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
</template>
