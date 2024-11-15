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
    <ChallengeCard
    :imagePath="sqliLoginBypassImage"
    imageAlt="Open lock"
    header="SQLi: login bypass"
    description="Forget passkeys, this is how you do true passwordless login"
    routePath="/vulnerabilities/sqli1"
  />        <ChallengeCard
    :imagePath="sqliSecondOrderImage"
    imageAlt="Double agent"
    header="SQLi: second order"
    description="Sometimes the injection doesn't happen right away"
    routePath="/vulnerabilities/sqli2"
  />        <ChallengeCard
    :imagePath="ssrfWebhookImage"
    imageAlt="Castle with breached walls"
    header="SSRF: webhook"
    description="Sometimes you need to make a request to an external service"
    routePath="/vulnerabilities/ssrf1"
  />        <ChallengeCard
    :imagePath="ssrfLocalFileInclusionImage"
    imageAlt="Confused deputy"
    header="SSRF: local file inclusion"
    description="Sometimes you need to read a local file"
    routePath="/vulnerabilities/ssrf2"
  />
    </div>
  </div>
</template>

<script setup lang="ts">
import ChallengeCard from '@/components/ChallengeCard.vue'
import sqliLoginBypassImage from '@/assets/sqli_login_bypass.svg'
import sqliSecondOrderImage from '@/assets/sqli_second_order.svg'
import ssrfWebhookImage from '@/assets/ssrf_webhook.svg'
import ssrfLocalFileInclusionImage from '@/assets/ssrf_local_file_inclusion.svg'
</script>

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
