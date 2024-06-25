<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import PublicationList from '@/components/Publications/PublicationsList.vue';
import { useUser, error } from '@/composables/getUser';
import EditPublication from '@/components/Publications/EditPublication.vue';

// import VueJsonPretty from "vue-json-pretty";
const isAddPubMode = ref(false);
const data = ref([]);
const editIndex = ref(null);
const isPendingRefresh = ref(false);
let scholarCount = ref(0);
let dblpCount = ref(0);

// get data
onMounted(async () => {
  await loadData();
  // Initialize counters
  // Iterate through the array of objects
});

onUnmounted(() => {
  data.value = [];
});

function updateCounters(){
  scholarCount.value = 0;
  dblpCount.value = 0;
  data.value.map(obj => {
    if ('scholar' in obj && obj.match != false) {
      scholarCount.value++;
    }
    if ('dblp' in obj) {
      dblpCount.value++;
    }
  });
}

async function loadData() {
  isPendingRefresh.value = true;
  const res = await useUser("getPublications");
  isPendingRefresh.value = false;
  data.value = res.filter(item => item.match !== false);
  updateCounters();
}


async function getData() {
  isPendingRefresh.value = true;
  await useUser("refreshReportData");
  await loadData();
  isPendingRefresh.value = false;
}

// EDIT
function startEdit(index) {
  editIndex.value = index;
}

function saveEdit(index, item) {
  data.value[index] = item;
  editIndex.value = null;
}

function cancelEdit() {
  editIndex.value = null;
}

// ADD
function startAdd() {
  isAddPubMode.value = true;
}

function saveAdd(item) {
  isAddPubMode.value = false;  // add button appears again, component disapears
  data.value.unshift(item); // add the item in the begining
}

function cancelAdd() {
  isAddPubMode.value = false; // add button appears again, component disapears
}


// SPLIT
function splitPublications(index) { // delete old publication and add 2 new ones
  const item = data.value[index];
  data.value.splice(index, 1);
  data.value.splice(index, 0, { dblp: item.dblp });
  data.value.splice(index + 1, 0, { scholar: item.scholar });
}



</script>

<template>
  <div>
    <div v-if="!isPendingRefresh" class="data-summary">
    <div class="card">
      <h4>Total Publications</h4>
      <p class="count">{{ data.length }}</p>
    </div>
    <div class="card">
      <h4>Scholar</h4>
      <p class="count">{{ scholarCount }}</p>
    </div>
    <div class="card">
      <h4>DBLP</h4>
      <p class="count">{{ dblpCount }}</p>
    </div>
  </div>
    <!-- REFRESH DATA -->
    <div v-if="isPendingRefresh"><div class="spinner"></div>Refreshing</div>
    <button v-else @click="getData">Update data from dblp and scholar</button>
    <div v-if="error" style="color:red">{{ error }}</div>
    <!-- <div v-if="error === false" style="color:#14b8a6">The data has been refreshed successfully.</div> -->
    <!-- <p v-if="!isPendingRefresh">We were able to extract data for {{ data.length }} publications. From scholar there are {{ scholarCount }} and from
      dblp there are {{ dblpCount }}.</p> -->

    <!-- ADD PUBLICATION -->
    <button v-if="!isAddPubMode" @click="startAdd"> Add publication</button>
    <div v-if="isAddPubMode">
      <EditPublication @save="saveAdd" @cancel="cancelAdd" type="Add" />
    </div>
    <PublicationList :data="data" :editIndex="editIndex" from="pubs" @save="saveEdit" @cancel="cancelEdit"
      @splitPublications="splitPublications" @startEdit="startEdit" />
  </div>
</template>

<style scoped>
.data-summary {
  display: flex;
  justify-content: space-around;
  margin-bottom: 20px;
}

.card {
  background-color: #f9f9f9;
  padding: 10px;
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  text-align: center;
  width: 150px;
}

.card h3 {
  margin: 0 0 5px;
  font-size: 14px;
  color: #333;
}

.card .count {
  font-size: 18px;
  font-weight: bold;
  color: #14b8a6; /* Adjust this color to match your theme */
}</style>