import { defineStore } from 'pinia'
import apiClient from '@/api/client'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    isLoading: false,
    error: null,
    justLoggedIn: false
  }),

  actions: {
    async login(credentials) {
      this.isLoading = true;
      this.error = null;
    
      try {
        const test = await apiClient.post('/auth/login', credentials);
        console.log(test)
        this.justLoggedIn = true; 
        return true;
      } catch (error) {
        const message = error.response?.data?.msg || error.response?.data?.error || "Login failed";
    
        if (message.includes('Email not found') || message.includes('Incorrect password')) {
          this.error = "Invalid email or password.";
        } else {
          this.error = message;
        }
    
        return false;
      } finally {
        this.isLoading = false;
      }
    },
    

    async fetchUser() {
      this.isLoading = true;
      this.error = null;
    
      try {
        const { data } = await apiClient.get('/auth/me');
        this.user = data;
        this.justLoggedIn = false; 
        console.log("[authStore] user enregistré :", this.user);

        return true;
      } catch (error) {
        this.user = null;
        
        const message = error.response?.data?.msg 
          || error.response?.data?.error 
          || "Échec de la vérification de l'utilisateur";
    
        if (error.response?.status === 401) {
          console.warn('Non autorisé');
        } else {
          console.error('Erreur fetchUser:', message);
          this.error = message;
        }
        
        return false;
      } finally {
        this.isLoading = false;
      }
    },
    
    
    async register(userData) {
      this.isLoading = true
      this.error = null
  
      try {
        await apiClient.post('/auth/register', userData)
        const me = await apiClient.get('/auth/me')
        this.user = me.data.user
        return true
      } catch (error) {
        const raw = error.response?.data?.error || "Registration failed"
  
        if (
          raw.includes('Email') || raw.includes('Username')
        ) {
          this.error = "Unable to create account. Please check your email and password."
        } else {
          this.error = "An error occurred. Please try again."
        }
  
        return false
      } finally {
        this.isLoading = false
      }
    },

    async logout() {
      this.isLoading = true
      this.error = null

      try {
        await apiClient.post('/auth/logout')
      } catch (error) {
        console.warn('[logout] Échec côté serveur :', error.response?.data || error.message)
      } finally {
        this.user = null
        this.isLoading = false
      }
    },
    
    clearErrors() {
      this.error = null
    }
  },

  getters: {
    isAuthenticated: (state) => !!state.user
  },

  persist: {
    paths: ['user']
  }
})
