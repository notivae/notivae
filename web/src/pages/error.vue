<script setup lang="ts">
import { useRoute } from "vue-router";
import { LucideCircleX, LucideHouse, LucideArrowLeft } from "lucide-vue-next";
import { Button } from "@/components/ui/button";

definePage({
  meta: {
    requiresAuth: false,
  }
});

const currentRoute = useRoute();
</script>

<template>
  <main class="min-h-svh p-10 grid place-items-center">
    <section class="text-center space-y-6 max-w-md">
      <h1 class="text-5xl font-bold text-destructive-foreground">
        <LucideCircleX class="size-12 inline-block" />
        Error
        <LucideCircleX class="size-12 inline-block" />
      </h1>
      <p class="text-xl font-semibold">You encountered a critical error.</p>
      <p class="text-base text-muted-foreground font-mono">
        {{ currentRoute.query.name ?? "Error" }}: {{ currentRoute.query.message ?? "~unknown~" }}
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
