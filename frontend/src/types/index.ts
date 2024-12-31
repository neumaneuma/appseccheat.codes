export interface ApiResponse {
  message?: string
  error?: string
  detail?: string
}

export interface LoadingState {
  isLoading: boolean
  error: string | null
  success: string | null
}
