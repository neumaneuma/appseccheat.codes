<template>
  <div class="challenge-container">
    <div class="challenge-header">
      <h2 class="page-title">{{ title }}</h2>
      <FirstHint />

      <p v-if="!toggleIntroduction">
        <a class="intro-link" @click="toggleIntroduction = true">Click here</a> to view challenge background again.
      </p>
    </div>

    <template v-if="toggleIntroduction">
      <div class="section">
        <h3 class="section-title">{{ introduction }}</h3>
        <slot name="introduction"></slot>
      </div>
      <div class="section">
        <h3 class="section-title">Heard about it in the news?</h3>
        <slot name="news"></slot>
      </div>
    </template>

    <div class="section">
      <h3 class="section-title">Challenge</h3>
      <SecondHint />

      <!-- Hint 2 -->
      <div class="hint-container hint-error">
        <div class="hint-header collapsible" @click="toggleCollapsible">
          <div class="hint-title">
            <h3 class="hint-text">
              Hint #2:
              <span class="hint-description">What does the server-side vulnerability look like?</span>
            </h3>
          </div>
          <div class="hint-icons">
            <span class="plus" :class="{ hidden: isOpen }">+</span>
            <span class="minus" :class="{ hidden: !isOpen }">-</span>
          </div>
        </div>
        <div class="collapsible-content" ref="content">
          <!-- Code component would go here -->
        </div>
      </div>

      <!-- Hint 3 -->
      <div class="hint-container hint-success">
        <div class="hint-header collapsible" @click="toggleCollapsible">
          <div class="hint-title">
            <h3 class="hint-text">
              Hint #3:
              <span class="hint-description">Couldn't figure out the answer? Here is the exploit</span>
            </h3>
          </div>
          <div class="hint-icons">
            <span class="plus" :class="{ hidden: isOpen }">+</span>
            <span class="minus" :class="{ hidden: !isOpen }">-</span>
          </div>
        </div>
        <div class="collapsible-content" ref="content">
          <p class="exploit-text">
            View the <a href="https://github.com/neumaneuma/appseccheat.codes/blob/main/exploits/README.md"
                       target="_blank"
                       rel="noopener"
                       class="exploit-link">exploit README</a> to run the exploits locally.
          </p>
          <!-- Code component would go here -->
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { toggleCollapsible } from '@/helper'
import FirstHint from '@/views/FirstHint.vue'
import SecondHint from '@/views/SecondHint.vue'

interface Props {
  title: string
  introduction: string
  shouldShowIntroduction: boolean
  vulnerabilitySourceCode?: {
    link: string
    gist: string
  }
  exploitSourceCode?: {
    link: string
    gist: string
  }
}

const props = withDefaults(defineProps<Props>(), {
  shouldShowIntroduction: true,
  currentLink: '',
  vulnerabilitySourceCode: () => ({
    link: '',
    gist: ''
  }),
  exploitSourceCode: () => ({
    link: '',
    gist: ''
  })
})

// Initialize toggleIntroduction with the prop value
const toggleIntroduction = ref(props.shouldShowIntroduction)

// Watch for changes to the prop and update the internal state
watch(
  () => props.shouldShowIntroduction,
  (newValue) => {
    toggleIntroduction.value = newValue
  }
)

const isOpen = ref(false)
const content = ref<HTMLElement | null>(null)
</script>

<style scoped>
.challenge-container {
  padding: 2rem 1rem;
  max-width: 64rem;
  margin: 0 auto;
  color: rgb(75, 85, 99);
}

.challenge-header {
  padding-top: 1rem;
}

.page-title {
  margin-top: 1.5rem;
  font-size: 2.25rem;
  font-weight: 700;
  color: rgb(17, 24, 39);
}

.intro-link {
  color: rgb(96, 165, 250);
  text-decoration: none;
}

.intro-link:hover {
  text-decoration: underline;
}

.section {
  padding-top: 1rem;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: rgb(17, 24, 39);
  margin-bottom: 1rem;
}

.hint-container {
  border-width: 1px;
  border-radius: 0.375rem;
  margin: 1rem 0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.hint-container.hint-error {
  border-color: rgb(127, 29, 29);
  background-color: rgb(254, 242, 242);
}

.hint-container.hint-success {
  border-color: rgb(20, 83, 45);
  background-color: rgb(240, 253, 244);
}

.hint-header {
  display: grid;
  grid-template-columns: 2fr 1fr;
  height: 3rem;
  cursor: pointer;
  border-radius: 0.375rem;
}

.hint-error .hint-header {
  background-color: rgb(254, 202, 202);
}

.hint-error .hint-header:hover {
  background-color: rgb(252, 165, 165);
}

.hint-success .hint-header {
  background-color: rgb(187, 247, 208);
}

.hint-success .hint-header:hover {
  background-color: rgb(134, 239, 172);
}

.hint-title {
  display: flex;
  align-items: center;
  padding-left: 1rem;
}

.hint-text {
  font-size: 1rem;
  font-weight: 700;
  color: rgb(17, 24, 39);
}

.hint-error .hint-description {
  color: rgb(185, 28, 28);
}

.hint-error .hint-description:hover {
  color: rgb(153, 27, 27);
}

.hint-success .hint-description {
  color: rgb(22, 163, 74);
}

.hint-success .hint-description:hover {
  color: rgb(21, 128, 61);
}

.hint-icons {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 700;
}

.hidden {
  display: none;
}

.collapsible-content {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease-out;
  padding: 0 1rem;
}

.exploit-text {
  margin-top: 1rem;
}

.exploit-link {
  color: rgb(96, 165, 250);
  text-decoration: none;
}

.exploit-link:hover {
  text-decoration: underline;
}

@media (min-width: 640px) {
  .hint-header {
    height: 3rem;
  }
}
</style>
