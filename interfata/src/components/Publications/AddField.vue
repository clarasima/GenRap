<script setup>
import { ref } from 'vue';
const props = defineProps({
  item: Object
});

// const emit = defineEmits(['save', 'cancel']);

const editItem = ref(props.item);

const addFieldMode = ref(false);
const newFieldName = ref('');
const newFieldValue = ref('');

const toggleAddField = () => {
  addFieldMode.value = !addFieldMode.value;
  newFieldName.value = '';
  newFieldValue.value = '';
};

const addNewField = () => {
  if (newFieldName.value && newFieldValue.value) {
    if (!editItem.value["addedFields"]) {
      editItem.value["addedFields"] = {}
    }
    editItem.value["addedFields"][newFieldName.value] = newFieldValue.value;
    toggleAddField();
  } else {
    alert('Please provide both field name and value');
  }
};
const deleteField = (key) => {
  delete editItem.value["addedFields"][key];
};

</script>

<template>
  <!-- ADD FIELD -->
  <div v-if="editItem.addedFields">
    <div v-for="(value, key) in editItem.addedFields" :key="key">
      {{ key }}:
      <input v-model="editItem.addedFields[key]" :placeholder="value" />
      <button @click="deleteField(key)">Delete field {{ key }}</button>
    </div>
  </div>

  <p>
<button @click="toggleAddField">{{ addFieldMode ? 'Cancel Add Field' : 'Add Field' }}</button>
</p>

  <div v-if="addFieldMode">
    <input v-model="newFieldName" placeholder="Field Name" />
    <input v-model="newFieldValue" placeholder="Field Value" />
    <button @click="addNewField">Confirm Adding Field</button>
  </div>
</template>
