<script setup lang="ts">
import { PinInput, PinInputGroup, PinInputSlot } from "@/components/ui/pin-input";
import type { PinInputRootProps } from "reka-ui";
import { ref, watch } from "vue";

const PIN_LENGTH = 6;

const props = defineProps<Omit<PinInputRootProps, "modelValue"> & {
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
      const chars = newVal.trim().split("").slice(0, PIN_LENGTH);
      modelArray.value = [...chars, ...Array(PIN_LENGTH - chars.length).fill("")]
    },
    { immediate: true },
);

// Sync to outside (modelArray -> modelValue)
watch(
    modelArray,
    (newArray) => {
      const concatenated = newArray.join("").trim();
      emit("update:modelValue", concatenated);

      if (concatenated.length === PIN_LENGTH) {
        emit("complete");
      }
    },
    { deep: true },
);
</script>

<template>
  <PinInput
      otp
      v-model="modelArray"
      placeholder="○"
      class="justify-center"
  >
    <PinInputGroup>
      <PinInputSlot
          v-for="(id, index) in PIN_LENGTH"
          :key="id"
          :index="index"
          class="uppercase font-mono"
      />
    </PinInputGroup>
  </PinInput>
</template>
