<template>
  <div class="challenge-container">
    <ChallengeView
      :title="'Challenge #4: SSRF local file inclusion'"
      :introduction="'What is SSRF?'"
      :shouldShowIntroduction="shouldShowIntroduction"
    >
      <template #introduction>
        <SSRFIntroduction />
      </template>
      <template #news>
        <SSRFNews />
      </template>
    </ChallengeView>

    <p class="section-spacing">
      Catcoin is the hot new crypto currency that everyone is talking about. The following form is for a financial web app
      that will allow you to pick the API that is used to query the current price of catcoin.
    </p>

    <div class="api-urls">
      <code class="code-block">http://internal_api:12301/get_cat_coin_price_v1/</code>
      <code class="code-block">http://internal_api:12301/get_cat_coin_price_v2/</code>
    </div>

    <p class="instruction-text">
      Solve this challenge by stealing the
      <code class="inline-code">file:///etc/shadow</code> or
      <code class="inline-code">file:///etc/passwd</code> files.
    </p>

    <div class="form-container">
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

      <form @submit.prevent="submitUrl" class="api-form">
        <div class="form-group">
          <label class="form-label" for="api_url">
            Enter the API URL:
          </label>
          <div class="radio-group">
            <div v-for="(url, index) in predefinedUrls" :key="index" class="radio-option">
              <input
                type="radio"
                :id="'url-' + index"
                v-model="selectedUrl"
                :value="url"
                class="radio-input"
                :disabled="apiState.isLoading"
              >
              <label :for="'url-' + index">{{ url }}</label>
            </div>
            <div class="radio-option">
              <input
                type="radio"
                id="custom-url"
                v-model="selectedUrl"
                value="custom"
                class="radio-input"
                :disabled="apiState.isLoading"
              >
              <label for="custom-url">Custom URL</label>
            </div>
          </div>
          <input
            v-if="selectedUrl === 'custom'"
            v-model="customUrl"
            :disabled="apiState.isLoading"
            class="url-input"
            type="text"
            placeholder="Enter custom URL"
          >
        </div>
        <div class="form-actions">
          <button
            :disabled="apiState.isLoading || !isValidUrl"
            class="submit-button"
            type="submit"
          >
            <LoadingSpinner v-if="apiState.isLoading" />
            <span v-else>Get Price</span>
          </button>
        </div>
      </form>

      <!-- Response Display -->
      <div v-if="apiResponse" class="response-container">
        <h3 class="response-title">Response:</h3>
        <pre class="response-content">{{ apiResponse }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useApiState } from '@/composables/useApiState'
import AlertMessage from '@/components/shared/AlertMessage.vue'
import LoadingSpinner from '@/components/shared/LoadingSpinner.vue'
import SSRFIntroduction from '@/views/ssrf/SSRFIntroduction.vue'
import SSRFNews from '@/views/ssrf/SSRFNews.vue'
import ChallengeView from '@/views/ChallengeView.vue'
import { store } from '@/store'

const predefinedUrls = [
  'http://internal_api:12301/get_cat_coin_price_v1/',
  'http://internal_api:12301/get_cat_coin_price_v2/'
]

const selectedUrl = ref(predefinedUrls[0])
const customUrl = ref('')
const apiResponse = ref('')
const { state: apiState, handleApiCall } = useApiState()

function determineIfShouldShowIntroduction() {
  const shouldShowIntroduction = !store.ssrfIntroductionSeen
  store.ssrfIntroductionSeen = true
  return shouldShowIntroduction
}
const shouldShowIntroduction = computed(determineIfShouldShowIntroduction)

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

<style scoped>
.challenge-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.challenge-title {
  margin-top: 1.5rem;
  font-size: 2.25rem;
  line-height: 2.5rem;
  font-weight: 700;
  color: rgb(17, 24, 39);
}

.section-spacing {
  margin: 2rem 0;
}

.api-urls {
  display: flex;
  gap: 1rem;
  margin: 1rem 0;
}

.code-block {
  background-color: rgb(229, 231, 235);
  padding: 0.5rem;
  font-size: 0.875rem;
  border-radius: 0.25rem;
}

.inline-code {
  background-color: rgb(229, 231, 235);
  padding: 0.25rem;
}

.instruction-text {
  margin: 1rem 0;
}

.form-container {
  width: 100%;
  max-width: 20rem;
}

.api-form {
  background-color: white;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border-radius: 0.375rem;
  padding: 1.5rem 2rem 2rem;
  margin-bottom: 1rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-label {
  display: block;
  color: rgb(55, 65, 81);
  font-size: 0.875rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.radio-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.radio-option {
  display: flex;
  align-items: center;
}

.radio-input {
  margin-right: 0.5rem;
}

.url-input {
  margin-top: 0.5rem;
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 1px solid rgb(229, 231, 235);
  border-radius: 0.25rem;
  color: rgb(55, 65, 81);
  line-height: 1.25;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
}

.url-input:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.5);
}

.form-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.submit-button {
  background-color: rgb(107, 114, 128);
  color: white;
  font-weight: 700;
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
}

.submit-button:hover:not(:disabled) {
  background-color: rgb(156, 163, 175);
}

.submit-button:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.5);
}

.submit-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.response-container {
  margin-top: 1rem;
  padding: 1rem;
  background-color: rgb(243, 244, 246);
  border-radius: 0.375rem;
}

.response-title {
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.response-content {
  white-space: pre-wrap;
  font-size: 0.875rem;
}
</style>
