<template>
  <router-link :to="routePath" class="card">
    <div class="card-image-container">
      <img :src="imagePath" :alt="imageAlt" class="card-image" />
    </div>
    <div class="card-content">
      <h3 class="card-header">{{ header }}</h3>
      <p class="card-description">{{ description }}</p>
      <div class="card-arrow">
        <span>Start Challenge</span>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path d="M5 12h14"></path>
          <path d="m12 5 7 7-7 7"></path>
        </svg>
      </div>
    </div>
  </router-link>
</template>

<script setup lang="ts">
defineProps<{
  imagePath: string
  imageAlt: string
  header: string
  description: string
  routePath: string
}>()
</script>

<style scoped>
.card {
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow:
    0 4px 6px -1px rgb(0 0 0 / 0.1),
    0 2px 4px -2px rgb(0 0 0 / 0.1);
  transition: all 0.3s ease;
  text-decoration: none;
  color: inherit;
  height: 100%;
  border: 1px solid #e5e7eb;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow:
    0 10px 15px -3px rgb(0 0 0 / 0.1),
    0 4px 6px -4px rgb(0 0 0 / 0.1);
}

.card-image-container {
  width: 100%;
  padding: 1.5rem;
  background: #f8fafc;
  border-bottom: 1px solid #e5e7eb;
  aspect-ratio: 16/9;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.card-content {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  flex: 1;
}

.card-header {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.card-description {
  color: #64748b;
  font-size: 0.975rem;
  line-height: 1.5;
  margin: 0;
  flex: 1;
}

.card-arrow {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #2563eb;
  font-weight: 500;
  font-size: 0.875rem;
  margin-top: 0.5rem;
}

.card:hover .card-arrow {
  gap: 0.75rem;
}

.card:hover .card-arrow svg {
  transform: translateX(4px);
}

.card-arrow svg {
  transition: transform 0.2s ease;
}

@media (max-width: 768px) {
  .card-content {
    padding: 1rem;
  }

  .card-image-container {
    padding: 1rem;
  }
}
</style>
