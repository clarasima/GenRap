<script setup>
import EditPublication from '@/components/Publications/EditPublication.vue';
import PublicationBasic from '@/components/Publications/PublicationBasic.vue';
import PublicationMatch from '@/components/Publications/PublicationMatch.vue';
import { useRouter } from 'vue-router'
import { computed } from 'vue';
const router = useRouter()
const props = defineProps({
  item: Object,
  index: Number,
  editIndex: Number,
  from: String,
  selectedPublications: Array
});

const emit = defineEmits(['startEdit', 'saveEdit', 'cancelEdit', 'loadData', 'togglePublicationSelection', 'splitPublications']);

function startEdit() {
  emit('startEdit', props.index);
}
function splitPublications() {
  emit('splitPublications', props.index);
}


// EDIT
function saveEdit(index, item) {
  emit('saveEdit', index, item);
}

function cancelEdit() {
  emit('cancelEdit');
}
const fromReport = (props.from === 'report');
function showEdit() {
  const initial = !props.item.match || (props.item.match && (props.item?.best || props.item?.edited));
  return !fromReport && initial;
}

// Selection Report

function togglePublicationSelection() {
  const pubId = props.item._id;
  emit('togglePublicationSelection', pubId)
}

const source = computed(() => {
  return (props.item?.match) ? props.item.chosen : ((props.item?.dblp) ? 'dblp' : ((props.item?.scholar) ?
    'scholar' : 'interface'));
});


//Citations

const goToCitationsView = (id) => {
  router.push({
    name: 'citations',
    params: { id },
  });
}

</script>

<template>
  <div>
    <div v-if="props.editIndex === props.index">
      <EditPublication :item="props.item" :index="props.index" @save="saveEdit" @cancel="cancelEdit" type="Edit" />
    </div>
    <div v-else>
      <!-- Checkbox Report -->
      <div v-if="fromReport && props.item?.edited">
        <input type="checkbox" :checked="props.selectedPublications.has(props.item._id)"
          @change="togglePublicationSelection">
      </div>
      <!-- Publication -->
      <PublicationMatch v-if="props.item.match && !props.item.best && !props.item.edited" :item="props.item" @splitPublications="splitPublications" />
      <PublicationBasic v-else-if="props.item?.edited" :item="props.item.edited" :from-report="fromReport"
        :edited="true" :source="source" />
      <PublicationBasic v-else-if="props.item.scholar && !props.item.match" :item="props.item.scholar" :edited="false"
        source="Scholar" :new="props.item?.new" />
      <PublicationBasic v-else-if="props.item.dblp && !props.item.match" :item="props.item.dblp" :edited="false"
        source="DBLP" :new="props.item?.new" />
      <PublicationBasic v-else-if="props.item.best" :item="props.item.best" :edited="false" :source="props.item.chosen"
        :confirmed="props.item?.confirmed" />
      <div v-else>
        {{ props.item }}
      </div>

      <button v-if="showEdit()" @click="startEdit">Edit</button>

      <!-- Citations -->
      <p v-if="props.item?.scholar?.citations?.href" style="margin-top:10px">
        <button  @click="goToCitationsView(props.item._id)">See {{
          props.item?.scholar?.citations?.nr }} citations</button>
        <!-- <a v-if="props.item?.scholar?.citations?.href" style="color:blue"
          :href="props.item?.scholar?.citations?.href">{{
            item?.scholar?.citations?.href }}</a> -->
      </p>
    </div>
  </div>
</template>
