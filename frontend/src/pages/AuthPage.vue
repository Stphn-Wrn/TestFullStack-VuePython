<template>
    <v-container class="fill-height d-flex justify-center align-center">
      <v-card width="400" class="pa-4">
        <v-tabs v-model="tab">
          <v-tab value="login">Connect</v-tab>
          <v-tab value="register">Register</v-tab>
        </v-tabs>
  
        <v-window v-model="tab">
          <v-window-item value="login">
            <v-form @submit.prevent="handleLogin">
              <v-text-field v-model="email" label="Email" type="email" required></v-text-field>
              <v-text-field v-model="password" label="Mot de passe" type="password" required></v-text-field>
              <v-btn type="submit" block class="mt-2" color="primary">Log in</v-btn>
            </v-form>
          </v-window-item>
  
          <v-window-item value="register">
            <v-form @submit.prevent="handleRegister">
              <v-text-field v-model="email" label="Email" type="email" required></v-text-field>
              <v-text-field v-model="password" label="Mot de passe" type="password" required></v-text-field>
              <v-text-field v-model="confirmPassword" label="Confirmer le mot de passe" type="password" required></v-text-field>
              <v-btn type="submit" block class="mt-2" color="secondary">Register</v-btn>
            </v-form>
          </v-window-item>
        </v-window>
      </v-card>
    </v-container>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  const tab = ref('login');
  const email = ref('');
  const password = ref('');
  const confirmPassword = ref('');
  
  const handleLogin = () => {
    console.log('Connexion avec', email.value, password.value);
  };
  
  const handleRegister = () => {
    if (password.value !== confirmPassword.value) {
      alert("Passwords doesn't match");
      return;
    }
    console.log('Inscription avec', email.value, password.value);
  };
  </script>
  
  <style>
  .v-container {
    height: 100vh;
  }
  </style>