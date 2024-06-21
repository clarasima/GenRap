<script setup>
import useLogout from '@/composables/useLogout';
import { getToken } from '@/composables/tokenManagement';
import { useRouter } from 'vue-router';

const { token } = getToken();
const { logout } = useLogout();
const router = useRouter();

async function handleClick() {
  await logout();
  router.push({ name: 'login' })
}
</script>

<template>
  <div class="navbar">
    <nav>
      <img class="reports-icon" src="../assets/reports.svg" alt="Reports" />
      <h1>
        <router-link :to="{ name: 'home' }">GenRap</router-link>
      </h1>
      <div class="links">
        <div v-if="token">
          <router-link class="btn" :to="{ name: 'myPublications' }">My publications</router-link>
          <router-link class="btn" :to="{ name: 'createReport' }">Create publications report</router-link>
          <router-link class="btn" :to="{ name: 'pubCitations' }">My citations</router-link>
          <router-link class="btn" :to="{ name: 'userProfile' }">My profile</router-link>
          <button @click="handleClick">Logout</button>
        </div>
        <div v-else>
          <router-link class="btn" :to="{ name: 'login' }">Login</router-link>
          <router-link class="btn" :to="{ name: 'signup' }">Sign Up</router-link>
        </div>
      </div>
    </nav>
  </div>

</template>

<style scoped>
.reports-icon {
  max-height: 60px;
}

.navbar {
  padding: 16px 10px;
  margin-bottom: 60px;
  background: white;
}

nav {
  display: flex;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}

nav h1 {
  margin-left: 20px;
}

/* putthing everything in the flex to the right of the page */
nav .links {
  margin-left: auto;
}


nav .links a,
button {
  margin-left: 16px;
  font-size: 14px;
}
</style>
