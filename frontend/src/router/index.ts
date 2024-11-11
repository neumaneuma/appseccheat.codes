import { createRouter, createWebHistory } from 'vue-router'
import SQLiLoginBypassChallenge from '@/views/sqli/SQLiLoginBypassChallenge.vue'
import SQLiSecondOrderChallenge from '@/views/sqli/SQLiSecondOrderChallenge.vue'
import SSRFWebhookChallenge from '@/views/ssrf/SSRFWebhookChallenge.vue'
import SSRFLocalFileChallenge from '@/views/ssrf/SSRFLocalFileChallenge.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/vulnerabilities/sqli1',
      name: 'sqli-login-bypass',
      component: SQLiLoginBypassChallenge,
    },
    {
      path: '/vulnerabilities/sqli2',
      name: 'sqli-second-order',
      component: SQLiSecondOrderChallenge,
    },
    {
      path: '/vulnerabilities/ssrf1',
      name: 'ssrf-webhook',
      component: SSRFWebhookChallenge,
    },
    {
      path: '/vulnerabilities/ssrf2',
      name: 'ssrf-local-file',
      component: SSRFLocalFileChallenge,
    },
  ],
})

export default router
