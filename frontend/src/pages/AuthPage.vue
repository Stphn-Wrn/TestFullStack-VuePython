<template>
  <v-container class="fill-height d-flex justify-center align-center">
    <v-card width="450" class="pa-4">
      <v-tabs v-model="tab" grow>
        <v-tab value="login">Login</v-tab>
        <v-tab value="register">Register</v-tab>
      </v-tabs>

      <v-window v-model="tab">
        <v-window-item value="login">
          <v-form @submit.prevent="handleLogin" class="mt-4">
            <v-alert
              v-if="authStore.error"
              type="error"
              class="mb-4"
              density="compact"
              border="start"
            >
              {{ authStore.error }}
            </v-alert>

            <v-text-field
              v-model="loginForm.email"
              label="Email"
              type="email"
              required
              outlined
              :rules="[emailRules]"
            ></v-text-field>

            <v-text-field
              v-model="loginForm.password"
              label="Password"
              :type="showLoginPassword ? 'text' : 'password'"
              required
              outlined
              :append-inner-icon="showLoginPassword ? 'mdi-eye-off' : 'mdi-eye'"
              @click:append-inner="showLoginPassword = !showLoginPassword"
            />


            <v-btn
              type="submit"
              block
              class="mt-4"
              color="primary"
              :loading="authStore.isLoading"
              :disabled="authStore.isLoading"
              size="large"
            >
              Sign in
            </v-btn>
          </v-form>
        </v-window-item>

        <v-window-item value="register">
          <v-form @submit.prevent="handleRegister" class="mt-4">
            <v-alert
              v-if="authStore.error"
              type="error"
              class="mb-4"
              density="compact"
              border="start"
            >
              {{ authStore.error }}
            </v-alert>

            <v-text-field
              v-model="registerForm.username"
              label="Username"
              required
              outlined
            ></v-text-field>

            <v-text-field
              v-model="registerForm.email"
              label="Email"
              type="email"
              required
              outlined
              :rules="[emailRules]"
            ></v-text-field>

            <v-text-field
              v-model="registerForm.password"
              label="Password"
              :type="showRegisterPassword ? 'text' : 'password'"
              required
              outlined
              :rules="[passwordRules]"
              :append-inner-icon="showRegisterPassword ? 'mdi-eye-off' : 'mdi-eye'"
              @click:append-inner="showRegisterPassword = !showRegisterPassword"
            />


            <v-text-field
              v-model="registerForm.confirmPassword"
              label="Confirm Password"
              :type="showConfirmPassword ? 'text' : 'password'"
              required
              outlined
              :rules="[passwordMatch]"
              :append-inner-icon="showConfirmPassword ? 'mdi-eye-off' : 'mdi-eye'"
              @click:append-inner="showConfirmPassword = !showConfirmPassword"
            />

            <v-btn
              type="submit"
              block
              class="mt-4"
              color="secondary"
              :loading="authStore.isLoading"
              :disabled="authStore.isLoading"
              size="large"
            >
              Sign up
            </v-btn>
          </v-form>
        </v-window-item>
      </v-window>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { useAuthStore } from '../stores/authStore';
import { useRouter } from 'vue-router';

const router = useRouter()
const authStore = useAuthStore();

const tab = ref('login');

const showLoginPassword = ref(false)
const showRegisterPassword = ref(false)
const showConfirmPassword = ref(false)


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
const emailRules = (value) => {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return regex.test(value) || 'Please enter a valid email address'
}

const passwordRules = (value) =>
  value.length >= 8 || 'Password must be at least 8 characters long';

const passwordMatch = computed(() =>
  registerForm.value.password === registerForm.value.confirmPassword ||
  'Passwords do not match'
);

const handleLogin = async () => {
  const success = await authStore.login({
    email: loginForm.value.email,
    password: loginForm.value.password
  })

  if (success) {
   router.push('/dashboard');
   console.log(success)
  }
}

const handleRegister = async () => {
  if (!registerForm.value.username || 
      !registerForm.value.email || 
      !registerForm.value.password) {
    authStore.error = 'Please fill in all fields';
    return;
  }

  if (registerForm.value.password !== registerForm.value.confirmPassword) {
    authStore.error = "Passwords do not match";
    return;
  }

  const success = await authStore.register({
    username: registerForm.value.username,
    email: registerForm.value.email,
    password: registerForm.value.password
  });

  if (success) {
    router.push('/dashboard');
  }
}

function clearErrorOnChange(fields) {
  fields.forEach(field => {
    watch(field, () => authStore.error = null)
  })
}
watch(tab, () => {
  authStore.clearErrors()
})

clearErrorOnChange([
  () => loginForm.value.email,
  () => loginForm.value.password,
  () => registerForm.value.username,
  () => registerForm.value.email,
  () => registerForm.value.password,
  () => registerForm.value.confirmPassword
])
</script>

<style scoped>
.v-card {
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}
</style>
