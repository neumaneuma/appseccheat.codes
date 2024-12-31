<template>
  <div class="ssrf-introduction">
    <p>
      SSRF (server-side request forgery) is when an attacker can trick the server into performing
      HTTP requests on the attacker's behalf. Examples of HTTP requests that can be potentially
      dangerous for a web application are requests to a private IP address (i.e., one that is not
      accessible from the public Internet such as
      <span class="code-block">127.0.0.1</span>), requests to an internal admin API, or requests
      that use the <span class="code-block">file://</span> schema to access internal files on the
      network.
    </p>
    <p>
      How might an attacker pull this off? They simply need a server endpoint that accepts a URL or
      an IP address as input. A
      <a
        href="https://en.wikipedia.org/wiki/Webhook"
        target="_blank"
        rel="noopener"
        class="wiki-link"
        >webhook</a
      >
      is a common feature these days that offers such a vector to attackers. The intended
      functionality of a webhook is to provide a way for client applications to receive
      notifications about events in real-time. But instead of supplying a valid public IP address,
      what if an attacker supplies a private IP address?
    </p>
    <!-- ... rest of the content ... -->
  </div>
</template>

<style scoped>
.ssrf-introduction {
  line-height: 1.5;
}

.ssrf-introduction p {
  margin-bottom: 1rem;
}

.code-block {
  background-color: rgb(229, 231, 235); /* Tailwind's gray-200 */
  padding: 0.25rem;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono',
    'Courier New', monospace;
}

.wiki-link {
  color: inherit;
  text-decoration: none;
}

.wiki-link:hover {
  text-decoration: underline;
}
</style>
