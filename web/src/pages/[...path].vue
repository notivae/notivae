<script setup lang="ts">
import { Button } from "@/components/ui/button";
import { LucideHouse, LucideArrowLeft } from "lucide-vue-next";

definePage({
  meta: {
    requiresAuth: false,
  }
});
</script>

<template>
  <main class="min-h-svh p-10 grid place-items-center">
    <section class="text-center space-y-6 max-w-md">
      <h1 class="text-5xl font-bold text-destructive-foreground">404</h1>
      <p class="text-xl font-semibold">Page Not Found</p>
      <p class="text-base text-muted-foreground">
        The page you’re looking for doesn’t exist or has been moved.
      </p>
      <div class="flex justify-center gap-4">
        <router-link
            :to="{ name: '/' }"
        >
          <Button>
            <LucideHouse />
            Go Home
          </Button>
        </router-link>
        <Button
            variant="secondary"
            @click="$router.back()"
        >
          <LucideArrowLeft />
          Go Back
        </Button>
      </div>
    </section>
  </main>
</template>
