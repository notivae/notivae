<script setup lang="ts">
import { SidebarFooter, SidebarMenu, SidebarMenuButton, SidebarMenuItem } from "@/components/ui/sidebar";
import { useAuthStore } from "@/stores/auth.ts";
import { DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuGroup, DropdownMenuItem, DropdownMenuSeparator } from "@/components/ui/dropdown-menu";
import { LucideBookText, LucideBug, LucideChevronsUpDown, LucideLogOut, LucideSettings } from "lucide-vue-next";
import { UserAvatar } from "@/components/common/user-avatar";

const { user } = useAuthStore();
</script>

<template>
  <SidebarFooter>
    <SidebarMenu>
      <SidebarMenuItem>
        <DropdownMenu>
          <DropdownMenuTrigger as-child>
            <SidebarMenuButton size="lg">
              <UserAvatar :user-id="user!.id" :name="user!.name" :avatar-blurhash="user!.avatar_blurhash" class="size-8 rounded-lg" />
              <div class="grid flex-1 text-left text-sm leading-tight">
                <template v-if="!user!.display_name">
                  <span class="truncate font-semibold">
                    {{ user!.name }}
                  </span>
                </template>
                <template v-else>
                  <span class="truncate font-semibold">
                    {{ user!.display_name }}
                  </span>
                  <span class="truncate text-xs">
                    {{ user!.name }}
                  </span>
                </template>
              </div>
              <LucideChevronsUpDown class="ml-auto size-4" />
            </SidebarMenuButton>
          </DropdownMenuTrigger>
          <DropdownMenuContent
              class="w-[var(--reka-dropdown-menu-trigger-width)] min-w-56 rounded-lg"
          >
            <DropdownMenuGroup>
              <a href="https://notivae.github.io/" target="_blank" rel="noopener noreferrer">
                <DropdownMenuItem>
                  <LucideBookText />
                  <span>
                    Documentation
                  </span>
                </DropdownMenuItem>
              </a>
              <a href="https://github.com/notivae/notivae/issues" target="_blank" rel="noopener noreferrer">
                <DropdownMenuItem>
                  <LucideBug />
                  <span>
                    Report a Bug
                  </span>
                </DropdownMenuItem>
              </a>
            </DropdownMenuGroup>
            <DropdownMenuSeparator />
            <DropdownMenuGroup>
              <router-link :to="{ name: '/(settings)/settings/' }">
                <DropdownMenuItem>
                  <LucideSettings />
                  <span>
                    Settings
                  </span>
                </DropdownMenuItem>
              </router-link>
            </DropdownMenuGroup>
            <DropdownMenuSeparator />
            <DropdownMenuGroup>
              <router-link :to="{ name: '/auth/logout' }">
                <DropdownMenuItem>
                  <LucideLogOut />
                  <span>
                    Log out
                  </span>
                </DropdownMenuItem>
              </router-link>
            </DropdownMenuGroup>
          </DropdownMenuContent>
        </DropdownMenu>
      </SidebarMenuItem>
    </SidebarMenu>
  </SidebarFooter>
</template>
