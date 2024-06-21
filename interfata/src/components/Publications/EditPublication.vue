<script setup>
import { ref } from 'vue';
import { updatePublication } from '@/composables/getUser';
import { getUserId } from '@/composables/tokenManagement';
import AddField from '@/components/Publications/AddField.vue';

const props = defineProps({
  item: Object,
  index: Number,
  type: String
});

const emit = defineEmits(['save', 'cancel']);

const defaultPub = {
  category: "",
  indexed: "",
  type: "",
  impactFactor: ""
};

const editItem = ref({ ...defaultPub });
if (props.type === "Edit") {
  const item = { ...props.item };
  if (item?.edited) {
    editItem.value = { ...item.edited };
  }
  else if (item?.best) {
    editItem.value = { ...item.best };
  }
  else if (item?.scholar) {
    editItem.value = { ...item.scholar };
  } else {
    editItem.value = { ...item.dblp };
  }
  if (!editItem.value.category) {
    editItem.value.category = "";
  }
  if (!editItem.value.indexed) {
    editItem.value.indexed = "";
  }
  if (!editItem.value.type) {
    editItem.value.type = "";
  }
  if (!editItem.value.impactFactor) {
    editItem.value.impactFactor = "";
  }
}

async function saveEdit() {
  let item = props.item;
  if(!item){
    item = {}
  }
  // if something changed I delete old data, that is not possible after the latest changes
  if (editItem.value.type === "journal") {
    editItem.value.category = "";
  }
  if (editItem.value.indexed === "BDI" || editItem.value.type === "conference") {
    editItem.value.impactFactor = "";
  }

  item.edited = { ...editItem.value };
  const requestBody = {
    "userId": getUserId(),
    "updatedData": item
  }
  if (props.type === "Edit") {
    requestBody.publicationId = item._id;
  }
  await updatePublication(requestBody);
  if (props.type === "Edit") {
    emit('save', props.index, item);
  } else {
    emit('save', item);
  }
  editItem.value = { ...defaultPub }
}

function cancelEdit() {
  editItem.value = { ...defaultPub }
  emit('cancel');
}

</script>

<template>
   <div>
    <h3>{{ type }} Publication</h3>
    <div class="form-row">
      <label for="title">Title</label>
      <input id="title" v-model="editItem.title" placeholder="Title" />
    </div>
    <div class="form-row">
      <label for="authors">Authors</label>
      <input id="authors" v-model="editItem.authors" placeholder="Authors" />
    </div>
    <div class="form-row">
      <label for="year">Year</label>
      <input id="year" v-model="editItem.year" placeholder="Year" />
    </div>
    <div class="form-row">
      <label for="type">Type</label>
      <select id="type" v-model="editItem.type">
        <option value="">Select Type</option>
        <option value="conference">Conference</option>
        <option value="journal">Journal</option>
        <option value="workshop">Workshop</option>
        <option value="book">Book</option>
      </select>
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
    <div v-if="editItem.type === 'conference' || editItem.type === 'workshop'" class="form-row">
      <label for="category">Category</label>
      <select id="category" v-model="editItem.category">
        <option value="">Select Category</option>
        <option value="A">A</option>
        <option value="B">B</option>
        <option value="C">C</option>
        <option value="D">D</option>
      </select>
    </div>
    <div v-if="(editItem.indexed === 'ISI' && editItem.type === 'journal') || editItem.type === 'workshop'" class="form-row">
      <label for="impactFactor">Impact Factor</label>
      <input id="impactFactor" type="number" step="0.1" v-model.number="editItem.impactFactor" placeholder="Impact Factor" />
    </div>

    <AddField :item="editItem" />
    <button @click="saveEdit">Save publication</button>
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
