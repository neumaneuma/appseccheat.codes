<template>
  <div class="ssrf-news">
    <p>
      SSRF is arguably the most popular vulnerability being exploited today. It is not easy to
      defend against, and it can cause a lot of damage. Here are three recent examples of it being
      exploited:
    </p>
    <ul class="news-list">
      <li>
        2019: Capital One
        <a
          href="https://krebsonsecurity.com/2019/08/what-we-can-learn-from-the-capital-one-hack/"
          target="_blank"
          rel="noopener"
          >suffered a breach of over 100 million customers because of SSRF</a
        >
      </li>
      <li>
        2020: Atlassian fell victim to the same
        <a href="https://jira.atlassian.com/browse/BSERV-12433" target="_blank" rel="noopener"
          >webhook attack described above</a
        >
      </li>
      <li>
        2021: Microsoft Exchange servers
        <a
          href="https://www.extrahop.com/company/blog/2021/exchange-server-security/"
          target="_blank"
          rel="noopener"
          >were compromised to devastating effect</a
        >
      </li>
    </ul>
  </div>
</template>

<style scoped>
.ssrf-news {
  line-height: 1.5;
}

.ssrf-news p {
  margin-bottom: 1rem;
}

.news-list {
  list-style-type: disc;
  padding-left: 2rem;
}

.news-list li {
  margin-bottom: 0.5rem;
}

.news-list a {
  color: inherit;
  text-decoration: none;
}

.news-list a:hover {
  text-decoration: underline;
}
</style>
