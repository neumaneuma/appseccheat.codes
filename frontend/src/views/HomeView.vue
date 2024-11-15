<template>
  <div>
  <div class="home-container">
    <p>
      Learn how to avoid
      <span class="code-text code-text-vulnerable">vulnerable code</span>
    </p>
    <p>
      Learn what
      <span class="code-text code-text-exploit">exploit code</span>
      looks like
    </p>
    <p>
      Learn how to write
      <span class="code-text code-text-secure">secure code</span>
    </p>
  </div>
  <div class="card-grid">
      <SQLiLoginBypassCard />
      <SQLiSecondOrderCard />
      <SSRFWebhookCard />
        <SSRFLocalFileCard />
    </div>
  </div>
</template>

<script setup lang="ts">
import SQLiLoginBypassCard from '@/components/sqli/SQLiLoginBypassCard.vue'
import SQLiSecondOrderCard from '@/components/sqli/SQLiSecondOrderCard.vue'
import SSRFWebhookCard from '@/components/ssrf/SSRFWebhookCard.vue'
import SSRFLocalFileCard from '@/components/ssrf/SSRFLocalFileCard.vue'</script>

<style scoped>
.home-container {
  padding-top: 4rem;
  padding-bottom: 2rem;
  text-align: center;
  font-weight: bold;
  font-size: 1.25rem;
  line-height: 1.75rem;
}

.code-text {
  font-family: monospace;
  padding: 0.25rem;
}

.code-text-vulnerable {
  background-color: #fecaca;
  color: #b91c1c;
  border-radius: 4px;
}

.code-text-exploit {
  background-color: #a7f3d0;
  color: #047857;
  border-radius: 4px;
}

.code-text-secure {
  background-color: #bfdbfe;
  color: #1d4ed8;
  border-radius: 4px;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  justify-items: center;
  width: 80%;
  margin: 0 auto;
}

</style>
