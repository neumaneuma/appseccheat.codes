<template>
  <div class="card-grid">
    <SQLiLoginBypassCard />
    <SQLiSecondOrderCard />
    <SSRFWebhookCard />
    <SSRFLocalFileCard />
  </div>
</template>

<script setup lang="ts">
import SQLiLoginBypassCard from '@/components/sqli/SQLiLoginBypassCard.vue'
import SQLiSecondOrderCard from '@/components/sqli/SQLiSecondOrderCard.vue'
import SSRFWebhookCard from '@/components/ssrf/SSRFWebhookCard.vue'
import SSRFLocalFileCard from '@/components/ssrf/SSRFLocalFileCard.vue'
</script>

<style scoped>
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  padding: 20px;
  width: 100%;
}
</style>
