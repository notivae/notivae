<script setup lang="ts">
import { SidebarProvider } from "@/components/ui/sidebar";
import { AppSidebar, AppSidebarToggle } from "@/components/app/sidebar";
</script>

<template>
  <SidebarProvider>
    <AppSidebar />
    <main>
      <AppSidebarToggle />
      <router-view />
    </main>
  </SidebarProvider>
</template>
