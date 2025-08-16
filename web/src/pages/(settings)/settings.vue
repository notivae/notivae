<script setup lang="ts">
import {
  LucideBell, LucideBrush,
  LucideFingerprint,
  LucideHome,
  LucideIdCard,
  LucideLogOut, LucideMonitorSmartphone, LucideSettings,
  LucideShieldUser,
  LucideUserRound
} from "lucide-vue-next";
import { useAuthStore } from "@/stores/auth.ts";
import {
  Sidebar,
  SidebarContent, SidebarFooter,
  SidebarGroup, SidebarHeader,
  SidebarMenu, SidebarMenuButton,
  SidebarMenuItem,
  SidebarProvider, SidebarSeparator,
} from "@/components/ui/sidebar";

const { user } = useAuthStore();
</script>

<template>
  <SidebarProvider>
    <Sidebar>
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <div class="flex w-full items-center gap-2 p-2 text-left text-lg">
              <LucideSettings />
              <span>
                Settings
              </span>
            </div>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarSeparator class="mx-0" />
      <SidebarContent>
        <SidebarGroup>
          <SidebarMenu>
            <SidebarMenuItem>
              <router-link :to="{ name: '/' }" v-slot="{ isActive }">
                <SidebarMenuButton :is-active="isActive">
                  <LucideHome />
                  <span>
                    Home
                  </span>
                </SidebarMenuButton>
              </router-link>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarGroup>
        <SidebarGroup>
          <SidebarMenu>
            <SidebarMenuItem>
              <router-link :to="{ name: '/(settings)/settings/(account)/account' }" v-slot="{ isActive }">
                <SidebarMenuButton :is-active="isActive">
                  <LucideUserRound />
                  <span>
                    Account
                  </span>
                </SidebarMenuButton>
              </router-link>
            </SidebarMenuItem>
            <SidebarMenuItem>
              <router-link :to="{ name: '/(settings)/settings/(account)/authentication-identities' }" v-slot="{ isActive }">
                <SidebarMenuButton :is-active="isActive">
                  <LucideIdCard />
                  <span>
                    Authentication Identities
                  </span>
                </SidebarMenuButton>
              </router-link>
            </SidebarMenuItem>
            <SidebarMenuItem>
              <router-link :to="{ name: '/(settings)/settings/(account)/mfa' }" v-slot="{ isActive }">
                <SidebarMenuButton :is-active="isActive">
                  <LucideFingerprint />
                  <span>
                    Multi-Factor Authentication
                  </span>
                </SidebarMenuButton>
              </router-link>
            </SidebarMenuItem>
            <SidebarMenuItem>
              <router-link :to="{ name: '/(settings)/settings/(account)/devices' }" v-slot="{ isActive }">
                <SidebarMenuButton :is-active="isActive">
                  <LucideMonitorSmartphone />
                  <span>
                    Devices
                  </span>
                </SidebarMenuButton>
              </router-link>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarGroup>
        <SidebarGroup>
          <SidebarMenu>
            <SidebarMenuItem>
              <router-link :to="{ name: '/(settings)/settings/(preferences)/appearance' }" v-slot="{ isActive }">
                <SidebarMenuButton :is-active="isActive">
                  <LucideBrush />
                  <span>
                    Appearance
                  </span>
                </SidebarMenuButton>
              </router-link>
            </SidebarMenuItem>
            <SidebarMenuItem>
              <router-link :to="{ name: '/(settings)/settings/(preferences)/notifications' }" v-slot="{ isActive }">
                <SidebarMenuButton :is-active="isActive">
                  <LucideBell />
                  Notifications
                </SidebarMenuButton>
              </router-link>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarGroup>
        <SidebarGroup v-if="user!.is_system_admin">
          <SidebarMenu>
            <SidebarMenuItem>
              <router-link :to="{ name: '/(admin)/admin/' }" v-slot="{ isActive }">
                <SidebarMenuButton :is-active="isActive">
                  <LucideShieldUser />
                  <span>
                    Admin Dashboard
                  </span>
                </SidebarMenuButton>
              </router-link>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter>
        <SidebarMenu>
          <SidebarMenuItem>
            <router-link :to="{ name: '/auth/logout' }" v-slot="{ isActive }">
              <SidebarMenuButton :is-active="isActive">
                <LucideLogOut />
                <span>
                  Logout
                </span>
              </SidebarMenuButton>
            </router-link>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
    </Sidebar>
    <main class="overflow-auto grow py-2 px-4 space-y-8">
      <router-view />
    </main>
  </SidebarProvider>
</template>
