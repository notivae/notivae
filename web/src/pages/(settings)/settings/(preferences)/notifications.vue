<script setup lang="ts">
import { LucideBell } from "lucide-vue-next";
import { SettingsDescription, SettingsHeading } from "@/components/settings/common";
</script>

<template>
  <div class="space-y-4">
    <SettingsHeading variant="h1">
      <LucideBell />
      Notifications
    </SettingsHeading>
    <SettingsDescription>
      Choose how and when you want to be notified. Control updates, alerts, and messages so you only get the stuff that matters to you.
    </SettingsDescription>
  </div>
</template>
