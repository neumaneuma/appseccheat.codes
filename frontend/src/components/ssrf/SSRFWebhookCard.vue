<template>
  <div class="relative group text-center w-72 rounded-xl overflow-hidden shadow-xl transform transition hover:-translate-y-0.5">
    <router-link to="/vulnerabilities/ssrf1">
      <div class="bg-indigo-700 h-60"></div>
      <div class="h-48">
        <div class="px-3 pt-4">
          <div class="font-bold text-xl mb-2">SSRF: bypass webhook</div>
          <p class="text-gray-700 text-base">
            Internal APIs are just external APIs that are a bit harder to access
          </p>
        </div>
        <div class="absolute bottom-4 inset-x-2">
          <p class="group-hover:underline uppercase inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700">
            Start challenge #3
          </p>
        </div>
      </div>
    </router-link>
  </div>
</template>
