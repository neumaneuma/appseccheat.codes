<template>
  <div class="challenge-container">
    <h2 class="challenge-title">Challenge #3: SSRF bypass webhook</h2>

    <SSRFIntroduction class="section-spacing" />
    <SSRFNews class="section-spacing" />

    <p class="section-spacing">
      This web server has a functionality built for webhooks. However, you can abuse this functionality to access an internal admin API.
      The only thing you know is that the internal API can be accessed through
      <span class="code-block">http://internal_api</span>
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

      <form @submit.prevent="submitWebhook" class="webhook-form">
        <div class="form-group">
          <label class="form-label" for="custom_url">
            Enter the URL to use for the webhook:
          </label>
          <input
            v-model="customUrl"
            :disabled="apiState.isLoading"
            class="form-input"
            name="custom_url"
            id="custom_url"
            type="text"
            placeholder="http://example.com/webhook"
          >
        </div>
        <div class="form-actions">
          <button
            :disabled="apiState.isLoading"
            class="submit-button"
            type="submit"
          >
            <LoadingSpinner v-if="apiState.isLoading" />
            <span v-else>Submit</span>
          </button>
        </div>
      </form>

      <!-- Response Display -->
      <div v-if="webhookResponse" class="response-container">
        <h3 class="response-title">Response:</h3>
        <pre class="response-content">{{ webhookResponse }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useApiState } from '@/composables/useApiState'
import AlertMessage from '@/components/shared/AlertMessage.vue'
import LoadingSpinner from '@/components/shared/LoadingSpinner.vue'
import SSRFIntroduction from '@/views/ssrf/SSRFIntroduction.vue'
import SSRFNews from '@/views/ssrf/SSRFNews.vue'

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

.code-block {
  background-color: rgb(229, 231, 235);
  padding: 0.25rem;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas,
    "Liberation Mono", "Courier New", monospace;
}

.form-container {
  width: 100%;
  max-width: 20rem;
}

.webhook-form {
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

.form-input {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 1px solid rgb(229, 231, 235);
  border-radius: 0.25rem;
  color: rgb(55, 65, 81);
  line-height: 1.25;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
  appearance: none;
}

.form-input:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.5);
}

.form-input:disabled {
  background-color: rgb(243, 244, 246);
  cursor: not-allowed;
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
