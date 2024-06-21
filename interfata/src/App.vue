<script setup>
import { RouterView } from 'vue-router'
import Navbar from './components/NavbarComp.vue';

</script>

<template>
  <Navbar/>
  <div class="content">
    <RouterView />
  </div>

</template>

<style>

.content {
  margin: 0 auto;
  max-width: 1200;
  padding: 0 20px;
  /* background-color: red; */
}
</style>
