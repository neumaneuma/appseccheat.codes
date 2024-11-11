<template>
  <div class="container mx-auto px-4 py-8">
    <h2 class="mt-6 text-4xl font-bold text-gray-900">Challenge #3: SSRF bypass webhook</h2>

    <p class="my-8">
      This web server has a functionality built for webhooks. However, you can abuse this functionality to access an internal admin API.
      The only thing you know is that the internal API can be accessed through
      <span class="bg-gray-200 p-1 font-mono">http://internal_api</span>
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

      <form @submit.prevent="submitWebhook" class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="custom_url">
            Enter the URL to use for the webhook:
          </label>
          <input
            v-model="customUrl"
            :disabled="apiState.isLoading"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            name="custom_url"
            id="custom_url"
            type="text"
            placeholder="http://example.com/webhook"
          >
        </div>
        <div class="flex items-center justify-between">
          <button
            :disabled="apiState.isLoading"
            class="bg-gray-500 hover:bg-gray-400 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline disabled:opacity-50"
            type="submit"
          >
            <LoadingSpinner v-if="apiState.isLoading" />
            <span v-else>Submit</span>
          </button>
        </div>
      </form>

      <!-- Response Display -->
      <div v-if="webhookResponse" class="mt-4 p-4 bg-gray-100 rounded-md">
        <h3 class="font-bold mb-2">Response:</h3>
        <pre class="whitespace-pre-wrap text-sm">{{ webhookResponse }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useApiState } from '@/composables/useApiState'
import AlertMessage from '@/components/shared/AlertMessage.vue'
import LoadingSpinner from '@/components/shared/LoadingSpinner.vue'

const customUrl = ref('')
const webhookResponse = ref('')
const { state: apiState, handleApiCall } = useApiState()

const submitWebhook = async () => {
  try {
    const result = await handleApiCall(
      async () => {
        const response = await fetch('/vulnerabilities/ssrf1/submit_webhook/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ url: customUrl.value }),
        })

        if (!response.ok) {
          const error = await response.json()
          throw new Error(error.detail || 'Webhook submission failed')
        }

        return response.text()
      },
      'Webhook submitted successfully!'
    )

    webhookResponse.value = result
  } catch (error) {
    console.error('Error:', error)
  }
}
</script>
