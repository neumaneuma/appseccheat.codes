<template>
  <div class="challenge-container">
    <h2 class="challenge-title">Challenge #2: SQLi second order</h2>
    <SQLiIntroduction />
    <SQLiNews />
    <div class="forms-grid">
      <!-- Registration Form -->
      <div class="form-section">
        <h3 class="section-title">Register New Account</h3>
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

        <form @submit.prevent="submitRegister" class="form">
          <div class="form-group">
            <label class="form-label" for="username">
              Username
            </label>
            <input
              v-model="registerForm.username"
              :disabled="registerState.isLoading"
              class="form-input"
              :class="{ 'input-error': registerFormErrors.username }"
              name="username"
              id="username"
              type="text"
              placeholder="Username"
            >
            <p v-if="registerFormErrors.username" class="error-message">
              {{ registerFormErrors.username }}
            </p>
          </div>
          <div class="form-group">
            <label class="form-label" for="password">
              Password
            </label>
            <input
              v-model="registerForm.password"
              :disabled="registerState.isLoading"
              class="form-input"
              :class="{ 'input-error': registerFormErrors.password }"
              name="password"
              id="password"
              type="password"
              placeholder="******************"
            >
            <p v-if="registerFormErrors.password" class="error-message">
              {{ registerFormErrors.password }}
            </p>
          </div>
          <div class="form-actions">
            <button
              :disabled="registerState.isLoading || !isRegisterFormValid"
              class="submit-button"
              type="submit"
            >
              <LoadingSpinner v-if="registerState.isLoading" />
              <span v-else>Register</span>
            </button>
          </div>
        </form>
      </div>

      <!-- Change Password Form -->
      <div class="form-section">
        <h3 class="section-title">Change Password</h3>
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

        <form @submit.prevent="submitChangePassword" class="form">
          <div class="form-group">
            <label class="form-label" for="old-password">
              Old Password
            </label>
            <input
              v-model="passwordForm.oldPassword"
              :disabled="changePasswordState.isLoading"
              class="form-input"
              :class="{ 'input-error': passwordFormErrors.oldPassword }"
              name="old-password"
              id="old-password"
              type="password"
              placeholder="Old Password"
            >
            <p v-if="passwordFormErrors.oldPassword" class="error-message">
              {{ passwordFormErrors.oldPassword }}
            </p>
          </div>
          <div class="form-group">
            <label class="form-label" for="new-password">
              New Password
            </label>
            <input
              v-model="passwordForm.newPassword"
              :disabled="changePasswordState.isLoading"
              class="form-input"
              :class="{ 'input-error': passwordFormErrors.newPassword }"
              name="new-password"
              id="new-password"
              type="password"
              placeholder="New Password"
            >
            <p v-if="passwordFormErrors.newPassword" class="error-message">
              {{ passwordFormErrors.newPassword }}
            </p>
          </div>
          <div class="form-group">
            <label class="form-label" for="verify-password">
              Verify New Password
            </label>
            <input
              v-model="passwordForm.verifyPassword"
              :disabled="changePasswordState.isLoading"
              class="form-input"
              :class="{ 'input-error': passwordFormErrors.verifyPassword }"
              name="verify-password"
              id="verify-password"
              type="password"
              placeholder="Verify New Password"
            >
            <p v-if="passwordFormErrors.verifyPassword" class="error-message">
              {{ passwordFormErrors.verifyPassword }}
            </p>
          </div>
          <div class="form-actions">
            <button
              :disabled="changePasswordState.isLoading || !isPasswordFormValid"
              class="submit-button"
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

.forms-grid {
  display: grid;
  gap: 2rem;
  margin-top: 2rem;
}

@media (min-width: 768px) {
  .forms-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.form-section {
  width: 100%;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.form {
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

.input-error {
  border-color: rgb(239, 68, 68);
}

.error-message {
  color: rgb(239, 68, 68);
  font-size: 0.75rem;
  font-style: italic;
  margin-top: 0.25rem;
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
