import { ref } from 'vue'
import axios from 'axios'
import { getToken, getUserId } from './tokenManagement'
import { updatePub } from '@/services/apiService'

export const error = ref(null)
export const errorPublication = ref(null)
export const publicationId = ref(null)
export const isPendingPublication = ref(null)
export const isPending = ref(false)
const user = ref(null)

const savedUser = localStorage.getItem('user_username')
const { token } = getToken()
if (savedUser) {
  user.value = savedUser
}

export const getUser = () => {
  return { user }
}
export const getUserValue = () => {
  return user.value
}
export const getUserName = () => {
  if (user.value) {
    return user.value.name
  }
}
export const getUserFields = () => {
  if (user.value.desiredFields) {
    let desiredFields = user.value.desiredFields

    // Check if desiredFields is not an array
    if (!Array.isArray(desiredFields)) {
      // Convert to array
      desiredFields = Object.values(desiredFields)
    }
    return desiredFields
  }
  return [] // Return an empty array if user.value is not defined
}

export const setUser = (newUser) => {
  user.value = newUser
}

export const removeUser = () => {
  localStorage.removeItem('user_username')
  user.value = null
}

async function getUserFromDB() {
  const url = `http://localhost:5000/user/${getUserId()}`
  try {
    const response = await axios.get(url, {
      headers: {
        'x-access-token': token.value,
        'Content-Type': 'application/json'
      }
    })
    return response.data
  } catch (error) {
    console.error('Error fetching user from DB:', error)
    throw error
  }
}

async function postRequest(url, requestBody) {
  try {
    const response = await axios.post(url, requestBody, {
      headers: {
        'x-access-token': getToken().token.value,
        'Content-Type': 'application/json'
      }
    })
    return response.data
  } catch (error) {
    console.error('Error fetching user from DB:', error)
    throw error
  }
}

async function getRequest(url) {
  try {
    const response = await axios.get(url, {
      headers: {
        'x-access-token': getToken().token.value,
        'Content-Type': 'application/json'
      }
    })
    return response.data
  } catch (error) {
    console.error('Error fetching user from DB:', error)
    throw error
  }
}

export async function getCSV(url, requestBody) {
  try {
    const response = await axios.post(url, requestBody, {
      headers: {
        'x-access-token': getToken().token.value,
        'Content-Type': 'application/json'
      },
      responseType: 'blob'
    })
    return response.data
  } catch (error) {
    console.error('Error fetching CSV', error)
    throw error
  }
}

export const useUser = async (typeData) => {
  error.value = null
  isPending.value = true
  try {
    let res
    if (typeData === 'getUser') {
      res = await getUserFromDB()
      setUser(res)
    } else if (typeData === 'refreshReportData') {
      const url = `http://localhost:5000/publications/user/${getUserId()}/refresh`
      res = await postRequest(url, {})
    } else if (typeData === 'getPublications') {
      const url = `http://localhost:5000/publications/user/${getUserId()}`
      res = await getRequest(url);
    }

    error.value = false
    isPending.value = false
    return res
  } catch (err) {
    console.error(err.message, err)
    error.value = 'Error fetching user data'
    if (err.message == 'Request failed with status code 404') {
      error.value = 'No documents found for this user in the database. Try refreshing the data.'
    }
    isPending.value = false
  }
}
export const updatePublication = async (requestBody) => {
  errorPublication.value = null
  isPendingPublication.value = true

  publicationId.value = requestBody.publicationId
  try {
    let res = await updatePub(requestBody);
    errorPublication.value = false
    isPendingPublication.value = false
    return res
  } catch (err) {
    console.error(err.message)
    errorPublication.value = 'Error fetching user data'
    isPendingPublication.value = false
  }
}

export const splitPublication = async (pubId) => {
  errorPublication.value = null
  isPendingPublication.value = true
  publicationId.value = pubId
  const url = `http://localhost:5000/publications/${pubId}/split`
  try {
    let res = await postRequest(url, {})
    errorPublication.value = false
    isPendingPublication.value = false
    return res
  } catch (err) {
    console.error(err.message)
    errorPublication.value = 'Error fetching user data'
    isPendingPublication.value = false
  }
}
