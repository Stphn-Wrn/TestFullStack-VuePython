import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/authStore'

const routes = [
  {
    path: '/auth',
    name: 'Auth',
    component: () => import('../pages/AuthPage.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../pages/DashboardPage.vue'),
    meta: { requiresAuth: true }
  }
  
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach(async (to) => {
  const auth = useAuthStore();
  
  if (to.meta.requiresAuth && !auth.user) {
    await auth.fetchUser();
    if (!auth.user) return '/auth';
  }
  
  if (auth.isAuthenticated && !auth.user) {
    await auth.fetchUser();
  }
  
  if (to.meta.guestOnly && auth.isAuthenticated) {
    return '/';
  }
});

export default router;