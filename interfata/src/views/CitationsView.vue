<script setup>
import { ref, onMounted } from 'vue';
import { error, isPending, fetchCitations, refreshCitations, getPublicationScholar } from '@/composables/getCitations';
import CitationItem from '@/components/Citations/CitationItem.vue';
import EditCitation from '@/components/Citations/EditCitation.vue';
import { getCSV } from '@/composables/getUser';
const props = defineProps({
  id: String
});

const citations = ref([]);
const allCitations = ref([]);
const title = ref("");
const publication = ref({});
const linkHref = ref("");
const expectedNumber = ref(0);
const editIndex = ref(null);
const reportMode = ref(false);
const selectedCitations = ref(new Set());
const defaultFields = ['title', 'authors', 'year', 'conference', 'indexed', 'impactFactor']
const selectedFields = ref([...defaultFields]);
const newField = ref('');

async function refreshCitationsLocal() {
  await refreshCitations(props.id);
  const result = await fetchCitations(props.id);
  citations.value = [...result];
  allCitations.value = [...result];
}

onMounted(async () => {
  publication.value = await getPublicationScholar(props.id);
  expectedNumber.value = publication.value?.citations?.nr;
  title.value = publication.value.title;
  linkHref.value = publication.value.citations?.href;
  const result = await fetchCitations(props.id);
  citations.value = [...result];
  allCitations.value = [...result];
});

function startEdit(index) {
  editIndex.value = index;
}

function saveEdit(citation) {
  citations.value[editIndex.value].edited = citation;
  editIndex.value = null;
}

function cancelEdit() {
  editIndex.value = null;
}

function toggleReportMode() {
  reportMode.value = !reportMode.value;
  if (reportMode.value) {
    citations.value = citations.value.filter(item => item.edited);
  } else {
    citations.value = allCitations.value;
  }
}

function toggleCitationSelection(citationId) {
  if (selectedCitations.value.has(citationId)) {
    selectedCitations.value.delete(citationId);
  } else {
    selectedCitations.value.add(citationId);
  }
}

async function getSelectedCitations(format, name) {
  const selected = Array.from(selectedCitations.value);
  try {
    const urlReq = `http://localhost:5000/generate`;
    const payload = {
      ids: selected,
      type: 'citations',
      fields: selectedFields.value,
      format
    };
    const response = await getCSV(urlReq, payload);
    const url = window.URL.createObjectURL(new Blob([response]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', name);
    document.body.appendChild(link);
    link.click();
  } catch (error) {
    console.error(`Error downloading ${name}:`, error);
  }
}

function selectAllCitations() {
  citations.value.forEach(citation => {
    selectedCitations.value.add(citation._id);
  });
}
function deselectAllCitations() {
  selectedCitations.value.clear();
}

function addField() {
  if (newField.value && !selectedFields.value.includes(newField.value)) {
    selectedFields.value.push(newField.value);
    newField.value = '';
  }
}

function removeField(field) {
  const index = selectedFields.value.indexOf(field);
  if (index > -1) {
    selectedFields.value.splice(index, 1);
  }
}
</script>

<template>

  <div>
    <h2 style=" text-align: center;">{{ title }}</h2>
    <div>
      <div v-if="!isPendingRefresh" class="data-summary">
        <div class="card">
          <h4>Total Citations</h4>
          <p class="count">{{ citations.length }}</p>
        </div>
        <div class="card">
          <h4>Expected Citations</h4>
          <p class="count">{{ expectedNumber }}</p>
        </div>
      </div>
    </div>
    <p>
      <a :href="linkHref" target="_blank" style="color:var(--teal--500); text-decoration: underline;">
        See Google Scholar citations page
      </a>
    </p>
    <!-- REFRESH DATA -->
    <div v-if="isPending">
      <div class="spinner"></div>
      Refreshing
    </div>
    <button v-else @click="refreshCitationsLocal">Update citations</button>
    <div v-if="error" style="color:red">{{ error }}</div>

    <!-- Report -->
    <button v-if="!reportMode" @click="toggleReportMode">Make Citation Report</button>
    <button v-else @click="toggleReportMode">Cancel Making Citation Report</button>
    <div v-if="reportMode === true">
      <button @click="selectAllCitations">Select All</button>
      <button @click="deselectAllCitations">Deselect All</button>
      <div>
        <input v-model="newField" placeholder="New Field" class="field-input" />
        <button @click="addField" class="btn">Add Field</button>
      </div>
      <ul class="field-list">
        <li v-for="field in selectedFields" :key="field" >
        <div class="field-item">{{ field }}</div>
           <button @click="removeField(field)" class="btn btn-remove">Remove</button>
        </li>
      </ul>
      <button @click="getSelectedCitations('excel', 'citations.xlsx')">Get Excel Report</button>
      <button @click="getSelectedCitations('csv', 'citations.csv')">Get CSV Report</button>
      <button @click="getSelectedCitations('txt', 'citations.txt')">Get TXT Report</button>
    </div>
    <!-- data -->
    <div v-if="Array.isArray(citations) && citations.length">
      <div v-for="(citation, index) in citations" :key="citation._id" class="citation">
        <div v-if="editIndex === index">
          <EditCitation v-if="citation.edited" :item="citation.edited" :index="props.index" @save="saveEdit"
            @cancel="cancelEdit" type="Edit" :citationId="citation._id" />
          <EditCitation v-else :item="citation.citation" :index="props.index" @save="saveEdit" @cancel="cancelEdit"
            type="Edit" :citationId="citation._id" />
        </div>
        <div v-else>
          <CitationItem v-if="citation.edited" :citation="citation.edited" :index="index"
            :selectedCitations="selectedCitations" @startEdit="startEdit" :citationId="citation._id"
            :report-mode="reportMode" @toggleCitationSelection="toggleCitationSelection"></CitationItem>
          <CitationItem v-else :citation="citation.citation" :index="index" :selectedCitations="selectedCitations"
            @startEdit="startEdit" :citationId="citation._id" :report-mode="reportMode"
            @toggleCitationSelection="toggleCitationSelection"></CitationItem>
        </div>
      </div>
    </div>
    <div v-else-if="!isPendingRefresh">
      <p>No citations found.</p>
    </div>
  </div>
</template>

<style scoped>
p {
  font-size: 18px;
}

.citation {
  margin-bottom: 20px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.report-option {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.report-option input[type="radio"] {
  margin-right: 8px;
}

.year-input {
  width: 100px;
  margin-left: 8px;
}

button {
  margin-top: 8px;
  margin-right: 8px;
}

.input-custom {
  width: auto !important;
  margin: 0px !important;
}


.field-management {
  display: flex;
  align-items: center;
  margin-top: 10px;
}

.field-input {
  margin-right: 10px;
}

.field-list {
  list-style: none;
  padding: 0;
  margin: 10px 0;
}

.field-item {
  margin-bottom: 5px;
}



.data-summary {
  display: flex;
  justify-content: space-around;
  margin-bottom: 20px;
}

.card {
  background-color: #f9f9f9;
  padding: 10px;
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  text-align: center;
  width: 150px;
}

.card h4 {
  margin: 0 0 5px;
  font-size: 14px;
  color: #333;
}

.card .count {
  font-size: 18px;
  font-weight: bold;
  color: #14b8a6;
}


.field-list {
  list-style: none;
  padding: 0;
  margin: 10px 0;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.field-item {
  white-space: nowrap; 
  background-color: #14b8a6; 
  color: white;
  padding: 8px 12px;
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  font-weight: 500;
}
</style>
