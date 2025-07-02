import './index.css';
import 'vue-sonner/style.css';
import { createApp } from 'vue';
import App from '@/App.vue';
import router from "@/router";

createApp(App)
    .use(router)
    .mount('#app');
