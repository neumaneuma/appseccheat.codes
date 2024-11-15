<template>
  <div class="challenge-container">
    <ChallengeView
      :title="'Challenge #1: SQLi login bypass'"
      :introduction="'What is SQL injection?'"
      :shouldShowIntroduction="shouldShowIntroduction"
      :vulnerabilitySourceCode="{
        fileLink: 'https://github.com/neumaneuma/appseccheat.codes/blob/main/vulnerabilities/sqli1.py',
        snippet: sqliLoginBypassVulnerableSnippet
      }"
      :exploitSourceCode="{
        fileLink: 'https://github.com/neumaneuma/appseccheat.codes/blob/main/exploits/sqli_login_bypass.py',
        snippet: sqliLoginBypassExploitSnippet
      }"
    >
      <template #introduction>
        <SQLiIntroduction />
      </template>
      <template #news>
        <SQLiNews />
      </template>
    </ChallengeView>

    <p class="challenge-description">
      You know there is a user with the username
      <span class="code-block">administrator</span>. Try to figure out how to login as
      <span class="code-block">administrator</span> without knowing what their password is!
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

      <form @submit.prevent="submitLogin" class="login-form">
        <div class="form-group">
          <label class="form-label" for="username">
            Username
          </label>
          <input
            v-model="username"
            :disabled="apiState.isLoading"
            class="form-input"
            name="username"
            id="username"
            type="text"
            placeholder="Username"
          >
        </div>
        <div class="form-group">
          <label class="form-label" for="password">
            Password
          </label>
          <input
            v-model="password"
            :disabled="apiState.isLoading"
            class="form-input"
            name="password"
            id="password"
            type="password"
            placeholder="******************"
          >
        </div>
        <div class="form-actions">
          <button
            :disabled="apiState.isLoading"
            class="submit-button"
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
import { ref, computed } from 'vue'
import { useApiState } from '@/composables/useApiState'
import AlertMessage from '@/components/AlertMessage.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import { SQLI_LOGIN_BYPASS_API_VULNERABLE_URL } from '@/constants'
import SQLiIntroduction from '@/views/sqli/SQLiIntroduction.vue'
import SQLiNews from '@/views/sqli/SQLiNews.vue'
import ChallengeView from '@/views/ChallengeView.vue'
import { store } from '@/store'
import { sqliLoginBypassVulnerableSnippet } from '@/snippets'
import { sqliLoginBypassExploitSnippet } from '@/snippets'

const username = ref('')
const password = ref('')
const { state: apiState, handleApiCall } = useApiState()

function determineIfShouldShowIntroduction() {
  const shouldShowIntroduction = !store.sqliIntroductionSeen
  store.sqliIntroductionSeen = true
  return shouldShowIntroduction
}
const shouldShowIntroduction = computed(determineIfShouldShowIntroduction)


const submitLogin = async () => {
  await handleApiCall(
    async () => {
      const response = await fetch(SQLI_LOGIN_BYPASS_API_VULNERABLE_URL, {
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

.challenge-description {
  margin: 2rem 0;
}

.code-block {
  background-color: rgb(229, 231, 235);
  padding: 0.25rem;
  font-family: ui-monospace, SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace;
}

.form-container {
  width: 100%;
  max-width: 20rem;
}

.login-form {
  background-color: white;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border-radius: 0.375rem;
  padding: 1.5rem 2rem 2rem;
  margin-bottom: 1rem;
}

.form-group {
  margin-bottom: 1.5rem;
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
}

.form-input:focus {
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
</style>
