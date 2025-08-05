<script setup lang="ts">
import { PinInput, PinInputGroup, PinInputSlot, PinInputSeparator } from "@/components/ui/pin-input";
import type { PinInputRootProps } from "reka-ui";
import { ref, watch } from "vue";

const CODE_LENGTH = 8;

const props = defineProps<Omit<PinInputRootProps, "modelValue">  & {
  modelValue: string
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: string): void
  (e: "complete"): void
}>();

// Internal state
const modelArray = ref<string[]>([]);

// Sync from outside (modeValue -> modelArray)
watch(
    () => props.modelValue,
    (newVal) => {
      const chars = newVal.trim().split("").slice(0, CODE_LENGTH);
      modelArray.value = [...chars, ...Array(CODE_LENGTH - chars.length).fill("")]
    },
    { immediate: true },
);

// Sync to outside (modelArray -> modelValue)
watch(
    modelArray,
    (newArray) => {
      const concatenated = newArray.join("").trim();
      emit("update:modelValue", concatenated);

      if (concatenated.length === CODE_LENGTH) {
        emit("complete");
      }
    },
    { deep: true },
);
</script>

<template>
  <PinInput
      v-model="modelArray"
      placeholder="○"
      class="justify-center"
  >
    <PinInputGroup>
      <template v-for="(id, index) in CODE_LENGTH" :key="id">
        <PinInputSlot
            :index="index"
            :class="{
                'rounded-r-md border-r': index === Math.floor(CODE_LENGTH / 2-1),
                'rounded-l-md border-l': index === Math.floor(CODE_LENGTH / 2),
            }"
            class="uppercase font-mono"
        />
        <template v-if="index === Math.floor(CODE_LENGTH / 2-1)">
          <PinInputSeparator class="w-2 mx-1" />
        </template>
      </template>
    </PinInputGroup>
  </PinInput>
</template>
