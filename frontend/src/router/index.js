import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/authStore'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('../pages/AuthPage.vue'),
    meta: { requiresGuest: true }
  },
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
  const auth = useAuthStore()

  if (to.meta.requiresAuth) {
    const isLoggedIn = auth.user || await auth.fetchUser()

    if (!isLoggedIn) {
      return {
        path: '/auth',
        query: { redirectTo: to.fullPath }
      }
    }
  }

  if (to.meta.requiresGuest && auth.user) {
    return '/dashboard'
  }
})
;

export default router;