<script setup>
import useLogin from '@/composables/useLogin.js';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const { error, login, isPending } = useLogin();

const username = ref('');
const password = ref('');
const passwordVisible = ref(false);

const router = useRouter();

const handleSubmit = async () => {
    await login(username.value, password.value);
    if (!error.value) {
        router.push({ name: 'home' }); 
    }
}

const togglePasswordVisibility = () => {
    passwordVisible.value = !passwordVisible.value;
}
</script>

<template>
    <form @submit.prevent="handleSubmit">
        <h3>Log in</h3>
        <input type="text" placeholder="Username" v-model="username">
        
        <div class="password-container">
            <input :type="passwordVisible ? 'text' : 'password'" placeholder="Password" v-model="password">
            <button type="button" @click="togglePasswordVisibility">
                <img  v-if="passwordVisible" class="reports-icon" src="../../assets/eyeClosed.svg" />
                <img v-else class="reports-icon" src="../../assets/eyeOpen.svg" />
            </button>
        </div>

        <div v-if="error" class="error"> {{ error }}</div>
        <button v-if="!isPending">Log in</button>
        <button v-else disabled>Loading</button>
    </form>
</template>

<style scoped>
.error {
  color: red;
}

.password-container {
  display: flex;
  align-items: center;
}

.password-container button {
  margin-left: 8px;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 1.2em;
}

.password-container button:hover svg {
  fill: #007bff; /* Change color on hover */
}
</style>
