<script setup lang="ts">
import { computed } from "vue";
import { useServerFeatures } from "@/composables/api/useServerFeatures.ts";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useQueryNext } from "@/composables/common/useQueryNext.ts";
import { IconNotivaeLogo, IconAuthProviderLocal, IconAuthProviderMagicLink, IconAuthProviderOIDC } from "@/components/icons";

definePage({
  meta: {
    requiresAuth: false,
    followNextIfAuthenticated: true,
  }
});

const nextRoute = useQueryNext();
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
      <div class="flex items-center justify-center gap-1 self-center text-xl font-medium font-mono">
        <IconNotivaeLogo class="size-5" />
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
                    <IconAuthProviderLocal class="size-5" />
                    <span class="m-auto">
                      Login via Password
                    </span>
                  </Button>
                </router-link>
              </template>
              <template v-if="serverFeatures?.auth.magic_link">
                <router-link :to="{ name: '/auth/login/magic-link/', query: { ...$route.query } }">
                  <Button variant="outline" class="w-full pl-2 cursor-pointer">
                    <IconAuthProviderMagicLink  class="size-5" />
                    <span class="m-auto">
                      Login via Magic-Link
                    </span>
                  </Button>
                </router-link>
              </template>
              <template v-if="serverFeatures?.auth.oidc">
                <a :href="oidcRedirectUrl">
                  <Button variant="outline" class="w-full pl-2 cursor-pointer">
                    <IconAuthProviderOIDC class="size-5" />
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
