<script setup>
const props = defineProps({
  item: Object,
  edited: Boolean,
  fromReport: Boolean,
  source: String,
  new: Boolean,
  confirmed: Boolean
});
</script>

<template>
  <div>
    <div class="title-container">
      <div v-if="props?.new" title="Publication extracted in the last update or that has been split from a match" class="rounded-tag new-tag">New</div>
      <div v-if="props?.confirmed" title="Match Confirmed" class="rounded-tag confirmed-tag"><img class="reports-icon" src="../../assets/twoLinked.svg" /></div>
      <div v-if="props?.edited" title="Publication edited by you!" class="rounded-tag edited-tag"><img class="reports-icon" src="../../assets/check.svg" /></div>

      <h3 style=" padding: 0; margin-bottom: 22px; ">{{ props.item.title }}</h3>
    </div>
    <p>Authors: {{ (typeof props.item.authors === 'string' ||
      !props.item.authors) ? props.item.authors : props.item.authors.join(', ') }}</p>
    <p>Year: {{ props.item.year }}</p>
    <p v-if="props.item?.type">Type: {{ props.item?.type }}</p>
    <p v-if="props.item?.indexed">Indexed: {{ props.item?.indexed }}</p>
    <p v-if="props.item?.category">Category: {{ props.item?.category }}</p>
    <p v-if="props.item?.impactFactor">Impact factor: {{ props.item?.impactFactor }}</p>
    <p>Source: {{props.source}}</p>
    <div v-if="props.item.addedFields">
      <div v-for="(value, key) in props.item.addedFields" :key="key">{{ key }}: {{ value }}</div>
    </div>

  </div>
</template>

<style scoped>
.title-container {
  display: flex;
  align-items: center;
}

.title-container h3 {
  margin-right: 10px;
}

.edited-tag {
  background-color: #14b8a6;
  color: white;
  margin:0;
  margin-right: 15px;
  width: 30px;
}

.new-tag {
  background-color: #f43f5e;
  width: 30px;
  margin-right: 15px;
  font-size: 14px;
}

.confirmed-tag {
  background-color: #3b82f6;
  width: 30px;
  color: white;
  margin:0;
  margin-right: 15px;
}



.match {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
}
</style>
