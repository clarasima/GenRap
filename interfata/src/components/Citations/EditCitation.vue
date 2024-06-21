<script setup>
import { ref } from 'vue';
import { updateCitation } from '@/composables/getCitations';
import { getUserId } from '@/composables/tokenManagement';

const props = defineProps({
  item: Object,
  index: Number,
  type: String,
  citationId: String
});

const emit = defineEmits(['save', 'cancel']);

const defaultPub = {
  category: "",
  indexed: "",
  impactFactor: "",
  conference: ""
};

const editItem = ref({ ...defaultPub });
if (props.type === "Edit") {
  const item = { ...props.item };
  editItem.value = { ...item };
  if (item?.edited) {
    editItem.value = { ...item.edited };
  }
  if (!editItem.value.indexed) {
    editItem.value.indexed = "";
  }
  if (!editItem.value.impactFactor) {
    editItem.value.impactFactor = "";
  }
  if (!editItem.value.conference) {
    editItem.value.conference = "";
  }
}

async function saveEdit() {
  let item = props.item;
  if (!item) {
    item = {}
  }
  const requestBody = {
    "userId": getUserId(),
    "updatedData": editItem.value
  }
  if (props.type === "Edit") {
    requestBody.citationId = props.citationId;
  }
  await updateCitation(requestBody);
  emit('save', editItem.value);
  editItem.value = { ...defaultPub }
}

function cancelEdit() {
  editItem.value = { ...defaultPub }
  emit('cancel');
}

</script>

<template>
  <div>
    <h3>{{ type }} Citation</h3>
    
    <div class="form-row">
      <label for="title">Title</label>
      <input id="title" v-model="editItem.title" placeholder="Title" />
    </div>
    
    <div class="form-row">
      <label for="authors">Authors</label>
      <input id="authors" v-model="editItem.authors" placeholder="Authors" />
    </div>
    
    <div class="form-row">
      <label for="conference">Conference</label>
      <input id="conference" v-model="editItem.conference" placeholder="Conference" />
    </div>
    
    <div class="form-row">
      <label for="year">Year</label>
      <input id="year" v-model="editItem.year" placeholder="Year" />
    </div>
    
    <div class="form-row">
      <label for="indexed">Index</label>
      <select id="indexed" v-model="editItem.indexed">
        <option value="">Select Index</option>
        <option value="BDI">BDI</option>
        <option value="ISI">ISI</option>
        <option value="Unranked">Unranked</option>
      </select>
    </div>
    
    <div class="form-row">
      <label for="impactFactor">Impact Factor</label>
      <input id="impactFactor" type="number" step="0.1" v-model.number="editItem.impactFactor" placeholder="Impact Factor" />
    </div>

    <button @click="saveEdit">Save citation</button>
    <button @click="cancelEdit">Cancel</button>
  </div>
</template>
<style scoped>
.form-row {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.form-row label {
  width: 150px;
  margin-right: 10px;
  font-weight: bold;
}

.form-row input,
.form-row select {
  flex: 1;
  padding: 5px;
  font-size: 14px;
}
</style>
