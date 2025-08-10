<script setup lang="ts">
import { CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Info } from "lucide-vue-next";
import { FormField, FormItem, FormLabel, FormControl, FormMessage } from "@/components/ui/form";
</script>

<template>
  <CardHeader>
    <CardTitle>Create Administrator Account</CardTitle>
    <CardDescription>
      This administrator account will have full access to all features and settings. Choose strong credentials to keep your application secure.
    </CardDescription>
  </CardHeader>

  <CardContent class="grid gap-4">
    <FormField v-slot="{ componentField }" name="username">
      <FormItem>
        <FormLabel>Username</FormLabel>
        <FormControl>
          <Input type="text" v-bind="componentField" autocomplete="username" />
        </FormControl>
        <FormMessage />
      </FormItem>
    </FormField>

    <FormField v-slot="{ componentField }" name="displayName">
      <FormItem>
        <FormLabel>Display Name</FormLabel>
        <FormControl>
          <Input type="text" v-bind="componentField" autocomplete="name" />
        </FormControl>
        <FormMessage />
      </FormItem>
    </FormField>

    <FormField v-slot="{ componentField }" name="email">
      <FormItem>
        <FormLabel>Email</FormLabel>
        <FormControl>
          <Input type="email" v-bind="componentField" autocomplete="email" />
        </FormControl>
        <FormMessage />
      </FormItem>
    </FormField>

    <FormField v-slot="{ componentField }" name="password">
      <FormItem>
        <FormLabel>Password</FormLabel>
        <FormControl>
          <Input type="password" v-bind="componentField" autocomplete="new-password" placeholder="******" />
        </FormControl>
        <FormMessage />
      </FormItem>
    </FormField>

    <Alert variant="default">
      <Info class="w-4 h-4" />
      <AlertTitle>Authentication Note</AlertTitle>
      <AlertDescription>
        The new administrator account will use the built-in authentication provider with your given credentials.
        You can later change the authentication provider via the users settings.
      </AlertDescription>
    </Alert>
  </CardContent>
</template>
