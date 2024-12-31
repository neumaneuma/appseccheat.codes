import { createRouter, createWebHistory, type RouteLocationNormalizedGeneric } from 'vue-router'
import SQLiLoginBypassChallenge from '../views/sqli/SQLiLoginBypassChallenge.vue'
import SQLiSecondOrderChallenge from '../views/sqli/SQLiSecondOrderChallenge.vue'
import SSRFWebhookChallenge from '../views/ssrf/SSRFWebhookChallenge.vue'
import SSRFLocalFileChallenge from '../views/ssrf/SSRFLocalFileChallenge.vue'
import SQLiLoginBypassSolution from '../views/sqli/SQLiLoginBypassSolution.vue'
import SQLiSecondOrderSolution from '../views/sqli/SQLiSecondOrderSolution.vue'
import SSRFWebhookSolution from '../views/ssrf/SSRFWebhookSolution.vue'
import SSRFLocalFileSolution from '../views/ssrf/SSRFLocalFileSolution.vue'
import AboutView from '../views/AboutView.vue'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/challenges/sqli1',
      name: 'sqli1-challenge',
      component: SQLiLoginBypassChallenge,
    },
    {
      path: '/challenges/sqli2',
      name: 'sqli2-challenge',
      component: SQLiSecondOrderChallenge,
    },
    {
      path: '/challenges/ssrf1',
      name: 'ssrf1-challenge',
      component: SSRFWebhookChallenge,
    },
    {
      path: '/challenges/ssrf2',
      name: 'ssrf2-challenge',
      component: SSRFLocalFileChallenge,
    },
    {
      path: '/solutions/sqli1',
      name: 'sqli1-solution',
      component: SQLiLoginBypassSolution,
    },
    {
      path: '/solutions/sqli2',
      name: 'sqli2-solution',
      component: SQLiSecondOrderSolution,
    },
    {
      path: '/solutions/ssrf1',
      name: 'ssrf1-solution',
      component: SSRFWebhookSolution,
    },
    {
      path: '/solutions/ssrf2',
      name: 'ssrf2-solution',
      component: SSRFLocalFileSolution,
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView,
    },
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
  ],

  // Automatically scroll to the top of the page when navigating to a new route
  // Also, the type of savedPosition is very difficult to get right...
  scrollBehavior(
    _to: RouteLocationNormalizedGeneric,
    _from: RouteLocationNormalizedGeneric,
    savedPosition: any,
  ): any | ScrollToOptions {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  },
})

export default router
