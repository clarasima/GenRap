import { ref } from 'vue'
import axios from 'axios'
import { getToken, getUserId } from './tokenManagement'

export const error = ref(null)
export const isPending = ref(false)

export const fetchCitations = async (publicationId) => {
  try {
    error.value = null
    isPending.value = true
    const response = await axios.get(
      `http://localhost:5000/citations/${publicationId}`,
      {
        headers: {
          'x-access-token': getToken().token.value,
          'Content-Type': 'application/json'
        }
      }
    )
    error.value = false

    return response.data
  } catch (error) {
    error.value = error
    console.error('Failed to fetch citations:', error)
  } finally {
    isPending.value = false
  }
}

export const refreshCitations = async (publicationId) => {
  try {
    error.value = null
    isPending.value = true
    await axios.post(
      'http://localhost:5000/citations/refresh',
      {
        userId: getUserId(),
        publicationId
      },
      {
        headers: {
          'x-access-token': getToken().token.value,
          'Content-Type': 'application/json'
        }
      }
    )
    error.value = false
  } catch (error) {
    error.value = error
    console.error('Failed to refresh citations:', error)
  } finally {
    isPending.value = false
  }
}
export const getPublicationScholar = async (publicationId) => {
  try {
    error.value = null
    isPending.value = true
    const response = await axios.get(
      `http://localhost:5000/publications/${publicationId}/scholar`,
      {
        headers: {
          'x-access-token': getToken().token.value,
          'Content-Type': 'application/json'
        }
      }
    )
    error.value = false
    if(response.data.message){
      throw new Error(response.data.message)
    }
    return response.data.title
  } catch (error) {
    error.value = error
    console.error('Failed to refresh citations:', error)
  } finally {
    isPending.value = false
  }
}

export const updateCitation = async (requestBody) => {
  try {
    error.value = null
    isPending.value = true
    const response = await axios.post(
      'http://localhost:5000/citations/update',
      requestBody,
      {
        headers: {
          'x-access-token': getToken().token.value,
          'Content-Type': 'application/json'
        }
      }
    )
    error.value = false
    if(response.data.message){
      throw new Error(response.data.message)
    }
    return response.data.title
  } catch (error) {
    error.value = error
    console.error('Failed to refresh citations:', error)
  } finally {
    isPending.value = false
  }
}