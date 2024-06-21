<script setup>
import { getToken } from '@/composables/tokenManagement';
import { useUser, getUserName } from '@/composables/getUser';
import { ref, onMounted } from "vue";
const { token } = getToken();
const name = ref("")
const isPending = ref(false)

onMounted(async () => {
  isPending.value = true;
  await useUser("getUser");
  name.value = getUserName();
  isPending.value = false;
});

</script>

<template>
  <div v-if="isPending">
    <div class="spinner"></div> Pending
  </div>
  <h1 v-else-if="token">Welcome back to GenRap, {{ name }}!</h1>
  <h1 v-else>Welcome to GenRap!</h1>
</template>

<style scoped>
.image-container {
  width: 300px;
  /* Set the desired width */
  height: auto;
  /* Set the desired height to crop vertically */
  overflow: hidden;
  /* Hide the overflow to crop the image */
  position: relative;
  /* Position context for the image */
}

.cropped-image {
  width: 100%;
  /* Ensures the image fills the container width */
  height: auto;
  /* Maintains the aspect ratio */
  object-fit: cover;
  /* Scale the image to cover the container */
  object-position: center;
  /* Center the image within the container */
  clip-path: inset(17% 0 17% 0);
  /* Clip 20% from top and bottom, showing the middle 60% */
}
</style>
