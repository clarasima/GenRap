import { ref } from 'vue';
import axios from 'axios';
import { getUserId, getToken } from '@/composables/tokenManagement';

export function usePublications() {
  const data = ref([]);
  const userId = getUserId();

  async function loadData() {
    try {
      const response = await axios.post('http://localhost:5000/get_publications', {
        userId
      }, {
        headers: {
          'x-access-token': getToken().token.value,
          'Content-Type': 'application/json'
        }
      });
      data.value = response.data;
    } catch (error) {
      console.error('Failed to load data:', error);
    }
  }

  function startEdit(index) {
    // Logic for starting edit
  }

  function confirmMatch(index, isMatch) {
    // Logic for confirming match
  }

  function selectSource(index, source) {
    // Logic for selecting source
  }

  function goToCitationsView(id) {
    // Logic for navigating to citations view
  }

  function togglePublicationSelection(publicationId) {
    // Logic for toggling publication selection
  }

  return {
    data,
    loadData,
    startEdit,
    confirmMatch,
    selectSource,
    goToCitationsView,
    togglePublicationSelection
  };
}
