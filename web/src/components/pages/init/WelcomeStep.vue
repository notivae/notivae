<script setup lang="ts">
import { CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { LucideInfo } from "lucide-vue-next";
</script>

<template>
  <CardHeader>
    <CardTitle>
      Welcome to Notivae
    </CardTitle>
    <CardDescription>
      Let’s get your application ready. We’ll walk you through a few simple steps to initialize your instance.
    </CardDescription>
  </CardHeader>
  <CardContent>
    <Alert variant="warning">
      <LucideInfo class="h-4 w-4" />
      <AlertTitle>Heads up</AlertTitle>
      <AlertDescription>
        This setup only runs once.
      </AlertDescription>
    </Alert>
  </CardContent>
</template>
