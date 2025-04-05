import { defineStore } from 'pinia';
import apiClient from '@/api/client';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    isLoading: false,
    error: null
  }),

  actions: {
    async login(credentials) {
      this.isLoading = true;
      this.error = null;

      try {
        const loginResponse = await apiClient.post('/auth/login', credentials);
        this.user = loginResponse.data.user;
        this.token = loginResponse.data.token;
        return true;
      } catch (error) {
        this.error = error.response?.data?.message || "Erreur de connexion";
        return false;
      } finally {
        this.isLoading = false;
      }
    },

    async fetchUser() {
      
    },

    logout() {
      apiClient.post('/auth/logout'); 
      this.user = null;
    }
  },

  getters: {
    isAuthenticated: (state) => !!state.user
  }
});