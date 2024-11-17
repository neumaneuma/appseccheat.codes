<template>
  <SolutionView
    :patchedSourceCode="patchedSourceCode"
    :previousChallengeLink="'/challenge/sqli-login-bypass'"
    :nextChallengeLink="'/challenge/sqli-second-order'"
  >
    <template #solution>
      <p>To fix SQL injection vulnerabilities in login forms, you should:</p>
      <ul>
        <li>Use parameterized queries or prepared statements instead of string concatenation</li>
        <li>Implement proper input validation and sanitization</li>
        <li>Use an ORM (Object-Relational Mapping) when possible</li>
        <li>Follow the principle of least privilege for database users</li>
      </ul>
    </template>
  </SolutionView>
</template>

<script setup lang="ts">
import SolutionView from '@/views/SolutionView.vue'
import { sqliLoginBypassPatchedSnippet } from '@/snippets'

const patchedSourceCode = {
  fileLink: 'https://github.com/neumaneuma/appseccheat.codes/blob/main/backend/patches/sqli_login_bypass.py',
  snippet: sqliLoginBypassPatchedSnippet
}
</script>
