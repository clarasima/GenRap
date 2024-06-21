import { ref } from 'vue';
import axios from 'axios';
import { getUserId, getToken } from '@/composables/tokenManagement';

export function usePublicationEditor() {
  const editItem = ref({});
  const editIndex = ref(null);

  async function saveEdit() {
    // Logic to save edited publication
  }

  function cancelEdit() {
    editIndex.value = null;
    editItem.value = {};
  }

  return {
    editItem,
    saveEdit,
    cancelEdit
  };
}
