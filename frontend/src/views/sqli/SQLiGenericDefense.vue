<template>
  <div>
    <p>
      This defense makes use of what is known as a
      <a
        href="https://cheatsheetseries.owasp.org/cheatsheets/Query_Parameterization_Cheat_Sheet.html#parameterized-query-examples"
        target="_blank"
        >parameterized query</a
      >. A succinct way of explaining it is that a parameterized query interprets user input as data
      instead of code.
    </p>
    <p>
      Another technique that can supplement a parameterized query is to implement an allowlist. An
      allowlist specifies what characters are allowed as input, and rejects everything else.
      However, for most situations involving SQL injection, it is impractical to implement an
      allowlist because all characters are valid. For example, restricting what characters a user
      can enter for a password is considered a poor user experience. Therefore a parameterized query
      should be the primary line of defense.
    </p>
  </div>
</template>
