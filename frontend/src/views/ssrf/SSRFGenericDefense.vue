<template>
  <div>
    <p>
    There are two main ways to defend against an SSRF attack: an allowlist, which is preferred, or a blocklist. However,
    sometimes an allowlist is not feasible because there are an arbitrary number of valid inputs to the application. A
    webhook is one such example where an allowlist is not possible because any public IP address or URL is valid.
    Therefore this solution makes use of a blocklist.
</p>
<p>A blocklist is very difficult to get right because there are so many ways to get around it. At a minimum, any
    implementation of a blocklist to prevent SSRF must include the following features:</p>
<ul>
    <li>
        Rejection of any private IP address. It is important to note that this also includes any URLs that are publicly
        resolvable by DNS to a private IP address or from an <a href="https://www.acunetix.com/blog/web-security-zone/what-are-open-redirects/" target="_blank">open redirect</a>. This can be prevented by performing a DNS look up on any URL, and
        then checking if the IP address falls within the private reserved range.
    </li>
    <li>Rejection of any unresolvable URLs or IP addresses. Failure to do so could result in a denial of service attack
        on
        the web server. To address this requires having a time out on the request so that if it cannot complete in a
        certain
        amount of time the web app would just give up.</li>
    <li>Rejection of any scheme that is not HTTP or HTTPS. Examples of schemes that attackers might try are the <span
            class="code-block">file</span> and <span class="code-block">gopher</span>
        schemes.
    </li>
</ul>
  </div>
</template>

<style scoped>
.code-block {
  background-color: rgb(216, 218, 222);
  padding: 0.15rem;
  font-family: ui-monospace, SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace;
}
</style>
