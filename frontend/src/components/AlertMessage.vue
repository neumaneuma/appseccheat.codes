<template>
  <div v-if="message" :class="['alert', type === 'error' ? 'alert-error' : 'alert-success']">
    <p class="alert-text">{{ message }}</p>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  message: string | null
  type: 'error' | 'success'
}>()
</script>

<style scoped>
.alert {
  border-radius: 0.375rem;
  padding: 1rem;
  margin-bottom: 1rem;
  border-width: 1px;
}

.alert-error {
  background-color: rgb(254, 242, 242);
  color: rgb(185, 28, 28);
  border-color: rgb(185, 28, 28);
}

.alert-success {
  background-color: rgb(240, 253, 244);
  color: rgb(21, 128, 61);
  border-color: rgb(21, 128, 61);
}

.alert-text {
  font-size: 0.875rem;
  line-height: 1.25rem;
}
</style>
