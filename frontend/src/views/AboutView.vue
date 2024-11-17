<template>
  <div class="about">
    <div class="content-section">
      <h2 class="section-title">Why is this for programmers/software developers?</h2>
      <p class="section-text">
        Hi! My name is Bradley. I created AppSec Cheat Codes while attending a 12 week batch at
        <a href="https://www.recurse.com" target="_blank" rel="noopener">Recurse Center</a>
        in the middle of 2021. If you are a programmer, even with only a few months of experience, I
        would highly recommend applying to Recurse Center. It is a great place to get better at
        developing software and to meet a fantastic community of people.
      </p>
      <p class="section-text">
        The premise of this web app is for people to learn application security through code. A
        programmer's primary skill set is first and foremost code. I find that there is not much out
        there for software developers to learn how to code securely in a hands-on manner. This web
        app hopefully helps to fill the void a little bit more.
      </p>
    </div>

    <div class="content-section">
      <h2 class="section-title">What is next?</h2>
      <p class="section-text">
        I have a lot more planned for what I want to add, though I won't be able to work on this
        full time anymore. Here is what I have in mind (not in any particular order):
      </p>
      <ul class="feature-list">
        <li>
          Port the frontend over from Jinja2 to Elm. I am not a fan of Javascript, so I decided to
          try using a server-side template for the frontend. It turns out that I am not much of a
          fan of server-side templates either. I tried Elm a few years ago, and I liked it, however,
          my functional programming skills are quite rusty.
        </li>
        <li>Add challenges for CORS, XSS, CSRF, and directory traversal vulnerabilities.</li>
        <li>Add implementations of all challenges in golang.</li>
        <li>
          Change the bland purple color for all the cards on the homepage so that it is something
          with a better UI. I didn't know what to put for it since I have 0 knowledge of graphics,
          so the purple was just a placeholder.
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.about {
  padding: 0 1rem;
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
