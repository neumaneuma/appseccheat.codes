<template>
  <SolutionView
    :patchedSourceCode="patchedSourceCode"
    :title="'Solution #2: SQLi second order'"
    :previousChallengeLink="'/challenges/sqli2'"
    :nextChallengeLink="'/challenges/ssrf1'"
  >
    <template #solution>
      <p>To prevent second-order SQL injection attacks:</p>
      <ul>
        <li>Use parameterized queries for both data insertion and retrieval</li>
        <li>Implement proper input validation at all data entry points</li>
        <li>Sanitize data both when storing and retrieving from the database</li>
        <li>Use proper escaping mechanisms when necessary</li>
      </ul>
    </template>
  </SolutionView>
</template>

<script setup lang="ts">
import SolutionView from '@/views/SolutionView.vue'
import { sqliSecondOrderPatchedSnippet } from '@/snippets'

const patchedSourceCode = {
  fileLink: 'https://github.com/neumaneuma/appseccheat.codes/blob/main/backend/patches/sqli_second_order.py',
  snippet: sqliSecondOrderPatchedSnippet
}
</script>
