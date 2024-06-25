<script setup>
import { ref, onMounted } from 'vue';
import { useUser } from '@/composables/getUser';
import { useRouter } from 'vue-router'
const router = useRouter()
const data = ref([]);
const isPendingRefresh = ref(false);

onMounted(async () => {
  await loadData();
});

async function loadData() {
  isPendingRefresh.value = true;
  const res = await useUser("getPublications");
  isPendingRefresh.value = false;
  data.value = res.filter(item => item.match !== false && item?.scholar?.citations?.href);
}


const goToCitationsView = (id) => {
  router.push({
    name: 'citations',
    params: { id },
  });
}

</script>

<template>
  <div v-if="isPendingRefresh"><div class="spinner"></div> Pending </div>
  <div v-else>
    <div v-for="(item, index) in data" :key="index" class="publication">
      <h3 style="margin-top:10px">
        {{ item.scholar.title }}
      </h3>
      <a :href="$router.resolve({ name: 'citations', params: { id: item._id } }).href" target="_blank">
        <button v-if="item?.scholar?.citations?.href" @click.prevent="goToCitationsView(item._id)">
          See citations {{ item?.scholar?.citations?.nr }}
        </button>
      </a>
    </div>
  </div>
</template>

<style scoped>

</style>