<script setup lang="ts">
import { Button } from "@/components/ui/button";
import {
  LucideHome, LucideLayoutDashboard,
  LucideLogs, LucideSettings, LucideShieldUser, LucideUsersRound,
} from "lucide-vue-next";
import { Separator } from "@/components/ui/separator";

definePage({
  meta: {
    requiresAdmin: true,
  },
});
</script>

<template>
  <div class="flex gap-8 p-4">
    <!-- Sidebar -->
    <div class="flex flex-col gap-1 items-stretch">
      <h1 class="text-2xl font-extrabold text-center">
        <LucideShieldUser class="inline-block" />
        Admin Dashboard
      </h1>
      <Separator />
      <router-link :to="{ name: '/' }">
        <Button variant="ghost" class="w-full justify-start">
          <LucideHome />
          Home
        </Button>
      </router-link>
      <router-link :to="{ name: '/(settings)/settings' }">
        <Button variant="ghost" class="w-full justify-start">
          <LucideSettings />
          User Settings
        </Button>
      </router-link>
      <Separator />
      <router-link :to="{ name: '/(admin)/admin/dashboard' }" v-slot="{ isActive }">
        <Button :variant="isActive ? 'secondary' : 'ghost'" class="w-full justify-start">
          <LucideLayoutDashboard />
          Dashboard
        </Button>
      </router-link>
      <router-link :to="{ name: '/(admin)/admin/users' }" v-slot="{ isActive }">
        <Button :variant="isActive ? 'secondary' : 'ghost'" class="w-full justify-start">
          <LucideUsersRound />
          Users
        </Button>
      </router-link>
      <Separator />
      <router-link :to="{ name: '/(admin)/admin/logs' }" v-slot="{ isActive }">
        <Button :variant="isActive ? 'secondary' : 'ghost'" class="w-full justify-start">
          <LucideLogs />
          Logs
        </Button>
      </router-link>
    </div>
    <!-- Main Content -->
    <div class="flex-1 overflow-auto">
      <router-view />
    </div>
  </div>
</template>
