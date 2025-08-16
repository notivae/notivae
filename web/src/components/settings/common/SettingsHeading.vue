<script setup lang="ts">
import { SidebarTrigger, useSidebar } from "@/components/ui/sidebar";
import { cn } from "@/lib/utils.ts";
import type { HTMLAttributes } from "vue";
import { reactiveOmit } from "@vueuse/core";
import { useForwardProps, Primitive } from "reka-ui";
import type { PrimitiveProps } from "reka-ui";
import { Separator } from "@/components/ui/separator";
import { cva, type VariantProps } from "class-variance-authority";

const headingVariants = cva(
    'flex gap-2 items-center [&>svg]:size-[1em]',
    {
      variants: {
        variant: {
          'h1': 'text-2xl font-extrabold border-b border-border',
          'h2': 'text-xl font-bold border-b border-border',
          'h3': 'text-lg font-semibold border-b border-border',
          'h4': 'text-base font-medium',
          'h5': 'text-sm font-normal',
          'h6': 'text-xs font-light',
        }
      },
      defaultVariants: {
        variant: 'h2',
      },
    },
);
type HeadingVariants = VariantProps<typeof headingVariants>

const props = defineProps<PrimitiveProps & {
  class?: HTMLAttributes['class']
  variant: HeadingVariants['variant']
}>();

const delegatedProps = reactiveOmit(props, 'class', 'variant');
const forwarded = useForwardProps(delegatedProps);

const { isMobile } = useSidebar();
</script>

<template>
  <Primitive
      role="heading"
      v-bind="forwarded"
      :as="props.variant!"
      :class="cn(headingVariants({ variant }), props.class)"
  >
    <template v-if="variant == 'h1' && isMobile">
      <SidebarTrigger class="h-6 w-6 [&_svg:not([class*='size-'])]:size-6" />
      <Separator orientation="vertical" class="data-[orientation=vertical]:h-6" />
    </template>
    <slot />
  </Primitive>
</template>
