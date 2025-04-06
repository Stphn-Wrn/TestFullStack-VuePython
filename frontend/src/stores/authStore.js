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
      this.isLoading = true
      this.error = null
  
      try {
        await apiClient.post('/auth/login', credentials)
        const me = await apiClient.get('/auth/me')
        this.user = me.data.user
        return true
      } catch (error) {
        const raw = error.response?.data?.error || "Login failed"
        
        if (
          raw.includes('Email not found') ||
          raw.includes('Incorrect password')
        ) {
          this.error = "Invalid email or password"
        } else {
          this.error = "An error occurred. Please try again."
        }
  
        return false
      } finally {
        this.isLoading = false
      }
    },

    async fetchUser() {
      try {
        const { data } = await apiClient.get('/auth/me')
        this.user = data.user
        return true
      } catch (error) {
        this.user = null
        if (error.response?.status === 401) {
          console.warn('Utilisateur non connecté')
        }
        return false
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
