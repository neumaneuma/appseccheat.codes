<template>
  <router-link :to="routePath" class="card-link">
    <div class="card">
      <img :src="imagePath" :alt="imageAlt" class="logo" />
      <h3 class="title">{{ header }}</h3>
      <p class="description">{{ description }}</p>
    </div>
  </router-link>
</template>

<script setup lang="ts">
interface CardProps {
  imagePath: string
  imageAlt: string
  header: string
  description: string
  routePath: string
}

defineProps<CardProps>()
</script>

<style scoped>
.card-link {
  text-decoration: none;
  color: inherit;
  cursor: pointer;
}

.card {
  width: 300px;
  height: 300px;
  border: 2px solid #e1e4e8;
  border-radius: 20px;
  padding: 16px;
  background-color: #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition:
    transform 0.2s ease-in-out,
    box-shadow 0.2s ease-in-out;
}

.logo {
  width: 100%;
  height: auto;
  max-width: 200px;
  max-height: 200px;
}

.title {
  font-weight: bold;
  font-size: 20px;
  margin-top: 10px;
  transition: text-decoration-color 0.2s ease-in-out;
  text-decoration: underline transparent;
}

.description {
  font-size: 13px;
  color: #767373;
  margin: 8px 0 12px;
  text-align: center;
  transition: text-decoration-color 0.2s ease-in-out;
  text-decoration: underline transparent;
}

.card-link:hover .title {
  text-decoration: underline;
}
</style>
