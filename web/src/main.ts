import './index.css';
import 'vue-sonner/style.css';

import { createApp } from 'vue';
import { VueQueryPlugin } from "@tanstack/vue-query";
import { createPinia } from "pinia";
import axios from "axios";

import "@/services/ws";

import App from '@/AppWrapper.vue';
import { router } from "@/router";


axios.defaults.withCredentials = true;
axios.defaults.timeout = 15_000;


createApp(App)
    .use(VueQueryPlugin)
    .use(createPinia())
    .use(router)
    .mount('#app');
