<script setup>
import { useUser, error, isPending, getUserValue } from '@/composables/getUser';
import { ref, onMounted, watchEffect } from 'vue';

onMounted(async () => {
  await useUser("getUser");
});

const user = ref(null);

watchEffect(() => {
  user.value = getUserValue();
});
</script>

<template>
  <div v-if="error" class="error">{{ error }}</div>
  <div v-if="!isPending && user" class="user-card">
    <h2>User Information</h2>
    <div class="user-detail">
      <p class="label">Name:</p>
      <p class="value">{{ user.name }}</p>
    </div>
    <div class="user-detail">
      <p class="label">Username:</p>
      <p class="value">{{ user.username }}</p>
    </div>
    <div class="user-detail">
      <p class="label">Dblp Profile:</p>
      <p class="value">
        <a :href="user.dblp_profile" target="_blank">{{ user.dblp_profile }}</a>
      </p>
    </div>
    <div class="user-detail">
      <p class="label">Scholar Profile:</p>
      <p class="value">
        <a :href="user.scholar_profile" target="_blank">{{ user.scholar_profile }}</a>
      </p>
    </div>
  </div>
  <div v-else>  <div v-if="isPendingRefresh"><div class="spinner"></div> Loading</div></div>
</template>

<style scoped>
.error {
  color: red;
  font-weight: bold;
  margin: 10px 0;
}

.user-card {
  background: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  max-width: 50%; 
  margin: 20px auto;
  word-wrap: break-word;
}

.user-card h2 {
  margin-bottom: 20px;
  text-align: center;
}

.user-detail {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.user-detail .label {
  font-weight: bold;
  margin-right: 10px;
}

.user-detail .value {
  flex: 1;
  text-align: left;
  word-break: break-all;
}

.user-detail .value a {
  color: blue;
  text-decoration: underline;
}
</style>
