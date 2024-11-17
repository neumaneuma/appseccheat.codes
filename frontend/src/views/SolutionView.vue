<template>
  <div class="solution-container">
    <div class="solution-header">
      <h2 class="page-title">{{ title }}</h2>
    </div>

    <div>
      <h3 class="section-title">How to Fix This Vulnerability</h3>
      <div class="content-wrapper">
        <slot name="solution"></slot>
      </div>
    </div>

    <div class="hint-container solution-hint">
      <div class="hint-header">
        <div class="hint-title">
          <h3 class="hint-text">Secure Implementation</h3>
        </div>
      </div>
      <div class="code-container">
        <p>
          File truncated for brevity.
          <a :href="patchedSourceCode.fileLink" class="link" target="_blank">Click here</a> to view
          full file.
        </p>
        <CodeSnippet :code="patchedSourceCode.snippet" :language="'python'" />
      </div>
    </div>

    <div class="navigation-buttons">
      <RouterLink
        v-if="previousChallengeLink"
        :to="previousChallengeLink"
        class="nav-button previous"
      >
        ← Previous Challenge
      </RouterLink>
      <RouterLink v-if="nextChallengeLink" :to="nextChallengeLink" class="nav-button next">
        Next Challenge →
      </RouterLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
import CodeSnippet from '@/components/CodeSnippet.vue'

type SourceCodeLinks = {
  fileLink: string
  snippet: string
}

interface Props {
  patchedSourceCode: SourceCodeLinks
  title: string
  previousChallengeLink?: string
  nextChallengeLink?: string
}

defineProps<Props>()
</script>

<style scoped>
.solution-container {
  padding: 4rem 2rem;
  max-width: 64rem;
  margin: 0 auto;
  color: rgb(75, 85, 99);
}

.solution-header {
  padding-top: 1rem;
}

.page-title {
  margin-top: 1.5rem;
  font-size: 2.25rem;
  font-weight: 700;
  color: rgb(17, 24, 39);
}

.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: rgb(17, 24, 39);
  margin-bottom: 1rem;
}

.hint-container {
  border-width: 1px;
  border: 1px solid rgb(37, 99, 235); /* blue-600 */
  border-radius: 0.375rem;
  margin: 1rem 0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  background-color: white;
}

.hint-container.solution-hint {
  border-color: rgb(37, 99, 235); /* blue-600 */
}

.hint-header {
  display: grid;
  grid-template-columns: 2fr 1fr;
  height: 3rem;
  border-radius: 0.375rem;
  background-color: rgb(219, 234, 254); /* blue-100 */
}

.hint-title {
  display: flex;
  align-items: center;
  padding-left: 1rem;
}

.hint-text {
  font-size: 1rem;
  font-weight: 700;
  color: rgb(37, 99, 235); /* blue-600 */
}

.content-wrapper {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.code-container {
  padding: 1rem;
}

.link {
  color: rgb(96, 165, 250);
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}

.navigation-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 3rem;
  padding: 1rem 0;
}

.nav-button {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  border-radius: 0.375rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease;
  background-color: rgb(96, 165, 250);
  color: white;
}

.nav-button:hover {
  background-color: rgb(59, 130, 246);
  transform: translateY(-1px);
}

.nav-button.previous {
  margin-right: auto;
}

.nav-button.next {
  margin-left: auto;
}

@media (max-width: 640px) {
  .navigation-buttons {
    flex-direction: column;
    gap: 1rem;
  }

  .nav-button {
    text-align: center;
  }
}
</style>
