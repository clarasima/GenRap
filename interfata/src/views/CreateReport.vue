<script setup>
import { ref, onMounted } from 'vue';
import PublicationList from '@/components/Publications/PublicationsList.vue';
import { useUser, getCSV, getUserFields } from '@/composables/getUser';

const data = ref([]);
const reportOption = ref('custom');
const isPendingRefresh = ref(false);
const selectedPublications = ref(new Set());
const startYear = ref('');
const endYear = ref('');
const newField = ref('');
const selectedFields = ref(['title', 'authors', 'year', 'category', 'indexed', 'type', 'impactFactor']);
const showFieldManager = ref(false);

// get data
onMounted(async () => {
    await loadData();
    await useUser("getUser");
    let userFields = await getUserFields();
    if (userFields?.length)
        selectedFields.value = await getUserFields();
});

async function loadData() {
    isPendingRefresh.value = true;
    const res = await useUser("getPublications");
    isPendingRefresh.value = false;
    data.value = res.filter(item => item.match !== false && item?.edited);
}

function deselectPublications() {
    selectedPublications.value.clear();
}

function selectPublications() {
    if (reportOption.value === 'year') {
        data.value.forEach(item => {
            const year = parseInt(item?.edited?.year);
            if (year === parseInt(startYear.value) && item?.edited) {
                selectedPublications.value.add(item._id);
            }
        });
    } else if (reportOption.value === 'interval') {
        const start = parseInt(startYear.value);
        const end = parseInt(endYear.value);
        data.value.forEach(item => {
            const year = parseInt(item?.edited?.year);
            if (year >= start && year <= end && item?.edited) {
                selectedPublications.value.add(item._id);
            }
        });
    }
}

function togglePublicationSelection(publicationId) {
    if (selectedPublications.value.has(publicationId)) {
        selectedPublications.value.delete(publicationId);
    } else {
        selectedPublications.value.add(publicationId);
    }
}

async function getSelectedPublications(format, name) {
    const selected = Array.from(selectedPublications.value);
    try {
        const urlReq = `http://localhost:5000/generate`
        const payload = {
            ids: selected,
            type: 'publications',
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

function setReportOption(str) {
    reportOption.value = str;
}

function addField() {
    if (newField.value && !selectedFields.value.includes(newField.value)) {
        selectedFields.value.push(newField.value);
        newField.value = "";
    }
}

function removeField(field) {
    const index = selectedFields.value.indexOf(field);
    if (index > -1) {
        selectedFields.value.splice(index, 1);
    }
}

function toggleFieldManager() {
    showFieldManager.value = !showFieldManager.value;
}

</script>

<template>
    <div v-if="isPendingRefresh">
        <div class="spinner"></div> Pending
    </div>
    <div v-else>
        <h3>Choose filter option</h3>
        <label class="report-option" @click="setReportOption('custom')">
            <input class="input-custom" type="radio" v-model="reportOption" value="custom"> Custom Selection
        </label>
        <label class="report-option" @click="setReportOption('year')">
            <input class="input-custom" type="radio" v-model="reportOption" value="year"> Select by Year
            <input type="number" v-model="startYear" placeholder="Year" class="year-input">
        </label>
        <label class="report-option" @click="setReportOption('interval')">
            <input class="input-custom" type="radio" v-model="reportOption" value="interval"> Select by Interval
            <input class="input-custom" type="number" v-model="startYear" placeholder="Start Year">
            <input class="input-custom" type="number" v-model="endYear" placeholder="End Year">
        </label>
        <p> <button @click="selectPublications">Select</button>
            <button @click="deselectPublications">Deselect all</button>
        </p>

        <h3>Manage Fields</h3>
        <button @click="toggleFieldManager">
            {{ showFieldManager ? 'Hide' : 'Show' }} Field Manager
        </button>
        <!-- <div v-show="!showFieldManager">Actual Fields: {{ selectedFields.join(',') }}</div> -->
        <ul v-show="!showFieldManager" class="field-list">
            <li v-for="field in selectedFields" :key="field" class="field-item">
                {{ field }}
            </li>
        </ul>
        <div v-show="showFieldManager">
            <div>
                <input v-model="newField" placeholder="New Field" />
                <button @click="addField"> Confirm Adding {{ newField }} in report</button>
            </div>
            <ul  class="field-list">
                <li v-for="field in selectedFields" :key="field">
                   <div class="field-item">
                    {{ field }} 
                   </div>
                    
                    <button @click="removeField(field)">Remove</button>
                </li>
            </ul>
        </div>

        <h3>Make Report</h3>
        <button @click="getSelectedPublications('excel', 'publications.xlsx')">Get Excel Report</button>
        <button @click="getSelectedPublications('csv', 'publications.csv')">Get CSV Report</button>
        <button @click="getSelectedPublications('txt', 'publications.txt')">Get TXT Report</button>
        <PublicationList :data="data" from="report" :selectedPublications="selectedPublications"
            @togglePublicationSelection="togglePublicationSelection" />
    </div>
</template>

<style scoped>
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

ul {
    list-style-type: none;
    padding: 0;
}

ul li {
    margin-bottom: 5px;
}


.field-list {
  list-style-type: none;
  padding: 0;
  margin: 10px 0;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.field-item {
  background-color: #14b8a6; /* Teal 500 */
  color: white;
  padding: 8px 12px;
  border-radius: 6px;
  font-weight: 500;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  white-space: nowrap; /* Prevents wrapping of text within the item */
}
</style>
