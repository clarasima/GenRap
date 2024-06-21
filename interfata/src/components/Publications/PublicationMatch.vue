<script setup>
import { updatePublication, splitPublication } from '@/composables/getUser';
const props = defineProps({
  item: Object,
  edited: Boolean,
  fromReport: Boolean,
  source: String,
  new: Boolean,
  confirmed: Boolean
});
const emit = defineEmits([ 'splitPublications']);


function confirmMatch(isMatch) {
  const item = props.item;
  if (isMatch) {
    item.confirmed = true;
  } else {
    splitPublication(item._id);
    emit('splitPublications')
  }
}

function selectSource(source) {
  const item = props.item;
  if (source === 'dblp') {
    item.chosen = 'dblp';
    item.best = item.dblp;
  } else {
    item.chosen = 'scholar';
    item.best = item.scholar;
  }
  const requestBody = { "userId": item.user_id, "publicationId": item._id, "updatedData": item };
  updatePublication(requestBody);
}

</script>

<template>
  <div class="match">
    <div v-if="props.item?.new" style="background-color: red;  width: 40px;" class="rounded-tag">
      New!</div>
    <div class="publication">
      <h3>{{ props.item.dblp.title }}</h3>
      <p>Authors: {{ props.item.dblp.authors.join(', ') }}</p>
      <p>Year: {{ props.item.dblp.year }}</p>
      <p>Source: DBLP</p>
    </div>
    <div class="publication">
      <h3>{{ props.item.scholar.title }}</h3>
      <p>Authors: {{ props.item.scholar.authors.join(', ') }}</p>
      <p>Year: {{ props.item.scholar.year }}</p>
      <p>Source: Scholar</p>
    </div>
    <div v-if="!props.item.confirmed">
      <button @click="confirmMatch(true)">Yes, this is a match</button>
      <button @click="confirmMatch(false)">No, separate publications</button>
    </div>
    <div v-else>
      <button @click="selectSource('dblp')">Keep DBLP</button>
      <button @click="selectSource('scholar')">Keep Scholar</button>
    </div>
  </div>
</template>

<style scoped>
.publication {
  border: 1px solid #ccc;
  padding: 16px;
  margin-bottom: 16px;
}

.match {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
}
</style>
