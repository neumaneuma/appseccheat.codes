<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header class="banner">
    <nav class="nav-container">
      <div class="left-nav">
        <RouterLink to="/" class="nav-link large-font">AppSec Cheat Codes</RouterLink>
      </div>
      <div class="right-nav">
        <RouterLink to="/about" class="nav-link">About</RouterLink>
        <a href="https://github.com/neumaneuma/appseccheat.codes" class="nav-link">GitHub</a>
      </div>
    </nav>
  </header>

  <RouterView />
</template>

<style scoped>
.banner {
  background-color: #ffffff; /* Dark blue background */
  padding: 10px 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.nav-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 20px;
}

.left-nav {
  flex: 1;
}

.right-nav {
  display: flex;
  gap: 20px;
}

.large-font {
  font-size: 24px;
  font-weight: bold;
}

.nav-link {
  color: #3d474b;
  text-decoration: none;
  font-size: 18px;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.3s, color 0.3s;
}

.nav-link:hover {
  background-color: #bfdbfe;
  color: #1d4ed8;
}


</style>
