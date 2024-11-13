<template>
  <div class="hint-container">
    <div class="hint-header collapsible" @click="toggleCollapsible">
      <div class="hint-title">
        <h3 class="hint-text">
          How should I approach this?
        </h3>
      </div>
      <div class="hint-icons">
        <span class="plus" :class="{ hidden: isOpen }">+</span>
        <span class="minus" :class="{ hidden: !isOpen }">-</span>
      </div>
    </div>
    <div class="collapsible-content" ref="content">
      <div class="content-wrapper">
        <p>This is a <a href="https://dev.to/atan/what-is-ctf-and-how-to-get-started-3f04" target="_blank" rel="noopener" class="link">capture the flag (CTF)</a> webapp designed to teach software developers the fundamentals of <a href="https://en.wikipedia.org/wiki/Application_security" target="_blank" rel="noopener" class="link">application security (AppSec)</a>. Software developers learn best when reading and writing code. Most CTFs are catered towards <a href="https://en.wikipedia.org/wiki/Penetration_test" target="_blank" rel="noopener" class="link">pentesters</a> who predominantly use a variety of tools for CTFs and in their day jobs. While certainly a more efficient approach, this does not, however, translate well for a software developer trying to learn AppSec.</p>

        <p>How is a software developer supposed to learn how to write secure code if all they learn how to do from a CTF is click a few buttons and enter some input into a text field? That is why the purpose of this CTF is to reframe the concept of AppSec in terms of code.</p>

        <p>There are 3 hints for every challenge. One hint will show you <span class="emphasis">the exact code of the server-side vulnerability that you are trying to exploit</span>. It is one thing to read a description of a vulnerability, and a whole another thing to actually see a working example of the code. Another hint will show you <span class="emphasis">the exact code of the exploit and how to run it</span>. Technically this is less of a hint and more just the answer to how to solve the challenge, but let's not get too hung up on semantics.</p>

        <p>The next logical step is to provide the diff between what the vulnerable code looks like and what the secure code looks like. This is accessible to anyone who solves the challenge, which considering the exploit is provided if you cannot figure out how to write it on your own, is literally anyone.</p>

        <p>And finally, as if this wall of text wasn't long enough, there is even more to it. If you want to run the webapp locally just follow the instructions on this <a href="https://github.com/neumaneuma/appseccheat.codes/blob/main/README.md" target="_blank" rel="noopener" class="link">README</a>. Make any modifications you want. Add code, remove code, break things, figure out how to fix them. This is what I believe to be the most effective way for a developer to learn a concept: through code.</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { toggleCollapsible } from '../helper'
const isOpen = ref(false)
const content = ref<HTMLElement | null>(null)


</script>

<style scoped>
.hint-container {
  border: 1px solid rgb(17, 24, 39);
  border-radius: 0.375rem;
  background-color: white;
  margin: 1rem 0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.hint-header {
  display: grid;
  grid-template-columns: 2fr 1fr;
  height: 3rem;
  background-color: rgb(229, 231, 235);
  border-radius: 0.375rem;
  cursor: pointer;
}

.hint-header:hover {
  background-color: rgb(209, 213, 219);
}

.hint-title {
  display: flex;
  align-items: center;
  padding-left: 1rem;
  grid-column: span 2;
}

.hint-text {
  font-size: 1rem;
  font-weight: 700;
  color: rgb(17, 24, 39);
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

.emphasis {
  font-style: italic;
}

@media (min-width: 640px) {
  .hint-header {
    height: 3rem;
  }
}
</style>
