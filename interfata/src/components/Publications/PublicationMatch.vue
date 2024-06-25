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
const emit = defineEmits(['splitPublications']);

function confirmMatch(isMatch) {
  const item = props.item;
  if (isMatch) {
    item.confirmed = true;
  } else {
    splitPublication(item._id);
    emit('splitPublications');
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
    <div v-if="props.item?.new" title="Publication extracted in the last update or that has been split from a match" style="margin-bottom: 10px;" class="rounded-tag new-tag">
      New</div>

  <div class="match">
    <div class="publication">
      <h3 style="margin-top: 10px;">{{ props.item.dblp.title }}</h3>
      <p>Authors: {{ props.item.dblp.authors.join(', ') }}</p>
      <p>Year: {{ props.item.dblp.year }}</p>
      <p>Source: DBLP</p>
    </div>
    <div  class="publication">
      <h3 style="margin-top: 10px;">{{ props.item.scholar.title }}</h3>
      <p>Authors: {{ props.item.scholar.authors.join(', ') }}</p>
      <p>Year: {{ props.item.scholar.year }}</p>
      <p>Source: Scholar</p>
    </div>
  </div>
  <div style="display: flex;justify-content: space-around;margin-bottom: 16px;width: 100%" v-if="!props.item.confirmed">
    <button @click="confirmMatch(true)">Yes, this is a match</button>
    <button @click="confirmMatch(false)">No, separate publications</button>
  </div>
  <div v-else style="display: flex;justify-content: space-around;margin-bottom: 16px;width: 100%">
    <button @click="selectSource('dblp')">Keep DBLP</button>
    <button @click="selectSource('scholar')">Keep Scholar</button>
  </div>
</template>

<style scoped>
.match {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
  width: 100%;
}

.publication {
  flex: 1;
  margin: 0 10px;
  padding: 16px;
  border: 1px solid #ddd;
  border-radius: 6px;
  background-color: #f9f9f9;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.new-tag {
  background-color: #f43f5e;
  margin-right: 15px;
  width: 40px;
  font-size: 14px;
  padding: 3px 6px;
  border-radius: 6px;
  color: white;
  text-align: center;
}
</style>
