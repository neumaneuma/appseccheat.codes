<template>
  <SolutionView
    :patchedSourceCode="patchedSourceCode"
    :title="'Solution #3: SSRF bypass webhook'"
    :previousChallengeLink="'/challenges/sqli2'"
    :nextChallengeLink="'/challenges/ssrf2'"
  >
    <template #solution>
      <p>To prevent SSRF attacks in webhook implementations:</p>
      <ul>
        <li>Implement strict URL validation and whitelisting</li>
        <li>Validate and sanitize all user-provided URLs</li>
        <li>Use a webhook signing mechanism to verify requests</li>
        <li>Implement rate limiting and timeout controls</li>
      </ul>
    </template>
  </SolutionView>
</template>

<script setup lang="ts">
import SolutionView from '@/views/SolutionView.vue'
import { ssrfWebhookPatchedSnippet } from '@/snippets'

const patchedSourceCode = {
  fileLink: 'https://github.com/neumaneuma/appseccheat.codes/blob/main/backend/patches/ssrf_webhook.py',
  snippet: ssrfWebhookPatchedSnippet
}
</script>
