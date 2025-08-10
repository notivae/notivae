<script setup lang="ts">
import logoSrc from "@/assets/logo.svg";
import { Card } from "@/components/ui/card";
import { Stepper, StepperTrigger, StepperItem, StepperSeparator } from "@/components/ui/stepper";
import { type Component, type ComponentPublicInstance, ref } from "vue";
import { Button } from "@/components/ui/button";
import { AdminAccountCreationStep, FinishStep, WelcomeStep } from "@/components/pages/init";
import { type LucideIcon, LucideRocket, LucideShieldUser, LucideWandSparkles } from "lucide-vue-next";
import axios from "axios";
import * as z from "zod";
import { Form } from "vee-validate";
import { toTypedSchema } from "@vee-validate/zod";


definePage({
  meta: {
    requiresAuth: false,
  },
  beforeEnter: async (_to, _from, next) => {
    try {
      const response = await axios.get<boolean>("/api/init-completed");

      if (response.data === true) {
        // already initialized: redirect to homepage
        console.warn("already initialized");
        return next({ name: '/' });
      }

      // Not initialized: continue to setup
      return next();
    } catch (initError) {
      console.error("Error checking init state:", initError);
      if (initError instanceof Error) {
        return next({ name: "/error", query: { name: initError.name, message: initError.message } });  // block navigation
      } else {
        return next(false);
      }
    }
  },
});

type StepDetails = {
  component: Component,
  icon: LucideIcon
  schema?: z.ZodSchema
}

const STEPS: StepDetails[] = [
  {
    component: WelcomeStep,
    icon: LucideWandSparkles,
  },
  {
    component: AdminAccountCreationStep,
    icon: LucideShieldUser,
    schema: z.object({
      username: z.string().trim().nonempty(),
      displayName: z.string().trim(),
      email: z.string().trim().toLowerCase().email(),
      password: z.string().trim().nonempty(),
    }),
  },
  {
    component: FinishStep,
    icon: LucideRocket,
  },
];
const stepIndex = ref(1);

type FinishStepComponentInstance = ComponentPublicInstance<{
  confirmSetup: () => Promise<void>
  isSuccess: boolean
  isPending: boolean
  isError: boolean
  error: Error
}>

const finishStepRef = ref<FinishStepComponentInstance | null>(null);
</script>

<template>
  <div class="min-h-svh grid place-items-center gap-6 bg-muted p-6">
    <div class="flex flex-col w-full max-w-lg gap-6">
      <div class="flex items-center gap-2 self-center font-medium">
        <img :src="logoSrc" alt="notivae logo" class="size-6" />
        Notivae
      </div>
      <Form
          v-slot="{ meta, validate }"
          as="" keep-values :validation-schema="toTypedSchema(STEPS[stepIndex-1].schema ?? z.any())"
      >
        <Stepper
            as-child
            v-model="stepIndex"
            v-slot="{ isPrevDisabled, isNextDisabled, nextStep, prevStep, isFirstStep, isLastStep }"
        >
          <form
              @submit.prevent="async () => {
                const { valid } = await validate();
                if (valid) nextStep();
              }"
          >
            <Card class="w-full">
              <!-- Stepper -->
              <div class="flex w-full flex-start gap-2">
                <StepperItem
                    v-for="(step, index) in STEPS"
                    :key="index"
                    v-slot="{ state }"
                    class="relative flex w-full flex-col items-center justify-center"
                    :step="index+1"
                >
                  <StepperSeparator
                      v-if="(index+1) !== STEPS.length"
                      class="absolute left-[calc(50%+20px)] right-[calc(-50%+10px)] top-5 block h-0.5 shrink-0 rounded-full bg-muted group-data-[state=completed]:bg-primary"
                  />
                  <StepperTrigger as-child>
                    <Button
                        type="button"
                        :variant="(state === 'completed' || state === 'active') ? 'secondary' : 'outline'"
                        size="icon"
                        class="z-10 rounded-full shink-0 border"
                        :class="{ 'border-primary': (state === 'completed' || state === 'active') }"
                        :disabled="state !== 'completed' && !meta.valid"
                    >
                      <component :is="step.icon" class="size-full text-secondary-foreground" />
                    </Button>
                  </StepperTrigger>
                </StepperItem>
              </div>

              <!-- Step -->
              <component :is="STEPS[stepIndex-1].component" ref="finishStepRef" />

              <!-- Actions -->
              <div class="flex items-center justify-end gap-2 px-6">
                <Button
                    v-if="!isFirstStep && !finishStepRef?.isSuccess"
                    type="button"
                    variant="outline"
                    size="sm"
                    class="justify-self-start"
                    :disabled="isPrevDisabled"
                    @click="prevStep"
                >
                  Back
                </Button>
                <Button
                    v-if="!isLastStep"
                    :disabled="isNextDisabled"
                    type="submit"
                    size="sm"
                >
                  Next
                </Button>
                <template v-else>
                  <Button
                      v-if="!finishStepRef?.isSuccess || finishStepRef?.isError"
                      type="button"
                      size="sm"
                      @click="finishStepRef?.confirmSetup"
                  >
                    <template v-if="finishStepRef?.isError">Retry</template>
                    <template v-else>Confirm</template>
                  </Button>
                  <router-link v-else :to="{ name: '/' }" v-slot="{ navigate }">
                    <Button
                        type="button"
                        size="sm"
                        :disabled="!finishStepRef?.isSuccess"
                        @click="navigate"
                    >
                      Finish
                    </Button>
                  </router-link>
                </template>
              </div>
            </Card>
          </form>
        </Stepper>
      </Form>
    </div>
  </div>
</template>
