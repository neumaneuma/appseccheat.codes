import { ref } from 'vue'
import type { LoadingState } from '../types'

export function useApiState() {
  const state = ref<LoadingState>({
    isLoading: false,
    error: null,
    success: null,
  })

  const resetState = () => {
    state.value = {
      isLoading: false,
      error: null,
      success: null,
    }
  }

  const handleApiCall = async <T>(apiCall: () => Promise<T>, successMessage: string) => {
    try {
      state.value.isLoading = true
      state.value.error = null
      state.value.success = null

      const response = await apiCall()
      state.value.success = successMessage
      return response
    } catch (error) {
      state.value.error = error instanceof Error ? error.message : 'An unexpected error occurred'
      throw error
    } finally {
      state.value.isLoading = false
    }
  }

  return {
    state,
    resetState,
    handleApiCall,
  }
}
