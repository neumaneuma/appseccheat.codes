<template>
  <div class="about">
    <div class="content-section">
      <h2 class="section-title">What is this?</h2>
      <p class="section-text">
        Hi! My name is Bradley. I created AppSec Cheat Codes while attending a 12 week batch at
        <a href="https://www.recurse.com" target="_blank" rel="noopener">Recurse Center</a>
        in the middle of 2021. After allowing the project to languish for a bit, I revived it at the
        end of 2024.
      </p>
      <p class="section-text">
        The premise of this web app is for developers to learn application security through code. A
        developer's primary skillset is first and foremost coding. There is not much out there for
        software developers to learn how to code securely in a hands-on manner. This web app
        hopefully helps to fill the void a little bit.
      </p>
      <p class="section-text">
        Each challenge provides a vulnerable API endpoint that can be exploited. What makes this
        different from your typical
        <a
          href="https://en.wikipedia.org/wiki/Capture_the_flag_(cybersecurity)"
          target="_blank"
          rel="noopener"
          >CTF</a
        >
        is that the challenges include hints in the form of A) what the vulnerable code looks like,
        and B) what code to exploit it looks like. After solving the challenge, you can then see
        what the patched code looks like that fixes the vulnerability.
      </p>
    </div>
  </div>
</template>

<style scoped>
.about {
  padding: 4rem 2rem;
  max-width: 64rem;
  margin: 0 auto;
  color: rgb(75, 85, 99);
}

.content-section {
  padding-top: 1rem;
  margin-bottom: 1rem;
}

.section-title {
  margin-top: 1.5rem;
  font-size: 1.5rem;
  line-height: 2rem;
  font-weight: 700;
  color: rgb(17, 24, 39);
}

.section-text {
  margin-top: 1rem;
}

.feature-list {
  list-style-type: disc;
  padding-left: 2rem;
  margin-top: 1rem;
}

.feature-list li {
  margin-bottom: 0.5rem;
}

@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
  }
}
</style>
