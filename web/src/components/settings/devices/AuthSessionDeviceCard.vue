<script setup lang="ts">
import type { AuthSessionInfo } from "@/types/api.ts";
import { computed } from "vue";
import { UAParser } from "ua-parser-js";
import { Tooltip, TooltipTrigger, TooltipContent } from "@/components/ui/tooltip";
import { Card, CardContent } from "@/components/ui/card";
import { LucideDot, LucideMinus, LucideMonitor, LucideSmartphone, LucideTablet } from "lucide-vue-next";

const props = defineProps<{
  session: AuthSessionInfo
}>();

function formatDateTime(dt: string): string {
  const formatter = new Intl.DateTimeFormat(undefined, {
    dateStyle: "short",
    timeStyle: "short",
  });
  return formatter.format(new Date(dt));
}

const userAgent = computed(() => UAParser(props.session.user_agent));
</script>

<template>
  <Card>
    <CardContent class="flex items-center gap-4">
      <div class="rounded-full bg-secondary p-1">
        <LucideSmartphone v-if="userAgent.device.type === 'mobile'" />
        <LucideTablet v-else-if="userAgent.device.type === 'tablet'" />
        <LucideMonitor v-else />
      </div>
      <div class="grow space-y-2 text-sm" :class="{'text-muted-foreground': session.revoked || (new Date(session.expires_at) < new Date())}">
        <p>
          <Tooltip>
            <TooltipTrigger as-child>
              <span>
                {{ userAgent.os.name }}
                <LucideDot class="inline-block size-4" />
                {{ userAgent.browser.name }}
                <LucideDot class="inline-block size-4" />
                {{ session.ip_address }}
              </span>
            </TooltipTrigger>
            <TooltipContent>
              {{ session.user_agent }}
            </TooltipContent>
          </Tooltip>
        </p>
        <p>
          <Tooltip>
            <TooltipTrigger as-child>
              <span>
                {{ formatDateTime(session.created_at) }}
              </span>
            </TooltipTrigger>
            <TooltipContent>
              Created: {{ session.created_at }}
            </TooltipContent>
          </Tooltip>
          <LucideMinus class="inline-block size-4" />
          <Tooltip>
            <TooltipTrigger as-child>
              <span>
                {{ formatDateTime(session.expires_at) }}
              </span>
            </TooltipTrigger>
            <TooltipContent>
              Expires: {{ session.expires_at }}
            </TooltipContent>
          </Tooltip>
        </p>
      </div>
      <slot name="actions" />
    </CardContent>
  </Card>
</template>
