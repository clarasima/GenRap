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
    <div v-if="props?.edited && !props.fromReport" class="rounded-tag"
      style="background-color: green; width: 70px">Edited ✓</div>
    <h3>{{ props.item.title }}</h3>
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
    <div v-if="props?.new" class="rounded-tag" style="background-color: red; width: 40px">New!</div>
    <!-- {{ props }} -->
    <div v-if="props?.confirmed" style="background-color: purple; width: 150px" class="rounded-tag">
          Confirmed match.</div>
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
