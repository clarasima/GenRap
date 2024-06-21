<script setup>
import useSignup from '../../composables/useSignup.js';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const { error, signup, isPending } = useSignup();

const name = ref('');
const scholar = ref('');
const dblp = ref('');
const username = ref('');
const password = ref('');
const success = ref(false);
const seconds = ref(2);

const scholarMissing = ref(false);
const dblpMissing = ref(false);

const router = useRouter();
function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms))
}

const handleSubmit = async () => {
    const scholarValue = scholarMissing.value ? false : scholar.value;
    const dblpValue = dblpMissing.value ? false : dblp.value;

    await signup(username.value, password.value, name.value, dblpValue, scholarValue);
    if (!error.value) {
        success.value = true;
        for (let i = 2; i >= 1; i--) {
            await sleep(1000);
            seconds.value = seconds.value - 1;
        }
        router.push({ name: 'login' });
    }
}
const handleClick = () => {
    router.push({ name: 'login' });
}
</script>

<template>
    <form v-if="!success" @submit.prevent="handleSubmit">
        <h3>Sign up</h3>
        <input type="text" placeholder="Name" v-model="name">
        <input type="text" placeholder="Username" v-model="username">
        <input type="password" placeholder="Password" v-model="password">

        <div class="checkbox-container">
            <input type="checkbox" id="missingScholar" v-model="scholarMissing">
            <label for="missingScholar">I don't have a Scholar profile</label>
        </div>
        <div v-if="!scholarMissing">
            <input type="url" placeholder="Scholar profile URL" v-model="scholar">
        </div>

        <div class="checkbox-container">
            <input type="checkbox" id="missingDblp" v-model="dblpMissing">
            <label for="missingDblp">I don't have a DBLP profile</label>
        </div>
        <div v-if="!dblpMissing">
            <input type="url" placeholder="DBLP profile URL" v-model="dblp">
        </div>

        <div v-if="error" class="error"> {{ error }}</div>
        <button v-if="!isPending" style="display:block">Sign up</button>
        <button v-else disabled>Loading</button>
    </form>

    <div v-else>
        <h1>You signed up successfully, {{ name }}. You will be redirected to Login Page in {{ seconds }} seconds</h1>
        <button @click="handleClick">Go to Login now.</button>
    </div>
</template>

<style scoped>
.checkbox-container {
  display: inline-flex;
  align-items: center;
  margin-bottom: 8px; /* Adds some space below each checkbox-container for better spacing */
}

.checkbox-container input[type="checkbox"] {
  transform: scale(1.2); /* Optionally scale the checkbox for better visibility */
}

.checkbox-container label {
  margin: 0; /* Remove any default margin from the label */
}

.error {
  color: red;
}
</style>