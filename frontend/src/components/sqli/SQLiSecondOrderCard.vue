<template>
  <div class="card">
    <router-link to="/vulnerabilities/sqli2">
      <div class="card-banner"></div>
      <div class="card-content">
        <div class="card-body">
          <div class="card-title">SQLi: second order</div>
          <p class="card-text">
            Sometimes the injection doesn't happen right away
          </p>
        </div>
        <div class="card-footer">
          <p class="challenge-button">
            Start challenge #2
          </p>
        </div>
      </div>
    </router-link>
  </div>
</template>

<style scoped>
.card {
  position: relative;
  width: 18rem; /* 72 * 0.25 = 18rem */
  text-align: center;
  border-radius: 0.75rem;
  overflow: hidden;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.card:hover {
  transform: translateY(-0.125rem);
}

.card-banner {
  height: 15rem;
  background-color: rgb(67, 56, 202); /* indigo-700 */
}

.card-content {
  height: 12rem;
  position: relative;
}

.card-body {
  padding: 1rem 0.75rem;
}

.card-title {
  font-weight: 700;
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
}

.card-text {
  color: rgb(55, 65, 81);
  font-size: 1rem;
}

.card-footer {
  position: absolute;
  bottom: 1rem;
  left: 0.5rem;
  right: 0.5rem;
}

.challenge-button {
  display: inline-block;
  text-transform: uppercase;
  background-color: rgb(229, 231, 235);
  border-radius: 9999px;
  padding: 0.25rem 0.75rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: rgb(55, 65, 81);
}

.card:hover .challenge-button {
  text-decoration: underline;
}
</style>
