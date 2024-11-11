<template>
  <div class="container mx-auto px-4 py-8">
    <h2 class="mt-6 text-4xl font-bold text-gray-900">Challenge #2: SQLi second order</h2>
    <SQLiIntroduction />
    <SQLiNews />
    <div class="grid md:grid-cols-2 gap-8 mt-8">
      <!-- Registration Form -->
      <div class="w-full">
        <h3 class="text-xl font-bold mb-4">Register New Account</h3>
        <AlertMessage
          v-if="registerState.error"
          :message="registerState.error"
          type="error"
        />
        <AlertMessage
          v-if="registerState.success"
          :message="registerState.success"
          type="success"
        />

        <form @submit.prevent="submitRegister" class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
          <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="username">
              Username
            </label>
            <input
              v-model="registerForm.username"
              :disabled="registerState.isLoading"
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              :class="{ 'border-red-500': registerFormErrors.username }"
              name="username"
              id="username"
              type="text"
              placeholder="Username"
            >
            <p v-if="registerFormErrors.username" class="text-red-500 text-xs italic mt-1">
              {{ registerFormErrors.username }}
            </p>
          </div>
          <div class="mb-6">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="password">
              Password
            </label>
            <input
              v-model="registerForm.password"
              :disabled="registerState.isLoading"
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"
              :class="{ 'border-red-500': registerFormErrors.password }"
              name="password"
              id="password"
              type="password"
              placeholder="******************"
            >
            <p v-if="registerFormErrors.password" class="text-red-500 text-xs italic mt-1">
              {{ registerFormErrors.password }}
            </p>
          </div>
          <div class="flex items-center justify-between">
            <button
              :disabled="registerState.isLoading || !isRegisterFormValid"
              class="bg-gray-500 hover:bg-gray-400 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline disabled:opacity-50"
              type="submit"
            >
              <LoadingSpinner v-if="registerState.isLoading" />
              <span v-else>Register</span>
            </button>
          </div>
        </form>
      </div>

      <!-- Change Password Form -->
      <div class="w-full">
        <h3 class="text-xl font-bold mb-4">Change Password</h3>
        <AlertMessage
          v-if="changePasswordState.error"
          :message="changePasswordState.error"
          type="error"
        />
        <AlertMessage
          v-if="changePasswordState.success"
          :message="changePasswordState.success"
          type="success"
        />

        <form @submit.prevent="submitChangePassword" class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
          <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="old-password">
              Old Password
            </label>
            <input
              v-model="passwordForm.oldPassword"
              :disabled="changePasswordState.isLoading"
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              :class="{ 'border-red-500': passwordFormErrors.oldPassword }"
              name="old-password"
              id="old-password"
              type="password"
              placeholder="Old Password"
            >
            <p v-if="passwordFormErrors.oldPassword" class="text-red-500 text-xs italic mt-1">
              {{ passwordFormErrors.oldPassword }}
            </p>
          </div>
          <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="new-password">
              New Password
            </label>
            <input
              v-model="passwordForm.newPassword"
              :disabled="changePasswordState.isLoading"
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              :class="{ 'border-red-500': passwordFormErrors.newPassword }"
              name="new-password"
              id="new-password"
              type="password"
              placeholder="New Password"
            >
            <p v-if="passwordFormErrors.newPassword" class="text-red-500 text-xs italic mt-1">
              {{ passwordFormErrors.newPassword }}
            </p>
          </div>
          <div class="mb-6">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="verify-password">
              Verify New Password
            </label>
            <input
              v-model="passwordForm.verifyPassword"
              :disabled="changePasswordState.isLoading"
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"
              :class="{ 'border-red-500': passwordFormErrors.verifyPassword }"
              name="verify-password"
              id="verify-password"
              type="password"
              placeholder="Verify New Password"
            >
            <p v-if="passwordFormErrors.verifyPassword" class="text-red-500 text-xs italic mt-1">
              {{ passwordFormErrors.verifyPassword }}
            </p>
          </div>
          <div class="flex items-center justify-between">
            <button
              :disabled="changePasswordState.isLoading || !isPasswordFormValid"
              class="bg-gray-500 hover:bg-gray-400 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline disabled:opacity-50"
              type="submit"
            >
              <LoadingSpinner v-if="changePasswordState.isLoading" />
              <span v-else>Change Password</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useApiState } from '@/composables/useApiState'
import AlertMessage from '@/components/shared/AlertMessage.vue'
import LoadingSpinner from '@/components/shared/LoadingSpinner.vue'
import SQLiIntroduction from '@/views/sqli/SQLiIntroduction.vue'
import SQLiNews from '@/views/sqli/SQLiNews.vue'

// Register form state
const registerForm = ref({
  username: '',
  password: ''
})

const registerFormErrors = computed(() => {
  const errors: Record<string, string> = {}
  if (!registerForm.value.username) {
    errors.username = 'Username is required'
  }
  if (!registerForm.value.password) {
    errors.password = 'Password is required'
  }
  return errors
})

const isRegisterFormValid = computed(() => {
  return Object.keys(registerFormErrors.value).length === 0 &&
    registerForm.value.username.length > 0 &&
    registerForm.value.password.length > 0
})

// Password change form state
const passwordForm = ref({
  oldPassword: '',
  newPassword: '',
  verifyPassword: ''
})

const passwordFormErrors = computed(() => {
  const errors: Record<string, string> = {}
  if (!passwordForm.value.oldPassword) {
    errors.oldPassword = 'Old password is required'
  }
  if (!passwordForm.value.newPassword) {
    errors.newPassword = 'New password is required'
  }
  if (!passwordForm.value.verifyPassword) {
    errors.verifyPassword = 'Password verification is required'
  } else if (passwordForm.value.newPassword !== passwordForm.value.verifyPassword) {
    errors.verifyPassword = 'Passwords do not match'
  }
  return errors
})

const isPasswordFormValid = computed(() => {
  return Object.keys(passwordFormErrors.value).length === 0 &&
    passwordForm.value.oldPassword.length > 0 &&
    passwordForm.value.newPassword.length > 0 &&
    passwordForm.value.verifyPassword.length > 0
})

// API states
const { state: registerState, handleApiCall: handleRegister } = useApiState()
const { state: changePasswordState, handleApiCall: handleChangePassword } = useApiState()

const submitRegister = async () => {
  if (!isRegisterFormValid.value) return

  try {
    await handleRegister(
      async () => {
        const response = await fetch('/vulnerabilities/sqli2/register/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: registerForm.value.username,
            password: registerForm.value.password
          }),
        })

        if (!response.ok) {
          const error = await response.json()
          throw new Error(error.detail || 'Registration failed')
        }

        return response.json()
      },
      'Registration successful!'
    )

    // Clear form after successful registration
    registerForm.value = {
      username: '',
      password: ''
    }
  } catch (error) {
    console.error('Error:', error)
  }
}

const submitChangePassword = async () => {
  if (!isPasswordFormValid.value) return

  try {
    await handleChangePassword(
      async () => {
        const response = await fetch('/vulnerabilities/sqli2/change_password/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            old: passwordForm.value.oldPassword,
            new: passwordForm.value.newPassword,
            new_verify: passwordForm.value.verifyPassword
          }),
        })

        if (!response.ok) {
          const error = await response.json()
          throw new Error(error.detail || 'Password change failed')
        }

        return response.json()
      },
      'Password changed successfully!'
    )

    // Clear form after successful password change
    passwordForm.value = {
      oldPassword: '',
      newPassword: '',
      verifyPassword: ''
    }
  } catch (error) {
    console.error('Error:', error)
  }
}
</script>
