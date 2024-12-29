<template>
  <div class="page-container">
    <div class="home-container">
      <div class="taglines">
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
    </div>
    <div class="card-grid">
      <ChallengeCard
        :imagePath="sqliLoginBypassImage"
        imageAlt="Open lock"
        header="SQLi: login bypass"
        description="Forget passkeys, this is how you do true passwordless login"
        routePath="/challenges/sqli1"
      />
      <ChallengeCard
        :imagePath="sqliSecondOrderImage"
        imageAlt="Double agent"
        header="SQLi: second order"
        description="Sometimes the injection doesn't happen right away"
        routePath="/challenges/sqli2"
      />
      <ChallengeCard
        :imagePath="ssrfWebhookImage"
        imageAlt="Castle with breached walls"
        header="SSRF: webhook"
        description="Sometimes you need to make a request to an external service"
        routePath="/challenges/ssrf1"
      />
      <ChallengeCard
        :imagePath="ssrfLocalFileInclusionImage"
        imageAlt="Confused deputy"
        header="SSRF: local file inclusion"
        description="Sometimes you need to read a local file"
        routePath="/challenges/ssrf2"
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
.page-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.home-container {
  padding: 4rem 1rem;
  text-align: center;
}

.main-title {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 2rem;
  background: linear-gradient(45deg, #1d4ed8, #047857);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.taglines {
  font-weight: bold;
  font-size: 1.25rem;
  line-height: 2.5rem;
}

.code-text {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  padding: 0.25rem 0.5rem;
  transition: transform 0.2s ease;
  display: inline-block;
}

.code-text:hover {
  transform: translateY(-2px);
}

.code-text-vulnerable {
  background-color: #fecaca;
  color: #b91c1c;
  border-radius: 6px;
}

.code-text-exploit {
  background-color: #a7f3d0;
  color: #047857;
  border-radius: 6px;
}

.code-text-secure {
  background-color: #bfdbfe;
  color: #1d4ed8;
  border-radius: 6px;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  width: 100%;
  padding: 2rem 0;
}

/* Add responsive design */
@media (max-width: 768px) {
  .main-title {
    font-size: 2rem;
  }

  .taglines {
    font-size: 1.1rem;
    line-height: 2rem;
  }

  .card-grid {
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    padding: 1rem 0;
  }
}
</style>
