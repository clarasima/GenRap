<script setup>
import PublicationItem from '@/components/Publications/PublicationsItem.vue';
// import { ref } from 'vue';
// import VueJsonPretty from "vue-json-pretty";
const props = defineProps({
    data: Array,
    editIndex: Number,
    from: String,
    selectedPublications: Array
});

const emit = defineEmits(['save', 'cancel', 'update:editIndex', 'update:editItem', 'splitPublications', 'startEdit', 'togglePublicationSelection']);


function startEdit(index) {
    emit('startEdit', index);
}

function saveEdit(index, item) {
    emit('save', index, item);
}
function splitPublications(index) {
    emit('splitPublications', index);
}
function togglePublicationSelection(pubId) {
    emit('togglePublicationSelection', pubId)
}

function cancelEdit() {
    emit('cancel');
}
// let ind =0

// function getIndex(){
//     ind++;
//     return ind;

// }

</script>

<template>
     <!-- <VueJsonPretty :data="data" /> -->
    <div>
        <div v-for="(item, index) in data" :key="index" class="publication">
            <!-- <p v-if="item.scholar"> {{ getIndex() }}</p> -->
            <PublicationItem :item="item" :index="index" :editIndex="props.editIndex" :from="props.from" :selectedPublications="props.selectedPublications"
                @startEdit="startEdit" @saveEdit="saveEdit" @cancelEdit="cancelEdit" @splitPublications="splitPublications" @togglePublicationSelection="togglePublicationSelection"/>
        </div>
    </div>
</template>

<style scoped>
.publication {
    border: 1px solid #ccc;
    padding: 16px;
    margin-bottom: 16px;
}
</style>
