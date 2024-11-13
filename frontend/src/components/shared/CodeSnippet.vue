<template>
    <pre class="language-{{ language }}">
      <code ref="codeElement" class="language-{{ language }}">{{ code }}</code>
    </pre>
  </template>

  <script setup lang="ts">
  import { ref, onMounted, watch } from 'vue'
  import Prism from 'prismjs'
  import 'prismjs/themes/prism.css' // You can choose a different theme if you like

  const props = defineProps<{
    code: string
    language: string
  }>()

  const codeElement = ref<HTMLElement | null>(null)

  const highlightCode = () => {
    if (codeElement.value) {
      Prism.highlightElement(codeElement.value)
    }
  }

  onMounted(() => {
    highlightCode()
  })

  watch(() => props.code, () => {
    highlightCode()
  })
  </script>

  <style scoped>
  pre {
    background: #f5f5f5;
    padding: 1rem;
    border-radius: 0.5rem;
    overflow-x: auto;
  }
  </style>
