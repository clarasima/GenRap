import { ref } from 'vue'
import axios from 'axios'
import { setToken } from './tokenManagement'
const error = ref(null)
const isPending = ref(false)

async function signInWithUsernameAndPassword(username, password) {
  const url = 'http://localhost:5000/login'

  // Basic Auth: base64 encode the 'username:password' string
  const authHeader = 'Basic ' + btoa(`${username}:${password}`)

  try {
    const response = await axios.get(url, {
      headers: {
        Authorization: authHeader
      }
    })

    return response.data
  } catch (error) {
    console.error('Error during sign-in:', error)
    throw error
  }
}

const login = async (username, password) => {
  error.value = null
  isPending.value = true
  try {
    const res = await signInWithUsernameAndPassword(username, password)
    if (res.token) {
      setToken(res.token);
    }
    error.value = null
    isPending.value = false
    return res
  } catch (err) {
    console.error(err.message)
    error.value = 'Incorrect login credentials'
    isPending.value = false
  }
}

const useLogin = () => {
  return { error, login, isPending }
}

export default useLogin
