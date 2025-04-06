import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { createPinia } from 'pinia';
import { createVuetify } from 'vuetify';
import 'vuetify/styles';
import piniaPersistedState from 'pinia-plugin-persistedstate'

const app = createApp(App);
const vuetify = createVuetify();
const pinia = createPinia()
pinia.use(piniaPersistedState)

app.use(router);
app.use(pinia)
app.use(vuetify);
app.mount('#app');