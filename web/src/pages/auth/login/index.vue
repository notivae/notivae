<script setup lang="ts">
import { computed } from "vue";
import { useRoute } from "vue-router";
import { useServerFeatures } from "@/composables/useServerFeatures.ts";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

import logoSrc from "@/assets/logo.svg";
import authLocalSrc from "@/assets/auth-provider/local.svg";
import authMagicLinkSrc from "@/assets/auth-provider/magic-link.svg";
import authOidcSrc from "@/assets/auth-provider/oidc.svg";

definePage({
  meta: {
    requiresAuth: false,
    followNextIfAuthenticated: true,
  }
});

const currentRoute = useRoute();
const nextRoute = computed<string>(() => (currentRoute.query.next as string) ?? "/");
const { data: serverFeatures } = useServerFeatures();

const oidcRedirectUrl = computed(() => {
  const url = new URL("/api/auth/oidc/redirect", window.location.href);
  url.searchParams.set("next", nextRoute.value);
  return url.href;
});
</script>

<template>
  <div class="min-h-svh grid place-items-center gap-6 bg-muted p-6 md:p-10">
    <div class="flex flex-col w-full max-w-sm gap-6">
      <div class="flex items-center gap-2 self-center font-medium select-none">
        <img :src="logoSrc" alt="notivae logo" class="size-6" />
        Notivae
      </div>
      <Card>
        <CardHeader class="text-center">
          <CardTitle class="text-xl">
            Welcome back!
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div class="grid gap-6">
            <div class="flex flex-col gap-4">
              <template v-if="serverFeatures?.auth.local">
                <router-link :to="{ name: '/auth/login/password/', query: { ...$route.query } }">
                  <Button variant="outline" class="w-full pl-2 cursor-pointer">
                    <img aria-hidden="true" :src="authLocalSrc" alt="Password" class="size-5 dark:invert" />
                    <span class="m-auto">
                      Login via Password
                    </span>
                  </Button>
                </router-link>
              </template>
              <template v-if="serverFeatures?.auth.magic_link">
                <router-link :to="{ name: '/auth/login/magic-link/', query: { ...$route.query } }">
                  <Button variant="outline" class="w-full pl-2 cursor-pointer">
                    <img aria-hidden="true" :src="authMagicLinkSrc" alt="Magic-Link" class="size-5 dark:invert " />
                    <span class="m-auto">
                      Login via Magic-Link
                    </span>
                  </Button>
                </router-link>
              </template>
              <template v-if="serverFeatures?.auth.oidc">
                <a :href="oidcRedirectUrl">
                  <Button variant="outline" class="w-full pl-2 cursor-pointer">
                    <img aria-hidden="true" :src="authOidcSrc" alt="OIDC" class="size-5 dark:invert" />
                    <span class="m-auto">
                      Login via OIDC
                    </span>
                  </Button>
                </a>
              </template>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  </div>
</template>
