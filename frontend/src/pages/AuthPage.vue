<template>
  <v-container class="fill-height d-flex justify-center align-center">
    <v-card width="450" class="pa-4">
      <v-tabs v-model="tab" grow>
        <v-tab value="login">Connexion</v-tab>
        <v-tab value="register">Inscription</v-tab>
      </v-tabs>

      <v-window v-model="tab">
        <v-window-item value="login">
          <v-form @submit.prevent="handleLogin" class="mt-4">
            <v-text-field
              v-model="loginForm.email"
              label="Email"
              type="email"
              required
              :error-messages="authStore.error"
              outlined
            ></v-text-field>
            
            <v-text-field
              v-model="loginForm.password"
              label="Mot de passe"
              type="password"
              required
              outlined
            ></v-text-field>
            
            <v-btn
              type="submit"
              block
              class="mt-4"
              color="primary"
              :loading="authStore.isLoading"
              size="large"
            >
              Se connecter
            </v-btn>
          </v-form>
        </v-window-item>

        <v-window-item value="register">
          <v-form @submit.prevent="handleRegister" class="mt-4">
            <v-text-field
              v-model="registerForm.username"
              label="Nom d'utilisateur"
              required
              :error-messages="authStore.error"
              outlined
            ></v-text-field>
            
            <v-text-field
              v-model="registerForm.email"
              label="Email"
              type="email"
              required
              outlined
            ></v-text-field>
            
            <v-text-field
              v-model="registerForm.password"
              label="Mot de passe"
              type="password"
              required
              outlined
              :rules="[passwordRules]"
            ></v-text-field>
            
            <v-text-field
              v-model="registerForm.confirmPassword"
              label="Confirmer le mot de passe"
              type="password"
              required
              outlined
              :rules="[passwordMatch]"
            ></v-text-field>
            
            <v-btn
              type="submit"
              block
              class="mt-4"
              color="secondary"
              :loading="authStore.isLoading"
              size="large"
            >
              S'inscrire
            </v-btn>
          </v-form>
        </v-window-item>
      </v-window>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useAuthStore } from '../stores/authStore';

const authStore = useAuthStore();
const tab = ref('login');

const loginForm = ref({
  email: '',
  password: ''
});

const registerForm = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
});

// Règles de validation
const passwordRules = (value) => {
  return value.length >= 8 || 'Le mot de passe doit contenir au moins 8 caractères';
};

const passwordMatch = computed(() => 
  registerForm.value.password === registerForm.value.confirmPassword || 
  'Les mots de passe ne correspondent pas'
);

const handleLogin = async () => {
  if (!loginForm.value.email || !loginForm.value.password) {
    authStore.error = 'Veuillez remplir tous les champs';
    return;
  }
  
  await authStore.login({
    email: loginForm.value.email,
    password: loginForm.value.password
  });
};

const handleRegister = async () => {
  if (!registerForm.value.username || 
      !registerForm.value.email || 
      !registerForm.value.password) {
    authStore.error = 'Veuillez remplir tous les champs';
    return;
  }
  
  if (registerForm.value.password !== registerForm.value.confirmPassword) {
    authStore.error = "Les mots de passe ne correspondent pas";
    return;
  }
  
  await authStore.register({
    username: registerForm.value.username,
    email: registerForm.value.email,
    password: registerForm.value.password
  });
};
</script>

<style scoped>


.v-card {
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}
</style>