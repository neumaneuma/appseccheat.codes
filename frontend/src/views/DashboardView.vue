<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-4xl font-bold mb-8">Security Challenges</h1>

    <div class="mb-12">
      <h2 class="text-2xl font-bold mb-4">SQL Injection Challenges</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <SQLiLoginBypassCard />
        <SQLiSecondOrderCard />
      </div>
    </div>

    <div class="mb-12">
      <h2 class="text-2xl font-bold mb-4">SSRF Challenges</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <SSRFWebhookCard />
        <SSRFLocalFileCard />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import SQLiLoginBypassCard from '@/components/sqli/SQLiLoginBypassCard.vue'
import SQLiSecondOrderCard from '@/components/sqli/SQLiSecondOrderCard.vue'
import SSRFWebhookCard from '@/components/ssrf/SSRFWebhookCard.vue'
import SSRFLocalFileCard from '@/components/ssrf/SSRFLocalFileCard.vue'
</script>
