import { defineStore } from 'pinia';
import apiClient from '@/api/client';
import router from '@/router';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    isLoading: false,
    error: null,
    justLoggedIn: false,
  }),

  actions: {
    async login(credentials) {
      this.isLoading = true;
      this.error = null;

      try {
        let user = await apiClient.post('/auth/login', credentials);
        if (user) {
          await this.fetchUser();
          this.justLoggedIn = true;
          return true;
        }
        return false;
      } catch (error) {
        const message =
          error.response?.data?.msg ||
          error.response?.data?.error ||
          'Login failed';

        if (
          message.includes('Email not found') ||
          message.includes('Incorrect password')
        ) {
          this.error = 'Invalid email or password.';
        } else {
          this.error = message;
        }

        return false;
      } finally {
        this.isLoading = false;
      }
    },

    async refreshToken() {
      try {
        const response = await apiClient.post('/auth/refresh');

        return response.status === 200;
      } catch (error) {
        await this.logout();
        throw error;
      }
    },
    async fetchUser() {
      try {
        // Le cookie access_token est envoyé automatiquement
        const { data } = await apiClient.get('/auth/me');
        this.user = data;
        return true;
      } catch (error) {
        if (error.response?.status === 401) {
          const refreshed = await this.refreshToken();
          if (refreshed) return this.fetchUser();
        }
        throw error;
      }
    },

    async register(credentials) {
      this.isLoading = true;
      this.error = null;

      try {
        const res = await apiClient.post('/auth/register', credentials);

        if (res.status === 201) {
          await this.fetchUser();
          return true;
        }
        return false;
      } catch (error) {
        const err = error.response?.data?.error;

        // Gestion des erreurs de validation retournées en objet
        if (err && typeof err === 'object') {
          const firstField = Object.keys(err)[0];
          this.error = err[firstField][0]; // Prend le premier message d'erreur
        } else {
          this.error = err || 'Registration failed';
        }

        return false;
      } finally {
        this.isLoading = false;
      }
    },

    async logout() {
      this.isLoading = true;
      this.error = null;

      try {
        await apiClient.post('/auth/logout');
      } catch (error) {
        console.warn(error.response?.data || error.message);
      } finally {
        this.user = null;
        this.isLoading = false;
        router.push('/');
      }
    },

    clearErrors() {
      this.error = null;
    },
  },

  getters: {
    isAuthenticated: (state) => !!state.user,
  },

  persist: {
    paths: ['user'],
  },
});
