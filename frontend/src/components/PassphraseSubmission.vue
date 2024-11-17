<template>
  <section class="challenge-section">
    <h2 class="section-title">Submit Challenge Passphrase</h2>
    <p class="challenge-description">
      Once you've successfully exploited the challenge, submit the passphrase you received to
      complete it.
    </p>

    <div class="form-container">
      <AlertMessage
        v-if="passphraseApiState.error"
        :message="passphraseApiState.error"
        type="error"
      />
      <AlertMessage
        v-if="passphraseApiState.success"
        :message="passphraseApiState.success"
        type="success"
      />

      <form @submit.prevent="submitPassphrase" class="form">
        <div class="form-group">
          <label class="form-label" for="passphrase">Challenge Passphrase</label>
          <input
            v-model="passphrase"
            :disabled="passphraseApiState.isLoading"
            class="form-input"
            name="passphrase"
            id="passphrase"
            type="text"
            placeholder="Enter the passphrase"
          />
        </div>
        <div class="form-actions">
          <button :disabled="passphraseApiState.isLoading" class="submit-button" type="submit">
            <LoadingSpinner v-if="passphraseApiState.isLoading" />
            <span v-else>Submit Passphrase</span>
          </button>
        </div>
      </form>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useApiState } from '@/composables/useApiState'
import AlertMessage from '@/components/AlertMessage.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'

const props = defineProps<{
  challengeId: string
}>()

const router = useRouter()
const passphrase = ref('')
const { state: passphraseApiState, handleApiCall: handlePassphraseApiCall } = useApiState()

const submitPassphrase = async () => {
  await handlePassphraseApiCall(async () => {
    const response = await fetch(`http://localhost:12300/submission`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        secret: passphrase.value,
        challenge: props.challengeId,
      }),
    })

    const body = await response.json()
    if (!response.ok) {
      throw new Error(body.message || 'There was an error submitting the passphrase')
    }

    if (body.result) {
      router.push(`/solutions/${props.challengeId}`)
      return
    }

    throw new Error('Incorrect passphrase')
  }, 'Challenge completed successfully!')
}
</script>

<style scoped>
.challenge-section {
  background-color: white;
  border-radius: 1rem;
  padding: 2rem;
  box-shadow:
    0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: rgb(17, 24, 39);
  margin-bottom: 1rem;
}

.challenge-description {
  margin-bottom: 1.5rem;
  color: rgb(55, 65, 81);
}

.form {
  background-color: rgb(249, 250, 251);
  border-radius: 0.75rem;
  padding: 1.5rem;
  border: 1px solid rgb(229, 231, 235);
  width: 100%;
  box-sizing: border-box;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  color: rgb(55, 65, 81);
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  letter-spacing: 0.025em;
}

.form-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid rgb(209, 213, 219);
  border-radius: 0.5rem;
  color: rgb(55, 65, 81);
  line-height: 1.25;
  transition: all 0.15s ease-in-out;
  background-color: rgb(249, 250, 251);
  box-sizing: border-box;
}

.form-input:hover {
  border-color: rgb(156, 163, 175);
}

.form-input:focus {
  outline: none;
  border-color: rgb(59, 130, 246);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
  background-color: white;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 2rem;
}

.submit-button {
  background-color: rgb(59, 130, 246);
  color: white;
  font-weight: 600;
  padding: 0.75rem 2rem;
  border-radius: 0.5rem;
  transition: all 0.15s ease-in-out;
  border: none;
  cursor: pointer;
  min-width: 8rem;
}

.submit-button:hover:not(:disabled) {
  background-color: rgb(37, 99, 235);
  transform: translateY(-1px);
}

.submit-button:active:not(:disabled) {
  transform: translateY(1px);
}

.submit-button:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.4);
}

.submit-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  background-color: rgb(156, 163, 175);
}
</style>
