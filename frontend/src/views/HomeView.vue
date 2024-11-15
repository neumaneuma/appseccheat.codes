<template>
  <div class="home-container">
    <p>
      Learn how to avoid
      <span class="code-text code-text-danger">vulnerable code</span>
    </p>
    <p>
      Learn what
      <span class="code-text code-text-success">exploit code</span>
      looks like
    </p>
    <p>
      Learn how to write
      <span class="code-text code-text-primary">secure code</span>
    </p>
    <DashboardView />
  </div>
</template>

<script setup lang="ts">
import DashboardView from '@/views/DashboardView.vue'
</script>

<style scoped>
.home-container {
  padding-top: 8rem;
  text-align: center;
  font-weight: bold;
  font-size: 1.25rem;
  line-height: 1.75rem;
}

.code-text {
  font-family: monospace;
  padding: 0.25rem;
}

.code-text-danger {
  background-color: #fecaca;
  color: #b91c1c;
  border-radius: 4px;
}

.code-text-success {
  background-color: #a7f3d0;
  color: #047857;
  border-radius: 4px;
}

.code-text-primary {
  background-color: #bfdbfe;
  color: #1d4ed8;
  border-radius: 4px;
}
</style>
