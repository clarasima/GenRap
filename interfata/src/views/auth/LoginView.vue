<script setup>
import useLogin from '@/composables/useLogin.js';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const { error, login, isPending } = useLogin();

const username = ref('');
const password = ref('');

const router = useRouter();

const handleSubmit = async () => {
    await login(username.value, password.value);
    if (!error.value) {
        router.push({ name: 'home' }); 
    }
}

</script>

<template>
    <form @submit.prevent="handleSubmit">
        <h3>Log in</h3>
        <input type="text" placeholder="Username" v-model="username">
        <input type="password" placeholder="Password" v-model="password">
        <div v-if="error" class="error"> {{ error }}</div>
        <button v-if="!isPending">Log in</button>
        <button v-else disabled>Loading</button>

    </form>
</template>
