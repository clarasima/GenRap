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

  return {
    data,
    loadData
  };
}
