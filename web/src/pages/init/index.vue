<script setup lang="ts">
import logoSrc from "@/assets/logo.svg";
import { Card, CardContent } from "@/components/ui/card";
import { Stepper, StepperTrigger, StepperItem, StepperSeparator } from "@/components/ui/stepper";
import { type Component, ref } from "vue";
import { Button } from "@/components/ui/button";
import { FinishStep, WelcomeStep } from "@/components/pages/init";
import type { LucideIcon } from "lucide-vue-next";
import axios from "axios";

definePage({
  meta: {
    requiresAuth: false,
  },
  beforeEnter: async (_to, _from, next) => {
    try {
      const response = await axios.get<boolean>("/api/init-completed");

      if (response.data === true) {
        // already initialized: redirect to homepage
        return next({ name: '/' });
      }

      // Not initialized: continue to setup
      return next();
    } catch (error) {
      console.error("Error checking init state:", error);
      return next(false);  // block navigation
    }
  },
});

type StepDetails = {
  component: Component,
  icon: LucideIcon | string
}

const STEP_COMPONENTS: StepDetails[] = [
  { component: WelcomeStep, icon: logoSrc },
  { component: FinishStep, icon: logoSrc },
];
const stepIndex = ref(1);
</script>

<template>
  <div class="min-h-svh grid place-items-center gap-6 bg-muted p-6 md:p-10">
    <div class="flex flex-col w-full max-w-md gap-6">
      <div class="flex items-center gap-2 self-center font-medium">
        <img :src="logoSrc" alt="notivae logo" class="size-6" />
        Notivae
      </div>
      <Stepper v-slot="{ nextStep, prevStep }" v-model="stepIndex" class="block w-full">
        <Card>
          <!-- Stepper -->
          <div class="flex w-full flex-start gap-2">
            <StepperItem
                v-for="(step, index) in STEP_COMPONENTS"
                :key="index"
                v-slot="{ state }"
                class="relative flex w-full flex-col items-center justify-center"
                :step="index+1"
            >
              <StepperSeparator
                  v-if="(index+1) !== STEP_COMPONENTS.length"
                  class="absolute left-[calc(50%+20px)] right-[calc(-50%+10px)] top-5 block h-0.5 shrink-0 rounded-full bg-muted group-data-[state=completed]:bg-primary"
              />
              <StepperTrigger as-child>
                <Button
                    :variant="state === 'completed' || state === 'active' ? 'default' : 'outline'"
                    size="icon"
                    class="z-10 rounded-full shink-0"
                    :disabled="state !== 'completed'"
                >
                  <img v-if="typeof step.icon === 'string'" :src="step.icon" alt="" />
                  <component v-else :is="step.icon" />
                </Button>
              </StepperTrigger>
            </StepperItem>
          </div>

          <!-- Step -->
          <component :is="STEP_COMPONENTS[stepIndex-1].component" />

          <!-- Actions -->
          <CardContent>
            <div class="flex items-center justify-end gap-2">
              <Button
                  v-if="stepIndex !== 1 && stepIndex !== STEP_COMPONENTS.length"
                  variant="outline"
                  size="sm"
                  class="justify-self-start"
                  @click="prevStep"
              >
                Back
              </Button>
              <Button v-if="stepIndex !== STEP_COMPONENTS.length" size="sm" @click="nextStep">
                Next
              </Button>
              <router-link v-else :to="{ name: '/' }">
                <Button size="sm">
                  Finish
                </Button>
              </router-link>
            </div>
          </CardContent>
        </Card>
      </Stepper>
    </div>
  </div>
</template>
