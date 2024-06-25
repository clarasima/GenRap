<script setup>
import PublicationItem from '@/components/Publications/PublicationsItem.vue';
const props = defineProps({
    data: Array,
    editIndex: Number,
    from: String,
    selectedPublications: Set
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

</script>

<template>
    <div>
        <div v-for="(item, index) in data" :key="index" class="publication">
            <PublicationItem :item="item" :index="index" :editIndex="props.editIndex" :from="props.from" :selectedPublications="props.selectedPublications"
                @startEdit="startEdit" @saveEdit="saveEdit" @cancelEdit="cancelEdit" @splitPublications="splitPublications" @togglePublicationSelection="togglePublicationSelection"/>
        </div>
    </div>
</template>

<style scoped>

</style>
