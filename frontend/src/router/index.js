import { createRouter, createWebHistory } from 'vue-router';
import AuthView from '../pages/AuthPage.vue';
import DashboardView from '../pages/DashboardPage.vue';

const routes = [
  { path: '/', component: AuthView },
  { path: '/dashboard', component: DashboardView }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;