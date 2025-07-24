import './index.css';
import 'vue-sonner/style.css';

import { createApp } from 'vue';
import { createPinia } from "pinia";
import axios from "axios";

import "@/services/ws";

import App from '@/App.vue';
import router from "@/router";


axios.defaults.withCredentials = true;


createApp(App)
    .use(router)
    .use(createPinia)
    .mount('#app');
