<script setup lang="ts">
import { Button } from "@/components/ui/button";
import {
  LucideHome, LucideLayoutDashboard,
  LucideSettings, LucideShieldUser,
} from "lucide-vue-next";
import { Separator } from "@/components/ui/separator";

definePage({
  meta: {
    requiresAdmin: true,
  },
});
</script>

<template>
  <div class="min-h-svh bg-muted">
    <div class="max-w-5xl min-h-svh mx-auto bg-background p-6">
      <h1 class="text-2xl font-extrabold text-center">
        <LucideShieldUser class="inline-block" />
        Admin Dashboard
      </h1>
      <div class="mt-4 flex gap-8">
        <div class="flex flex-col gap-1 items-stretch">
          <router-link :to="{ name: '/' }">
            <Button variant="ghost" class="w-full justify-start">
              <LucideHome />
              Home
            </Button>
          </router-link>
          <Separator />
          <router-link :to="{ name: '/(admin)/admin/dashboard' }" v-slot="{ isActive }">
            <Button :variant="isActive ? 'secondary' : 'ghost'" class="w-full justify-start">
              <LucideLayoutDashboard />
              Dashboard
            </Button>
          </router-link>
        </div>
        <div class="grow">
          <router-view />
        </div>
      </div>
    </div>
  </div>
</template>
