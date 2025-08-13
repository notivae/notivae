<script setup lang="ts">
import { Button } from "@/components/ui/button";
import {
  LucideBell, LucideBrush,
  LucideFingerprint,
  LucideHome,
  LucideIdCard,
  LucideLogOut, LucideMonitorSmartphone,
  LucideSettings, LucideShieldUser,
  LucideUserRound
} from "lucide-vue-next";
import { Separator } from "@/components/ui/separator";
import { useAuthStore } from "@/stores/auth.ts";

const auth = useAuthStore();
</script>

<template>
  <div class="min-h-svh bg-muted">
    <div class="max-w-5xl min-h-svh mx-auto bg-background p-6">
      <h1 class="text-2xl font-extrabold text-center">
        <LucideSettings class="inline-block" />
        Settings
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
          <router-link :to="{ name: '/(settings)/settings/(account)/account' }" v-slot="{ isActive }">
            <Button :variant="isActive ? 'secondary' : 'ghost'" class="w-full justify-start">
              <LucideUserRound />
              Account
            </Button>
          </router-link>
          <router-link :to="{ name: '/(settings)/settings/(account)/authentication-identities' }" v-slot="{ isActive }">
            <Button :variant="isActive ? 'secondary' : 'ghost'" class="w-full justify-start">
              <LucideIdCard />
              Authentication Identities
            </Button>
          </router-link>
          <router-link :to="{ name: '/(settings)/settings/(account)/mfa' }" v-slot="{ isActive }">
            <Button :variant="isActive ? 'secondary' : 'ghost'" class="w-full justify-start">
              <LucideFingerprint />
              Multi-Factor Authentication
            </Button>
          </router-link>
          <router-link :to="{ name: '/(settings)/settings/(account)/devices' }" v-slot="{ isActive }">
            <Button :variant="isActive ? 'secondary' : 'ghost'" class="w-full justify-start">
              <LucideMonitorSmartphone />
              Devices
            </Button>
          </router-link>
          <Separator />
          <router-link :to="{ name: '/(settings)/settings/(preferences)/appearance' }" v-slot="{ isActive }">
            <Button :variant="isActive ? 'secondary' : 'ghost'" class="w-full justify-start">
              <LucideBrush />
              Appearance
            </Button>
          </router-link>
          <router-link :to="{ name: '/(settings)/settings/(preferences)/notifications' }" v-slot="{ isActive }">
            <Button :variant="isActive ? 'secondary' : 'ghost'" class="w-full justify-start">
              <LucideBell />
              Notifications
            </Button>
          </router-link>
          <Separator />
          <template v-if="auth.user?.is_system_admin">
            <router-link :to="{ name: '/(admin)/admin' }" v-slot="{ isActive }">
              <Button :variant="isActive ? 'secondary' : 'ghost'" class="w-full justify-start">
                <LucideShieldUser />
                Admin Dashboard
              </Button>
            </router-link>
            <Separator />
          </template>
          <router-link :to="{ name: '/auth/logout' }">
            <Button variant="ghost" class="w-full justify-start hover:text-destructive-foreground">
              <LucideLogOut />
              Logout
            </Button>
          </router-link>
        </div>
        <div class="flex-1 overflow-auto">
          <router-view />
        </div>
      </div>
    </div>
  </div>
</template>
