<template>
  <div class="container mx-auto px-4 py-8">
    <h2 class="mt-6 text-4xl font-bold text-gray-900">Challenge #4: SSRF local file inclusion</h2>

    <p class="my-8">
      Catcoin is the hot new crypto currency that everyone is talking about. The following form is for a financial web app
      that will allow you to pick the API that is used to query the current price of catcoin.
    </p>

    <div class="flex gap-4 my-4">
      <code class="bg-gray-200 p-2 text-sm rounded">http://internal_api:12301/get_cat_coin_price_v1/</code>
      <code class="bg-gray-200 p-2 text-sm rounded">http://internal_api:12301/get_cat_coin_price_v2/</code>
    </div>

    <p class="my-4">
      Solve this challenge by stealing the
      <code class="bg-gray-200 p-1">file:///etc/shadow</code> or
      <code class="bg-gray-200 p-1">file:///etc/passwd</code> files.
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

      <form @submit.prevent="submitUrl" class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="api_url">
            Enter the API URL:
          </label>
          <div class="space-y-2">
            <div v-for="(url, index) in predefinedUrls" :key="index" class="flex items-center">
              <input
                type="radio"
                :id="'url-' + index"
                v-model="selectedUrl"
                :value="url"
                class="mr-2"
                :disabled="apiState.isLoading"
              >
              <label :for="'url-' + index">{{ url }}</label>
            </div>
            <div class="flex items-center">
              <input
                type="radio"
                id="custom-url"
                v-model="selectedUrl"
                value="custom"
                class="mr-2"
                :disabled="apiState.isLoading"
              >
              <label for="custom-url">Custom URL</label>
            </div>
          </div>
          <input
            v-if="selectedUrl === 'custom'"
            v-model="customUrl"
            :disabled="apiState.isLoading"
            class="mt-2 shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            type="text"
            placeholder="Enter custom URL"
          >
        </div>
        <div class="flex items-center justify-between">
          <button
            :disabled="apiState.isLoading || !isValidUrl"
            class="bg-gray-500 hover:bg-gray-400 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline disabled:opacity-50"
            type="submit"
          >
            <LoadingSpinner v-if="apiState.isLoading" />
            <span v-else>Get Price</span>
          </button>
        </div>
      </form>

      <!-- Response Display -->
      <div v-if="apiResponse" class="mt-4 p-4 bg-gray-100 rounded-md">
        <h3 class="font-bold mb-2">Response:</h3>
        <pre class="whitespace-pre-wrap text-sm">{{ apiResponse }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useApiState } from '@/composables/useApiState'
import AlertMessage from '@/components/shared/AlertMessage.vue'
import LoadingSpinner from '@/components/shared/LoadingSpinner.vue'

const predefinedUrls = [
  'http://internal_api:12301/get_cat_coin_price_v1/',
  'http://internal_api:12301/get_cat_coin_price_v2/'
]

const selectedUrl = ref(predefinedUrls[0])
const customUrl = ref('')
const apiResponse = ref('')
const { state: apiState, handleApiCall } = useApiState()

const isValidUrl = computed(() => {
  if (selectedUrl.value === 'custom') {
    return customUrl.value.trim().length > 0
  }
  return true
})

const getEffectiveUrl = () => {
  return selectedUrl.value === 'custom' ? customUrl.value : selectedUrl.value
}

const submitUrl = async () => {
  try {
    const result = await handleApiCall(
      async () => {
        const response = await fetch('/vulnerabilities/ssrf2/submit_api_url/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ url: getEffectiveUrl() }),
        })

        if (!response.ok) {
          const error = await response.json()
          throw new Error(error.detail || 'URL submission failed')
        }

        return response.text()
      },
      'Request successful!'
    )

    apiResponse.value = result
  } catch (error) {
    console.error('Error:', error)
  }
}
</script>
