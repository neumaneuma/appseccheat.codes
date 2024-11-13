<template>
  <div class="hint-container">
    <div class="hint-header collapsible" @click="toggleCollapsible">
      <div class="hint-title">
        <h3 class="hint-text">
          Hint #1: <span class="hint-description">Generic Hint</span>
        </h3>
      </div>
      <div class="hint-icons">
        <span class="plus" :class="{ hidden: isOpen }">+</span>
        <span class="minus" :class="{ hidden: !isOpen }">-</span>
      </div>
    </div>
    <div class="collapsible-content" ref="content">
      <div class="content-wrapper">
        <p>If you are unsure on how to proceed, then the following may help:</p>

        <p>You can enter the input necessary to exploit this challenge manually through your browser, or you can use an automated tool such as <a href="https://portswigger.net/burp" target="_blank" rel="noopener" class="link">Burp Suite</a> or <a href="https://www.zaproxy.org" target="_blank" rel="noopener" class="link">OWASP ZAP</a>. However, since this CTF is focused specifically on the code side of application security, neither of those solutions will be presented here.</p>

        <p>The exploit code and instructions on how to run it is presented in the third hint. However, you are encouraged to attempt to write the exploit code yourself before looking at the answer. In order to do this, you need to understand what fields are being set in the HTTP request being sent to the server from the browser. This is so that you can craft your own HTTP request from the script you write. You can use your <a href="https://www.twilio.com/blog/2017/09/everything-you-ever-wanted-to-know-about-secure.html-forms.html" target="_blank" rel="noopener" class="link">browser's developer tools</a> to figure out this information or you can use a tool that can decrypt encrypted traffic on your computer. Burp Suite and OWASP ZAP both offer this feature in addition to their automated pentesting. I personally used <a href="https://mitmproxy.org" target="_blank" rel="noopener" class="link">mitmproxy</a> when writing the exploit scripts for this site because it has a lot fewer features than those other tools, and therefore is a lot simpler to use.</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const isOpen = ref(false)
const content = ref<HTMLElement | null>(null)

const toggleCollapsible = () => {
  isOpen.value = !isOpen.value

  if (content.value) {
    if (content.value.style.maxHeight) {
      content.value.style.maxHeight = ''
    } else {
      content.value.style.maxHeight = `${content.value.scrollHeight}px`
    }
  }
}
</script>

<style scoped>
.hint-container {
  border: 1px solid rgb(120, 113, 108);
  border-radius: 0.375rem;
  background-color: rgb(254, 252, 232);
  margin: 1rem 0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.hint-header {
  display: grid;
  grid-template-columns: 1fr 1fr;
  height: 3rem;
  background-color: rgb(254, 240, 138);
  border-radius: 0.375rem;
  cursor: pointer;
}

.hint-header:hover {
  background-color: rgb(253, 224, 71);
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

.hint-description {
  color: rgb(161, 98, 7);
}

.hint-description:hover {
  color: rgb(133, 77, 14);
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
}

.content-wrapper {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.link {
  color: rgb(96, 165, 250);
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}

@media (min-width: 640px) {
  .hint-header {
    height: 3rem;
  }
}
</style>
