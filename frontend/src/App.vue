<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <nav class="nav-container">
      <div class="left-nav">
        <RouterLink to="/"
            ><span class="large-font">AppSec Cheat Codes</span></RouterLink
          >
        </div>
        <div class="right-nav">
          <RouterLink to="/about">About</RouterLink>
          <a href="https://github.com/neumaneuma/appseccheat.codes">GitHub</a>
      </div>
    </nav>
  </header>

  <RouterView />
</template>

<style scoped>
.nav-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  padding: 0 20px;
}

.left-nav {
  flex: 1;
}

.right-nav {
  display: flex;
  gap: 20px; /* Adjust spacing between links as needed */
}

.large-font {
  font-size: 20px;
  font-weight: bold;
}
</style>
