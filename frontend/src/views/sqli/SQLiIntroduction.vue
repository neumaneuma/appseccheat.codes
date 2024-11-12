<template>
  <div class="sqli-intro">
    <p>
      SQL injection is when an attacker can trick the server into running attacker-supplied SQL code against its database. For
      example, suppose you are an
      <a href="https://xkcd.com/327/" target="_blank" rel="noopener noreferrer" class="link">elite hacker mom</a>. You name your son
      <span class="code-block">Robert'); DROP TABLE Students;--</span>
      and send him off to school.
    </p>

    <p>
      If your son's school has a server that is vulnerable to SQL injection, then when they go to add your son as a student in
      the school's database this is the SQL query that is run:
    </p>

    <p class="code-example">
      <span class="sql-code">INSERT INTO Students VALUES '</span>
      <span class="user-input">Robert</span>
      <span class="sql-code">'); DROP TABLE Students;</span>
      <span class="sql-comment">-- ');</span>
    </p>

    <p class="sql-code">Black text is SQL code</p>
    <p class="user-input">Red text is data from the user</p>
    <p class="sql-comment">Green text is a comment</p>

    <p>
      The intended result is for an insert statement to be executed. However, because the school is vulnerable to SQL
      injection, what happens is that the insert statement is executed, and then a drop statement is subsequently executed.
    </p>

    <p>
      In plain English: a student named Robert gets added to the list of students at the school, and then that list of
      students is subsequently deleted. This is how the student records are lost for the year. What would the SQL query look
      like if the school wasn't vulnerable to SQL injection?
    </p>

    <p class="code-example">
      <span class="sql-code">INSERT INTO Students VALUES '</span>
      <span class="user-input">Robert'); DROP TABLE Students;--</span>
      <span class="sql-code">');</span>
    </p>
  </div>
</template>

<style scoped>
.sqli-intro {
  line-height: 1.5;
}

.sqli-intro p {
  margin-bottom: 1rem;
}

.link {
  color: rgb(59, 130, 246);
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}

.code-block, .code-example {
  background-color: rgb(229, 231, 235);
  padding: 0.25rem;
  font-family: ui-monospace, SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace;
}

.code-example {
  display: inline-block;
  width: max-content;
}

.sql-code {
  color: rgb(17, 24, 39);
}

.user-input {
  color: rgb(239, 68, 68);
}

.sql-comment {
  color: rgb(16, 185, 129);
}
</style>
