import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { createPinia } from 'pinia';
import { createVuetify } from 'vuetify';
import 'vuetify/styles';

const app = createApp(App);
const vuetify = createVuetify();

app.use(router);
app.use(createPinia());
app.use(vuetify);
app.mount('#app');