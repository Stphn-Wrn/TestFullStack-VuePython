<template>
  <v-container class="fill-height d-flex justify-center align-center">
    <v-card width="400" class="pa-4">
      <v-tabs v-model="tab">
        <v-tab value="login">Connexion</v-tab>
        <v-tab value="register">Inscription</v-tab>
      </v-tabs>

      <v-window v-model="tab">
        <v-window-item value="login">
          <v-form @submit.prevent="handleLogin">
            <v-text-field 
              v-model="loginForm.email" 
              label="Email" 
              type="email" 
              required
              :error-messages="authStore.error"
            ></v-text-field>
            <v-text-field 
              v-model="loginForm.password" 
              label="Mot de passe" 
              type="password" 
              required
            ></v-text-field>
            <v-btn 
              type="submit" 
              block 
              class="mt-2" 
              color="primary"
              :loading="authStore.isLoading"
            >Se connecter</v-btn>
          </v-form>
        </v-window-item>

        <v-window-item value="register">
          <v-form @submit.prevent="handleRegister">
            <v-text-field 
              v-model="registerForm.email" 
              label="Email" 
              type="email" 
              required
              :error-messages="authStore.error"
            ></v-text-field>
            <v-text-field 
              v-model="registerForm.password" 
              label="Mot de passe" 
              type="password" 
              required
            ></v-text-field>
            <v-text-field 
              v-model="registerForm.confirmPassword" 
              label="Confirmer le mot de passe" 
              type="password" 
              required
              :rules="[passwordMatch]"
            ></v-text-field>
            <v-btn 
              type="submit" 
              block 
              class="mt-2" 
              color="secondary"
              :loading="authStore.isLoading"
            >S'inscrire</v-btn>
          </v-form>
        </v-window-item>
      </v-window>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '../stores/authStore'

const authStore = useAuthStore()
const tab = ref('login')

const loginForm = ref({
  email: '',
  password: ''
})

const registerForm = ref({
  email: '',
  password: '',
  confirmPassword: ''
})

const passwordMatch = computed(() => 
  registerForm.value.password === registerForm.value.confirmPassword || 
  'Les mots de passe ne correspondent pas'
)

const handleLogin = async () => {
  await authStore.login(loginForm.value)
}

const handleRegister = async () => {
  if (registerForm.value.password !== registerForm.value.confirmPassword) {
    authStore.error = "Les mots de passe ne correspondent pas"
    return
  }
  await authStore.register({
    email: registerForm.value.email,
    password: registerForm.value.password
  })
}
</script>

<style>
.v-container {
  height: 100vh;
}
</style>