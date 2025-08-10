<script setup lang="ts">
import { CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useMutation } from "@tanstack/vue-query";
import axios from "axios";
import { useFormValues } from "vee-validate";
import { ErrorBox } from "@/components/common/error-box";
import { LucideLoader } from "lucide-vue-next";

type FormValues = {
  username: string
  displayName: string
  email: string
  password: string
}

const formValues = useFormValues<FormValues>();

const { mutateAsync, isSuccess, isPending, isError, error } = useMutation({
  mutationFn: async () => {
    await axios.post<void>("/api/init", {
      admin_account: {
        username: formValues.value.username,
        display_name: formValues.value.displayName,
        email: formValues.value.email,
        password: formValues.value.password,
      },
    });
  },
});

async function confirmSetup() {
  await mutateAsync();
}

defineExpose({
  confirmSetup,
  isSuccess,
  isPending,
  isError,
  error,
});
</script>

<template>
  <CardHeader>
    <template v-if="!isSuccess">
      <CardTitle>
        Final Step
      </CardTitle>
      <CardDescription>
        Confirm to complete the initialization process.
      </CardDescription>
    </template>
    <template v-else>
      <CardTitle>
        Setup Complete!
      </CardTitle>
      <CardDescription>
        You may now finish and start using the application.
      </CardDescription>
    </template>
  </CardHeader>

  <CardContent class="space-y-4">
    <!-- Loading -->
    <div v-if="isPending" class="flex items-center gap-2">
      <LucideLoader class="animate-spin" />
      <span>Processing your setup...</span>
    </div>

    <!-- Error -->
    <ErrorBox v-else-if="isError" :error="error" />
  </CardContent>
</template>
