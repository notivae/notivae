<script setup lang="ts">
import { LucideLogs } from "lucide-vue-next";
import { Separator } from "@/components/ui/separator";
import { ref } from "vue";
import { useWebSocketEvent } from "@/composables/useWebSocketEvent.ts";
import type { AdminLogMessage } from "@/types/ws.ts";
import { useQuery } from "@tanstack/vue-query";
import axios from "axios";
import { ErrorBox } from "@/components/common/error-box";


const logMessages = ref<AdminLogMessage[]>([]);

const { error: loadingError } = useQuery<AdminLogMessage[]>({
  queryKey: ["api", "admin", "logs", "query"],
  queryFn: async () => {
    const response = await axios.get<AdminLogMessage[]>("/api/admin/logs/query");
    logMessages.value = response.data;
    return response.data;
  },
  refetchOnWindowFocus: false,
  retry: false,
});

useWebSocketEvent("log", (message) => {
  logMessages.value.push(message);
});

function levelToName(lvl: number): string {
  switch (lvl) {
    case 10: return "DEB";
    case 20: return "INF";
    case 30: return "WAR";
    case 40: return "ERR";
    case 50: return "CRI";
    default: return lvl.toString();
  }
}

function levelToColor(lvl: number) {
  switch (lvl) {
    case 0: return "var(--color-logging-debug)";
    case 10: return "var(--color-logging-debug)";
    case 20: return "var(--color-logging-info)";
    case 30: return "var(--color-logging-warning)";
    case 40: return "var(--color-logging-error)";
    case 50: return "var(--color-logging-critical)";
    default: return "inherit";
  }
}

const timestampFormatter = new Intl.DateTimeFormat(undefined, {
  dateStyle: "short",
  timeStyle: "medium",
});

function formatTimestamp(timestamp: string): string {
  return timestampFormatter.format(new Date(timestamp));
}

const abbreviateCache = new Map<string, string>();

function abbreviateKey(key: string): string {
  if (abbreviateCache.has(key))
    return abbreviateCache.get(key)!;

  const parts = key.split(".");
  if (parts.length <= 2) {
    abbreviateCache.set(key, key);
    return key;
  }
  const abbreviated = parts.slice(0, -2).map(part => part[0]).join(".") + "." + parts.slice(-2).join(".");
  abbreviateCache.set(key, abbreviated);
  return abbreviated;
}

function openJsonInNewTab(json: object) {
  const blob = new Blob([JSON.stringify(json)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  window.open(url, "_blank");
  URL.revokeObjectURL(url);
}
</script>

<template>
  <div class="space-y-4">
    <div>
      <h2 class="text-xl font-bold">
        <LucideLogs class="inline-block mr-1" />
        Logs
      </h2>
      <Separator />
    </div>
    <ErrorBox :error="loadingError" />

    <div class="overflow-x-auto max-w-full">
      <table class="w-full font-mono text-sm bg-secondary rounded-sm">
        <thead>
          <tr class="sticky top-0">
            <th class="px-2 whitespace-nowrap">Timestamp</th>
            <th class="px-2 whitespace-nowrap">Level</th>
            <th class="px-2 whitespace-nowrap">Module</th>
            <th class="px-2 whitespace-nowrap">Line</th>
            <th class="px-2 whitespace-nowrap">Message</th>
            <th class="px-2 whitespace-nowrap">Context</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(log, index) in logMessages" :key="index" :style="{ color: levelToColor(log.level) }">
            <td class="px-2 w-px whitespace-nowrap" :title="log.timestamp">
              {{ formatTimestamp(log.timestamp) }}
            </td>
            <td class="px-2 w-px whitespace-nowrap">
              {{ levelToName(log.level) }}
            </td>
            <td class="px-2 w-px whitespace-nowrap" :title="log.module">
              {{ abbreviateKey(log.module) }}
            </td>
            <td class="px-2 w-px whitespace-nowrap text-right">
              {{ log.lineno }}
            </td>
            <td class="px-2 whitespace-nowrap">
              {{ log.message }}
            </td>
            <td class="px-2 w-px whitespace-nowrap cursor-pointer" @click="openJsonInNewTab(log.context)" :title="JSON.stringify(log.context, null, 2)">
              {{ Object.keys(log.context).length ? "{...}" : "{}" }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
