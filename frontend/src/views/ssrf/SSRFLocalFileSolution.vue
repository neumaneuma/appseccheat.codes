<template>
  <SolutionView
    :patchedSourceCode="patchedSourceCode"
    :title="'Solution #4: SSRF local file inclusion'"
    :previousChallengeLink="'/challenges/ssrf1'"
  >
    <template #solution>
      <p>To prevent SSRF attacks targeting local files:</p>
      <ul>
        <li>Implement strict URL validation and whitelisting</li>
        <li>Use URL parsing libraries to validate URLs</li>
        <li>Block access to internal IP addresses and localhost</li>
        <li>Implement proper access controls and file path validation</li>
      </ul>
    </template>
  </SolutionView>
</template>

<script setup lang="ts">
import SolutionView from '@/views/SolutionView.vue'
import { ssrfLocalFileInclusionPatchedSnippet } from '@/snippets'

const patchedSourceCode = {
  fileLink: 'https://github.com/neumaneuma/appseccheat.codes/blob/main/backend/patches/ssrf_local_file_inclusion.py',
  snippet: ssrfLocalFileInclusionPatchedSnippet
}
</script>
