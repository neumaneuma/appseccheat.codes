<template>
  <div class="container mx-auto px-4 py-8">
    <h2 class="mt-6 text-4xl font-bold text-gray-900">Challenge #1: SQLi login bypass</h2>

    <p class="my-8">
      You know there is a user with the username
      <span class="bg-gray-200 p-1 font-mono w-max">administrator</span>. Try to figure out how to login as
      <span class="bg-gray-200 p-1 font-mono w-max">administrator</span> without knowing what their password is!
    </p>

    <div class="w-full max-w-xs">
      <AlertMessage
        v-if="apiState.error"
        :message="apiState.error"
        type="error"
      />
      <AlertMessage
        v-if="apiState.success"
        :message="apiState.success"
        type="success"
      />

      <form @submit.prevent="submitLogin" class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="username">
            Username
          </label>
          <input
            v-model="username"
            :disabled="apiState.isLoading"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            name="username"
            id="username"
            type="text"
            placeholder="Username"
          >
        </div>
        <div class="mb-6">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="password">
            Password
          </label>
          <input
            v-model="password"
            :disabled="apiState.isLoading"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"
            name="password"
            id="password"
            type="password"
            placeholder="******************"
          >
        </div>
        <div class="flex items-center justify-between">
          <button
            :disabled="apiState.isLoading"
            class="bg-gray-500 hover:bg-gray-400 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline disabled:opacity-50"
            type="submit"
          >
            <LoadingSpinner v-if="apiState.isLoading" />
            <span v-else>Login</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useApiState } from '@/composables/useApiState'
import AlertMessage from '@/components/shared/AlertMessage.vue'
import LoadingSpinner from '@/components/shared/LoadingSpinner.vue'

const username = ref('')
const password = ref('')
const { state: apiState, handleApiCall } = useApiState()

const submitLogin = async () => {
  await handleApiCall(
    async () => {
      const response = await fetch('/vulnerabilities/sqli1/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: username.value,
          password: password.value
        }),
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Login failed')
      }

      return response.json()
    },
    'Login successful!'
  )
}
</script>
