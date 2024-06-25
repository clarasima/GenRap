<script setup>
const props = defineProps({
  citation: Object,
  selectedCitations: Array,
  index: Number,
  reportMode: Boolean,
  citationId: String
});

const emit = defineEmits(['startEdit', 'toggleCitationSelection']);

function startEdit() {
  emit('startEdit', props.index);
}

// EDIT
function showEdit() {
  return true;
}

// Selection Report

function toggleCitationSelection() {
  const citId = props.citationId;
  emit('toggleCitationSelection', citId)
}

</script>

<template>
  <div style="position: relative">
    <!-- Checkbox Report -->
    <div v-if="reportMode" class="checkbox-container" >
      <input type="checkbox" :checked="props.selectedCitations.has(props.citationId)" @change="toggleCitationSelection">
    </div>
    
    <!-- Publication -->
    <h3>{{ citation.title }}</h3>
    <p><strong>Link: </strong>
      <a :href="citation.urlCit"  target="_blank" style="  color: var(--teal--500);text-decoration: underline;">
        {{
          citation.urlCit
        }}
      </a>
    </p>
    <p><strong>Year:</strong> {{ citation.year }}</p>
    <p><strong>Authors:</strong> {{ citation.authors }}</p>
    <p><strong>Conference:</strong> {{ citation.conference }}</p>
    <p v-if="citation.indexed"><strong>Index:</strong> {{ citation.indexed }}</p>
    <p v-if="citation.impactFactor"><strong>Impact Factor:</strong> {{ citation.impactFactor }}</p>
    <button v-if="showEdit()" @click="startEdit">Edit</button>
  </div>
</template>
