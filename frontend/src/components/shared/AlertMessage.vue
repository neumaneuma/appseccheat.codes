<template>
  <div v-if="message" :class="[
    'rounded-md p-4 mb-4',
    type === 'error' ? 'bg-red-50 text-red-700 border border-red-700' : 'bg-green-50 text-green-700 border border-green-700'
  ]">
    <p class="text-sm">{{ message }}</p>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  message: string | null
  type: 'error' | 'success'
}>()
</script>
